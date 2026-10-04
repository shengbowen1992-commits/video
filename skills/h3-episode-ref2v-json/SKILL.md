---
name: h3-episode-ref2v-json
description: 为 ComfyUI H3 双人物 Ref2V 整集工作流生成、修改或检查可上传的分段 JSON。全局 Picture 1 为女主、Picture 2 为男主，Picture 3 为每段开场图或上一段尾帧；逐段写秒数、图片绝对路径、内容 LoRA 和官方 Ref2VA 六字段 prompt。用户要求这个三图 Ref2V 工作流的分镜 JSON 时使用。
---

# H3 双人物 Ref2V 整集 JSON

交付实际 UTF-8 `.json` 文件，适配 **H3-整集JSON-Ref2V-双人物全局-Picture3开场参考**。外层 JSON 是本地工作流协议；内层 prompt 参照 MiniMax 官方 Ref2VA 格式。

## 编写

1. 阅读 [JSON 约定](references/json-contract.md) 和 [Ref2VA 写法](references/ref2va-format.md)。修改旧文件先读取原文，按用户要求保留内容及段号。
2. 从对话提取男女主身份图、每段剧情、开场来源、时长、对白、LoRA。Picture 1 女主、Picture 2 男主在画布全局选择，不写进 JSON。Picture 3 在每段 `first_frame` 指定。不要交换这三个槽位。
3. 每段显式写 `duration_sec`，未指定时按 10 秒起草并说明；内容 LoRA 未指定时写 `loras: []`。分辨率、FPS、原生/加速、步数、偏移、加速 LoRA、图片适配与参考图精度留在画布。
4. 图片段写真实本机绝对路径，查看已有参考图后描述开场。缺少路径时只标注草稿与待补素材，继续完成不受影响的段落，不虚构已存在图片。`previous_tail` 尚未生成时只根据预期承接状态规划；不能声称看过实际尾帧。
5. 为每段写独立英文六字段 prompt，女主为 `<Subject 1>`、身份来自 `<Picture 1>`；男主为 `<Subject 2>`、身份来自 `<Picture 2>`。将 `<Picture 3>` 单独定义为本段开场构图与当前场景状态。对白、歌词和画面文字保留用户原语言及原字句。
6. 每段内部从 `[Shot 1]` 开始；后续段也重新从 `[Shot 1]` 开始。服装当前状态、手持物、接触关系与位置按本段 Picture 3 承接，不从身份图重新恢复已经改变的状态，不重复已完成动作。同一个人在第三张图出现不意味着新增一个人物。
7. 用 JSON 序列化器保存。默认输出到当前工作区 `generated-json/<episode_id>.json`，用户指定位置优先。运行下方检查，再人工核对身份绑定、画面语义、动作/对白与秒数、LoRA 兼容性及触发词来源。交付文件链接、段数、各段秒数、计划总时长及待补项。

仅要求 JSON 时，交付文件即完成。渲染、上传和发布按用户对这些动作的实际授权执行。

## 开场图约束

本图通过 `MiniMaxH3ReferenceToVideo` 的三个参考输入绑定三张图。`first_frame` 是沿用本地 JSON 的字段名，实际进入 Ref2VA 第三参考槽位。**Picture 3 约束开场，不保证生成第一帧逐像素一致。** 使用尾帧也不保证动作速度、声音和剪辑无缝。不要因为字段叫首帧就改用 I2V 节点。

## 模板与检查

[三段模板](assets/episode.example.json) 为图片 → 上段尾帧 → 新图片，秒数 10、8、10。图像路径为教学占位，使用前替换；模板的动作也须按真实素材修改。

整个 skill 可单独复制安装，不读取其他 skill。Python 3.10+ 标准库即可进行结构检查：

```sh
python -X utf8 scripts/validate_episode.py /path/to/episode.json
```

交付可运行文件时，在素材所在机器检查两张全局身份图及各段开场图；图片解码需要 Pillow：

```sh
python -X utf8 scripts/validate_episode.py /path/to/episode.json --check-images --female-reference /path/to/female.png --male-reference /path/to/male.png
```

已有本机 Ref2V 项目时，加 `--project-root /path/to/h3-episode-ref2v-json` 调用真实 `h3_ref2v_episode/json_import.py`。附加 LoRA 名称可加 `--comfy-url http://127.0.0.1:8188`，只 GET 检查安装列表；未在线时报告未检查，不为写 JSON 启动服务。明确报告是否调用了真实导入器、检查了图片和 LoRA 名称；失败的显式检查不得降级为成功。

结构校验不能证明人物一致性、触发词有效、模型兼容性、声音自然或视频质量。技能包提供编写与校验，生成依赖外部 ComfyUI 节点、工作流及模型。
