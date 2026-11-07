#!/usr/bin/env python3
"""The site icons are the supplied portrait, resized, not a new drawing."""

import hashlib
import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "portrait-vicente.png"
SUPPLIED_SHA256 = "5b6caeb741b166008926f5058fc82ec3a9fbaf24ce331ad615ca34c95ebdee91"


def resized(n):
    im = Image.open(SOURCE).convert("RGBA")
    return im.resize((n, n), Image.Resampling.LANCZOS)


class PortraitIcons(unittest.TestCase):
    def test_source_is_the_supplied_file(self):
        self.assertEqual(hashlib.sha256(SOURCE.read_bytes()).hexdigest(), SUPPLIED_SHA256)
        self.assertEqual(Image.open(SOURCE).size, (400, 400))

    def test_png_icons_are_resamples_of_that_file(self):
        for n, name in [
            (16, "favicon-16x16.png"),
            (32, "favicon-32x32.png"),
            (48, "favicon-48x48.png"),
            (96, "favicon-96x96.png"),
            (180, "apple-touch-icon.png"),
            (192, "icon-192.png"),
            (512, "icon-512.png"),
        ]:
            got = Image.open(ROOT / name).convert("RGBA")
            self.assertEqual(got.size, (n, n), name)
            self.assertEqual(list(got.getdata()), list(resized(n).getdata()), name)

    def test_ico_contains_16_32_and_48(self):
        ico = Image.open(ROOT / "favicon.ico")
        sizes = set(ico.info.get("sizes") or [])
        self.assertTrue({(16, 16), (32, 32), (48, 48)} <= sizes, sizes)

    def test_svg_embeds_the_exact_portrait(self):
        svg = (ROOT / "favicon.svg").read_text(encoding="utf-8")
        self.assertIn("image/png;base64,", svg)
        import base64
        start = svg.index("base64,") + len("base64,")
        end = svg.index('"', start)
        self.assertEqual(base64.b64decode(svg[start:end]), SOURCE.read_bytes())

    def test_wordmarks_use_the_portrait_and_signature_is_untouched(self):
        mark = 'src="/portrait-vicente.png"'
        for name in [
            "index.html",
            "historia.html",
            "familia.html",
            "poems.html",
            "articles.html",
            "la-toma.html",
            "modern-play.html",
            "whats-in-the-air.html",
            "whats-in-the-air-2026-11-06.html",
        ]:
            self.assertIn(mark, (ROOT / name).read_text(encoding="utf-8"), name)
        self.assertFalse((ROOT / "vicente-gabriel-flores-signature.png").exists())
        historia = (ROOT / "historia.html").read_text(encoding="utf-8")
        self.assertIn("Primavera de 2026", historia)
        self.assertIn("19 June 1858", (ROOT / "familia.html").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
