# H3 声音提示词通用规范

来源：用户提供的《H3_声音提示词通用规范.md》。本文件将其两层声音结构接入现有 H3 提示词格式。以后新写或修改 H3 声音提示词时默认应用，无需用户再次点名。只做格式转换时保留原文；示例不授权增加人物反应、对白、剧情、配乐或参考音频输入。

## 两层结构与配乐分工

| 内容 | 位置 |
| --- | --- |
| 已确定的声音类型、整体风格、连续环境底声、自然变化和技术排除项 | `overall_soundscape` |
| 发声者、动作或情绪触发点、质感、音高／强弱／时长变化、必要停顿、跨镜头衔接 | 对应 `[Shot N]` |
| 精确对白、歌词、场景内可听见的音乐、与动作同步的物理音效 | 对应 `[Shot N]` |
| 观众听见而人物听不见的配乐 | `non_diegetic_music` |

Ref2VA 的 Shot 写在 `detailed_description`；I2V／I2VA 等三字段模式的 Shot 写在 `integrated_multimodal_description`。保留该模式原来的开场引用句、字段顺序、标签和切点语法，不因声音规则切换工作流或新增字段。

`overall_soundscape` 按现有格式用 1–4 句简洁英文概括，不堆逐秒事件、精确发声次数或第二份镜头脚本。先写每个 Shot 的具体声音，再总结整段，避免两处矛盾。每个独立生成的段都自带适用声音规则；`story_segments.json` 的 `raw_prompt: true` 模式不能只把规则放在不会拼接的外层 `global_prompt`，该字段仍为空字符串。

## 全局模板：按当前场景选择

已经确定有人物声音和环境声时，可从原规范的最简模板开始，再按实际场景具体化：

```text
overall_soundscape:
Human vocal reactions and scene ambience remain natural,
performance-driven, and responsive to the action.
Vocal pitch, duration, intensity, spacing, and texture vary organically
rather than repeating in a fixed mechanical pattern.
Specific synchronized vocal reactions and sound changes
are described inside each shot.
```

只强调已确定的人声、不要求环境声时：

```text
overall_soundscape:
The human vocal performance remains natural, irregular,
and responsive to the action.
Avoid obvious mechanical looping or uniform repetition.
Specific synchronized vocal reactions and their timing
are described inside each shot.
```

环境声重要时，说明当前场景实际的底声及其持续关系，例如克制的室内底噪；不把室内环境强加给户外镜头。只需环境音／物理音效时，不加入人物发声模板。无对白不等于完全静音；明确要求整段无声时用 `overall_soundscape: N/A`，并去掉 Shot 内矛盾的声音事件。没有请求配乐时保持 `non_diegetic_music: N/A`；文档里的电子乐示例不是默认曲风。

## Shot 内声音的写法

只在声音影响效果的镜头写必要细节，不给每一秒强塞声音，也不为演示模板增加三个镜头。通常一个主要触发点、一次变化和必要时一个停顿就足够；具体数量服从场景和用户要求。

写清四个维度：

1. **Trigger**：谁在什么动作或情绪变化时发声；物理音效绑定接触、落地、门锁闭合等实际事件。
2. **Texture**：按场景选择 `soft`、`low`、`muffled`、`open`、`trembling`、`sharp`、`strained`、`warm`、`short`、`fuller` 等。`breathy-but-voiced` 表示带气息但仍有声带发声，不等于纯呼吸循环。
3. **Dynamics**：说明如何变化，如先低后饱满、短暂尖锐后回落、音高与强度稍升；不要每个 Shot 都只写 `louder` 或 `more intense`。
4. **Spacing**：反应之间允许自然不等长间隔和短暂停顿，如 `followed by a short natural pause`；不强制每次运动对应一次发声。

结构示例，替换为用户当前场景，不原样交付占位文字：

```text
[Shot N] ...
As the established action reaches its trigger,
the identified subject gives the planned vocal reaction.
Describe its texture and change in pitch, intensity or duration,
then any necessary pause and its transition into the next shot.
```

发声主体和 `(Sx)` 使用现有提示词规范的稳定标签。非语言反应的质感和动作写在说明文字中，不伪装成新增对白；已有对白按原语言、原字句及 `<d>[Language] ...</d>` 规则保留。声音发生在镜头切点两侧时，说明是连续、衰减、停顿还是新的反应；对白跨切点继续使用既有 `<scenetrans>` 规则。

## 自然变化、嘴部状态与 V18 动作强度

- 默认避免固定每秒几次发声、每个动作一个固定音节、始终同一音高／音量等机械循环。自然反应使用变化的音高、时长、质感、强弱与间隔；这不是禁止用户明确要求的节拍、精确次数或同步声效。脚步、碰撞、拍手等因果同步的物理声音仍准确对齐实际事件。
- 声音与可见嘴部状态一致。若既定动作使嘴部受阻，适用的反应可短暂变闷；恢复开口时再变清楚。原文的接吻例子仅适用于剧情已包含该动作时，不作为默认情节，也不让闭嘴的倾听者说话。
- 配合 V18 时，人物真实动作频率提高可让已要求的声音反应更及时、稍密或更饱满，但保留自然间隔。不要机械地每动一次就发一次声，也不自动让所有声音都更响。
- 可按场景使用 `As the performers' actual physical cadence increases, the vocal reactions become somewhat more frequent and fuller, while remaining irregularly spaced.` 或 `The vocal timing does not match every movement one-for-one.`，仅描述已确定的人物反应。
- V18 的持续动作与声音中的短暂停顿可以并存；声带休止不代表肢体必须停止。正常实时 1× 的画面和声音保持同步，不用后期加速音轨或画面制造强度。

## 配乐与实际音频参考

只有请求包含观众配乐时才写其乐器、速度、节奏、发展和相对人声的音量关系。人物在场景里能听到的音乐按场景声处理，不误放到 audience-only score。

只有工作流确实绑定音频参考时才定义 `<Audio N>`。引用规范不自动启用节点或复用源视频录音；准确对白重演、音色参考和原录音复用是不同要求。

- `subject_definitions`：说明来源、作用和关联发声者，例如 `<Audio 1> is the vocal-timbre and delivery reference for <Subject 1> (S1).`，复用目标人物既定的 speaker ID。
- `retention_analysis`：将原文泛称的 copy 按实际用途写为正式标记 `fully_copy` 或 `partially_copy`；生成式音色／表演参考用 `reference`，仅宽泛氛围用 `weak_reference`。不要直接写未定义的 `copy` 标记。
- 对应 Shot：注明何时使用该音色、表演风格或被复用的音频事件，并保留现有标签规则。
- `overall_soundscape` 或 `non_diegetic_music`：在对应声音层总结引用关系；不只在全局提一次就省略关键事件，也不重复整段对白。

## 编写与验收顺序

先确定画面和已批准的声音意图 → 找各 Shot 的声音触发点 → 写必要的主体、质感、动态和间隔 → 总结 `overall_soundscape` → 单独处理配乐 → 检查整段及跨段衔接。

交付前检查：声音来源清楚；反应与动作、嘴部状态和情绪一致；对白原文与标签保留；全局与局部无矛盾；未新增未请求的发声或配乐；实际音频参考和正式标记一致；每段执行提示词都包含所需规则。

格式／JSON 校验不能证明声音自然或同步。获准渲染后，按正常速度逐段试听并核对事件时机、口型、机械重复、停顿、跨镜头接缝、人声与配乐层级，以及最终成片段首杂音。没有完成试听时如实标记未验证；不能把音轨存在或解码通过称为声音验收通过。
