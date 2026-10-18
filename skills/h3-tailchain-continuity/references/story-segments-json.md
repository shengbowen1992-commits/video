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

固定结构不加入 `version`、`sets`、`clips`、时长、分辨率或其他未定义外层字段。需要中文审阅稿时，按用户要求另行交付；不要用审阅翻译替换执行提示词。

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

## 唯一引用绑定：双身份图 + Picture 3 尾帧线稿

- **唯一支持：方案五衍生·尾帧线稿续接。** 第一段仅传 `<Picture 1>` 女主身份和 `<Picture 2>` 男主身份；从第 2 段起，额外传上一段实际最后一帧转换的线稿作为 `<Picture 3>`。身份图始终固定，第三张图随段更新但编号始终为 3。任何一段都不绑定 `<Video 1>`，也不切换到其他续接模式。
- 角色身份和实际人数来自用户要求及输入；文件格式只规定 Picture 1/2/3 的固定职责。
- 音频参考只有在工作流确实绑定音频输入时才定义 `<Audio N>`；本续接 profile 本身不增加视频参考或其他图像角色。

### 唯一支持：双身份图与 Picture 3 尾帧线稿

适用工作流：`H3-方案5衍生-全局人物-尾帧线稿续接-横竖屏.json`。这是原 Picture 3 尾帧参考方案增加线稿预处理后的版本，仍使用 Ref2VA。

| 提示词标签 | 第一段 | 第二段及以后 | 用途 |
| --- | --- | --- | --- |
| `<Picture 1>` | 固定女主参考图 | 同一张女主参考图 | 女主身份 |
| `<Picture 2>` | 固定男主参考图 | 同一张男主参考图 | 男主身份 |
| `<Picture 3>` | 不传入、不引用 | 上一段实际尾帧的线稿 | 首个 Shot 的开场构图、姿态、接触点、道具位置及动作阶段 |

运行时执行：完成单段视频 → 提取实际最后一帧 → 转成线稿 → 追加到下一段参考图。当前线稿版不做 2 倍超分或调色。写初始 JSON 时无需提前提供尚未生成的尾帧路径，也不能声称看过实际尾帧。

每个后续段的完整六节 `prompt` 必须保留 Pictures 1/2 的身份分工，并明确：**开场构图、人物位置、姿态、接触关系、道具位置及可见动作阶段以 Picture 3 为准；颜色、材质、衣服/身体状态和灯光由 `Continuity State Lock:` 承接。** 不再使用另一套纯文字开场状态方案，也不要用文字重复写死 Picture 3 已经表达的姿态或空间关系。下一步具体动作单独描述，从参考图状态继续。

每段在 `[Shot 1]` 前还必须写一次 `Reference Priority:` 和一次 `Character Identity Lock:`。前者明确 Pictures 1/2 的身份优先级高于 Picture 3；后者锁定脸型、眼型、发型、发色、肤色、身材比例、成年年龄观感和角色身份，禁止换脸、换发型、改年龄、改身材比例或生成成另一个角色。身份锁只锁身份，不冻结表情、姿态或剧情明确改变的服装状态。

默认尾帧线稿方案中，**每一段（包括第一段）**都必须在 `detailed_description` 的 `[Shot 1]` 前写一个 `Continuity State Lock:`。它负责线稿无法可靠表达的跨段状态，不是第二份姿态/构图描述。

`Continuity State Lock:` 至少按当前任务中已有且相关的信息覆盖：

- `Wardrobe/Body State:` 分人物写当前服装/层次、是否穿着、松开、部分脱下、完全脱下、扣合/解开、鞋履和必要的身体裸露状态。
- 衣服如果**只脱到一半**，必须记录剩余附着点和布料位置，例如哪只袖子/肩带/裤腿仍在、衣服堆在哪个身体位置、哪部分已经露出；下一 Shot/下一段从这个状态继续，不能重新从“完整穿着”开始，也不能无过程跳到“完全脱掉”。
- `Color/Material State:` 明确已建立且需要保持的头发/肤色外观、服装颜色/材质、床品、墙面、家具和重要道具颜色/材质。
- `Continuity State Lock:` 是**当前状态序列化器，不是历史账本**。某件衣物、鞋履、配饰或道具一旦进入“已不存在/已离开当前画面”的稳定终态，并且后续没有明确重新引入，就不要在后续段的 `Wardrobe/Body State:`、`Color/Material State:`、`retention_analysis:`、否定句、初始造型回顾或 `whenever still present` 一类条件句中继续点名它，也不要继续重复它的颜色/材质。这样可避免模型仅因名词再次出现而把已结束状态重新激活。
- 终态之后只写**正向当前状态**。例如人物已进入稳定全裸状态时，后续段直接写当前身体状态持续不变，不再逐件回顾此前脱掉的衣物。若已移除物仍真实留在当前画面中，例如衣服落在椅子或地面上，则把它作为独立场景道具记录当前位置、颜色和材质，而不是继续当作人物穿着状态。
- `Lighting/Exposure State:` 明确已建立的光源类型、方向、软硬、色温倾向、白平衡、曝光/对比度和整体色彩风格；剧情没有明确改变时，每段都重复要求保持一致。

除非用户明确指定另一种画面风格，每段英文执行提示词还必须重复下面这句默认母版观感；Picture 3 是线稿，不能替代色彩、黑位、高光、颗粒和镜头响应的文字承接：

`The image has a premium high-definition feature-film Blu-ray master appearance with balanced cinematic exposure, natural skin tone, deep clean blacks, readable layered shadows, smooth highlight roll-off, refined real-lens detail, restrained fine film grain, and stable color rendering.`

这句描述的是生成画面的视觉目标，不证明真实分辨率、码率、编码、位深、HDR 母版或蓝光碟制作。用户明确选择其他风格时，保留其风格，不使用该句，也不启用对应的可选校验开关。

第一段用用户提供的信息和真实参考建立基线，不猜看不见的细节。第二段及以后：姿态、人物位置、接触点、相机轴线、道具位置和可见动作阶段交给 Picture 3；文字状态锁负责颜色、材质、衣服/鞋履、道具可变状态和灯光/曝光。身份图不能把剧情已改变的状态重置。

已完成的一次性状态转换不因新段或切镜而再演一次；部分完成的转换必须从继承阶段继续。任何 Shot 真正改变衣服、道具、色彩或灯光状态时，在该 Shot 末尾写清** resulting state **，下一 Shot/段直接继承结果。

规划与实际证据分开处理：未来尾帧尚未生成时，只能从上一段**明确计划完成的结尾状态**推导下一段的文字状态，不能声称已看过未来 Picture 3；计划未明确完成、未知或无依据的状态不能猜测。实际结果经接受后，**已接受的原始尾帧决定可变状态，其派生线稿决定开场几何**。实际状态与计划不一致时，在授权范围内改写下一段或重做上一段，不能以冲突文字掩盖差异。当前视角无法辨认的细节沿用此前已确认且未改变的状态，不从黑白线条猜颜色。当前 Runner 自动传图，但不会自动识别状态、进行人工验收或重写提示词。

续接段可用以下结构；方括号内容只填相关且有依据的状态，不把模板原样交付，也不用于第一段：

```text
Reference Priority:
Priority 1: <Picture 1> is the female identity authority and <Picture 2> is
the male identity authority. Priority 2: <Picture 3> carries only the
immediately preceding accepted tail-lineart geometry and motion phase.

Character Identity Lock:
Preserve each referenced character's face shape, eye shape, hairstyle,
hair color, skin tone, body proportion, adult age appearance and identity.

Continuity State Lock:
Wardrobe/Body State: [per-subject current garment/body state; include exact
remaining attachment points and fabric location for any partial removal].
Color/Material State: [established subject, garment, bedding, wall, furniture
and important prop colors/materials that remain unchanged].
Lighting/Exposure State: [established light type/direction/softness,
color-temperature tendency, white balance, exposure/contrast, black level,
highlight roll-off, grain character and overall grade].

Opening Geometry: follow <Picture 3> for composition, positions, pose,
contacts, camera axis, prop placement and visible action phase.
Continue forward without replaying completed transitions.
```

不要让线稿成为目标画风，不把其中的人物当成第三个角色，也不从黑白线条臆测颜色或光照。第一段的整个 prompt 不得定义或提及 Picture 3，包括“没有 Picture 3”之类的否定句。多人物状态账本是创作过程中的工作记录，不添加到固定 JSON 外层字段。

## Shot Authoring Model

创作期可用下面的 Shot 对象整理信息，但它不是当前 Runner 的可执行外层 schema，不要直接把这些字段添加到交付的 `story_segments.json`。最终仍把有效内容写入现有六节 `prompt`；`references` 与 `continuity` 用于校对，不要把参考图已表达的身份、姿态和空间关系重复写成长篇文本。

```json
{
  "shot_id": "",
  "duration": "15s",
  "references": {
    "picture1": "female_identity_reference",
    "picture2": "male_identity_reference",
    "picture3": "previous_tailframe_lineart"
  },
  "continuity": {
    "previous_state": true,
    "maintain_identity": true,
    "maintain_environment": true,
    "maintain_pose_transition": true
  },
  "camera": {
    "movement": "",
    "angle": "",
    "lens_style": ""
  },
  "prompt": {
    "en": "",
    "zh": ""
  }
}
```

同时维护三类创作期状态：Character State（`identity`, `appearance`, `clothing_state`, `pose_state`, `emotion_state`）、Environment State（`location`, `lighting`, `color_temperature`, `camera_position`, `background_objects`）和 Motion State（`previous_pose`, `body_direction`, `camera_axis`, `movement_direction`）。实际交付文本只写剧情、镜头、动作、光影、声音，以及线稿无法表达但确需延续的非几何状态；不要用文字重新解释 Picture 3 已经给出的开场几何。

摄影机默认采用电影感真人实拍、受控且真实的手持运动、稳定轴线和顺滑有动机的转接。避免随机跳机位、不可能的透视变化、突然无动机变焦和镜头感不一致。除非用户明确要求风格化或 CGI，执行提示词加入 `photorealistic, real human skin texture, natural facial expression, realistic body movement, cinematic lighting, natural motion blur, high detail`；未覆盖默认风格时，再加入上面的高清电影蓝光母版标准句。排除 CGI 感、塑料/蜡像皮肤、过度磨皮、假人式动作、手机 HDR 感、锐化光晕、死黑、爆高光和不稳定颗粒。

使用 `raw_prompt: true` 时，把这些规则写进每段 `prompt`，不要指望外层 `global_prompt` 或 Runner 自动补写。JSON 外层结构不变，不添加尾帧路径、图像预处理或分辨率字段。Ref2VA 用第三张图约束开场，不承诺逐像素首帧一致，也不因此自动改用 I2V。

## 扩展段数和运行参数

四段就写四个对象，六段就追加 `id: 5`、`id: 6`，更多段按同样规则追加。每个对象都包含完整提示词，不能只写本段与上段的差异。

分辨率、采样步数、模型和时长由独立运行配置控制，不属于这个故事文件。当前动态 Runner 用项目配置中的 `segment_duration_seconds` 统一控制单段时长；在提示词里写“15 秒”不会自动设置生成时长。若用户要求不同段采用不同长度，先说明当前消费者需要额外支持，不添加会被忽略的 `duration_seconds` 字段，也不擅自改变用户时长。

段数没有固定上限不代表计算资源无限。此规范也不修改渲染器支持的帧数、尺寸或时长范围。

## 校验与交付

```text
python scripts/validate_story_segments.py /path/to/story_segments.json
```

上面的校验器只检查 JSON 语法、字段集合、类型、非空值和连续编号；只输出段数和结构校验结果，不打印提示词正文，不改写文件，不联网、不提交渲染。它把 `prompt` 当作不透明字符串。

当前默认的方案五衍生·尾帧线稿续接还应额外运行：

```text
python scripts/validate_tailchain_prompts.py --require-premium-bluray-master /path/to/story_segments.json
```

这个静态校验器只检查可机械确认的正文契约：六节标题恰好各一次且顺序正确、每段包含 Pictures 1/2、每段各包含一次 `Reference Priority:`、`Character Identity Lock:` 和 `Continuity State Lock:` 标记、正文不包含已移除的独立文字开场状态模块、第一段完全不提 Picture 3、第二段起必须引用 Picture 3、任何一段都不得引用 Video 1。加上 `--require-premium-bluray-master` 时，还会检查每段是否包含完全一致的高清电影蓝光母版标准句；只有用户明确选择其他风格时才省略该开关。它不会判断可变状态是否真的连续、表情/声音是否自然、动作是否重演、实际分辨率/编码或成片是否合格；这些仍按本 skill 的人工交付前检查、导出验证和渲染 QC 处理。

正常创作仍执行原有提示词规范的交付前检查。用户限制正文检查时遵守限制，只报告已完成的结构检查，不能把它说成提示词内容审核通过。

交付生成的 `story_segments.json` 和简短的段数/结构检查说明；时长计划作为单独说明，不伪装成此 JSON 已包含的运行设置。此 skill 不再提供其他 JSON/兼容 profile。
