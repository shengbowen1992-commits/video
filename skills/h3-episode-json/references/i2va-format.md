# 官方 I2VA 格式速查

来源：[官方 skill](https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills/h3-prompt-writing) 和 [base-en.txt](https://github.com/MiniMax-AI/MiniMax-H3/blob/main/skills/h3-prompt-writing/references/base-en.txt)。2026-10-04 核对；该指南最近修改提交为 `35491cdba2adfe62a510f725e8619f8e58783ea2`。I2V 在官方视听任务中称为 I2VA。

`prompt` 是下列文本序列化后的字符串，不是嵌套 JSON 对象：

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] ...

overall_soundscape: ...

non_diegetic_music: ...
```

首行逐字保留，空一行再写三个字段；名称和顺序固定。正文用英文，开场依据图片写风格、构图、人物和物件，再展开动作与结果。声音随可见动作描述；运镜以自然句说明方式及有意义的幅度、速度。

`[Shot 1]` 不加起始时间戳；段内后续切镜用 `[Shot 2] At 00:03.500, ...`，编号与时间递增且小于本段秒数。外层各段独立计时。

发声人物用稳定 `(S1)` 等编号。对白为 `<d>[Chinese] 用户原文</d>`，人物、声线及语气写在标签外；画面文字用英文双引号保留原文。旁白、跨切镜对白或末尾截断需要时，读取官方原文 §4.4 的标签约定再写。

`overall_soundscape`：1–4 句概括环境与动作声音，不重复对白；仅全程静音用 `N/A`。`non_diegetic_music`：1–3 句说明乐器、节奏、速度和音量变化；无配乐用 `N/A`。不要额外套用 Ref2VA 六字段结构。

本地接续约定及更严格的秒数范围见 [JSON 约定](json-contract.md)。校验器只查结构；对白忠实度、动作可实现性、预期尾帧与实际画面差异须另行检查。
