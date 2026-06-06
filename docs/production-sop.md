# 单期生产 SOP

## 阶段 0：选题建档

```bash
python tools/new_episode.py --id EP002 --slug sunk-cost --concept 沉没成本
```

补全 `episode-brief.json`，通过 G1。

## 阶段 1：概念机制卡

使用 `prompts/01-concept-analysis.md` 生成 `concept-sheet.json`。先保证因果机制、边界和反例准确，不写故事。

## 阶段 2：三个寓言方向

使用 `prompts/02-story-directions.md` 生成 `story-options.json`。人工按机制准确、故事独立、钩子、延迟揭晓、可视化和现实迁移评分，选择结果写入 `decision.json`，通过 G2。

## 阶段 3：成片脚本

使用 `prompts/03-script.md` 生成 `script.json`。默认 80–110 秒，概念在约 70% 以后首次出现。

## 阶段 4：故事板

使用 `prompts/04-storyboard.md` 生成 `storyboard.json`。

故事板面向 Seedance 时必须遵守：

- 一镜只表达一个主要动作。
- 一镜只使用一种主要运镜。
- 复杂动作拆镜，不让模型一次完成多次转折。
- 人物不承担知识口播。
- 时间线较长的镜头允许由较短生成片段加停帧、变速或 B 版补足。

## 阶段 5：gpt-image-2 视觉锚点

使用 `prompts/05-image-package.md` 生成 `asset-manifest.json`。

出图顺序：

1. 常驻角色设定图。
2. 本期场景空镜锚点。
3. 角色与场景主锚点。
4. 每个关键镜头的参考帧。

G3 只检查身份、服装、场景空间和构图，不要求图片表现完整运动过程。

## 阶段 6：Seedance 镜头任务

使用 `prompts/06-seedance-video-package.md` 生成 `video-manifest.json`。

MVP 执行方式：

1. 按 `clip_id` 顺序生成。
2. 优先选择 `image_to_video`。
3. 每个关键镜头先生成两个候选。
4. 文件按 `filename` 保存到 `video-clips/`。
5. 逐条完成 G4。
6. 同一片段连续失败两次，降低动作复杂度；仍失败则执行 `fallback`，改用静帧微动。

Seedance 默认不生成角色知识口播。环境声可保留，但必须能在剪映中独立关闭。

## 阶段 7：发布包与剪映辅助文件

使用 `prompts/07-publish-package.md` 生成 `publish-pack.json`，然后执行：

```bash
python tools/make_srt.py episodes/<episode-dir>
python tools/make_edit_list.py episodes/<episode-dir>
```

`edit-list.csv` 将同时列出视频片段、生成模式、参考图、原生音频策略和剪映处理说明。

## 阶段 8：剪映总装

顺序建议：

1. 先铺独立旁白。
2. 按旁白节奏放入通过 G4 的 Seedance 片段。
3. 用停帧、变速、裁切和静帧补足时间线。
4. 导入并人工修正字幕。
5. 处理 Seedance 原生环境声。
6. 加入 BGM、揭晓字卡、栏目包装和 AI 标识。
7. 完整观看两遍并通过 G5。

## 阶段 9：发布与回流

在 `analytics/episode-metrics.csv` 记录平台指标和生产指标：

- Seedance 计划片段数。
- 首次通过片段数。
- 重生成片段数。
- 静帧降级片段数。
- 生成成本与时间。
- 3 秒留存、完播、转发、收藏和评论猜中率。
