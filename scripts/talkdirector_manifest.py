#!/usr/bin/env python3
"""Initialize, recover, and gate CutDirector's internal project manifest."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any

try:
    from validate_talkdirector import (
        ValidationError,
        execution_blockers,
        load_and_validate_recipes,
        validate_pipeline_manifest,
    )
except ModuleNotFoundError:  # Imported as scripts.talkdirector_manifest in tests.
    from scripts.validate_talkdirector import (
        ValidationError,
        execution_blockers,
        load_and_validate_recipes,
        validate_pipeline_manifest,
    )


ROOT = Path(__file__).resolve().parents[1]
IDENTITY_KEYS = ("segment_id", "beat_id", "asset_id", "check_id")
STATUS_RANKS = {
    "missing": 0, "available": 1,
    "pending": 0, "blocked": 1, "rejected": 1, "fail": 1,
    "verified": 2, "pass": 2,
}


def _slug(source_id: str) -> str:
    readable = re.sub(r"[^A-Za-z0-9._-]+", "-", source_id).strip(".-")[:48] or "source"
    digest = hashlib.sha256(source_id.encode("utf-8")).hexdigest()[:10]
    return f"{readable}-{digest}"


def manifest_path(cache_root: Path, source_id: str) -> Path:
    return cache_root.resolve() / _slug(source_id) / "manifest.json"


def _write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(rendered, encoding="utf-8")
    os.replace(temporary, path)


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValidationError(f"{path}: JSON top level must be an object")
    return payload


def _identity_key(items: list[Any]) -> str | None:
    dictionaries = [item for item in items if isinstance(item, dict)]
    for key in IDENTITY_KEYS:
        if dictionaries and all(key in item for item in dictionaries):
            return key
    return None


def merge_preserving_confirmed(existing: Any, incoming: Any, field: str = "") -> Any:
    """Merge new facts without replacing non-empty human/model decisions."""
    if incoming is None:
        return copy.deepcopy(existing)
    if existing is None or existing == "":
        return copy.deepcopy(incoming)
    if (
        field == "time_range"
        and isinstance(existing, dict)
        and isinstance(incoming, dict)
        and existing.get("confirmed_by_user") is False
        and incoming.get("confirmed_by_user") is True
    ):
        return copy.deepcopy(incoming)
    if isinstance(existing, dict) and isinstance(incoming, dict):
        result = copy.deepcopy(existing)
        for key, value in incoming.items():
            if key == "state":
                continue
            result[key] = merge_preserving_confirmed(result.get(key), value, key)
        return result
    if isinstance(existing, list) and isinstance(incoming, list):
        if not existing:
            return copy.deepcopy(incoming)
        key = _identity_key(existing + incoming)
        if key:
            result = copy.deepcopy(existing)
            positions = {item[key]: index for index, item in enumerate(result)}
            for item in incoming:
                if item[key] in positions:
                    index = positions[item[key]]
                    result[index] = merge_preserving_confirmed(result[index], item)
                else:
                    positions[item[key]] = len(result)
                    result.append(copy.deepcopy(item))
            return result
        result = copy.deepcopy(existing)
        for item in incoming:
            if item not in result:
                result.append(copy.deepcopy(item))
        return result
    if field == "confirmed_by_user" and existing is False and incoming is True:
        return True
    if field in {"status", "verification_status"}:
        if STATUS_RANKS.get(str(incoming), -1) > STATUS_RANKS.get(str(existing), -1):
            return copy.deepcopy(incoming)
    return copy.deepcopy(existing)


def new_manifest(source_id: str, source_kind: str, recipe: dict[str, Any]) -> dict[str, Any]:
    gates = {
        name: {"status": "pending", "evidence": []}
        for name in recipe["execution_gates"]
    }
    return {
        "contract_version": "0.2",
        "source": {
            "source_id": source_id,
            "kind": source_kind,
            "aspect_ratio": None,
            "duration_seconds": None,
            "protected_regions": [],
        },
        "transcript": {"status": "missing", "segments": []},
        "visual_beats": [],
        "edit_plan": {
            "state": "planned",
            "recipe_id": recipe["recipe_id"],
            "representative_beat_id": None,
            "approved_beat_ids": [],
            "gates": gates,
            "blockers": [],
            "approval_evidence": {"first": None, "second": None},
            "write_intent": None,
        },
        "assets": [],
        "verification": {"checks": []},
    }


def initialize(cache_root: Path, source_id: str, source_kind: str, recipe_id: str, recipes: dict[str, dict[str, Any]]) -> Path:
    if recipe_id not in recipes:
        raise ValidationError(f"unknown recipe_id: {recipe_id}")
    path = manifest_path(cache_root, source_id)
    if path.exists():
        manifest = _read_json(path)
        if manifest["source"]["source_id"] != source_id:
            raise ValidationError("cache source identity mismatch")
        if manifest["edit_plan"]["recipe_id"] != recipe_id:
            raise ValidationError("existing cache uses another recipe; create a separate source/project ID")
    else:
        manifest = new_manifest(source_id, source_kind, recipes[recipe_id])
    validate_pipeline_manifest(manifest, recipes)
    _write_json_atomic(path, manifest)
    return path


def build(path: Path, facts: dict[str, Any], recipes: dict[str, dict[str, Any]]) -> dict[str, Any]:
    current = _read_json(path)
    if facts.get("source", {}).get("source_id") not in (None, current["source"]["source_id"]):
        raise ValidationError("facts source_id does not match cache")
    merged = merge_preserving_confirmed(current, facts)
    state = current["edit_plan"]["state"]
    if state in {"planned", "blocked", "ready"}:
        blockers = execution_blockers(merged, recipes)
        merged["edit_plan"]["blockers"] = blockers
        merged["edit_plan"]["state"] = "blocked" if blockers else "ready"
        merged["edit_plan"]["write_intent"] = None
    elif state in {"executing", "verified"}:
        merged["edit_plan"]["state"] = state
    validate_pipeline_manifest(merged, recipes)
    _write_json_atomic(path, merged)
    return merged


def transition(path: Path, target: str, operation_id: str | None, scope: str, recipes: dict[str, dict[str, Any]]) -> dict[str, Any]:
    manifest = _read_json(path)
    current = manifest["edit_plan"]["state"]
    if target == "executing":
        if current != "ready":
            raise ValidationError("only a ready manifest may enter executing")
        validate_pipeline_manifest(manifest, recipes)
        if not operation_id or not operation_id.strip():
            raise ValidationError("executing transition requires an operation_id")
        if scope == "expanded" and not manifest["edit_plan"]["approval_evidence"].get("second"):
            raise ValidationError("expanded execution requires second-approval evidence")
        manifest["edit_plan"]["write_intent"] = {"operation_id": operation_id, "scope": scope}
        manifest["edit_plan"]["state"] = "executing"
    elif target == "verified":
        if current != "executing":
            raise ValidationError("only an executing manifest may enter verified")
        manifest["edit_plan"]["state"] = "verified"
    else:
        raise ValidationError(f"unsupported transition target: {target}")
    validate_pipeline_manifest(manifest, recipes)
    _write_json_atomic(path, manifest)
    return manifest


def create_recipe_draft(cache_root: Path, recipe_id: str) -> Path:
    if not re.fullmatch(r"prompt-[0-9]{3}-[a-z0-9-]+", recipe_id):
        raise ValidationError("recipe_id must look like prompt-003-short-name")
    path = cache_root.resolve() / "recipe-drafts" / f"{recipe_id}.json"
    if path.exists():
        return path
    draft = {
        "recipe_schema_version": "0.2",
        "recipe_id": recipe_id,
        "status": "draft-template",
        "name": "",
        "public_prompt": "",
        "triggers": {},
        "required_inputs": [],
        "asset_strategy": {},
        "layout_safe_zones": {},
        "timing_animation": {},
        "blocking_policies": {},
        "execution_gates": [],
        "fallback_chain": [],
        "verification": {},
        "compatibility": {},
    }
    _write_json_atomic(path, draft)
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--cache-root", type=Path)
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init")
    init_parser.add_argument("--source-id", required=True)
    init_parser.add_argument("--source-kind", choices=("chatcut-project", "media-file", "external-context"), default="chatcut-project")
    init_parser.add_argument("--recipe-id", required=True)

    build_parser = subparsers.add_parser("build")
    build_parser.add_argument("--source-id", required=True)
    build_parser.add_argument("--facts", type=Path, required=True)

    transition_parser = subparsers.add_parser("transition")
    transition_parser.add_argument("--source-id", required=True)
    transition_parser.add_argument("--to", choices=("executing", "verified"), required=True)
    transition_parser.add_argument("--operation-id")
    transition_parser.add_argument("--scope", choices=("representative", "expanded"), default="representative")

    draft_parser = subparsers.add_parser("new-recipe")
    draft_parser.add_argument("--recipe-id", required=True)

    args = parser.parse_args()
    root = args.root.resolve()
    cache_root = (args.cache_root or root / ".talkdirector").resolve()
    recipes = load_and_validate_recipes(root)
    if args.command == "init":
        path = initialize(cache_root, args.source_id, args.source_kind, args.recipe_id, recipes)
    elif args.command == "build":
        path = manifest_path(cache_root, args.source_id)
        build(path, _read_json(args.facts), recipes)
    elif args.command == "transition":
        path = manifest_path(cache_root, args.source_id)
        transition(path, args.to, args.operation_id, args.scope, recipes)
    else:
        path = create_recipe_draft(cache_root, args.recipe_id)
    print(path)


if __name__ == "__main__":
    main()
