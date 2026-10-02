---
name: h3-adult-action-prompting
description: Write MiniMax H3 adult-action video prompts for explicitly adult fictional or synthetic characters. Use when the request involves sexual positions, penetration motion, thrusting/riding/grinding/bouncing, motion frequency or amplitude, body-response synchronization, face-priority camera framing, or converting adult motion language into H3 T2VA/I2VA/Ref2VA structure. Supports Picture 1 / Picture 2 identity references, bilingual CN/EN prompt drafting, and precise motion-cycle wording instead of vague intensity tags.
---

# H3 Adult Action Prompting

Write technically explicit MiniMax H3 prompts for **fictional or synthetic adult characters only**. Convert adult-action intent into concrete body geometry, motion direction, frequency, amplitude, body response, camera framing, and continuity constraints.

Read:
- [references/adult-action-dictionary-en.md](references/adult-action-dictionary-en.md) for H3-ready English action vocabulary.
- [references/adult-action-dictionary-zh.md](references/adult-action-dictionary-zh.md) when the user writes in Chinese or asks for Chinese output.
- [references/source-and-safety.md](references/source-and-safety.md) for provenance, reference-image handling, and hard boundaries.

## Hard Boundary

- Sexual content must involve explicitly adult fictional or synthetic characters.
- Do not write explicit sexual prompts that preserve, imitate, or bind the identity or likeness of a real person.
- If a supplied image is a real person, do not turn that person's identity into explicit sexual content. Offer a fictional/synthetic adult character with the same non-identifying pose, camera geometry, lighting, or composition instead.
- Never use minors, ambiguous-age subjects, school-age framing, or age-regression/age-play cues.
- Do not infer consent from an image. For explicit adult scenes, write consensual adult participation unless the user explicitly requests a fictional dark-literary scenario that remains within allowed boundaries.

## Primary Goal

Do not rely on vague tags such as:

```text
fast sex
intense
passionate
hardcore
rough
```

Translate them into executable motion:

```text
active subject
+ sexual position
+ active body part
+ motion direction
+ cadence/frequency
+ range/amplitude
+ complete movement cycle
+ receiving subject's synchronized body response
+ contact/hand placement
+ expression/gaze
+ camera
+ continuity
```

Canonical motion sentence:

```text
<Subject 2> performs continuous forward-and-back pelvic thrusts
at a fast, steady cadence with a pronounced range of motion.
His hips visibly withdraw before each forward drive, creating
a complete repeated movement cycle.

<Subject 1>'s hips, waist, shoulders, and upper torso rock
forward and backward in synchronization with each thrust.
```

Fast physical action means **higher action frequency at normal real-time playback**, not time-lapse, fast-forward, or accelerated video playback.

## Reference-Image Routing

When pictures only define character identity:

```text
<Picture 1> = female fictional/synthetic adult identity reference
<Picture 2> = male fictional/synthetic adult identity reference
```

Define reusable subjects:

```text
<Subject 1> is the fictional adult woman whose appearance comes from <Picture 1>.
<Subject 2> is the fictional adult man whose appearance comes from <Picture 2>.
```

Use the subjects throughout the target-video description. Do **not** treat identity-only pictures as first-frame anchors.

For full-reference / Ref2VA output, use these six sections in this exact order:

```text
subject_definitions:
summary:
retention_analysis:
detailed_description:
overall_soundscape:
non_diegetic_music:
```

Use `[reference generation]` when pictures provide identity/style/action guidance but are not literal target frames.

If the user explicitly says a picture is the literal first frame, switch to I2VA framing and use the official first-frame alignment sentence:

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.
```

Do not use that sentence for identity-only references.

## Motion Construction Contract

For every explicit motion request, resolve these dimensions:

1. **Position**
   - rear-entry / doggy style
   - low kneeling rear-entry
   - bent-over rear-entry
   - missionary
   - cowgirl
   - reverse cowgirl
   - seated straddle
   - prone
   - side-lying
   - standing

2. **Active subject**
   - State who drives the motion.
   - For riding positions, the upper subject usually drives the movement unless the user says otherwise.
   - For rear-entry positions, do not leave the driver ambiguous.

3. **Active body part**
   - pelvis / hips
   - torso
   - legs
   - head / mouth for oral motion

4. **Direction**
   - forward-and-back
   - up-and-down
   - circular / elliptical grinding
   - rocking

5. **Frequency**
   - slow
   - moderate
   - fast / rapid
   - steady rhythmic cadence
   - gradually increasing frequency

6. **Amplitude**
   - short-range
   - moderate
   - pronounced / large-range
   - deep

7. **Movement cycle**
   For thrusting, prefer:
   ```text
   a clear backward reset followed by each forward drive
   ```
   This reduces "vibration-only" motion.

8. **Receiving-body response**
   Describe at least 2 linked regions when strong movement is requested:
   - hips / waist
   - shoulders / upper torso
   - breasts / soft-tissue inertia
   - head / hair secondary motion
   - weight shift

9. **Stabilizers**
   State the body parts that remain fixed:
   - hands remain planted
   - supporting knee remains planted
   - raised leg remains elevated
   - hand remains on hip/thigh/lower back

10. **Camera**
    Use H3 camera language naturally:
    - medium close shot
    - low-angle shot
    - frontal three-quarter angle
    - rear-view shot
    - POV
    - tracking shot
    - static shot
    - push in with small amplitude at slow speed
    - arc shot

11. **Continuity**
    Explicitly preserve:
    - position
    - character identity
    - anatomy/body proportions
    - spatial relation
    - established clothing state
    - lighting/exposure
    - face visibility when requested

## Face-Priority Camera Contract

When the user says "看女主正脸", "跟随女主的脸", "睁眼看镜头", or equivalent:

- Prefer frontal or frontal three-quarter views.
- Use medium-close framing unless the user requests otherwise.
- Keep the face inside frame throughout motion.
- Write head posture explicitly if the pose would naturally hide the face.
- Use small-amplitude tracking instead of frequent cuts.
- Do not make the sexual action unreadable merely to obtain a face close-up.

Reusable wording:

```text
The camera maintains a frontal three-quarter medium close shot,
tracking with small amplitude while keeping <Subject 1>'s face
clearly visible. Her head remains lifted enough to stay within
the frame, and she occasionally directs her gaze toward the camera.
```

## Body-Response Contract

When the request asks for 大幅度 / 高频 / 激烈 / 更猛 / 动作明显:

Do not write only "intense" or "vigorous." Describe visible propagation:

```text
<Subject 1>'s hips and waist respond first,
followed by rhythmic motion through her shoulders and upper torso.
Her hair and soft tissue show natural secondary inertia,
while her supporting arms remain stable.
```

Avoid contradictory instructions such as:
- "very fast" + "almost no movement"
- "large-range" + "keep every body part fixed"
- "face close-up" + "show full-body action" without a camera strategy

## Position-Preservation Contract

When a specific pose matters, restate its anchors once or twice, not every sentence.

Example:

```text
<Subject 1> remains on both knees with her upper torso lowered,
hips raised, and one leg bent and elevated to the side.
The supporting knee and both hands remain planted throughout.
```

Then add:

```text
The raised leg does not drop, both subjects do not switch position,
and their relative orientation remains unchanged.
```

## Shot Timing

H3 target duration is normally 4–15 seconds.

For a single continuous action shot:
- Prefer one `[Shot 1]`.
- Do not split 0–3 / 3–10 / 10–15 into artificial shots unless there is an actual cut.
- Describe temporal progression in natural prose: begins immediately → stabilizes → intensifies or changes framing → ends while maintaining continuity.

For actual cuts:
```text
[Shot 2] At 00:05.000, the camera cuts to...
```

## Sound

`overall_soundscape` should summarize:
- room ambience
- mattress/fabric/footstep/contact sounds
- breathing
- non-verbal adult vocal reactions

Do not repeat dialogue there.

Use:

```text
non_diegetic_music: N/A
```

unless background music is explicitly requested.

## Output Language

H3 execution prompts should be written in English by default.

If the user asks for Chinese:
- provide a Chinese prompt or explanation;
- preserve H3 field names when the user wants strict official formatting;
- if both are requested, give English execution prompt first and Chinese counterpart second.

## Minimal Input

Accept short requests such as:

```text
Picture 1 = female lead
Picture 2 = male lead
15s
low kneeling rear-entry
male drives motion
fast + large range
female face visible
front 45-degree medium close shot
```

Do not ask for details that can be safely expressed as technical defaults. Do not invent new sexual acts, partners, plot events, costumes, or locations that the user did not request.

## Pre-Delivery Check

Before returning a prompt, verify:

- [ ] all sexual subjects are fictional/synthetic adults;
- [ ] no real-person identity is sexualized;
- [ ] picture roles are correct;
- [ ] position is explicit;
- [ ] active subject is explicit;
- [ ] direction is explicit;
- [ ] frequency is explicit if requested;
- [ ] amplitude is explicit if requested;
- [ ] complete movement cycle is described for thrusting;
- [ ] receiving-body response is synchronized;
- [ ] support limbs/pose anchors are preserved;
- [ ] face framing matches the request;
- [ ] camera move is simple and readable;
- [ ] no accidental wide shot if medium-close was requested;
- [ ] continuity and anatomy are protected;
- [ ] total timeline fits the requested duration;
- [ ] sound/music fields match the request.
