# TalkDirector v0.2 管线契约

用户始终只需要用自然语言描述效果。以下中间产物、命令和状态只供导演代理、确定性脚本与执行 Skill 协作，不要求用户填写 JSON 或运行命令。

## 六段产物流

1. `source`：项目或素材身份、画幅、时长和真实保护区。
2. `transcript`：逐字原文与时间；缺失时保存当前状态，只请求一个来源输入。
3. `visual_beats`：模型负责语义锚点、视觉目的、媒介、recipe 匹配与导演判断。
4. `edit_plan`：代码负责状态、代表性 Beat、确认、门禁、阻断原因与写入意图。
5. `assets`：每个素材的来源、验证状态和唯一职责。
6. `verification`：写入后素材、开始、中段、结束的真实证据。

机器字段见 `schemas/talkdirector-pipeline.schema.json`，规则实现见 `scripts/validate_talkdirector.py`。

## 项目缓存与恢复

每个来源使用 `.talkdirector/<safe-project-or-source-id>/manifest.json`。目录已加入 `.gitignore`，只保存本地运行状态，不进入 recipe 或公开 Prompt。

代理内部按以下顺序使用 `scripts/talkdirector_manifest.py`：

1. `init`：从 recipe 和来源身份创建最小 `planned` 骨架。重复调用产生同一路径和相同内容。
2. `build`：合并新读取的项目事实，按 ID 合并 transcript、Beat、素材和证据；只补齐空值或推进可验证状态，不覆盖已确认的文案、导演判断、时间或参数。
3. `transition --to executing`：任何 ChatCut 写操作前运行；只有全部门禁通过才能记录本次写入意图。
4. 写操作后再次 `build`，加入实际素材与开、中、尾证据。
5. `transition --to verified`：证据覆盖 recipe 要求后才能完成。

崩溃或中断后从同一 manifest 继续，不重新询问已经确认的数据。来源或 recipe 不同必须使用新的来源 ID，避免混用状态。

## 状态机

| 状态 | 含义 | 允许的下一步 |
| --- | --- | --- |
| `planned` | 仅有最小骨架，尚未计算具体阻断 | 读取事实并 build |
| `blocked` | 可恢复，但时间、素材、安全区、文案、手势或确认仍不足 | 补齐一个阻断事实后 build |
| `ready` | recipe 的全部门禁有证据，且代表性 Beat 可执行 | 写前 transition |
| `executing` | 已通过写前验证并记录 operation ID | 执行一次批准范围内的写入，收集证据 |
| `verified` | recipe 要求的写后证据全部通过 | 展示结果并等待扩展确认 |

不允许 `blocked -> executing`、`ready -> verified` 或 `executing -> verified`（证据不足）。降级时先更新 Beat/recipe 事实并重新计算门禁，不默默改变导演意图。

## recipe 门禁

- Prompt 001：精确时间、可靠手势、官方素材、安全区、第一次确认。
- Prompt 002：精确时间、逐字文案、安全区、第一次确认；右栏不得超过 45%，滚动保持舒适匀速，不要求全文滚完。

所有通过门禁都必须带证据。`blocked` 会保存确定性的阻断代码、用户可理解的原因和解除方式。

## 模型与代码的边界

- 模型负责：理解自然语言、选择视觉语言、判断是否值得做、匹配 recipe、设计降级路线。
- 代码负责：必填字段、ID 引用、时间范围、保护区矩形、状态迁移、资产验证、执行门禁和证据完整性。
- 脚本通过不等于审美通过；模型判断也不能绕过确定性门禁。

## Prompt 003 入口

在选题和素材明确后，代理可用 `new-recipe` 在忽略目录中生成空白 draft。它不会自动进入 `recipes/`，也不会编造 Prompt 003 的名称、文案、触发条件或素材策略；完成真实验证后再按 recipe 契约发布。
