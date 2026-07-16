import json
import unittest
from pathlib import Path

from scripts.generate_visual_gallery import generate_gallery


class VisualGalleryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads(
            Path("references/chatcut-official-catalog.json").read_text(
                encoding="utf-8"
            )
        )
        cls.gallery = generate_gallery(cls.catalog)

    def test_every_entry_is_linked_once(self):
        for entry in self.catalog["entries"]:
            self.assertEqual(
                self.gallery.count(entry["entry_url"]),
                1,
                entry["name"],
            )

    def test_every_motion_graphic_uses_an_existing_local_thumbnail(self):
        for entry in self.catalog["entries"]:
            if entry["target"] != "motion-graphics":
                continue
            thumbnail = Path(
                "assets/official-gallery",
                f'{entry["reference_id"]}.jpg',
            )
            self.assertTrue(thumbnail.is_file(), entry["name"])
            self.assertIn(thumbnail.as_posix(), self.gallery)

    def test_gallery_hides_internal_rules_and_ids(self):
        self.assertNotIn("模板/预设 ID", self.gallery)
        self.assertNotIn("Quality Gate", self.gallery)
        for entry in self.catalog["entries"]:
            self.assertNotIn(f'ID: {entry["reference_id"]}', self.gallery)

    def test_gallery_reports_the_official_total(self):
        self.assertIn("123 个官方效果", self.gallery)


if __name__ == "__main__":
    unittest.main()
