# 视觉风格圣经

## 1. 核心风格

温暖、克制、有电影构图感的手绘寓言绘本。画面应像一本会轻微运动的成人寓言书，而不是儿童卡通、写实电影截图或游戏概念设定图。

固定英文风格锚点：

```text
warm hand-painted allegorical storybook illustration, restrained cinematic composition,
soft natural light, subtle painterly texture, emotionally readable characters,
coherent environment design, mature fable tone, vertical 9:16 composition
```

## 2. 画面规范

- 比例：9:16。
- 主体：位于中部安全区，避免贴近顶部和底部。
- 景别：远景建立空间，中景推进故事，近景只用于关键决定和揭晓前情绪。
- 背景：有足够环境信息，但不堆满装饰。
- 光线：自然光为主；故事升级时可逐渐降低明度或饱和度。
- 文字：图片内部禁止生成任何可读文字，由剪映统一添加。

## 3. 色彩

基础色：土黄、灰绿、雾蓝、木棕、暖灰。

- 平静：暖晨光、低对比。
- 异常出现：局部冷色或阴影加深。
- 冲突升级：降低整体饱和度，保留关键物体色彩。
- 揭晓与解释：恢复清晰中性色，不使用夸张金光。

## 4. 一致性优先级

1. 角色身份可识别。
2. 服装和标志物一致。
3. 场景地理和时间连续。
4. 画风和色调一致。
5. 单张画面的精致程度。

当精美程度与一致性冲突时，优先一致性。

## 5. 负面约束

```text
no photorealism, no 3D render, no anime, no chibi proportions,
no modern objects, no readable text, no watermark, no extra fingers,
no duplicated character, no costume redesign, no excessive fantasy ornaments,
no glossy commercial poster look
```

## 6. gpt-image-2 镜头 Prompt 结构

每个镜头按以下顺序组织：

1. 固定风格锚点。
2. 角色锚点和不可变特征。
3. 场景、时间、动作和情绪。
4. 构图、景别、镜头方向和字幕安全区。
5. 与上一镜头的连续性。
6. 负面约束。

不要只写抽象情绪，例如“很紧张”；应描述可见动作，例如“阿远双手紧握木桶边缘，回头看向排队的人群”。
