# How to Use the Original Prompting Guide — English

The original `prompting-guide.json` should be treated as a **retrieval/reference corpus**, not as a fixed H3 prompt template.

## Intended use

For a requested scene:

1. Write or identify the user's core intent:
   - subjects
   - action
   - pose
   - setting
   - style
   - camera
   - expression
2. Search the original JSON for the closest theme or vocabulary.
3. Read the relevant entry's:
   - Key Descriptive Elements
   - Structure and Patterns
   - Token Significance
   - Actionable Advice
4. Extract useful terminology and phrasing.
5. Normalize duplicate or conflicting slang.
6. Translate only the useful semantics into H3-ready continuous-motion language.
7. Place the result in the correct H3 mode structure.

## Do not

- paste the entire JSON into every prompt;
- treat every niche term as mandatory;
- copy image-only caption syntax blindly into video prompts;
- replace H3 camera/motion language with tag piles;
- treat identity-only pictures as literal first frames.

## Recommended retrieval query

Search by:
- exact sexual act;
- position;
- dominant motion verb;
- body-response term;
- camera term;
- style/aesthetic.

Example:

```text
rear-entry + pounding + gripping hips + frontal three-quarter + medium close
```

Then convert the retrieved concepts to H3 motion language.
