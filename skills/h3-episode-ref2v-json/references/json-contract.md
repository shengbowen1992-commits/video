# JSON 字段约定

这是画布全局参数版的编写子集，核对日期 2026-10-05。顶层仅包含 `version`、`episode_id`、`title`、`shots`。

| 字段 | 规则 |
| --- | --- |
| `version` | 整数 1 |
| `episode_id` | 1–80 位英文、数字、下划线、连字符；新集换值，续跑保持 |
| `title` | 用户可读标题 |
| `shots` | 1–64 段，按顺序生成 |
| `shots[].id` | 从 1 开始连续编号 |
| `duration_sec` | 显式填写，5–15 秒；小数须落在 24 FPS 帧边界 |
| `first_frame` | 本段 Picture 3 来源，见下文 |
| `prompt` | 完整 Ref2VA 六字段文本，换行按 JSON 正确转义 |
| `seed` | 可省略或 null；指定时为 0–18446744073709551615 的整数 |
| `loras` | 显式数组，每段最多 4 个；空数组表示无内容 LoRA |

男女主参考图通过画布全局上传或填写本机完整路径。不要向 JSON 添加 `identity_references`、`female`、`male`、`width`、`height`、`fps`、`sampling_profile`、`steps` 等字段。

第一段必须使用图片：

```json
"first_frame": {"type": "image", "path": "F:/素材/开场图/001.png"}
```

后续段使用上段尾帧：

```json
"first_frame": {"type": "previous_tail"}
```

用 `previous_tail` 时不写 `path`。PNG、JPEG、WebP 本机绝对路径均可；Windows 路径建议写 `/`，使用反斜杠时按 JSON 转义为 `\\`。网络共享、相对路径和 HTTP 图片网址不属于当前导入器的素材路径。

附加内容 LoRA 写准确文件名与强度：

```json
"loras": [{"name": "子目录/实际模型.safetensors", "strength": 0.6}]
```

同段不重复名称，强度在 -10 到 10 之间。名称需与 ComfyUI 的 LoRA 下拉列表完全一致；需要触发词时按作者说明写进本段 prompt，不凭名称猜触发词。每段独立填写，不从前段继承。加速 4/8 步 LoRA 由画布自动匹配 Ref2V 文件，不能写进内容 LoRA 数组。

导入器兼容的旧版参数字段不等于本 skill 的默认输出约定。修改用户旧 JSON 时先核实目标节点，避免丢弃目标版本所需字段。

校验器离线只检查路径语法。`--check-images` 要求同时提供 `--female-reference` 与 `--male-reference`，并检查所有现有输入可解码；未来尾帧无需预先存在。全局图 CLI 参数用于检查，不写入输出 JSON。
