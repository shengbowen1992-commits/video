#!/usr/bin/env python3
"""Validate sequence.json for the local H3 identity-tailchain controllers."""

from __future__ import annotations

import json
import sys
from pathlib import Path


I2V_FIRST_LINE = (
    "For the target video, at 0.00 seconds into the target video, "
    "<Picture 1> (from [Shot 1]) is fully referenced."
)
I2V_FIELDS = (
    "integrated_multimodal_description:",
    "overall_soundscape:",
    "non_diegetic_music:",
)
REF_FIELDS = (
    "subject_definitions:",
    "summary:",
    "retention_analysis:",
    "detailed_description:",
    "overall_soundscape:",
    "non_diegetic_music:",
)


def fail(message: str) -> None:
    raise ValueError(message)


def ordered(text: str, labels: tuple[str, ...]) -> bool:
    cursor = -1
    for label in labels:
        cursor = text.find(label, cursor + 1)
        if cursor < 0:
            return False
    return True


def validate_data(data: dict, require_cn: bool = False) -> tuple[int, float]:
    if data.get("version") != 3:
        fail("version must be 3")
    sets = data.get("sets")
    if not isinstance(sets, list) or not sets:
        fail("sets must be a nonempty array")
    first_set = sets[0]
    if not isinstance(first_set, dict) or not str(first_set.get("set_id", "")).strip():
        fail("sets[0].set_id must be nonempty")
    clips = first_set.get("clips")
    if not isinstance(clips, list) or not 1 <= len(clips) <= 32:
        fail("sets[0].clips must contain 1 to 32 clips")

    total = 0.0
    for index, clip in enumerate(clips, start=1):
        if not isinstance(clip, dict):
            fail(f"clip {index:02d} must be an object")
        expected_id = f"{index:02d}"
        if str(clip.get("clip_id", "")) != expected_id:
            fail(f"clip {index:02d} clip_id must be {expected_id}")
        prompt_en = str(clip.get("prompt_en", "")).strip()
        if not prompt_en:
            fail(f"clip {index:02d} is missing prompt_en")
        if not ordered(prompt_en, REF_FIELDS):
            fail(f"clip {index:02d} is missing ordered Ref2VA fields in prompt_en")
        if require_cn and not str(clip.get("prompt_cn", "")).strip():
            fail(f"clip {index:02d} is missing prompt_cn")
        try:
            duration = float(clip.get("duration_seconds"))
        except (TypeError, ValueError):
            fail(f"clip {index:02d} has invalid duration_seconds")
        if not 5.0 <= duration <= 15.0:
            fail(f"clip {index:02d} duration_seconds must be between 5 and 15")
        total += duration

        if "seed" in clip and clip["seed"] is not None:
            seed = int(clip["seed"])
            if not 0 <= seed < 2**63:
                fail(f"clip {index:02d} seed must be in [0, 2^63)")

        if index >= 2:
            i2v = str(clip.get("prompt_i2v_en", "")).strip()
            if not i2v:
                fail(f"clip {index:02d} is missing prompt_i2v_en")
            if i2v.splitlines()[0].strip() != I2V_FIRST_LINE:
                fail(f"clip {index:02d} has an invalid I2VA first line")
            if not ordered(i2v, I2V_FIELDS):
                fail(f"clip {index:02d} is missing ordered I2VA fields")

    return len(clips), total


def validate(path: Path, require_cn: bool = False) -> tuple[int, float]:
    with path.open("r", encoding="utf-8-sig") as handle:
        data = json.load(handle)
    return validate_data(data, require_cn=require_cn)


def main() -> int:
    arguments = list(sys.argv[1:])
    require_cn = False
    if "--require-cn" in arguments:
        arguments.remove("--require-cn")
        require_cn = True
    if len(arguments) != 1:
        print("usage: validate_sequence.py [--require-cn] PATH_TO_SEQUENCE_JSON", file=sys.stderr)
        return 2
    path = Path(arguments[0]).resolve()
    try:
        count, total = validate(path, require_cn=require_cn)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1
    print(
        f"VALID: clips={count}, total_seconds={total:g}, "
        f"prompt_cn_required={require_cn}, path={path}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
