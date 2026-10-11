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

## Identity Preservation Contract and Hairstyle Geometry Gate

Pictures 1/2 are the only permanent identity and hairstyle authority. Picture 3 contributes prior-tail geometry and motion phase and may affect temporary pose, expression, and local motion state, including pose/body deformation and expression-driven soft-tissue deformation, but it cannot redefine permanent identity features such as facial identity, identity-specific facial structure, hairstyle geometry, skin tone, body proportions or other stable appearance traits. Prompt text is supplementary state only and cannot override reference-image identity. Resolve conflicts as identity > geometry > supplementary text, correcting the lower-priority handoff geometry or mutable-state wording as needed. Compare rendered identity against face shape and facial proportions beneath the current expression; eye shape, spacing and characteristic gaze; nose shape, lips and jaw contour; skin tone and distinctive features; height ratio, shoulder width, build silhouette and apparent adult age. Reject a continuation that swaps, averages, beautifies, stylizes, redesigns or generates a similar-but-different person even when expression, pose and motion continuity are acceptable.

Treat hairstyle geometry as part of identity. Preserve hair color, length, density, root placement, crown contour, parting line and location, bangs/forehead fringe, tied-versus-loose state, overall silhouette, main volume distribution and principal face-framing locks. Natural movement may affect hair ends, a few loose strands and gravity-driven settling, but motion changes hair position rather than hairstyle structure; it must not move the roots or parting line, alter the crown contour, change length/bangs, switch tied/loose state or redistribute the main volume unless the user explicitly requested that hairstyle transition.

## Reference Detail Preservation Contract

Compare more than the broad face category. Preserve supported facial asymmetry, distinctive feature shape and spacing, characteristic skin features, natural proportions, hairstyle texture, and other visible personal traits that distinguish Pictures 1/2 from an averaged substitute. Reject idealized symmetry, generic beauty-template normalization, influencer-style face conversion, standardized feature proportions, or uniformly perfected skin.

This gate is evidence-bound: preserve only details the identity reference resolves clearly. Do not manufacture freckles, scars, moles, pores, asymmetry, or hair texture to make the output appear more distinctive. If the source is too small, blurred, occluded, or overprocessed to verify a detail, report that limitation instead of inventing it.

## Prompt Placement

Put the clarity and exposure target where H3 uses it:

- `subject_definitions`: identify the referenced subject and the appearance features supplied by its actual source; do not invent source features to express a desired quality target.
- `retention_analysis`: for each defined reference, identify which actual exposure, skin tone, focus, white balance, opening framing, or lighting features are retained, using the appropriate relationship marker. Newly requested lighting is not automatically a preserved reference attribute.
- `detailed_description` or `integrated_multimodal_description`: put the global clarity/exposure target here, then describe the visible key light, controlled movement, simple camera behavior, and stable final handoff interval. Keep scene-wide constraints out of `summary` and out of unrelated retention entries.

For the complete section-placement rules, read [ref2va-prompt-contract.md](ref2va-prompt-contract.md).

Repeat the essential clarity/exposure sentence in every clip. Do not assume the first clip's lighting instruction will survive a long chain.

Within the default production style, preserve the requested mood through artificial-light color and fixture choice while keeping the room and face bright; never introduce daylight to imply time of day. When the user explicitly overrides the bright minimal-interior style for a night or dim interior, retain that environment but add a motivated soft key or practical light on the face rather than silently turning it into daylight. Prefer `cleanly and evenly exposed face with retained highlight and shadow detail` over vague words such as `cinematic`, which can encourage crushed shadows.

## Live Action Quality Standard

Unless the user requests a stylized or CGI look, require sharp eyes, stable facial proportions, clear skin detail, realistic lens perspective, natural depth of field, and optically credible focus changes. Keep one coherent photographic language through the chain: cinematic clarity, stable exposure, white balance, lens perspective, depth-of-field behavior, contrast response, natural motion-blur character, sharpness response, focus behavior and color rendering. Depth of field must behave like a real lens, and motion blur must follow subject/camera movement without erasing identity-critical face structure. Reject AI face drift, inconsistent sharpness, artificial skin smoothing, unmotivated lens-style changes, illustration-like rendering, game-engine sheen, waxy/plastic skin or blurred facial detail.

### Visual Quality and Material Realism Gate

Preserve one lighting and color-science system across seams: source direction, softness, color-temperature tendency, exposure, white balance, contrast, color response, natural highlight roll-off and readable shadow layers. Skin retains natural pores and microtexture, fine tonal variation, restrained micro-specular response and a subtle natural subsurface response.

Keep materials already present in the scene optically distinct rather than applying one generic reflection model:

- silk: soft directional sheen;
- cotton: comparatively diffuse response;
- leather: broader controlled highlights;
- metal: sharper reflections;
- stone: dense, mostly matte response with restrained specularity;
- glass: coherent transparency, refraction and controlled reflections.

These examples guide rendering of materials already present; they do not authorize adding wardrobe, props or surfaces.

## Temporal Consistency Contract

Review every accepted Segment in motion and across its full seam interval. Preserve the same lens character, color science, skin-rendering behavior, identity appearance, facial-detail response, hairstyle structure, and material response unless the user explicitly requested a visible transition.

Reject face morphing, identity drift, inconsistent skin texture, unmotivated lens-style changes, temporal flicker, frame-to-frame detail instability, or gradual rendering-style drift. A stable selected frame does not pass this gate when the moving face, hair, skin detail, lens response, or material appearance fluctuates before or after it.

## Bright Windowless Minimal-Interior Gate

Unless the user explicitly overrides the production style, treat the following as a package-level invariant rather than an optional mood suggestion:

- every scene is an enclosed interior with no visible windows, skylights, glass exterior walls, or daylight openings;
- lighting comes only from bright, soft, even artificial fixtures and face-oriented key/fill sources, never sunlight, daylight, moonlight, or window light;
- doors, walls, trim, cabinets, and furniture use warm white, off-white, light beige, or light neutral gray, with plain surfaces, simple lines, sparse decoration, and an uncluttered layout;
- dark wood dominance, ornate doors, heavy furniture, saturated walls, deep shadowy corners, and busy decorative patterns are excluded unless explicitly requested;
- the artificial-light direction, color temperature, exposure, light neutral palette, and minimalist furnishing style remain stable across every seam.

Every English execution prompt must contain this exact canonical sentence:

`The setting is an enclosed windowless interior with no visible windows and no natural light. It is illuminated only by bright, soft, even artificial lighting. Doors, walls, and furniture are light-colored, plain, and minimalist.`

Record the policy in the root `scene_style` object and validate it with `--require-bright-minimal-interior`. During visual QC, reject a clip before continuation when a window, daylight spill, dark heavy decor, or ornate furniture appears. Do not hide a violating literal tail by describing a sudden replacement background in the next prompt; rerender the first bad clip or obtain an explicit user override.

## Motion and Framing

When facial clarity is the priority:

- favor medium and medium-close front or three-quarter views at important moments;
- keep one dominant subject transition per clip;
- avoid rapid head turns during important expressions or dialogue;
- avoid stacking fast walking, arm motion, hair motion, and a strong camera move;
- for one-time transitions, settle the final 0.75-1.0 seconds into low-velocity motion with stable focus and lighting. For user-requested sustained cyclic motion, preserve the requested cadence and cycle phase while keeping the literal tail clear, focused, and evenly lit; do not force a pause or slow playback.

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
- a visible window, daylight or sunlight contribution, dark/heavy wall or furniture treatment, or ornate/busy decor when the bright minimal-interior contract is active.
- facial proportion, eye/nose/lip/jaw, height/shoulder/build or hairstyle-geometry drift from Pictures 1/2.
- visual-style drift, physically implausible depth of field or motion blur, clipped highlight roll-off, crushed shadow layers, plastic skin, or one generic shine applied across different materials.

Use face-region measurements when available. Compare luminance and sharpness against the identity reference and the first accepted clip rather than relying on one universal threshold. Automated scores are triage signals; accept only after visual inspection of the decoded face and the seam interval.

Do not repair a failed generation only with super-resolution, sharpening, or global exposure gain. Those operations may improve presentation after acceptance, but cannot recreate missing facial structure or remove temporal motion smear.
