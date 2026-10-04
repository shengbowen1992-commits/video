# h3-adult-action-prompting

MiniMax H3 adult-action prompt skill for explicitly adult fictional/synthetic characters.

The skill uses a **paired bilingual source + H3 translation + dual-document output** architecture:

```text
prompting-guide.json
prompting-guide-Chinese.json
        ↓
paired retrieval / semantic normalization
        ↓
one shared H3 semantic plan
        ↓
H3_Prompt_EN.md
H3_Prompt_ZH-CN.md
```

## Mandatory deliverables

Every successful execution returns two synchronized H3 Markdown documents:

```text
H3_Prompt_EN.md
H3_Prompt_ZH-CN.md
```

The two documents use the same H3 mode, subjects, references, shots, timing, motion mechanics, camera, continuity, soundscape, and music.

The Chinese document is a full H3-formatted companion document, not a summary.

See:

- `references/bilingual-output-contract.md`

## Main files

- `SKILL.md` — skill router, source policy, H3 execution contract, dual-output requirement
- `SKILL.en.md` — English usage guide
- `SKILL.zh-CN.md` — 中文使用说明
- `agents/openai.yaml` — UI metadata

## Source / retrieval references

The full source pair is present:

- `references/prompting-guide.json`
- `references/prompting-guide-Chinese.json`

Use the English file as the authoritative source for exact theme/token wording and the Chinese file as the companion corpus for Chinese lookup and review.

Supporting references:

- `references/prompting-guide-source.md`
- `references/prompting-guide-usage-en.md`
- `references/prompting-guide-usage-zh.md`
- `references/bilingual-output-contract.md`

Neither JSON is treated as H3 syntax or pasted wholesale into final prompts.

## Fast normalized dictionaries

- `references/adult-action-dictionary-en.md`
- `references/adult-action-dictionary-zh.md`

These are compact lookup references, not replacements for the complete source corpora.

## H3 translation layer

- `references/h3-motion-translation-en.md`
- `references/h3-motion-translation-zh.md`

These references expand short source terms into continuous H3 motion, camera, body-response, and continuity language.

## Bilingual parity rule

Build one semantic plan first. Then render both files.

Keep H3 protocol tokens unchanged across both versions, including:

```text
<Subject N>
<Picture N>
<Video N>
[Shot N]
[reference generation]
```

For Ref2VA, both files keep the exact six-section field order.

## Safety / provenance

- `references/source-and-safety.md`

## Repository path

```text
skills/h3-adult-action-prompting/
```

This directory is a standalone skill package. Copy the whole directory when installing; no files from the repository root or sibling skills are required for ordinary use. Other skills are listed in the repository README and have their own directories.

The paired source JSON files are already included. The historical translation-maintenance scripts are optional: `build_bilingual_prompting_guide.py` uses `deep-translator` and network access; `prompting_guide_bilingual.py` uses `requests`, Argos Translate and its model runtime when translating. Do not run these scripts merely to install or use the skill. The stopped repository translation workflow remains stopped.

For maintenance of this standalone folder, `prompting_guide_bilingual.py merge` accepts `--skill-root` (defaults to this skill directory). The previous `--repo-root` option remains available for older repository automation.
