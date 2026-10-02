# Original Prompting Guide Sources

This skill uses a paired English/Chinese prompting-guide corpus:

```text
references/prompting-guide.json
references/prompting-guide-Chinese.json
```

## Roles

### English source

`prompting-guide.json` is the authoritative source for:

- exact theme names;
- original English prompt tokens;
- caption phrasing;
- niche vocabulary;
- camera/style terminology;
- prompt-construction patterns.

### Chinese companion

`prompting-guide-Chinese.json` is the companion corpus for:

- Chinese lookup;
- Chinese reading and review;
- semantic cross-checking;
- helping Chinese-language requests map to the corresponding English source theme.

Prefer the same theme key(s) across both corpora.

Neither file is MiniMax H3 syntax.

## Retrieval rule

For every request:

1. identify the closest theme(s);
2. read the relevant source sections;
3. extract only useful semantics;
4. normalize them into one H3 semantic plan;
5. render both H3 deliverables from that plan.

Do not independently derive different English and Chinese prompts from the two corpora.

## Output contract

Every normal execution produces:

```text
H3_Prompt_EN.md
H3_Prompt_ZH-CN.md
```

See:

- `bilingual-output-contract.md`

## Supporting references

- `adult-action-dictionary-en.md`
- `adult-action-dictionary-zh.md`
- `h3-motion-translation-en.md`
- `h3-motion-translation-zh.md`
- `prompting-guide-usage-en.md`
- `prompting-guide-usage-zh.md`
