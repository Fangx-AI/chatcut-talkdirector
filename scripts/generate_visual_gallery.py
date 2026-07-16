#!/usr/bin/env python3
"""Generate the user-facing visual gallery from the official ChatCut catalog."""

from __future__ import annotations

import argparse
import html
import json
from collections import defaultdict
from pathlib import Path


SECTION_ORDER = (
    "口播增强",
    "数据与图表",
    "列表与步骤",
    "章节与标题",
    "引用与字幕条",
    "其他动效",
    "App Promo",
    "Seedance 2 视频生成",
)


def motion_graphics_section(entry: dict[str, str]) -> str:
    text = f'{entry["name"]} {entry["description"]}'.lower()
    routes = (
        (
            "口播增强",
            (
                "talking-head",
                "talking head",
                "speaker",
                "presenter",
                "interview",
                "portrait",
            ),
        ),
        (
            "数据与图表",
            (
                "chart",
                "dashboard",
                "benchmark",
                "metric",
                "statistics",
                "comparison",
                "counter",
                "data ",
            ),
        ),
        (
            "列表与步骤",
            (
                "list",
                "checklist",
                "step",
                "numbered",
                "timeline",
                "framework",
                "pillar",
            ),
        ),
        (
            "章节与标题",
            ("chapter", "title", "headline", "opener", "section intro"),
        ),
        (
            "引用与字幕条",
            ("quote", "lower third", "lower-third", "callout", "subtitle"),
        ),
    )
    for section, keywords in routes:
        if any(keyword in text for keyword in keywords):
            return section
    return "其他动效"


def section_for(entry: dict[str, str]) -> str:
    if entry["target"] == "app-promo":
        return "App Promo"
    if entry["target"] == "video-gen":
        return "Seedance 2 视频生成"
    return motion_graphics_section(entry)


def render_card(entry: dict[str, str]) -> str:
    name = html.escape(entry["name"])
    description = html.escape(entry["description"])
    entry_url = entry["entry_url"].replace('"', "%22")

    if entry["target"] == "motion-graphics":
        image_url = html.escape(
            f'assets/official-gallery/{entry["reference_id"]}.jpg', quote=True
        )
        media = (
            f'<a href="{entry_url}"><img src="{image_url}" alt="{name}" '
            'width="100%"></a>'
        )
        action = "点击预览图，在 ChatCut 中使用"
    else:
        poster_url = html.escape(entry["poster_url"], quote=True)
        video_url = html.escape(entry["preview_video_url"], quote=True)
        media = (
            f'<a href="{video_url}"><img src="{poster_url}" alt="{name}" '
            'width="100%"></a>'
        )
        action = f'<a href="{entry_url}">在 ChatCut 中使用 →</a>'

    return (
        '<td width="50%" valign="top">\n'
        f'{media}<br>\n'
        f'<strong>{name}</strong><br>\n'
        f'<sub>{description}</sub><br>\n'
        f'{action}\n'
        "</td>"
    )


def render_section(title: str, entries: list[dict[str, str]]) -> str:
    rows = []
    for index in range(0, len(entries), 2):
        cards = [render_card(entry) for entry in entries[index : index + 2]]
        if len(cards) == 1:
            cards.append('<td width="50%"></td>')
        rows.append("<tr>\n" + "\n".join(cards) + "\n</tr>")
    return f"## {title}\n\n<table>\n" + "\n".join(rows) + "\n</table>"


def generate_gallery(catalog: dict) -> str:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for entry in catalog["entries"]:
        grouped[section_for(entry)].append(entry)

    sections = [
        render_section(section, grouped[section])
        for section in SECTION_ORDER
        if grouped[section]
    ]
    total = catalog["count"]
    synced_on = html.escape(catalog["synced_on"])
    source_url = html.escape(catalog["source_url"], quote=True)
    intro = f"""# ChatCut 官方 Prompt 视觉画廊

先看效果，再决定怎么剪。这里收录 **{total} 个官方效果**：104 个 Motion Graphics、14 个 Seedance 2 视频生成方案和 5 个 App Promo。

- 动效：点击预览图，直接在 ChatCut 中使用。
- 视频：点击封面观看官方预览，再进入 ChatCut 使用。

> 官方目录同步于 {synced_on}，来源：[ChatCut Prompt Library]({source_url})。
"""
    return intro + "\n" + "\n\n".join(sections) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--catalog", default="references/chatcut-official-catalog.json"
    )
    parser.add_argument("--output", default="VISUAL-GALLERY.md")
    args = parser.parse_args()

    catalog = json.loads(Path(args.catalog).read_text(encoding="utf-8"))
    output = Path(args.output)
    output.write_text(generate_gallery(catalog), encoding="utf-8")
    print(f"Wrote {output} with {catalog['count']} official entries")


if __name__ == "__main__":
    main()
