# Adult Explicit Action Continuity

This reference is a specialized continuity and artifact-prevention layer for **explicit sexual scenes involving fictional adults**. It extends the parent skill's Ref2VA six-section format, Picture 3 tail-lineart rules, mutable-state ledger, V18 real-time motion contract, shot-specific expression rules, and layered sound standard.

Use it only when the requested scene is explicitly sexual. Do not inject its sexual vocabulary into nonsexual, merely suggestive, or format-only tasks. All depicted characters must be adults.

This module supports both constrained choreography and broad delegated authoring. When the user explicitly grants broad creative control over a fictional-adult sexual scene, it may invent and sequence additional sexual acts, position changes, wardrobe transitions, intensity escalation, climax events, ejaculation/fluid outcomes, vocal reactions, and aftermath beats within that delegated scope. Keep the established cast and relationship mapping unless cast changes are also delegated, honor explicit exclusions, and preserve anatomical/temporal continuity. For narrowly specified requests, stay within the user's stated action set.

For reusable position geometry, support-point definitions, high-impact cyclic motion fragments, female visual-anchor camera patterns, and Picture 3 phase handoff language, read [adult-position-motion-library.md](adult-position-motion-library.md). Treat that file as a selective library: load only the active action/position template and adapt it to the inherited scene.

## 1. Rule Priority

For an adult explicit tailchain, resolve instructions in this order:

1. user-requested adult action and relationship dynamics;
2. permanent identity references for who each subject is;
3. actual accepted previous tail / Picture 3 for opening geometry and visible action phase;
4. text-carried mutable state for clothing, nudity, footwear, props, and other non-geometric state;
5. this adult-action module for anatomy/contact continuity;
6. the matching template from the adult position/motion library for support geometry, action path, and reusable choreography language;
7. V18 for real 1× movement frequency, amplitude, and impact-cycle behavior when intensity is requested;
8. shot-specific expression and sound rules.

Never use this module to override the user's requested action with a different sexual act.

## 2. Adult Body Ownership and Genital Attachment

Explicit sexual scenes are especially prone to detached, duplicated, swapped, or floating anatomy. Prevent that in the actual execution Shot text when the risk is relevant.

- A penis remains continuously attached to the owning subject's pelvis/groin with stable orientation relative to that pelvis.
- Vulva/vaginal anatomy remains part of the owning subject's pelvis; breasts remain attached to the owning chest; hands, arms, legs, and feet remain attached to their correct bodies.
- Never describe attached anatomy as a separate prop that can be carried, presented, held away from the body, floated, swapped, or independently repositioned.
- Do not duplicate genitals or create a second incompatible anatomical path because a camera angle changes.
- A cut or Picture 3 reference never changes anatomical ownership.
- When several bodies overlap, explicitly anchor ambiguous hands/limbs to their owner: e.g. “<Subject 2>'s right hand remains on <Subject 1>'s left hip.”
- If a hand is not needed for the action, place it on a stable landmark such as thigh, hip, waist, abdomen, shoulder, jaw, mattress, or bedding instead of adding ambiguous genital handling.

When artifact risk is high, use concise explicit continuity language in the Shot:

```text
Anatomical continuity remains stable: the visible genital anatomy stays
continuously attached to the correct subject's pelvis with no detached,
duplicated, floating, swapped, or independently handheld anatomy.
```

Do not repeat this block in every Shot when one scoped statement before the affected shots is sufficient.

## 3. Nudity and Wardrobe Prerequisites

Sexual actions often depend on clothing already being moved or removed. Track this explicitly for **every participant**, not only the camera-priority subject.

Before a sexual action begins:

- identify which garment layers actually obstruct the requested contact;
- schedule each necessary clothing transition before the dependent action;
- complete each one-time removal only once;
- carry the resulting nude/partially nude state forward;
- never restore a removed garment from Picture 1/2 merely because a new segment starts.

For **every adult segment**, the parent skill's `Continuity State Lock:` must enumerate the current clothing/nudity state of every participant, not only the visual lead. If a garment is mid-removal, include the exact remaining attachment points and fabric location (for example, one sleeve still on the forearm while the other shoulder is bare). Keep that partial state through subsequent cuts/segments until the same continuous removal changes it. Do not repeatedly start “taking off the shirt/trousers” from the fully worn state.

Avoid late conditional wording such as:

```text
If his trousers are still on, remove them now.
```

Prefer a planned prior transition and a definite inherited state:

```text
Opening State: both subjects remain in the clothing/nudity state established
at the preceding accepted end state. The required garment removal is already
complete; the removed garment does not return.
```

If the actual accepted tail contradicts the planned state, fix the chain before the dependent sexual action instead of hiding the mismatch in text.

### Terminal nude-state vocabulary isolation

Once a participant reaches a stable fully nude state and no re-dressing is requested, later segments should serialize the **positive current body state only**. Do not keep reintroducing the names, colors, or materials of garments that are no longer worn.

- In later `Wardrobe/Body State:` text, prefer concise current-state wording such as `both subjects are fully nude and remain fully nude throughout this segment` rather than listing every previously removed garment.
- Do not repeat absent garment names inside `Color/Material State:`, `retention_analysis:`, initial-outfit recaps, negative instructions, conditional branches, or clauses such as `whenever still present`. Mentioning an absent garment can reactivate the clothing concept even when the sentence says not to restore it.
- `Color/Material State:` should describe only currently present subject appearance, visible scene materials, lighting-relevant surfaces, and props that still exist in the active scene.
- If a removed garment is still physically visible in the scene, track it as a separate prop with its current location and appearance. If it is not visible and no later action uses it, omit it completely from subsequent prompts.
- Permanent identity references control identity, hair identity, and body proportions; after the nude state is established they must not be allowed to re-authorize the reference image's original clothing.
- `retention_analysis:` must not say that clothing state may continue to evolve when the intended terminal nude state is locked. State that the current nude body state remains unchanged unless the user explicitly requests a later wardrobe transition.

This rule is a specialization of the parent skill's semantic quarantine: preserve the current visible state, not the vocabulary of a completed clothing history.

## 4. Oral Sex Continuity

For oral sex already requested by the user:

- keep the recipient's genital anatomy continuously attached to the correct pelvis;
- describe the giver's mouth/head/neck path relative to that attached anatomy, not as manipulation of a detached object;
- keep hand support on stable body landmarks unless manual genital stimulation is itself requested;
- if manual assistance is requested, describe the hand as contacting anatomy **while that anatomy remains visibly attached to the pelvis**;
- maintain one coherent mouth-to-body geometry across cuts;
- when the mouth disengages, state the release and next contact explicitly rather than teleporting between mouth positions;
- if the face must remain visible, choose a side-front or three-quarter camera that shows the giver's face without changing the anatomical path.

Avoid artifact-prone wording that makes anatomy sound independent:

- avoid “she holds the penis up in her hand” unless the visual can still clearly preserve continuous pelvic attachment;
- avoid “she carries/moves it toward her mouth”;
- avoid unspecified “grips the base” when the model is already producing detached anatomy.

Prefer:

```text
The penis remains continuously attached to <Subject 2>'s pelvis.
<Subject 1> lowers her mouth along the established body line while her hands
brace on his thighs/hips. Her head and neck provide the main movement.
```

If hand stimulation is explicitly part of the requested scene, use:

```text
Her hand moves along the attached shaft while its base remains continuously
connected to <Subject 2>'s pelvis; the hand follows the same anatomical axis
rather than moving the genital anatomy independently.
```

## 5. Manual Genital Stimulation

When manual genital stimulation is explicitly requested:

- identify the owner of the anatomy and the owner of the hand;
- maintain continuous attachment of the anatomy to the pelvis;
- describe hand travel along the existing anatomical axis;
- do not let the hand become a second independent source of genital motion that changes ownership or attachment;
- keep the other hand on a stable landmark if it is not part of the requested action;
- maintain plausible wrist, elbow, and shoulder connection to the hand doing the action.

For close framing, preserve enough of the pelvis/torso or body context to make attachment legible when detached-anatomy artifacts have been a problem.

## 6. Penetrative Intercourse Continuity

For penetrative vaginal or anal intercourse already requested by the user:

- establish the two pelvises and their orientation before penetration;
- keep the penetrating anatomy attached to the penetrating subject's pelvis;
- keep the receiving anatomy attached to the receiving subject's pelvis;
- describe entry, withdrawal, and repeated motion along one coherent anatomical axis;
- large-amplitude or high-cadence movement changes **travel and frequency**, not anatomical ownership or insertion direction;
- do not allow the penis to emerge from the wrong body region, duplicate, bend through impossible paths, or remain visually disconnected from the penetrating pelvis;
- do not let a camera cut silently reverse which subject is penetrating or receiving;
- when penetration ends, describe visible withdrawal/release before a new unrelated action begins.

For sustained cyclic intercourse across a segment seam, Picture 3 carries the visible phase. Continue from that phase instead of resetting to “about to enter” or replaying initial penetration.

When V18 is active, preserve normal 1× playback and express intensity through actual hip/pelvic travel, cadence, weight transfer, body compression/rebound, and supporting limbs. Do not use fast-forward or speed-ramp language.

For recurring penetrative positions, select the matching reusable template in [adult-position-motion-library.md](adult-position-motion-library.md) rather than rewriting support geometry from scratch. The library currently covers supine face-to-face, raised-leg supine, edge-of-bed, kneeling rear entry, prone rear entry, woman-on-top, reverse woman-on-top, seated face-to-face, side-lying, standing rear entry, and standing wall-supported variants.

## 7. Sexual Position Transitions

A position change is a one-time transition and must obey the same anti-replay/state-machine rules as clothing changes.

Before writing a transition, decide:

- current support points: hands, knees, feet, back, shoulders;
- current pelvis orientation;
- whether genital contact/penetration remains engaged, is intentionally released, or is re-established;
- which subject initiates the weight shift;
- the continuous path into the new position;
- final support points and camera axis.

Do not teleport from one sexual position to another at a cut.

Use one of three explicit continuity models:

### A. Contact preserved

The bodies rotate/reposition while the existing intimate contact stays continuously engaged. Describe the weight shift and pelvis path.

### B. Contact released then re-established

State the release/withdrawal first, perform the body transition, then explicitly re-establish the requested contact. Do not imply impossible continuous penetration through a geometry change that cannot plausibly preserve it.

### C. Non-penetrative transition

For kissing, breast stimulation, oral sex, or manual stimulation, carry the exact current contact point forward or explicitly release it before changing target.

The next segment must inherit the **resulting** position, not replay the whole transition.

## 8. Explicit Camera Priority

When the user designates one adult performer as the visual anchor:

- organize cuts, tracking, orbiting, over-shoulder angles, and height changes around that performer;
- preserve enough body context to keep the sexual action anatomically readable;
- front or three-quarter facial visibility may be prioritized without forcing continuous eye contact;
- a brief look toward camera lasts only a moment and never pauses oral/manual/penetrative movement;
- do not cut away to isolated genital close-ups so aggressively that identity/body ownership becomes ambiguous unless the user explicitly asks for that framing.

When anatomy artifacts are recurring, slightly wider body-context shots are preferable to extreme crops that remove the pelvis/torso attachment context.

## 9. Natural Pleasure Expressions

When visible pleasure, arousal, intensity, or climax expression is requested or included in an authorized broad choreography, do not use one fixed “pleasure face” in every Shot.

Tie expression to the current physical trigger and vary it naturally:

- eyelids may close, half-close, or briefly reopen;
- brow may tighten slightly during stronger stimulation, then soften;
- jaw may loosen; lips may part on exhale;
- the head may tilt or briefly tip back when consistent with the body position;
- fingers may tighten on a partner, bedding, or support surface;
- shoulders/abdomen/pelvis may tense and release with the action;
- gaze may return to the partner, task, or camera when requested.

Avoid constant smiling, permanently open eyes, permanently closed eyes, or a frozen exaggerated climax face.

A camera glance is an overlay on the ongoing action, not a new action. The mouth/head/hips/hands continue the requested sexual movement during the brief glance.

## 10. Adult Vocal Reactions

This module extends [h3-sound-prompt-standard.md](h3-sound-prompt-standard.md).

When moans, gasps, whimpers, breathy vocalizations, muffled reactions, or climax vocalizations are requested or included in an authorized broad choreography:

- every affected Shot gets its own trigger-specific vocal behavior;
- vary texture, pitch, duration, intensity, and spacing;
- do not map one vocalization to every thrust/stroke/movement;
- maintain natural silent gaps and breath-only moments;
- keep mouth state compatible with the action: a kiss or oral action may muffle a vocalization; an open mouth after release can make it clearer;
- stronger physical cadence may make reactions somewhat more frequent or fuller without turning them into a metronome;
- do not add spoken dialogue unless requested.

Useful adult non-dialogue textures include:

- low breathy moan;
- short open moan;
- muffled moan during mouth contact;
- sharp gasp at a stronger transition;
- broken breath with intermittent voiced sound;
- longer uncontrolled moan near a requested climax.

These are options, not a mandatory sequence.

## 11. Climax Continuity

Apply climax rules when climax is explicitly requested, already part of the source scene, or intentionally introduced under the user's broad creative delegation.

Build it as a progression, not an abrupt label:

### Build-up

- breathing becomes less regular;
- grip/support tension increases;
- expression becomes less controlled;
- vocal reactions may become fuller or closer together;
- the existing sexual movement continues at the requested real 1× cadence.

### Peak

- visible whole-body tension or a stronger localized muscular response;
- brief disruption of breathing;
- stronger but non-mechanical vocalization if requested;
- eyes may close or lose precise focus;
- hands/legs/support points tighten consistently with the pose.

### Release / immediate aftermath

- movement may naturally reduce only because the requested action reaches its end, not because playback slows;
- breathing remains elevated;
- grip and facial tension gradually soften;
- preserve the final body/contact state clearly enough for the next tail if the chain continues.

Under broad creative delegation, ejaculation, fluid outcomes, individual or simultaneous climax, and their timing may be intentionally designed as story beats. Keep the outcome anatomically owned by the correct subject, make its timing and visible consequences continuous, and do not include any outcome the user explicitly excluded. Under a narrow request, do not add these outcomes unless they are part of the requested action.

## 12. Picture 3 Tailchain Handoff for Adult Actions

For segment 2 onward in the default lineart profile:

- Picture 3 controls opening pose, pelvis orientation, limb placement, contact points, camera axis, and the visible phase of the current sexual action.
- Text carries nudity/garment state and any other non-geometric mutable state.
- The segment's `Continuity State Lock:` also repeats the established color/material palette and lighting/exposure state because the lineart cannot preserve those attributes.
- For cyclic oral/manual/penetrative motion, continue from the inherited phase instead of restarting the action.
- For one-time position changes, the previous segment owns the completed transition; the next segment begins from the resulting position.
- Never write “begins penetration” again if penetration is already visibly underway in Picture 3.
- Never re-remove clothing that the state ledger already marks absent.
- If the actual accepted tail shows an anatomy/contact error, do not propagate it into the next segment merely because a lineart was generated; regenerate or correct within the authorized workflow.

## 13. Artifact-Prone Wording to Review

Review adult prompts for wording that can accidentally create disconnected anatomy or repeated state transitions.

Potentially risky when context is ambiguous:

- “holds it up”;
- “carries it toward”;
- “grips the base” without visible pelvic attachment;
- “the penis moves” without a subject/pelvis anchor;
- “she is suddenly on top”;
- “he is now behind her” without a transition path;
- “if the clothes are still on...”;
- repeating “removes” in multiple segments after the garment is already absent;
- “starts penetration” in every continuation segment.

Replace with explicit ownership, attachment, state, and continuous body paths.

## 14. Pre-Delivery Adult Explicit Review

When this module is active, verify in addition to the parent skill's checklist:

1. every visible sexual body part has one stable owner;
2. genital anatomy remains continuously attached to the correct pelvis;
3. no detached, duplicated, floating, swapped, or independently handheld genital anatomy is requested;
4. required nudity/garment changes are completed before the dependent sexual action and do not replay later;
5. oral action uses one coherent mouth/head/body path and stable anatomical attachment;
6. manual stimulation follows attached anatomy rather than moving it as a prop;
7. penetrative motion follows one coherent pelvis-to-pelvis axis with stable penetrator/receiver roles;
8. sexual position transitions use a continuous weight/support path and explicitly preserve, release, or re-establish contact;
9. cyclic sexual actions inherit the current phase across Picture 3 seams instead of restarting;
10. the requested visual-anchor subject remains the camera priority without losing anatomical context;
11. requested pleasure expressions vary by trigger and do not become a fixed face;
12. requested moans/gasps are written inside affected Shots with natural irregular spacing;
13. requested climax is built through visible/vocal progression rather than appearing abruptly;
14. every invented sexual act, climax, fluid outcome, wardrobe transition, or escalation remains inside the user's delegated adult scope and respects explicit exclusions; no undelegated cast or relationship change was introduced.

These checks are semantic authoring checks. The static JSON/prompt validators cannot prove them; rendered QC remains necessary for actual anatomy and continuity.
