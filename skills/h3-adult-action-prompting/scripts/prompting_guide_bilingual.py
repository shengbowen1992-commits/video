#!/usr/bin/env python3
"""
Build the bilingual prompting-guide source library for h3-adult-action-prompting.

Source:
  https://huggingface.co/NSFW-API/NSFW_Wan_1.3b/resolve/main/prompting-guide.json

The source SHA-256 is pinned to the user's uploaded prompting-guide(1).json:
  8f1693636c7928248aaa241f4db7315e8da132b642ac498f25e385a6f1fb178c

Modes:
  translate-shard --shard N --shard-size 100 --output DIR
  merge --shards-dir DIR --repo-root DIR --shard-size 100

The English source is preserved byte-for-byte after SHA validation.
The Chinese file keeps the same top-level keys and ordering while translating
the explanatory value strings into Simplified Chinese.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
from collections import OrderedDict
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import requests

SOURCE_URL = (
    "https://huggingface.co/NSFW-API/NSFW_Wan_1.3b/"
    "resolve/main/prompting-guide.json"
)
SOURCE_SHA256 = "8f1693636c7928248aaa241f4db7315e8da132b642ac498f25e385a6f1fb178c"
SKILL_REL = Path("skills/h3-adult-action-prompting")
SOURCE_REL = SKILL_REL / "references" / "source"


def download_source() -> bytes:
    r = requests.get(SOURCE_URL, timeout=120)
    r.raise_for_status()
    data = r.content
    digest = hashlib.sha256(data).hexdigest()
    if digest != SOURCE_SHA256:
        raise RuntimeError(
            "Source prompting-guide.json SHA-256 mismatch. "
            f"Expected {SOURCE_SHA256}, got {digest}. "
            "Refusing to translate a source that differs from the user's uploaded file."
        )
    return data


def load_source() -> Tuple[bytes, OrderedDict]:
    raw = download_source()
    obj = json.loads(raw.decode("utf-8"), object_pairs_hook=OrderedDict)
    if not isinstance(obj, dict):
        raise TypeError("Expected a top-level JSON object.")
    if len(obj) != 1268:
        raise RuntimeError(f"Expected 1268 top-level entries, got {len(obj)}.")
    return raw, obj


def split_for_translation(text: str, limit: int = 4200) -> List[str]:
    """Split decoded value text into translation-safe chunks."""
    if len(text) <= limit:
        return [text]

    # Prefer paragraph boundaries, then line boundaries, then spaces.
    paras = re.split(r"(\n\n+)", text)
    chunks: List[str] = []
    current = ""

    for part in paras:
        if not part:
            continue
        if len(current) + len(part) <= limit:
            current += part
            continue

        if current:
            chunks.append(current)
            current = ""

        if len(part) <= limit:
            current = part
            continue

        lines = part.splitlines(keepends=True)
        for line in lines:
            if len(current) + len(line) <= limit:
                current += line
                continue
            if current:
                chunks.append(current)
                current = ""

            if len(line) <= limit:
                current = line
                continue

            rest = line
            while len(rest) > limit:
                cut = rest.rfind(" ", 0, limit)
                if cut < int(limit * 0.6):
                    cut = limit
                chunks.append(rest[:cut])
                rest = rest[cut:]
            current = rest

    if current:
        chunks.append(current)
    return chunks


def translate_text(text: str, retries: int = 7) -> str:
    # Imported lazily so merge mode does not need deep-translator.
    from deep_translator import GoogleTranslator

    translator = GoogleTranslator(source="en", target="zh-CN")
    out: List[str] = []

    for idx, chunk in enumerate(split_for_translation(text)):
        # Keep pure whitespace unchanged.
        if not chunk.strip():
            out.append(chunk)
            continue

        last_error = None
        for attempt in range(retries):
            try:
                translated = translator.translate(chunk)
                if not translated or not translated.strip():
                    raise RuntimeError("empty translation")
                out.append(translated)
                # Gentle pacing reduces anonymous endpoint throttling.
                time.sleep(0.15)
                break
            except Exception as exc:
                last_error = exc
                wait = min(45, 2 ** attempt)
                print(
                    f"translation retry {attempt + 1}/{retries} "
                    f"for chunk {idx + 1}: {exc}; sleeping {wait}s",
                    file=sys.stderr,
                    flush=True,
                )
                time.sleep(wait)
                translator = GoogleTranslator(source="en", target="zh-CN")
        else:
            raise RuntimeError(f"Translation failed after {retries} attempts: {last_error}")

    return "".join(out)


def translate_shard(shard: int, shard_size: int, output: Path) -> None:
    _, obj = load_source()
    items = list(obj.items())
    start = shard * shard_size
    end = min(len(items), start + shard_size)
    if start >= len(items):
        raise ValueError(f"Shard {shard} starts past the end of {len(items)} entries.")

    output.mkdir(parents=True, exist_ok=True)
    translated: OrderedDict[str, str] = OrderedDict()
    total = end - start

    for local_i, (key, value) in enumerate(items[start:end], 1):
        if not isinstance(value, str):
            raise TypeError(f"Entry {key!r} is not a string.")
        print(
            f"[shard {shard:02d}] {local_i}/{total}: {key}",
            flush=True,
        )
        translated[key] = translate_text(value)

    out_path = output / f"shard-{shard:02d}.json"
    out_path.write_text(
        json.dumps(translated, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {out_path} ({len(translated)} entries)", flush=True)


def shard_path(lang: str, start: int, end: int) -> str:
    return (
        f"source/{lang}/shards/"
        f"prompting-guide-{start + 1:04d}-{end:04d}.json"
    )


def write_shards(
    obj: OrderedDict,
    base: Path,
    lang: str,
    shard_size: int,
) -> List[Dict[str, object]]:
    items = list(obj.items())
    shard_dir = base / lang / "shards"
    shard_dir.mkdir(parents=True, exist_ok=True)

    # Remove stale shard files so the generated tree exactly matches this source.
    for old in shard_dir.glob("prompting-guide-*.json"):
        old.unlink()

    meta: List[Dict[str, object]] = []
    for start in range(0, len(items), shard_size):
        end = min(len(items), start + shard_size)
        part = OrderedDict(items[start:end])
        name = f"prompting-guide-{start + 1:04d}-{end:04d}.json"
        path = shard_dir / name
        path.write_text(
            json.dumps(part, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        meta.append(
            {
                "start_index": start + 1,
                "end_index": end,
                "entry_count": end - start,
                "path": str(Path("source") / lang / "shards" / name),
                "first_key": items[start][0],
                "last_key": items[end - 1][0],
            }
        )
    return meta


def merge(shards_dir: Path, repo_root: Path, shard_size: int) -> None:
    raw, english = load_source()
    expected_keys = list(english.keys())

    shard_files = sorted(shards_dir.rglob("shard-*.json"))
    if not shard_files:
        raise RuntimeError(f"No translated shard files found under {shards_dir}")

    chinese: OrderedDict[str, str] = OrderedDict()
    for path in shard_files:
        part = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=OrderedDict)
        for key, value in part.items():
            if key in chinese:
                raise RuntimeError(f"Duplicate translated key: {key}")
            chinese[key] = value

    got_keys = list(chinese.keys())
    if got_keys != expected_keys:
        missing = [k for k in expected_keys if k not in chinese]
        extra = [k for k in chinese if k not in english]
        first_mismatch = next(
            (
                (i, expected_keys[i], got_keys[i])
                for i in range(min(len(expected_keys), len(got_keys)))
                if expected_keys[i] != got_keys[i]
            ),
            None,
        )
        raise RuntimeError(
            "Translated shard key/order mismatch. "
            f"expected={len(expected_keys)} got={len(got_keys)} "
            f"missing={missing[:5]} extra={extra[:5]} first_mismatch={first_mismatch}"
        )

    base = repo_root / SOURCE_REL
    en_dir = base / "en"
    zh_dir = base / "zh-CN"
    en_dir.mkdir(parents=True, exist_ok=True)
    zh_dir.mkdir(parents=True, exist_ok=True)

    # Preserve the exact original bytes.
    (en_dir / "prompting-guide.en.json").write_bytes(raw)

    # Chinese translation: same keys/order, translated values.
    (zh_dir / "prompting-guide.zh-CN.json").write_text(
        json.dumps(chinese, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    en_meta = write_shards(english, base, "en", shard_size)
    zh_meta = write_shards(chinese, base, "zh-CN", shard_size)

    index = OrderedDict(
        [
            ("source_url", SOURCE_URL),
            ("source_sha256", SOURCE_SHA256),
            ("entry_count", len(english)),
            ("translation_language", "zh-CN"),
            (
                "translation_note",
                "Machine-translated for reading convenience. "
                "Use prompting-guide.en.json as the authoritative source for exact terminology.",
            ),
            ("shard_size", shard_size),
            ("english_shards", en_meta),
            ("chinese_shards", zh_meta),
            ("keys", expected_keys),
        ]
    )
    (base / "prompting-guide.index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(
        f"Built bilingual source library: {len(english)} entries; "
        f"{len(en_meta)} English shards; {len(zh_meta)} Chinese shards.",
        flush=True,
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    t = sub.add_parser("translate-shard")
    t.add_argument("--shard", type=int, required=True)
    t.add_argument("--shard-size", type=int, default=100)
    t.add_argument("--output", type=Path, required=True)

    m = sub.add_parser("merge")
    m.add_argument("--shards-dir", type=Path, required=True)
    m.add_argument("--repo-root", type=Path, required=True)
    m.add_argument("--shard-size", type=int, default=100)

    args = ap.parse_args()
    if args.cmd == "translate-shard":
        translate_shard(args.shard, args.shard_size, args.output)
    else:
        merge(args.shards_dir, args.repo_root, args.shard_size)


if __name__ == "__main__":
    main()
