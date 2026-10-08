# V18 动作频率与幅度规范

来源：用户提供的《V18_动作频率与幅度_提示词规范.md》。以下将其动作语言接入现有提示词结构；不新增剧情、姿势、角色、工作流或渲染授权。

## 触发与范围

视频创作或动作修改中，用户说“大幅度”“幅度再大点”“激情／激情一点”“激烈”“高频”“动作快一点”“更猛”“更有力”“强烈身体动作”或同义表达时，自动读取并应用本规范，不要求再说 V18 或手动粘贴模板。明确说“按 V18”也触发。

- 只改变用户指向的镜头、阶段或已有动作；“后半段激情一点”不改变前半段。
- “大幅度”优先增加单次位移与完整行程；“高频／动作快一点”优先增加真实动作频率；“激情／激烈／更猛”用于身体表演时，组合提高频率、幅度和力量。未要求渐强时，不自动安排三阶段递增。
- 按语义识别：否定的“不要大幅度”、台词里出现的词、引用示例、单纯询问词义不触发强化；“激情演讲”只增强声音、表情及已有手势，不凭空增加身体往复动作。“大幅度降价”等非视频动作语境不适用。
- 用户明确指定慢动作、快放、只改情绪或维持某项频率／幅度时，以该次明确要求为准，不能暗中用 V18 抵消。只做格式转换时保持原文，不因正文包含触发词就注入规则。

## 不变的核心

默认始终正常实时 1× 播放。“快”指演员真实动作次数变密，“大”指单次实际位移范围增大；不能通过加速视频、变速曲线、延时摄影或跳帧代替表演变化。仅写 `fast`、`intense`、`aggressive` 或 `stronger acceleration` 不足以表达这一要求。

描述至少明确：动作主体、真实频率、完整幅度、可见运动路径。保持用户指定的动作和场景；`strong hip drive` 与 `clear forward-and-back travel` 只用于已有动作确实由髋部驱动、具有前后行程的情况。挥拳用手臂与躯干的发力路径，跑步用步频、步幅与行进路径，不硬套同一身体部位。

当用户还要求“身体跟着抖动／晃动／回弹”或同义的次级运动时，把它写成**主动作造成的物理响应**，不要把次级运动写成独立循环。头发、松散布料、肩胸、腹部、臀腿或其他可见软组织的摆动、弹跳、压缩与回弹，应与当前冲击方向、频率和力量存在因果关系；主动作更强时响应可以更明显，但不要机械地要求每一次循环都完全同幅、同相、同声音。相机应保留足够身体上下文，让这种响应能被看见，同时不牺牲身份、接触关系或动作路径的可读性。

## 放进实际执行的提示词

- Ref2VA：在每段 `detailed_description:` 的 `[Shot 1]` 之前放一次 Motion Intensity Contract，保留原有六节结构。随后每个 Shot 只描述自身强度、路径和承接状态，不重复整段合同。
- `story_segments.json` 的 `raw_prompt: true` 模式：每段 `prompt` 都必须自带适用规则；外层 `global_prompt` 保持空字符串，因为完整模式不会拼接它。只写在外层会导致规则不生效。
- I2V／I2VA：放在该模式实际执行的动作描述中。旧三字段契约保留规定的起始句和字段顺序，在 `integrated_multimodal_description` 中的 `[Shot 1]` 后、具体动作之前放合同；不新增字段，不切换到 Ref2VA。
- 独立渲染的段各放一次；同段内多 Shot 不重复完整合同。仅后半段适用时，在合同中明确适用 Shot／时间范围，其余镜头保持原计划。

## 全局 Motion Intensity Contract

通用身体动作版本，按用户指定的频率／幅度范围适配：

```text
Playback remains normal real-time 1× throughout.
Any increase in speed refers only to the performers'
actual physical movement frequency and movement amplitude.
Use forceful, urgent, high-cadence, large-amplitude,
full-range movement along the action's established physical path.
As requested intensity increases, raise the performers'
actual movement frequency and amplitude while preserving
natural real-time playback.
Avoid shallow rocking, low-amplitude repetition,
hesitant pauses, restrained pacing, speed ramps,
fast-forward, time-lapse, frame skipping,
or artificially accelerated playback.
```

若用户只要求加大幅度，将频率条款改为保持当前频率；只要求高频且保留幅度时，保持既定完整行程。排除项仅作用于指定强化区间，不抹掉原有剧情停顿、对白或其他镜头的克制表演。

原 V18 第 11 节的髋部驱动版本，仅在动作路径适用时使用：

```text
Playback remains normal real-time 1× throughout.

Any increase in speed refers only to the performers'
actual physical movement frequency and movement amplitude.

Use forceful, urgent, high-cadence, large-amplitude,
full-range body movement with strong hip drive
and clear forward-and-back travel.

As intensity increases, raise the performers'
actual movement frequency and amplitude while preserving
natural real-time playback.

Avoid shallow rocking, low-amplitude repetition,
hesitant pauses, restrained pacing, speed ramps,
fast-forward, time-lapse, frame skipping,
or artificially accelerated playback.
```

## Shot 内强度语言

按已批准的阶段选择；不是固定新增三个镜头：

| 强度 | 推荐表述 |
| --- | --- |
| 中强度 | `forceful full-range movement with a clearly increased physical cadence` |
| 高强度 | `stronger actual movement frequency, larger travel along the established path, and more forceful movement` |
| 峰值 | `the strongest sustained real-time cadence and largest controlled movement amplitude of the sequence` |

动作确为往复时，高强度可用原句 `stronger actual movement frequency, larger forward-and-back travel, and more forceful reciprocal movement`。每个 Shot 写清当前主体、具体行程与状态，不能只留下形容词。

## 连续性与原有规则的协调

原来的 forward-only／不反向规则用于防止已经完成的剧情动作被重新演一遍。它不禁止用户要求的往复运动中每一周期的自然返回。循环动作跨段要保留当前周期的相位、方向、接触点、身份及空间位置，接着下一周期运动，不重置为准备姿势。

用户要求持续高频时，不强制每段末尾减速、停顿或静止；沿当前动作自然延续并保证可用的清晰尾帧。若实际尾帧不合格，按已有质检流程处理，不通过快放或机械冻结来掩盖。一次性姿势转换仍遵循原来的防重演规则。

## 与声音规范配合

写 H3 声音时默认应用 [通用声音规范](h3-sound-prompt-standard.md)。动作频率提高不等于每次动作都发一次声；人物反应按情绪和事件自然变化，声音中的短暂停顿不要求持续动作停止。

## 交付前检查

1. 触发词已按语义解析，适用区间与频率／幅度要求符合用户本次请求。
2. 每段实际执行提示词含 1× 实时约束、对应频率／幅度／路径与技术排除项；没有把规则只放进空的外层字段。
3. 全局合同与局部 Shot、循环承接、对白和剧情停顿无矛盾；没有新增用户未要求的动作或三阶段剧情。
4. JSON／技能结构检查只证明结构。获准渲染后，逐段按正常速度观看，核对真实动作频率、幅度、路径与跨段承接；文件帧率、时长、完整解码均不能单独证明表演符合规范。
