---
name: h3-tailchain-continuity
description: Create workflow-ready MiniMax H3 identity-tailchain sequence JSON from the actual previous tail frame, emphasizing forward-only motion and reducing repeated or reversed actions. Use for Ref2V or hybrid Ref2VA-to-I2V tailchains; preserve user-specified people, story, scene, style, and camera choices without inventing content.
---

# H3 Tailchain Continuity Prompt Writer

Write technically executable prompts for H3 segment chains and package them as the exact JSON consumed by `H3IdentityTailChainLauncher` or `H3IdentityTailChainNativeLauncher`. This skill controls continuity language and packaging only. The user controls all people, plot, actions, setting, styling, dialogue, and shot intent.

## Scope Boundary

- Never invent or substitute characters, relationships, story beats, locations, props, dialogue, mood, or visual style.
- Do not turn an example from an earlier project into a default scenario.
- Preserve the user's requested action. Change only its temporal phrasing, geometry, pacing, and handoff when needed to prevent replay.
- Do not render, queue, upload, or alter a workflow unless the user separately asks.
- For a first segment driven by identity references, preserve the requested Ref2VA contract. For every true tail continuation, treat the extracted previous tail as the actual I2VA frame at 0.00 seconds.
- Default to writing a UTF-8 `sequence.json` file, not a prose-only answer. A prompt-only response is allowed only when the user explicitly asks for one.

## Required Inputs

Obtain or infer only from supplied material:

- requested segment count from 1 through 32;
- either one shared duration or an ordered duration list with one value per segment;
- actual previous tail-frame image or an exact description of it;
- target duration;
- one intended next action or state transition;
- identity, wardrobe, scene, camera, audio, and dialogue constraints the user explicitly wants preserved;
- whether the final state must remain unfinished for the following segment.

Inspect the actual tail image whenever a path or attachment exists. Do not write branching clauses to cover unseen possibilities. If no image is available, state that the opening-state reading is unverified and request a precise pose/contact description only when it is necessary.

Normalize timing as follows:

- Accept `segment_count=N` with `duration_seconds=S` to repeat one duration across all segments.
- Accept `segment_count=N` with `durations=[S1, S2, ... SN]` to assign each segment independently.
- Accept a bare ordered duration list and infer the segment count from its length.
- Require exactly one duration per segment after normalization. Do not silently truncate, pad, or reorder the list.
- Keep every duration between 5 and 15 seconds inclusive; 0.5-second increments are preferred for the local workflow.
- If neither count nor durations are supplied, infer the count from the user's explicit segment plan and default each segment to 10 seconds. State that default in the handoff.
- Derive total duration as the sum of normalized clip durations; do not force the result to a round minute.

## Continuity Method

Before drafting, form a compact state vector from the tail:

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

For a true tail-frame continuation, start exactly with:

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
- Clip 02 and later must also contain `prompt_i2v_en`. This is the primary prompt used by the true first-frame continuation controller.
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

`prompt_i2v_en` follows the three-field I2VA contract above. Do not put the permanent identity image into the `prompt_i2v_en` picture label: for continuation clips, `<Picture 1>` is the actual previous tail frame.

`prompt_cn` translation rules:

- For Clip 01, translate the effective `prompt_en`.
- For Clip 02 and later, translate the effective `prompt_i2v_en`, because that is what the true first-frame controller executes.
- Preserve field names, reference labels, shot labels, timestamps, speaker IDs, language tags, dialogue text, visible text, and special tokens exactly; translate only explanatory prose.
- Keep the same action order, timing, contact points, distances, camera directions, audio policy, and exclusions. Do not summarize, embellish, omit, or reinterpret.
- `prompt_cn` is for review only and must never replace the English execution fields.

Before delivery, run:

```powershell
python scripts/validate_sequence.py --require-cn C:\path\to\sequence.json
```

Resolve a working Python runtime available in the environment. Rewrite the JSON until validation succeeds.

The local launcher has a separate `duration_mode` widget. When clip durations differ, tell the user to set it to `per_clip_json`; otherwise the launcher's `uniform` setting overrides all JSON durations. When all durations are identical, either mode works, but `per_clip_json` remains the direct JSON-controlled choice. Do not claim that varying JSON durations will take effect while the launcher is still in `uniform` mode.

## Multi-Segment Planning

For a requested chain, plan state transitions before writing prose:

```text
segment N start state -> one dominant transition -> segment N tail target
segment N+1 start state -> next dominant transition -> segment N+1 tail target
```

Do not let adjacent segments own the same action. The prior segment owns completion; the next segment starts from the resulting geometry. When the actual render differs from the planned tail, discard the stale next prompt and rewrite it from the real tail image.

For higher reliability, prefer 5–7 seconds per action. When 10 seconds is required, allocate early seconds to the transition and remaining seconds to a non-reversing settle or hold.

## Delivery

Write the finished JSON to the user-specified directory. If no directory is supplied, create a clearly named project folder under the active video workspace and save it as `sequence.json`. Return the clickable file path, clip count, ordered duration list, total duration, validation result, and concise risk flags only when ambiguity remains. Explicitly report whether the launcher should use `uniform` or `per_clip_json`. Do not paste the full JSON into chat unless the user asks to preview it.

Before delivery, verify:

- the prompt begins from the actual tail rather than the planned tail;
- no quarantined completed-action term remains, including in negatives;
- the first two seconds contain a single explicit motion direction;
- no forward motion is followed by its inverse;
- there is only one dominant transition;
- the ending can serve as an unambiguous next first frame;
- no story or scene content was added beyond the user's request.
- the saved document parses as JSON and passes `scripts/validate_sequence.py`.
- every clip includes a faithful `prompt_cn` translation of the prompt actually executed for that clip.
