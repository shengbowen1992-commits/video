# Source, Intended Use, and Boundaries

## Source

The action vocabulary in this skill was normalized from the user's supplied `prompting-guide(1).json`, a large community-caption prompting guide associated with adult image/video generation language.

The source repeatedly uses:
- direct sexual-act terminology;
- explicit position names;
- action verbs such as `penetrating`, `thrusting`, `pounding`, `straddling`, `riding`, `grinding`, `bouncing`;
- body-response language such as `rocking`, `jiggling`, `bouncing`, `arched back`;
- camera terms such as `close-up`, `POV`, `low angle`, `rear view`, `from behind`.

This skill does **not** treat the source JSON as MiniMax H3's official syntax. It uses that vocabulary as a lexical source, then rewrites it into H3-style continuous video descriptions.

## H3 Adaptation Principle

Caption/tag language:

```text
doggy style, pounding, close-up, from behind
```

is expanded into motion-language:

```text
The active subject performs continuous forward-and-back pelvic thrusts
at a fast, steady cadence with a pronounced range of motion.
The receiving subject's hips, waist, shoulders, and upper torso
rock in synchronization with each repeated movement.
```

The key transformation is:

```text
sexual-act label
→ body geometry
→ direction
→ cadence
→ amplitude
→ complete cycle
→ body response
→ camera
→ continuity
```

## Reference Images

A picture used only to define a fictional/synthetic character's appearance is an identity reference, not automatically a keyframe.

Example:

```text
<Subject 1> is the fictional adult woman whose appearance comes from <Picture 1>.
<Subject 2> is the fictional adult man whose appearance comes from <Picture 2>.
```

Use standalone `<Picture N>` keyframe semantics only when the image actually anchors a target frame.

## Safety Boundary

This skill is for explicitly adult fictional or synthetic characters.

Do not:
- sexualize a real person's identity or likeness;
- transform a real person's uploaded image into explicit sexual content;
- use minors or ambiguous-age subjects;
- use age-regression or school-age sexual framing.

A real-person image may still be abstracted for non-identifying technical information such as pose geometry, camera angle, lighting direction, or general composition, then applied to fictional adult characters.
