# H3 成人动作提示词 — 中文指南

本文件是主 `SKILL.md` 的中文版说明。

现在这个 Skill 的核心流程是：

```text
中英文 Prompting Guide 双语检索
→ 生成一份统一的 H3 语义计划
→ 输出英文 H3 文档
→ 基于同一语义计划输出中文 H3 文档
→ 双语一致性校验
```

## 双语源文件

固定使用：

```text
references/prompting-guide.json
references/prompting-guide-Chinese.json
```

其中：

- `prompting-guide.json`：英文原始语料，负责精确主题名、Prompt token、caption 表达和英文术语。
- `prompting-guide-Chinese.json`：中文对应语料，负责中文检索、理解和校对。

优先使用相同主题 key 或等价主题进行双语检索。

不要把两份 JSON 直接当成 H3 官方语法，也不要整段照搬到最终 Prompt。

## 强制输出两个文档

每次 Skill 正常执行完成后，默认必须产出两个独立 Markdown 文档：

```text
H3_Prompt_EN.md
H3_Prompt_ZH-CN.md
```

这两个文档不能分别“重新创作”。

正确流程是：

1. 先根据用户需求和双语 Guide 检索结果生成**一份统一语义计划**。
2. 先渲染英文 H3 文档。
3. 再从同一语义计划渲染中文 H3 文档。
4. 最后做双语一致性校验。

只有用户在当前请求里明确说“只要英文”或“只要中文”时，才可以省略另一份。

详细规则：

- `references/bilingual-output-contract.md`

## Ref2VA 六段格式

如果是 Ref2VA，两个文档都必须严格使用以下六段，顺序不能变：

```text
subject_definitions:
summary:
retention_analysis:
detailed_description:
overall_soundscape:
non_diegetic_music:
```

中文版也**不要翻译这些字段名**。

中文版只翻译字段内部的自然语言描述。

以下 H3 协议标记在中英文两个文件中都必须保持完全一致：

```text
<Subject N>
<Picture N>
<Video N>
[Shot N]
[reference generation]
fully_preserved
partially_preserved
attribute_transfer
weak_reference
```

时间戳、Shot 编号、Subject 编号、Picture 编号也不能因为翻译而改变。

## 非 Ref2VA 格式

对于 T2VA / I2VA / FL2VA / L2VA，中英文两个文件都保留这些 H3 字段名：

```text
integrated_multimodal_description:
overall_soundscape:
non_diegetic_music:
```

如果某种模式要求固定协议句，则即使在中文版中，该固定协议句也保持原样。

## 统一语义计划

双语输出之前，先整理一份内部 H3 计划：

```text
H3 模式
→ 人物与参考图/视频角色
→ 体位和空间几何
→ 主动方
→ 主动身体部位
→ 运动方向
→ 频率
→ 幅度
→ 完整动作周期
→ 接收方身体反馈
→ 支撑点 / 接触点
→ 表情 / 视线
→ 镜头
→ 环境 / 灯光
→ 连续性
→ 声音 / 音乐
```

不要直接把 `fast`、`rough`、`intense` 这种模糊词当最终动作描述。

要转换成可见、可执行的运动机制，例如：

```text
快速、稳定的连续前后骨盆运动
+ 明显运动幅度
+ 每次前驱之前有清晰回撤
+ 接收方腰、肩和上半身同步反馈
```

## 推荐检索流程

用户提出具体动作或主题时：

1. 先在英文 `prompting-guide.json` 中找最接近的主题和关键 token。
2. 再在 `prompting-guide-Chinese.json` 中查看对应中文内容。
3. 阅读该主题的：
   - Key Descriptive Elements
   - Structure and Patterns
   - Token Significance
   - Actionable Advice
4. 提取真正对视频生成有效的信息。
5. 去掉重复、冲突或只对社区标签有意义的 slang。
6. 转换成完整 H3 动作、镜头和连续性语言。
7. 输出完全同步的英文版和中文版。

## 两个文档必须保持一致的内容

最终交付前检查：

- H3 模式一致；
- Subject 数量和编号一致；
- Picture / Video 引用一致；
- Shot 数量和顺序一致；
- 时间戳一致；
- 动作方向一致；
- 动作频率和幅度一致；
- 身体反馈一致；
- 镜头位置、景别和运动一致；
- 连续性约束一致；
- 声音设计一致；
- 音乐设置一致。

中文版必须是**完整 H3 文档**，不能只做英文版摘要。

## 文件交付规则

如果当前环境支持创建文件，直接创建：

```text
H3_Prompt_EN.md
H3_Prompt_ZH-CN.md
```

并返回两个文件的下载链接。

如果当前环境不支持文件创建，则在回复中分别给出两个完整文档块。

## 安全边界

本 Skill 只用于明确成年、虚构或合成角色。

禁止：

- 将真实人物身份或肖像用于露骨性内容；
- 把真实人物上传照片直接转换为露骨色情内容；
- 未成年人或年龄不明确角色；
- 年龄回退、校园未成年化性场景。

真实人物图片最多只能提取不具身份性的技术信息，例如姿势几何、镜头角度、光线方向和构图，然后应用到虚构成年角色。
