---
name: h3-adult-action-prompting
description: Convert adult-action intent for explicitly adult fictional or synthetic characters into MiniMax H3 T2VA/I2VA/Ref2VA prompts. Retrieve from the paired English/Chinese prompting-guide corpora, normalize action/camera/continuity semantics once, then always deliver synchronized English and Simplified-Chinese H3 documents.
---

# H3 Adult Action Prompting

Use this skill for explicitly adult **fictional or synthetic** characters.

## Mandatory output

Every successful execution produces two synchronized Markdown documents:

```text
H3_Prompt_EN.md
H3_Prompt_ZH-CN.md
```

Read and follow:

- [references/bilingual-output-contract.md](references/bilingual-output-contract.md)

Do **not** independently invent the English and Chinese versions. Build one semantic H3 plan, render the English document, then render the Chinese document from the same plan and run a parity check.

Only return one language if the user explicitly asks for a single-language deliverable.

## Language guides

- English instructions: [SKILL.en.md](SKILL.en.md)
- 中文说明：[SKILL.zh-CN.md](SKILL.zh-CN.md)

## Paired source corpora

The source corpora are now present in this skill:

```text
references/prompting-guide.json
references/prompting-guide-Chinese.json
```

Use them as a paired retrieval corpus:

- `prompting-guide.json` is the authoritative source for exact English theme names, prompt tokens, caption phrasing, and source terminology.
- `prompting-guide-Chinese.json` is the Chinese companion corpus for Chinese lookup, comprehension, and review.
- Prefer the same theme key(s) across both files.
- Do not treat either JSON file as MiniMax H3 syntax.
- Do not paste source entries wholesale into the final H3 prompt.

Read:

- [references/prompting-guide-source.md](references/prompting-guide-source.md)
- [references/prompting-guide-usage-en.md](references/prompting-guide-usage-en.md)
- [references/prompting-guide-usage-zh.md](references/prompting-guide-usage-zh.md)

Compact fallback dictionaries remain available for fast lookup:

- [references/adult-action-dictionary-en.md](references/adult-action-dictionary-en.md)
- [references/adult-action-dictionary-zh.md](references/adult-action-dictionary-zh.md)

## Source → H3 translation

After retrieval, translate source terminology using:

- [references/h3-motion-translation-en.md](references/h3-motion-translation-en.md)
- [references/h3-motion-translation-zh.md](references/h3-motion-translation-zh.md)

Create one normalized semantic plan:

```text
source theme / caption phrase
→ H3 mode
→ subject/reference roles
→ position and body geometry
→ active subject
→ active body part
→ motion direction
→ cadence
→ amplitude
→ complete movement cycle
→ receiving-body response
→ stabilizers / contact
→ expression / gaze
→ camera
→ setting / lighting
→ continuity
→ soundscape / music
```

Do not rely on vague tags such as `fast`, `intense`, or `rough` when the user is asking for visible motion. Resolve them into explicit movement mechanics.

## H3 mode selection

Choose the H3 mode before writing either output file.

Use Ref2VA when reference assets define reusable subjects, style, scene identity, or whole-video reference relationships.

Use I2VA first-frame semantics only when the supplied image is explicitly the target video's literal starting frame.

For identity-only reference pictures, define them as subjects rather than literal keyframes.

## Ref2VA structure

Both output files use this exact six-section order:

```text
subject_definitions:
summary:
retention_analysis:
detailed_description:
overall_soundscape:
non_diegetic_music:
```

For identity-only references:

```text
<Subject 1> is the fictional adult woman whose appearance comes from <Picture 1>.
<Subject 2> is the fictional adult man whose appearance comes from <Picture 2>.
```

Use `[reference generation]` when reference pictures define identity/style but are not literal target frames.

In the Chinese document, keep H3 field names, `<Subject N>`, `<Picture N>`, `<Video N>`, `[Shot N]`, timestamps, retention markers, and fixed protocol strings unchanged; translate only the descriptive prose.

## T2VA / I2VA / FL2VA / L2VA structure

For non-Ref2VA outputs, keep these field names exact in both files:

```text
integrated_multimodal_description:
overall_soundscape:
non_diegetic_music:
```

Any H3-required fixed protocol sentence remains exact even in `H3_Prompt_ZH-CN.md`.

## Single continuous shot rule

For one continuous action:

- prefer one `[Shot 1]`;
- do not split the timeline into artificial cuts;
- describe progression naturally in prose;
- keep playback at normal real-time 1×;
- interpret “faster” as higher physical-action frequency, not video fast-forward.

## Camera and face priority

When the user prioritizes the female lead's face:

- prefer frontal or frontal three-quarter medium-close framing;
- keep the face inside frame;
- keep head posture readable;
- use small-amplitude tracking instead of unnecessary cuts;
- preserve enough action geometry that the physical interaction remains understandable.

## Continuity

Preserve when requested:

- character identity;
- body proportions and anatomy;
- established position;
- supporting limbs;
- relative body orientation;
- clothing state;
- lighting and color temperature;
- camera scale;
- face visibility.

## Safety boundary

Read [references/source-and-safety.md](references/source-and-safety.md).

Never:

- sexualize a real person's identity or likeness;
- transform a real-person uploaded photo into explicit sexual content;
- use minors or ambiguous-age subjects;
- use age-regression or school-age sexual framing.

A real-person image may only contribute non-identifying technical information such as pose geometry, camera angle, lighting direction, or composition, then be re-applied to fictional adult characters.

## Pre-delivery check

Before returning the two documents, verify:

- all sexual subjects are fictional/synthetic adults;
- the same source theme(s) underpin both languages;
- both documents use the same H3 mode;
- subject/reference numbering matches;
- shot count, order, and timing match;
- action mechanics, cadence, amplitude, and body response match;
- camera instructions match;
- continuity constraints match;
- soundscape and music match;
- English H3 prose is complete;
- Chinese H3 prose is a full synchronized rendering, not a summary;
- the H3 field order and protocol tokens are preserved.
