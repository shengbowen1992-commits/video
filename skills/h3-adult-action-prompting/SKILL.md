---
name: h3-adult-action-prompting
description: Convert adult-action intent for explicitly adult fictional or synthetic characters into MiniMax H3 T2VA/I2VA/Ref2VA prompts. Use source-first retrieval from prompting-guide.json when available, then normalize pose, action, cadence, amplitude, body response, camera, expression, setting, lighting, and continuity into precise H3 motion language. Supports bilingual Chinese/English authoring and Picture 1 / Picture 2 identity references.
---

# H3 Adult Action Prompting

Use this skill for explicitly adult **fictional or synthetic** characters.

## Language guide

- For English instructions, read [SKILL.en.md](SKILL.en.md).
- 中文说明请读 [SKILL.zh-CN.md](SKILL.zh-CN.md).

## Source-first retrieval

This skill uses the original `prompting-guide.json` as a retrieval corpus **when that file is available**.

Read:
- [references/prompting-guide-source.md](references/prompting-guide-source.md)
- [references/prompting-guide-usage-en.md](references/prompting-guide-usage-en.md)
- [references/prompting-guide-usage-zh.md](references/prompting-guide-usage-zh.md)

Do not treat the original JSON as MiniMax H3 syntax. Use it to retrieve terminology, phrasing, niche vocabulary, camera/style cues, and prompt-construction patterns.

If the full JSON is not present in this skill directory, fall back to:
- [references/adult-action-dictionary-en.md](references/adult-action-dictionary-en.md)
- [references/adult-action-dictionary-zh.md](references/adult-action-dictionary-zh.md)

## H3 translation layer

After retrieval, translate source terminology using:
- [references/h3-motion-translation-en.md](references/h3-motion-translation-en.md)
- [references/h3-motion-translation-zh.md](references/h3-motion-translation-zh.md)

Core transformation:

```text
source term / caption phrase
→ position and body geometry
→ active subject
→ active body part
→ motion direction
→ cadence
→ amplitude
→ complete movement cycle
→ receiving-body response
→ stabilizers / hand contact
→ expression / gaze
→ camera
→ continuity
→ H3 mode structure
```

Do not rely on vague tags such as `fast sex`, `intense`, or `rough` when the user is asking for actual visible motion. Resolve them into explicit movement mechanics.

## Ref2VA structure

For full-reference output, preserve this six-section order:

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

Only use first-frame I2VA wording when the user explicitly says that the supplied picture is the target video's actual starting frame.

## Single continuous shot rule

For one continuous action:
- prefer one `[Shot 1]`;
- do not split the timeline into artificial cuts;
- describe progression naturally in prose;
- keep playback at normal real-time 1×;
- interpret "faster" as higher physical-action frequency, not video fast-forward.

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
- established sexual position;
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

Verify:
- all sexual subjects are fictional/synthetic adults;
- picture roles are correct;
- source terminology was used only as reference language;
- active subject is explicit;
- position is explicit;
- direction is explicit;
- cadence and amplitude are explicit when requested;
- thrusting uses a complete cycle rather than vibration-only wording;
- receiving-body response is synchronized;
- support points are stable;
- camera framing matches the user's request;
- continuity constraints are present;
- H3 section order and timing are valid.
