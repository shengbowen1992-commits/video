# 官方格式与本工作流绑定

2026-10-05 核对 [MiniMax 官方 skill](https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills/h3-prompt-writing) 和 [Ref2VA 指南](https://github.com/MiniMax-AI/MiniMax-H3/blob/35491cdba2adfe62a510f725e8619f8e58783ea2/skills/h3-prompt-writing/references/ref-en.txt)。字段、标签含义和镜头语法来自官方；三图槽位、外层 JSON 和 5–15 秒限制来自当前本地导入器。

## 六字段

| 字段（顺序固定） | 内容 |
| --- | --- |
| `subject_definitions` | 女主 `<Subject 1>` 的身份来源 `<Picture 1>`；男主 `<Subject 2>` 的身份来源 `<Picture 2>`；独立定义 `<Picture 3>` 的开场构图、姿态、服装状态、道具及空间关系 |
| `summary` | 概括本段发生的具体事件和引用关系；两张身份图与一张开场图通常使用 `[reference generation + keyframe completion]` |
| `retention_analysis` | 按定义的引用范围说明保留关系，不承诺整张身份图背景和服装都照搬 |
| `detailed_description` | 风格与全局约束先于 Shot；按播放顺序写画面、动作、镜头、声音和准确对白 |
| `overall_soundscape` | 连续环境底声和整体声场 |
| `non_diegetic_music` | 观众听见而人物听不见的配乐；没有请求时为 `N/A` |

六个标题各出现一次，各字段非空，字段之间空一行。不加 I2VA 首行引用句或 `integrated_multimodal_description`，不加第七个全局规则字段。

## 引用范围与连续状态

女主和男主身份图主要提供脸与发型。以实际图可见信息为依据，不从不可见位置推测鞋、衣服或身体属性。女主、男主出现在第三张图时仍为原来的两个 Subject，不新增重复人物。

第三张图单独定义后，对它写一条保留分析；只作为 Subject 来源的前两张图不必再分别定义成独立主体。使用官方视觉关系值 `fully_preserved`、`partially_preserved`、`attribute_transfer`、`weak_reference`，范围须与定义一致。身份角色只定义脸与发型时，服装变化不意味着换人；如定义包括会被改变的属性，缩小保留范围或使用部分保留。

下一段从实际传入 Picture 3 的当前状态继续。连续动作、已经完成的转身或交接不能重演；物件所有者、哪只手持物、衣服位置、人物接触关系继续承接。换视角时保留场景中的真实位置，不把画面左右变化误写成角色换位。

本工作流没有视频、音频参考输入，不定义 `<Video N>` 或 `<Audio N>`。上一段尾帧是静态图片，不自动成为视频延续输入或音频引用。

## 段内镜头与声音

每段开场 `[Shot 1]` 不带起始时间。段内确有切镜时使用 `[Shot 2] At 00:03.500, ...`；切点连续递增且小于该段 `duration_sec`。JSON 第几段与段内 Shot 编号是两件事。

官方对生成任务正文通常建议 350–500 英文词，这是写作指导，不是导入器的字数校验。动作和对白须先适配秒数，避免为凑字数增加情节。随包模板是精简的结构教学示例。

对白、歌词及画面文字保留原语言与原文。说话者按实际首次发声顺序固定 `(S1)`、`(S2)`，不因 Subject 编号而自动指定。口头内容放在本段 Shot 中，以 `<d>[Chinese] 原对白。</d>` 标注；同一个人后续复用 speaker ID。保留分析不放 speaker ID。

Shot 中写具体声音的来源、触发动作和时机，环境连续底声放 `overall_soundscape`，对白不要在两处重复。不添加未请求的人声或音乐；整段静音时声音字段为 `N/A`，正文不能仍描述可听声音。语音休止不意味着动作必须暂停。

这套文字只提供条件约束，不能证明生成结果已满足身份、首帧或音画接续要求。
