"""Offline regression checks for navigation validation (no project runtime)."""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import check_wikilinks as checker


class LinkChecks(unittest.TestCase):
    def setUp(self) -> None:
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.wiki = self.root / 'wiki'
        self.wiki.mkdir()
        self.source = self.wiki / 'source.md'
        self.source.write_text('# Source\n')
        root_patch = patch.object(checker, 'ROOT', self.root)
        wiki_patch = patch.object(checker, 'WIKI', self.wiki)
        root_patch.start()
        wiki_patch.start()
        self.addCleanup(root_patch.stop)
        self.addCleanup(wiki_patch.stop)

    def check(self, text: str) -> tuple[int, list[str]]:
        self.source.write_text(text)
        inventory = [path for path in self.root.rglob('*') if path.is_file()]
        return checker.check_file(self.source, inventory)

    def test_examples_are_not_links(self) -> None:
        total, errors = self.check('`[[missing]]`\n```md\n[[missing]]\n```\n'
                                   '~~~md\n[missing](gone.md)\n~~~\n')
        self.assertEqual((total, errors), (0, []))

    def test_actual_missing_link_is_reported_with_line(self) -> None:
        total, errors = self.check('# Source\n\n[[missing]]')
        self.assertEqual(total, 1)
        self.assertEqual(errors, ['MISSING wiki/source.md:3 -> missing'])

    def test_attachments_and_encoded_markdown_paths(self) -> None:
        (self.wiki / 'image one.png').write_bytes(b'fixture')
        self.assertEqual(self.check('![[image one.png]]\n![image](image%20one.png)'), (2, []))

    def test_archive_relative_link_and_heading(self) -> None:
        archive = self.root / 'archive'
        archive.mkdir()
        (archive / 'history.md').write_text('# History\n## A decision\n')
        self.assertEqual(self.check('[history](../archive/history.md#a-decision)'), (1, []))

    def test_missing_heading_fails(self) -> None:
        (self.wiki / 'target.md').write_text('# Target\n')
        total, errors = self.check('[[target#Missing]]')
        self.assertEqual(total, 1)
        self.assertEqual(len(errors), 1)
        self.assertTrue(errors[0].startswith('MISSING HEADING'))

    def test_fenced_heading_is_not_a_destination(self) -> None:
        (self.wiki / 'target.md').write_text('# Target\n```py\n# Fake\n```\n')
        self.assertTrue(self.check('[[target#Fake]]')[1])

    def test_bare_ambiguous_name_fails(self) -> None:
        for name in ['first', 'second']:
            directory = self.wiki / name
            directory.mkdir()
            (directory / 'duplicate.md').write_text('# Duplicate\n')
        self.assertTrue(self.check('[[duplicate]]')[1][0].startswith('AMBIGUOUS'))

    def test_explicit_missing_path_does_not_guess_same_stem(self) -> None:
        (self.wiki / 'target.md').write_text('# Target\n')
        self.assertTrue(self.check('[[wrong/target]]')[1][0].startswith('MISSING'))

    def test_external_urls_are_not_fetched(self) -> None:
        self.assertEqual(self.check('[site](https://example.com/missing#fragment)'), (0, []))

    def test_repeated_heading_slugs_and_inline_code(self) -> None:
        (self.wiki / 'target.md').write_text('# Target\n## A `value`\n## A `value`\n')
        self.assertEqual(self.check('[target](target.md#a-value-1)'), (1, []))


if __name__ == '__main__':
    unittest.main()
