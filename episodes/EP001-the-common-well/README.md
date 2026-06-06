# EP001｜多打一桶水

- 概念：公地悲剧
- 状态：Seedance 制作基线，尚未生成正式图片与视频
- 目标时长：100 秒
- 故事方向：公共水井

## 执行顺序

1. 审核 `episode-brief.json` 和 `concept-sheet.json`。
2. 查看三个方向并读取 `decision.json`。
3. 以 `script.json` 和 `storyboard.json` 为叙事依据。
4. 按 `asset-manifest.json` 用 gpt-image-2 生成并审核角色、场景和参考帧。
5. 按 `video-manifest.json` 逐条生成 Seedance 视频片段并通过 G4。
6. 执行 `make_srt.py` 和 `make_edit_list.py`。
7. 在剪映中加入独立旁白、字幕、BGM、环境声和字卡，通过 G5。
