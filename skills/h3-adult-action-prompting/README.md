# h3-adult-action-prompting

MiniMax H3 adult-action prompt skill for explicitly adult fictional/synthetic characters.

The skill now uses a **source-first + H3 translation** architecture:

```text
original prompting-guide terminology
        ↓
semantic retrieval / normalization
        ↓
H3 motion translation
        ↓
T2VA / I2VA / Ref2VA prompt
```

## Main files

- `SKILL.md` — skill router and execution contract
- `SKILL.en.md` — complete English usage guide
- `SKILL.zh-CN.md` — 完整中文使用说明
- `agents/openai.yaml` — UI metadata

## Source / retrieval references

- `references/prompting-guide-source.md`
- `references/prompting-guide-usage-en.md`
- `references/prompting-guide-usage-zh.md`

The original large `prompting-guide.json` is treated as a retrieval corpus when available. It is **not** treated as H3 syntax or pasted wholesale into prompts.

## Fast normalized dictionaries

- `references/adult-action-dictionary-en.md`
- `references/adult-action-dictionary-zh.md`

These are compact lookup references, not replacements for the complete source corpus.

## H3 translation layer

- `references/h3-motion-translation-en.md`
- `references/h3-motion-translation-zh.md`

These files define how short source terms such as `pounding`, `riding`, `grinding`, `bouncing`, `POV`, or `close-up` are expanded into continuous H3 motion, camera, and continuity language.

## Safety / provenance

- `references/source-and-safety.md`

## Repository path

```text
skills/h3-adult-action-prompting/
```

The existing repository-root `SKILL.md` remains unchanged.
