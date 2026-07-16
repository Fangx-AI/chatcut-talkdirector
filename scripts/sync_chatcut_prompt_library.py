#!/usr/bin/env python3
"""Build a compact catalog from ChatCut's official Prompt Library."""

from __future__ import annotations

import argparse
import html
import json
from collections import Counter
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from urllib.request import Request, urlopen


SOURCE_URL = "https://chatcut.io/prompt-library"
MIN_EXPECTED_CARDS = 100
CATEGORY_LABELS = {
    "app-promo": "App Promo",
    "video-gen": "Video Generation / Seedance 2",
    "motion-graphics": "Motion Graphics",
}


class PromptCardParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.current: dict[str, object] | None = None
        self.cards: list[dict[str, object]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag == "a" and "data-prompt-library-card" in attributes:
            self.current = {
                "name": attributes.get("aria-label") or "",
                "entry_url": attributes.get("href") or "",
                "depth": 1,
                "texts": [],
                "preview_video_url": "",
                "poster_url": "",
            }
        elif self.current is not None:
            self.current["depth"] = int(self.current["depth"]) + 1
            if tag == "video":
                self.current["preview_video_url"] = attributes.get("src") or ""
                self.current["poster_url"] = attributes.get("poster") or ""
            elif tag == "source" and not self.current["preview_video_url"]:
                self.current["preview_video_url"] = attributes.get("src") or ""

    def handle_endtag(self, _tag: str) -> None:
        if self.current is None:
            return
        self.current["depth"] = int(self.current["depth"]) - 1
        if self.current["depth"] == 0:
            self.cards.append(self.current)
            self.current = None

    def handle_data(self, data: str) -> None:
        if self.current is None:
            return
        text = " ".join(data.split())
        if text:
            texts = self.current["texts"]
            assert isinstance(texts, list)
            texts.append(text)


def parse_cards(page: str, enforce_minimum: bool = False) -> list[dict[str, str]]:
    parser = PromptCardParser()
    parser.feed(page)
    cards: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()

    for raw in parser.cards:
        name = html.unescape(str(raw["name"])).strip()
        entry_url = html.unescape(str(raw["entry_url"])).strip()
        key = (name, entry_url)
        if not name or not entry_url or key in seen:
            continue
        seen.add(key)

        query = parse_qs(urlparse(entry_url).query)
        target = query.get("target", ["uncategorized"])[0]
        texts = [html.unescape(str(value)).strip() for value in raw["texts"]]
        description = next(
            (
                value
                for value in texts
                if value != name
                and not value.lower().startswith("try this prompt")
                and len(value) > 12
            ),
            "Official ChatCut Prompt Library entry.",
        )
        reference_id = query.get(
            "template", query.get("preset", query.get("prompt", [""]))
        )[0]
        cards.append(
            {
                "name": name,
                "entry_url": entry_url,
                "target": target,
                "category": CATEGORY_LABELS.get(target, target),
                "description": description,
                "reference_id": reference_id,
                "preview_video_url": html.unescape(
                    str(raw["preview_video_url"])
                ).strip(),
                "poster_url": html.unescape(str(raw["poster_url"])).strip(),
            }
        )

    if enforce_minimum and len(cards) < MIN_EXPECTED_CARDS:
        raise RuntimeError(
            f"Only found {len(cards)} cards; expected at least {MIN_EXPECTED_CARDS}. "
            "The official page structure may have changed."
        )
    return cards


def fetch_cards() -> list[dict[str, str]]:
    request = Request(SOURCE_URL, headers={"User-Agent": "TalkDirector catalog sync"})
    with urlopen(request, timeout=30) as response:
        page = response.read().decode("utf-8")
    return parse_cards(page, enforce_minimum=True)


def escape_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def render_catalog(cards: list[dict[str, str]], synced_on: str | None = None) -> str:
    synced_on = synced_on or date.today().isoformat()
    counts = Counter(card["category"] for card in cards)
    lines = [
        "# ChatCut 官方 Prompt Library 完整目录",
        "",
        f"最后同步：{synced_on}",
        f"官方来源：{SOURCE_URL}",
        f"收录条目：{len(cards)}",
        "",
        "> 本文件由 `scripts/sync_chatcut_prompt_library.py` 生成。保存名称、用途、类别、官方入口和模板 ID；不复制官方页面中的完整模板代码。",
        "",
        "## 使用规则",
        "",
        "1. 先用本目录寻找与用户视觉任务完全匹配或高度相似的官方条目。",
        "2. 完全匹配时优先使用官方入口或模板 ID，并只替换用户内容与必要属性。",
        "3. 部分匹配时借鉴信息结构和动效机制，不冒充官方原模板。",
        "4. 官方模板仍须通过 TalkDirector 的人物、字幕、手势、品牌和 Quality Gate 检查。",
        "5. 用户要求最新目录、条目不存在或入口失效时，重新运行同步脚本。",
        "",
        "## 分类统计",
        "",
        "| 分类 | 数量 |",
        "| --- | ---: |",
    ]
    for category in sorted(counts):
        lines.append(f"| {escape_cell(category)} | {counts[category]} |")

    for category in CATEGORY_LABELS.values():
        category_cards = [card for card in cards if card["category"] == category]
        if not category_cards:
            continue
        lines.extend(
            [
                "",
                f"## {category}",
                "",
                "| # | 官方名称 | 用途 | 模板/预设 ID | 官方入口 |",
                "| ---: | --- | --- | --- | --- |",
            ]
        )
        for index, card in enumerate(category_cards, start=1):
            reference_id = card["reference_id"] or "-"
            lines.append(
                "| {index} | {name} | {description} | `{reference_id}` | [打开]({url}) |".format(
                    index=index,
                    name=escape_cell(card["name"]),
                    description=escape_cell(card["description"]),
                    reference_id=escape_cell(reference_id),
                    url=card["entry_url"],
                )
            )
    return "\n".join(lines) + "\n"


def render_catalog_json(cards: list[dict[str, str]], synced_on: str) -> str:
    payload = {
        "source_url": SOURCE_URL,
        "synced_on": synced_on,
        "count": len(cards),
        "category_counts": dict(Counter(card["category"] for card in cards)),
        "entries": cards,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default="references/chatcut-official-catalog.md",
        help="Catalog output path relative to the current working directory.",
    )
    parser.add_argument(
        "--json-output",
        default="references/chatcut-official-catalog.json",
        help="Machine-readable catalog output path.",
    )
    args = parser.parse_args()
    output = Path(args.output)
    json_output = Path(args.json_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    json_output.parent.mkdir(parents=True, exist_ok=True)
    cards = fetch_cards()
    synced_on = date.today().isoformat()
    output.write_text(
        render_catalog(cards, synced_on), encoding="utf-8", newline="\n"
    )
    json_output.write_text(
        render_catalog_json(cards, synced_on), encoding="utf-8", newline="\n"
    )
    print(f"Wrote {len(cards)} official entries to {output} and {json_output}")


if __name__ == "__main__":
    main()
