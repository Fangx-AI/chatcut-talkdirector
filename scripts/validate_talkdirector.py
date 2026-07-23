#!/usr/bin/env python3
"""Deterministically validate CutDirector recipes and pipeline manifests."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


RECIPE_REQUIRED_FIELDS = {
    "recipe_schema_version", "recipe_id", "name", "status", "public_prompt",
    "triggers", "required_inputs", "asset_strategy", "layout_safe_zones",
    "timing_animation", "blocking_policies", "execution_gates",
    "fallback_chain", "verification", "compatibility",
}
PIPELINE_REQUIRED_FIELDS = {
    "contract_version", "source", "transcript", "visual_beats", "edit_plan",
    "assets", "verification",
}
PLAN_STATES = ("planned", "blocked", "ready", "executing", "verified")
GATE_NAMES = {"time", "gesture", "assets", "copy", "safe_zones", "first_approval"}


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
    _require(all(isinstance(value, (int, float)) and not isinstance(value, bool) for value in rect), f"{label}: rect values must be numbers")
    x, y, width, height = rect
    _require(all(0 <= value <= 1 for value in rect), f"{label}: rect values must be normalized 0..1")
    _require(x + width <= 1 and y + height <= 1, f"{label}: rect exceeds the frame")


def _valid_time_range(time_range: Any, duration: float | None) -> bool:
    if not isinstance(time_range, dict):
        return False
    if not {"start_seconds", "end_seconds", "confirmed_by_user"} <= time_range.keys():
        return False
    start, end = time_range["start_seconds"], time_range["end_seconds"]
    if not isinstance(start, (int, float)) or isinstance(start, bool):
        return False
    if not isinstance(end, (int, float)) or isinstance(end, bool):
        return False
    return 0 <= start < end and (duration is None or end <= duration) and isinstance(time_range["confirmed_by_user"], bool)


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

    gates = recipe["execution_gates"]
    _require(isinstance(gates, list) and gates, f"{path}: execution_gates must be non-empty")
    _require(len(gates) == len(set(gates)) and set(gates) <= GATE_NAMES, f"{path}: execution_gates are invalid")

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
    stages, checks = verification.get("required_stages"), verification.get("checks")
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
    excerpt = compatibility.get("readme_prompt_excerpt")
    if excerpt:
        _require(excerpt in readme, f"{path}: README compatibility Prompt excerpt changed")


def load_and_validate_recipes(root: Path) -> dict[str, dict[str, Any]]:
    recipe_paths = sorted((root / "recipes").glob("*.json"))
    _require(recipe_paths, f"{root}: no recipes found")
    recipes: dict[str, dict[str, Any]] = {}
    for path in recipe_paths:
        recipe = _read_json(path)
        validate_recipe(recipe, path, root)
        _require(recipe["recipe_id"] not in recipes, f"duplicate recipe_id: {recipe['recipe_id']}")
        recipes[recipe["recipe_id"]] = recipe
    for legacy_id in (
        "prompt-001-gesture-logo-pop",
        "prompt-002-split-screen-explainer",
        "prompt-003-brand-mode-comparison",
    ):
        _require(legacy_id in recipes, f"compatibility recipe missing: {legacy_id}")
    return recipes


def _blocker(code: str, message: str, resolution: str) -> dict[str, str]:
    return {"code": code, "message": message, "resolution": resolution}


def execution_blockers(manifest: dict[str, Any], recipes: dict[str, dict[str, Any]]) -> list[dict[str, str]]:
    """Return deterministic reasons the manifest cannot enter ready/executing."""
    source, transcript, plan = manifest["source"], manifest["transcript"], manifest["edit_plan"]
    recipe = recipes[plan["recipe_id"]]
    blockers: list[dict[str, str]] = []
    duration = source.get("duration_seconds")
    if not isinstance(duration, (int, float)) or isinstance(duration, bool) or duration <= 0:
        blockers.append(_blocker("source-duration", "Source duration is unknown.", "Inspect the source duration."))
    if not isinstance(source.get("aspect_ratio"), str):
        blockers.append(_blocker("source-aspect", "Source aspect ratio is unknown.", "Inspect the source frame."))
    if transcript.get("status") != "available" or not transcript.get("segments"):
        blockers.append(_blocker("transcript", "Transcript context is unavailable.", "Read or create a source transcript."))

    beat_id = plan.get("representative_beat_id")
    beat = next((item for item in manifest["visual_beats"] if item.get("beat_id") == beat_id), None)
    if beat is None:
        blockers.append(_blocker("representative-beat", "No representative Beat is selected.", "Plan one representative Beat."))
    else:
        if beat.get("recipe_id") != recipe["recipe_id"]:
            blockers.append(_blocker("recipe-match", "Representative Beat does not use the selected recipe.", "Use one matching recipe."))
        if not _valid_time_range(beat.get("time_range"), duration if isinstance(duration, (int, float)) else None):
            blockers.append(_blocker("time-range", "The exact time range is missing or invalid.", "Inspect and confirm an exact source range."))
        elif recipe["timing_animation"]["requires_confirmed_time_range"] and not beat["time_range"]["confirmed_by_user"]:
            blockers.append(_blocker("time-confirmation", "The exact time range is not user-confirmed.", "Ask the user to confirm the exact range."))
        if not beat.get("transcript_segment_ids") or not beat.get("anchor_text") or not beat.get("director_decision"):
            blockers.append(_blocker("beat-content", "The representative Beat lacks source-grounded content.", "Complete the verbatim anchor and director decision."))

    for gate_name in recipe["execution_gates"]:
        gate = plan.get("gates", {}).get(gate_name)
        if not isinstance(gate, dict) or gate.get("status") != "pass" or not gate.get("evidence"):
            blockers.append(_blocker(f"gate-{gate_name}", f"The {gate_name} gate has not passed.", "Resolve and record evidence for this gate."))

    if not isinstance(plan.get("approval_evidence", {}).get("first"), str) or not plan["approval_evidence"]["first"].strip():
        blockers.append(_blocker("first-approval", "First approval evidence is missing.", "Obtain approval for the representative Beat."))
    if beat_id is not None and plan.get("approved_beat_ids") != [beat_id]:
        blockers.append(_blocker("approved-beat", "Only the representative Beat may be approved before expansion.", "Approve exactly the representative Beat."))

    if beat is not None and recipe["asset_strategy"]["required"]:
        asset_map = {asset.get("asset_id"): asset for asset in manifest["assets"]}
        asset_ids = beat.get("asset_ids", [])
        if not asset_ids or any(asset_map.get(asset_id, {}).get("verification_status") != "verified" for asset_id in asset_ids):
            blockers.append(_blocker("verified-assets", "Required official assets are not verified.", "Verify each official asset and provenance."))

    if not source.get("protected_regions"):
        blockers.append(_blocker("safe-zones", "Protected regions have not been measured.", "Inspect captions, speaker, gestures, and existing graphics."))

    params = beat.get("parameters", {}) if beat else {}
    if recipe["recipe_id"] == "prompt-001-gesture-logo-pop":
        brands = params.get("brands")
        if not isinstance(brands, list) or not brands or any(not item.get("name") or not item.get("asset_id") for item in brands if isinstance(item, dict)) or any(not isinstance(item, dict) for item in brands or []):
            blockers.append(_blocker("brand-mapping", "Brand names and verified assets are not mapped.", "Map every named brand to its verified official asset."))
    elif recipe["recipe_id"] == "prompt-002-split-screen-explainer":
        if not isinstance(params.get("title"), str) or not params.get("title", "").strip():
            blockers.append(_blocker("split-title", "The verbatim title is missing.", "Record the user-provided title."))
        points = params.get("points")
        if not isinstance(points, list) or not 3 <= len(points) <= 5 or any(not isinstance(point, str) or not point.strip() for point in points or []):
            blockers.append(_blocker("split-points", "Three to five verbatim points are required.", "Record 3-5 points in narration order."))
        if not isinstance(params.get("long_text"), str) or not params.get("long_text", "").strip():
            blockers.append(_blocker("split-long-text", "The verbatim long text is missing.", "Record the complete source text."))
        ratio = params.get("right_column_ratio")
        if not isinstance(ratio, (int, float)) or isinstance(ratio, bool) or not 0 < ratio <= 0.45:
            blockers.append(_blocker("split-ratio", "The right column exceeds or lacks its 45% limit.", "Set a readable ratio no greater than 0.45."))
        if params.get("scroll_to_end_required") is not False:
            blockers.append(_blocker("split-scroll-end", "The plan incorrectly requires the full text to finish.", "Allow partial display at a comfortable constant speed."))
        if params.get("scroll_speed_policy") != "constant-comfortable":
            blockers.append(_blocker("split-scroll-speed", "The scroll policy may accelerate or jump.", "Use constant-comfortable scrolling."))
        protected = {region.get("kind") for region in source.get("protected_regions", [])}
        if "captions" not in protected or not ({"speaker", "person"} & protected):
            blockers.append(_blocker("split-safe-regions", "Caption and speaker safe zones are not both recorded.", "Measure captions and the required speaker/person region."))
    elif recipe["recipe_id"] == "prompt-003-brand-mode-comparison":
        for field, code, message in (
            ("brand_name", "mode-brand", "The exact brand identity is missing."),
            ("mode_a_title", "mode-a-title", "Mode A title is missing."),
            ("mode_a_capability", "mode-a-capability", "Mode A needs exactly one core capability."),
            ("mode_b_title", "mode-b-title", "Mode B title is missing."),
            ("final_left", "mode-final-left", "The left side of the final comparison is missing."),
            ("final_right", "mode-final-right", "The right side of the final comparison is missing."),
            ("summary_line", "mode-summary", "The final summary line is missing."),
        ):
            if not isinstance(params.get(field), str) or not params.get(field, "").strip():
                blockers.append(_blocker(code, message, f"Record a verbatim {field} value."))
        mode_b_capabilities = params.get("mode_b_capabilities")
        if (
            not isinstance(mode_b_capabilities, list)
            or not 2 <= len(mode_b_capabilities) <= 4
            or any(not isinstance(item, str) or not item.strip() for item in mode_b_capabilities or [])
        ):
            blockers.append(_blocker("mode-b-capabilities", "Mode B requires two to four verbatim capabilities.", "Record 2-4 short capabilities in narration order."))
        if params.get("icon_persists_between_stages") is not True:
            blockers.append(_blocker("mode-icon-continuity", "The brand icon is not guaranteed to persist between stages.", "Keep one icon stable across the body-to-conclusion transition."))
        if params.get("background_color") != "#000000":
            blockers.append(_blocker("mode-black-background", "The verified recipe requires a pure black background.", "Set background_color to #000000."))
        if params.get("sound_profile") != "light-tight":
            blockers.append(_blocker("mode-sound-profile", "The sound design may be heavy or muddy.", "Use the light-tight sound profile."))
        if params.get("export_first_frame_check") is not True:
            blockers.append(_blocker("mode-export-boundary", "The exported first-frame check is not enabled.", "Inspect the actual first frame of the partial export."))

    unique: dict[str, dict[str, str]] = {}
    for item in blockers:
        unique.setdefault(item["code"], item)
    return list(unique.values())


def validate_pipeline_manifest(manifest: dict[str, Any], recipes: dict[str, dict[str, Any]]) -> None:
    missing = PIPELINE_REQUIRED_FIELDS - manifest.keys()
    _require(not missing, f"pipeline manifest missing fields: {sorted(missing)}")
    _require(manifest["contract_version"] == "0.2", "unsupported pipeline contract version")

    source = manifest["source"]
    for field in ("source_id", "kind", "aspect_ratio", "duration_seconds", "protected_regions"):
        _require(field in source, f"source missing {field}")
    _require(isinstance(source["source_id"], str) and source["source_id"].strip(), "source_id is required")
    _require(source["kind"] in {"chatcut-project", "media-file", "external-context"}, "source kind is invalid")
    duration = source["duration_seconds"]
    _require(duration is None or (isinstance(duration, (int, float)) and not isinstance(duration, bool) and duration > 0), "source duration must be null or positive")
    aspect = source["aspect_ratio"]
    _require(aspect is None or (isinstance(aspect, str) and re.fullmatch(r"[1-9][0-9]*:[1-9][0-9]*", aspect)), "source aspect_ratio must be null or look like 16:9")
    _require(isinstance(source["protected_regions"], list), "protected_regions must be a list")
    for index, region in enumerate(source["protected_regions"]):
        _require(isinstance(region, dict) and region.get("kind"), f"protected region {index} has no kind")
        _validate_rect(region.get("rect"), f"protected region {index}")

    transcript = manifest["transcript"]
    _require(transcript.get("status") in {"available", "missing"}, "transcript status is invalid")
    segments = transcript.get("segments")
    _require(isinstance(segments, list), "transcript segments must be a list")
    _require(transcript["status"] != "missing" or not segments, "missing transcript cannot contain segments")
    _require(transcript["status"] != "available" or segments, "available transcript must contain segments")
    segment_map: dict[str, dict[str, Any]] = {}
    for segment in segments:
        segment_id = segment.get("segment_id")
        _require(segment_id and segment_id not in segment_map, "transcript segment IDs must be unique")
        start, end = segment.get("start_seconds"), segment.get("end_seconds")
        _require(isinstance(start, (int, float)) and isinstance(end, (int, float)) and 0 <= start < end, f"segment {segment_id}: invalid time range")
        _require(duration is None or end <= duration, f"segment {segment_id}: outside source duration")
        _require(isinstance(segment.get("text"), str) and segment["text"].strip(), f"segment {segment_id}: text is empty")
        segment_map[segment_id] = segment

    beats = manifest["visual_beats"]
    _require(isinstance(beats, list), "visual_beats must be a list")
    beat_map: dict[str, dict[str, Any]] = {}
    for beat in beats:
        beat_id = beat.get("beat_id")
        _require(beat_id and beat_id not in beat_map, "visual Beat IDs must be unique")
        _require(beat.get("recipe_id") is None or beat.get("recipe_id") in recipes, f"beat {beat_id}: unknown recipe_id")
        _require(isinstance(beat.get("transcript_segment_ids"), list), f"beat {beat_id}: transcript references must be a list")
        _require(all(item in segment_map for item in beat["transcript_segment_ids"]), f"beat {beat_id}: unknown transcript segment")
        anchor = beat.get("anchor_text")
        if anchor is not None:
            source_text = " ".join(segment_map[item]["text"] for item in beat["transcript_segment_ids"])
            _require(isinstance(anchor, str) and anchor.strip() and anchor in source_text, f"beat {beat_id}: anchor_text is not verbatim transcript text")
        _require(beat.get("purpose") in {None, "explain", "remember", "rhythm", "emotion", "transition"}, f"beat {beat_id}: invalid purpose")
        _require(beat.get("medium") in {None, "mg", "generated-video", "generated-image", "b-roll", "full-screen", "pip", "split-screen", "keep-clean"}, f"beat {beat_id}: invalid medium")
        _require(beat.get("director_decision") is None or (isinstance(beat["director_decision"], str) and beat["director_decision"].strip()), f"beat {beat_id}: invalid director_decision")
        _require(beat.get("time_range") is None or _valid_time_range(beat["time_range"], duration), f"beat {beat_id}: invalid time range")
        _require(isinstance(beat.get("parameters"), dict), f"beat {beat_id}: parameters must be an object")
        _require(isinstance(beat.get("asset_ids"), list), f"beat {beat_id}: asset_ids must be a list")
        beat_map[beat_id] = beat

    plan = manifest["edit_plan"]
    _require(plan.get("state") in PLAN_STATES, "edit_plan state is invalid")
    recipe_id = plan.get("recipe_id")
    _require(recipe_id in recipes, "edit_plan recipe_id is invalid")
    recipe = recipes[recipe_id]
    _require(isinstance(plan.get("approved_beat_ids"), list) and len(plan["approved_beat_ids"]) == len(set(plan["approved_beat_ids"])), "approved Beat IDs must be unique")
    _require(all(item in beat_map for item in plan["approved_beat_ids"]), "edit_plan approves an unknown Beat")
    _require(isinstance(plan.get("approval_evidence"), dict) and {"first", "second"} <= plan["approval_evidence"].keys(), "approval_evidence needs first and second")
    _require(isinstance(plan.get("gates"), dict), "gates must be an object")
    _require(set(recipe["execution_gates"]) <= plan["gates"].keys(), "recipe execution gates are missing")
    for name, gate in plan["gates"].items():
        _require(name in GATE_NAMES and isinstance(gate, dict), f"gate {name} is invalid")
        _require(gate.get("status") in {"pending", "blocked", "pass"} and isinstance(gate.get("evidence"), list), f"gate {name} is invalid")
        _require(gate["status"] != "pass" or gate["evidence"], f"gate {name}: passing gate needs evidence")
    _require(isinstance(plan.get("blockers"), list), "blockers must be a list")
    for item in plan["blockers"]:
        _require(isinstance(item, dict) and all(isinstance(item.get(field), str) and item[field].strip() for field in ("code", "message", "resolution")), "blocker is invalid")
    intent = plan.get("write_intent")
    _require(intent is None or (isinstance(intent, dict) and isinstance(intent.get("operation_id"), str) and intent["operation_id"].strip() and intent.get("scope") in {"representative", "expanded"}), "write_intent is invalid")
    if intent is not None and intent["scope"] == "expanded":
        second = plan["approval_evidence"].get("second")
        _require(isinstance(second, str) and second.strip(), "expanded write intent requires second-approval evidence")

    asset_map: dict[str, dict[str, Any]] = {}
    _require(isinstance(manifest["assets"], list), "assets must be a list")
    for asset in manifest["assets"]:
        asset_id = asset.get("asset_id")
        _require(asset_id and asset_id not in asset_map, "asset IDs must be unique")
        for field in ("kind", "source_type", "verification_status", "responsibility"):
            _require(asset.get(field), f"asset {asset_id}: missing {field}")
        _require(asset["verification_status"] in {"pending", "verified", "rejected"}, f"asset {asset_id}: invalid verification status")
        asset_map[asset_id] = asset
    for beat in beats:
        _require(all(item in asset_map for item in beat["asset_ids"]), f"beat {beat['beat_id']}: unknown asset")

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

    blockers = execution_blockers(manifest, recipes)
    state = plan["state"]
    if state == "planned":
        _require(not plan["blockers"] and intent is None, "planned state cannot have blockers or write intent")
    elif state == "blocked":
        _require(blockers, "blocked state requires an unresolved execution blocker")
        _require([item["code"] for item in plan["blockers"]] == [item["code"] for item in blockers], "stored blockers do not match current facts")
        _require(intent is None, "blocked state cannot have write intent")
    else:
        _require(not blockers and not plan["blockers"], f"{state} state cannot have execution blockers")
        if state == "ready":
            _require(intent is None, "ready state cannot have write intent")
        else:
            _require(intent is not None, f"{state} state requires write intent")
        if state == "verified":
            beat_id = plan["representative_beat_id"]
            passing = {check["stage"] for check in checks if check["beat_id"] == beat_id and check["status"] == "pass" and check["evidence"]}
            _require(set(recipe["verification"]["required_stages"]) <= passing, "verified state lacks required post-write evidence")


def validate_repository(root: Path, manifest_path: Path | None = None) -> dict[str, dict[str, Any]]:
    root = root.resolve()
    schema = _read_json(root / "schemas" / "talkdirector-pipeline.schema.json")
    _require(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", "pipeline schema must declare JSON Schema 2020-12")
    recipes = load_and_validate_recipes(root)
    if manifest_path is not None:
        validate_pipeline_manifest(_read_json(manifest_path), recipes)
    return recipes


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()
    recipes = validate_repository(args.root, args.manifest)
    suffix = f" and {args.manifest}" if args.manifest else ""
    print(f"Validated {len(recipes)} CutDirector recipes{suffix}")


if __name__ == "__main__":
    main()
