#!/usr/bin/env python3
"""Validate Obsidian-style wikilinks under mm-knowledge/wiki.

Resolves links by either path relative to wiki without .md, or by unique markdown
file stem, matching Obsidian's common [[Page Name]] behavior closely enough for
agent hygiene checks.
"""
from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki"
LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")


def main() -> int:
    files = sorted(WIKI.rglob("*.md"))
    by_path = {str(path.relative_to(WIKI)).removesuffix(".md"): path for path in files}
    by_stem: dict[str, list[Path]] = defaultdict(list)
    for path in files:
        by_stem[path.stem].append(path)

    missing: list[tuple[Path, str]] = []
    ambiguous: list[tuple[Path, str, list[Path]]] = []
    total = 0

    for path in files:
        text = path.read_text(encoding="utf-8")
        for link in LINK_RE.findall(text):
            total += 1
            if link in by_path:
                continue
            stem_matches = by_stem.get(link, [])
            if len(stem_matches) == 1:
                continue
            if len(stem_matches) > 1:
                ambiguous.append((path, link, stem_matches))
            else:
                missing.append((path, link))

    for path, link in missing:
        print(f"MISSING {path.relative_to(ROOT)} -> [[{link}]]")
    for path, link, matches in ambiguous:
        rendered = ", ".join(str(match.relative_to(ROOT)) for match in matches)
        print(f"AMBIGUOUS {path.relative_to(ROOT)} -> [[{link}]] matches {rendered}")

    ok = not missing and not ambiguous
    print(f"wikilinks: total={total} ok={total - len(missing) - len(ambiguous)} missing={len(missing)} ambiguous={len(ambiguous)} files={len(files)}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
