import copy
import json
import unittest
from pathlib import Path

from scripts.validate_talkdirector import (
    ValidationError,
    load_and_validate_recipes,
    validate_pipeline_manifest,
    validate_recipe,
    validate_repository,
)


ROOT = Path(__file__).resolve().parents[1]


class RecipeValidationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.recipes = load_and_validate_recipes(ROOT)

    def test_repository_contains_both_compatible_verified_recipes(self):
        self.assertEqual(
            set(self.recipes),
            {
                "prompt-001-gesture-logo-pop",
                "prompt-002-split-screen-explainer",
            },
        )
        self.assertTrue(all(recipe["status"] == "verified" for recipe in self.recipes.values()))

    def test_recipes_cover_required_execution_sections(self):
        required = {
            "triggers",
            "required_inputs",
            "asset_strategy",
            "layout_safe_zones",
            "timing_animation",
            "fallback_chain",
            "verification",
        }
        for recipe in self.recipes.values():
            self.assertLessEqual(required, recipe.keys())

    def test_prompt_001_has_explicit_missing_material_and_gesture_policies(self):
        policies = self.recipes["prompt-001-gesture-logo-pop"]["blocking_policies"]
        self.assertIn("no_obvious_gesture", policies)
        self.assertIn("logo_unverifiable", policies)
        self.assertIn("safe_zone_conflict", policies)

    def test_prompt_002_has_copy_overflow_and_conflict_policies(self):
        policies = self.recipes["prompt-002-split-screen-explainer"]["blocking_policies"]
        self.assertIn("missing_verbatim_copy", policies)
        self.assertIn("long_text_overflow", policies)
        self.assertIn("safe_zone_conflict", policies)

    def test_missing_recipe_field_fails(self):
        path = ROOT / "recipes" / "prompt-001-gesture-logo-pop.json"
        recipe = copy.deepcopy(self.recipes[path.stem])
        del recipe["verification"]
        with self.assertRaisesRegex(ValidationError, "missing recipe fields"):
            validate_recipe(recipe, path, ROOT)

    def test_non_terminal_fallback_chain_fails(self):
        path = ROOT / "recipes" / "prompt-002-split-screen-explainer.json"
        recipe = copy.deepcopy(self.recipes[path.stem])
        recipe["fallback_chain"][-1]["terminal"] = False
        with self.assertRaisesRegex(ValidationError, "final fallback"):
            validate_recipe(recipe, path, ROOT)

    def test_missing_verification_stage_fails(self):
        path = ROOT / "recipes" / "prompt-001-gesture-logo-pop.json"
        recipe = copy.deepcopy(self.recipes[path.stem])
        recipe["verification"]["checks"] = [
            check
            for check in recipe["verification"]["checks"]
            if check["stage"] != "ending"
        ]
        with self.assertRaisesRegex(ValidationError, "stage has no check"):
            validate_recipe(recipe, path, ROOT)


class PipelineManifestValidationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.recipes = load_and_validate_recipes(ROOT)
        cls.valid = json.loads(
            (ROOT / "tests" / "fixtures" / "pipeline-manifest-valid.json").read_text(
                encoding="utf-8"
            )
        )

    def test_valid_representative_execution_passes(self):
        validate_pipeline_manifest(copy.deepcopy(self.valid), self.recipes)

    def test_reversed_time_range_fails(self):
        manifest = copy.deepcopy(self.valid)
        manifest["visual_beats"][0]["time_range"]["start_seconds"] = 3.5
        manifest["visual_beats"][0]["time_range"]["end_seconds"] = 2.0
        with self.assertRaisesRegex(ValidationError, "invalid or out-of-source"):
            validate_pipeline_manifest(manifest, self.recipes)

    def test_unconfirmed_time_cannot_execute(self):
        manifest = copy.deepcopy(self.valid)
        manifest["visual_beats"][0]["time_range"]["confirmed_by_user"] = False
        with self.assertRaisesRegex(ValidationError, "user-confirmed time range"):
            validate_pipeline_manifest(manifest, self.recipes)

    def test_unverified_required_asset_cannot_execute(self):
        manifest = copy.deepcopy(self.valid)
        manifest["assets"][0]["verification_status"] = "pending"
        with self.assertRaisesRegex(ValidationError, "assets must be verified"):
            validate_pipeline_manifest(manifest, self.recipes)

    def test_missing_ending_evidence_cannot_mark_executed(self):
        manifest = copy.deepcopy(self.valid)
        manifest["verification"]["checks"][-1]["evidence"] = []
        with self.assertRaisesRegex(ValidationError, "lacks passing verification evidence"):
            validate_pipeline_manifest(manifest, self.recipes)

    def test_non_verbatim_anchor_fails(self):
        manifest = copy.deepcopy(self.valid)
        manifest["visual_beats"][0]["anchor_text"] = "模型改写的品牌句"
        with self.assertRaisesRegex(ValidationError, "not verbatim transcript"):
            validate_pipeline_manifest(manifest, self.recipes)

    def test_repository_cli_contract_can_validate_fixture(self):
        validate_repository(
            ROOT,
            ROOT / "tests" / "fixtures" / "pipeline-manifest-valid.json",
        )


if __name__ == "__main__":
    unittest.main()
