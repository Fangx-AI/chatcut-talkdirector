# ChatCut 官方提示词结构参考

最后核对：2026-07-15

## 官方来源

- Prompt Library: https://chatcut.io/prompt-library
- Motion Graphics Guide: https://chatcut.io/docs/examples-motion-graphics
- Motion Graphics planning guide: https://chatcut.io/blog/motion-graphics
- Seedance 2.0 Prompt Guide: https://chatcut.io/blog/seedance-2-prompt-guide
- Production Seedance examples: https://chatcut.io/blog/seedance-2-0-prompts-examples

正常使用读取本文件，不要求每次联网。用户要求最新模板、模板名称无法确认或官方页面明显更新时，重新检查官方来源并报告核对日期。只提炼模板名称、任务、布局、动画逻辑和可编辑字段，不复制整段模板实现代码。

## 按信息任务匹配结构

| 任务 | 官方结构参考 | 借鉴点 |
| --- | --- | --- |
| 人物身份 | AI Speaker Intro Card、Paper/Editorial Lower Third | 精确姓名和身份、清晰层级、短入场 |
| 关键词或强观点 | AI Talking-Head Keyword Card、Keyword typing、Type emphasis | 人物和关键词分区、一次一个焦点、一个强调色 |
| 步骤和清单 | AI Numbered Talking-Head Overlay、AI Bullet Points Overlay、Hand-Drawn List Overlay | 人物与列表共存、逐项跟随原声出现 |
| 引语和结论 | AI Story Quote Card、Quote card 系列 | 全屏短节拍、逐行进入、最后一行落点 |
| 章节切换 | AI Chapter Label、AI Dial Chapter Card、Chapter title 系列 | 快速建立章节、单一动作、明确退场 |
| 数据和对比 | Bar、Line、Pie、Donut、Benchmark Chart 系列 | 图表类型和数据明确、按叙述顺序揭示 |
| 流程和时间 | Vertical Timeline、Checklist、Progress 系列 | 节点依次出现、状态变化清楚 |

模板名称用于识别成熟结构，不要求调用同名模板。若原片人物位置、字幕、画幅或品牌风格冲突，镜像、重排、定制或放弃。

## MG 提示词语法

```text
[图形类型] + [准确内容] + [布局/位置] + [入场、强调、退场] + [字体/颜色/材质] + [时长/透明背景] + [可编辑字段] + [保护区和禁止项]
```

先写类型，再写内容，再写风格。标题、姓名、数字、步骤和图表数据必须准确。说明文字、颜色、字体、数值、时长、位置、图片或视频窗口中哪些需要可编辑。

示例：

```markdown
创建一个 5 秒的口播编号列表 overlay。人物保留在右侧透明视频窗口，左侧依次显示“记录重复任务 / 删除无效信息 / 汇入一个系统”。使用黑白编辑风和一个亮绿色强调色，项目在对应口播词点逐项进入并干净退场。文字、颜色、字体、时长和视频窗口位置可编辑。底部 22% 保持透明给字幕，不使用玻璃卡、粒子或持续辉光。
```

## 生成画面提示词语法

ChatCut 官方 Seedance 资料强调：给每个素材明确职责，使用具体名词，默认一个镜头和一个主要镜头运动。

```text
[素材及职责] + [单个画面任务] + [主体动作] + [时间/节奏] + [一个主要镜头运动] + [灯光/材质/空间/声音名词] + [保持项] + [禁止项] + [时长和画幅]
```

需要多个镜位或场景时拆成多个生成任务，由剪辑组织。主体运动复杂时减少镜头运动；主体静止时才把运动交给镜头。参考图、参考视频和音频不能无职责地堆在 prompt 开头。

## 双层输出

官方 Seedance 预设的短用户提示词背后还有镜头、灯光、素材路由和约束层。Visual Beat Map 因此分成：

```markdown
- ChatCut 用户提示词：创建一个口播编号要点 overlay，人物保留在右侧，左侧依次显示 3 个步骤，9:16。
- 导演约束层：根据实际空白区确认人物侧；每次一个焦点；入场跟随原声词点；底部字幕区净空；无玻璃卡、粒子和持续发光；结束后干净回到人物。
```

用户提示词负责“要什么”，导演约束层负责“怎样才不会做差”。不要把短提示词误当成完整导演信息。
