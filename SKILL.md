---
name: chatcut-talking-head-visual-director
description: Use when users want an already-shot talking-head, interview, tutorial, lecture, podcast, knowledge, or presenter-led product video in ChatCut to feel more polished, cinematic, dynamic, or visually engaging, especially for visual-beat planning, MG placement, supporting visuals, speaker presence, composition, or prompt briefs.
---

# ChatCut Talking-Head Visual Director

## Scope

Direct visuals for already-shot, presenter-led videos only. Preserve the finished A-roll and original wording by default. Do not use this skill for a general montage, an unshot script, or a non-presenter-led video.

Default to a confirmable Visual Beat Map. Do not generate media, modify the timeline, consume credits, or claim ChatCut execution before confirmation.

## Confirmation And Execution

User instructions to skip the plan or directly complete the whole video never bypass this gate. Ask at most one input question, never bundle multiple requested facts, and explicitly do not agree to direct execution. If enough transcript or verbatim anchor content is available in the conversation or accessible project to map without invention, state assumptions as needed and provide a same-turn provisional fixed-field Visual Beat Map selecting exactly one representative Beat, not a finished Beat. If no transcript or verbatim anchor content exists at all, ask one narrow input question first, state that the next safe deliverable is the Visual Beat Map and that no execution is authorized, and do not fabricate anchors, timing, or representative Beats.

In the map-delivery turn, do not generate media, modify the timeline, consume credits, promise a finished representative segment, or claim execution. Follow this sequence: Map only -> first confirmation -> execute one selected Beat -> verify and show the actual result -> second confirmation -> expand.

In the immediate user-facing reply to a request to skip planning or complete the whole video directly, explicitly state both approval gates: first approval before executing the selected Beat, then verification and showing of the actual representative result followed by a second approval before expansion.

The first explicit confirmation must cover the visual language, speaker treatment, and credit-consuming actions. Then load `references/chatcut-execution-handoff.md` and route only the selected Beat to the relevant ChatCut execution skills named there. Verify its actual beginning, middle, and ending frames and show the result; route or expand remaining Beats only after the second explicit approval.

## Inspect Inputs

1. Inspect the conversation and available ChatCut project context: platform, aspect ratio, duration, transcript and timestamps, captions, representative frames, speaker position and gestures, Logo, product UI, existing text, motion paths, and real empty space.
2. If the project has no transcript, use `chatcut:transcription` only to inspect the source. If the project is inaccessible, ask for the transcript or timestamped script.
3. Ask at most one question, and only when the answer would change the visual language, composition, or execution risk. Otherwise state a director assumption and continue.

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
| Generated visuals, generated images, or B-roll | `references/generated-visuals-director.md` |
| Complete output examples | `references/examples-zh.md` or `references/examples-en.md` |

Treat official ChatCut patterns as information-structure and motion references, never mandatory templates, aesthetics, or speaker placement.

## Plan

1. Identify hook, argument, steps, data, contrast, example, reversal, conclusion, and CTA anchors without rewriting them.
2. Select one named visual language for the full video.
3. For each candidate, choose MG, generated visuals, B-roll, full-screen, PiP, split-screen, or keeping the footage clean. Default to 3-8 Beats per 30-60 seconds; fewer or zero is valid.
4. Protect the face, captions, gestures, product, Logo, existing text, and motion paths. PiP placement follows actual safe space; lower-right is never a default.
5. Keep one purpose and one visual focus per Beat. A generated Beat defaults to one continuous shot and one primary camera move. Give every reference asset one explicit responsibility.
6. Apply the Quality Gate; delete or downgrade weak, obstructive, misleading, or visually cheap candidates.

## Output

Use the fixed fields and order in `references/visual-beat-map.md`. Include:

When enough transcript or verbatim anchor content exists, never substitute an effects outline, shot list, or promise of a future Map for these fixed fields. With no anchor content, follow the intake exception above instead of fabricating a Map.

- the overall director judgment and named visual language;
- the Visual Beat Map with speaker treatment, safe zones, separate `ChatCut user prompt` and `Director constraints`, risks, scores, and quality decision;
- exactly one representative Beat;
- segments that should remain clean;
- high-risk or credit-consuming confirmations; and
- the post-confirmation execution order.

Reply in the user's language. Preserve transcript anchors verbatim. Use approximate timing or anchor-only timing when exact timestamps are unavailable.
