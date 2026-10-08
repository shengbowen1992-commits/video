#!/usr/bin/env python3
"""Statically validate the default Plan 5 tail-lineart prompt contract and state-lock marker without echoing prompt text."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from validate_story_segments import reject_constant, unique_object, validate_data


HEADINGS = (
    "subject_definitions:",
    "summary:",
    "retention_analysis:",
    "detailed_description:",
    "overall_soundscape:",
    "non_diegetic_music:",
)


def validate_tailchain_data(data: object) -> int:
    count = validate_data(data)
    assert isinstance(data, dict)
    segments = data["segments"]
    assert isinstance(segments, list)

    for index, segment in enumerate(segments, 1):
        prompt = segment["prompt"]
        prefix = f"segment {index}: "

        positions = []
        for heading in HEADINGS:
            occurrences = prompt.count(heading)
            if occurrences != 1:
                raise ValueError(prefix + f"{heading} must appear exactly once")
            positions.append(prompt.find(heading))
        if positions != sorted(positions):
            raise ValueError(prefix + "six prompt headings must appear in the required order")

        for reference in ("<Picture 1>", "<Picture 2>"):
            if reference not in prompt:
                raise ValueError(prefix + f"missing required identity reference {reference}")

        state_lock_count = prompt.count("Continuity State Lock:")
        if state_lock_count != 1:
            raise ValueError(prefix + "Continuity State Lock: must appear exactly once")

        detailed_pos = prompt.find("detailed_description:")
        shot1_pos = prompt.find("[Shot 1]")
        lock_pos = prompt.find("Continuity State Lock:")
        if not (detailed_pos < lock_pos < shot1_pos):
            raise ValueError(prefix + "Continuity State Lock: must appear inside detailed_description before [Shot 1]")

        if index == 1:
            if "<Picture 3>" in prompt:
                raise ValueError(prefix + "must not mention Picture 3 in the default tail-lineart profile")
        elif "<Picture 3>" not in prompt:
            raise ValueError(prefix + "must reference previous-tail lineart <Picture 3>")

        if "<Video 1>" in prompt:
            raise ValueError(prefix + "must not reference Video 1 in the default Plan 5 tail-lineart profile")

    return count


def validate(path: Path) -> int:
    with path.open(encoding="utf-8-sig") as handle:
        data = json.load(
            handle,
            object_pairs_hook=unique_object,
            parse_constant=reject_constant,
        )
    return validate_tailchain_data(data)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    args = parser.parse_args(argv)
    try:
        count = validate(args.path)
    except json.JSONDecodeError as exc:
        print(f"INVALID: JSON syntax at line {exc.lineno}, column {exc.colno}", file=sys.stderr)
        return 1
    except (OSError, UnicodeError) as exc:
        print(f"INVALID: cannot read UTF-8 JSON ({type(exc).__name__})", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1

    print(
        f"VALID: segments={count}, static_prompt_contract=true, "
        "semantic_continuity_validated=false, render_quality_validated=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
