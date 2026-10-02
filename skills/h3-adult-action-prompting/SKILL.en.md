# H3 Adult Action Prompting — English Guide

This guide complements the repository's main `SKILL.md`.

The skill now uses a **paired bilingual source + single-plan + dual-document output** workflow.

## Source pair

Use:

```text
references/prompting-guide.json
references/prompting-guide-Chinese.json
```

The English JSON is the authoritative source for exact source terminology and prompt tokens. The Chinese JSON is the companion corpus for Chinese retrieval and review.

For a requested scene:

1. Retrieve the closest theme(s) from the source pair.
2. Extract useful:
   - Key Descriptive Elements;
   - Structure and Patterns;
   - Token Significance;
   - Actionable Advice.
3. Normalize them into one H3 semantic plan.
4. Render the English H3 document.
5. Render the Chinese H3 document from the same plan.
6. Run a bilingual parity check.

Do not create two independently authored prompts.

## Mandatory deliverables

Every successful execution returns:

```text
H3_Prompt_EN.md
H3_Prompt_ZH-CN.md
```

The English file is the canonical H3 prose rendering.

The Chinese file must contain the same:

- mode;
- subjects;
- reference roles;
- shot count and timing;
- action mechanics;
- cadence and amplitude;
- body response;
- camera;
- continuity;
- soundscape;
- music.

Keep H3 protocol tokens identical in both documents.

See:

- `references/bilingual-output-contract.md`

## Ref2VA output contract

Use these six sections in this exact order in **both** files:

```text
subject_definitions:
summary:
retention_analysis:
detailed_description:
overall_soundscape:
non_diegetic_music:
```

When pictures define character identity only:

```text
<Subject 1> is the fictional adult woman whose appearance comes from <Picture 1>.
<Subject 2> is the fictional adult man whose appearance comes from <Picture 2>.
```

Use `[reference generation]` when the pictures are identity/style references rather than literal target frames.

In the Chinese document, keep these exact structural tokens unchanged:

```text
subject_definitions:
summary:
retention_analysis:
detailed_description:
overall_soundscape:
non_diegetic_music:
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

Translate only the descriptive prose.

## Non-Ref2VA output contract

For T2VA / I2VA / FL2VA / L2VA, keep these field names in both files:

```text
integrated_multimodal_description:
overall_soundscape:
non_diegetic_music:
```

If H3 requires a fixed protocol sentence, preserve it exactly in both files.

## Motion translation formula

Translate vague source tags into:

```text
active subject
+ position
+ active body part
+ motion direction
+ cadence
+ amplitude/range
+ complete cycle
+ receiving-body response
+ stabilizers/contact
+ expression/gaze
+ camera
+ continuity
```

Example:

```text
<Subject 2> performs continuous forward-and-back pelvic thrusts
at a fast, steady cadence with a pronounced range of motion.
His hips visibly withdraw before each forward drive, creating
a complete repeated movement cycle.

<Subject 1>'s hips, waist, shoulders, and upper torso rock
forward and backward in synchronization with each thrust.
```

## Lookup order

When a user requests a specific adult action:

1. Search the English source for the closest exact theme/token.
2. Search the Chinese companion source using the same or equivalent theme.
3. Use the compact dictionaries only as fallback/normalization aids.
4. Preserve niche terminology only when it helps identify the action, camera, or style.
5. Remove redundant community slang that does not improve H3 execution.
6. Build one semantic plan.
7. Render both H3 documents from that plan.

## Delivery rule

When file creation is available, create both Markdown files and return links.

If file creation is unavailable, return two complete document blocks headed:

```text
H3_Prompt_EN.md
H3_Prompt_ZH-CN.md
```

Do not return a Chinese summary in place of the full Chinese H3 document.

## Safety boundary

This skill is only for explicitly adult fictional or synthetic characters.

Never:

- sexualize a real person's identity or likeness;
- turn a real person's uploaded image into explicit sexual content;
- use minors or ambiguous-age subjects;
- use age-regression or school-age sexual framing.

A real-person reference may only contribute non-identifying technical features such as pose geometry, camera angle, lighting direction, or composition, which must then be applied to fictional adult characters.
