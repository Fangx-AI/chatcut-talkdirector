import json
import unittest
from pathlib import Path

from scripts.sync_chatcut_prompt_library import parse_cards, render_catalog_json


class PromptCatalogTest(unittest.TestCase):
    def setUp(self):
        self.page = Path("tests/fixtures/prompt-library-sample.html").read_text(
            encoding="utf-8"
        )

    def test_extracts_video_preview_metadata(self):
        cards = parse_cards(self.page)
        video = next(card for card in cards if card["target"] == "video-gen")
        self.assertEqual(video["reference_id"], "video-preset-1")
        self.assertEqual(video["preview_video_url"], "https://cdn.example/video.mp4")
        self.assertEqual(video["poster_url"], "https://cdn.example/poster.jpg")

    def test_motion_graphic_uses_live_entry_without_fake_video(self):
        cards = parse_cards(self.page)
        mg = next(card for card in cards if card["target"] == "motion-graphics")
        self.assertEqual(mg["reference_id"], "mg-template-1")
        self.assertEqual(mg["preview_video_url"], "")
        self.assertEqual(mg["poster_url"], "")

    def test_json_catalog_is_machine_readable(self):
        payload = json.loads(render_catalog_json(parse_cards(self.page), "2026-07-16"))
        self.assertEqual(payload["count"], 2)
        self.assertEqual(len(payload["entries"]), 2)
        self.assertEqual(payload["synced_on"], "2026-07-16")


if __name__ == "__main__":
    unittest.main()
