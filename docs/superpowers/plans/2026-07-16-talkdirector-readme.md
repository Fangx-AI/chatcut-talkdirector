# ChatCut TalkDirector README Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and publish a premium, image-led GitHub README for ChatCut TalkDirector, then rename the public repository and local checkout without breaking Skill installation.

**Architecture:** Image 2 generates a text-free presenter source plate. Exact product typography and production overlays are composed deterministically into the final hero, while supporting diagrams remain code-native SVG assets for crisp GitHub rendering. The README is Chinese-first, links to the existing Skill contract, and makes only claims proven by the tracked tests.

**Tech Stack:** Markdown, Image 2 built-in image generation, SVG, HTML/CSS composition, Playwright screenshots, PowerShell, Git, GitHub CLI.

## Global Constraints

- Product name is **ChatCut TalkDirector**; Chinese name is **ChatCut 口播导演**.
- Repository name becomes `chatcut-talkdirector`.
- Keep the Skill identifier `chatcut-talking-head-visual-director` unchanged.
- Use the lines **读懂口播，导演画面。** and **Read the words. Direct the visuals.**
- Visual palette is ink black, warm ivory, signal green, and a small REC red accent.
- The hero must show an already-shot talking-head presenter as the first visual signal.
- Do not create fake ChatCut UI or claim a real render, timeline edit, or credit-consuming action.
- Keep the factual claims `9/9 scenarios` and `12 references`.
- Lower-right PiP is never presented as the default.
- Image 2 generates the presenter/source plate without embedded text.

---

### Task 1: Image 2 Presenter Source Plate

**Files:**
- Create: `assets/talkdirector-presenter.png`
- Create ignored evidence: `.superpowers/sdd/readme-assets/image2-prompt.md`

**Interfaces:**
- Consumes: no repository image assets.
- Produces: a text-free 16:9 presenter photograph used by the hero compositor.

- [ ] **Step 1: Record the exact generation prompt**

Write this prompt to the ignored evidence file:

```text
Use case: ads-marketing
Asset type: GitHub README masthead source plate
Primary request: a premium editorial photograph of a confident East Asian creator delivering a talking-head explanation to camera in a modern, restrained studio
Scene/backdrop: ink-black acoustic studio with subtle warm practical depth, no visible equipment
Subject: one presenter, waist-up, natural expressive hand gesture, direct eye contact, credible educator/creator rather than influencer glamour
Style/medium: high-end editorial photography, realistic skin and fabric, professional commercial post-production
Composition/framing: subject on the right third, generous clean negative space on the left, 16:9 landscape, eye line near upper third
Lighting/mood: warm ivory key light, soft controlled rim, calm authority, sharp face and hands
Color palette: ink black, warm ivory, restrained signal green wardrobe detail, tiny muted red accent
Constraints: no text, no letters, no logos, no watermark, no UI, no subtitles, no microphones, no camera equipment, no extra people, no holograms, no neon, no blue-purple gradient, no glow
```

- [ ] **Step 2: Generate with the built-in Image 2 path**

Use `image_gen__imagegen` with the prompt above and no reference images. Copy the generated result from the reported Codex generated-images location into `assets/talkdirector-presenter.png`.

- [ ] **Step 3: Inspect the source plate**

Run the local image viewer on `assets/talkdirector-presenter.png`.

Expected: one credible presenter; face and both visible hands are anatomically sound; left half has clean negative space; no text, watermark, fake interface, neon, or equipment.

- [ ] **Step 4: Reject or accept**

If any expected condition fails, regenerate once with only the failed condition tightened. Keep only the accepted source plate in `assets/`.

- [ ] **Step 5: Commit the accepted source plate**

```powershell
git add assets/talkdirector-presenter.png
git commit -m "feat: add TalkDirector presenter artwork"
```

Expected: one new tracked raster asset and a clean worktree.

### Task 2: Brand Masthead And Visual System

**Files:**
- Create: `assets/hero.png`
- Create: `assets/directing-flow.svg`
- Create: `assets/composition-atlas.svg`
- Create: `assets/quality-gate.svg`
- Create: `assets/visual-beat-map.svg`
- Create ignored render source: `.superpowers/sdd/readme-assets/hero.html`

**Interfaces:**
- Consumes: `assets/talkdirector-presenter.png`.
- Produces: five README-ready visual assets with one shared design system.

- [ ] **Step 1: Build the hero compositor**

Create a 2400 × 1000 HTML canvas with:

- ink-black `#0B0C0D` background;
- presenter photograph cropped on the right 52%;
- left title `ChatCut\nTalkDirector` in warm ivory `#F2EBDD`;
- subtitle `读懂口播，导演画面。`;
- eyebrow `TALKING-HEAD VISUAL DIRECTION`;
- signal green `#B7F34A` for Beat markers;
- REC red `#E6503C` for one recording indicator;
- footer labels `READ · ROUTE · DIRECT · VERIFY`;
- right-side caption safe-area frame, sparse waveform, and three Beat ticks;
- no gradients, glow, fake editor controls, or unreadable microcopy.

- [ ] **Step 2: Render the hero**

Use Playwright at device scale factor 2 to screenshot only the 2400 × 1000 hero element into `assets/hero.png`.

Expected: exact title and Chinese line; presenter remains the primary visual signal; no text clipping at 2400 px or when displayed at 800 px.

- [ ] **Step 3: Author the four supporting SVGs**

Use a fixed `viewBox="0 0 1600 900"`, internal CSS, `<title>`, and `<desc>`.

- `directing-flow.svg`: `逐字稿 → 导演判断 → 保留人物 / MG / 生成画面 / 分屏 / 全屏`.
- `composition-atlas.svg`: four labeled frames, `原画面`, `分屏`, `自适应 PiP`, `短暂全屏`; place PiP in a different safe region per frame.
- `quality-gate.svg`: overloaded effects on the left crossed out; sparse high-value Beats on the right accepted.
- `visual-beat-map.svg`: one truthful planning example with anchor, purpose, medium, speaker treatment, prompt, risk, and approval state.

All SVGs use the hero palette and no external fonts or resources.

- [ ] **Step 4: Render and inspect every asset**

Open `hero.png` and each SVG at original detail. Also render the SVGs at 800 px width.

Expected: no blank canvas, clipping, overlapping labels, malformed Chinese, or unreadable mobile text.

- [ ] **Step 5: Run asset checks**

```powershell
$expected = @(
  'assets/hero.png',
  'assets/talkdirector-presenter.png',
  'assets/directing-flow.svg',
  'assets/composition-atlas.svg',
  'assets/quality-gate.svg',
  'assets/visual-beat-map.svg'
)
$missing = $expected | Where-Object { -not (Test-Path -LiteralPath $_) }
if ($missing) { throw "Missing assets: $($missing -join ', ')" }
rg -n "TODO|TBD|PLACEHOLDER|linearGradient|filter=|feGaussianBlur" assets
```

Expected: all six assets exist; `rg` returns no matches.

- [ ] **Step 6: Commit the visual system**

```powershell
git add assets/hero.png assets/directing-flow.svg assets/composition-atlas.svg assets/quality-gate.svg assets/visual-beat-map.svg
git commit -m "feat: add TalkDirector README visual system"
```

### Task 3: Premium GitHub README

**Files:**
- Create: `README.md`
- Reference: `SKILL.md`
- Reference: `tests/forward-results.md`
- Reference: `references/visual-beat-map.md`
- Reference: `references/quality-gate.md`

**Interfaces:**
- Consumes: the five visual assets from Task 2 and factual repository data.
- Produces: the GitHub project front page.

- [ ] **Step 1: Write the masthead and navigation**

The opening must contain:

```markdown
<div align="center">

![ChatCut TalkDirector — 读懂口播，导演画面](assets/hero.png)

# ChatCut TalkDirector

**Read the words. Direct the visuals.**<br>
**读懂口播，导演画面。**

专门为已经拍好的口播视频做视觉导演：读懂文案，再判断何时保留人物、加入 MG、补充生成画面、改变构图，或让画面保持干净。

[![Scenarios](https://img.shields.io/badge/scenarios-9%2F9-B7F34A?style=flat-square&labelColor=0B0C0D)](#验证)
[![References](https://img.shields.io/badge/references-12-F2EBDD?style=flat-square&labelColor=0B0C0D)](references)
[![Skill](https://img.shields.io/badge/skill-ChatCut-E6503C?style=flat-square&labelColor=0B0C0D)](SKILL.md)

[为什么](#为什么需要它) · [怎么工作](#怎么工作) · [视觉判断](#视觉判断) · [示例](#visual-beat-map-示例) · [安装](#安装)

</div>
```

- [ ] **Step 2: Write the problem and directing model**

Explain in no more than six short paragraphs:

- already-shot talking-head videos often have strong content but repetitive visuals;
- adding effects everywhere makes the result cheaper and harder to follow;
- TalkDirector reads transcript anchors and routes each high-value moment;
- the visual follows the meaning;
- one representative Beat is executed and verified before expansion;
- planning never authorizes generation, timeline changes, or credit use.

Place `assets/directing-flow.svg` after the routing explanation.

- [ ] **Step 3: Write the visual judgment section**

Use a compact table with these rows:

| Route | Use when | Speaker |
| --- | --- | --- |
| 保持人物 | 表情、信任和语气更重要 | 全幅保留 |
| MG | 关键词、步骤、关系或数字需要解释 | 原画面、分屏或透明叠加 |
| 生成画面 | 抽象隐喻或缺少可用画面 | 短暂全屏或分屏 |
| B-roll | 有真实素材可以补充事实 | 人物让位 |
| 保持干净 | 视觉不会增加理解 | 不加效果 |

Show `composition-atlas.svg` and state that lower-right PiP is a candidate, never a default.

- [ ] **Step 4: Write Quality Gate and example sections**

Show `quality-gate.svg` and summarize:

- one purpose and one visual focus per Beat;
- no more than two cheap effect families in one Beat;
- protect face, captions, gestures, product, Logo, and motion paths;
- generated Beat defaults to one continuous shot and one primary camera move.

Show `visual-beat-map.svg`, then link to `references/examples-zh.md` and `references/examples-en.md`.

- [ ] **Step 5: Write install, invocation, repository map, validation, and limitations**

Use these exact install commands:

```powershell
git clone https://github.com/Fangx-AI/chatcut-talkdirector.git
New-Item -ItemType Junction `
  -Path "$HOME\.codex\skills\chatcut-talking-head-visual-director" `
  -Target "$(Resolve-Path .\chatcut-talkdirector)"
```

Invocation:

```text
使用 $chatcut-talking-head-visual-director 分析这条口播，
先输出可确认的 Visual Beat Map，不要直接生成或修改时间线。
```

State that the repository contains one root Skill, 12 focused references, Chinese and English examples, and nine behavior scenarios. State that live ChatCut timeline execution and credit-gating are not covered by the repository's offline behavior evidence.

- [ ] **Step 6: Validate README claims and links**

```powershell
$readme = Get-Content -Raw -Encoding utf8 README.md
@(
  'assets/hero.png',
  'assets/directing-flow.svg',
  'assets/composition-atlas.svg',
  'assets/quality-gate.svg',
  'assets/visual-beat-map.svg',
  'SKILL.md',
  'references/examples-zh.md',
  'references/examples-en.md'
) | ForEach-Object {
  if ($readme -notmatch [regex]::Escape($_)) { throw "README missing link: $_" }
}
if ($readme -notmatch '9/9' -or $readme -notmatch '12') { throw 'README missing factual validation counts' }
```

Expected: exit 0.

- [ ] **Step 7: Commit the README**

```powershell
git add README.md
git commit -m "docs: launch ChatCut TalkDirector"
```

### Task 4: Repository And Installation Rename

**Files:**
- Modify remote repository metadata.
- Move local directory from `C:\Users\PC\Documents\Skill\chatcut-talking-head-visual-director` to `C:\Users\PC\Documents\Skill\chatcut-talkdirector`.
- Recreate junction `C:\Users\PC\.codex\skills\chatcut-talking-head-visual-director`.

**Interfaces:**
- Consumes: clean committed `main` branch.
- Produces: public repository `Fangx-AI/chatcut-talkdirector`, matching local checkout, and a working installed Skill path.

- [ ] **Step 1: Push tracked README work before renaming**

```powershell
git push origin main
```

Expected: remote accepts all new commits.

- [ ] **Step 2: Rename the GitHub repository**

```powershell
gh repo rename chatcut-talkdirector --repo Fangx-AI/chatcut-talking-head-visual-director --yes
git remote set-url origin https://github.com/Fangx-AI/chatcut-talkdirector.git
gh repo edit Fangx-AI/chatcut-talkdirector `
  --description "ChatCut TalkDirector reads talking-head scripts and directs motion graphics, generated visuals, speaker composition, and clean visual beats."
```

Expected: `gh repo view Fangx-AI/chatcut-talkdirector` reports a public repository with default branch `main`.

- [ ] **Step 3: Verify absolute local move paths**

```powershell
$source = [IO.Path]::GetFullPath('C:\Users\PC\Documents\Skill\chatcut-talking-head-visual-director')
$target = [IO.Path]::GetFullPath('C:\Users\PC\Documents\Skill\chatcut-talkdirector')
$root = [IO.Path]::GetFullPath('C:\Users\PC\Documents\Skill')
if (-not $source.StartsWith($root) -or -not $target.StartsWith($root)) { throw 'Move escaped workspace root' }
if (-not (Test-Path -LiteralPath $source)) { throw 'Source checkout missing' }
if (Test-Path -LiteralPath $target) { throw 'Target checkout already exists' }
```

Expected: exit 0.

- [ ] **Step 4: Move the checkout and recreate the junction**

Run from `C:\Users\PC\Documents\Skill`:

```powershell
Move-Item -LiteralPath 'C:\Users\PC\Documents\Skill\chatcut-talking-head-visual-director' `
  -Destination 'C:\Users\PC\Documents\Skill\chatcut-talkdirector'

$installed = 'C:\Users\PC\.codex\skills\chatcut-talking-head-visual-director'
$item = Get-Item -LiteralPath $installed -Force
if ($item.LinkType -ne 'Junction') { throw 'Installed path is not a junction' }
Remove-Item -LiteralPath $installed
New-Item -ItemType Junction -Path $installed `
  -Target 'C:\Users\PC\Documents\Skill\chatcut-talkdirector'
```

Expected: local checkout exists under the new name and installed Skill junction targets it.

### Task 5: Final Rendering And Publication Verification

**Files:**
- Verify: `README.md`
- Verify: `assets/*`
- Verify: installed junction and GitHub repository.

**Interfaces:**
- Consumes: published renamed repository and all final assets.
- Produces: verified public GitHub front page.

- [ ] **Step 1: Run local Skill and repository checks**

```powershell
$env:PYTHONUTF8 = '1'
$env:PYTHONPATH = (Resolve-Path '.superpowers\sdd\python-deps').Path
& 'C:\Users\PC\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  'C:\Users\PC\.codex\skills\.system\skill-creator\scripts\quick_validate.py' .
git diff --check
git status --short --branch
```

Expected: `Skill is valid!`, no diff errors, and `main...origin/main` with no changes.

- [ ] **Step 2: Re-run the privacy and history scan**

```powershell
$hits = git log --all --format=%H | ForEach-Object {
  git grep -n -I -E '<private-domain>|<private-project-name>|<private-project-id>' $_ -- 2>$null
}
if ($hits) { $hits; throw 'Sensitive string found in reachable history' }
```

Expected: no matches.

- [ ] **Step 3: Verify local and remote identity**

```powershell
$local = git rev-parse HEAD
$remote = (git ls-remote origin refs/heads/main).Split()[0]
if ($local -ne $remote) { throw 'Local and remote HEAD differ' }
gh repo view Fangx-AI/chatcut-talkdirector `
  --json nameWithOwner,url,visibility,defaultBranchRef,description
```

Expected: local and remote SHA match; repository is public and named `Fangx-AI/chatcut-talkdirector`.

- [ ] **Step 4: Open and inspect the public GitHub page**

Open `https://github.com/Fangx-AI/chatcut-talkdirector` in a browser at desktop and mobile widths.

Expected:

- hero loads and remains readable;
- no broken images or links;
- first viewport communicates talking-head specialization;
- text does not overflow or overlap;
- anchor navigation works;
- no claim implies completed live ChatCut execution.

- [ ] **Step 5: Record final verification**

Update the task plan to complete and report:

- public repository URL;
- local checkout path;
- installed Skill path;
- generated asset list;
- validation results;
- residual gap that live ChatCut execution was not run.
