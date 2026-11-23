#!/usr/bin/env python3
"""JSON-LD checks for the structured-data pass.

Poems are CreativeWork with genre poetry. Art is VisualArtwork.
Plays carry author and language. Author images carry license fields.
"""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEED = ["creator", "creditText", "copyrightNotice", "license", "acquireLicensePage"]
RIGHTS = "https://vicentegabrielflores.com/rights.html"
PLAYS = [
    "la-toma.html",
    "modern-play.html",
    "belmont-road.html",
    "davos.html",
    "from-ship-to-ship-01-laetare.html",
]
AIR = sorted(ROOT.glob("whats-in-the-air-20??-??-??.html"))
FLAGGED = [
    "index.html",
    "author.html",
    "modern-play.html",
    "la-toma.html",
    "davos.html",
    "the-manifest.html",
    "rights.html",
    "stories/index.html",
]


def blocks(path):
    text = path.read_text(encoding="utf-8")
    found = []
    for raw in re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', text, re.S):
        found.append(json.loads(raw))
    return found


def walk(node, acc):
    if isinstance(node, dict):
        acc.append(node)
        for value in node.values():
            walk(value, acc)
    elif isinstance(node, list):
        for value in node:
            walk(value, acc)


def nodes(path):
    acc = []
    for block in blocks(path):
        walk(block, acc)
    return acc


def types(node):
    value = node.get("@type")
    return value if isinstance(value, list) else [value]


class JsonLd(unittest.TestCase):
    def test_every_block_parses_and_poem_is_not_a_type(self):
        for path in ROOT.rglob("*.html"):
            for node in nodes(path):
                self.assertNotIn("Poem", types(node), path)

    def test_poem_pages_are_creative_work(self):
        for path in (ROOT / "poems").glob("*.html"):
            works = [n for n in nodes(path) if "CreativeWork" in types(n) and n.get("genre") == "poetry"]
            self.assertTrue(works, path.name)

    def test_visual_artwork(self):
        for name in ("art.html", "art/jinghan.html", "art/lawrence.html", "art/leo.html"):
            works = [n for n in nodes(ROOT / name) if "VisualArtwork" in types(n)]
            self.assertTrue(works, name)
            for work in works:
                self.assertNotEqual(work.get("dateCreated"), "2026-11-13", name)
                self.assertIn("artform", work, work.get("name"))
                creator = work["creator"]
                self.assertEqual(creator.get("@type"), "Person")
                self.assertEqual(creator.get("name"), "Vicente Gabriel Flores")
                self.assertTrue(work.get("url"))
                self.assertTrue(work.get("image"))

    def test_plays(self):
        for name in PLAYS:
            plays = [n for n in nodes(ROOT / name) if "Play" in types(n)]
            self.assertTrue(plays, name)
            for play in plays:
                self.assertIn("author", play)
                self.assertIn("inLanguage", play)
        manifest = nodes(ROOT / "modern-play.html")
        play = next(n for n in manifest if "Play" in types(n))
        self.assertEqual(play["datePublished"], "2026")
        laetare = next(n for n in nodes(ROOT / "from-ship-to-ship-01-laetare.html") if "Play" in types(n))
        self.assertEqual(laetare["datePublished"], "2026-11-19")

    def test_author_images_carry_license(self):
        pages = [ROOT / name for name in FLAGGED]
        pages += AIR
        pages += [ROOT / "from-ship-to-ship.html", ROOT / "from-ship-to-ship-01-laetare.html"]
        for path in pages:
            images = [n for n in nodes(path) if "ImageObject" in types(n)]
            self.assertTrue(images, path.name)
            for image in images:
                url = image.get("contentUrl") or image.get("url") or ""
                if "/assets/artifacts/" in url:
                    continue
                for field in NEED:
                    self.assertIn(field, image, f"{path.name} {url} {field}")
                self.assertEqual(image["license"], RIGHTS)
                self.assertEqual(image["acquireLicensePage"], RIGHTS)


if __name__ == "__main__":
    unittest.main()
