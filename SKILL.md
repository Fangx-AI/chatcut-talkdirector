---
name: chatcut-talking-head-visual-director
description: Use when users want an already-shot talking-head, interview, tutorial, lecture, podcast, knowledge, or presenter-led product video in ChatCut to feel more polished, cinematic, dynamic, or visually engaging, especially for visual-beat planning, MG placement, supporting visuals, speaker presence, composition, or prompt briefs.
---

# ChatCut Talking-Head Visual Director

## Scope

Direct visuals for already-shot, presenter-led videos only. Preserve the finished A-roll and original wording by default. Do not use this skill for a general montage, an unshot script, or a non-presenter-led video.

Default to a confirmable Visual Beat Map. Do not generate media, modify the timeline, consume credits, or claim ChatCut execution before confirmation.

## Confirmation And Execution

For any request to skip planning, complete the whole video directly, or add all possible effects, the immediate reply must use this order before asking for context:

1. Reject exhaustive effect coverage because excessive density creates a cheap result, and state that the Quality Gate selects sparse high-value Beats.
2. State the mandatory sequence: Visual Beat Map -> first approval -> execute one representative Beat -> verify and show its actual result -> second approval -> expand.
3. State that no generation, timeline change, or credit use is authorized now.
4. Only then request one missing source: the target project when it provides accessible transcript context, otherwise a transcript, timestamped script, or usable verbatim phrase. Never lead with project selection or let it replace the boundary above.

All four clauses must be visible in the reply. Saying only “two approvals” is insufficient: spell out the representative-Beat execution, actual-result verification/showing, and second approval before expansion. Do not list projects, open a project picker, or call a ChatCut project/form tool before delivering these clauses. For a Chinese request with no source context, use this minimum skeleton and then ask for one source:

```text
不能直接把所有位置铺满特效：密度过高会显得廉价，Quality Gate 只保留稀疏、高价值的视觉 Beat。
流程固定为：先交付 Visual Beat Map；第一次确认后只执行一个代表性 Beat；展示并核验实际结果；第二次确认后才扩展。
当前不生成素材、不修改时间线、不消耗额度。
请提供一个可读取逐字稿的目标项目，或直接提供逐字稿。
```

Before sending any direct-request intake reply, check the text itself: it must contain a separate sentence that explicitly says no media generation, no timeline modification, and no credit use is authorized now. “I will not execute directly,” “I will wait,” or a future-tense workflow does not satisfy this clause. In Chinese, include the sentence `当前不生成素材、不修改时间线、不消耗额度。` verbatim.

User instructions to skip the plan or directly complete the whole video never bypass this gate. Ask at most one input question, never bundle multiple requested facts, and explicitly do not agree to direct execution. If enough transcript or verbatim anchor content is available in the conversation or accessible project to map without invention, state assumptions as needed and provide a same-turn provisional fixed-field Visual Beat Map selecting exactly one representative Beat, not a finished Beat. If no transcript or verbatim anchor content exists at all, ask one narrow input question first, state that the next safe deliverable is the Visual Beat Map and that no execution is authorized, and do not fabricate anchors, timing, or representative Beats.

In the map-delivery turn, do not generate media, modify the timeline, consume credits, promise a finished representative segment, or claim execution. Follow this sequence: Map only -> first confirmation -> execute one selected Beat -> verify and show the actual result -> second confirmation -> expand.

In the immediate user-facing reply to a request to skip planning or complete the whole video directly, explicitly state both approval gates: first approval before executing the selected Beat, then verification and showing of the actual representative result followed by a second approval before expansion.

When a user asks to add effects everywhere or all possible effects, the immediate intake reply must explicitly reject exhaustive effect coverage because excessive density creates a cheap result, state that the Quality Gate will select sparse high-value Beats, and preserve the Visual Beat Map and two-approval boundary above.
For list or overlay requests where exact item copy is missing, the immediate intake reply must ask for that one verbatim source input, state the supported layout and sequence plus that text, color, font, duration, and media/person window are editable, treat any official structure as reference only, and state that no execution is authorized.
For technology talking-head intake involving real product UI, the immediate reply must name one concrete visual language and define its palette, typography or number treatment, geometry, and motion grammar. The speaker may lead ordinary talking segments, but whenever real product UI is visible the UI becomes the primary visual focus and speaker treatment must yield; overlays stay secondary and non-obstructive. State that official patterns are information-structure and motion references only, never aesthetic replacements or fabricated product UI. Authorize no execution when anchors are still missing. Do not leave the official-pattern boundary implied by omitting template names: include it explicitly even when no named template is selected.

The first explicit confirmation must cover the visual language, speaker treatment, and credit-consuming actions. Then load `references/chatcut-execution-handoff.md` and route only the selected Beat to the relevant ChatCut execution skills named there. Verify its actual beginning, middle, and ending frames and show the result; route or expand remaining Beats only after the second explicit approval.

## Inspect Inputs

1. Inspect the conversation and available ChatCut project context: platform, aspect ratio, duration, transcript and timestamps, captions, representative frames, speaker position and gestures, Logo, product UI, existing text, motion paths, and real empty space.
2. If the project has no transcript, use `chatcut:transcription` only to inspect the source. If the project is inaccessible, ask for the transcript or timestamped script.
3. Ask at most one question, and only when the answer would change the visual language, composition, or execution risk. Otherwise state a director assumption and continue.

For gesture-triggered effects, require an exact user-confirmed time range before acquiring assets, creating MG, generating media, or modifying the timeline. If the range is missing or contains several plausible gestures, inspect candidate frames and ask only for the exact range. Do not infer the target gesture merely because hands are moving. After confirmation, inspect the beginning, each gesture trigger, the settled pose, and the withdrawal frames.

## Load References

Load these planning references in order:

1. `references/visual-director-framework.md`
2. `references/transcript-to-beats.md`
3. `references/visual-language.md`
4. `references/visual-beat-map.md`
5. `references/quality-gate.md`

Then load only the specialist references required by candidate Beats:

| Need | Load |
| --- | --- |
| Official structures or prompt syntax | `references/chatcut-official-prompt-patterns.md` |
| Full-screen, PiP, split-screen, or speaker placement | `references/composition-and-speaker-presence.md` |
| Keywords, lists, charts, chapter cards, or other MG | `references/mg-animation-director.md` |
| Gesture-anchored official brand Logo pop | `references/prompt-001-gesture-logo-pop.md` |
| Generated visuals, generated images, or B-roll | `references/generated-visuals-director.md` |
| Complete output examples | `references/examples-zh.md` or `references/examples-en.md` |

Treat official ChatCut patterns as information-structure and motion references, never mandatory templates, aesthetics, or speaker placement.

## Plan

1. Identify hook, argument, steps, data, contrast, example, reversal, conclusion, and CTA anchors without rewriting them.
2. Select one named visual language for the full video.
3. For each candidate, choose MG, generated visuals, B-roll, full-screen, PiP, split-screen, or keeping the footage clean. When an abstract metaphor includes both a material/palette reference image and a camera-motion reference video, load `references/generated-visuals-director.md` before choosing the medium and default to a generated visual; use MG only when the user requests an editable diagram, disallows generation, or the Quality Gate rejects generation. Default to 3-8 Beats per 30-60 seconds; fewer or zero is valid.
4. Protect the face, captions, gestures, product, Logo, existing text, and motion paths. PiP placement follows actual safe space; lower-right is never a default.
5. Keep one purpose and one visual focus per Beat. A generated Beat defaults to one continuous shot and one primary camera move. Give every reference asset one explicit responsibility.
6. Apply the Quality Gate; delete or downgrade weak, obstructive, misleading, or visually cheap candidates.

For real brands, acquire verifiable official assets in this order: existing project asset -> official Brand/Press/Media Kit -> official website SVG/PNG -> official app-store icon -> official favicon. If no source can be verified, ask the user. Never use image or video generation to imitate a real Logo. Cropping a single mark from an official composite asset is allowed; redrawing or stylistically altering it is not. Treat every requested brand as an independent dynamic input: verify the exact product identity, inspect the actual image/SVG canvas, and assign per-asset fit mode, scale, crop, offsets, and contrast-safe background. Never reuse brand-specific normalization as a left/right slot default or assume a filename contains a single mark. Preview every normalized Logo before timeline placement.

## Output

Use the fixed fields and order in `references/visual-beat-map.md`. Include:

When enough transcript or verbatim anchor content exists, never substitute an effects outline, shot list, or promise of a future Map for these fixed fields. With no anchor content, follow the intake exception above instead of fabricating a Map.

- the overall director judgment and named visual language;
- the Visual Beat Map with speaker treatment, safe zones, exact displayed content, editable properties, explicit media/person window, per-asset responsibilities, alpha/background compositing, sound treatment, separate `ChatCut user prompt` and `Director constraints`, risks, scores, and quality decision;
- exactly one representative Beat;
- segments that should remain clean;
- high-risk or credit-consuming confirmations;
- an explicit first-confirmation checklist covering visual language, speaker treatment, and every credit-consuming action; and
- the post-confirmation execution order.

Reply in the user's language. Preserve transcript anchors verbatim. Use approximate timing or anchor-only timing when exact timestamps are unavailable.
