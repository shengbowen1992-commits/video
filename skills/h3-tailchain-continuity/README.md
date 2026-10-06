# H3 双人物身份 + Picture 3 尾帧线稿续接

当前默认使用方案五衍生的尾帧线稿版本：保留之前的 Ref2VA Picture 3 尾帧参考方案，将第三张图改为上一段实际尾帧的线稿。

| 项目 | 当前用法 |
| --- | --- |
| 本地工作流 | `H3-方案5衍生-全局人物-尾帧线稿续接-横竖屏.json` |
| 固定身份 | 每段均传 `<Picture 1>` 女主、`<Picture 2>` 男主 |
| 第一段 | 只有两张身份图，不引用不存在的 Picture 3 |
| 第二段及以后 | 追加上一段实际最后一帧转换的线稿，始终编号 `<Picture 3>` |
| 跨段承接 | Picture 3 提供开场构图、姿态与动作阶段；Opening State 文字补充这些状态和下一步动作 |
| 故事文件 | `story_segments.json`，每段 `raw_prompt: true`，完整六节 `prompt` |
| 运行参数 | 分辨率、4/8 步、LoRA 开关与强度、单段时长在工作流设置，不写进故事 JSON |

运行链路：单段视频 → 提取实际最后一帧 → 转线稿 → 下一段 Picture 3。不执行尾帧 2 倍超分或调色，不绑定参考视频。第三张图表达结构，人物身份仍由前两张图提供；输出保留用户要求的画风及当前颜色/服装状态，不照着线稿生成黑白画面。Ref2VA 参考图不保证逐像素首帧一致。

写初始 JSON 无需提供未来尾帧路径。每个后续段必须在实际 `prompt` 中说明 Picture 3 的用途，不能只写 Opening State 而漏掉图像引用，也不能声称已看过尚未生成的尾帧。

原版 `H3-动态多段-方案5-无Video-OpeningState-576x960.json`（也称 `H3-方案5-女主单图-男主单图-576x960.json`）仍可显式选择：它才是每段只传两张身份图、仅用文字承接的方案。旧彩色尾帧 Picture 3 版本也保留；继续已有任务使用其原配置和素材快照，不随 skill 默认值改变。

- [完整提示词规则](SKILL.md)
- [六节 Ref2VA 正文规范](references/ref2va-prompt-contract.md)
- [故事 JSON 结构与各方案绑定](references/story-segments-json.md)
- [V18 动作要求](references/v18-motion-intensity.md)
- [分层声音规范](references/h3-sound-prompt-standard.md)

本仓库提供提示词技能、格式说明和校验脚本；ComfyUI 节点与本地运行环境不随仓库分发。修改提示词 skill 不会启动渲染或改变已有任务。
