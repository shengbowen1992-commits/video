#!/usr/bin/env python3
"""
Build a Simplified-Chinese translation of the original prompting-guide.json.

- Verifies the upstream English source by SHA-256.
- Preserves all 1268 top-level keys and their original order.
- Translates values with the offline Argos Translate en->zh model.
- Keeps clearly minor/child-coded sexual themes untranslated and replaces only
  their value with a Chinese omission notice.
- Supports sharded translation for GitHub Actions, then merges the shards.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from collections import OrderedDict
from pathlib import Path
from typing import List, Tuple

import requests

SOURCE_URL = (
    "https://huggingface.co/NSFW-API/NSFW_Wan_1.3b/"
    "resolve/main/prompting-guide.json"
)
SOURCE_SHA256 = "8f1693636c7928248aaa241f4db7315e8da132b642ac498f25e385a6f1fb178c"
SKILL_REL = Path("skills/h3-adult-action-prompting")
SOURCE_REL = SKILL_REL / "references" / "source"

OMISSION_ZH = "[已省略：该主题涉及未成年人、年龄不明确或儿童化的性内容，因此未翻译正文。]"

# Deliberately specific child/minor indicators. Do not block ordinary "young adult"
# or the explicit adult age range 18-19.
BLOCK_RE = re.compile(
    r"(?i)(?:"
    r"\bunderage\b|\bminor\b|\bchild(?:ren|hood|like)?\b|\bkid(?:s)?\b|"
    r"\bschoolgirl\b|\bschoolboy\b|\blittle\s+girl\b|\blittle\s+boy\b|"
    r"\bpreteen\b|\bpre-teen\b|\bteenage\s+(?:girl|boy)\b|"
    r"\bbarely\s+legal\b|\bage[- ]?regression\b|\baged[- ]?up\b"
    r")"
)


def download_source() -> bytes:
    r = requests.get(SOURCE_URL, timeout=120)
    r.raise_for_status()
    data = r.content
    digest = hashlib.sha256(data).hexdigest()
    if digest != SOURCE_SHA256:
        raise RuntimeError(
            f"Source SHA-256 mismatch: expected {SOURCE_SHA256}, got {digest}"
        )
    return data


def load_source() -> Tuple[bytes, OrderedDict]:
    raw = download_source()
    obj = json.loads(raw.decode("utf-8"), object_pairs_hook=OrderedDict)
    if not isinstance(obj, dict):
        raise TypeError("Expected a top-level JSON object")
    if len(obj) != 1268:
        raise RuntimeError(f"Expected 1268 top-level entries, got {len(obj)}")
    return raw, obj


def is_blocked(key: str, value: str) -> bool:
    # 18_19 is an explicit adult range, so it is not blocked merely by its key.
    return bool(BLOCK_RE.search(key + "\n" + value))


def get_package():
    """Return the installed direct en->zh Argos package."""
    import argostranslate.package

    packages = argostranslate.package.get_installed_packages()
    for pkg in packages:
        if getattr(pkg, "type", None) == "translate" and pkg.from_code == "en" and pkg.to_code == "zh":
            return pkg
    raise RuntimeError("Argos en->zh language package is not installed")


def split_translation_units(text: str, max_chars: int = 420):
    """Split text into short units while preserving all separators for reconstruction."""
    units = []
    # Preserve newline runs exactly. Translate only non-newline pieces.
    for block in re.split(r"(\\n+)", text):
        if not block:
            continue
        if block.startswith("\\n"):
            units.append((False, block))
            continue

        # Preserve leading Markdown bullet/number indentation outside the MT model.
        m = re.match(r"^(\\s*(?:(?:[-*+]\\s+)|(?:\\d+[.)]\\s+))?)(.*?)(\\s*)$", block, re.S)
        prefix, core, suffix = m.group(1), m.group(2), m.group(3)
        if prefix:
            units.append((False, prefix))

        # Split long prose at sentence-ish boundaries first.
        pieces = re.split(r"(?<=[.!?。！？])(?=\\s+)", core)
        for piece in pieces:
            if not piece:
                continue
            while len(piece) > max_chars:
                cut = piece.rfind(" ", 0, max_chars)
                if cut < max_chars // 2:
                    cut = max_chars
                head, piece = piece[:cut], piece[cut:]
                units.append((bool(re.search(r"[A-Za-z]", head)), head))
            if piece:
                units.append((bool(re.search(r"[A-Za-z]", piece)), piece))

        if suffix:
            units.append((False, suffix))
    return units


def batch_translate_values(items):
    """Translate many theme values in one CTranslate2 batch for speed."""
    import ctranslate2
    import argostranslate.settings as settings

    pkg = get_package()
    params = {
        "model_path": str(pkg.package_path / "model"),
        "device": settings.device,
        "inter_threads": settings.inter_threads,
        "intra_threads": settings.intra_threads,
    }
    if settings.compute_type != "auto":
        params["compute_type"] = settings.compute_type
    translator = ctranslate2.Translator(**params)

    layouts = []
    source_segments = []
    blocked = []

    for key, value in items:
        if is_blocked(key, value):
            layouts.append((key, [("fixed", OMISSION_ZH)]))
            blocked.append(key)
            continue

        layout = []
        for should_translate, unit in split_translation_units(value):
            if should_translate:
                idx = len(source_segments)
                source_segments.append(unit)
                layout.append(("translated", idx))
            else:
                layout.append(("fixed", unit))
        layouts.append((key, layout))

    if source_segments:
        print(f"Batch translating {len(source_segments)} text units", flush=True)
        tokenized = [pkg.tokenizer.encode(x) for x in source_segments]
        target_prefix = None
        if pkg.target_prefix != "":
            target_prefix = [[pkg.target_prefix]] * len(tokenized)

        results = translator.translate_batch(
            tokenized,
            target_prefix=target_prefix,
            replace_unknowns=True,
            max_batch_size=settings.batch_size,
            batch_type="tokens",
            beam_size=1,
            num_hypotheses=1,
            length_penalty=0.2,
            return_scores=False,
        )

        translations = []
        for result in results:
            value = pkg.tokenizer.decode(result.hypotheses[0])
            if pkg.target_prefix and value.startswith(pkg.target_prefix):
                value = value[len(pkg.target_prefix):]
            translations.append(value.lstrip(" "))
    else:
        translations = []

    out = OrderedDict()
    for key, layout in layouts:
        parts = []
        for kind, payload in layout:
            if kind == "fixed":
                parts.append(payload)
            else:
                parts.append(translations[payload])
        out[key] = "".join(parts)
    return out, blocked

def translate_shard(shard: int, shard_size: int, output: Path) -> None:
    _, obj = load_source()
    items = list(obj.items())
    start = shard * shard_size
    end = min(len(items), start + shard_size)
    if start >= len(items):
        raise ValueError(f"Shard {shard} starts past the end of {len(items)} entries")

    selected = items[start:end]
    print(
        f"[shard {shard:02d}] translating entries {start+1}-{end} ({len(selected)} themes)",
        flush=True,
    )
    result, blocked = batch_translate_values(selected)

    output.mkdir(parents=True, exist_ok=True)
    out_path = output / f"shard-{shard:02d}.json"
    out_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\\n",
        encoding="utf-8",
    )
    (output / f"shard-{shard:02d}.blocked.json").write_text(
        json.dumps(blocked, ensure_ascii=False, indent=2) + "\\n",
        encoding="utf-8",
    )
    print(f"[shard {shard:02d}] wrote {len(result)} themes", flush=True)

def write_shards(obj: OrderedDict, base: Path, lang: str, shard_size: int):
    items = list(obj.items())
    shard_dir = base / lang / "shards"
    shard_dir.mkdir(parents=True, exist_ok=True)
    for old in shard_dir.glob("prompting-guide-*.json"):
        old.unlink()

    meta = []
    for start in range(0, len(items), shard_size):
        end = min(len(items), start + shard_size)
        part = OrderedDict(items[start:end])
        name = f"prompting-guide-{start+1:04d}-{end:04d}.json"
        path = shard_dir / name
        path.write_text(
            json.dumps(part, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        meta.append({
            "start_index": start + 1,
            "end_index": end,
            "entry_count": end - start,
            "path": str(Path("source") / lang / "shards" / name),
            "first_key": items[start][0],
            "last_key": items[end-1][0],
        })
    return meta


def merge(shards_dir: Path, repo_root: Path, shard_size: int) -> None:
    raw, english = load_source()
    expected_keys = list(english.keys())

    shard_files = sorted(
        p for p in shards_dir.rglob("shard-*.json")
        if not p.name.endswith(".blocked.json")
    )
    if not shard_files:
        raise RuntimeError(f"No translated shard files found under {shards_dir}")

    chinese: OrderedDict[str, str] = OrderedDict()
    blocked_keys: List[str] = []
    for path in shard_files:
        part = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=OrderedDict)
        for key, value in part.items():
            if key in chinese:
                raise RuntimeError(f"Duplicate translated key: {key}")
            chinese[key] = value

        blocked_path = path.with_name(path.stem + ".blocked.json")
        if blocked_path.exists():
            blocked_keys.extend(json.loads(blocked_path.read_text(encoding="utf-8")))

    if list(chinese.keys()) != expected_keys:
        missing = [k for k in expected_keys if k not in chinese]
        extra = [k for k in chinese if k not in english]
        raise RuntimeError(
            f"Translated keys/order mismatch. missing={missing[:10]} extra={extra[:10]}"
        )

    base = repo_root / SOURCE_REL
    en_dir = base / "en"
    zh_dir = base / "zh-CN"
    en_dir.mkdir(parents=True, exist_ok=True)
    zh_dir.mkdir(parents=True, exist_ok=True)

    # Preserve exact upstream bytes for the English source.
    (en_dir / "prompting-guide.en.json").write_bytes(raw)

    # Full Chinese version with identical top-level keys/order.
    (zh_dir / "prompting-guide.zh-CN.json").write_text(
        json.dumps(chinese, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    en_meta = write_shards(english, base, "en", shard_size)
    zh_meta = write_shards(chinese, base, "zh-CN", shard_size)

    index = OrderedDict([
        ("source_url", SOURCE_URL),
        ("source_sha256", SOURCE_SHA256),
        ("entry_count", len(english)),
        ("translation_language", "zh-CN"),
        ("translator", "Argos Translate en->zh offline model"),
        ("translation_note",
         "Machine translation for reading convenience. Top-level keys and order are preserved. "
         "Use the English source as authoritative for exact prompt tokens."),
        ("omitted_minor_or_child_coded_entries", sorted(set(blocked_keys))),
        ("omission_notice_zh", OMISSION_ZH),
        ("shard_size", shard_size),
        ("english_shards", en_meta),
        ("chinese_shards", zh_meta),
        ("keys", expected_keys),
    ])
    (base / "prompting-guide.index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(
        f"Built {len(english)} entries; blocked={len(set(blocked_keys))}; "
        f"en_shards={len(en_meta)} zh_shards={len(zh_meta)}",
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
