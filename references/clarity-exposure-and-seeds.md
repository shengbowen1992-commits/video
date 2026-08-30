# H3 Face Clarity, Exposure, and Seed Guidance

Read this reference when a user prioritizes bright clear people, reports dark or soft results under the same workflow, asks how to set seeds, or authorizes rendering/rerendering/QC.

## Diagnose the Failure Pattern

Classify the visible symptom before changing anything:

- Dark from frame 1: inspect the permanent reference, actual starting tail, scene lighting language, and seed.
- Darkens from clip to clip: treat it as tail-conditioned exposure drift. Stop before the next clip and repair the first bad handoff.
- Sharp while still but soft during movement: reduce simultaneous subject and camera motion; this is temporal motion quality, not an output-resolution problem.
- Soft even while still: inspect face size, source-reference detail, focus language, seed, and generated base resolution.
- ComfyUI preview is bright but the encoded file is dark: compare decoded frames and inspect color range/transfer metadata before changing prompts.
- A standalone reference-like face appears at a planned close-up: inspect `face-only`, `isolate the face`, portrait framing, and instructions that remove every other subject from view.
- A reference-like face flashes for one frame at a clip boundary: inspect permanent-reference versus previous-tail label mapping and first-frame anchoring.
- A reference-like portrait occupies most of a segment: inspect over-strong identity conditioning, ambiguous picture authority, and the segment seed after fixing the prompt roles.

Do not diagnose from workflow names or settings alone. Inspect decoded frames from the actual output.

## Reference-Face Takeover Gate

The permanent reference supplies facial identity, not a replacement shot. In every Ref2VA continuation, state that the permanent reference cannot contribute its pose, crop, framing, background, lighting, camera angle, or portrait composition. The actual previous tail owns the current scene geometry and opening composition.

Do not use `face-only close-up`, `isolate her/his face`, `the other subject is completely outside frame`, or similar language merely to obtain a clear expression. Use a contextual medium-close view and retain at least one current-scene anchor such as the existing shoulder/contact geometry, the other subject's established screen-side presence, or a recognizable background element.

During rendered QC, distinguish three failure locations:

- Mid-clip at the requested close-up time: prompt-induced reference takeover.
- Exactly at the seam for one or a few frames: reference/tail mapping or anchoring failure.
- Most of the clip: excessive reference authority or an unlucky seed after the prompt roles are already correct.

Reject an unrequested standalone reference-like portrait before extracting the next tail. Prompt-role repair comes before seed replacement or lowering reference strength.

## Export and Color-Metadata Gate

Separate generated exposure from export behavior with a decoded-frame comparison:

1. Compare the same source and exported interval after decoding, not screenshots from two players.
2. Measure face-region exposure when available and whole-frame luma only as supporting evidence.
3. Inspect `pix_fmt`, `color_range`, `color_space`, `color_transfer`, and `color_primaries` with `ffprobe`.
4. If decoded luma is stable but players disagree, treat missing or inconsistent color metadata as the leading cause.
5. If decoded luma changes systematically after encoding, inspect range conversion and scale/filter parameters before touching prompts.

For ordinary SDR delivery, preserve the source range and write consistent Rec.709 primaries, transfer, and matrix metadata when the encoder supports it. Mark TV/limited versus PC/full range only when the pixel values actually use that range; changing a tag without a matching conversion creates a new brightness error. Verify the result by decoding it again.

Avoid unnecessary lossy H.264 passes. When all completed clips have compatible codec parameters and timestamps can be normalized safely, prefer a verified stream-copy concat. If a final re-encode is required, encode once at the delivery boundary rather than repeatedly transcoding accepted clips. Re-encoding can soften fine facial detail even when average brightness remains unchanged.

## Input Quality Gate

The permanent identity reference should show an unobstructed, in-focus, naturally exposed face with enough pixel area to resolve the eyes, nose, mouth, and face outline. Reject a reference whose identity-critical face is tiny, strongly compressed, clipped, heavily beautified, motion-blurred, hidden by hair or hands, or dominated by backlight unless the user explicitly accepts the risk.

For continuation clips, the actual tail carries geometry and lighting. Preserve it only if the handoff face remains readable and the intended scene exposure has not drifted. Never claim an earlier nearby frame is the exact tail. If literal-tail continuity is required and the tail fails, rerender the preceding clip.

## Prompt Placement

Put the clarity and exposure target where H3 uses it:

- `subject_definitions`: keep the face unobstructed and identity features resolvable.
- `retention_analysis`: preserve face exposure, natural skin tone, focus, white balance, framing scale, and lighting direction.
- `detailed_description` or `integrated_multimodal_description`: describe the visible key light, controlled movement, simple camera behavior, and stable final handoff interval.

Repeat the essential clarity/exposure sentence in every clip. Do not assume the first clip's lighting instruction will survive a long chain.

Use lighting that fits the requested scene. For night or dim interiors, retain the dark environment but add a motivated soft key or practical light on the face; do not silently turn the scene into daylight. Prefer `cleanly and evenly exposed face with retained highlight and shadow detail` over vague words such as `cinematic`, which can encourage crushed shadows.

## Motion and Framing

When facial clarity is the priority:

- favor medium and medium-close front or three-quarter views at important moments;
- keep one dominant subject transition per clip;
- avoid rapid head turns during important expressions or dialogue;
- avoid stacking fast walking, arm motion, hair motion, and a strong camera move;
- settle the final 0.75-1.0 seconds into low-velocity motion with stable focus and lighting.

A distant full-body figure cannot retain the same facial detail as a medium-close face at the same output resolution. Do not promise otherwise.

## Seed Selection and Rerendering

Use one fixed, recorded seed for each clip. Different clips should normally use different seeds; the permanent identity reference and previous-tail reference provide continuity, while fixed per-clip seeds provide reproducibility.

Recommended procedure:

1. Resolve and record the complete seed list before rendering.
2. Render clip 1 and accept it only after checking opening, midpoint, and final handoff frames.
3. Render each next clip from the accepted literal tail and its own recorded seed.
4. If a clip is dark or soft but its action and geometry are otherwise correct, rerun that clip with two to four alternate seeds, changing no other variable during the seed comparison.
5. Lock the accepted seed and discard downstream results based on any rejected tail.

Do not use a new random seed on every retry without recording it. That makes improvements non-reproducible and prevents an honest comparison. Do not change prompt, seed, sampler, and step count simultaneously when trying to identify the cause.

Using the same seed for every clip is not a general consistency control. Because prompts and tail inputs change, an identical seed does not guarantee matching identity or lighting and may repeat unwanted composition or motion tendencies. Reserve same-seed reuse for an explicit experiment or for A/B tests where input, prompt, and settings are otherwise identical.

## Rendered-Output Quality Gate

When rendering or QC is authorized, inspect each clip at minimum at the opening, midpoint, and within the final 0.75 seconds. Reject or flag a clip before continuation when any identity-critical face has:

- crushed facial shadows or clipped facial highlights;
- materially darker exposure than the accepted reference/preceding clip without story justification;
- defocus or motion smear that removes the eyes, mouth, or face outline;
- strong haze, bloom, ghost trails, double edges, or frame-to-frame exposure pumping;
- a final tail that is worse than the clip midpoint and unsuitable to seed the next clip.
- an unrequested standalone face or portrait that reproduces the permanent reference's crop, pose, background, or lighting instead of the active scene.

Use face-region measurements when available. Compare luminance and sharpness against the identity reference and the first accepted clip rather than relying on one universal threshold. Automated scores are triage signals; accept only after visual inspection of the decoded face and the seam interval.

Do not repair a failed generation only with super-resolution, sharpening, or global exposure gain. Those operations may improve presentation after acceptance, but cannot recreate missing facial structure or remove temporal motion smear.
