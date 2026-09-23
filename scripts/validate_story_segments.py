#!/usr/bin/env python3
"""Validate only the dynamic-series JSON envelope, without displaying prompt text."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def validate_data(data: object) -> int:
    if not isinstance(data, dict) or set(data) != {"global_prompt", "segments"}:
        raise ValueError("root must contain exactly global_prompt and segments")
    if data["global_prompt"] != "":
        raise ValueError("global_prompt must be an empty string in raw mode")
    segments = data["segments"]
    if not isinstance(segments, list) or not segments:
        raise ValueError("segments must be a nonempty array")
    required = {"id", "title", "raw_prompt", "prompt"}
    for index, segment in enumerate(segments, 1):
        prefix = f"segment {index}: "
        if not isinstance(segment, dict):
            raise ValueError(prefix + "must be an object")
        if not required <= set(segment) or set(segment) - required - {"seed"}:
            raise ValueError(prefix + "requires id, title, raw_prompt, prompt; only seed is optional")
        if type(segment["id"]) is not int or segment["id"] != index:
            raise ValueError(prefix + "id must be a consecutive integer starting at 1")
        if segment["raw_prompt"] is not True:
            raise ValueError(prefix + "raw_prompt must be boolean true")
        for field in ("title", "prompt"):
            if not isinstance(segment[field], str) or not segment[field].strip():
                raise ValueError(prefix + field + " must be a nonempty string")
        if "seed" in segment:
            seed = segment["seed"]
            if type(seed) is not int or not 0 <= seed < 2**63:
                raise ValueError(prefix + "seed must be an integer in [0, 2^63)")
    return len(segments)


def unique_object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON object key")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise ValueError("non-standard JSON numeric constant")


def validate(path: Path) -> int:
    with path.open(encoding="utf-8-sig") as handle:
        data = json.load(handle, object_pairs_hook=unique_object, parse_constant=reject_constant)
    return validate_data(data)


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
    print(f"VALID: segments={count}, envelope_only=true, prompt_content_validated=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
