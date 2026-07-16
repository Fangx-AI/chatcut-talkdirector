# Visual-First README And Official Gallery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a result-first GitHub README and a visual gallery that lets users see verified TalkDirector effects and all 123 current ChatCut official Prompt Library entries without reading internal rules.

**Architecture:** Extend the existing Python catalog sync into a structured metadata pipeline that records official preview video/poster URLs. Use Playwright only for Motion Graphics cards that have no downloadable preview, capturing one representative official frame per template. Generate `VISUAL-GALLERY.md` from machine-readable metadata, while keeping README short and showing only verified and curated effects.

**Tech Stack:** Python 3.14 standard library and `unittest`, Node.js, `@playwright/test` 1.61.1, FFmpeg, Markdown, ChatCut export and verification tools.

## Global Constraints

- README sells results; Gallery shows capability; Prompt text enables immediate use; Skill and references retain internal rules.
- Do not commit all official MP4 files. Store remote MP4/poster URLs for 19 video entries.
- Do not create AI approximations of official previews.
- Capture representative frames for 104 Motion Graphics entries from the official live-rendered cards.
- Label official references separately from TalkDirector Verified Prompts.
- Keep `assets/IMAGE-PROMPTS.md` outside every commit unless it gains a real content diff.
- Preserve the current Visual Beat Map, Quality Gate, and two-confirmation execution boundary in internal documentation.

---

## File Map

- Modify `scripts/sync_chatcut_prompt_library.py`: parse preview metadata and emit Markdown plus JSON catalogs.
- Create `tests/fixtures/prompt-library-sample.html`: deterministic video and MG card fixture.
- Create `tests/test_sync_chatcut_prompt_library.py`: parser and catalog regression tests.
- Create `references/chatcut-official-catalog.json`: generated machine-readable source for Gallery generation.
- Create `package.json` and `package-lock.json`: pin the thumbnail capture dependency.
- Create `scripts/capture_prompt_library_thumbnails.spec.mjs`: capture official MG media frames.
- Create `assets/official-gallery/`: generated 16:9 JPEG thumbnails named by template ID.
- Create `scripts/generate_visual_gallery.py`: build the user-facing visual gallery.
- Create `tests/test_generate_visual_gallery.py`: gallery completeness and copy tests.
- Create `VISUAL-GALLERY.md`: generated user-facing gallery.
- Create `assets/verified-prompts/prompt-001-gesture-logo-pop.gif`: real verified Prompt 001 preview.
- Rewrite `README.md`: result-first public page.

---

### Task 1: Structured Official Preview Metadata

**Files:**
- Modify: `scripts/sync_chatcut_prompt_library.py`
- Create: `tests/fixtures/prompt-library-sample.html`
- Create: `tests/test_sync_chatcut_prompt_library.py`
- Create: `references/chatcut-official-catalog.json`

**Interfaces:**
- Produces `parse_cards(page: str) -> list[dict[str, str]]`.
- Each card contains `name`, `description`, `target`, `category`, `reference_id`, `entry_url`, `preview_video_url`, and `poster_url`.
- Produces `references/chatcut-official-catalog.json` with top-level keys `source_url`, `synced_on`, `count`, `category_counts`, and `entries`.
- Keeps `references/chatcut-official-catalog.md` for agent-readable lookup.

- [ ] **Step 1: Add a deterministic HTML fixture**

Create two `a[data-prompt-library-card]` elements: one `video-gen` card containing `<video src="https://cdn.example/video.mp4" poster="https://cdn.example/poster.jpg">`, and one `motion-graphics` card containing a template ID and no video.

- [ ] **Step 2: Write failing parser tests**

```python
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
```

- [ ] **Step 3: Run the tests and verify RED**

Run:

```powershell
$env:PYTHONUTF8='1'
python -m unittest tests.test_sync_chatcut_prompt_library -v
```

Expected: import or assertion failures because `parse_cards` and `render_catalog_json` do not exist.

- [ ] **Step 4: Refactor the parser and add JSON output**

Move network fetching out of parsing. Extend `PromptCardParser.handle_starttag` so a nested `video` records `src` and `poster` on the current card. Add:

```python
def parse_cards(page: str, enforce_minimum: bool = False) -> list[dict[str, str]]:
    parser = PromptCardParser()
    parser.feed(page)
    cards = normalize_cards(parser.cards)
    if enforce_minimum and len(cards) < MIN_EXPECTED_CARDS:
        raise RuntimeError(f"Only found {len(cards)} official cards")
    return cards


def render_catalog_json(cards: list[dict[str, str]], synced_on: str) -> str:
    payload = {
        "source_url": SOURCE_URL,
        "synced_on": synced_on,
        "count": len(cards),
        "category_counts": dict(Counter(card["category"] for card in cards)),
        "entries": cards,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
```

Add CLI argument `--json-output`, defaulting to `references/chatcut-official-catalog.json`, and write both generated files in one run.

- [ ] **Step 5: Run tests and live sync**

```powershell
$env:PYTHONUTF8='1'
python -m unittest tests.test_sync_chatcut_prompt_library -v
python scripts/sync_chatcut_prompt_library.py
```

Expected: three tests pass; live sync reports 123 entries; JSON contains 19 non-empty `preview_video_url` values and 104 empty values.

- [ ] **Step 6: Add live completeness assertions**

```powershell
$catalog = Get-Content references/chatcut-official-catalog.json -Raw -Encoding UTF8 | ConvertFrom-Json
if ($catalog.count -ne 123) { throw "Expected 123 official entries" }
if (($catalog.entries | Where-Object preview_video_url).Count -ne 19) { throw "Expected 19 videos" }
if (($catalog.entries | Where-Object target -eq 'motion-graphics').Count -ne 104) { throw "Expected 104 MG entries" }
```

- [ ] **Step 7: Commit Task 1**

```powershell
git add scripts/sync_chatcut_prompt_library.py tests/fixtures/prompt-library-sample.html tests/test_sync_chatcut_prompt_library.py references/chatcut-official-catalog.md references/chatcut-official-catalog.json
git commit -m "feat: capture official prompt preview metadata"
```

---

### Task 2: Official Motion Graphics Thumbnails

**Files:**
- Create: `package.json`
- Create: `package-lock.json`
- Create: `scripts/capture_prompt_library_thumbnails.spec.mjs`
- Create: `assets/official-gallery/*.jpg`
- Modify: `.gitignore`

**Interfaces:**
- Consumes `references/chatcut-official-catalog.json`.
- Produces `assets/official-gallery/<template-id>.jpg` at the official card's 16:9 media-frame dimensions.
- Accepts environment variable `CAPTURE_LIMIT`; omitted means all 104 MG entries.

- [ ] **Step 1: Add the pinned Playwright maintenance dependency**

```json
{
  "private": true,
  "scripts": {
    "gallery:capture": "playwright test scripts/capture_prompt_library_thumbnails.spec.mjs --workers=1"
  },
  "devDependencies": {
    "@playwright/test": "1.61.1"
  }
}
```

Run `npm install` and add `node_modules/` and `test-results/` to `.gitignore`.

- [ ] **Step 2: Create the capture test**

The Playwright test must:

```javascript
import fs from "node:fs";
import path from "node:path";
import { test, expect } from "@playwright/test";

const catalog = JSON.parse(
  fs.readFileSync("references/chatcut-official-catalog.json", "utf8"),
);
const entries = catalog.entries.filter((entry) => entry.target === "motion-graphics");
const limit = Number(process.env.CAPTURE_LIMIT || entries.length);

test("capture official motion graphic cards", async ({ page }) => {
  test.setTimeout(12 * 60 * 1000);
  await page.setViewportSize({ width: 1440, height: 1000 });
  await page.goto(catalog.source_url, { waitUntil: "domcontentloaded" });

  for (const entry of entries.slice(0, limit)) {
    const card = page.locator(
      `a[data-prompt-library-card][href*="template=${entry.reference_id}"]`,
    );
    await expect(card).toHaveCount(1);
    await card.scrollIntoViewIfNeeded();
    await page.waitForTimeout(1200);
    const frame = card.locator(".prompt-library-media-frame");
    await frame.screenshot({
      path: path.join("assets", "official-gallery", `${entry.reference_id}.jpg`),
      type: "jpeg",
      quality: 80,
    });
  }
});
```

- [ ] **Step 3: Verify one capture before the batch**

```powershell
$env:CAPTURE_LIMIT='1'
npm run gallery:capture
```

Expected: one JPEG exists, opens correctly, contains the official card frame, and has no card title or surrounding webpage chrome.

- [ ] **Step 4: Capture all Motion Graphics thumbnails**

```powershell
Remove-Item Env:CAPTURE_LIMIT -ErrorAction SilentlyContinue
npm run gallery:capture
$count = (Get-ChildItem assets/official-gallery -Filter *.jpg).Count
if ($count -ne 104) { throw "Expected 104 MG thumbnails, got $count" }
```

- [ ] **Step 5: Run a visual sample check**

Inspect at least the thumbnails for:

- `AI Stack Chart Animation`
- `AI Line Chart Animation`
- `AI Radar Chart Animation`
- `AI Numbered Talking-Head Overlay`
- `AI Speaker Intro Card`
- `AI Story Quote Card`

Reject blank, loading, clipped, or duplicated thumbnails and adjust the wait only if the official page visibly needs more render time.

- [ ] **Step 6: Commit Task 2**

```powershell
git add package.json package-lock.json .gitignore scripts/capture_prompt_library_thumbnails.spec.mjs assets/official-gallery
git commit -m "feat: add official motion graphic previews"
```

---

### Task 3: Generate The User-Facing Visual Gallery

**Files:**
- Create: `scripts/generate_visual_gallery.py`
- Create: `tests/test_generate_visual_gallery.py`
- Create: `VISUAL-GALLERY.md`

**Interfaces:**
- Consumes `references/chatcut-official-catalog.json` and `assets/official-gallery/*.jpg`.
- Produces `VISUAL-GALLERY.md` with every official entry exactly once.
- Video entries use official poster images linked to official MP4 previews.
- MG entries use local official-frame thumbnails linked to official ChatCut entry URLs.

- [ ] **Step 1: Write failing gallery tests**

```python
import json
import unittest
from pathlib import Path

from scripts.generate_visual_gallery import generate_gallery


class VisualGalleryTest(unittest.TestCase):
    def test_every_entry_is_linked_once(self):
        catalog = json.loads(
            Path("references/chatcut-official-catalog.json").read_text(encoding="utf-8")
        )
        gallery = generate_gallery(catalog)
        for entry in catalog["entries"]:
            self.assertEqual(gallery.count(entry["entry_url"]), 1)

    def test_gallery_hides_internal_ids(self):
        catalog = json.loads(
            Path("references/chatcut-official-catalog.json").read_text(encoding="utf-8")
        )
        gallery = generate_gallery(catalog)
        self.assertNotIn("模板/预设 ID", gallery)
        self.assertNotIn("Quality Gate", gallery)
```

- [ ] **Step 2: Run tests and verify RED**

```powershell
$env:PYTHONUTF8='1'
python -m unittest tests.test_generate_visual_gallery -v
```

Expected: import failure because the generator does not exist.

- [ ] **Step 3: Implement category routing and card rendering**

Use deterministic keyword routing for MG subcategories: Talking Head, Data & Charts, Lists & Steps, Chapters & Titles, Quotes & Lower Thirds, and Other Motion Graphics. Render two cards per HTML table row so GitHub keeps previews readable. Each card contains only image, official name, one-sentence purpose, and one action link.

Add CLI defaults:

```python
parser.add_argument("--catalog", default="references/chatcut-official-catalog.json")
parser.add_argument("--output", default="VISUAL-GALLERY.md")
```

- [ ] **Step 4: Generate and test the Gallery**

```powershell
python scripts/generate_visual_gallery.py
python -m unittest tests.test_generate_visual_gallery -v
```

Expected: tests pass; Gallery references 123 official entry URLs exactly once.

- [ ] **Step 5: Check Markdown assets and links**

Verify every local image path exists and issue HTTP `HEAD` requests for the 19 poster and MP4 URLs. A `403` on `HEAD` must be retried with a ranged `GET`; only a failed ranged request counts as broken.

- [ ] **Step 6: Commit Task 3**

```powershell
git add scripts/generate_visual_gallery.py tests/test_generate_visual_gallery.py VISUAL-GALLERY.md
git commit -m "feat: publish official visual prompt gallery"
```

---

### Task 4: Verified Prompt 001 Preview And Result-First README

**Files:**
- Create: `assets/verified-prompts/prompt-001-gesture-logo-pop.mp4`
- Create: `assets/verified-prompts/prompt-001-gesture-logo-pop.gif`
- Rewrite: `README.md`

**Interfaces:**
- Uses ChatCut project `0065e47f-1f7b-428b-a80c-26e545282af1` and timeline `882c2c1a-ae49-401d-a3c6-0df4d4be74e1` as the verified Prompt 001 source.
- README links to `VISUAL-GALLERY.md`, `SKILL.md`, and `references/prompt-001-gesture-logo-pop.md`.

- [ ] **Step 1: Re-verify the source timeline**

Read the project and render frames 22, 35, 45, 60, 88, and 100. Confirm: clean frame, left entry, right entry, both settled, exit, and clean return.

- [ ] **Step 2: Export the verified source**

Export the 1280x720 timeline as H.264 MP4. Track the render to completion and save the downloaded file as:

```text
assets/verified-prompts/prompt-001-gesture-logo-pop.mp4
```

- [ ] **Step 3: Create a GitHub-inline GIF**

```powershell
ffmpeg -y -i assets/verified-prompts/prompt-001-gesture-logo-pop.mp4 -vf "fps=12,scale=720:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128[p];[s1][p]paletteuse=dither=bayer:bayer_scale=3" -loop 0 assets/verified-prompts/prompt-001-gesture-logo-pop.gif
```

Expected: GIF loops, remains readable, and is below 8 MB. If larger, reduce scale to 640 while keeping 12 fps.

- [ ] **Step 4: Rewrite README in the approved order**

Use this section order only:

```markdown
Hero
See It Work
Verified Prompt Series
What It Can Add
Official Prompt Highlights
How It Works In 3 Steps
Install
Technical Details links
```

The first visible example embeds the Prompt 001 GIF and this copyable Prompt:

```text
在 [时间段]，给人物两侧的指向手势添加 [品牌 A] 和 [品牌 B] 的官方 Logo 弹出特效：[品牌 A] 在画面左侧，[品牌 B] 在画面右侧，分别跟随对应手指抬起时弹出，手势结束时退场。请自动获取可验证的官方 Logo，保持人物全屏，不遮挡脸、字幕、手和产品，并先展示关键帧让我确认。
```

Select 6 official highlights: AI Numbered Talking-Head Overlay, AI Talking-Head Keyword Card, AI Stack Chart Animation, AI Line Chart Animation, AI Radar Chart Animation, and AI Speaker Intro Card. Use their real thumbnails and link each to its official entry.

- [ ] **Step 5: Remove internal-detail sections from the public path**

Remove expanded Quality Gate rules, repository counts, test-process narration, routing details, and current-boundary prose from README. Keep links to `SKILL.md`, `VISUAL-GALLERY.md`, and test evidence under one compact Technical Details line.

- [ ] **Step 6: Verify README rendering**

Render the Markdown in a GitHub-compatible preview at desktop and mobile widths. Confirm no broken local images, horizontal overflow, unreadable two-column tables, or first-screen rule text.

- [ ] **Step 7: Commit Task 4**

```powershell
git add README.md assets/verified-prompts/prompt-001-gesture-logo-pop.mp4 assets/verified-prompts/prompt-001-gesture-logo-pop.gif
git commit -m "docs: make TalkDirector results visible"
```

---

### Task 5: End-To-End Verification And Release

**Files:**
- Verify all files from Tasks 1-4.

**Interfaces:**
- Produces a release-ready `main` branch with a visual README, complete Gallery, and repeatable official preview sync.

- [ ] **Step 1: Run all deterministic checks**

```powershell
$env:PYTHONUTF8='1'
python -m unittest discover -s tests -p 'test_*.py' -v
python C:/Users/PC/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
python scripts/sync_chatcut_prompt_library.py
python scripts/generate_visual_gallery.py
git diff --check
```

Expected: all tests pass, Skill is valid, sync reports 123 entries, regeneration leaves no unexpected diff, and `git diff --check` exits zero.

- [ ] **Step 2: Run visual and asset checks**

Confirm:

- 104 MG JPEGs exist and six named samples are nonblank.
- 19 official video entries have reachable poster and MP4 URLs.
- Prompt 001 GIF is under 8 MB and visually matches the verified timeline.
- Every README and Gallery local link resolves.
- Gallery contains 123 official entries exactly once.

- [ ] **Step 3: Review the final Git diff**

Ensure no generated cache, `node_modules`, browser test output, unrelated local file, or `assets/IMAGE-PROMPTS.md` line-ending-only change is staged.

- [ ] **Step 4: Push the completed commits**

```powershell
git push origin main
git fetch origin main
git status -sb
git log -1 --oneline --decorate
```

Expected: `main...origin/main` with only the existing line-ending status for `assets/IMAGE-PROMPTS.md`, and remote `main` points to the final release commit.
