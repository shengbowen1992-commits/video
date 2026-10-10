---
name: h3-tailchain-continuity
description: Write and revise MiniMax H3 Ref2VA prompts and dynamic multi-segment story_segments.json files from durations, references, and a scene description, with legacy sequence.json compatibility. Use for V18 motion-intensity requests (大幅度, 激情, 激烈, 高频, 更猛), six-section prompt formatting, reference retention, global constraints, two-layer sound design, audiovisual shot timing, and Ref2VA/I2V continuity. Defaults to Plan 5 tail-lineart continuation with permanent female Picture 1 and male Picture 2, plus the preceding segment's final-frame lineart as Picture 3 from segment 2 onward; retain clear faces and reproducible per-clip seeds when quality consistency is requested.
---

# H3 Tailchain Continuity Prompt Writer

Write technically executable prompts for H3 segment chains and package them as `story_segments.json` by default. Retain `sequence.json` for an explicitly requested legacy controller or Ref2VA/I2VA dual-prompt package. Do not require the user to choose LoRA, native sampling, a launcher, model settings, reference-image paths, seeds, or sampling parameters. This skill may record deterministic seeds when quality consistency is requested, but it does not bind them to a renderer. It controls continuity language and JSON packaging only; the user controls the scene and any explicitly supplied people, plot, actions, styling, dialogue, or camera intent.

## V18 Motion Intensity Routing

When a video action request includes 大幅度, 激情, 激烈, 高频, 动作快一点, 更猛, 更有力, or equivalent physical-performance intent, read [references/v18-motion-intensity.md](references/v18-motion-intensity.md) and apply its V18 Motion Intensity Contract automatically. Interpret meaning, scope, negation, and explicit overrides; do not require the user to name V18. Keep playback at normal real-time 1× while translating the requested intensity into actual movement frequency, amplitude, and the established physical path.

Place the contract once in each affected execution prompt, not once per Shot or only in an outer JSON field. Adapt anatomical/path language to the existing action. For requested cyclic motion, preserve cycle phase at seams: the anti-replay and low-velocity handoff defaults below must not suppress natural return strokes or sustained high cadence. Follow the reference for exact placement, intensity levels, and review checks.

## H3 Sound Authoring Standard

Before authoring or revising H3 execution prompts, read [references/h3-sound-prompt-standard.md](references/h3-sound-prompt-standard.md) and apply its two-layer sound structure by default. Put overall sound style, continuous ambience and natural variation in `overall_soundscape`; put identified vocal reactions, action-triggered sounds, dynamics, pauses and cross-cut timing in the corresponding Shot. Audience-only music stays in `non_diegetic_music` and remains `N/A` when not requested.

Use the selected mode's existing fields and actual audio bindings. Preserve exact dialogue, silence requests and format-only source text; templates do not authorize new voices, music or reference inputs. Apply the standard inside each complete execution prompt, not only in an unused outer `global_prompt`. With V18, sustain the requested physical cadence while allowing natural vocal spacing rather than one vocal response per movement. Prompt validation does not replace listening to rendered audio.

If spoken or nonverbal vocal reactions are explicitly requested, every affected Shot must contain its relevant trigger-specific reaction; `overall_soundscape` alone is insufficient. Apply the source, trigger, texture, dynamics, spacing, and visible-response guidance in the sound reference without adding unrequested sounds. A request for a silent gesture alone does not activate this vocal requirement.

## Adult Explicit Action Continuity Routing

When the user's scene explicitly involves **fictional adult characters** performing explicit sexual actions, read [references/adult-action-continuity.md](references/adult-action-continuity.md) and apply it in addition to the general Ref2VA, tail-lineart, V18, state-ledger, expression, and sound rules.

Activate this module only for explicit adult sexual content such as oral sex, genital/manual stimulation, penetrative intercourse, explicit sexual position transitions, nudity prerequisites for those actions, or climax continuity. Do not load or inject its sexual vocabulary into nonsexual scenes, suggestive-but-nonexplicit scenes, or format-only transformations that must preserve source wording.

The adult module is a **specialized continuity, choreography, and artifact-prevention layer**. When the user explicitly delegates broad creative control over a fictional-adult sexual scene, the author may freely design additional sexual acts, position changes, wardrobe transitions, intensity escalation, climax events, ejaculation/fluid outcomes, and audiovisual progression within that delegated scope. Keep the established cast and relationship mapping unless the user also delegates cast changes, and honor any explicit exclusions. When the user gives a narrow action list instead of broad creative authority, preserve that narrower scope. All depicted characters must be adults.

When an explicit adult scene includes penetrative intercourse, oral/manual genital action, explicit position changes, broad delegated adult choreography, or a request for stronger/rougher/higher-cadence/larger-amplitude sexual motion, also read [references/adult-position-motion-library.md](references/adult-position-motion-library.md). Select only the position/action template that matches the current Shot; use it as reusable geometry and motion language, not as permission to paste unrelated acts into every segment. Combine its high-impact templates with V18 when intensity is requested, and preserve Picture 3's inherited cycle phase at seams.

The position library is an extensible reference, not a whitelist. Under broad adult creative delegation, the author may design a new physically coherent position or AV-style choreography that is not yet in the library. Before using a new position, define support points, pelvis/body orientation, driver/receiver roles, anatomical axis, physically available travel, force path, receiving-body response, camera readability, and the release/preserve/re-establish transition model. If the new pattern is likely to recur, add a reusable template to the library instead of treating the existing catalog as exhaustive.

Default adult kissing style under broad AV choreography: unless the user requests a softer kiss, write kissing as aggressive open-mouth French kissing with clearly parted lips, active tongue contact, changing head angles, jaw/neck movement, close face pressure and irregular brief releases for breath before re-engaging. Kissing is an overlay on the ongoing body action and must not automatically pause the established cyclic motion.

## Optional H3 LoRA Routing

When the user explicitly asks which H3 LoRAs to use, supplies LoRA filenames/triggers, or the active workflow already exposes LoRA slots that must be configured, read [references/h3-lora-routing.md](references/h3-lora-routing.md).

Keep three layers separate: author-published metadata, this repository's empirical multi-LoRA starting points, and per-segment enable/disable decisions. Do not present project starting strengths as official author defaults. Do not force LoRA choices into an ordinary prompt-only task when the user did not request adapter configuration.

Use role-based routing rather than loading everything at full strength: anatomy adapters only where their anatomy is relevant, one broad main-motion layer by default, optional Ref2VA enhancement conservatively, and realism according to its documented trigger requirements. Trigger words belong in the actual executed prompt only when the selected adapter documents or requires them; a project helper label such as `LoRA trigger cues:` is not an H3 protocol field by itself.

Actual LoRA filenames, strengths, sampler/scheduler, node order and runtime toggles remain workflow/runtime configuration unless the consuming controller explicitly supports them. The current `story_segments.json` outer schema does not gain new LoRA fields from this reference.

## Express Emotion and Intensity Through Observable Actions

When authoring or revising emotional performance or physical intensity, do not use adjectives or abstract states as the entire action instruction. Words such as “大幅度”, “用力”, “享受”, “紧张”, “愤怒”, “intense”, or “enjoying” may qualify a concrete action, but cannot replace it. Apply this rule inside each affected Shot in the actual execution prompt, not only in a summary or an outer JSON field.

Describe who moves, which body part moves, and what it does to which target. Make direction/path, visible range, pace/repetition, contact or weight transfer, and the resulting posture clear where relevant. Express emotion through context-appropriate gaze, facial changes, hand movements, and body reactions; do not force every cue into every shot or assign one fixed gesture to every emotion. Use meaningful spatial anchors or timing when helpful, without inventing unsupported exact measurements.

Examples illustrate the writing method only; use them only when the underlying action already belongs to the user's scene:

- Instead of only “用力推门”: “双掌抵住门板，前脚向前踏半步，屈肘后逐渐伸直双臂，肩膀和身体重心向前压，门板随推动缓慢打开。”
- Instead of only “大幅度挥手”: “手臂从腰侧抬到头顶上方，再向身体外侧划出宽弧，连续左右摆动。”
- Instead of only “享受地喝茶”: “抿一口茶后缓缓咽下，眼睑轻合，肩膀放松下沉，嘴角微微抬起。”
- Instead of only “紧张地等候”: “视线反复移向门口，拇指来回摩擦另一只手的指节，双肩微微收紧。”

Preserve the requested emotion, existing action, physical path, and continuity. Do not invent new plot beats, props, contact, dialogue, or sounds to demonstrate a feeling. For intensity requests, also apply V18; visible movement must carry the requested amplitude and cadence rather than merely adding stronger adjectives. Pure format-only packaging preserves the source wording and reports vague action descriptions separately instead of rewriting them without authorization.

When visible emotional or performance reactions are requested, put a concrete response inside every affected Shot, tied to that Shot's current trigger. Vary the relevant eyelid, gaze, brow, jaw, lip, head, hand, shoulder, or torso response rather than repeating one fixed signature expression. These are available cues, not a mandatory list for every shot; breathing as a visible response does not authorize an added vocal sound. A requested brief camera glance happens during the ongoing action and must not introduce a pause or reduce its cadence.

## Female Face Priority Camera Contract

When the woman is the visual anchor, or when an adult two-person AV-style scene has no contrary framing instruction, default to **seeing the woman's face first** across kissing, intercourse, oral/manual action, position transitions, and other intimate performance. Preserve a readable frontal-to-three-quarter view of her face whenever physically possible. The male performer does not need a frontal face unless the user explicitly requests it.

This is a **scene-adaptive framing rule, not a fixed camera position**. Do not force every shot into the same male-over-shoulder composition, but also do **not** leave the camera choice as an unresolved menu of options for the renderer. The author must inspect the current body geometry and explicitly choose one concrete camera position for every identity-critical Shot.

Scene-adaptive decision rule:
- **face-to-face kissing / wall pin / close frontal intercourse where the man's head would naturally block the woman**: prefer a camera just behind and slightly above the man's right or left shoulder, whichever keeps the woman's face frontal-to-three-quarter; the man becomes a limited foreground frame element;
- **supine woman already facing upward toward camera**: prefer offset bed-end, low front three-quarter, or side-front three-quarter; do not insert over-shoulder merely by habit;
- **woman-on-top / seated straddle**: prefer lower-partner POV-like, low front three-quarter, or side-front medium-close framing, whichever keeps her face naturally frontal;
- **rear-entry / prone**: prefer side-front or front-three-quarter toward the woman, with her head/eyes turned enough to keep the face readable while preserving rear-body action context;
- **oral action with the woman as giver**: prefer front or front-three-quarter toward her face while retaining the recipient's pelvis/body attachment context;
- **standing or hybrid positions**: choose the side/height that reveals the woman's frontal or three-quarter face without breaking support geometry.

Do not write several alternative angles inside one execution Shot such as “over-shoulder or side-front or low-front.” Resolve the choice during authoring and write the single selected angle explicitly. The selected camera must satisfy the woman's face-priority goal before delivery.

Default priority:
- preserve the woman's eyes, nose bridge, cheeks, jawline, and overall facial readability before preserving the man's frontal face;
- if one performer must be partially occluded, prefer occluding the man;
- the man may appear as shoulder, back-of-head, cheek edge, jaw edge, neck, or partial side profile when that better preserves the woman's face;
- prefer the woman's face around frontal to roughly 20–35 degrees three-quarter rather than a full side profile when the action geometry allows it;
- avoid an equal side-profile two-shot when another coherent angle can keep the woman's face readable;
- during kissing or close face-to-face intercourse, rotate or offset the man's head first rather than forcing the woman's head into profile;
- in rear-entry, prone, woman-on-top, oral, seated, or standing positions, choose a different face-preserving angle when over-shoulder would be unnatural or would hide the action;
- male frontal-face visibility is optional unless explicitly requested.

Use male-over-shoulder only when it is the best solution for the current geometry. When used, place the camera just behind and slightly above the man's shoulder and keep his shoulder / cheek edge / back of head only as a limited foreground frame element. Do not let that foreground element block the woman's eyes, nose bridge, cheeks, or jawline.

Face priority does not mean a detached portrait crop. Preserve enough torso, pelvis, support-point, or partner context to keep the active action readable.

## Scope Boundary

- Treat explicit user constraints as fixed. When the user delegates broad authorial control, freely design story beats, action progression, contact/choreography, wardrobe transitions, props, vocal reactions, climax/aftermath beats, and other details that fall inside that delegated scope; do not substitute cast, relationships, location, or visual style unless those are also delegated.
- Do not turn an example from an earlier project into a default scenario.
- For a narrowly specified action request, preserve the requested action and change only authorized timing, geometry, pacing, and handoff details. For broad creative delegation, construct a coherent forward progression rather than limiting the prompt to only actions explicitly named by the user.
- Do not render, queue, upload, or alter a workflow unless the user separately asks.
- Default to Plan 5 tail-lineart continuation: two permanent identity pictures in every segment, plus the preceding segment's final-frame lineart as `<Picture 3>` from segment 2 onward. The workflow extracts and converts the tail automatically. Use the original text-only Opening State profile only when explicitly selected; do not silently substitute it for the three-picture route.
- Unless the user explicitly requests a silhouette, obscured face, or deliberately dim treatment, default identity-critical faces to clean, bright, even exposure and clearly resolved detail without changing the requested time of day or mood.
- Unless the user explicitly overrides this production style, place every generated scene in a bright enclosed interior with no visible windows and no natural light. Use only bright, soft, even artificial lighting, and keep doors, walls, trim, and furniture light-colored, plain, uncluttered, and minimalist.
- Default to writing a UTF-8 `story_segments.json` file, not a prose-only answer. A prompt-only response is allowed only when the user explicitly asks for one.

## Output File Format: Select Before Authoring

The default is **Plan 5 tail-lineart continuation**, for `H3-方案5衍生-全局人物-尾帧线稿续接-横竖屏.json`. Every segment binds the same `<Picture 1>` female identity and `<Picture 2>` male identity. Segment 1 receives only those two images. From segment 2 onward, `<Picture 3>` is the lineart made from the immediately preceding segment's actual final frame. It remains `<Picture 3>` in every continuation; its number does not increase with the segment ID. No segment binds `<Video 1>`. The runtime extracts the tail and converts it to lineart without 2× upscaling or color correction.

In each continuation's six-section prompt, keep identity attached to Pictures 1/2. **Picture 3 governs the opening composition, body positions, pose, contact points, prop placement, camera axis and visible action phase.** Keep Opening State brief: primarily supplement established colors and current clothing state that the lineart cannot express clearly, without restating or preassigning spatial/pose details that could conflict with the actual tail. Keep the requested subsequent action separate from this opening-state supplement; it begins from the supplied reference rather than resetting the pose. The lineart is not a third character or the target drawing style.

The current runner passes the actual lineart but does not automatically recognize mutable state or rewrite the JSON prompt. This is the existing Ref2VA Picture 3 tail-reference route with a lineart preprocessing step, not an I2V mode switch or a pixel-exact first-frame guarantee. Apply the following state-authority rules when writing or revising this profile.

### Tail-Lineart State Continuity

Split continuity authority into three layers:

1. Permanent identity references control facial identity and stable identity-critical appearance.
2. `<Picture 3>` controls opening geometry: composition, body positions, pose, contact points, prop placement, camera axis, and visible action phase.
3. Prompt text carries relevant non-geometric mutable state that lineart cannot reliably preserve: colors, garment identity/layers, wearing or fastening state, footwear state, changed prop state, established material/color palette, and lighting/exposure state.

### Mandatory Per-Segment Continuity State Lock

For the default tail-lineart profile, **every segment**, including Segment 1, must carry a concise `Continuity State Lock:` block inside `detailed_description` before `[Shot 1]`. Do not rely on the outer `global_prompt`, Picture 3, or an identity image to remember these non-geometric states.

The block must cover, when relevant and known:

- **Wardrobe/Body State** for every persistent subject: each garment and layer currently worn, loosened, partially removed, fully removed, fastened/unfastened, footwear on/off, and current nudity state where applicable.
- For a **partially completed garment transition**, record the remaining attachment points and fabric location precisely enough to continue the same removal rather than restarting it: e.g. which sleeve/strap/leg remains on, where the garment is gathered, and which body region is already uncovered.
- **Color/Material State**: established hair/skin appearance, garment colors/materials, bedding, walls, furniture, and important prop colors/materials that must remain visually stable.
- **Lighting/Exposure State**: established artificial-light type, direction, softness, color-temperature tendency, white balance, exposure/contrast level, and overall grade/palette.

Segment 1 establishes the known baseline from the user request and supplied references without inventing unsupported hidden details. Segment 2+ repeats the currently established state explicitly because lineart cannot carry color or material information reliably. If the story intentionally changes wardrobe, color, prop state, or lighting, treat that as a one-time state transition: describe it once, make the resulting end state explicit, and carry only the new state into later segments.

Within any Shot that changes wardrobe or another mutable visual state, finish the relevant action with a concise **resulting-state sentence**. The next Shot/segment starts from that exact result. A garment that is still partly on remains partly on with the same remaining attachment points; it does not jump back to fully worn or ahead to fully removed.

Segment 1 has no previous tail: do not define or mention `<Picture 3>` anywhere in its prompt, including a negative instruction. Segment 2 onward uses the immediately preceding accepted final-frame lineart as `<Picture 3>`. Technical completion alone does not establish visual acceptance; stop for review or correction when the actual tail disagrees with the intended state.

Maintain a concise working mutable-state ledger independently for every persistent subject and relevant prop, not only the visual lead. Follow the [per-subject ledger and state-handoff rules](references/ref2va-prompt-contract.md#per-subject-mutable-state-ledger). Completed one-time changes remain in their resulting states until the story explicitly reverses them; identity pictures or camera cuts must not reset them. This planning ledger is not an extra field in `story_segments.json`.

Before future tails exist, derive the next prompt's text-carried state from the previous segment's explicitly completed planned end state. Distinguish this planning assumption from an observed result; never claim to have inspected a future Picture 3. Omit unsupported details or unresolved outcomes instead of guessing. Partial transitions continue from their inherited phase rather than being treated as complete or restarted.

Once an accepted raw tail exists, it is authoritative for mutable state, while its derived Picture 3 is authoritative for opening geometry. Actual accepted evidence overrides a merely planned state. If they disagree, revise the next prompt or regenerate the preceding segment within the authorized scope; do not conceal the mismatch with contradictory text. Preserve confirmed unchanged details that the current view does not reveal, and never infer colors from black-and-white lines.

### Other Output Profiles

Explicit alternatives remain supported: the original **Plan 5 (No Video / Opening State)** uses only Pictures 1/2 and textual continuity; the older color-tail Picture 3 workflow uses its actual tail-processing configuration rather than claiming lineart. Preserve the selected workflow's binding and existing task snapshots.

For a new multi-segment chain, read [references/story-segments-json.md](references/story-segments-json.md) and use the dynamic-series envelope: `global_prompt` plus `segments`, with consecutive integer `id`, `title`, `raw_prompt: true`, and one complete `prompt` string per segment. Support the requested positive segment count, including 4, 6, and more; this envelope has no fixed segment-count maximum.

This changes the delivered file format, not the prompt-writing standard. Apply the existing six-section Ref2VA contract, style, speech, shot timing, retention, and continuity requirements to every `prompt`. Do not flatten the six sections into separate JSON properties, substitute a plot summary, or introduce new scene requirements for packaging. A format-only repackaging preserves the supplied prompt strings exactly.

Resolve reference numbers from the selected workflow before writing prompts. In the original two-image dynamic workflow and Plan 6, `<Picture 1>` and `<Picture 2>` retain their assigned identities. The original workflow uses `<Video 1>` from segment 2 onward; Plan 6 is hybrid and binds it only on video-reference segments. Where bound, `<Video 1>` means the immediately preceding tail video and its number does not increase with `id`. Both Plan 5 variants keep Pictures 1/2 as identities and have no video input; only the tail-reference variant adds Picture 3. See [the workflow-specific mappings](references/story-segments-json.md). Do not infer a cast count from the number of pictures, relabel an identity image as a tail, or mechanically replace tags in existing user text. Reference conditioning does not guarantee literal first-frame equality.

Only use the sections marked **Legacy** below when the user requests `sequence.json`, the existing `version: 3` controller, or a Ref2VA/I2VA dual-prompt package. That profile retains its `sets/clips`, translations, duration fields, 1–32-clip limit, and image-tail mapping. Its packaging-only requirements do not add `prompt_en`, `prompt_cn`, `prompt_i2v_en`, `scene_style`, or duration fields to `story_segments.json`. Preserve the existing prompt-level style policy within the actual execution text.

For a format-only request, do not silently convert reference roles, language, or timing to make a different renderer compatible. Report a binding or duration mismatch separately. Do not render or modify runtime configuration merely to produce either file.

## Ref2VA Authoring Route

Before writing or revising any Ref2VA execution prompt, read [references/ref2va-prompt-contract.md](references/ref2va-prompt-contract.md). It defines section responsibilities, global-constraint placement, reference and speaker labels, retention markers, cut-time syntax, sound layers, an original complete example, and the pre-delivery review.

- For an explicit single-prompt request, output the six-section prompt without requiring a segment chain or JSON wrapper. For a chain, apply the same contract independently to every `prompt` (dynamic series) or `prompt_en` (legacy sequence), using only the selected profile's outer fields.
- For shot-to-shot character continuity, use the reference's three-layer method: define identities, retain referenced appearance, then put global invariants before `[Shot 1]` and concrete state handoffs inside subsequent shots. Stable build/hair/wardrobe identity does not freeze acting poses or reverse clothing changes explicitly required by the story.
- For a format-only edit, preserve the user's text, language, meaning, reference mapping, and timing. Normalize only authorized syntax; report missing semantic material instead of inventing it. Follow the reference's format-only procedure, including restricted-content inspection when requested.
- Official format requirements, upstream writing recommendations, and this repository's production defaults are different. The 5–15-second sequence limit, windowless-interior policy, and identity/tail layout are repository contracts, not universal H3 syntax. Explicit user scene/style choices override the corresponding defaults.
- The legacy picture layout below assumes one permanent identity image and one tail image. Dynamic-series bindings depend on the selected workflow: the current default adds Picture 3 tail-lineart to the two identities from segment 2 onward; original Plan 5 is explicitly text-only; the original dynamic workflow and Plan 6 bind video only where configured. Reserve a distinct label for each identity and a separate label for the tail instead of assigning two incompatible roles to `<Picture 2>`.

## Minimal Input Contract

Require only:

- requested positive segment count (the legacy `sequence.json` profile supports 1 through 32);
- either one shared duration or an ordered duration list with one value per segment;
- one scene description, which may include people, actions, setting, wardrobe, mood, camera, audio, or dialogue at whatever detail the user chooses.

Do not ask the user for a launcher, LoRA/native choice, reference-image path, model, sampler, steps, resolution, seed, or continuity mode. When the user prioritizes quality consistency or reproducible rendering but supplies no seed, choose and record deterministic per-clip seeds under the seed policy below instead of asking. The consuming workflow supplies the selected profile's references at runtime: the current default supplies two permanent identities and automatically appends the previous tail-lineart from segment 2 onward. Do not require a pre-existing tail file when authoring initial JSON. If no identity details are included in the scene, define neutral persistent subjects from their assigned identity pictures without inventing facial landmarks, wardrobe, or biography. If the scene contains fewer action beats than segments and the user has not delegated creative expansion, extend only with forward motion, reaction, settling, or holds already implied by the scene. If broad authorial control is delegated, create additional forward-moving beats within the authorized scope instead of padding the chain with repetitive holds.

When the request prioritizes brightness, facial clarity, seed selection, rendering, rerendering, or rendered-output QC, also read [references/clarity-exposure-and-seeds.md](references/clarity-exposure-and-seeds.md) and apply its quality gates. Do not load it for an unrelated prompt-only request.

When revising an already rendered chain and an actual tail image is available, inspect it and rewrite the affected next clip from that real state. For initial JSON authoring, use the planned tail state from the preceding clip and keep the runtime reference contract explicit.

Accept the minimal request in this form without asking follow-up questions:

```text
segment_count: 6
duration_seconds: 10
scene: user scene description
```

Also accept `durations: [10, 8, 12, ...]` instead of one shared duration. If no output directory is given, choose a clearly named project folder under the active video workspace.

Normalize timing as follows:

- Accept `segment_count=N` with `duration_seconds=S` to repeat one duration across all segments.
- Accept `segment_count=N` with `durations=[S1, S2, ... SN]` to assign each segment independently.
- Accept a bare ordered duration list and infer the segment count from its length.
- Require exactly one duration per segment after normalization. Do not silently truncate, pad, or reorder the list.
- Keep every duration between 5 and 15 seconds inclusive; 0.5-second increments are preferred for the local workflow.
- If neither count nor durations are supplied, infer the count from the user's explicit segment plan and default each segment to 10 seconds. State that default in the handoff.
- Derive total duration as the sum of normalized clip durations; do not force the result to a round minute.

For dynamic-series delivery, durations remain a planning/runtime requirement, not extra story JSON fields. The current Runner uses one shared `segment_duration_seconds` in its separate project configuration; a varying duration list needs explicit consumer support and must not be silently flattened or added as ignored fields. Refer to the selected output contract before promising runtime support.

## Legacy Workflow-Neutral Contract

For the legacy `sequence.json` profile only, produce both contracts in the same JSON:

- `prompt_en` is a complete Ref2VA prompt. Clip 01 establishes the permanent identity from `<Picture 1>`. Clip 02 onward describe `<Picture 1>` as permanent identity and `<Picture 2>` as the previous actual tail.
- `prompt_i2v_en` is included for Clip 02 onward and treats `<Picture 1>` as the previous tail used as the literal 0.00-second frame.
- LoRA versus native is not encoded in the JSON. A LoRA or native Ref2VA workflow can consume `prompt_en`; a true-first-frame I2V workflow can consume `prompt_i2v_en`.
- Do not recommend or enable dual sampling, first-frame anchoring, a sampling profile, or model parameters unless the user separately asks for workflow configuration.

The default `prompt_en` identity/tail semantics are:

- `<Picture 1>` is the permanent highest-priority facial identity and appearance reference in every clip.
- `<Picture 2>` is the exact ending frame of the previous final/processed clip and controls the next opening pose, contact geometry, composition, wardrobe, lighting, spatial layout, and camera direction.
- When the references conflict, `<Picture 1>` controls facial identity and `<Picture 2>` controls opening geometry.
- Treat `<Picture 1>` as identity-only unless the user explicitly asks to reproduce its portrait composition. It must not control or reproduce the reference pose, crop, framing, background, lighting, camera angle, or standalone-photo composition.
- Define the persistent lead as `<Subject 1>` from `<Picture 1>`. Repeat only identity landmarks explicitly supplied by the user or visibly available from an attached reference; otherwise use neutral identity-preservation wording.
- Keep the face unobstructed and large enough to resolve. Prefer front or three-quarter medium/medium-close views at identity-critical moments; avoid prolonged profile-only, back-of-head, extreme-angle, or tiny-face framing when likeness is the priority.
- Keep identity, wardrobe, and scene retention separate from motion instructions. Do not ask the tail reference to redefine the face.

The consuming workflow may inject or bind these pictures differently, but the generated prompt fields must preserve the semantics above and must not name a particular launcher.

## Reference-Face Takeover Prevention

Prevent the permanent identity image from suddenly replacing the active scene with a standalone reference-like face:

- Repeat this identity boundary in every Ref2VA clip: `<Picture 1> is used only for facial identity. Never reproduce its pose, crop, framing, background, lighting, camera angle, or standalone portrait composition.`
- For Clip 02 onward, make the resolved previous-tail reference authoritative for the current scene, action, spatial relationship, camera scale, lighting, and composition. Continue from its geometry before introducing any new framing.
- When facial clarity is requested, prefer a contextual medium-close or close two-shot that preserves the current environment, action, and subject relationship. Do not translate “clear face” into a detached portrait.
- Avoid `face-only close-up`, `isolate the face`, `the other subject is completely outside frame`, `portrait shot`, or equivalent wording unless the user explicitly requests a standalone face shot and accepts reference-composition takeover risk.
- When a close view is necessary, state what current-scene geometry remains visible, for example the existing shoulder line, contact point, screen-side relationship, or recognizable background element. Keep the active action continuous through the closer framing.
- Do not describe the permanent reference image as a literal first frame in continuation prompts. In `prompt_i2v_en`, `<Picture 1>` remains the actual previous tail; the permanent identity image must not be relabeled as the I2V opening frame.
- A seed change may remove one occurrence but does not repair ambiguous reference authority. Fix picture roles and framing language first, then use a fixed alternate seed only if needed.

If a rendered clip shows only a reference-like face, reject it as an identity-reference takeover unless the user explicitly requested that composition. Do not propagate its tail into later clips.

## Default Face Clarity and Exposure Contract

Apply this contract to every clip unless it conflicts with an explicit artistic request:

- Keep each identity-critical face unobstructed, in focus, and large enough to resolve. Prefer front or three-quarter medium/medium-close framing when the face matters; do not leave the lead tiny for most of a clip.
- Preserve the requested environment and time of day while giving the face a clean, bright, soft key light appropriate to that environment. A night scene may remain visibly night while the face stays readable and naturally colored.
- Keep facial exposure, white balance, skin tone, contrast, and focus stable across the clip and across the seam. Retain detail in both facial shadows and highlights; do not achieve brightness by clipping the skin.
- Prefer controlled subject motion and one simple camera move. At identity-critical moments, avoid combining rapid head rotation, fast body movement, and strong camera motion.
- State the quality target positively in each execution prompt of the selected profile (both Ref2VA and I2V for a legacy dual-prompt package). A reusable sentence is: `The face remains cleanly and evenly exposed with a soft frontal key light, natural skin tone, clearly resolved eyes and facial features, stable exposure and white balance, sharp focus, crisp motion edges, and controlled movement throughout the shot.`
- Short technical exclusions such as `no crushed facial shadows, no blown facial highlights, no haze, no bloom, no ghost trails` are allowed, but they supplement rather than replace the positive visible target.
- Do not treat extra sampling steps, bitrate, sharpening, or super-resolution as a substitute for a well-exposed, sharp generated face. Missing or motion-smeared facial detail must be corrected at generation time.

For a non-cyclic 10-second transition clip, use one dominant transition and reserve the final 0.75-1.0 seconds for a low-velocity continuation or stable hold with the face visible, exposure settled, and motion edges clean. This is the handoff-quality interval for the next clip, not dead time.

## Bright Windowless Minimal-Interior Contract

Apply this scene contract to every clip unless the user explicitly overrides it:

- Use an enclosed interior with no visible windows, glass curtain walls, skylights, exterior openings, or daylight views. Do not introduce a window as background decoration.
- Do not use sunlight, daylight, moonlight, window light, or any other natural-light motivation. Illuminate the scene only with bright, soft, even artificial sources such as diffused ceiling fixtures plus a soft frontal key/fill on identity-critical faces.
- Keep the overall exposure bright and clean without clipped skin or flat overexposure. Avoid dark corners, heavy backlight, strong chiaroscuro, muddy brown grading, and deep crushed shadows.
- Make doors, walls, trim, cabinets, tables, seating, and other visible furniture light-colored and restrained: warm white, off-white, light beige, or light neutral gray. Prefer plain surfaces, simple lines, sparse decoration, and an uncluttered minimalist layout.
- Exclude dark wood dominance, ornate carved doors, visually heavy furniture, saturated feature walls, luxurious decorative clutter, and busy patterns unless the user explicitly requests one of them.
- Preserve the same artificial-light direction, color temperature, palette, wall/door treatment, and furniture style across clip boundaries. A tail with a window, daylight spill, or dark heavy decor fails the handoff gate and must not be propagated.

Repeat this exact sentence in every English execution prompt so the package can be validated deterministically:

`The setting is an enclosed windowless interior with no visible windows and no natural light. It is illuminated only by bright, soft, even artificial lighting. Doors, walls, and furniture are light-colored, plain, and minimalist.`

Put the global environment and lighting description, including the canonical sentence, at the opening of `detailed_description` or inside `integrated_multimodal_description`, then show the visible fixture/key-light behavior in the shot. Use `retention_analysis` only for the actual environment or lighting preserved from a defined reference/tail, with its reference label and relationship marker; do not use it as a bucket for newly requested scene rules. Short exclusions such as `no windows, no daylight, no sunlight, no dark heavy furniture` may supplement the positive contract. If an actual previous tail violates this contract, do not make the window or light source disappear at frame 1; stop and rerender the first violating clip or request an explicit style override.

## Seed Policy

A seed makes a result reproducible; it does not carry identity and does not guarantee brightness or quality.

- For quality-consistent multi-clip work, default to one recorded fixed seed per clip, with a different seed for each clip. Do not use one identical seed for the whole chain unless the user explicitly requests that experiment.
- If the user supplies one seed for a multi-clip chain, treat it as a base seed and derive a stable unique seed for every clip unless the user explicitly says to reuse the identical value. Record the resolved seed on every clip.
- If the user supplies a complete ordered seed list, preserve it exactly. Require one valid seed per clip and do not truncate, pad, or reorder it.
- When no seed is supplied and reproducibility or quality consistency is requested, choose one base seed, derive a deterministic unique per-clip list, save it in the clip objects, and report the list. Use a stable derivation such as `seed[i] = (base_seed + i * 10007) mod 2^63`, with zero-based `i`, resolving any collision before delivery.
- Keep a clip's seed fixed while comparing prompt, workflow, or parameter changes. If composition and continuity are acceptable but exposure or sharpness fails, test a small bounded set of alternate seeds for that clip, select the visually accepted result, and then lock that seed.
- Never change seeds of already accepted clips merely for variety. If rerendering a clip changes its accepted tail, all later clips derived from the old tail must be treated as stale and rerendered from the new actual tail.

For prompt-only packages without a quality-consistency or reproducibility request, seeds may remain omitted so the JSON stays renderer-neutral.

## Multi-Subject Instance Continuity

Prevent duplicate people or objects when the previous tail already contains more than the permanently locked lead:

- Assign every persistent visible person or important object a stable `<Subject N>` ID. For Clip 02 onward, state that each such subject is the same existing instance already visible in the resolved previous-tail reference.
- Never reintroduce an existing tail subject with indefinite wording such as `a person enters`, `another person approaches`, or `a new vehicle appears` unless the user explicitly requests an additional instance. Rewrite it as the same subject continuing from the current tail position.
- When the requested count is unambiguous, state the permitted count positively and explicitly, for example: `Exactly one instance of <Subject 2> remains in the shot throughout this clip.` A short technical exclusion such as `no additional people` or `no duplicate subjects` is allowed because extra-subject suppression does not replay a completed story action.
- Keep reference authority separate: permanent identity images control only their assigned identities; the previous-tail reference carries current positions and contact geometry. For the lineart profile, derive mutable appearance from the accepted raw tail or the scoped planning ledger, not from black-and-white lines. Preserve any separate identity references supplied for secondary subjects.
- A single-person identity reference should contain only the intended locked subject. If it also contains an unintended person, crop or replace it when asset editing is authorized; otherwise label every visible person and flag the duplication risk rather than silently treating the extra person as background.
- Preserve the exact count and screen-side assignment across the seam. Do not move an existing subject to a distant new position by restaging the subject; describe one continuous path from the tail position or insert a bridge segment.
- For an intentional entrance or exit, specify which stable subject moves, its visible path, and the exact before/after count. Do not combine an existing tail instance with a separately worded arrival of the same subject.
- `anchor_first_frame=true` cannot solve duplicate-instance drift. It matches only the encoded first frame; the prompt and Ref2VA subject mapping must keep the same instance count after frame 1.

Place these constraints where they affect model interpretation: map stable subjects in `subject_definitions`, preserve referenced identity/count/opening position in `retention_analysis`, and put the requested global instance count plus forward continuation from the tail in `detailed_description`. Do not mark a planned entrance or movement as a loss of identity retention. In a legacy dual-prompt package, apply the same instance mapping to `prompt_i2v_en` without inventing a second copy of any subject.

## Continuity Method

Before drafting, form a compact state vector from the preceding planned tail, or from the actual tail when one exists:

1. subject positions and screen direction;
2. body pose, head orientation, limb placement, and all contact points;
3. measurable spacing between important body parts or objects;
4. the motion already underway, including direction and approximate speed;
5. camera framing, axis, movement, scene geometry, and lighting;
6. each persistent subject's relevant mutable garment, footwear and prop state;
7. which action or one-time state transition has already completed and must leave the active action vocabulary.

For a one-time transition, design a forward-only path. For user-requested cyclic movement, preserve phase and the current trajectory through natural return strokes instead; do not force a monotonic path across whole cycles:

- At 0.00 seconds, preserve the state vector exactly.
- Within the first 0.25 seconds, continue the visible trajectory; do not pause to re-establish the pose.
- For a one-time transition, describe one monotonic geometric change in the first 1–2 seconds, such as distance continuously increasing, an elbow angle continuously opening, a hand sliding along one path, or shoulders rotating in one direction.
- Give a one-time transition segment one dominant transition, optionally followed by settling without reversal. A requested cyclic segment instead sustains its established movement without replaying an earlier story transition.
- Keep camera motion simple and subordinate to subject motion. Prefer one unbroken shot at a stable axis for a seam-critical continuation.
- End in a stable state, or in one clearly unfinished trajectory whose direction the next segment can continue.

## Semantic Replay Prevention

Anti-replay applies to one-time mutable-state transitions as well as plot actions: putting on or removing an outer garment, opening/closing or fastening/unfastening, picking up/dropping/handing off an object, switching a device on/off, and completing a one-way positional transition. Carry each resulting state forward unless the story explicitly reverses it. A camera cut or new reference does not authorize repeating the transition. True cyclic motion instead continues from its inherited phase.

Build a temporary quarantine list from actions completed in the preceding segment. Remove those concepts from the continuation prompt, including:

- negative instructions containing the completed action;
- labels such as `post-X`, `after X`, `second X`, `X again`, or `do not X`;
- recap sentences that name or summarize the completed action;
- conditional branches that describe both the earlier and later states.

H3 can reactivate a concept even when it appears inside a negation. Replace semantic prohibitions with visible positive geometry. Prefer `the distance between their faces increases continuously` over naming an earlier face action and forbidding its repetition.

Quarantine completed transition verbs, not the necessary current-state facts. For example, carry `the blue jacket lies on the chair; the same gray shirt remains visible` rather than recapping how the jacket got there or giving another removal instruction. Keep such object state distinct from Picture 3's authority over its opening placement.

### Terminal-State Vocabulary Isolation

Treat every state field as a serializer of the **current visible state**, not a historical ledger. Once an entity reaches a stable absent terminal state and the story does not explicitly reintroduce it, remove that entity's vocabulary from later prompts as well as its transition verb.

- Do not keep naming an absent garment, accessory, footwear item, prop, or other removed entity in `Wardrobe/Body State:`, `Color/Material State:`, `retention_analysis:`, negative instructions, recap sentences, initial-state reminders, or conditional clauses merely to say that it is gone.
- Do not preserve the color/material attributes of an entity that is no longer present. `Color/Material State:` should list only currently present people, surfaces, objects, and visible materials that still need continuity.
- If a removed entity remains physically visible in the active scene, reclassify it as a scene prop and track its current location/appearance. If it is absent from the active scene, omit it entirely until the user explicitly reintroduces it.
- When a body or wardrobe state is terminal and should remain locked, write the positive current state directly. Do not write that the state may `evolve` in `retention_analysis:` unless a later state change is actually requested.
- Permanent identity references define identity only; they never authorize restoration of a mutable appearance state that the story has already changed.

This lexical isolation is especially important with lineart tails because Picture 3 cannot carry color/material evidence strongly enough to counteract a reactivated noun from Picture 1/2 or from the text prompt.

Use negative wording only for short technical exclusions that do not repeat the completed semantic action, for example cuts, text, watermarks, anatomy defects, or extra subjects when relevant.

## Legacy H3 I2VA Output Contract

For an exact-first-frame I2V continuation, start exactly with:

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.
```

After one blank line, output exactly these fields in order:

```text
integrated_multimodal_description: [Shot 1] ...

overall_soundscape: ...

non_diegetic_music: ...
```

Write field contents in English except exact user-supplied dialogue or visible text. Preserve exact dialogue using the H3 language-tag syntax when dialogue exists. Do not add dialogue or music. Use `N/A` for non-diegetic music when none is requested.

Within `integrated_multimodal_description`:

- anchor only attributes visible in the tail or explicitly supplied by the user;
- express the opening motion directly, without `if` branches;
- use strictly increasing timestamps inside the duration;
- describe physically observable paths and contact changes;
- keep identity, wardrobe, screen positions, axis, and environment stable;
- keep the current scene and relationship visible during close framing; never replace the continuation with a standalone identity-reference portrait;
- avoid ending with a new action that has not visibly begun.

## Legacy Workflow JSON Contract

For the legacy profile only, create this exact outer structure:

```json
{
  "version": 3,
  "title": "user-supplied or neutral descriptive title",
  "scene_style": {
    "environment": "windowless_bright_minimal_interior",
    "lighting": "bright_even_artificial_only",
    "palette": "light_neutral_plain_minimal"
  },
  "sets": [
    {
      "set_id": "filesystem-safe-stable-id",
      "clips": []
    }
  ]
}
```

The first `set` must contain 1–32 clips. Preserve the user's requested segment count. Every clip must contain:

```json
{
  "clip_id": "01",
  "duration_seconds": 10,
  "prompt_en": "...",
  "prompt_cn": "..."
}
```

Rules:

- Number `clip_id` consecutively with two digits.
- Unless explicitly overridden by the user, include the exact `scene_style` object shown above and repeat the canonical bright-windowless-minimal sentence in every `prompt_en` and `prompt_i2v_en` execution prompt.
- Keep `duration_seconds` between 5 and 15 inclusive.
- Use the normalized ordered duration list, so each clip may have a different `duration_seconds` value.
- `prompt_en` is mandatory for every clip because the workflow validator requires it.
- `prompt_cn` is mandatory for every newly generated clip. It is a human-readable Chinese translation and is ignored safely by the local controller.
- Clip 01 uses `prompt_en` as the Ref2VA identity-establishing prompt and normally omits `prompt_i2v_en`.
- Clip 02 and later must also contain `prompt_i2v_en`. This is the primary prompt used by the exact-first-frame continuation controller and a compatibility field in LoRA identity-lock mode.
- For Clip 02 and later, retain a complete, nonempty `prompt_en` as the Ref2VA compatibility/fallback prompt; do not use a placeholder.
- Put line breaks inside JSON strings as escaped `\n`. Write valid JSON with no comments, trailing commas, Markdown fences, or unresolved placeholders.
- Add `seed` when the user supplies one, requests per-clip seeds, or activates the quality-consistency/reproducibility seed policy. It must be an integer from 0 through `2^63-1` exclusive.
- When the deterministic seed policy is active, add a valid `seed` to every clip; never create a partially seeded sequence. Different per-clip seeds are the default, while identical seeds are allowed only when explicitly requested.

Every `prompt_en` uses these six plain field headings, with ASCII colons and no Markdown heading prefixes:

```text
subject_definitions:
summary:
retention_analysis:
detailed_description:
overall_soundscape:
non_diegetic_music:
```

Apply the full [Ref2VA prompt contract](references/ref2va-prompt-contract.md), not just the headings. In particular, keep `summary` to one short task paragraph; give each separately tracked reference its retention marker; place global filming/performance rules before `[Shot 1]` in `detailed_description`; use `[Shot N] At MM:SS.mmm, ...` for later cuts; and keep dialogue, ambience, and score in their proper fields. No field provides an absolute obedience guarantee.

For dual-reference Ref2VA continuation, keep `<Picture 1>` associated with permanent identity and `<Picture 2>` associated with the previous tail. Describe the next clip's first 0.5–1.0 seconds from the exact tail geometry before introducing a new transition.

`prompt_i2v_en` follows the three-field I2VA contract above. Do not put the permanent identity image into the `prompt_i2v_en` picture label: for continuation clips, `<Picture 1>` is the actual previous tail frame.

`prompt_cn` translation rules:

- Translate `prompt_en` for every clip. The compatibility `prompt_i2v_en` must preserve the same scene action, timing, geometry, audio policy, and ending state in I2V form, so the Chinese review remains semantically accurate whichever renderer is selected later.
- Preserve field names, reference labels, shot labels, timestamps, speaker IDs, language tags, dialogue text, visible text, and special tokens exactly; translate only explanatory prose.
- Keep the same action order, timing, contact points, distances, camera directions, audio policy, and exclusions. Do not summarize, embellish, omit, or reinterpret.
- `prompt_cn` is for review only and must never replace the English execution fields.

Before delivery, run:

```powershell
python scripts/validate_sequence.py --require-cn --require-bright-minimal-interior C:\path\to\sequence.json
```

When the deterministic seed policy is active, also pass `--require-seeds`.

Use `--require-bright-minimal-interior` only while that default production style is active; omit it when the user explicitly overrides the style. This validator checks the JSON package and selected textual contracts, not full Ref2VA semantics, retention completeness, language, dialogue attribution, or shot timing. Also complete the manual pre-delivery review in the Ref2VA reference; a `VALID` result alone does not establish prompt quality or rendered compliance.

Resolve a working Python runtime available in the environment. Rewrite the JSON until validation succeeds.

If the consuming workflow exposes a separate `duration_mode`, varying JSON durations require its JSON-controlled/per-clip option; a uniform override may replace the JSON values. Report this as a compatibility note, not as a workflow binding.

## Multi-Segment Planning

For a requested chain, plan state transitions before writing prose:

```text
segment N start state -> one dominant transition -> segment N tail target
segment N+1 start state -> next dominant transition -> segment N+1 tail target
```

Do not let adjacent segments replay the same completed story transition. The prior segment owns completion; the next segment starts from the resulting geometry. A sustained cyclic action may span segments while continuing its current cycle phase. When the actual render differs from the planned tail, discard the stale next prompt and rewrite it from the real tail image.

For one-time transitions, prefer 5–7 seconds per action when duration is not fixed. When 10 seconds is required, allocate early seconds to the transition and remaining seconds to a non-reversing settle or hold. For requested sustained cyclic motion, maintain the requested cadence through the segment and handoff instead of inserting a settle or hold.

## Strong Head-Tail Linkage

Treat a seam as a short interval, not a single matching frame:

- For one-time transitions, end the previous clip with 0.5–1.0 seconds of low-velocity, unfinished motion whose direction is explicit. For requested sustained cyclic motion, continue its cadence and cycle phase with a clear usable tail instead of forcing deceleration.
- Keep the final 0.75-1.0 seconds cleanly exposed and sharp enough to condition the next clip. Avoid ending during a blink, rapid head turn, occlusion, strong shadow crossing, focus pull, or high-motion smear.
- Start the next clip with the same subject positions, contact points, face direction, camera axis, focal scale, lighting, and motion vector. For a one-time transition, continue that vector for at least 0.5 seconds before changing action. For cyclic motion, continue from the inherited phase and allow the next natural return stroke without resetting the cycle.
- Do not change sitting/standing state, embrace/contact state, screen side, camera distance, or scene geometry at the seam. Move those changes into the body of the next clip.
- Extract the next reference from the actual `final_clip`, including any anchored output, rather than from a planned tail or raw source clip.
- Treat the literal final tail as a quality gate. When rendering or QC is authorized, stop the chain if that tail is visibly underexposed, clipped, defocused, motion-smeared, or identity-damaged; rerender the affected clip instead of silently substituting an earlier prettier frame or propagating the bad tail.
- `anchor_first_frame=true` only forces the first encoded frame to equal the previous tail. It does not prevent frame 2 from jumping. Never accept a seam solely because the 0.00-second frame matches.
- After rendering, compare each boundary at `T-0.05`, `T+0.05`, and preferably `T+0.25` seconds. If the pose or camera jumps immediately after the anchor, rewrite and regenerate the next clip; do not label the seam continuous.

When the user separately requests rendering or QC, inspect every clip at its opening, midpoint, and final handoff interval, plus every before/after seam pair. Compare the identity reference against close, unobstructed midpoint faces; check face exposure, shadow/highlight detail, focus, motion smear, and exposure drift separately from identity. A completed controller or queue is insufficient: require the workflow's terminal completion evidence, the final MP4, `ffprobe`, and visual seam/identity/exposure evidence before calling the chain successful. Automated luminance or blur scores may flag candidates, but visual face-region review is the acceptance gate.

## Delivery

Write the finished JSON to the user-specified directory. If no directory is supplied, create a clearly named project folder under the active video workspace. Default to `story_segments.json` and run `python scripts/validate_story_segments.py PATH_TO_JSON`; this checks only the envelope. For the default Plan 5 tail-lineart profile, also run `python scripts/validate_tailchain_prompts.py PATH_TO_JSON`; this statically checks the six-section heading order, the fixed Picture/Video binding contract, and the required per-segment `Continuity State Lock:` marker only. It does not validate semantic continuity, mutable-state correctness, sound/expression quality, or render quality. For an explicitly selected legacy profile, save `sequence.json` and use its validator and compatibility notes above. Return the clickable file path, segment count, planned ordered durations and total, and the accurately scoped validation result. Runtime timing must be supplied separately for dynamic-series files. Do not ask the user to choose LoRA/native or a launcher, and do not paste the full JSON into chat unless the user asks to preview it.

Before delivery, verify:

- each requested emotion or intensity in the affected execution Shots is grounded in concrete observable actions, with relevant direction, range, rhythm, and physical reactions; adjectives alone do not satisfy this check;
- a revision prompt begins from the accepted actual tail when available; initial tail-lineart JSON defers opening geometry to Picture 3 and derives text-carried state only from an explicitly completed planned prior end state, without presenting that plan as observed evidence;
- every default tail-lineart segment contains one `Continuity State Lock:` before `[Shot 1]`, covering the known per-subject wardrobe/body state plus stable color/material and lighting/exposure state; continuation segments restate these because Picture 3 is lineart;
- mutable state is tracked independently for every persistent subject and relevant prop that changes; each Shot completing a one-time transition makes the resulting end state unambiguous, while partial transitions retain their exact remaining attachment points/fabric location and continue from that inherited phase;
- completed garment, footwear, color/lighting and prop transitions do not replay or silently revert; an actual accepted raw tail overrides a conflicting planned state;
- terminal-state vocabulary isolation is respected: once a removed entity is no longer present, later prompts do not keep naming it or its obsolete color/material attributes unless it remains visible as a separately tracked prop; locked body/wardrobe states are written as positive current states rather than historical removal recaps;
- close interactions preserve each visible body part's correct subject ownership and plausible physical attachment; attached anatomy is not described as an independent handheld object;
- when the adult explicit-action module is active, genital anatomy keeps correct ownership and continuous attachment; oral/manual/penetrative contact follows the requested anatomical path; prerequisite nudity/garment state is completed before the dependent sexual action; position changes preserve or explicitly release/re-establish the relevant contact rather than teleporting it;
- when the adult explicit-action module is active, requested or authorially planned pleasure expressions, moans/gasps, and climax behavior are trigger-specific and naturally varied rather than a fixed face, one sound per movement, or an abrupt unsupported climax state;
- every Shot affected by a requested vocal reaction has its own source and action-triggered sound details, not just a global soundscape sentence;
- a user-designated visual anchor remains the camera priority across cuts and moves without freezing the action during a brief camera glance;
- no quarantined completed-action term remains, including in negatives;
- the opening continues the inherited trajectory; one-time transitions keep a single direction, while requested cyclic actions preserve phase through natural return strokes;
- no completed story transition is replayed or undone; natural return strokes within a requested movement cycle are allowed;
- there is only one dominant transition or sustained action cycle, according to the requested action;
- the ending can serve as an unambiguous next first frame;
- no story or scene content was added beyond the user's request.
- the saved document parses as JSON and passes the selected profile's validator; dynamic-series packaging does not change the prompt strings.
- for a legacy package, every clip includes a faithful `prompt_cn` translation of the prompt actually executed for that clip.
- for a legacy package, both `prompt_en` and `prompt_i2v_en` preserve the same scene action and ending state without naming a launcher.
- the permanent identity reference is explicitly identity-only and cannot take over pose, crop, background, lighting, or standalone framing.
- no unrequested `face-only`, isolated portrait, or other-subject-fully-out-of-frame instruction can cause a reference-like face insert.
- every identity-critical clip carries the clear-face exposure contract unless the user explicitly requested a conflicting visual treatment.
- every non-overridden clip carries the canonical windowless, artificial-light-only, light-colored minimalist-interior contract; in a legacy package, `scene_style` also records the same policy and the corresponding validation flag passes.
- no actual or planned handoff tail contains a visible window, natural-light spill, dark wall/door treatment, or heavy ornate furniture that would be propagated into the next clip.
- when deterministic seeds are active, every clip has one recorded valid seed and the resolved ordered seed list is reported.
- Ref2VA prompts keep permanent face identity and previous-tail geometry on separate, correctly typed references; default tail-lineart segment 1 contains no Picture 3 reference anywhere, while every continuation uses Picture 3 only for structural opening geometry/action phase and keeps Pictures 1/2 as identities. Opening State supplements relevant colors and mutable non-geometric state. Video-reference profiles use `<Video 1>` without incrementing its number; both Plan 5 variants have no video reference.
- every persistent subject already visible in the previous tail keeps the same stable ID, instance count, and screen-side assignment; no existing subject is reintroduced as a new arrival.
- the permanent identity image contains only the intended locked subject, or every additional visible subject is intentionally mapped and reported as a risk.
- seam validation checks beyond the anchored first frame and does not hide a frame-2 jump.
- the final handoff interval is visually sharp, evenly exposed, identity-safe, and suitable as the literal next tail; otherwise the chain stops for regeneration.
- rendered QC rejects any unrequested standalone reference-like face and prevents that tail from entering the next clip.
