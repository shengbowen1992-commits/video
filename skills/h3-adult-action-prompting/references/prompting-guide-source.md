# Original Prompting Guide Source

This skill is designed to work with the original community `prompting-guide.json` as a retrieval corpus.

Recommended local path when the source file is available:

```text
references/prompting-guide.json
```

Because the original file is large, the repository also contains compact normalized dictionaries and H3 translation references for fast lookup:

- `adult-action-dictionary-en.md`
- `adult-action-dictionary-zh.md`
- `h3-motion-translation-en.md`
- `h3-motion-translation-zh.md`
- `prompting-guide-usage-en.md`
- `prompting-guide-usage-zh.md`

If the full JSON is present, prefer source-first retrieval. If it is absent, fall back to the normalized references above.
