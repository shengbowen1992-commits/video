# H3 LoRA Routing

This reference is the optional runtime-adapter layer for MiniMax H3 prompt work in this repository. It is used only when the user explicitly supplies LoRAs, asks for LoRA recommendations/routing, or the active workflow already has LoRA slots that must be configured.

The core tailchain skill remains renderer-neutral. Do **not** invent LoRAs, download files, change sampler/scheduler, or add adapter settings when the user did not ask for them.

> Metadata snapshot: 2026-10-08. External model cards can change. Re-check the source page before treating a version, filename, trigger, or author-published strength as current.

## 1. Separate three kinds of information

Never mix these categories:

1. **Author-published metadata** — filename, trigger word, supported mode, strength range, sampler/scheduler notes.
2. **Project starting point** — conservative values chosen for this repository's multi-LoRA Ref2VA stack. These are empirical defaults, not author claims.
3. **Per-segment routing** — which adapters are enabled for the current action and why.

When documenting a value, label it clearly if it is only a project starting point.

## 2. Current adapter registry

### fal MiniMax H3 Realism People

Source: https://huggingface.co/fal/MiniMax-H3-Realism-People-LoRA

- File: `h3-realism-people-t2v-i2v-r2v.safetensors`
- Role: realistic people, skin texture, faces, expressions, film-style lighting/camera behavior.
- Supported by the published model card for T2V, I2V and Ref2V/Ref2VA-style use.
- Trigger: `r34l1sm`
- Author-published strength: 1.0 intended; 0.6–0.8 for a lighter touch.
- Prompt placement: the author explicitly says to start the prompt with `r34l1sm`.
- Project multi-stack starting point: **0.50–0.70**, normally **0.50 or 0.60** when several other LoRAs are active. Raise only after checking identity, skin texture and motion artifacts.

If this LoRA is loaded for a segment, put `r34l1sm` in the actual executed prompt. Do not hide it only in a JSON field that the renderer ignores.

### AfterMidnight MiniMax H3 NSFW — Ref2VA

Source: https://huggingface.co/Scorpio1111/AfterMidnight-MiniMax-H3-NSFW

- Role: main Ref2VA adult-motion/coherence layer.
- Mode: the published card describes it as a Ref2VA LoRA.
- Flavor: `sexytime`
  - Author-published strength: **1.0**
  - Intended emphasis: sex scenes and coherent motion.
- Flavor: `softer`
  - Author-published strength: **0.8–1.0**
  - Intended emphasis: detail/stability more than motion.
- Use **one flavor at a time**.
- Published workflow warning: use **Euler sampler + beta scheduler** for this adapter; the card warns that other choices can cause audio problems.
- No fixed trigger word is documented on the retrieved model card.
- Project multi-stack starting point:
  - `sexytime`: **0.75–0.90**, normally **0.80**.
  - `softer`: **0.80–1.00** when stability/detail is preferred.

Treat AfterMidnight as a **main-motion layer**. Do not automatically stack it at high strength with another broad adult-motion LoRA.

### HMNSFW V2.5 AIO

Source: https://huggingface.co/Hearmeman/minimax-h3-loras

- File: `HMNSFW-AIO-V2.5.safetensors`
- Role: broad adult-action/motion adapter.
- Trigger: `hmmotion`
- Author-published strength: **0.5–0.9**
- Project starting point when used as the main-motion alternative: **0.65–0.75**, normally **0.70**.

Default policy: **AfterMidnight sexytime OR HMNSFW V2.5** is the main-motion layer. Do not run both high unless deliberately performing an A/B or controlled stack test.

### HMPenis v1.0

Source: https://huggingface.co/Hearmeman/minimax-h3-loras

- File: `HMPenis_v2_e35.safetensors`
- Role: male anatomy.
- Trigger: `HMPenis`, preferably leading/early in the relevant prompt prose.
- The published table does not give one fixed strength; the repository guidance says adapters with a blank value can be started at 1.0 and pulled back.
- Published notes recommend specifying camera direction such as front/POV-like, back, or side when relevant.
- Project multi-stack starting point: **0.50–0.65**, normally **0.55**.

Enable only in segments where the requested framing/action actually benefits from that anatomy adapter. Do not put the trigger into unrelated early segments merely because the LoRA exists in the workflow.

### HMPussy V1

Source: https://huggingface.co/Hearmeman/minimax-h3-loras

- File: `Vagina_minimax-h3_epoch20.safetensors`
- Role: female anatomy.
- Trigger: `pussy`
- Author-published strength: **1.0**
- Project multi-stack starting point: **0.50–0.70**, normally **0.60**, then raise only if the anatomy benefit outweighs identity/texture interference.

Enable only in segments where the requested framing/action benefits from the adapter. It does not need to be active in kissing, clothing transition, or other unrelated shots.

### HMBreasts V2

Source: https://huggingface.co/Hearmeman/minimax-h3-loras

- File: `HMBreastsV2.safetensors`
- Role: chest/breast anatomy/detail.
- Current published trigger: `tits`, written in ordinary prose.
- No single fixed strength was published in the retrieved table; use the source's general guidance to start stronger when isolated and pull back in a multi-LoRA stack.
- Use only when chest anatomy/detail is actually important. Motion/secondary-body response still comes from the base model, motion layer and prompt; this adapter is not a substitute for V18 motion language.

### Mystic XXX V4 Ref2VA

Release reference: https://civarchive.com/models/2856467?modelVersionId=3266628

- Use the dedicated **Ref2VA** V4 file, not merely a similarly named non-Ref2VA file.
- Role: optional adult/anatomy Ref2VA enhancement.
- Release notes describe the Ref2VA file as experimental and state that no audio was trained for that file.
- Published recommended range: **0.2–1.0**; the author reports using V4 at 1.0.
- No fixed trigger word is documented in the retrieved V4 release notes.
- Project multi-stack starting point: **0.15–0.30**, normally **0.20**, because this repository prioritizes dual-identity retention and Picture 3 continuity over maximum adapter influence.

Mystic is optional. If identity, anatomy ownership, audio behavior, or temporal stability degrades, disable Mystic first or reduce it before weakening the permanent identity references.

## 3. Conceptual stack order

Use this as a routing/debugging order, not as a claim that every loader mathematically depends on physical node order:

1. **Anatomy specialization** — HMPenis / HMPussy / HMBreasts when relevant.
2. **One main-motion layer** — AfterMidnight *or* HMNSFW.
3. **Optional Ref2VA enhancer** — Mystic V4 Ref2VA at conservative strength.
4. **Realism/people layer** — fal Realism People.

Example project baseline:

```text
HMPenis                  0.55   # only relevant segments
HMPussy V1               0.60   # only relevant segments
AfterMidnight sexytime   0.80   # main motion
Mystic V4 Ref2VA         0.20   # optional
Realism People           0.50   # r34l1sm
```

The real requirement is **role separation** and controlled total influence. If the implementation merges all LoRAs additively, physical loader order may have little or no semantic effect; use the order above mainly for workflow readability, toggling, and fault isolation.

## 4. Dynamic segment routing

Do not enable every adapter merely because it is installed.

For the current two-identity tail-lineart workflow, a useful default pattern is:

| Segment/action type | Main motion | Anatomy | Optional enhancer | Realism trigger |
| --- | --- | --- | --- | --- |
| kissing / non-genital foreplay / clothing transition | AfterMidnight sexytime 0.75–0.85 | none unless clearly needed | Mystic 0–0.20 | `r34l1sm` |
| oral action centered on male anatomy | AfterMidnight sexytime 0.75–0.85 | HMPenis 0.50–0.65 | Mystic 0–0.20 | `r34l1sm` |
| penetrative action where both anatomies need reinforcement | AfterMidnight sexytime 0.75–0.90 | HMPenis 0.50–0.65 + HMPussy 0.50–0.70 | Mystic 0–0.20 | `r34l1sm` |
| identity-critical close-up / stability test | AfterMidnight softer 0.8–1.0 or reduce main motion | only the minimum needed | usually off first | `r34l1sm` |
| HMNSFW A/B alternative | HMNSFW V2.5 0.65–0.75 | same anatomy routing | Mystic conservative/off | `r34l1sm` + `hmmotion` |

These are **project starting points**, not guarantees. Keep seed, base model, resolution, sampler/scheduler and prompt fixed when comparing one LoRA change.

## 5. Trigger routing

Triggers must appear in the actual prompt consumed by H3 when the corresponding adapter requires them.

Current verified triggers:

```text
Realism People  -> r34l1sm
HMNSFW V2.5     -> hmmotion
HMPenis         -> HMPenis
HMPussy V1      -> pussy
HMBreasts V2    -> tits
```

No fixed trigger is currently documented in the retrieved model-card/release text for:

```text
AfterMidnight sexytime / softer
Mystic XXX V4 Ref2VA
```

For fal Realism People, prefer putting `r34l1sm` at the start of the complete executed prompt because that is the author's documented usage.

For HMPenis/HMPussy/HMBreasts/HMNSFW, place the trigger in natural prompt text near the relevant action/anatomy context. A helper line such as `LoRA trigger cues: ...` is a project authoring convention only; it is not an H3 protocol field. Use it only if the full line is actually passed through to the model.

## 6. Prompt/state interaction

LoRA routing must not override continuity authority:

1. Picture 1/2 keep permanent identity.
2. Picture 3 keeps opening geometry/action phase.
3. text keeps current non-geometric state.
4. LoRAs bias motion/anatomy/appearance only.

A LoRA never authorizes:

- restoring a removed garment;
- changing the number or ownership of body parts;
- replacing a permanent identity;
- restarting a completed one-time transition;
- ignoring the accepted previous tail;
- inventing a new action that the prompt did not request.

When a terminal state is locked, continue using the parent skill's terminal-state vocabulary isolation. Do not reintroduce obsolete clothing/prop vocabulary merely because an anatomy or realism LoRA is active.

## 7. Failure isolation

When output quality degrades, change **one layer at a time**.

Recommended order:

1. Disable/reduce Mystic first.
2. Reduce anatomy adapters that are not essential to the current shot.
3. Reduce the main-motion adapter if motion becomes incoherent or identity drifts.
4. Adjust realism last if the problem is specifically skin/face texture, lighting feel, or excess documentary motion.
5. If using AfterMidnight, verify Euler + beta before blaming the prompt for audio anomalies.
6. Keep seed/prompt/base workflow fixed during an A/B comparison.

Typical symptoms:

- **identity drift** → reduce optional enhancer, then anatomy, then main-motion strength.
- **anatomy over-emphasis in unrelated shots** → disable that anatomy adapter and remove its trigger from those segments.
- **plastic skin** → verify Realism People is loaded and `r34l1sm` is present; test 0.6–0.8 before adding more LoRAs.
- **motion too weak** → first increase the one selected main-motion layer and apply V18 concrete cadence/amplitude language; do not solve it by stacking every motion LoRA.
- **motion too chaotic** → lower main-motion strength or use AfterMidnight softer; do not compensate with more negative prompt clutter.
- **audio anomaly with AfterMidnight** → verify the published Euler + beta requirement.

## 8. Repository boundary

Do not write runtime LoRA lists or strengths into `story_segments.json` outer fields unless the consuming workflow explicitly supports such fields. The current story JSON schema does not.

Prompt triggers may appear in the existing six-section prompt string when they are required by the active adapter. Actual adapter file selection, node wiring, strength, sampler and scheduler remain workflow/runtime configuration unless a separate controller schema explicitly supports them.

When a user asks only for prompt/JSON authoring and has not selected LoRAs, do not force this reference into the task.
