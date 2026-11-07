#!/usr/bin/env python3
"""Review checks for the supported historia/familia factual corrections.

These assertions lock the strings that were changed and the strings that
must stay: chapel attribution, Juana's birth year, derived ages, Benancia's
1838 birth year, children's surnames, the Hall of Honor nominator claim,
and auction-dependent dates.
"""

from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
HISTORIA = (ROOT / "historia.html").read_text(encoding="utf-8")
FAMILIA = (ROOT / "familia.html").read_text(encoding="utf-8")


class SupportedCorrections(unittest.TestCase):
    def test_margarita_wedding_date_is_19_june_1858(self):
        self.assertIn(
            "would on the nineteenth of June, eighteen hundred and fifty-eight, marry José María Flores",
            HISTORIA,
        )
        self.assertIn(
            "He married Margarita on the nineteenth of June, eighteen hundred and fifty-eight. He was twenty-eight; she was twenty-four.",
            HISTORIA,
        )
        self.assertIn(
            "In the year eighteen hundred and fifty-eight, on the nineteenth of June,",
            HISTORIA,
        )
        self.assertIn("mil ochocientos cincuenta y ocho", HISTORIA)
        self.assertIn(
            "Second Convergence · Flores &amp; Stephenson · 19 June 1858",
            FAMILIA,
        )
        self.assertNotIn("c. 1860", FAMILIA)
        self.assertNotIn(
            "on a date the parish records of the Concordia chapel preserve but which the chronicler has not yet retrieved",
            HISTORIA,
        )

    def test_josefina_surname_on_historia(self):
        self.assertEqual(HISTORIA.count("Josefina Samaniego Siqueiros"), 4)
        self.assertEqual(HISTORIA.count("Josefina Samaniego de Flores"), 6)
        self.assertIn("grandmother Josefina Samaniego.", HISTORIA)
        self.assertEqual(HISTORIA.count("Flores-Samaniego"), 3)
        self.assertNotIn("Josefina Gómez Velarde", HISTORIA)
        self.assertIn(
            "her mother was Guadalupe Siqueiros, sister of Jesusita Siqueiros de Hart.",
            HISTORIA,
        )

    def test_benancia_death_and_marriage_keep_1838(self):
        self.assertEqual(HISTORIA.count("Benancia (1838 – 1918)"), 2)
        self.assertNotIn("Benancia (1838 – 1898)", HISTORIA)
        self.assertIn(
            "In the year eighteen hundred and sixty-five, on the sixteenth of August, <em>Benancia Stephenson",
            HISTORIA,
        )
        self.assertIn("aged twenty-five", HISTORIA)
        self.assertNotIn("eighteen hundred and sixty-three", HISTORIA)

    def test_albert_french_death_year_keeps_birth_approximation(self):
        self.assertEqual(HISTORIA.count("(c. 1820 – 1877)"), 2)
        self.assertNotIn("(c. 1820 – 1880s)", HISTORIA)
        self.assertIn("He died in eighteen hundred and seventy-seven.", HISTORIA)
        self.assertIn("approximately Hugh", HISTORIA)


class HeldText(unittest.TestCase):
    def test_chapel_attribution_unchanged(self):
        self.assertIn("the chapel her family had built two years before", HISTORIA)
        self.assertIn(
            "She commissioned the chapel of San José de Concordia el Alto in eighteen hundred and fifty-four.",
            HISTORIA,
        )
        self.assertIn("The chapel Juana had built.", HISTORIA)
        self.assertNotIn("Hugh had built for Juana", HISTORIA)
        self.assertNotIn("husband had built for her", HISTORIA)
        self.assertIn(
            "Built the first Catholic church on the east bank of the Río Grande",
            FAMILIA,
        )
        self.assertIn(
            "Juana María Ascárate brought the land, the name, and built the chapel.",
            FAMILIA,
        )

    def test_juana_birth_conflict_unchanged(self):
        self.assertIn(
            "Born in El Paso del Norte in eighteen hundred and nine (by the family chart; the public record gives eighteen hundred).",
            HISTORIA,
        )
        self.assertIn("1809 — 6 Feb 1856", FAMILIA)

    def test_scene_ages_and_derived_years_unchanged(self):
        self.assertIn("He was twenty-eight; she was twenty-four.", HISTORIA)
        self.assertIn("Margarita Stephenson — aged twenty-four", HISTORIA)
        self.assertIn("José María Flores — aged twenty-eight", HISTORIA)
        self.assertIn("Margarita is twenty-four. José María is twenty-eight.", HISTORIA)
        self.assertIn("from the second year of the marriage forward", HISTORIA)
        self.assertIn("the second year of Margarita and José María", HISTORIA)
        self.assertIn("French would be, four years later,", HISTORIA)
        self.assertIn("aged thirty-three, married Josefina Samaniego Siqueiros, aged twenty", HISTORIA)

    def test_child_surnames_and_cousinship_unchanged(self):
        self.assertIn("María del Carmen Flores Gómez", HISTORIA)
        self.assertIn("José Jesús Flores Gómez Jr.", HISTORIA)
        self.assertIn("Carlos Flores Gómez", HISTORIA)
        self.assertNotIn("Flores Samaniego", HISTORIA)
        self.assertIn("María Manuela Gómez Velarde", HISTORIA)
        self.assertIn("Gómez Velarde family of Chihuahua", HISTORIA)
        self.assertIn("Josefa <em>Samaniego Siqueiros</em>", FAMILIA)
        self.assertIn("1863 — 1951", FAMILIA)
        self.assertIn("María Manuela <em>Gómez Velarde</em>", FAMILIA)

    def test_nominator_and_auction_wording_unchanged(self):
        nominator = "who nominated and successfully inscribed these ancestors into the El Paso County Historical Society"
        self.assertIn(nominator, FAMILIA)
        self.assertIn(nominator, (ROOT / "index.html").read_text(encoding="utf-8"))
        self.assertIn(
            "on a date in the late summer or early autumn the chronicler has not yet retrieved",
            HISTORIA,
        )
        self.assertIn("federal auction in 1867", FAMILIA)
        self.assertIn("federal marshal's sale in 1867", FAMILIA)
        self.assertIn("around 1860", FAMILIA)

    def test_other_1860s_records_not_rewritten(self):
        self.assertIn("mil ochocientos sesenta y uno", HISTORIA)
        self.assertIn("mil ochocientos sesenta y siete", HISTORIA)
        self.assertIn("born at Concordia in eighteen hundred and sixty-two", HISTORIA)

    def test_only_the_two_pages_and_this_test_change(self):
        diff = subprocess.check_output(
            ["git", "diff", "--name-only", "HEAD"],
            cwd=ROOT,
            text=True,
        ).split()
        allowed = {
            "historia.html",
            "familia.html",
            "tests/historical_corrections_review.py",
        }
        self.assertTrue(set(diff) <= allowed, diff)


if __name__ == "__main__":
    unittest.main()
