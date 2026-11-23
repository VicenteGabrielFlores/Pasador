#!/usr/bin/env python3
"""The dramatic portrait is the author photo. Icons stay on the older mark."""

import json
import re
import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DRAMATIC = ROOT / "assets/author-portrait-dramatic.jpg"
WEBP = ROOT / "assets/author-portrait-dramatic.webp"
OG = ROOT / "assets/author-portrait-dramatic-og.jpg"
TEXT_SUFFIXES = {".html", ".xml", ".json", ".js", ".css", ".py", ".svg", ".webmanifest", ".txt", ".md"}


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
        with Image.open(DRAMATIC) as jpg, Image.open(WEBP) as webp, Image.open(OG) as og:
            self.assertEqual(jpg.format, "JPEG")
            self.assertEqual(jpg.size, (1199, 1312))
            self.assertTrue(jpg.info.get("progressive"))
            self.assertEqual(webp.format, "WEBP")
            self.assertEqual(webp.size, (1199, 1312))
            self.assertEqual(og.format, "JPEG")
            self.assertEqual(og.size, (1200, 630))
            self.assertTrue(og.info.get("progressive"))
        self.assertLess(DRAMATIC.stat().st_size, 200_000)
        self.assertLess(WEBP.stat().st_size, DRAMATIC.stat().st_size)
        self.assertLess(OG.stat().st_size, 200_000)

    def test_old_oil_portraits_are_removed(self):
        self.assertFalse((ROOT / "assets/author/vicente-gabriel-flores-portrait.jpg").exists())
        self.assertFalse((ROOT / "assets/author/vicente-gabriel-flores-portrait-560.jpg").exists())
        self.assertFalse((ROOT / "assets/author").exists())
        needle = "vicente-gabriel-flores-portrait"
        folder = "assets/author/"
        for path in ROOT.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            if path.resolve() == Path(__file__).resolve():
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            rel = path.relative_to(ROOT).as_posix()
            self.assertNotIn(needle, text, rel)
            self.assertNotIn(folder, text, rel)

    def test_published_dimensions_match_the_files(self):
        with Image.open(DRAMATIC) as jpg, Image.open(OG) as og:
            width, height = jpg.size
            og_width, og_height = og.size
        author = (ROOT / "author.html").read_text(encoding="utf-8")
        self.assertIn(f'width="{width}" height="{height}"', author)
        self.assertIn(f'property="og:image:width" content="{og_width}"', author)
        self.assertIn(f'property="og:image:height" content="{og_height}"', author)
        for name in ("author.html", "index.html"):
            for node in persons(ROOT / name):
                if node.get("name") != "Vicente Gabriel Flores":
                    continue
                image = node.get("image")
                if isinstance(image, dict):
                    self.assertEqual(image.get("width"), width, name)
                    self.assertEqual(image.get("height"), height, name)

    def test_homepage_author_section_uses_the_portrait(self):
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        author = index.split('id="author"', 1)[1].split("</section>", 1)[0]
        self.assertNotIn('class="author-portrait"', author)
        self.assertIn('href="/author.html"', author)
        self.assertIn(
            "https://vicentegabrielflores.com/assets/author-portrait-dramatic.jpg",
            index,
        )
        self.assertIn('src="/assets/portrait-menu.webp"', index)
        self.assertIn(
            'property="og:image" content="https://vicentegabrielflores.com/og-image.jpg"',
            index,
        )
        self.assertIn(
            'name="twitter:image" content="https://vicentegabrielflores.com/og-image.jpg"',
            index,
        )

    def test_one_person_entity(self):
        canonical = "https://vicentegabrielflores.com/#author"
        image = "https://vicentegabrielflores.com/assets/author-portrait-dramatic.jpg"
        same = [
            "https://x.com/pasadornovel",
            "https://www.amazon.com/author/vicentegabrielflores",
        ]
        jobs = ["Writer", "Poet", "Playwright", "Visual Artist"]
        description = "Tejano writer and visual artist based in Austin, Texas."

        def named(path):
            return [node for node in persons(path) if node.get("name") == "Vicente Gabriel Flores"]

        for name in ("author.html", "index.html"):
            nodes = named(ROOT / name)
            self.assertTrue(nodes, name)
            for node in nodes:
                self.assertEqual(node.get("@id"), canonical, name)
                got = node.get("image")
                url = got.get("url") if isinstance(got, dict) else got
                self.assertEqual(url, image, name)
                self.assertEqual(node.get("jobTitle"), jobs, name)
                self.assertEqual(node.get("description"), description, name)
                self.assertEqual(node.get("sameAs"), same, name)
                self.assertEqual(node.get("url"), "https://vicentegabrielflores.com/author.html", name)

        for name in (
            "artifacts.html",
            "whats-in-the-air.html",
            "poems/the-invocation.html",
            "stories/salt-water.html",
            "art.html",
            "the-manifest.html",
        ):
            text = (ROOT / name).read_text(encoding="utf-8")
            self.assertIn(canonical, text, name)
            for node in persons(ROOT / name):
                if node.get("name") == "Vicente Gabriel Flores" or node.get("@id") == canonical:
                    self.assertEqual(node.get("@id"), canonical, name)
                    self.assertNotIn("image", node, name)

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
