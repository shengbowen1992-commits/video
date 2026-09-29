# 当前尾帧续接版：实际文件示例

先读 [完整要求与运行说明](../../references/plan5-tailimage.md)。这里的 JSON 有不同用途，不能互相替代。

| 文件 | 用途 |
| --- | --- |
| [story_segments.json](story_segments.json) | 12×5秒、3:5测试的分段故事文件；可通过仓库结构校验，导入本衍生工作流时另设每段5秒、576×960。 |
| [source-audit.json](source-audit.json) | 从本地测试文件移出的测试记录、逐段提示词哈希及与实际执行图的比对结果。 |
| [benchmark-continuation-executed.txt](benchmark-continuation-executed.txt) | 最新5/10/15秒耗时测试共用的实际执行提示词，含控制器参考前缀；这是已经拥有上一段尾帧的续接样片。 |
| [benchmark-10s-api.json](benchmark-10s-api.json) | 上述提示词实际执行的10秒 ComfyUI API 图，243帧、576×960、Turbo4；不是画布布局文件，也不是 story_segments.json。 |
| [duration-benchmark.json](duration-benchmark.json) | 两轮6次实测数据、计时口径、参数和限制。 |
| [continuation-six-sections.txt](continuation-six-sections.txt) | 当前无前缀的完整六节续接正文；保留原六节内容与内部参考角色，已准备、未重新渲染。 |
| [continuation-10s-prepared-api.json](continuation-10s-prepared-api.json) | 与无前缀正文对应的10秒 API 图；不是实际执行记录，不可用作故事 JSON。 |
| [six-section-revision.json](six-section-revision.json) | 新旧文本哈希、参数差异及未渲染状态。 |

## 当前格式：六节正文直接执行

控制器已取消额外前缀，身份定义、尾帧保留和具体接续都由六节正文表达。`story_segments.json` 原本就包含这些内容，因此无需改写12段历史正文便可由新建任务直接使用；这是格式修改，不是剧情连续性修复。新任务审计比较 `story.prompt == saved_prompt == graph.prompt`。

下面的历史文件保持原样：带 `executed` 的文本和原 `benchmark-10s-api.json` 仍记录修订前真实执行内容。新 `prepared` 文件只移除六节前的重复说明、使用独立输出文件前缀，其余生成参数与六节正文保持一致；没有重新渲染，不能把旧耗时／画面结论当作新格式的效果证明。

## 历史12段示例

保留每段原 `prompt`、标题和种子；只把非标准 `test_metadata` 字段移到 `source-audit.json`，没有把它改写成10秒剧情。每段六节正文均与本机实际执行图核对，差别只有已记录的控制器前缀。示例里的身份编号只是该次角色标识，使用者需在工作流里提供对应两张全局人物图。

这版是压力测试记录，**存在多出人物、手部伪影、部分段落重置及衣物回跳等已知问题**。公开的是当时实际使用的提示词，不冒充修复后的无缝连续模板。不要把示例里的室内情侣剧情、动作或演员身份推广成其他任务的默认要求。

```sh
python scripts/validate_story_segments.py examples/plan5-tailimage/story_segments.json
```

该命令只检查外层结构，不证明画面质量或连续性通过。

执行文本保留控制器前缀末尾的原始空格；本目录 `.gitattributes` 为该审计文件关闭换行转换，JSON 固定 LF，便于按记录的 SHA-256 核对。

## 最新时长测试

以历史第7段的高清尾帧为同一起点，对第8段舞蹈提示词做时长中性调整：去掉固定五秒措辞，将固定步数改为整个请求时长持续的步频。两轮全部样片共用这份文本，同轮同种子；没有把上一条测试输出接到下一条测试，因此不能用这些独立样片验证长链衰减。

两个 API 图都保留原参考输入文件名和模型名，使用者需要对应模型、自定义节点及三个参考文件；本仓库没有上传人物图片、尾帧或视频。直接在其他机器提交可能缺少资源。它们不是无需准备即可启动的通用安装包。不要把含 Picture 3 的续接文本当成无上一段尾帧的第一段。新任务使用无前缀六节正文，旧执行文本用于审计，不能作为当前格式模板。

本次本地控制器仅修改了提示词拼接行为，图片绑定与模型参数不变；仓库发布规范、文字和 JSON 示例，没有发布媒体素材，也没有证明以前的连续性问题已修复。
