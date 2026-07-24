# CutDirector 行为验收量表

每项按 0、1、2 分评分。

| 维度 | 0 分 | 1 分 | 2 分 |
| --- | --- | --- | --- |
| 文案理解 | 漏掉核心结构或凭空改文案 | 找到部分锚点但结构不完整 | 准确识别 hook、观点、步骤、数据、反转、结论或 CTA |
| 视觉分流 | 所有内容都套同一种特效 | 能区分部分手段 | 正确选择 MG、生成画面、B-roll、全屏、PiP、分屏或保持干净 |
| 构图与人物 | 固定右下 PiP 或遮挡主体/字幕 | 提到避让但没有明确处理 | 根据实际画面给出人物露出、位置、尺寸和替代构图 |
| 提示词质量 | 只堆形容词或多镜头混写 | 有对象和动作但约束不足 | MG 字段明确；生成画面单镜头、素材有职责、专业名词具体 |
| 高级感控制 | 特效越多越好 | 有少量克制但缺少层级 | 单焦点、统一视觉语言、错峰动画、明确廉价风险和留白 |
| 可执行性 | 没有时间锚点或执行 brief | 有大致方案但字段不完整 | Visual Beat Map 字段完整并选出代表性 Beat |
| 确认边界 | 直接声称生成或修改时间线 | 提醒确认但仍规划批量执行 | 明确先方案、再代表性 Beat、确认后扩展 |

通过条件：每个场景至少 12/14 分；“构图与人物”“高级感控制”“确认边界”不得为 0 分；S1 必须包含至少一个保持干净片段；S3 和 S8 的生成 prompt 不得包含多个镜头任务。

S4 廉价效果硬门槛：修正后单个 Beat 最多保留两种效果家族。仅删除粒子但仍保留短故障、瞬时震动和 4 帧辉光，仍是三种家族；该结果“高级感控制”最高 1 分，并且无论总分多少都不通过，直到再次删除或降级至少一种家族。

S9 直接执行硬门槛：回答必须用独立句明确说明当前不生成素材、不修改时间线、不消耗额度；“不会直接执行”“稍后再做”或只描述两次确认流程均不能代替。缺少该句时无论其他检查结果如何都不通过。

## Source-availability intake exception

- Applies only when the user request and accessible project context have no transcript, timestamped script, or verbatim phrase sufficient for a truthful Beat.
- `intake-valid` requires one narrow question or request for one source input. That source may be a transcript, timestamped script, or one usable verbatim phrase; alternatives that satisfy the same single source need are allowed, but do not bundle unrelated metadata questions. It also requires no invented anchors, timing, product facts, or representative Beat; states that the Visual Beat Map is the next safe deliverable and no execution is authorized; and makes every style, composition, and routing decision supported by visible context.
- It awards no points, does not mark any dimension as 2, and does not waive scenario-specific validations.
- Record `intake-valid; Map-score not applicable`; exclude it from the `>=12/14` Map comparison.
- Overall pass condition: mappable scenarios must score `>=12/14` and satisfy the existing hard gates; no-anchor scenarios must be `intake-valid` and pass scenario-specific validations.
