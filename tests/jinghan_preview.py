#!/usr/bin/env python3
"""Private-preview checks for the iron doors and the crawlable catalog."""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = (ROOT / "index.html").read_text(encoding="utf-8")
FAMILIA = (ROOT / "familia.html").read_text(encoding="utf-8")


class Doors(unittest.TestCase):
    def test_unlock_script_and_preload_come_before_paint(self):
        self.assertIn('localStorage.getItem("doorUnlocked")', INDEX)
        self.assertLess(INDEX.index("doorUnlocked"), INDEX.index("<body"))
        self.assertIn(
            'rel="preload" as="image" href="/assets/art/jinghan-gold-leaf-painting-vicente-gabriel-flores-1584.jpg"',
            INDEX,
        )

    def test_jinghan_is_pixel_locked(self):
        self.assertIn('viewBox="0 0 1584 672"', INDEX)
        self.assertIn('width="1584" height="672"', INDEX)
        self.assertIn("aspect-ratio:1584 / 672", (ROOT / "assets/doors.css").read_text(encoding="utf-8"))

    def test_catalog_is_not_hidden(self):
        catalog = INDEX.split('id="catalog"', 1)[1].split("</section>", 1)[0]
        self.assertNotIn("display:none", catalog)
        self.assertNotIn("display: none", catalog)
        self.assertNotIn("visibility:hidden", catalog)
        self.assertNotIn("visibility: hidden", catalog)
        self.assertIn("The Harness-Maker", catalog)
        self.assertIn("CONCORDIA: la heredera", catalog)
        self.assertIn("Primary Documentary Evidence", catalog)
        self.assertIn("Verified Family Chronicles", catalog)
        self.assertIn("Dramatized Literature", catalog)

    def test_bolt_years_and_motion(self):
        self.assertIn("1706 · 1731 · 1836 · 1858 · 1913 · 2026 · ∞", INDEX)
        css = (ROOT / "assets/doors.css").read_text(encoding="utf-8")
        self.assertIn("0.35s", css)
        self.assertIn("0.55s", css)
        self.assertIn("prefers-reduced-motion", css)


class Books(unittest.TestCase):
    def test_pages_schema_and_sitemap(self):
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        for name in ("the-harness-makers-son.html", "pasador.html", "concordia.html"):
            page = (ROOT / name).read_text(encoding="utf-8")
            self.assertIn('"@type": "Book"', page)
            self.assertIn('"@id": "https://vicentegabrielflores.com/#author"', page)
            self.assertIn("Verify the history", page)
            self.assertIn(f"https://vicentegabrielflores.com/{name}", sitemap)
            data = json.loads(re.search(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', page, re.S).group(1))
            self.assertEqual(data["@type"], "Book")
            self.assertNotIn("isbn", json.dumps(data).lower())


class Familia(unittest.TestCase):
    def test_founding_families_count_and_children(self):
        self.assertIn("Curbelo", FAMILIA)
        self.assertIn("Granado", FAMILIA)
        self.assertIn("Mission of Guadalupe", FAMILIA)
        self.assertIn("Second Convergence · Flores &amp; Stephenson · 19 June 1858", FAMILIA)
        self.assertIn("Their children.", FAMILIA)
        self.assertIn("Manuel, Carlos, Ramón, Antonio, Alfredo, Carmen, Albert", FAMILIA)
        self.assertIn("Eleven", FAMILIA)
        self.assertNotIn("Sixth generation", FAMILIA)
        self.assertNotIn("Twelve <em>Generations</em>", FAMILIA)


if __name__ == "__main__":
    unittest.main()
