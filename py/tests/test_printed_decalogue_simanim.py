"""Issue wlc-utils#62: the Simanim-Decalogue page (printed-decalogue-simanim.html).

The four cantillation strands of the opening אנכי…מצותי span are derived live from the vendored
``in/accgram/printed_decalogue_teamim.json`` by the shared ``printed_decalogue_strands`` module:
for each Exodus reading it reads the first chanted verse and derives the accent on אנכי (first
word) and עבדים.  These tests pin that derivation (which now lives on the strands module, not on
this page) and confirm the Simanim page body renders.

The vendored source JSON is committed here, so these FAIL rather than skip if it is absent --
see ``test_printed_decalogue``'s docstring and ``wlc_paths.require_sibling``.

Run:
    .venv/Scripts/python.exe -m pytest py/tests/test_printed_decalogue_simanim.py -v
"""

from __future__ import annotations


from accgram import printed_decalogue as pd
from accgram import printed_decalogue_simanim_page as sim
from accgram import printed_decalogue_strands as pds
from accgram import transcription_parse as tp
from accgram import transcription_verdict_column as tvc

import wlc_paths


def _results() -> list[pd.VersionResult]:
    return pd.check_all(pd.load_source())


def test_four_readings_derive_expected_accents() -> None:
    """אנכי / עבדים accents, derived from the data, match the established four readings.

    ``pds.resolve_readings`` itself raises if a derived accent diverges from its expected value,
    so this both exercises the derivation and pins the (accent-on-אנכי, accent-on-עבדים) pairs.
    """
    readings = pds.resolve_readings(_results())
    got = {r.name: (r.anokhi_accent, r.avadim_accent) for r in readings}
    assert got == {
        "m-trad taḥton": ("pashta", "etnaḥta"),
        "m-trad elyon": ("tipeḥa", "silluq"),
        "p-trad taḥton": ("tipeḥa", "silluq"),
        "p-trad elyon": ("pashta", "revia"),
    }


def test_printed_taxton_equals_manuscript_elyon() -> None:
    """The page's headline identity: p-trad taḥton = m-trad elyon on both boundary words.

    The identity is SPAN-LIMITED -- it holds only through עבדים. At the אנכי…מצותי span's other
    signal word, על־פני, the two strands part (p-trad taḥton silluq, m-trad elyon revia), which is
    what gives each its own row in the companion page's four-strands table. See
    ``test_printed_decalogue_page.test_signal_pairs_identify_strands``."""
    readings = {r.name: r for r in pds.resolve_readings(_results())}
    pt, me = readings["p-trad taḥton"], readings["m-trad elyon"]
    assert (pt.anokhi_accent, pt.avadim_accent) == (me.anokhi_accent, me.avadim_accent)


def test_avadim_located_within_each_first_verse() -> None:
    """עבדים is found (by letter skeleton) in every reading's first chanted verse --
    verse-finally in the standalone readings, mid-verse in the merged ones."""
    readings = pds.resolve_readings(_results())
    for r in readings:
        assert pds.base_skeleton(r.avadim_word) == pds.AVADIM


def test_body_renders() -> None:
    """The full Simanim page body builds without error and is non-empty.

    It needs the grammar-check results again, and for a different reason than it once did: not to
    tabulate the strands (that moved to the companion page) but because each verdict table's last
    column states a transcription's verdict against its Wikisource strand's (issue wlc-utils#52). A row
    naming a stem
    with no committed transcription fails here, on the lookup.
    """
    source = pd.load_source()
    verdicts = tvc.by_stem(tp.check_all(pd.check_all(source)))
    body = sim.render_body_contents(source, verdicts)
    assert isinstance(body, tuple) and len(body) > 0


def test_scan_images_committed() -> None:
    """Both SimTiq note scans are committed locally (the page references them by relative path,
    not the issue CDN)."""
    img_dir = wlc_paths.gh_pages_dir() / "accgram" / "img"
    for name in (
        "Simanim-Tiqqun-p-083-Ex-Dec-elyon-sidenote.png",
        "Simanim-Tiqqun-p-246-Ex-Dec-p-trad-taxton-footnote.png",
    ):
        assert (img_dir / name).is_file(), f"missing committed scan {name}"
