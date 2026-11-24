#!/usr/bin/env python3
"""Check local Markdown/wiki links, attachments, and heading fragments.

Defaults to wiki/; pass repo-relative files/directories to check archive pages too.
Code examples are ignored. Remote URLs are not fetched.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / 'wiki'
WIKI_RE = re.compile(r'!?\[\[([^\]|]+)(?:\|[^\]]+)?\]\]')
MARKDOWN_RE = re.compile(r'!?\[[^\]\n]*\]\((<[^>]+>|[^)\n]+)\)')


def without_fences(text: str) -> str:
    """Keep line numbers stable while removing fenced code examples."""
    lines = []
    fence = ''
    for line in text.splitlines(keepends=True):
        marker = re.match(r'^\s{0,3}(`{3,}|~{3,})', line)
        if fence:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence):
                fence = ''
            lines.append('\n')
        elif marker:
            fence = marker[1]
            lines.append('\n')
        else:
            lines.append(line)
    return ''.join(lines)


def without_code(text: str) -> str:
    return re.sub(r'(`+)([^`\n]|(?!\1)`)*?\1', '', without_fences(text))


def slug(text: str) -> str:
    text = re.sub(r'[^\w\-\s]', '', text.lower())
    return re.sub(r'\s', '-', text.strip())


def headings(path: Path) -> set[str]:
    result = set()
    counts: dict[str, int] = {}
    for line in without_fences(path.read_text(encoding='utf-8')).splitlines():
        match = re.match(r'^#{1,6}\s+(.+?)\s*#*$', line)
        if not match:
            continue
        title = match[1]
        result.add(title)
        key = slug(title)
        count = counts.get(key, 0)
        result.add(f'{key}-{count}' if count else key)
        counts[key] = count + 1
    return result


def resolve_wiki(source: Path, target: str, inventory: list[Path]) -> list[Path]:
    if not target:
        return [source]
    for base in (WIKI, ROOT, source.parent):
        candidate = base / target
        for path in (candidate, Path(str(candidate) + '.md')):
            if path.is_file():
                return [path]
    if '/' in target:
        return []
    return [path for path in inventory if path.name == target or
            (path.suffix == '.md' and path.stem == target)]


def local_links(text: str) -> list[tuple[int, str, bool]]:
    clean = without_code(text)
    links = [(m.start(), m[1], True) for m in WIKI_RE.finditer(clean)]
    links += [(m.start(), m[1].strip('<>'), False) for m in MARKDOWN_RE.finditer(clean)]
    return [(clean.count('\n', 0, pos) + 1, target, wiki) for pos, target, wiki in links]


def check_file(source: Path, inventory: list[Path]) -> tuple[int, list[str]]:
    errors = []
    total = 0
    for line, raw_target, wiki in local_links(source.read_text(encoding='utf-8')):
        if not wiki and re.match(r'(?:[a-zA-Z][\w+.-]*:|//)', raw_target):
            continue
        total += 1
        target, _, fragment = unquote(raw_target).partition('#')
        if wiki:
            matches = resolve_wiki(source, target, inventory)
        else:
            path = (source.parent / Path(target).expanduser()) if target else source
            matches = [path] if path.exists() else []
        prefix = f'{source.relative_to(ROOT)}:{line} -> {raw_target}'
        if not matches:
            errors.append(f'MISSING {prefix}')
        elif len(matches) > 1:
            errors.append(f'AMBIGUOUS {prefix}')
        elif fragment and matches[0].suffix == '.md':
            anchors = headings(matches[0])
            if fragment not in anchors and slug(fragment) not in anchors:
                errors.append(f'MISSING HEADING {prefix}')
    return total, errors


def main() -> int:
    roots = [ROOT / arg for arg in sys.argv[1:]] or [WIKI]
    if any(not path.exists() for path in roots):
        print('Input path does not exist.', file=sys.stderr)
        return 2
    files = sorted({file for path in roots for file in
                    ([path] if path.is_file() else path.rglob('*.md'))})
    inventory = [file for directory in ('wiki', 'archive', 'raw')
                 for file in (ROOT / directory).rglob('*') if file.is_file()]
    total = 0
    errors = []
    for file in files:
        count, failures = check_file(file, inventory)
        total += count
        errors.extend(failures)
    for error in errors:
        print(error)
    print(f'links: total={total} ok={total - len(errors)} errors={len(errors)} files={len(files)}')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
