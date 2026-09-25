# 多段视频产出文件：story_segments.json

这是外层文件交付规范。每一段 `prompt` 内部继续遵循 [原有 Ref2VA 提示词规范](ref2va-prompt-contract.md)，包括六节职责、引用标签、保留关系、全局约束、镜头时间、对白和声音写法。外层 JSON 不新增剧情、人物、动作或风格要求，也不降低原有提示词标准。

## 固定外层结构

保存为 UTF-8 JSON 文件，默认文件名为 `story_segments.json`。下例只演示结构，其中占位文字必须换成按原规范完成的提示词，不能直接当作成品交付：

```json
{
  "global_prompt": "",
  "segments": [
    {
      "id": 1,
      "title": "第一段",
      "raw_prompt": true,
      "prompt": "subject_definitions:\n[按原规范填写]\n\nsummary:\n[按原规范填写]\n\nretention_analysis:\n[按原规范填写]\n\ndetailed_description:\n[按原规范填写]\n\noverall_soundscape:\n[按原规范填写]\n\nnon_diegetic_music:\n[按原规范填写]"
    },
    {
      "id": 2,
      "title": "第二段",
      "raw_prompt": true,
      "prompt": "subject_definitions:\n[按原规范填写]\n\nsummary:\n[按原规范填写]\n\nretention_analysis:\n[按原规范填写]\n\ndetailed_description:\n[按原规范填写本段及承接状态]\n\noverall_soundscape:\n[按原规范填写]\n\nnon_diegetic_music:\n[按原规范填写]"
    }
  ]
}
```

| 字段 | 要求 |
| --- | --- |
| `global_prompt` | 必填空字符串。完整模式不会拼接它，不能在这里存放希望生效的规则。 |
| `segments` | 必填非空数组，一个对象对应一段；没有固定的 4、6 或 32 段上限。 |
| `id` | 必填整数，按数组顺序从 1 连续递增，不使用字符串、布尔值或小数写法。 |
| `title` | 必填非空字符串，可用用户提供的标题或“第一段”等中性名称。 |
| `raw_prompt` | 必填布尔值 `true`，不能写成字符串。 |
| `prompt` | 必填非空字符串，包含本段完整六节提示词。 |
| `seed` | 可选，仅在原有种子规则适用时添加；整数范围为 `0 <= seed < 2^63`。不要因打包格式新增种子要求。 |

固定结构不加入 `version`、`sets`、`clips`、`prompt_en`、`prompt_cn`、`prompt_i2v_en`、`scene_style`、时长或分辨率等额外字段。需要中文审阅稿时，按用户要求另行交付；不要用审阅翻译替换执行提示词。

机器可读定义见 [story-segments.schema.json](story-segments.schema.json)。JSON Schema 负责基础字段形状；严格整数写法，以及数组中 `id` 必须依次为 `1..N` 的跨元素规则，以下面的校验器为准。

## prompt 正文仍按原规范

`prompt` 是一个完整字符串。以下标题在字符串中恰好各出现一次、按原顺序排列，使用英文冒号，不加 Markdown 标题符号：

```text
subject_definitions:
summary:
retention_analysis:
detailed_description:
overall_soundscape:
non_diegetic_music:
```

六节的职责、英语写作约定及用户原语言保留例外、保留关系标记、镜头/对白标签等以原规范为准。本文件不重新定义这些规则。全局拍摄/表演约束仍放在每段 `detailed_description` 的 `[Shot 1]` 之前，后续镜头仍承接具体状态。

把已有完整提示词包装为 JSON 时，使用 JSON 序列化处理换行、引号和反斜杠。读取 JSON 后得到的 `prompt` 应与包装前的原文逐字符相同；不得为了装入文件而翻译、缩写或改写正文。格式包装不代表自动修复原文的其他问题。

## 按工作流选择引用绑定

- 原始双图动态工作流和方案六：`<Picture 1>`、`<Picture 2>` 分别保持原来分配的身份参考角色，不把第二张身份图变成尾帧。原始工作流从第 2 段开始绑定上一段尾部视频；方案六为混合策略，仅在选定的视频参考段绑定。实际绑定时始终使用 `<Video 1>`：若第 3 段使用视频参考，它指第 2 段尾部；若第 6 段使用，它指第 5 段尾部。未绑定的段不要写 `<Video 1>`。JSON 的 `id` 递增，视频输入编号不递增。
- 方案五（无 Video / Opening State）：六张图每段都按下表重新作为参考图输入；**任何一段都不绑定 `<Video 1>`**。从第 2 段起在各段完整提示词中描述上一段结束后的 Opening State 与下一步动作，不要把不存在的视频引用写进提示词。`raw_prompt: true` 时 Runner 直接使用 `prompt` 原文，不会自动补写承接语句。
- 视频带有音轨不代表已启用参考音频输入；仅在实际绑定了音频参考时按原规范定义 `<Audio N>`。
- 角色的身份、性别和实际人数来自用户要求及输入，不由文件格式规定。这是一套输入绑定说明，不是硬性首帧锁定或跨段连续性的保证。既有旧格式使用的尾帧图片和这里的尾部视频不能未经确认互换。

### 方案五：五张女主参考图的专用编号

适用工作流：`H3-动态多段-方案5-无Video-OpeningState-576x960.json`。在节点的 `female_reference_dir` 输入框里填写**任意存在的绝对目录路径**，例如 `F:\video\素材\2026-09-25-棕金礼服人物参考-v1`；该路径只是示例，不是默认值或固定目录。节点从你填写的目录读取文件名主干恰好为 `picture01` 至 `picture05` 的五张图片（支持 PNG、JPG、JPEG、WEBP）。男主图片仍由工作流中的单张图片节点提供。启动任务时六张图都会复制到该任务的 `refs` 文件夹，重做旧任务使用当时的快照。

| 提示词标签 | 输入 | 用途 |
| --- | --- | --- |
| `<Picture 1>` | `picture01` | 女主正脸近景 |
| `<Picture 2>` | `picture02` | 同一女主左侧约 30–45° 的 3/4 脸半身 |
| `<Picture 3>` | `picture03` | 同一女主右侧约 30–45° 的 3/4 脸半身 |
| `<Picture 4>` | `picture04` | 同一女主正面半身 |
| `<Picture 5>` | `picture05` | 同一女主正面全身 |
| `<Picture 6>` | 工作流中的男主单图 | 男主身份 |

五张女主图片是**一个人物的多角度身份参考**，不能把它们写成五位女性，也不能让任一参考照的姿势、裁切或背景强制接管镜头构图。提示词仍按原有六节格式写在每段 `prompt` 中，外层 JSON 字段不变。已有双图提示词用于新版方案五时，先核实原角色对应关系：原来代表男主的 `<Picture 2>` 需改为 `<Picture 6>`；新版 `<Picture 2>` 只表示女主左侧 3/4 脸。不要无差别替换所有 `<Picture 2>`，也不要改动单段 Ref2VA 或其他工作流的编号。

## 扩展段数和运行参数

四段就写四个对象，六段就追加 `id: 5`、`id: 6`，更多段按同样规则追加。每个对象都包含完整提示词，不能只写本段与上段的差异。

分辨率、采样步数、模型和时长由独立运行配置控制，不属于这个故事文件。当前动态 Runner 用项目配置中的 `segment_duration_seconds` 统一控制单段时长；在提示词里写“15 秒”不会自动设置生成时长。若用户要求不同段采用不同长度，先说明当前消费者需要额外支持，不添加会被忽略的 `duration_seconds` 字段，也不擅自改变用户时长。

段数没有固定上限不代表计算资源无限。此规范也不修改渲染器支持的帧数、尺寸或时长范围。

## 校验与交付

```text
python scripts/validate_story_segments.py /path/to/story_segments.json
```

校验器只检查 JSON 语法、字段集合、类型、非空值和连续编号；只输出段数和结构校验结果，不打印提示词正文，不改写文件，不联网、不提交渲染。它把 `prompt` 当作不透明字符串，不证明六节正文、语义、连续性、人物或成片质量合格。

正常创作仍执行原有提示词规范的交付前检查。用户限制正文检查时遵守限制，只报告已完成的结构检查，不能把它说成提示词内容审核通过。

交付生成的 JSON 文件和简短的段数/结构检查说明；时长计划作为单独说明，不伪装成此 JSON 已包含的运行设置。用户明确要求旧 `sequence.json` 或 Ref2VA/I2VA 双提示词包时，使用技能中的 Legacy 规范及旧校验器，不能混合两套外层字段。
