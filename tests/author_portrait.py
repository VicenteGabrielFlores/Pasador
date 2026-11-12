#!/usr/bin/env python3
"""The approved oil portrait is the author photo. Icons stay on the older mark."""

import json
import re
import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
FULL = ROOT / "assets/author/vicente-gabriel-flores-portrait.jpg"
SMALL = ROOT / "assets/author/vicente-gabriel-flores-portrait-560.jpg"
URL = "https://vicentegabrielflores.com/assets/author/vicente-gabriel-flores-portrait.jpg"


def persons(path):
    text = path.read_text(encoding="utf-8")
    found = []
    for match in re.finditer(
        r'<script type="application/ld\+json">\s*(.*?)\s*</script>', text, re.S
    ):
        data = json.loads(match.group(1))

        def walk(node):
            if isinstance(node, dict):
                kind = node.get("@type")
                if kind == "Person" or (isinstance(kind, list) and "Person" in kind):
                    found.append(node)
                for value in node.values():
                    walk(value)
            elif isinstance(node, list):
                for value in node:
                    walk(value)

        walk(data)
    return found


class AuthorPortrait(unittest.TestCase):
    def test_optimized_copies(self):
        with Image.open(FULL) as full, Image.open(SMALL) as small:
            self.assertEqual(full.size, (1024, 1024))
            self.assertEqual(small.size, (560, 560))
        self.assertLess(FULL.stat().st_size, 200_000)
        self.assertLess(SMALL.stat().st_size, 200_000)

    def test_homepage_author_section_uses_the_portrait(self):
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        author = index.split('id="author"', 1)[1].split("</section>", 1)[0]
        self.assertIn('class="author-portrait"', author)
        self.assertIn('alt="Portrait of Vicente Gabriel Flores"', author)
        self.assertIn("/assets/author/vicente-gabriel-flores-portrait-560.jpg", author)
        self.assertIn("/assets/author/vicente-gabriel-flores-portrait.jpg", author)
        self.assertIn('src="/portrait-vicente.png"', index)
        self.assertIn(
            'property="og:image" content="https://vicentegabrielflores.com/og-image.jpg"',
            index,
        )
        self.assertIn(
            'name="twitter:image" content="https://vicentegabrielflores.com/og-image.jpg"',
            index,
        )

    def test_person_nodes_point_at_the_portrait(self):
        for name in (
            "index.html",
            "artifacts.html",
            "whats-in-the-air.html",
            "poems/the-invocation.html",
            "stories/salt-water.html",
        ):
            nodes = persons(ROOT / name)
            self.assertTrue(nodes, name)
            for node in nodes:
                image = node.get("image")
                url = image.get("url") if isinstance(image, dict) else image
                self.assertEqual(url, URL, name)

    def test_icons_are_not_replaced(self):
        for name in (
            "favicon.svg",
            "favicon.ico",
            "apple-touch-icon.png",
            "icon-192.png",
            "icon-512.png",
            "portrait-vicente.png",
        ):
            raw = (ROOT / name).read_bytes()
            self.assertNotIn(b"vicente-gabriel-flores-portrait", raw)


if __name__ == "__main__":
    unittest.main()
