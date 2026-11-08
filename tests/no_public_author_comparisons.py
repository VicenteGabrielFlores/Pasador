#!/usr/bin/env python3
"""Public pages must not rank this work against famous authors.

Shelf lines, tribute voice, and "in the tradition of" claims are removed.
Historical mentions, scholarly sources, attributed quotations, and the
manuscript's own fiction stay.
"""

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

PUBLIC = [
    p
    for p in ROOT.iterdir()
    if p.suffix in {".html", ".md", ".xml", ".txt"} and p.is_file()
]

# Phrases that were public self-comparison or shelf positioning.
ABSENT = [
    "García Márquez",
    "Garcia Marquez",
    "Garcíamarqu",
    "Garciamarqu",
    "Dostoevsky",
    "Dostoyevsky",
    "Dostoievsk",
    "James Clavell",
    "Clavell",
    "One Hundred Years of Solitude",
    "Cien años de soledad",
    "magical realism",
    "realismo mágico",
    "Pedro Páramo",
    "Juan Rulfo",
    "Rulfo",
    "Anthony Doerr",
    "Cloud Cuckoo",
    "Simon Jimenez",
    "Vanished Birds",
    "Bullet Swallower",
    "House of Broken Angels",
    "The Old Gringo",
    "Carlos Fuentes",
    "Elizabeth Gonzalez James",
    "Luis Alberto Urrea",
    "Wolf Hall",
    "Ragtime",
    "literary godfather",
    "tribute voice",
    "deliberate tribute",
    "On the Shelf",
    "In the Conversation",
    "Comparable to",
    "In the tradition of",
]


class PublicComparisonsRemoved(unittest.TestCase):
    def test_comparison_phrases_are_absent(self):
        hits = []
        for path in PUBLIC:
            text = path.read_text(encoding="utf-8")
            for phrase in ABSENT:
                if phrase in text:
                    hits.append(f"{path.name}: {phrase}")
        self.assertEqual(hits, [])


class PreservedPassages(unittest.TestCase):
    def test_byline_purchase_links_and_nov8_air_stay(self):
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        toma = (ROOT / "la-toma.html").read_text(encoding="utf-8")
        air = (ROOT / "whats-in-the-air-2026-11-08.html").read_text(encoding="utf-8")
        self.assertIn("Vicente Gabriel Flores", index)
        self.assertIn("portrait-vicente.png", index)
        self.assertIn("vicente-gabriel-flores-signature.png", air)
        self.assertIn("Handwritten signature of Vicente Gabriel Flores", air)
        self.assertIn("https://www.amazon.com/dp/B0H2NJC11X", toma)
        self.assertIn("https://www.amazon.com/dp/B0H2P3ZZMS", toma)
        self.assertIn("https://www.amazon.com/dp/B0H2PHBFGV", toma)
        self.assertIn("What Passes Through", air)
        self.assertIn("November 8, 2026", air)

    def test_historical_and_quoted_author_mentions_stay(self):
        chronicle = (ROOT / "PASADOR_Chronicles_Complete.md").read_text(encoding="utf-8")
        historia = (ROOT / "historia.html").read_text(encoding="utf-8")
        manifest = (ROOT / "the-manifest.html").read_text(encoding="utf-8")
        # Canary wine in the historical record, not a model for the novel.
        self.assertIn("the sweet amber wine that Shakespeare called the cup of Canary", chronicle)
        self.assertIn("The Merry Wives of Windsor", chronicle)
        self.assertIn("mentioned by Shakespeare and by Marlowe", chronicle)
        # Period chronicle method, and a scholarly source who shares a surname.
        self.assertIn("en el modo de los cronistas de las Indias", chronicle)
        self.assertIn("en tributo al castellano escrito de cada época", chronicle)
        self.assertIn("Fuentes, Armando Curbelo.", chronicle)
        self.assertIn("García, Mario T.", historia)
        # A life episode and an attributed closing quotation.
        self.assertIn("The Tale of Genji", chronicle)
        self.assertIn("cuando me senté a escribir PASADOR", chronicle)
        self.assertIn("I owe to **Elon Musk**", chronicle)
        # Figures inside the story, not a shelf.
        self.assertIn("Ambrose Bierce", manifest)
        self.assertIn("does not distinguish between Villa, or Hollywood, or Ambrose Bierce", manifest)


if __name__ == "__main__":
    unittest.main()
