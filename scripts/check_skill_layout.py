#!/usr/bin/env python3
"""Check package boundaries, relative Markdown links, JSON and Python syntax offline."""
import ast
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


def check(root):
    errors = []
    names = []
    if (root / 'SKILL.md').exists():
        errors.append('Root SKILL.md would make the skill catalog ambiguous')
    skill_dirs = sorted(path for path in (root / 'skills').iterdir() if path.is_dir())
    for skill in skill_dirs:
        entry = skill / 'SKILL.md'
        if not entry.is_file():
            errors.append(f'{skill.name}: missing SKILL.md')
            continue
        content = entry.read_text(encoding='utf-8-sig')
        front = re.match(r'^---\r?\n(.*?)\r?\n---(?:\r?\n|$)', content, re.S)
        if not front:
            errors.append(f'{skill.name}: missing YAML frontmatter')
            continue
        name = re.search(r'^name: ([a-z0-9]+(?:-[a-z0-9]+)*)$', front[1], re.M)
        description = re.search(r'^description: (.+)$', front[1], re.M)
        if not name or name[1] != skill.name or len(skill.name) > 64:
            errors.append(f'{skill.name}: name does not match directory')
        if not description or not 1 <= len(description[1].strip()) <= 1024:
            errors.append(f'{skill.name}: missing or oversized description')
        names.append(skill.name)
        for path in skill.rglob('*'):
            if path.is_symlink() or path.resolve().is_relative_to(skill.resolve()) is False:
                errors.append(f'{path.relative_to(root)}: must stay inside its skill')
        for markdown in skill.rglob('*.md'):
            body = markdown.read_text(encoding='utf-8-sig')
            for match in re.finditer(r'\[[^\]\n]*\]\(([^)\n]+)\)', body):
                target = match[1].strip().strip('<>')
                parsed = urlsplit(target)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                resolved = (markdown.parent / unquote(parsed.path)).resolve()
                if not resolved.is_relative_to(skill.resolve()):
                    errors.append(f'{markdown.relative_to(root)}: link escapes skill: {target}')
                elif not resolved.exists():
                    errors.append(f'{markdown.relative_to(root)}: missing link: {target}')
    for path in root.rglob('*'):
        if not path.is_file() or '.git' in path.parts or '__pycache__' in path.parts:
            continue
        try:
            if path.suffix == '.json':
                json.loads(path.read_text(encoding='utf-8-sig'))
            elif path.suffix == '.py':
                ast.parse(path.read_text(encoding='utf-8-sig'), filename=str(path))
        except (ValueError, SyntaxError, UnicodeError) as error:
            errors.append(f'{path.relative_to(root)}: {error}')
    return names, errors


if __name__ == '__main__':
    names, errors = check(Path(__file__).resolve().parents[1])
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        raise SystemExit(1)
    print('VALID: isolated skill packages: ' + ', '.join(names))
