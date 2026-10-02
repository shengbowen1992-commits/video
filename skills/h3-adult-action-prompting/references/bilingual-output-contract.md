# Mandatory Bilingual H3 Output Contract

Every successful execution of this skill must produce **two separate, synchronized H3 documents**:

```text
H3_Prompt_EN.md
H3_Prompt_ZH-CN.md
```

The two files are not independently authored variants. They are two renderings of **one shared semantic plan**.

## Generation order

1. Retrieve the closest source theme(s) from:
   - `prompting-guide.json` — authoritative English source terminology.
   - `prompting-guide-Chinese.json` — Chinese companion corpus for Chinese lookup and review.
2. Normalize the requested scene into one internal plan:
   - H3 mode;
   - subjects and reference roles;
   - position / body geometry;
   - active subject and active body part;
   - motion direction;
   - cadence;
   - amplitude;
   - complete movement cycle;
   - receiving-body response;
   - stabilizers / contact points;
   - expression / gaze;
   - camera;
   - setting / lighting;
   - continuity;
   - soundscape / music.
3. Render the English H3 document first.
4. Render the Chinese H3 document from the **same plan**.
5. Run a parity check before delivery.

Do not retrieve one theme for English and a different theme for Chinese unless the user explicitly requests different content.

## What must stay identical in both files

Keep these synchronized:

- H3 mode;
- subject numbering;
- reference numbering;
- shot count;
- shot order;
- timestamps;
- camera placement and movement;
- action cadence and amplitude;
- continuity constraints;
- sound events;
- music choice;
- reference retention level.

Preserve protocol tokens exactly in both files:

```text
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

Do not translate protocol tokens, reference labels, shot labels, or timestamps.

## Ref2VA section contract

Both files must use this exact six-section order:

```text
subject_definitions:
summary:
retention_analysis:
detailed_description:
overall_soundscape:
non_diegetic_music:
```

The Chinese file keeps these section names in English and translates the prose inside them into Chinese.

## T2VA / I2VA / FL2VA / L2VA section contract

For non-Ref2VA modes, keep the H3 field names unchanged in both files:

```text
integrated_multimodal_description:
overall_soundscape:
non_diegetic_music:
```

If a mode requires a fixed protocol sentence, keep that sentence exactly as required by H3 even in the Chinese document.

## Chinese document rule

`H3_Prompt_ZH-CN.md` is a full H3-formatted companion document, not a summary.

Translate the descriptive prose into natural Chinese while preserving:

- H3 field names;
- subject/reference tags;
- shot/timestamp notation;
- fixed protocol phrases;
- camera command names when exact H3 wording matters;
- dialogue, lyrics, and visible text in their requested/original language.

## File-delivery rule

When the environment supports file creation, create and return both Markdown files.

If file creation is unavailable, return two complete, clearly separated document blocks with the same filenames as headings.

Never return only one language by default. Suppress one file only if the user explicitly asks for a single-language deliverable.

## Parity check

Before delivery, verify:

- both files use the same H3 mode;
- both files contain the same subjects and references;
- both files have the same shot count and timing;
- action mechanics match exactly;
- camera instructions match exactly;
- continuity constraints match exactly;
- soundscape and music match exactly;
- neither file introduces content absent from the other.
