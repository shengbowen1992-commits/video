---
name: h3-tailchain-continuity
description: Create workflow-neutral MiniMax H3 identity-tailchain sequence JSON from only a segment count, per-segment duration or duration list, and scene description. Default to permanent-reference identity plus previous-tail continuity, and include both Ref2VA and I2V prompt fields so LoRA or native workflows can consume the same JSON without binding the skill to a renderer.
---

# H3 Tailchain Continuity Prompt Writer

Write technically executable prompts for H3 segment chains and package them as one workflow-neutral `sequence.json`. Do not require the user to choose LoRA, native sampling, a launcher, model settings, reference-image paths, seeds, or sampling parameters. Those are renderer concerns. This skill controls continuity language and JSON packaging only; the user controls the scene and any explicitly supplied people, plot, actions, styling, dialogue, or camera intent.

## Scope Boundary

- Never invent or substitute characters, relationships, story beats, locations, props, dialogue, mood, or visual style.
- Do not turn an example from an earlier project into a default scenario.
- Preserve the user's requested action. Change only its temporal phrasing, geometry, pacing, and handoff when needed to prevent replay.
- Do not render, queue, upload, or alter a workflow unless the user separately asks.
- Default to a permanent identity reference plus previous-tail continuity semantic contract without binding it to a specific workflow implementation.
- Default to writing a UTF-8 `sequence.json` file, not a prose-only answer. A prompt-only response is allowed only when the user explicitly asks for one.

## Minimal Input Contract

Require only:

- requested segment count from 1 through 32;
- either one shared duration or an ordered duration list with one value per segment;
- one scene description, which may include people, actions, setting, wardrobe, mood, camera, audio, or dialogue at whatever detail the user chooses.

Do not ask the user for a launcher, LoRA/native choice, reference-image path, model, sampler, steps, resolution, seed, or continuity mode. The consuming workflow supplies the permanent identity image and previous tail at runtime. If no identity details are included in the scene, define a neutral persistent `<Subject 1>` from `<Picture 1>` and do not invent facial landmarks, wardrobe, or biography. If the scene contains fewer action beats than segments, extend only with forward motion, reaction, settling, or holds already implied by the scene; do not invent new plot events.

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
- Define the persistent lead as `<Subject 1>` from `<Picture 1>`. Repeat only identity landmarks explicitly supplied by the user or visibly available from an attached reference; otherwise use neutral identity-preservation wording.
- Keep the face unobstructed and large enough to resolve. Prefer front or three-quarter medium/medium-close views at identity-critical moments; avoid prolonged profile-only, back-of-head, extreme-angle, or tiny-face framing when likeness is the priority.
- Keep identity, wardrobe, and scene retention separate from motion instructions. Do not ask the tail reference to redefine the face.

The consuming workflow may inject or bind these pictures differently, but the generated prompt fields must preserve the semantics above and must not name a particular launcher.

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
- avoid ending with a new action that has not visibly begun.

## Workflow JSON Contract

Create this exact outer structure:

```json
{
  "version": 3,
  "title": "user-supplied or neutral descriptive title",
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
- Keep `duration_seconds` between 5 and 15 inclusive.
- Use the normalized ordered duration list, so each clip may have a different `duration_seconds` value.
- `prompt_en` is mandatory for every clip because the workflow validator requires it.
- `prompt_cn` is mandatory for every newly generated clip. It is a human-readable Chinese translation and is ignored safely by the local controller.
- Clip 01 uses `prompt_en` as the Ref2VA identity-establishing prompt and normally omits `prompt_i2v_en`.
- Clip 02 and later must also contain `prompt_i2v_en`. This is the primary prompt used by the exact-first-frame continuation controller and a compatibility field in LoRA identity-lock mode.
- For Clip 02 and later, retain a complete, nonempty `prompt_en` as the Ref2VA compatibility/fallback prompt; do not use a placeholder.
- Put line breaks inside JSON strings as escaped `\n`. Write valid JSON with no comments, trailing commas, Markdown fences, or unresolved placeholders.
- Add `seed` only when the user supplies one or requests per-clip seeds. It must be an integer from 0 through `2^63-1` exclusive.

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
python scripts/validate_sequence.py --require-cn C:\path\to\sequence.json
```

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
- Start the next clip with the same subject positions, contact points, face direction, camera axis, focal scale, lighting, and motion vector. Continue that vector for at least 0.5 seconds before changing action.
- Do not change sitting/standing state, embrace/contact state, screen side, camera distance, or scene geometry at the seam. Move those changes into the body of the next clip.
- Extract the next reference from the actual `final_clip`, including any anchored output, rather than from a planned tail or raw source clip.
- `anchor_first_frame=true` only forces the first encoded frame to equal the previous tail. It does not prevent frame 2 from jumping. Never accept a seam solely because the 0.00-second frame matches.
- After rendering, compare each boundary at `T-0.05`, `T+0.05`, and preferably `T+0.25` seconds. If the pose or camera jumps immediately after the anchor, rewrite and regenerate the next clip; do not label the seam continuous.

When the user separately requests rendering or QC, inspect every before/after seam pair and every segment midpoint. Compare the identity reference against close, unobstructed midpoint faces, and report recognizable identity separately from pixel-level likeness. A completed controller or queue is insufficient: require the workflow's terminal completion evidence, the final MP4, `ffprobe`, and visual seam/identity evidence before calling the chain successful.

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
- Ref2VA prompts keep permanent face identity and previous-tail geometry on separate picture references.
- seam validation checks beyond the anchored first frame and does not hide a frame-2 jump.
