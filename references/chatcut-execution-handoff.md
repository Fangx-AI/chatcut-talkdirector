# ChatCut 执行 Handoff

## 进入条件

只有用户明确确认 Visual Beat Map 或某个代表性 Beat 后才进入执行。确认必须覆盖视觉语言、人物处理和会触发额度的生成动作。

## 执行 Skill 路由

按需要使用已安装的 ChatCut skills：

| 任务 | Skill |
| --- | --- |
| 读取/处理口播剪辑原则 | `chatcut:talking-head-guide` |
| 获取 transcript、字幕和词点 | `chatcut:transcription` |
| 创建或放置 MG | `chatcut:create-motion-graphics` |
| 生成视频补画面 | `chatcut:video-gen` |
| 生成或编辑静态画面 | `chatcut:image-gen` |
| 导入用户或外部素材 | `chatcut:asset-import` |
| 背景音乐和节奏 | `chatcut:music` |
| 音效或旁白 | `chatcut:voice` |
| 检查时间线和画面 | `chatcut:verification` |
| 导出成片 | `chatcut:export` |

如果某个 Skill 不可用，报告缺失能力，不编造工具调用或执行结果。

## 代表性 Beat 执行顺序

1. 重新确认 Beat 的文案锚点、时间、画幅、人物处理和保护区。
2. 以已完成的 A-roll 时间为锚，不先移动口播主体。
3. 检查 Beat 开始、中间和结束附近的真实画面。
4. 根据 Beat 类型创建一项 MG、生成画面或导入素材。
5. 只放置到批准的时间范围，保留可编辑属性。
6. 检查字幕、脸、手势、产品、Logo、文字和运动路径。
7. 在开始、中间和结束帧验证入场、可读性、停留和退场。
8. 向用户展示代表性结果并等待确认。
9. 只有确认后才按同一视觉系统扩展其余 Beat。

## Handoff 包

执行者接收：

```markdown
- Beat ID 和文案锚点
- 精确或约时间范围
- 主视觉语言
- 官方结构参考
- 画面设计
- 人物处理与位置尺寸
- ChatCut 用户提示词
- 导演约束层
- 生成 prompt（如有）
- 保护区
- 可编辑字段
- 廉价风险
- Quality Gate 评分和结论
```

缺少人物处理、保护区或质量结论时，不执行该 Beat。

## 额度和确认

MG、视频和图片生成可能触发 ChatCut 确认卡或消耗额度。不要绕过确认；确认被拒绝、取消或超时时，停止并等待用户新指令。属性面板中的文字、颜色、字体、位置和时长调整优先用于低成本迭代。

## 失败降级

1. 先删除一个竞争动作或装饰。
2. 生成视频失败时尝试更明确的单镜头约束。
3. 第二次仍失败时改用生成图片、MG、真实 B-roll 或保持干净。
4. PiP 无安全区时改为分屏、全屏或原画面。
5. 任何降级都更新 Visual Beat Map，不默默改变导演意图。

## 扩展整条视频

复用已确认的字体、色板、形状和运动语法，不复制每个 Beat 的具体模板。每完成一组 Beat 后运行 ChatCut verification，检查整体密度和连续性；连续重视觉后恢复人物和留白。
