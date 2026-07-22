#!/usr/bin/env python3
"""Validate TalkDirector recipes and optional v0.2 pipeline manifests."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


RECIPE_REQUIRED_FIELDS = {
    "recipe_schema_version",
    "recipe_id",
    "name",
    "status",
    "public_prompt",
    "triggers",
    "required_inputs",
    "asset_strategy",
    "layout_safe_zones",
    "timing_animation",
    "blocking_policies",
    "fallback_chain",
    "verification",
    "compatibility",
}
PIPELINE_REQUIRED_FIELDS = {
    "contract_version",
    "source",
    "transcript",
    "visual_beats",
    "edit_plan",
    "assets",
    "verification",
}
PLAN_STATES = (
    "intake",
    "draft",
    "first-approved",
    "representative-executed",
    "second-approved",
    "expanded",
)
EXECUTABLE_STATES = set(PLAN_STATES[2:])
POST_EXECUTION_STATES = set(PLAN_STATES[3:])
SECOND_APPROVAL_STATES = set(PLAN_STATES[4:])


class ValidationError(ValueError):
    """A deterministic contract violation."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def _read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValidationError(f"{path}: cannot read valid JSON: {error}") from error
    _require(isinstance(payload, dict), f"{path}: top level must be an object")
    return payload


def _first_text_fence(markdown: str) -> str:
    match = re.search(r"```text\s*\n(.*?)\n```", markdown, flags=re.DOTALL)
    _require(match is not None, "public Prompt source has no ```text code fence")
    return match.group(1).replace("\r\n", "\n").strip()


def _validate_rect(rect: Any, label: str) -> None:
    _require(isinstance(rect, list) and len(rect) == 4, f"{label}: rect must have 4 numbers")
    _require(all(isinstance(value, (int, float)) for value in rect), f"{label}: rect values must be numbers")
    x, y, width, height = rect
    _require(all(0 <= value <= 1 for value in rect), f"{label}: rect values must be normalized 0..1")
    _require(x + width <= 1 and y + height <= 1, f"{label}: rect exceeds the frame")


def _validate_time_range(time_range: Any, duration: float, label: str) -> None:
    _require(isinstance(time_range, dict), f"{label}: time_range must be an object")
    for field in ("start_seconds", "end_seconds", "confirmed_by_user"):
        _require(field in time_range, f"{label}: time_range missing {field}")
    start = time_range["start_seconds"]
    end = time_range["end_seconds"]
    _require(isinstance(start, (int, float)) and isinstance(end, (int, float)), f"{label}: time values must be numbers")
    _require(0 <= start < end <= duration, f"{label}: invalid or out-of-source time range {start}-{end}")
    _require(isinstance(time_range["confirmed_by_user"], bool), f"{label}: confirmed_by_user must be boolean")


def validate_recipe(recipe: dict[str, Any], path: Path, root: Path) -> None:
    missing = RECIPE_REQUIRED_FIELDS - recipe.keys()
    _require(not missing, f"{path}: missing recipe fields: {sorted(missing)}")
    _require(recipe["recipe_schema_version"] == "0.2", f"{path}: unsupported recipe schema version")
    _require(recipe["recipe_id"] == path.stem, f"{path}: recipe_id must match filename")
    _require(recipe["status"] in {"verified", "experimental"}, f"{path}: invalid status")
    _require(isinstance(recipe["public_prompt"], str) and recipe["public_prompt"].strip(), f"{path}: public_prompt is empty")

    triggers = recipe["triggers"]
    _require(isinstance(triggers, dict), f"{path}: triggers must be an object")
    for field in ("intent", "signals_any", "reject_when"):
        _require(field in triggers and triggers[field], f"{path}: triggers.{field} is required")

    inputs = recipe["required_inputs"]
    _require(isinstance(inputs, list) and inputs, f"{path}: required_inputs must be non-empty")
    input_ids = [item.get("id") for item in inputs if isinstance(item, dict)]
    _require(len(input_ids) == len(inputs) and len(set(input_ids)) == len(input_ids), f"{path}: required input IDs must be unique")
    for item in inputs:
        for field in ("id", "required_for", "description", "on_missing"):
            _require(item.get(field), f"{path}: required input {item.get('id')} missing {field}")

    assets = recipe["asset_strategy"]
    for field in ("required", "sources_in_order", "per_asset_inspection", "forbidden", "on_unverified"):
        _require(field in assets and assets[field] not in (None, [], ""), f"{path}: asset_strategy.{field} is required")
    _require(isinstance(assets["required"], bool), f"{path}: asset_strategy.required must be boolean")

    safe_zones = recipe["layout_safe_zones"]
    for field in ("protect", "placement_rule", "conflict_fallbacks"):
        _require(safe_zones.get(field), f"{path}: layout_safe_zones.{field} is required")

    timing = recipe["timing_animation"]
    for field in ("requires_confirmed_time_range", "trigger_alignment", "entry", "hold", "exit", "forbidden"):
        _require(field in timing and timing[field] not in (None, [], ""), f"{path}: timing_animation.{field} is required")
    _require(isinstance(timing["requires_confirmed_time_range"], bool), f"{path}: time requirement must be boolean")

    policies = recipe["blocking_policies"]
    for field in ("missing_time_range", "safe_zone_conflict"):
        _require(policies.get(field), f"{path}: blocking_policies.{field} is required")

    fallbacks = recipe["fallback_chain"]
    _require(isinstance(fallbacks, list) and len(fallbacks) >= 2, f"{path}: fallback_chain needs at least two steps")
    fallback_ids = [step.get("id") for step in fallbacks if isinstance(step, dict)]
    _require(len(fallback_ids) == len(fallbacks) and len(set(fallback_ids)) == len(fallback_ids), f"{path}: fallback IDs must be unique")
    for index, step in enumerate(fallbacks):
        for field in ("id", "when", "action", "terminal"):
            _require(field in step and step[field] not in (None, ""), f"{path}: fallback {index} missing {field}")
        _require(isinstance(step["terminal"], bool), f"{path}: fallback terminal must be boolean")
        _require(step["terminal"] is (index == len(fallbacks) - 1), f"{path}: only the final fallback may be terminal")

    verification = recipe["verification"]
    stages = verification.get("required_stages")
    checks = verification.get("checks")
    _require(isinstance(stages, list) and stages, f"{path}: verification.required_stages is required")
    _require(isinstance(checks, list) and checks, f"{path}: verification.checks is required")
    check_ids = [check.get("id") for check in checks]
    _require(len(check_ids) == len(set(check_ids)), f"{path}: verification check IDs must be unique")
    covered_stages = set()
    for check in checks:
        for field in ("id", "stage", "rule", "evidence_required"):
            _require(check.get(field), f"{path}: verification check missing {field}")
        covered_stages.add(check["stage"])
    _require(set(stages) <= covered_stages, f"{path}: required verification stage has no check")

    compatibility = recipe["compatibility"]
    prompt_source = root / compatibility.get("public_prompt_source", "")
    _require(prompt_source.is_file(), f"{path}: public Prompt source does not exist")
    published_prompt = _first_text_fence(prompt_source.read_text(encoding="utf-8"))
    recipe_prompt = recipe["public_prompt"].replace("\r\n", "\n").strip()
    _require(recipe_prompt == published_prompt, f"{path}: recipe public_prompt changed from published Prompt")
    legacy_reference = compatibility.get("legacy_reference")
    _require(legacy_reference and (root / legacy_reference).is_file(), f"{path}: legacy public path is missing")

    readme = (root / "README.md").read_text(encoding="utf-8")
    prompt_number = recipe["recipe_id"].split("-")[1]
    _require(f"Prompt {prompt_number}" in readme, f"{path}: README no longer exposes Prompt {prompt_number}")
    _require(legacy_reference in readme, f"{path}: README no longer links the legacy public path")
    if compatibility.get("readme_must_contain_public_prompt"):
        _require(recipe_prompt in readme, f"{path}: README public Prompt changed")
    readme_prompt_excerpt = compatibility.get("readme_prompt_excerpt")
    if readme_prompt_excerpt:
        _require(readme_prompt_excerpt in readme, f"{path}: README compatibility Prompt excerpt changed")


def load_and_validate_recipes(root: Path) -> dict[str, dict[str, Any]]:
    recipe_paths = sorted((root / "recipes").glob("*.json"))
    _require(recipe_paths, f"{root}: no recipes found")
    recipes: dict[str, dict[str, Any]] = {}
    for path in recipe_paths:
        recipe = _read_json(path)
        validate_recipe(recipe, path, root)
        recipe_id = recipe["recipe_id"]
        _require(recipe_id not in recipes, f"duplicate recipe_id: {recipe_id}")
        recipes[recipe_id] = recipe
    for legacy_id in ("prompt-001-gesture-logo-pop", "prompt-002-split-screen-explainer"):
        _require(legacy_id in recipes, f"compatibility recipe missing: {legacy_id}")
    return recipes


def validate_pipeline_manifest(
    manifest: dict[str, Any], recipes: dict[str, dict[str, Any]]
) -> None:
    missing = PIPELINE_REQUIRED_FIELDS - manifest.keys()
    _require(not missing, f"pipeline manifest missing fields: {sorted(missing)}")
    _require(manifest["contract_version"] == "0.2", "unsupported pipeline contract version")

    source = manifest["source"]
    for field in ("source_id", "kind", "aspect_ratio", "duration_seconds", "protected_regions"):
        _require(field in source, f"source missing {field}")
    duration = source["duration_seconds"]
    _require(isinstance(duration, (int, float)) and duration > 0, "source duration must be positive")
    _require(re.fullmatch(r"[1-9][0-9]*:[1-9][0-9]*", source["aspect_ratio"]) is not None, "source aspect_ratio must look like 16:9")
    for index, region in enumerate(source["protected_regions"]):
        _require(region.get("kind"), f"protected region {index} has no kind")
        _validate_rect(region.get("rect"), f"protected region {index}")

    transcript = manifest["transcript"]
    _require(transcript.get("status") in {"available", "missing"}, "transcript status is invalid")
    segments = transcript.get("segments")
    _require(isinstance(segments, list), "transcript segments must be a list")
    if transcript["status"] == "missing":
        _require(not segments, "missing transcript cannot contain segments")
    else:
        _require(segments, "available transcript must contain segments")
    segment_map: dict[str, dict[str, Any]] = {}
    for segment in segments:
        segment_id = segment.get("segment_id")
        _require(segment_id and segment_id not in segment_map, "transcript segment IDs must be unique")
        start = segment.get("start_seconds")
        end = segment.get("end_seconds")
        _require(isinstance(start, (int, float)) and isinstance(end, (int, float)), f"segment {segment_id}: times must be numbers")
        _require(0 <= start < end <= duration, f"segment {segment_id}: invalid time range")
        _require(isinstance(segment.get("text"), str) and segment["text"].strip(), f"segment {segment_id}: text is empty")
        segment_map[segment_id] = segment

    beats = manifest["visual_beats"]
    _require(isinstance(beats, list), "visual_beats must be a list")
    beat_map: dict[str, dict[str, Any]] = {}
    for beat in beats:
        beat_id = beat.get("beat_id")
        _require(beat_id and beat_id not in beat_map, "visual Beat IDs must be unique")
        recipe_id = beat.get("recipe_id")
        _require(recipe_id is None or recipe_id in recipes, f"beat {beat_id}: unknown recipe_id")
        segment_ids = beat.get("transcript_segment_ids")
        _require(isinstance(segment_ids, list) and segment_ids, f"beat {beat_id}: transcript references are required")
        _require(all(segment_id in segment_map for segment_id in segment_ids), f"beat {beat_id}: unknown transcript segment")
        source_text = " ".join(segment_map[segment_id]["text"] for segment_id in segment_ids)
        anchor = beat.get("anchor_text")
        _require(isinstance(anchor, str) and anchor.strip() and anchor in source_text, f"beat {beat_id}: anchor_text is not verbatim transcript text")
        _require(beat.get("purpose") in {"explain", "remember", "rhythm", "emotion", "transition"}, f"beat {beat_id}: invalid purpose")
        _require(beat.get("medium") in {"mg", "generated-video", "generated-image", "b-roll", "full-screen", "pip", "split-screen", "keep-clean"}, f"beat {beat_id}: invalid medium")
        _require(isinstance(beat.get("director_decision"), str) and beat["director_decision"].strip(), f"beat {beat_id}: director_decision is required")
        _validate_time_range(beat.get("time_range"), duration, f"beat {beat_id}")
        _require(isinstance(beat.get("asset_ids"), list), f"beat {beat_id}: asset_ids must be a list")
        beat_map[beat_id] = beat

    edit_plan = manifest["edit_plan"]
    state = edit_plan.get("state")
    _require(state in PLAN_STATES, "edit_plan state is invalid")
    representative_id = edit_plan.get("representative_beat_id")
    approved_ids = edit_plan.get("approved_beat_ids")
    _require(isinstance(approved_ids, list) and len(approved_ids) == len(set(approved_ids)), "approved Beat IDs must be a unique list")
    _require(all(beat_id in beat_map for beat_id in approved_ids), "edit_plan approves an unknown Beat")
    approvals = edit_plan.get("approval_evidence")
    _require(isinstance(approvals, dict) and {"first", "second"} <= approvals.keys(), "approval_evidence needs first and second fields")

    if state == "intake":
        _require(transcript["status"] == "missing", "intake state requires a missing transcript")
        _require(not beats and representative_id is None and not approved_ids, "intake state cannot invent or approve Beats")
    else:
        _require(transcript["status"] == "available", f"{state} state requires an available transcript")
        _require(beats and representative_id in beat_map, f"{state} state needs exactly one valid representative Beat")

    if state in EXECUTABLE_STATES:
        _require(isinstance(approvals["first"], str) and approvals["first"].strip(), f"{state} state requires first-approval evidence")
        _require(approved_ids == [representative_id] or state in SECOND_APPROVAL_STATES, "before second approval only the representative Beat may be approved")
        representative = beat_map[representative_id]
        recipe_id = representative.get("recipe_id")
        if recipe_id and recipes[recipe_id]["timing_animation"]["requires_confirmed_time_range"]:
            _require(representative["time_range"]["confirmed_by_user"], "representative Beat needs a user-confirmed time range")

    asset_map: dict[str, dict[str, Any]] = {}
    for asset in manifest["assets"]:
        asset_id = asset.get("asset_id")
        _require(asset_id and asset_id not in asset_map, "asset IDs must be unique")
        for field in ("kind", "source_type", "verification_status", "responsibility"):
            _require(asset.get(field), f"asset {asset_id}: missing {field}")
        _require(asset["verification_status"] in {"pending", "verified", "rejected"}, f"asset {asset_id}: invalid verification status")
        asset_map[asset_id] = asset
    for beat in beats:
        _require(all(asset_id in asset_map for asset_id in beat["asset_ids"]), f"beat {beat['beat_id']}: unknown asset")
        if state in EXECUTABLE_STATES and beat["beat_id"] in approved_ids and beat.get("recipe_id"):
            recipe = recipes[beat["recipe_id"]]
            if recipe["asset_strategy"]["required"]:
                _require(beat["asset_ids"], f"beat {beat['beat_id']}: recipe requires verified assets")
                _require(all(asset_map[asset_id]["verification_status"] == "verified" for asset_id in beat["asset_ids"]), f"beat {beat['beat_id']}: all required assets must be verified")

    checks = manifest["verification"].get("checks")
    _require(isinstance(checks, list), "verification checks must be a list")
    check_ids: set[str] = set()
    for check in checks:
        check_id = check.get("check_id")
        _require(check_id and check_id not in check_ids, "verification check IDs must be unique")
        check_ids.add(check_id)
        _require(check.get("beat_id") in beat_map, f"verification check {check_id}: unknown Beat")
        _require(check.get("stage") in {"asset", "beginning", "middle", "ending"}, f"verification check {check_id}: invalid stage")
        _require(check.get("status") in {"pending", "pass", "fail"}, f"verification check {check_id}: invalid status")
        _require(isinstance(check.get("evidence"), list), f"verification check {check_id}: evidence must be a list")

    if state in POST_EXECUTION_STATES:
        representative = beat_map[representative_id]
        recipe = recipes.get(representative.get("recipe_id"))
        required_stages = set(recipe["verification"]["required_stages"] if recipe else ("beginning", "middle", "ending"))
        passing_stages = {
            check["stage"]
            for check in checks
            if check["beat_id"] == representative_id
            and check["status"] == "pass"
            and check["evidence"]
        }
        _require(required_stages <= passing_stages, "representative Beat lacks passing verification evidence for every required stage")

    if state in SECOND_APPROVAL_STATES:
        _require(isinstance(approvals["second"], str) and approvals["second"].strip(), f"{state} state requires second-approval evidence")


def validate_repository(root: Path, manifest_path: Path | None = None) -> dict[str, dict[str, Any]]:
    root = root.resolve()
    schema_path = root / "schemas" / "talkdirector-pipeline.schema.json"
    schema = _read_json(schema_path)
    _require(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", "pipeline schema must declare JSON Schema 2020-12")
    recipes = load_and_validate_recipes(root)
    if manifest_path is not None:
        manifest = _read_json(manifest_path)
        validate_pipeline_manifest(manifest, recipes)
    return recipes


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()
    recipes = validate_repository(args.root, args.manifest)
    suffix = f" and {args.manifest}" if args.manifest else ""
    print(f"Validated {len(recipes)} TalkDirector recipes{suffix}")


if __name__ == "__main__":
    main()
