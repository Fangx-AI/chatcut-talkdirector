<div align="center">

![CutDirector 顶部横幅](assets/hero.png)

# CutDirector

**专为已拍口播视频设计的 ChatCut 口播导演 Skill**

读懂逐字稿、人物动作和真实画面，在真正值得强化的时刻加入重点文字、Logo、图表、网页、分屏与补充画面。

你只需要描述想看到的结果。CutDirector 会先做一个可编辑的代表镜头，满意后再扩展到其他位置。

[![Verified Prompts](https://img.shields.io/badge/已验证_Prompt-003-E6503C?style=flat-square&labelColor=0B0C0D)](#已验证效果)
[![Official Effects](https://img.shields.io/badge/官方效果参考-123-B7F34A?style=flat-square&labelColor=0B0C0D)](VISUAL-GALLERY.md)
[![Made for ChatCut](https://img.shields.io/badge/为_ChatCut_打造-F2EBDD?style=flat-square&labelColor=0B0C0D)](https://chatcut.io/)

[查看真实效果与 Prompt](#已验证效果) · [30 秒开始](#30-秒开始) · [浏览效果参考库](VISUAL-GALLERY.md)

</div>

## 已验证效果

每个 Verified Prompt 都来自真实的 ChatCut 时间线：先完成、再验证，最后才公开为可复用 Prompt。

### Prompt 001 · 手势触发 Logo 弹出

[![Prompt 001 - 手势触发双侧官方 Logo 弹出](assets/verified-prompts/prompt-001-gesture-logo-pop.gif)](assets/verified-prompts/prompt-001-gesture-logo-pop.mp4)

**快速使用**

```text
当人物分别指向左右时，在左侧弹出 [品牌 A] 官方 Logo，右侧弹出 [品牌 B] 官方 Logo。先做这个片段给我看。
```

适合品牌对比、工具介绍和产品推荐。CutDirector 会在内部查找真实手势、验证官方素材、保护人物与字幕，并检查入场和退场。

<details>
<summary><strong>查看完整精确 Prompt</strong></summary>

```text
在 [时间段]，给人物两侧的指向手势添加 [品牌 A] 和 [品牌 B] 的官方 Logo 弹出特效：[品牌 A] 在画面左侧，[品牌 B] 在画面右侧，分别跟随对应手指抬起时弹出，手势结束时退场。请自动获取可验证的官方 Logo，保持人物全屏，不遮挡脸、字幕、手和产品，并先展示关键帧让我确认。
```

</details>

[查看 Prompt 001 的完整说明](references/prompt-001-gesture-logo-pop.md)

### Prompt 002 · 双栏讲解

[![Prompt 002 - 左侧要点逐条浮现，右侧长文本缓慢滚动](assets/verified-prompts/prompt-002-split-screen-explainer.gif)](assets/verified-prompts/prompt-002-split-screen-explainer.mp4)

**快速使用**

```text
把这段做成双栏讲解：左边按照口播依次出现重点，右边缓慢滚动完整资料。
```

适合 Prompt、代码、报告、合同和论文讲解。左侧负责结论，右侧只承担“完整材料正在流动”的证据作用。

<details>
<summary><strong>查看完整精确 Prompt</strong></summary>

```text
在 [时间段] 制作一段横屏双栏信息动效。左侧作为主视觉，显示标题「[标题]」，并让 [3-5 个要点] 按照叙述顺序逐条浮现：当前项高亮，历史项降低亮度保留，最后进入全部完成状态。右侧作为辅助信息区，放入 [完整长文本] 并让文字持续、匀速、缓慢地由下向上滚动。长文本不要求在视频结束前展示完，不要为了滚完全文而加快速度。右侧宽度不得超过画面的 45%，保持原视频时长和画幅，并先展示开始、中段和结束关键帧让我确认。
```

</details>

[观看 Prompt 002 演示视频](assets/verified-prompts/prompt-002-split-screen-explainer.mp4) · [查看完整说明](references/prompt-002-split-screen-explainer.md)

### Prompt 003 · 品牌双模式能力对比

[![Prompt 003 - 品牌图标贯穿普通模式与办公模式对比](assets/verified-prompts/prompt-003-brand-mode-comparison.gif)](assets/verified-prompts/prompt-003-brand-mode-comparison.mp4)

**快速使用**

```text
把这段做成品牌双模式对比：顶部保留官方图标，左边只放 [模式 A] 的一个核心能力，右边让 [模式 B] 的能力逐项落下，最后收束成「[能力 A] → [最终结果 B]」。使用纯黑背景和轻快卡点，图标不要单独淡出。
```

适合普通版与专业版、聊天模式与办公模式、免费版与付费版等双模式讲解。它用一个品牌图标维持身份连续性，以非对称信息量强调能力差异，并在结尾把多项功能压缩为一句结果。

<details>
<summary><strong>查看完整精确 Prompt</strong></summary>

```text
在 [时间段] 制作一段横屏全屏品牌双模式对比动效。

使用纯黑背景，顶部居中放置 [品牌] 的可验证官方图标。图标作为整段的品牌锚点，贯穿两个信息阶段，不要在中间转场时单独淡出或重新出现。

第一阶段并排展示两种模式：左侧标题「[模式 A]」，只保留一项核心能力「[能力 A]」；右侧标题「[模式 B]」，按照口播顺序依次出现 2-4 项能力。左侧使用中性灰弱化，右侧使用一个高亮强调色，不添加小号英文装饰。

第二阶段让第一阶段的标题和能力块一起退场，品牌图标保持稳定，然后把画面收束为「[能力 A] → [最终结果 B]」，下方补充一句「[总结句]」。音效使用轻、短、清脆的卡点，避免低沉 boom、机械拖尾和连续 whoosh。先展示第一阶段、能力递进、中间转场、最终结论和导出成片的实际第一帧让我确认；独立导出时，第一帧不得露出上一镜。
```

</details>

[观看 Prompt 003 演示视频](assets/verified-prompts/prompt-003-brand-mode-comparison.mp4) · [查看完整说明](references/prompt-003-brand-mode-comparison.md)

| Prompt | 观看任务 | 状态 |
| --- | --- | --- |
| **001** | 手势触发一个或多个官方品牌 Logo 弹出 | **已验证上线** |
| **002** | 左侧要点逐条浮现，右侧长文本缓慢滚动 | **已验证上线** |
| **003** | 品牌图标贯穿两种模式，能力递进后收束为结果对比 | **已验证上线** |

后续案例只在真实时间线中完成并通过验证后，才会加入这个系列。

## 30 秒开始

### 1. 安装 Skill

在 Codex 中使用 `$skill-installer` 安装：

```text
$skill-installer install https://github.com/Fangx-AI/cut-director
```

安装完成后重启 Codex。需要手动安装或参与开发时，请看[完整安装方式](#完整安装方式)。

### 2. 提供口播

打开目标 ChatCut 项目，或者提供已拍视频、逐字稿、时间段和你想强化的原句。

### 3. 说一句话

```text
使用 $cut-director 分析这条口播，找出最值得加画面的 3 个时刻，先做最值得的一个给我看。
```

CutDirector 会先给出少量高价值建议。只有在你确认后，才会生成素材、修改时间线或消耗额度。

## 你会得到什么

| 你提供 | CutDirector 交付 |
| --- | --- |
| 一条已拍口播或逐字稿 | 找出真正值得加入画面的时刻 |
| 一句自然语言需求 | 清晰、可确认的视觉方案 |
| “按这个做” | 一个真实、可编辑并经过验证的代表镜头 |
| “再大一点”“位置向右” | 延续当前结果做局部微调，不要求重填参数 |

CutDirector 不要求你填写裁切坐标、动画曲线、内部 Schema 或验证清单。缺少关键信息时，它只询问一个真正影响结果的问题。

## 直接开始

不知道该怎么做：

```text
分析这条口播，找出最值得加画面的 3 个时刻。
```

想探索不同风格：

```text
把这段口播做得更有科技感，给我 3 种明显不同的方案。
```

已经知道具体效果：

```text
“99%”出现时，从画面上方落下一个巨大的“99%”。
```

修改已有结果：

```text
这个框的位置不对，重新对准真正的搜索区域。
```

后续可以直接说“按第二版做”“字再大一点”“再给我两种风格”或“满意，继续其他位置”，不需要重新复制完整 Prompt。

## 不堆效果，只强化理解

![效果堆叠与高价值 Beat 对比](assets/quality-gate.jpg)

CutDirector 不追求“特效更多”。它会保留能够增加理解、强化焦点并保护人物表达的高价值时刻，也允许画面在不需要特效时保持干净。

## 它能为口播加什么

| 观看任务 | CutDirector 的处理 |
| --- | --- |
| 强调产品或品牌 | 图标、Logo、产品卡跟随手势或语义出现 |
| 解释关键词和步骤 | 关键词卡、编号列表、流程与对比动画 |
| 呈现数据和证据 | 柱状图、折线图、雷达图、数字计数器 |
| 切换章节和身份 | 章节标题、人物介绍、字幕条、引用卡 |
| 原画面不够 | 生成补充画面、B-roll、分屏或全屏视觉 |
| 画面已经足够强 | 保持人物与原画面干净，不为特效而特效 |

## 它如何工作

1. **读懂内容**：检查逐字稿、时间、人物、手势、字幕、产品界面和真实空白区域。
2. **先给方案**：选择少量高价值视觉时刻，并说明最值得先做哪一个。
3. **先做一个**：确认后制作一个代表镜头，展示真实开始、中段与结束画面。
4. **自然微调**：继续用自然语言修改；满意后再扩展到其他位置。

<details>
<summary><strong>查看导演判断、构图与视觉节奏</strong></summary>

### 导演判断

![逐字稿、语义锚点与导演判断流程](assets/directing-flow.jpg)

先读逐字稿和语义锚点，再决定保持人物、加入 MG、生成画面、使用 B-roll，或者让画面保持干净。

### 构图图谱

![口播视频构图图谱与安全区](assets/composition-atlas.jpg)

人物全幅、人物让位、分屏解释和画面接管不是固定模板，而是根据内容、手势、字幕与安全区做出的导演选择。

### 视觉节奏地图

![口播视频视觉节奏地图](assets/visual-beat-map.jpg)

每个视觉 Beat 都绑定原文锚点、视觉目的、画面手段、人物处理、风险与确认状态，让整条视频有节奏而不是随机加效果。

</details>

## 官方效果参考库

CutDirector 可以参考 ChatCut 官方 Prompt Library 的信息结构和动效模式，再根据真实人物、字幕和安全区重新导演。官方参考不等于已验证 Recipe；只有上方 Verified Prompt Series 中的效果已经完成真实时间线验证。

<table>
<tr>
<td width="50%" valign="top">
<a href="https://app.chatcut.io/?source=prompt-library&target=motion-graphics&template=8303fddb-dba0-474b-a1cc-58f40728482b"><img src="assets/official-gallery/8303fddb-dba0-474b-a1cc-58f40728482b.jpg" alt="编号要点与口播人物" width="100%"></a><br>
<strong>编号要点 + 口播人物</strong><br>
人物保留在右侧，左侧依次弹出重点列表。
</td>
<td width="50%" valign="top">
<a href="https://app.chatcut.io/?source=prompt-library&target=motion-graphics&template=e816057d-bd49-4a82-880c-d4555a9c1dce"><img src="assets/official-gallery/e816057d-bd49-4a82-880c-d4555a9c1dce.jpg" alt="关键词卡与口播人物" width="100%"></a><br>
<strong>关键词卡 + 口播人物</strong><br>
用大字强化核心观点，同时保留人物表达。
</td>
</tr>
<tr>
<td width="50%" valign="top">
<a href="https://app.chatcut.io/?source=prompt-library&target=motion-graphics&template=1a4cd0c3-ba36-4457-8428-49e57c61292f"><img src="assets/official-gallery/1a4cd0c3-ba36-4457-8428-49e57c61292f.jpg" alt="堆叠柱状图动画" width="100%"></a><br>
<strong>堆叠柱状图动画</strong><br>
把比例变化和构成关系变成可读的动态证据。
</td>
<td width="50%" valign="top">
<a href="https://app.chatcut.io/?source=prompt-library&target=motion-graphics&template=38bd86e5-2f30-46f7-ade8-1a9711220f0d"><img src="assets/official-gallery/38bd86e5-2f30-46f7-8428-49e57c61292f.jpg" alt="折线图动画" width="100%"></a><br>
<strong>折线图动画</strong><br>
用趋势交叉和增长变化解释口播中的数据。
</td>
</tr>
</table>

<div align="center">

### [浏览全部 123 个官方效果参考 →](VISUAL-GALLERY.md)

</div>

## 完整安装方式

### 推荐：Skill Installer

```text
$skill-installer install https://github.com/Fangx-AI/cut-director
```

安装完成后重启 Codex。

### 开发模式：Windows Junction

Junction 会让仓库中的修改立即反映到本地 Skill，适合开发和调试。

```powershell
git clone https://github.com/Fangx-AI/cut-director.git
New-Item -ItemType Directory -Force -Path "$HOME\.codex\skills"
New-Item -ItemType Junction `
  -Path "$HOME\.codex\skills\cut-director" `
  -Target "$(Resolve-Path .\cut-director)"
```

安装后可以这样调用：

```text
使用 $cut-director 分析这条口播，找出最值得加画面的 3 个时刻。
```

<details>
<summary><strong>从旧调用名迁移</strong></summary>

Skill 调用名已从 `$chatcut-talking-head-visual-director` 简化为 `$cut-director`。如果你使用旧的 Windows Junction 安装，请移除旧 Junction 后，按照上面的新路径重新创建。

</details>

## 技术与验证

[Skill 定义](SKILL.md) · [完整视觉画廊](VISUAL-GALLERY.md) · [官方 Prompt 目录](references/chatcut-official-catalog.md) · [导演框架](references/visual-director-framework.md) · [质量门禁](references/quality-gate.md) · [测试证据](tests/forward-results.md)
