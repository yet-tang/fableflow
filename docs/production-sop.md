# 单期生产 SOP

## 阶段 0：选题建档

人工从概念库选择概念，创建分集：

```bash
python tools/new_episode.py --id EP002 --slug sunk-cost --concept 沉没成本
```

补全 `episode-brief.json`，重点回答：

- 观众听过这个词吗？
- 不知道术语时，能否通过故事直觉理解？
- 有没有现实生活中的对应场景？
- 是否可能因为隐喻简化而产生误导？

通过 G1 后进入下一阶段。

## 阶段 1：概念机制卡

将 `episode-brief.json` 输入 `prompts/01-concept-analysis.md`。

审核重点：

- 核心因果链是否成立。
- 必要条件和边界是否写清。
- 是否区分“机制”与“结果”。
- 是否包含反例或失效场景。

## 阶段 2：三个故事方向

将 Brief、Concept Sheet 和三份 Bible 输入 `prompts/02-story-directions.md`。

每个方向只做故事提案，不写完整成片稿。人工选择时按以下优先级：

1. 概念映射准确。
2. 前 3 秒存在异常或冲突。
3. 角色目标明确。
4. 转折来自机制，而非强行制造。
5. 接近结尾才可能猜出概念。
6. 画面数量与制作成本可控。

将选择写入 `decision.json`，通过 G2。

## 阶段 3：成片脚本

运行 `prompts/03-script.md`，目标时长默认为 80–110 秒。

推荐节奏：

| 时间 | 功能 |
|---|---|
| 0–5 秒 | 反常识钩子 |
| 5–35 秒 | 规则与角色目标 |
| 35–60 秒 | 个体选择导致局势升级 |
| 60–70 秒 | 猜测停顿 |
| 70–85 秒 | 揭晓概念与一句定义 |
| 85–110 秒 | 隐喻映射、现实案例、记忆句 |

朗读一遍检查：句子是否口语化、是否有连续长句、是否能在目标时间内读完。

## 阶段 4：故事板

运行 `prompts/04-storyboard.md`。

建议每期 10–15 个镜头，每镜 3–8 秒。故事板必须包含：

- 画面具体发生什么。
- 出现哪些固定角色。
- 旁白和短字幕。
- 运镜方式。
- 情绪功能。
- 预留字幕安全区。

## 阶段 5：画面资产

运行 `prompts/05-image-package.md` 生成 `asset-manifest.json`。

资产分三类：

- `generate`：必须用 gpt-image-2 新生成。
- `reuse`：使用已有角色锚点或环境资产，通过裁切和微动完成。
- `title_card`：不需要叙事图，用剪映字卡完成。

出图顺序：

1. 本期新增环境锚点。
2. 第一张角色同框主锚点。
3. 关键转折镜头。
4. 其余衔接镜头。

G3 检查不通过时只重做失败资产，不修改已通过的脚本和镜头编号。

## 阶段 6：发布包与辅助文件

运行 `prompts/06-publish-package.md` 生成 `publish-pack.json`。

然后执行：

```bash
python tools/make_srt.py episodes/<episode-dir>
python tools/make_edit_list.py episodes/<episode-dir>
```

## 阶段 7：剪映装配

按照 `docs/jianying-workflow.md` 和 `edit-list.csv` 完成剪辑。G4 必须完整观看两遍：

- 第一遍关闭声音，只看画面和字幕。
- 第二遍不看画面，只听旁白和音效。

## 阶段 8：发布与回流

发布后在 `analytics/episode-metrics.csv` 增加一行。至少在 24 小时和 7 天两个时间点记录数据，避免只依据早期波动判断。
