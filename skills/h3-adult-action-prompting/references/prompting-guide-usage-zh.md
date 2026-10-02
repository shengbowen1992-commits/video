# 原版 Prompting Guide 使用方法 — 中文

原始 `prompting-guide.json` 应当作为**检索/参考语料库**使用，而不是固定的 H3 Prompt 模板。

## 推荐使用流程

针对一个用户场景：

1. 先确定核心需求：
   - 人物
   - 动作
   - 体位
   - 环境
   - 风格
   - 镜头
   - 表情
2. 在原始 JSON 中搜索最接近的主题或词汇。
3. 阅读相关条目的：
   - Key Descriptive Elements
   - Structure and Patterns
   - Token Significance
   - Actionable Advice
4. 提取真正有用的术语和措辞。
5. 合并重复、冲突或无价值的社区 slang。
6. 只把有用语义转换成 H3 连续视频动作语言。
7. 再放进对应的 H3 模式结构。

## 不要这样用

- 不要每次把整个 JSON 全部塞进 Prompt；
- 不要认为每个 niche 词都必须保留；
- 不要把图片 caption 语法原样照搬成视频 Prompt；
- 不要用大量 tag 堆叠替代 H3 的镜头和动作描述；
- 不要把只用于角色身份的图片错误当成首帧。

## 推荐检索方式

可以按以下组合搜索：
- 明确性行为
- 体位
- 核心运动词
- 身体反馈词
- 镜头词
- 风格词

例如：

```text
rear-entry + pounding + gripping hips + frontal three-quarter + medium close
```

找到源词之后，再转成 H3 的完整动作句。
