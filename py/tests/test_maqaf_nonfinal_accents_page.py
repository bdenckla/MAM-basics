"""The non-final-atom page (maqaf-nonfinal-accents.html) -- its committed scans.

A tree lint, one of the two test shapes this repo blesses: the page references its two figures by
relative path, so a scan that never reached ``gh-pages/accgram/img/`` gives a broken image on a
page that says nothing is wrong. Same shape as ``test_printed_decalogue_koren``'s
``test_scan_images_committed`` and its Simanim twin, down to naming the files outright.

Everything else about this page is checked by regenerating it: one run of
``main_accgram.py generate-html-maqaf-nonfinal-accents`` writes both the JSON and the HTML, and
``maqaf_nonfinal_accents_page.pin_claims`` re-derives every stated claim and raises on drift.

Run:
    .venv/Scripts/python.exe py/main_test.py py/tests/test_maqaf_nonfinal_accents_page.py
"""

from __future__ import annotations

import wlc_paths


def test_scan_images_committed() -> None:
    """Both printed-page scans the intro's figures reference are committed locally."""
    img_dir = wlc_paths.gh_pages_dir() / "accgram" / "img"
    for name in (
        # Koren's Deuteronomy appendix p. 39, the לא־תעשה line of its עליון.
        "Koren-appendix-p-39-Dt-Dec-p-trad-elyon-lo-taase.png",
        # The Simanim Tiqqun's Exodus appendix p. 246, the two lines holding both of its
        # תחתון compounds -- the second of them split across the line break.
        "Simanim-Tiqqun-p-246-Ex-Dec-p-trad-taxton-spreaders.png",
    ):
        assert (img_dir / name).is_file(), f"missing committed scan {name}"
