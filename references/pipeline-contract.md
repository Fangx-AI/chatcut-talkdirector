# TalkDirector v0.2 管线契约

用户始终只需要用自然语言描述效果。以下六类中间产物只供导演代理、确定性脚本和执行 Skill 协作，不向用户索要 JSON 或内部字段。

## 产物流

1. `source`：来源、画幅、时长和真实保护区。
2. `transcript`：逐字原文与时间；缺失时停在 `intake`，只请求一个来源输入。
3. `visual_beats`：模型负责语义锚点、视觉目的、媒介、recipe 匹配与导演判断。
4. `edit_plan`：代码约束代表性 Beat、两次确认状态与可执行范围。
5. `assets`：每个素材的来源、验证状态和唯一职责。
6. `verification`：代表性 Beat 的素材、开始、中段、结束证据。

机器契约见 `schemas/talkdirector-pipeline.schema.json`。运行：

```powershell
python scripts/validate_talkdirector.py
python scripts/validate_talkdirector.py --manifest path/to/pipeline.json
```

## 模型与代码的边界

- 模型负责：理解自然语言、选择视觉语言、判断是否值得做、匹配 recipe、设计降级方案。
- 代码负责：必填字段、ID 引用、时间范围、保护区矩形、确认状态、资产验证状态、降级链和验证证据完整性。
- 任何脚本通过都不等于画面审美通过；任何模型判断也不能绕过确定性门禁。

## 状态门禁

- `intake`：来源不足；不得有虚构 Beat。
- `draft`：只交付方案；不得执行。
- `first-approved`：只允许代表性 Beat，且精确时间和必需资产已确认。
- `representative-executed`：代表性 Beat 已执行，素材/开始/中段/结束检查全部通过并有证据。
- `second-approved`：用户看过实际结果后明确批准扩展。
- `expanded`：其余已批准 Beat 可按同一视觉系统执行。

降级不得默默改变导演意图。更新 recipe/Beat、重新验证，再继续执行。
