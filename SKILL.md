---
name: cut-director
description: Direct already-shot talking-head, interview, tutorial, lecture, podcast, knowledge, and presenter-led product videos in ChatCut. Use when a user describes a desired visual effect or asks to make speech-led footage more polished, dynamic, cinematic, clear, or visually engaging through visual-beat planning, motion graphics, supporting visuals, speaker composition, reusable CutDirector Prompts, or verified ChatCut execution.
---

# CutDirector

## Scope

Direct visuals for already-shot, presenter-led videos. Preserve finished A-roll and original wording by default. Do not use this Skill for a general montage, an unshot script, or a non-presenter-led video.

Let the user describe the result in natural language. Never ask the user to fill an internal schema, recipe, crop parameter, animation curve, or verification checklist.

## Core Workflow

1. Inspect the source, transcript, timing, frame, speaker, gestures, captions, Logo, product UI, existing text, motion paths, and real empty space.
2. Load the planning references in the order below. Identify verbatim anchors and select sparse, high-value visual Beats.
3. Match a verified effect recipe when its viewing task and constraints fit. Otherwise design a custom Beat using the same safety and fallback principles.
4. Deliver a confirmable Visual Beat Map and select exactly one representative Beat.
5. After the first approval, initialize or resume the project manifest and pass every recipe gate before executing only the representative Beat.
6. Record actual post-write evidence, reach `verified`, and show the result. Expand only after the second explicit approval.

The model owns semantics, director judgment, visual language, and medium choice. Deterministic scripts own required fields, IDs, time ranges, approval state, asset verification state, fallback chains, and evidence completeness. Read `references/pipeline-contract.md` before execution.

## Confirmation Boundary

Do not generate media, create MG, modify the timeline, consume credits, or claim execution before the first approval.

For a request to skip planning, finish the whole video immediately, or add effects everywhere, respond in this order:

1. Reject exhaustive effect coverage because excessive density looks cheap; state that the Quality Gate keeps sparse, high-value Beats.
2. State the complete sequence: Visual Beat Map -> first approval -> execute one representative Beat -> verify and show its actual result -> second approval -> expand.
3. State in a separate sentence that no generation, timeline change, or credit use is authorized now.
4. Request one missing source only: a target project with readable transcript context, a transcript, a timestamped script, or one usable verbatim phrase.

For Chinese intake with no source context, include this sentence verbatim:

```text
当前不生成素材、不修改时间线、不消耗额度。
```

Do not open a project picker or call a ChatCut project/form tool before stating this boundary. Project selection is source intake, not execution approval.

If no transcript or verbatim anchor exists, ask one narrow source question and stop at intake. Do not invent timing, anchors, facts, or a representative Beat. State that the Visual Beat Map is the next safe deliverable.

## Recipe Routing

Load only the matching recipe and its public reference:

| User intent | Internal recipe | Public compatibility path |
| --- | --- | --- |
| Official Logo follows a confirmed pointing gesture | `recipes/prompt-001-gesture-logo-pop.json` | `references/prompt-001-gesture-logo-pop.md` |
| Left-side points plus a continuously scrolling long-text evidence column | `recipes/prompt-002-split-screen-explainer.json` | `references/prompt-002-split-screen-explainer.md` |
| One official brand icon connects two product modes, with progressive capabilities and a final result comparison | `recipes/prompt-003-brand-mode-comparison.json` | `references/prompt-003-brand-mode-comparison.md` |
| A persistent top rail shows the active chapter while one global progress line fills continuously across the full program | `recipes/prompt-004-top-chapter-progress-rail.json` | `references/prompt-004-top-chapter-progress-rail.md` |

Treat recipe triggers as routing evidence, not keyword-only commands. A visual resemblance is insufficient when the viewing task differs.

Apply the recipe's required inputs, asset strategy, safe zones, timing, fallback chain, and verification rules internally. Keep the published Prompt text and paths stable. If a recipe blocks execution, follow its named fallback rather than improvising around the guardrail.

For gesture effects, require a user-confirmed exact time range before asset acquisition or timeline work. If several gestures are plausible, inspect candidate frames and ask only for the exact target range. Do not equate any moving hand with an intentional trigger.

For real brands, use verifiable official assets and never generate, redraw, or stylistically imitate a real Logo. If identity or provenance cannot be verified, stop that asset and request one verified source.

## Planning References

Load in this order:

1. `references/visual-director-framework.md`
2. `references/transcript-to-beats.md`
3. `references/visual-language.md`
4. `references/visual-beat-map.md`
5. `references/quality-gate.md`

Then load only what the selected Beats need:

| Need | Load |
| --- | --- |
| Official Prompt lookup or reuse | `references/chatcut-official-catalog.md`, `references/chatcut-prompt-routing.md`, `references/chatcut-official-prompt-patterns.md` |
| Full-screen, PiP, split-screen, or speaker placement | `references/composition-and-speaker-presence.md` |
| Keywords, lists, charts, chapter cards, or other MG | `references/mg-animation-director.md` |
| Generated visuals, images, or B-roll | `references/generated-visuals-director.md` |
| Full examples | `references/examples-zh.md` or `references/examples-en.md` |

Treat official ChatCut patterns as information-structure and motion references, never mandatory aesthetics, fabricated product UI, or automatic speaker placement.

## Director Rules

- Preserve transcript anchors verbatim. Use approximate or anchor-only timing when exact timestamps are unavailable.
- Default to 3-8 Beats per 30-60 seconds; fewer or zero is valid.
- Keep one purpose and one visual focus per Beat. A generated Beat defaults to one continuous shot and one primary camera move.
- Protect face, captions, gestures, product, Logo, existing text, and motion paths. Lower-right PiP is never a default.
- Let real product UI become the primary focus whenever visible; keep overlays secondary and non-obstructive. Never fabricate product UI as evidence.
- Give every reference asset one explicit responsibility.
- Apply the Quality Gate. Delete or downgrade weak, obstructive, misleading, visually cheap, or unverifiable candidates.

## User-Facing Output

Use the fixed order and fields in `references/visual-beat-map.md`. Include:

- overall director judgment and one named visual language;
- the Visual Beat Map with exact displayed content, speaker treatment, safe zones, editable properties, media/person window, asset responsibilities, compositing, sound, user prompt, director constraints, risks, scores, and quality decision;
- exactly one representative Beat;
- segments that should remain clean;
- high-risk or credit-consuming confirmations;
- a first-approval checklist covering visual language, speaker treatment, and every credit-consuming action; and
- the post-approval execution order.

Reply in the user's language. Present the result, not the internal recipe or JSON contract.

## Execution And Validation

After the first approval, read `references/chatcut-execution-handoff.md` and route only the representative Beat to the required ChatCut execution Skills.

Use the internal cache and state flow in `references/pipeline-contract.md`. Before every ChatCut write, merge known facts and require an `executing` transition. After the write, record actual asset, beginning, middle, and ending evidence and require a `verified` transition. For any Beat that covers or replaces the speaker frame, beginning and ending evidence must include the clean frame outside the Beat, the transition in progress, and the settled state; a good middle frame does not prove a clean handoff.

Never expose the manifest, commands, gates, or recovery mechanics as user work. Do not override a validation failure: fix a known fact, apply a documented fallback, or ask for the single blocking input. Show the verified result and wait for the second approval before expansion.
