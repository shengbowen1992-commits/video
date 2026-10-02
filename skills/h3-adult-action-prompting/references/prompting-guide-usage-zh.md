# 双语 Prompting Guide 使用方法 — 中文

使用以下两个源文件作为**检索/参考语料库**，而不是固定 H3 Prompt 模板：

```text
prompting-guide.json
prompting-guide-Chinese.json
```

## 推荐流程

针对一个用户场景：

1. 先确定：
   - 人物；
   - 动作；
   - 体位；
   - 环境；
   - 风格；
   - 镜头；
   - 表情；
   - 连续性要求。
2. 在英文 `prompting-guide.json` 中搜索最接近的主题、原始 token 和 caption 表达。
3. 在中文 `prompting-guide-Chinese.json` 中查看对应主题或等价主题的中文内容。
4. 阅读相关条目的：
   - Key Descriptive Elements
   - Structure and Patterns
   - Token Significance
   - Actionable Advice
5. 提取真正有用的术语、动作、镜头和结构信息。
6. 合并重复、冲突或无价值的社区 slang。
7. 生成一份统一 H3 语义计划。
8. 基于同一计划输出：
   - `H3_Prompt_EN.md`
   - `H3_Prompt_ZH-CN.md`
9. 做双语一致性校验。

## 源文件优先级

英文 `prompting-guide.json` 负责：

- 精确主题名；
- 原始 Prompt token；
- 英文动作/镜头术语；
- 原始 caption 表达。

中文 `prompting-guide-Chinese.json` 负责：

- 中文检索；
- 中文理解；
- 中文校对；
- 帮助中文需求映射回英文原主题。

不要因为中文版的翻译方式而改变英文原始 token 的含义。

## 不要这样用

- 不要把整个 JSON 塞进 Prompt；
- 不要认为所有 niche token 都必须保留；
- 不要把图片 caption 语法直接复制成视频 Prompt；
- 不要让英文版和中文版分别重新生成；
- 不要让翻译改变 Shot、Subject、Picture、Video 编号或时间戳；
- 不要用大量 tag 堆叠替代 H3 的动作、镜头和连续性语言；
- 不要把只用于角色身份的参考图片误当成首帧。

## 推荐检索形式

按组合搜索：

```text
体位 + 核心动作 + 身体反馈 + 镜头 + 风格
```

例如：

```text
rear-entry + pounding + gripping hips + frontal three-quarter + medium close
```

然后把检索到的语义改写成完整 H3 视频语言。

## 最终交付

默认必须交付两个完整同步的 H3 文档：

```text
H3_Prompt_EN.md
H3_Prompt_ZH-CN.md
```

详细规则：

- `bilingual-output-contract.md`
