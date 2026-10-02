#!/usr/bin/env python3
import hashlib
import json
import re
import time
import urllib.request
from collections import OrderedDict
from pathlib import Path

SOURCE_URL = "https://huggingface.co/NSFW-API/NSFW_Wan_1.3b/resolve/main/prompting-guide.json"
EXPECTED_SHA256 = "8f1693636c7928248aaa241f4db7315e8da132b642ac498f25e385a6f1fb178c"

ROOT = Path(__file__).resolve().parents[1]
REFS = ROOT / "references"
EN_PATH = REFS / "prompting-guide.source.en.json"
ZH_PATH = REFS / "prompting-guide.source.zh-CN.json"
META_PATH = REFS / "prompting-guide.translation-meta.json"

# Entries whose framing explicitly sexualizes underage / age-regressed /
# child-coded subjects are not reproduced or translated.
BLOCK_PATTERNS = [
    re.compile(r"\bunderage\b", re.I),
    re.compile(r"\baged[- ]?up\b", re.I),
    re.compile(r"\bage[- ]?regression\b", re.I),
    re.compile(r"\bchildlike\b", re.I),
    re.compile(r"\bschoolgirl\b", re.I),
    re.compile(r"\bschoolboy\b", re.I),
    re.compile(r"\blittle girl\b", re.I),
    re.compile(r"\blittle boy\b", re.I),
    re.compile(r"\bbarely legal\b", re.I),
]
BLOCK_KEYS = {"ABDL"}

MAX_CHARS = 4200


def download_source() -> bytes:
    req = urllib.request.Request(SOURCE_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    sha = hashlib.sha256(data).hexdigest()
    if sha != EXPECTED_SHA256:
        raise RuntimeError(
            f"Source SHA256 mismatch: expected {EXPECTED_SHA256}, got {sha}. "
            "Refusing to build from a changed source."
        )
    return data


def is_blocked(key: str, value: str) -> bool:
    if key in BLOCK_KEYS:
        return True
    haystack = key + "\n" + value
    return any(p.search(haystack) for p in BLOCK_PATTERNS)


def split_text(text: str, limit: int = MAX_CHARS):
    if len(text) <= limit:
        return [text]

    # Prefer paragraph boundaries, then line boundaries, then hard slices.
    paras = re.split(r"(\n\n+)", text)
    chunks, buf = [], ""
    for part in paras:
        if len(buf) + len(part) <= limit:
            buf += part
            continue
        if buf:
            chunks.append(buf)
            buf = ""
        if len(part) <= limit:
            buf = part
        else:
            lines = part.splitlines(keepends=True)
            for line in lines:
                if len(buf) + len(line) <= limit:
                    buf += line
                else:
                    if buf:
                        chunks.append(buf)
                        buf = ""
                    if len(line) <= limit:
                        buf = line
                    else:
                        for i in range(0, len(line), limit):
                            chunks.append(line[i:i+limit])
    if buf:
        chunks.append(buf)
    return chunks


def translate_chunk(translator, text: str) -> str:
    if not text.strip():
        return text
    last = None
    for attempt in range(7):
        try:
            out = translator.translate(text)
            if out:
                return out
        except Exception as exc:
            last = exc
        time.sleep(min(30, 2 ** attempt))
    raise RuntimeError(f"Translation failed after retries: {last}")


def main():
    from deep_translator import GoogleTranslator

    source_bytes = download_source()
    source = json.loads(source_bytes.decode("utf-8"), object_pairs_hook=OrderedDict)

    safe = OrderedDict()
    omitted = []
    for key, value in source.items():
        if is_blocked(key, value):
            omitted.append(key)
            continue
        safe[key] = value

    REFS.mkdir(parents=True, exist_ok=True)
    EN_PATH.write_text(
        json.dumps(safe, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    translator = GoogleTranslator(source="en", target="zh-CN")
    translated = OrderedDict()
    total = len(safe)

    for idx, (key, value) in enumerate(safe.items(), 1):
        parts = split_text(value)
        zh_parts = [translate_chunk(translator, p) for p in parts]
        translated[key] = "".join(zh_parts)

        if idx % 25 == 0 or idx == total:
            print(f"translated {idx}/{total}")
            # Checkpoint locally so a late error preserves progress in logs/workspace.
            ZH_PATH.write_text(
                json.dumps(translated, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

    meta = {
        "source_url": SOURCE_URL,
        "source_sha256": EXPECTED_SHA256,
        "source_top_level_entries": len(source),
        "included_entries": len(safe),
        "omitted_entries": len(omitted),
        "omitted_keys": omitted,
        "english_file": EN_PATH.name,
        "chinese_file": ZH_PATH.name,
        "translation": "Machine translation to Simplified Chinese via GoogleTranslator (deep-translator). Top-level source keys are preserved.",
        "safety_note": "Entries explicitly framed around underage, age-regressed, or child-coded sexual subjects are omitted from both local source copies.",
    }
    META_PATH.write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(json.dumps(meta, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
