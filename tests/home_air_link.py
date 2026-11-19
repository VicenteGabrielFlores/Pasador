#!/usr/bin/env python3
"""The homepage Air tile must link the newest edition file in the repo."""

import html
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def newest_edition():
    files = list(ROOT.glob("whats-in-the-air-20??-??-??.html"))
    if not files:
        raise AssertionError("no What's in the Air edition files")
    return max(files, key=lambda path: path.name)


def headlines(path):
    text = path.read_text(encoding="utf-8")
    match = re.search(
        r'<script type="application/ld\+json">\s*(.*?)\s*</script>', text, re.S
    )
    data = json.loads(match.group(1))
    return data["headline"], data["alternativeHeadline"]


class HomeAirLink(unittest.TestCase):
    def test_homepage_links_the_newest_edition(self):
        edition = newest_edition()
        href = "/" + edition.name
        english, spanish = headlines(edition)
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        match = re.search(r'<article class="tile" id="air">.*?</article>', index, re.S)
        self.assertIsNotNone(match, "Air tile missing")
        tile = match.group(0)
        hrefs = re.findall(
            r'href="(/whats-in-the-air-20\d\d-\d\d-\d\d\.html)"', tile
        )
        self.assertGreaterEqual(len(hrefs), 2, hrefs)
        self.assertTrue(all(item == href for item in hrefs), (hrefs, href))
        self.assertIn(f"<em>{english}</em>", tile)
        self.assertIn(f"<em>{spanish}</em>", tile)


class AirShareTitle(unittest.TestCase):
    def test_share_titles_render_as_whats_in_the_air(self):
        pages = [ROOT / "whats-in-the-air.html", *sorted(ROOT.glob("whats-in-the-air-20??-??-??.html"))]
        self.assertGreater(len(pages), 1)
        for path in pages:
            text = path.read_text(encoding="utf-8")
            for kind, attr in (("property", "og:title"), ("name", "twitter:title")):
                match = re.search(
                    rf'<meta {kind}="{attr}" content="([^"]*)"',
                    text,
                )
                self.assertIsNotNone(match, f"{path.name} {attr}")
                raw = match.group(1)
                self.assertNotIn("\u2019", raw, path.name)
                self.assertNotIn("\u2018", raw, path.name)
                self.assertEqual(html.unescape(raw), "What's in the Air", path.name)


if __name__ == "__main__":
    unittest.main()
