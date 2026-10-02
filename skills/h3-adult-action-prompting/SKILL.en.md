# H3 Adult Action Prompting — English Guide

This guide complements the repository's main `SKILL.md`. It converts adult-action intent into MiniMax H3-ready continuous-motion language.

## Source-first workflow

Use three layers:

1. **Source language** — consult `prompting-guide.json` when available, or the normalized dictionaries when it is not.
2. **Semantic normalization** — identify position, active subject, action verb, direction, cadence, range, body response, camera, expression, setting, lighting, and continuity.
3. **H3 translation** — rewrite the source terminology into complete, temporally readable motion sentences and then place them in the correct H3 mode structure.

Do not treat the source JSON as H3 syntax. It is a terminology and phrasing reference derived from adult caption data.

## Ref2VA output contract

For full-reference prompts, use these six sections in this order:

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

Use `[reference generation]` in the summary when the pictures are identity/style references rather than literal target frames.

## Motion translation formula

Translate vague adult-action tags into:

```text
active subject
+ sexual position
+ active body part
+ motion direction
+ cadence
+ amplitude/range
+ complete cycle
+ receiving-body response
+ stabilizers / hand contact
+ expression / gaze
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

1. Look for exact or near-exact terms in the original prompting guide if available.
2. Check:
   - `references/adult-action-dictionary-en.md`
   - `references/h3-motion-translation-en.md`
3. Preserve niche terminology only when it helps identify the action or style.
4. Remove redundant community slang that does not improve H3 execution.
5. Translate the final result into H3 motion language.

## Safety boundary

This skill is only for explicitly adult fictional or synthetic characters.

Never:
- sexualize a real person's identity or likeness;
- turn a real person's uploaded image into explicit sexual content;
- use minors or ambiguous-age subjects;
- use age-regression or school-age sexual framing.

A real-person reference may only contribute non-identifying technical features such as pose geometry, camera angle, lighting direction, or composition, which must then be applied to fictional adult characters.
