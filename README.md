# FableFlow

> 用 AI 把陌生概念变成“先听懂故事，最后才知道答案”的寓言知识短视频。

FableFlow 是一套面向视频号的半自动化内容生产基线。它将 **GPT-5.5 的概念拆解与故事创作**、**gpt-image-2 的统一角色和分镜画面生成**，以及 **剪映的成片制作**连接为一条可复用、可审核、可度量的生产流水线。

## 核心原则

1. **先理解，后命名**：故事前段不出现概念名称，接近结尾才揭晓。
2. **机制先于文采**：先准确拆解概念，再设计隐喻，避免“故事好听但知识讲错”。
3. **结构化交接**：每个阶段输出 JSON 资产，下一阶段只消费明确输入。
4. **人工把关关键节点**：选题、故事方向、关键画面和最终成片必须人工审核。
5. **统一世界观与角色资产**：画面风格和角色身份持续复用，形成栏目品牌。
6. **数据回流**：完播、转发、收藏和评论猜中率进入下一轮选题与脚本优化。

## 生产链路

```mermaid
flowchart LR
    A[概念库/人工选题] --> B[概念机制卡]
    B --> C[3个寓言方向]
    C -->|人工选择| D[成片脚本]
    D --> E[故事板]
    E --> F[画面资产清单]
    F --> G[gpt-image-2生成关键画面]
    G -->|人工一致性审核| H[字幕/旁白/发布包]
    H --> I[剪映模板装配]
    I -->|人工终审| J[发布]
    J --> K[数据回流]
    K --> A
```

## 仓库结构

```text
bibles/                 世界观、角色和视觉风格圣经
config/pipeline.json    阶段、输入输出与人工门禁定义
docs/                   架构、生产 SOP、剪映和质量规范
prompts/                GPT-5.5 各阶段执行提示词
schemas/                JSON 数据契约
templates/episode/      新分集模板
episodes/               每期的完整生产资产
analytics/              运营指标记录模板
tools/                  校验、创建分集、生成 SRT 和剪辑清单
```

## 快速开始

### 1. 安装校验依赖

```bash
python -m pip install -r requirements.txt
```

### 2. 校验仓库中的结构化资产

```bash
python tools/validate.py
```

### 3. 创建新分集

```bash
python tools/new_episode.py \
  --id EP002 \
  --slug sunk-cost \
  --concept 沉没成本
```

### 4. 按 Prompt 链生产

依次执行：

```text
prompts/01-concept-analysis.md
prompts/02-story-directions.md
prompts/03-script.md
prompts/04-storyboard.md
prompts/05-image-package.md
prompts/06-publish-package.md
```

每一步的输入和输出由 `config/pipeline.json` 与 `schemas/` 定义。

### 5. 生成剪映可用的辅助文件

```bash
python tools/make_srt.py episodes/EP001-the-common-well
python tools/make_edit_list.py episodes/EP001-the-common-well
```

输出：

- `subtitles.srt`：可导入剪映的字幕文件
- `edit-list.csv`：逐镜头素材、时长、运镜、旁白和音效建议

## 人工审核点

| Gate | 审核内容 | 未通过处理 |
|---|---|---|
| G1 选题 | 值得讲、能寓言化、具有现实映射 | 返回概念库重选 |
| G2 故事方向 | 隐喻准确、故事成立、不过早泄题 | 重选或重写方向 |
| G3 视觉资产 | 角色不漂、服装统一、画面可剪 | 只重生成失败镜头 |
| G4 成片 | 节奏、字幕、概念准确、平台合规 | 剪映局部返工 |

## 示例分集

`episodes/EP001-the-common-well/` 提供“公地悲剧”的完整样例，包括概念机制卡、三个故事方向、人工选择、脚本、故事板、画面资产清单与发布包。

## 当前边界

首版聚焦**稳定生产资产和人工可控交接**，不直接调用模型 API，也不自动操作剪映。模型调用和剪映装配保留人工触发，以便先验证栏目质量与数据表现，再逐步自动化。
