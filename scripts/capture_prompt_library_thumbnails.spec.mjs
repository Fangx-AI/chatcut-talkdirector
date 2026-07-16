import fs from "node:fs";
import path from "node:path";
import { test, expect } from "@playwright/test";

const catalog = JSON.parse(
  fs.readFileSync("references/chatcut-official-catalog.json", "utf8"),
);
const allEntries = catalog.entries.filter(
  (entry) => entry.target === "motion-graphics",
);
const requestedId = process.env.CAPTURE_ID || "";
const entries = requestedId
  ? allEntries.filter((entry) => entry.reference_id === requestedId)
  : allEntries;
const limit = Number(process.env.CAPTURE_LIMIT || entries.length);
const outputDir = path.join("assets", "official-gallery");

test("capture official motion graphic cards", async ({ page }) => {
  test.setTimeout(12 * 60 * 1000);
  console.log({ requestedId, selectedEntries: entries.length });
  fs.mkdirSync(outputDir, { recursive: true });
  await page.setViewportSize({ width: 1440, height: 1000 });
  await page.goto(catalog.source_url, { waitUntil: "domcontentloaded" });

  for (const entry of entries.slice(0, limit)) {
    const card = page.locator(
      `a[data-prompt-library-card][href*="template=${entry.reference_id}"]`,
    );
    await expect(card, entry.name).toHaveCount(1);
    await card.scrollIntoViewIfNeeded();
    const frame = card.locator(".prompt-library-media-frame");
    await expect(
      frame.locator(".motion-template-cover"),
      `${entry.name} should hydrate before capture`,
    ).toBeVisible({ timeout: 15_000 });
    await expect(frame, `${entry.name} media frame`).toBeVisible();
    let bestFrame = null;
    for (let sample = 0; sample < 6; sample += 1) {
      await page.waitForTimeout(400);
      const candidate = await frame.screenshot({
        type: "jpeg",
        quality: 80,
        animations: "allow",
      });
      if (bestFrame === null || candidate.length > bestFrame.length) {
        bestFrame = candidate;
      }
    }
    fs.writeFileSync(
      path.join(outputDir, `${entry.reference_id}.jpg`),
      bestFrame,
    );
  }
});
