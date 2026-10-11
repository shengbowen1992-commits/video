# H3 双人物身份 + Picture 3 尾帧线稿续接

本 skill 只保留方案五衍生的尾帧线稿版本：固定使用 Ref2VA Picture 3 尾帧线稿续接，不再保留其他 JSON/续接 profile。

| 项目 | 当前用法 |
| --- | --- |
| 本地工作流 | `H3-方案5衍生-全局人物-尾帧线稿续接-横竖屏.json` |
| 固定身份 | 每段均传 `<Picture 1>` 女主、`<Picture 2>` 男主 |
| 第一段 | 只有两张身份图，不引用不存在的 Picture 3 |
| 第二段及以后 | 追加上一段实际最后一帧转换的线稿，始终编号 `<Picture 3>` |
| 参考优先级 | Priority 1：Picture 1 女主身份 + Picture 2 男主身份；Priority 2：Picture 3 仅承接动作、空间、姿态和摄影机状态 |
| 跨段承接 | Picture 3 只管几何/动作相位；每段必须写 `Reference Priority`、`Character Identity Lock` 和 `Continuity State Lock`，不再使用独立文字开场状态模块 |
| 故事文件 | `story_segments.json`，每段 `raw_prompt: true`，完整六节 `prompt` |
| 静态校验 | `validate_story_segments.py` 校验外壳；`validate_tailchain_prompts.py` 校验六节标题、三块前置约束及 Picture/Video 绑定 |
| 运行参数 | 分辨率、4/8 步、LoRA 开关与强度、单段时长在工作流设置，不写进故事 JSON |

运行链路：单段视频 → 提取实际最后一帧 → 转线稿 → 下一段 Picture 3。不执行尾帧 2 倍超分或调色，不绑定参考视频。第三张图表达结构，人物身份仍由前两张图提供；输出保留用户要求的画风及当前颜色/服装状态，不照着线稿生成黑白画面。Ref2VA 参考图不保证逐像素首帧一致。

写初始 JSON 无需提供未来尾帧路径。每个后续段必须在实际 `prompt` 中说明 Picture 3 的用途，不能只写文字状态而漏掉 Picture 3 图像引用，也不能声称已看过尚未生成的尾帧。

文字不预先写死“已经坐下”等可见开场几何状态。每段在 [Shot 1] 前写 `Reference Priority:`、`Character Identity Lock:` 和 `Continuity State Lock:`：Pictures 1/2 锁定脸型、眼型、发型/发色、肤色、身材比例、成年年龄观感和角色身份；Picture 3 只锁定上一段尾帧的动作、空间、姿态、接触点、镜头轴线和运动方向。文字仅补充剧情、镜头、动作、光影、声音及线稿不能表达的非几何状态，避免重复解释参考图造成漂移。

默认真人质感为 photorealistic、真实皮肤纹理、自然表情与身体运动、电影照明、自然运动模糊和高细节；排除 CGI 感、塑料/蜡像皮肤、过度磨皮和假人式动作。摄影机采用电影感真人实拍、受控真实手持、稳定轴线与顺滑有动机的转接，避免随机跳机位、不可能透视、突然无动机变焦和镜头感不一致。

唯一支持的链路为：每段固定 Picture 1 女主身份 + Picture 2 男主身份；Segment 2 起追加上一段实际尾帧转换的 Picture 3 线稿。不要切换到纯文字、彩色尾帧、视频参考或其他兼容模式。

- [完整提示词规则](SKILL.md)
- [六节 Ref2VA 正文规范](references/ref2va-prompt-contract.md)
- [故事 JSON 结构与各方案绑定](references/story-segments-json.md)
- [V18 动作要求](references/v18-motion-intensity.md)
- [分层声音规范](references/h3-sound-prompt-standard.md)
- [成人露骨动作连续性（仅虚构成年人露骨场景启用）](references/adult-action-continuity.md)
- [成人体位与高冲击动作库（性交姿势、动作路径、支撑点、镜头与尾帧相位模板）](references/adult-position-motion-library.md)
- [H3 LoRA 路由（可选：trigger、强度、动态启停与堆叠排错）](references/h3-lora-routing.md)
- [默认尾帧线稿静态 Prompt 校验器](scripts/validate_tailchain_prompts.py)

本仓库提供提示词技能、格式说明和校验脚本；ComfyUI 节点与本地运行环境不随仓库分发。修改提示词 skill 不会启动渲染或改变已有任务。
