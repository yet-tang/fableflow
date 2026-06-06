# FableFlow

> 用 AI 把陌生概念变成“先听懂故事，最后才知道答案”的寓言知识短视频。

FableFlow 是一套面向视频号的半自动化内容生产基线。它将 **GPT-5.5 的概念拆解、故事和故事板**、**gpt-image-2 的统一角色与场景锚点**、**Seedance 的镜头生成**，以及 **剪映的最终装配**连接为一条可复用、可审核、可度量的生产流水线。

## 当前技术链路

```text
GPT-5.5
  概念机制卡 → 三个寓言方向 → 成片脚本 → 故事板 → Seedance 镜头包

gpt-image-2
  角色设定图 → 场景锚点 → 每个镜头的参考帧

Seedance 2.0
  参考图 / 文本 / 音频 / 视频 → 4–8 秒左右的可剪辑镜头片段

剪映
  旁白 → 字幕 → 镜头总装 → 环境声/BGM → 揭晓字卡 → 导出
```

Seedance 负责动作、运镜、光影和环境声；**不直接承担知识旁白**。旁白仍由独立音轨和剪映统一控制，保证术语、断句和栏目声音稳定。

## 核心原则

1. **先理解，后命名**：故事前段不出现概念名称，接近结尾才揭晓。
2. **机制先于文采**：先准确拆解概念，再设计隐喻。
3. **身份先于运动**：先用 gpt-image-2 固定角色和场景，再交给 Seedance 动起来。
4. **一镜一动作**：Seedance 镜头尽量只承担一个清晰动作和一种主要运镜。
5. **旁白与画面解耦**：生成视频不依赖角色说话，避免口型和知识文本失控。
6. **人工把关关键节点**：选题、故事方向、锚点图、视频片段和最终成片必须人工审核。
7. **结构化交接**：每个阶段输出 JSON，下一阶段只消费明确输入。
8. **数据回流**：完播、转发、收藏、猜中率和视频返工率进入下一轮优化。

## 生产链路

```mermaid
flowchart LR
    A[概念库/人工选题] --> B[概念机制卡]
    B --> C[3个寓言方向]
    C -->|人工选择| D[成片脚本]
    D --> E[故事板]
    E --> F[gpt-image-2角色/场景/参考帧]
    F -->|锚点审核| G[Seedance镜头包]
    G --> H[Seedance生成视频片段]
    H -->|视频审核| I[字幕/旁白/发布包]
    I --> J[剪映总装]
    J -->|人工终审| K[发布]
    K --> L[数据回流]
    L --> A
```

## 仓库结构

```text
bibles/                 世界观、角色和视觉风格圣经
config/pipeline.json    阶段、输入输出与人工门禁定义
docs/                   架构、生产 SOP、Seedance、剪映和质量规范
prompts/                GPT-5.5 各阶段执行提示词
schemas/                JSON 数据契约
templates/episode/      新分集模板
episodes/               每期的完整生产资产
analytics/              运营指标记录模板
tools/                  校验、创建分集、生成 SRT 和剪辑清单
```

## 快速开始

```bash
python -m pip install -r requirements.txt
python tools/validate.py
python tools/new_episode.py --id EP002 --slug sunk-cost --concept 沉没成本
```

按顺序执行：

```text
prompts/01-concept-analysis.md
prompts/02-story-directions.md
prompts/03-script.md
prompts/04-storyboard.md
prompts/05-image-package.md
prompts/06-seedance-video-package.md
prompts/07-publish-package.md
```

生成剪映辅助文件：

```bash
python tools/make_srt.py episodes/EP001-the-common-well
python tools/make_edit_list.py episodes/EP001-the-common-well
```

## 人工审核点

| Gate | 审核内容 | 未通过处理 |
|---|---|---|
| G1 选题 | 值得讲、能寓言化、具有现实映射 | 返回概念库重选 |
| G2 故事方向 | 隐喻准确、故事成立、不过早泄题 | 重选或重写方向 |
| G3 锚点资产 | 角色、服装、场景空间关系稳定 | 只重生成失败锚点 |
| G4 Seedance 镜头 | 身份稳定、动作自然、运镜可剪、无异常音画 | 只重生成失败片段 |
| G5 成片 | 节奏、字幕、概念准确、平台合规 | 剪映局部返工 |

## 示例分集

`episodes/EP001-the-common-well/` 提供“公地悲剧”的完整样例，并新增 `video-manifest.json`，用于把 13 镜故事板转换成 Seedance 可执行的视频任务。

## 当前边界

首版仍采用**半自动模式**：模型调用可先通过人工界面完成，仓库负责数据契约、命名、审核和交接。等 10 期内容验证后，再接入 Seedance API 和自动任务队列。
