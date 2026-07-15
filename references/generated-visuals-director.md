# 生成画面与 B-roll 导演

## 先选真实素材还是生成

| 需求 | 优先手段 |
| --- | --- |
| 真实产品、人物、地点、事件或证据 | 真实录屏、用户素材或可核验 B-roll |
| 抽象概念、未来状态、隐喻和无法实拍的氛围 | 生成视频或生成图片加镜头运动 |
| 数据、流程、界面关系 | MG 或真实界面标注 |
| 短暂节奏变化但没有信息任务 | 保持人物或使用已有 B-roll，不为填空而生成 |

生成画面不能冒充真实产品功能、新闻证据或用户没有提供的事实。

当抽象隐喻同时提供一张材质/色调参考图和一段镜头运动参考视频时，默认选择生成画面：图片只负责材质或色调，视频只负责镜头方向、速度和稳定感。只有用户明确要求可编辑图解、禁止生成，或 Quality Gate 判定生成风险不可接受时，才降级为 MG；不得在未说明理由时把两份生成参考仅当作 MG 灵感而放弃生成 prompt。

## 单镜头规则

一个 Visual Beat 默认对应一个连续镜头和一个主要镜头运动。不要在一条 prompt 中要求“先广角、再特写、再环绕、最后拉远”。需要多个镜头时拆成多个生成任务，再由剪辑安排。

主体动作复杂时使用静态机位、缓慢推近或轻微跟随。主体基本静止时才使用明显的推、拉、横移、俯拍下降或环绕。

## 素材职责

每个引用素材必须声明一个主要职责：

- 图片：主体一致性、产品轮廓、首帧/尾帧、材质、色彩或构图
- 视频：镜头运动、人物动作、阻挡、节奏或转场逻辑
- 音频：口播语气、音乐节拍、环境声或声音质感

没有职责的素材不要放进 prompt。

## Prompt 结构

```text
[素材及职责] + [单个画面任务] + [主体动作] + [时间/节奏] + [一个主要镜头运动] + [灯光/材质/空间/声音名词] + [保持项] + [禁止项] + [时长和画幅]
```

使用具体名词，例如静态机位、缓慢侧向横移、顶光、轮廓光、纸张纤维、墨水扩散、金属反射、玻璃折射、水流分叉、环境低频。不要只写“高级、电影感、震撼、梦幻”。

## 声音和人物

- 明确原口播声音是否持续。
- 补画面默认不生成新的对白。
- 需要环境声时说明它是否压在口播下方；不需要时要求静音或后期移除。
- 按 `composition-and-speaker-presence.md` 决定全屏、PiP 或分屏。

## 质量门槛

完整审看生成结果。身份漂移、手部错误、文字损坏、产品失真、物理穿帮或需要逐帧修复时，不视为可用成片。优先重新约束或改用 MG、图片、真实 B-roll、全屏短节拍或保持干净。

## 输出格式

```markdown
- 生成目的：解释 / 场景化 / 情绪 / 节奏 / 转场
- 参考素材职责：逐项列出；没有则写“无”
- 单镜头设计：主体、动作、构图和一个主要镜头运动
- 人物处理：全屏 / PiP / 分屏 / 不替换原画面
- 声音处理：保留原声、环境声或静音
- ChatCut 用户提示词：短指令
- 生成画面 prompt：完整专业约束
- 禁止项：事实、身份、文字、产品和风格风险
```

## 示例

```markdown
- 生成目的：把“信息经过筛选并汇入决定”具象化
- 参考素材职责：@image1 只作为纸张纤维和暖灰色调参考；@video1 只作为缓慢左向右横移的镜头运动参考
- 单镜头设计：俯拍纸面，墨水细流从多个入口进入，经过筛网式纸槽分叉并汇入一个清晰黑色圆点；相机持续缓慢横移
- 人物处理：全屏 3 秒，只保留原声；不使用 PiP，避免破坏隐喻构图
- 声音处理：保留原口播；生成环境声静音
- ChatCut 用户提示词：使用两份参考素材生成一个纸张与墨水隐喻的连续镜头，表现信息筛选并汇入决定，9:16。
- 生成画面 prompt：@image1 as paper-fiber texture and warm-gray palette reference. @video1 as slow left-to-right camera movement reference. One continuous top-down shot: thin black ink streams enter from several paper channels, pass through a tactile paper sieve, split briefly, then converge into one precise black decision point. Slow lateral camera move only. Soft overhead light, visible paper fibers, physically coherent ink absorption. Keep the center path readable. No text, no people, no cuts, no extra camera moves, no glass UI, no purple glow. 4 seconds, 9:16, silent; original talking-head audio remains in the edit.
- 禁止项：不生成文字、不出现人物、不做多镜头、不把纸张变成数字界面
```
