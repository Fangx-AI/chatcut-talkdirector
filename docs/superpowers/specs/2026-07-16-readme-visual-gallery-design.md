# TalkDirector README 与 Visual Gallery 设计

## 目标

把仓库首页从内部规则说明改造成效果优先的产品展示页。用户进入 GitHub 后，应在第一屏理解 TalkDirector 的用途，立即看到真实效果，并能复制一个 Prompt 开始使用。

完整官方 Prompt 能力放入独立 Visual Gallery。README 只展示精选效果，不承载路由算法、验证规则、同步实现和测试细节。

## 受众与价值顺序

主要受众是已经拍好口播、希望快速增加高质量视觉效果的创作者。他们的阅读顺序是：

1. 能做出什么效果
2. 是否有真实案例
3. Prompt 是否简单
4. 是否覆盖自己的场景
5. 如何安装和使用

内部规则、工程结构和测试证据不进入主要阅读路径。

## README 信息架构

### 1. Hero

- 使用现有高质量 Hero 图。
- 保留项目名 `ChatCut TalkDirector`。
- 使用一句具体价值表达：为已经拍好的口播自动匹配高质量动态图形、官方模板和生成画面。
- 提供三个入口：`立即使用`、`查看全部效果`、`安装 Skill`。

### 2. See It Work

- 第一项展示 Prompt 001 的真实成片动态预览。
- 同时展示效果名称、解决的问题和一条可复制 Prompt。
- 不展示动画参数、Logo 裁切规则或关键帧验证过程。

### 3. Verified Prompt Series

- 按 `Prompt 001`、`Prompt 002` 的序号展示经过实片验证的效果。
- 每项必须包含真实预览、效果名称、一句话价值、可复制 Prompt 和完整案例入口。
- 尚未实测的官方模板不能标记为 Verified Prompt。

### 4. What It Can Add

使用少量视觉示例展示核心能力：

- 关键词和图标
- 数据和图表
- 清单和步骤
- 章节和人物介绍
- 产品界面与 supporting visuals

每类只保留一句用户价值，不解释内部路由。

### 5. Official Prompt Highlights

- 精选 6-9 个最适合口播的 ChatCut 官方效果。
- 每项显示真实封面或动态预览、官方名称和观看任务。
- 点击后进入官方实时预览或 Visual Gallery 对应位置。
- 明确区分“官方参考”与“TalkDirector 已实测 Prompt”。

### 6. Three-Step Usage

只保留三个步骤：

1. 提供口播视频或打开 ChatCut 项目
2. 描述想要的效果或使用示例 Prompt
3. 查看代表性结果并确认扩展

### 7. Install

- 保留最短安装命令。
- 提供一条最小调用示例。
- 详细行为边界链接到 `SKILL.md`，不在 README 展开。

## 从 README 移出的内容

以下内容保留在 Skill 或 references，不在首页展开：

- Quality Gate 详细规则
- 两次确认的完整边界
- 官方模板匹配等级和路由算法
- 同步脚本实现
- 仓库文件数量和结构说明
- 行为测试过程
- 当前执行边界的长说明

README 可以在底部提供一个 `Technical details` 链接，但不重复正文。

## Visual Gallery

### 页面职责

建立独立的 `VISUAL-GALLERY.md`，展示 ChatCut 官方 Prompt Library 的全部可视化索引。用户按类别浏览，不需要阅读内部 catalog 表格。

分类至少包括：

- App Promo
- Video Generation / Seedance 2
- Talking Head
- Data & Charts
- Lists & Steps
- Chapters & Titles
- Quotes & Lower Thirds
- Other Motion Graphics

### Gallery 卡片

每个卡片只展示：

- 真实预览图
- 官方名称
- 一句话用途
- `查看动态预览` 或 `在 ChatCut 打开`

模板/预设 ID、同步日期和路由字段保留在机器目录，不显示在用户卡片正文。

## 预览获取

### 19 个视频类 Prompt

- 从官方页面保存远程 MP4 地址和 poster 地址。
- Gallery 使用轻量 poster 直接展示，点击后打开官方 MP4 或官方入口。
- 不把全部 MP4 提交进 Git 仓库。
- README 精选项需要内联动效时，只为少量精选案例制作压缩预览。

### 104 个 Motion Graphics Prompt

- 官方页面使用模板代码实时渲染，没有现成 MP4。
- 保存模板 ID 和官方实时预览入口。
- 为 Gallery 生成一个稳定代表帧缩略图，链接到官方实时预览。
- TalkDirector 实际匹配候选时，按需加载官方模板并检查开始、中间和结束画面；静态缩略图不能替代执行前验证。

### Verified Prompt

- 使用我们实际执行并经用户确认的成片预览。
- Prompt 001 使用本次手势触发双 Logo 的真实结果。
- 后续每天新增一个实测 Prompt 时，追加一项，不重做整个 Gallery。

## 数据与文件边界

- `references/chatcut-official-catalog.md`：机器可检索的完整官方目录。
- `references/chatcut-prompt-routing.md`：内部匹配规则。
- `VISUAL-GALLERY.md`：用户可浏览的可视目录。
- `assets/official-gallery/`：Gallery 的轻量缩略图。
- `assets/verified-prompts/`：已实测 Prompt 的真实预览。
- `scripts/sync_chatcut_prompt_library.py`：同步名称、用途、ID、入口和视频预览元数据。

README 不重复完整目录。

## 更新与失败处理

- 官方条目数量、名称、ID 或入口变化时，同步脚本更新机器目录。
- 视频地址不可访问时，保留官方入口并标记预览待刷新，不显示伪造封面。
- MG 代表帧生成失败时，使用统一的“查看官方实时预览”占位，不使用 AI 生成近似图。
- 任何预览必须能追溯到官方条目或已验证的真实项目。

## 验收标准

### README

- 第一屏包含产品名、价值、真实效果和明确入口。
- 用户在不阅读内部规则的情况下能复制 Prompt 001。
- 主要正文不展示同步实现、测试过程或仓库统计。
- 精选官方效果均有可见预览和有效入口。

### Visual Gallery

- 收录当前 123 个官方条目。
- 每项至少拥有一个真实缩略图或官方实时预览入口。
- 19 个视频类条目记录官方 MP4 预览。
- 104 个 MG 条目记录模板 ID 和实时预览入口。
- 不存在 AI 仿造的官方模板预览。

### 工程验证

- Skill 格式校验通过。
- 官方目录同步可重复运行且输出稳定。
- README、Gallery 和 catalog 的本地链接有效。
- 远程预览链接经过状态检查。
- GitHub 桌面和移动宽度下图片、表格和文字可读。
