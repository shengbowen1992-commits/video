---
name: h3-tailchain-continuity
description: Create workflow-neutral MiniMax H3 identity-tailchain sequence JSON from a segment count, durations, and scene description. Defaults to permanent-reference identity, previous-tail continuity, bright windowless artificial-lit minimalist interiors, clear well-exposed faces, and reproducible per-clip seeds when quality consistency is requested, while remaining compatible with Ref2VA and I2V renderers.
---

# H3 Tailchain Continuity Prompt Writer

Write technically executable prompts for H3 segment chains and package them as one workflow-neutral `sequence.json`. Do not require the user to choose LoRA, native sampling, a launcher, model settings, reference-image paths, seeds, or sampling parameters. This skill may record deterministic seeds when quality consistency is requested, but it does not bind them to a renderer. It controls continuity language and JSON packaging only; the user controls the scene and any explicitly supplied people, plot, actions, styling, dialogue, or camera intent.

## Scope Boundary

- Never invent or substitute characters, relationships, story beats, locations, props, dialogue, mood, or visual style.
- Do not turn an example from an earlier project into a default scenario.
- Preserve the user's requested action. Change only its temporal phrasing, geometry, pacing, and handoff when needed to prevent replay.
- Do not render, queue, upload, or alter a workflow unless the user separately asks.
- Default to a permanent identity reference plus previous-tail continuity semantic contract without binding it to a specific workflow implementation.
- Unless the user explicitly requests a silhouette, obscured face, or deliberately dim treatment, default identity-critical faces to clean, bright, even exposure and clearly resolved detail without changing the requested time of day or mood.
- Unless the user explicitly overrides this production style, place every generated scene in a bright enclosed interior with no visible windows and no natural light. Use only bright, soft, even artificial lighting, and keep doors, walls, trim, and furniture light-colored, plain, uncluttered, and minimalist.
- Default to writing a UTF-8 `sequence.json` file, not a prose-only answer. A prompt-only response is allowed only when the user explicitly asks for one.

## Minimal Input Contract

Require only:

- requested segment count from 1 through 32;
- either one shared duration or an ordered duration list with one value per segment;
- one scene description, which may include people, actions, setting, wardrobe, mood, camera, audio, or dialogue at whatever detail the user chooses.

Do not ask the user for a launcher, LoRA/native choice, reference-image path, model, sampler, steps, resolution, seed, or continuity mode. When the user prioritizes quality consistency or reproducible rendering but supplies no seed, choose and record deterministic per-clip seeds under the seed policy below instead of asking. The consuming workflow supplies the permanent identity image and previous tail at runtime. If no identity details are included in the scene, define a neutral persistent `<Subject 1>` from `<Picture 1>` and do not invent facial landmarks, wardrobe, or biography. If the scene contains fewer action beats than segments, extend only with forward motion, reaction, settling, or holds already implied by the scene; do not invent new plot events.

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

## Default Workflow-Neutral Contract

Always produce both contracts in the same JSON:

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
- For Clip 02 onward, make `<Picture 2>` authoritative for the current scene, action, spatial relationship, camera scale, lighting, and composition. Continue from its geometry before introducing any new framing.
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
- State the quality target positively in both Ref2VA and I2V execution prompts. A reusable sentence is: `The face remains cleanly and evenly exposed with a soft frontal key light, natural skin tone, clearly resolved eyes and facial features, stable exposure and white balance, sharp focus, crisp motion edges, and controlled movement throughout the shot.`
- Short technical exclusions such as `no crushed facial shadows, no blown facial highlights, no haze, no bloom, no ghost trails` are allowed, but they supplement rather than replace the positive visible target.
- Do not treat extra sampling steps, bitrate, sharpening, or super-resolution as a substitute for a well-exposed, sharp generated face. Missing or motion-smeared facial detail must be corrected at generation time.

For a 10-second clip, use one dominant transition and reserve the final 0.75-1.0 seconds for a low-velocity continuation or stable hold with the face visible, exposure settled, and motion edges clean. This is the handoff-quality interval for the next clip, not dead time.

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

Put the positive environment and lighting description in `retention_analysis` and the visible fixture/key-light behavior in `detailed_description` or `integrated_multimodal_description`. Short exclusions such as `no windows, no daylight, no sunlight, no dark heavy furniture` may supplement the positive contract. If an actual previous tail violates this contract, do not make the window or light source disappear at frame 1; stop and rerender the first violating clip or request an explicit style override.

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

- Assign every persistent visible person or important object a stable `<Subject N>` ID. For Clip 02 onward, state that each such subject is the same existing instance already visible in `<Picture 2>`.
- Never reintroduce an existing tail subject with indefinite wording such as `a person enters`, `another person approaches`, or `a new vehicle appears` unless the user explicitly requests an additional instance. Rewrite it as the same subject continuing from the current tail position.
- When the requested count is unambiguous, state the permitted count positively and explicitly, for example: `Exactly one instance of <Subject 2> remains in the shot throughout this clip.` A short technical exclusion such as `no additional people` or `no duplicate subjects` is allowed because extra-subject suppression does not replay a completed story action.
- Keep reference authority separate: `<Picture 1>` controls only the intended permanent identity; `<Picture 2>` carries the current positions, appearance, and contact geometry of secondary subjects unless the user supplies separate identity references for them.
- A single-person identity reference should contain only the intended locked subject. If it also contains an unintended person, crop or replace it when asset editing is authorized; otherwise label every visible person and flag the duplication risk rather than silently treating the extra person as background.
- Preserve the exact count and screen-side assignment across the seam. Do not move an existing subject to a distant new position by restaging the subject; describe one continuous path from the tail position or insert a bridge segment.
- For an intentional entrance or exit, specify which stable subject moves, its visible path, and the exact before/after count. Do not combine an existing tail instance with a separately worded arrival of the same subject.
- `anchor_first_frame=true` cannot solve duplicate-instance drift. It matches only the encoded first frame; the prompt and Ref2VA subject mapping must keep the same instance count after frame 1.

Place these constraints where they affect model interpretation: map stable subjects in `subject_definitions`, preserve identity/count/position in `retention_analysis`, and describe only forward continuation from the tail in `detailed_description`. Apply the same instance mapping to `prompt_i2v_en` without inventing a second copy of any subject.

## Continuity Method

Before drafting, form a compact state vector from the preceding planned tail, or from the actual tail when one exists:

1. subject positions and screen direction;
2. body pose, head orientation, limb placement, and all contact points;
3. measurable spacing between important body parts or objects;
4. the motion already underway, including direction and approximate speed;
5. camera framing, axis, movement, scene geometry, and lighting;
6. which action has already completed and must leave the active vocabulary.

Then design a forward-only path:

- At 0.00 seconds, preserve the state vector exactly.
- Within the first 0.25 seconds, continue the visible trajectory; do not pause to re-establish the pose.
- For the first 1–2 seconds, describe one monotonic geometric change, such as distance continuously increasing, an elbow angle continuously opening, a hand sliding along one path, or shoulders rotating in one direction.
- Give a 10-second segment one dominant transition. A quiet settling phase is allowed after it, but a reverse transition is not.
- Keep camera motion simple and subordinate to subject motion. Prefer one unbroken shot at a stable axis for a seam-critical continuation.
- End in a stable state, or in one clearly unfinished trajectory whose direction the next segment can continue.

## Semantic Replay Prevention

Build a temporary quarantine list from actions completed in the preceding segment. Remove those concepts from the continuation prompt, including:

- negative instructions containing the completed action;
- labels such as `post-X`, `after X`, `second X`, `X again`, or `do not X`;
- recap sentences that name or summarize the completed action;
- conditional branches that describe both the earlier and later states.

H3 can reactivate a concept even when it appears inside a negation. Replace semantic prohibitions with visible positive geometry. Prefer `the distance between their faces increases continuously` over naming an earlier face action and forbidding its repetition.

Use negative wording only for short technical exclusions that do not repeat the completed semantic action, for example cuts, text, watermarks, anatomy defects, or extra subjects when relevant.

## H3 I2VA Output Contract

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

## Workflow JSON Contract

Create this exact outer structure:

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

`prompt_en` follows the Ref2VA section order when Ref2VA formatting is needed:

```text
subject_definitions:
summary:
retention_analysis:
detailed_description:
overall_soundscape:
non_diegetic_music:
```

Every `prompt_en` must follow the official H3 Ref2VA contract rather than merely describing the plot:

- keep the six sections above in exactly that order;
- write the six section bodies in English except exact dialogue, lyrics, and visible scene text;
- use stable `<Subject N>`, `<Picture N>`, `<Video N>`, and `<Audio N>` labels;
- use stable `(S1)`, `(S2)`, and later speaker IDs and preserve exact dialogue inside `<d>[Language] ...</d>`;
- put `[Shot 1]` at the opening without a timestamp and give later cuts strictly increasing timestamps inside the clip duration;
- describe camera motion naturally with motion type and meaningful speed or amplitude;
- keep ambience and physical sounds in `overall_soundscape`, and audience-only score in `non_diegetic_music`.

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

Resolve a working Python runtime available in the environment. Rewrite the JSON until validation succeeds.

If the consuming workflow exposes a separate `duration_mode`, varying JSON durations require its JSON-controlled/per-clip option; a uniform override may replace the JSON values. Report this as a compatibility note, not as a workflow binding.

## Multi-Segment Planning

For a requested chain, plan state transitions before writing prose:

```text
segment N start state -> one dominant transition -> segment N tail target
segment N+1 start state -> next dominant transition -> segment N+1 tail target
```

Do not let adjacent segments own the same action. The prior segment owns completion; the next segment starts from the resulting geometry. When the actual render differs from the planned tail, discard the stale next prompt and rewrite it from the real tail image.

For higher reliability, prefer 5–7 seconds per action. When 10 seconds is required, allocate early seconds to the transition and remaining seconds to a non-reversing settle or hold.

## Strong Head-Tail Linkage

Treat a seam as a short interval, not a single matching frame:

- End the previous clip with 0.5–1.0 seconds of low-velocity, unfinished motion whose direction is explicit.
- Keep the final 0.75-1.0 seconds cleanly exposed and sharp enough to condition the next clip. Avoid ending during a blink, rapid head turn, occlusion, strong shadow crossing, focus pull, or high-motion smear.
- Start the next clip with the same subject positions, contact points, face direction, camera axis, focal scale, lighting, and motion vector. Continue that vector for at least 0.5 seconds before changing action.
- Do not change sitting/standing state, embrace/contact state, screen side, camera distance, or scene geometry at the seam. Move those changes into the body of the next clip.
- Extract the next reference from the actual `final_clip`, including any anchored output, rather than from a planned tail or raw source clip.
- Treat the literal final tail as a quality gate. When rendering or QC is authorized, stop the chain if that tail is visibly underexposed, clipped, defocused, motion-smeared, or identity-damaged; rerender the affected clip instead of silently substituting an earlier prettier frame or propagating the bad tail.
- `anchor_first_frame=true` only forces the first encoded frame to equal the previous tail. It does not prevent frame 2 from jumping. Never accept a seam solely because the 0.00-second frame matches.
- After rendering, compare each boundary at `T-0.05`, `T+0.05`, and preferably `T+0.25` seconds. If the pose or camera jumps immediately after the anchor, rewrite and regenerate the next clip; do not label the seam continuous.

When the user separately requests rendering or QC, inspect every clip at its opening, midpoint, and final handoff interval, plus every before/after seam pair. Compare the identity reference against close, unobstructed midpoint faces; check face exposure, shadow/highlight detail, focus, motion smear, and exposure drift separately from identity. A completed controller or queue is insufficient: require the workflow's terminal completion evidence, the final MP4, `ffprobe`, and visual seam/identity/exposure evidence before calling the chain successful. Automated luminance or blur scores may flag candidates, but visual face-region review is the acceptance gate.

## Delivery

Write the finished JSON to the user-specified directory. If no directory is supplied, create a clearly named project folder under the active video workspace and save it as `sequence.json`. Return the clickable file path, clip count, ordered duration list, total duration, validation result, and concise risk flags only when ambiguity remains. State that the JSON is workflow-neutral and contains both Ref2VA and I2V continuation fields. Do not ask the user to choose LoRA/native or a launcher, and do not paste the full JSON into chat unless the user asks to preview it.

Before delivery, verify:

- a revision prompt begins from the actual tail when one exists; an initial package uses the preceding planned tail state without claiming it was visually verified;
- no quarantined completed-action term remains, including in negatives;
- the first two seconds contain a single explicit motion direction;
- no forward motion is followed by its inverse;
- there is only one dominant transition;
- the ending can serve as an unambiguous next first frame;
- no story or scene content was added beyond the user's request.
- the saved document parses as JSON and passes `scripts/validate_sequence.py`.
- every clip includes a faithful `prompt_cn` translation of the prompt actually executed for that clip.
- both `prompt_en` and `prompt_i2v_en` preserve the same scene action and ending state without naming a launcher.
- the permanent identity reference is explicitly identity-only and cannot take over pose, crop, background, lighting, or standalone framing.
- no unrequested `face-only`, isolated portrait, or other-subject-fully-out-of-frame instruction can cause a reference-like face insert.
- every identity-critical clip carries the clear-face exposure contract unless the user explicitly requested a conflicting visual treatment.
- every non-overridden clip carries the canonical windowless, artificial-light-only, light-colored minimalist-interior contract; `scene_style` records the same policy and the validation flag passes.
- no actual or planned handoff tail contains a visible window, natural-light spill, dark wall/door treatment, or heavy ornate furniture that would be propagated into the next clip.
- when deterministic seeds are active, every clip has one recorded valid seed and the resolved ordered seed list is reported.
- Ref2VA prompts keep permanent face identity and previous-tail geometry on separate picture references.
- every persistent subject already visible in the previous tail keeps the same stable ID, instance count, and screen-side assignment; no existing subject is reintroduced as a new arrival.
- the permanent identity image contains only the intended locked subject, or every additional visible subject is intentionally mapped and reported as a risk.
- seam validation checks beyond the anchored first frame and does not hide a frame-2 jump.
- the final handoff interval is visually sharp, evenly exposed, identity-safe, and suitable as the literal next tail; otherwise the chain stops for regeneration.
- rendered QC rejects any unrequested standalone reference-like face and prevents that tail from entering the next clip.
