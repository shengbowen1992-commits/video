# How to Use the Paired Prompting Guides — English

Use the source pair as a **retrieval/reference corpus**, not as a fixed H3 prompt template:

```text
prompting-guide.json
prompting-guide-Chinese.json
```

## Workflow

For a requested scene:

1. Identify the user's:
   - subjects;
   - action;
   - position;
   - setting;
   - style;
   - camera;
   - expression;
   - continuity requirements.
2. Search `prompting-guide.json` for the closest exact theme(s) and source tokens.
3. Search `prompting-guide-Chinese.json` for the corresponding Chinese theme/content.
4. Read the relevant entry's:
   - Key Descriptive Elements;
   - Structure and Patterns;
   - Token Significance;
   - Actionable Advice.
5. Extract useful terminology and prompt-construction patterns.
6. Normalize duplicate/conflicting slang.
7. Build one H3 semantic plan.
8. Render:
   - `H3_Prompt_EN.md`
   - `H3_Prompt_ZH-CN.md`
9. Run the bilingual parity check.

## Source priority

Use the English source as authoritative for exact English theme/token wording.

Use the Chinese source for Chinese-language retrieval, comprehension, and review.

Do not let the Chinese file cause the English output to drift away from the original source terminology.

## Do not

- paste the full JSON into prompts;
- treat every niche token as mandatory;
- copy image-caption syntax blindly into video prompts;
- generate the English and Chinese prompts independently;
- use tag piles instead of H3 motion/camera language;
- change shot timing or reference numbering during translation;
- turn identity-only pictures into literal first frames.

## Recommended retrieval query

Search by combinations such as:

```text
position + dominant motion verb + body response + camera + style
```

Example:

```text
rear-entry + pounding + gripping hips + frontal three-quarter + medium close
```

Then convert the retrieved semantics to H3 motion language.

## Delivery

The default deliverable is always the two full synchronized H3 documents.

See:

- `bilingual-output-contract.md`
