# Prompt 使用说明

这些 Prompt 按 `config/pipeline.json` 顺序执行。每次调用都应附带指定输入文件的完整内容，并要求模型只输出可解析 JSON，不要使用 Markdown 代码围栏。

## 执行顺序

1. `01-concept-analysis.md`
2. `02-story-directions.md`
3. `03-script.md`
4. `04-storyboard.md`
5. `05-image-package.md`：生成 gpt-image-2 锚点和参考帧计划
6. `06-seedance-video-package.md`：生成 Seedance 视频任务
7. `07-publish-package.md`

## 通用执行参数

- 创作模型：GPT-5.5
- 图片模型：gpt-image-2
- 视频模型：Seedance 2.0
- 默认语言：简体中文
- 默认目标时长：80–110 秒
- 概念分析创造性偏低，故事方向偏高，正式脚本和生产包回到中等

## 版本管理

当 Prompt 发生实质变化时：

1. 在文件顶部更新 `prompt_version`。
2. 在新分集 `episode-brief.json` 记录使用版本。
3. 已发布分集不追溯重写，除非存在知识错误。

## 强制原则

- 不能跳过 Concept Sheet 直接凭印象写故事。
- 故事前 70% 不得直接出现概念名称、同义术语或教科书定义。
- 先用 gpt-image-2 固定身份，再让 Seedance 生成动作。
- Seedance 默认不生成角色知识口播，只生成视觉和可选环境声。
- 一条视频任务只承担一个主要动作和一种主要运镜。
- 所有 AI 输出均需经过对应人工 Gate。
