import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.talkdirector_manifest import (
    build,
    create_recipe_draft,
    initialize,
    manifest_path,
    transition,
)
from scripts.validate_talkdirector import (
    ValidationError,
    load_and_validate_recipes,
    validate_pipeline_manifest,
    validate_recipe,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "e2e"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class RecipeValidationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.recipes = load_and_validate_recipes(ROOT)

    def test_all_public_prompts_remain_compatible(self):
        self.assertEqual(
            set(self.recipes),
            {
                "prompt-001-gesture-logo-pop",
                "prompt-002-split-screen-explainer",
                "prompt-003-brand-mode-comparison",
                "prompt-004-top-chapter-progress-rail",
            },
        )
        self.assertTrue(all(recipe["status"] == "verified" for recipe in self.recipes.values()))

    def test_recipes_define_deterministic_execution_gates(self):
        self.assertEqual(
            self.recipes["prompt-001-gesture-logo-pop"]["execution_gates"],
            ["time", "gesture", "assets", "safe_zones", "first_approval"],
        )
        self.assertEqual(
            self.recipes["prompt-002-split-screen-explainer"]["execution_gates"],
            ["time", "copy", "safe_zones", "first_approval"],
        )
        self.assertEqual(
            self.recipes["prompt-003-brand-mode-comparison"]["execution_gates"],
            ["time", "assets", "copy", "safe_zones", "first_approval"],
        )
        self.assertEqual(
            self.recipes["prompt-004-top-chapter-progress-rail"]["execution_gates"],
            ["time", "copy", "safe_zones", "first_approval"],
        )
        progress_prompt = self.recipes["prompt-004-top-chapter-progress-rail"]["public_prompt"]
        self.assertIn("真实时长比例", progress_prompt)
        self.assertIn("跨章节时绝不清零、回跳", progress_prompt)

    def test_missing_recipe_field_fails(self):
        path = ROOT / "recipes" / "prompt-001-gesture-logo-pop.json"
        recipe = copy.deepcopy(self.recipes[path.stem])
        del recipe["execution_gates"]
        with self.assertRaisesRegex(ValidationError, "missing recipe fields"):
            validate_recipe(recipe, path, ROOT)

    def test_fallback_chain_and_verification_coverage_are_enforced(self):
        path = ROOT / "recipes" / "prompt-002-split-screen-explainer.json"
        recipe = copy.deepcopy(self.recipes[path.stem])
        recipe["fallback_chain"][-1]["terminal"] = False
        with self.assertRaisesRegex(ValidationError, "final fallback"):
            validate_recipe(recipe, path, ROOT)
        recipe = copy.deepcopy(self.recipes[path.stem])
        recipe["verification"]["checks"] = [item for item in recipe["verification"]["checks"] if item["stage"] != "ending"]
        with self.assertRaisesRegex(ValidationError, "stage has no check"):
            validate_recipe(recipe, path, ROOT)


class ManifestLifecycleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.recipes = load_and_validate_recipes(ROOT)

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.cache = Path(self.temporary.name) / ".talkdirector"

    def tearDown(self):
        self.temporary.cleanup()

    def _initialize(self, source_id: str, recipe_id: str) -> Path:
        return initialize(self.cache, source_id, "chatcut-project", recipe_id, self.recipes)

    def test_initialization_is_idempotent_and_path_is_project_scoped(self):
        path = self._initialize("Project A / source.mp4", "prompt-001-gesture-logo-pop")
        first = path.read_bytes()
        again = self._initialize("Project A / source.mp4", "prompt-001-gesture-logo-pop")
        self.assertEqual(path, again)
        self.assertEqual(first, again.read_bytes())
        self.assertEqual(path, manifest_path(self.cache, "Project A / source.mp4"))
        self.assertEqual(load(path)["edit_plan"]["state"], "planned")

    def test_prompt_001_recovers_from_blocked_to_ready_without_overwriting_old_decisions(self):
        path = self._initialize("p001", "prompt-001-gesture-logo-pop")
        initial = load(FIXTURES / "prompt-001" / "initial-facts.json")
        blocked = build(path, initial, self.recipes)
        self.assertEqual(blocked["edit_plan"]["state"], "blocked")
        codes = {item["code"] for item in blocked["edit_plan"]["blockers"]}
        self.assertTrue({"time-confirmation", "gate-time", "gate-gesture", "gate-assets", "first-approval", "verified-assets"} <= codes)

        conflicting = {"visual_beats": [{"beat_id": "beat-logo", "director_decision": "Replace the confirmed direction."}]}
        recovered = build(path, conflicting, self.recipes)
        self.assertEqual(recovered["visual_beats"][0]["director_decision"], initial["visual_beats"][0]["director_decision"])

        ready = build(path, load(FIXTURES / "prompt-001" / "ready-facts.json"), self.recipes)
        self.assertEqual(ready["edit_plan"]["state"], "ready")
        self.assertEqual(ready["edit_plan"]["blockers"], [])
        self.assertEqual(ready["visual_beats"][0]["time_range"]["start_seconds"], 11.2)
        validate_pipeline_manifest(ready, self.recipes)

    def test_execution_requires_preflight_and_verification_requires_evidence(self):
        path = self._initialize("p001-gates", "prompt-001-gesture-logo-pop")
        build(path, load(FIXTURES / "prompt-001" / "initial-facts.json"), self.recipes)
        with self.assertRaisesRegex(ValidationError, "only a ready"):
            transition(path, "executing", "dry-run-1", "representative", self.recipes)

        build(path, load(FIXTURES / "prompt-001" / "ready-facts.json"), self.recipes)
        with self.assertRaisesRegex(ValidationError, "second-approval"):
            transition(path, "executing", "dry-run-expanded", "expanded", self.recipes)
        executing = transition(path, "executing", "dry-run-1", "representative", self.recipes)
        self.assertEqual(executing["edit_plan"]["state"], "executing")
        with self.assertRaisesRegex(ValidationError, "post-write evidence"):
            transition(path, "verified", None, "representative", self.recipes)

        updated = build(path, load(FIXTURES / "prompt-001" / "post-write-evidence.json"), self.recipes)
        self.assertEqual(updated["edit_plan"]["state"], "executing")
        verified = transition(path, "verified", None, "representative", self.recipes)
        self.assertEqual(verified["edit_plan"]["state"], "verified")
        self.assertEqual({item["stage"] for item in verified["verification"]["checks"]}, {"asset", "beginning", "middle", "ending"})

    def test_prompt_002_ready_fixture_enforces_layout_scroll_and_safe_zones(self):
        path = self._initialize("p002", "prompt-002-split-screen-explainer")
        ready = build(path, load(FIXTURES / "prompt-002" / "ready-facts.json"), self.recipes)
        self.assertEqual(ready["edit_plan"]["state"], "ready")
        params = ready["visual_beats"][0]["parameters"]
        self.assertEqual(len(params["points"]), 4)
        self.assertLessEqual(params["right_column_ratio"], 0.45)
        self.assertFalse(params["scroll_to_end_required"])
        self.assertEqual(params["scroll_speed_policy"], "constant-comfortable")
        self.assertEqual({item["kind"] for item in ready["source"]["protected_regions"]}, {"speaker", "captions"})

        recipe = self.recipes["prompt-002-split-screen-explainer"]
        checks = {item["id"]: item for item in recipe["verification"]["checks"]}
        self.assertEqual(checks["opening_composition"]["evidence_required"], "boundary_frames")
        self.assertEqual(checks["completion_and_exit"]["evidence_required"], "boundary_frames")
        self.assertIn("接管前", checks["opening_composition"]["rule"])
        self.assertIn("恢复后", checks["completion_and_exit"]["rule"])

        transition(path, "executing", "dry-run-2", "representative", self.recipes)
        build(path, load(FIXTURES / "prompt-002" / "post-write-evidence.json"), self.recipes)
        verified = transition(path, "verified", None, "representative", self.recipes)
        self.assertEqual(verified["edit_plan"]["state"], "verified")

    def test_prompt_003_enforces_icon_background_sound_and_export_boundaries(self):
        path = self._initialize("p003", "prompt-003-brand-mode-comparison")
        ready_facts = load(FIXTURES / "prompt-003" / "ready-facts.json")
        ready = build(path, ready_facts, self.recipes)
        self.assertEqual(ready["edit_plan"]["state"], "ready")
        params = ready["visual_beats"][0]["parameters"]
        self.assertEqual(params["mode_a_capability"], "聊天对话")
        self.assertEqual(len(params["mode_b_capabilities"]), 4)
        self.assertTrue(params["icon_persists_between_stages"])
        self.assertEqual(params["background_color"], "#000000")
        self.assertEqual(params["sound_profile"], "light-tight")
        self.assertTrue(params["export_first_frame_check"])

        transition(path, "executing", "dry-run-3", "representative", self.recipes)
        build(path, load(FIXTURES / "prompt-003" / "post-write-evidence.json"), self.recipes)
        verified = transition(path, "verified", None, "representative", self.recipes)
        self.assertEqual(verified["edit_plan"]["state"], "verified")
        self.assertEqual(
            {item["stage"] for item in verified["verification"]["checks"]},
            {"asset", "beginning", "middle", "ending"},
        )

        invalid_path = self._initialize("p003-invalid", "prompt-003-brand-mode-comparison")
        invalid_facts = copy.deepcopy(ready_facts)
        invalid_params = invalid_facts["visual_beats"][0]["parameters"]
        invalid_params["icon_persists_between_stages"] = False
        invalid_params["background_color"] = "#090A0C"
        invalid_params["sound_profile"] = "heavy-low-frequency"
        invalid_params["export_first_frame_check"] = False
        blocked = build(invalid_path, invalid_facts, self.recipes)
        codes = {item["code"] for item in blocked["edit_plan"]["blockers"]}
        self.assertTrue(
            {
                "mode-icon-continuity",
                "mode-black-background",
                "mode-sound-profile",
                "mode-export-boundary",
            }
            <= codes
        )

    def test_breakpoint_recovery_uses_the_same_cache(self):
        path = self._initialize("resume-me", "prompt-001-gesture-logo-pop")
        build(path, load(FIXTURES / "prompt-001" / "initial-facts.json"), self.recipes)
        reloaded = load(manifest_path(self.cache, "resume-me"))
        self.assertEqual(reloaded["edit_plan"]["state"], "blocked")
        build(path, load(FIXTURES / "prompt-001" / "ready-facts.json"), self.recipes)
        self.assertEqual(load(path)["edit_plan"]["state"], "ready")

    def test_prompt_003_draft_entry_is_empty_idempotent_and_not_a_published_recipe(self):
        path = create_recipe_draft(self.cache, "prompt-003-future-effect")
        first = path.read_bytes()
        again = create_recipe_draft(self.cache, "prompt-003-future-effect")
        draft = load(again)
        self.assertEqual(first, again.read_bytes())
        self.assertEqual(draft["status"], "draft-template")
        self.assertEqual(draft["public_prompt"], "")
        self.assertNotIn("prompt-003-future-effect", self.recipes)

    def test_cli_dry_run_uses_external_temporary_cache(self):
        base = [
            sys.executable, str(ROOT / "scripts" / "talkdirector_manifest.py"),
            "--root", str(ROOT), "--cache-root", str(self.cache),
        ]

        def run(*arguments: str) -> subprocess.CompletedProcess:
            result = subprocess.run(base + list(arguments), capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 0, result.stderr)
            return result

        run("init", "--source-id", "cli-source", "--recipe-id", "prompt-002-split-screen-explainer")
        run("build", "--source-id", "cli-source", "--facts", str(FIXTURES / "prompt-002" / "ready-facts.json"))
        run("transition", "--source-id", "cli-source", "--to", "executing", "--operation-id", "cli-dry-run")
        run("build", "--source-id", "cli-source", "--facts", str(FIXTURES / "prompt-002" / "post-write-evidence.json"))
        run("transition", "--source-id", "cli-source", "--to", "verified")
        manifest = load(manifest_path(self.cache, "cli-source"))
        self.assertEqual(manifest["edit_plan"]["state"], "verified")


if __name__ == "__main__":
    unittest.main()
