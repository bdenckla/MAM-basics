r"""Where the two תחתון strands of one Decalogue part, site by site, derived live.

The three printed-Decalogue pages all count this one divergence set, and until now each
counted it its own way with no stated criterion -- 3 on the hub, 5 on the Koren page, 8 in
``tests/test_edition_transcriptions.py`` -- so no two of the three agreed and none could be
checked.  A 2026-07-25 claim-extraction audit of the rendered prose found the hub's "three"
flatly false against the table printed directly beneath it.  This module is the answer: ONE
criterion, applied once, with the counts derived from the vendored data instead of typed into
three prose sites.

**The criterion.**  A difference SITE is one chanted word at which the two strands' text
differs.  Where the strands put their maqafs differently -- the m-trad's two chanted words לא and
תעשה against the p-trad's single chanted word, the maqaf compound לא־תעשה -- the site is the
shortest run of chanted words on each side whose letter skeletons match, so a maqaf counts as ONE
site rather than as two or three coincidental differences.  ``diff_sites`` does that alignment.  Note that a maqaf
difference IS a site here and always has been: this module was already counting on the single
scale that the three pages now state to the reader (``MAQAF_IS_THE_LAST_RUNG``).

**What the criterion yields for Deuteronomy** (``dt_taxton_diff_counts``, pinned in
``DT_TAXTON_DECOMPOSITION`` and re-derived on every page generation):

  * **12** sites over the whole Decalogue, which decompose exactly:
  * **4** coupled to the one structural difference -- the p-trad closing its first chanted verse
    at מבית עבדים -- on אנכי, אלהיך, מבית and עבדים (``BOUNDARY_SKELETONS``);
  * **7** inside a single stretch of the Sabbath commandment, which is what
    ``printed_decalogue_page``'s appendix table displays;
  * **1** of vocalization only, the qamats/patax of לא תרצח, which changes no mark.

That the remaining seven really do all fall inside the Sabbath commandment is not assumed: the
count check compares the whole-Decalogue remainder against the sites found inside the Sabbath
chanted verse itself, so a difference appearing anywhere else would fail the build.

Exodus's own תחתון pair has 5 sites -- the same 4 boundary ones plus the same vocalization one,
and nothing in its Sabbath commandment at all, which is why the Koren and Simanim pages say an
Exodus Decalogue cannot adjudicate the Shabbat commandment.

Pure computation, like ``printed_decalogue_strands``: no HTML, and every accessor raises rather
than returns a wrong answer, so a re-vendoring that moved a difference fails at page-generation
time instead of leaving three pages' prose describing the old set.
"""

from __future__ import annotations

from accgram import printed_decalogue as pd
from accgram import printed_decalogue_strands as pds
from mb_cmn import hebrew_accent_strip as has

# One difference site: the run of chanted words each strand shows there, m-trad first.  Either
# side is usually a single chanted word; a side has two exactly where the other strand joins the
# same two atoms by maqaf.
Site = tuple[tuple[str, ...], tuple[str, ...]]

# The four chanted words the one structural difference drags along: the p-trad closes its first chanted
# verse at מבית עבדים where the m-trad runs on to על־פני, and that moves the accents on these
# four.  Single-sourced here because the hub's appendix both EXCLUDES them from its catalogue (they
# are the verdict section's own point) and names them in prose, and because the count check below
# classifies a site by asking whether its skeleton is one of them.
BOUNDARY_SKELETONS: tuple[str, ...] = ("אנכי", "אלהיך", "מבית", "עבדים")

# The letter skeleton that locates the Sabbath commandment's chanted verse: it is the only verse
# in either dt תחתון strand containing בהמתך.  Matched as a substring of a chanted word's skeleton,
# since the chanted word itself is the maqaf compound וכל־בהמתך.
_SABBATH_SKELETON = "בהמתך"


def diff_sites(m_words: tuple[str, ...], p_words: tuple[str, ...]) -> list[Site]:
    """The sites at which two strands' chanted-word sequences part, aligned by letter skeleton.

    The two strands are the same letters throughout -- they differ only in accents, vowels and
    where they put a maqaf -- so a difference is located by walking both sides in step and, on
    any disagreement, growing each side one chanted word at a time until the two skeletons match
    again.  That is what makes a maqaf difference one site rather than two or three coincidental
    differences: לא + תעשה on one side faces the single לא־תעשה on the other, and both sides
    advance past it together.  This alignment is where the trio's "counted once, at the atom whose
    marking changed" rule is actually implemented.

    Raises if the skeletons cannot be reconciled or a side runs out of chanted words -- the strands would
    then no longer be the same text, which is a re-vendoring to look at rather than to render.
    """
    sites: list[Site] = []
    i = j = 0
    while i < len(m_words) or j < len(p_words):
        if i < len(m_words) and j < len(p_words) and m_words[i] == p_words[j]:
            i, j = i + 1, j + 1
            continue
        take_m = take_p = 1
        while True:
            skel_m = "".join(pds.base_skeleton(w) for w in m_words[i : i + take_m])
            skel_p = "".join(pds.base_skeleton(w) for w in p_words[j : j + take_p])
            if skel_m == skel_p:
                break
            grow_m = len(skel_m) < len(skel_p)
            room = (
                (i + take_m < len(m_words)) if grow_m else (j + take_p < len(p_words))
            )
            if not room:
                raise AssertionError(
                    "cannot align the two תחתון strands at m-trad word "
                    f"{i} / p-trad word {j}: skeletons {skel_m!r} vs {skel_p!r} "
                    "-- the vendored readings drifted"
                )
            if grow_m:
                take_m += 1
            else:
                take_p += 1
        sites.append((m_words[i : i + take_m], p_words[j : j + take_p]))
        i, j = i + take_m, j + take_p
    return sites


def _words(
    results: list[pd.VersionResult], book: str, tradition: str
) -> tuple[str, ...]:
    by_key = {(vr.book, vr.reading, vr.tradition): vr for vr in results}
    vr = by_key[(book, "taxton", tradition)]
    return tuple(w for cv in vr.chanted_verses for w in cv.words)


def taxton_diff_sites(results: list[pd.VersionResult], book: str) -> list[Site]:
    """Every site at which one book's m-trad and p-trad תחתון strands part."""
    return diff_sites(
        _words(results, book, "manuscript"), _words(results, book, "printed")
    )


def sabbath_verse_words(
    results: list[pd.VersionResult], tradition: str
) -> tuple[str, ...]:
    """The words of the Deuteronomy תחתון Sabbath chanted verse, pulled live from the data.

    Asserts exactly one match so a data change that moved or renumbered the verse fails the
    build rather than silently mis-rendering.  (Moved here from ``printed_decalogue_page`` when
    the count check below needed the same verse.)
    """
    by_key = {(vr.book, vr.reading, vr.tradition): vr for vr in results}
    vr = by_key[("dt", "taxton", tradition)]
    sabbath = [
        cv
        for cv in vr.chanted_verses
        if any(_SABBATH_SKELETON in pds.base_skeleton(w) for w in cv.words)
    ]
    if len(sabbath) != 1:
        raise AssertionError(
            f"dt taxton {tradition}: expected exactly 1 Sabbath verse (skeleton "
            f"{_SABBATH_SKELETON}), found {len(sabbath)} -- the vendored readings drifted"
        )
    return sabbath[0].words


def is_vocalization_only(site: Site) -> bool:
    """True where the site's two sides carry the same marks and differ only in vowel pointing.

    Compared through the shared strip kernel under ``METEG_ALL``, which keeps letters, every
    accent, maqaf, sof pasuq, the paseq/legarmeh stroke and every meteg -- i.e.
    everything a cantillation difference could live in -- and drops exactly the vowels, dagesh,
    shin/sin dots and rafe.  So the one Decalogue site this is true of, the qamats/patax of
    לא תרצח, is separated from the accent differences by what the marks are rather than by name.
    """

    def marks(words: tuple[str, ...]) -> str:
        return "".join(has.strip_to_accents(w, keep_meteg=has.METEG_ALL) for w in words)

    return marks(site[0]) == marks(site[1])


def _classify(sites: list[Site]) -> dict[str, int]:
    boundary = vocalization = 0
    for site in sites:
        skeleton = "".join(pds.base_skeleton(w) for w in site[0])
        if skeleton in BOUNDARY_SKELETONS:
            boundary += 1
        elif is_vocalization_only(site):
            vocalization += 1
    return {
        "total": len(sites),
        "boundary": boundary,
        "vocalization": vocalization,
        "sabbath": len(sites) - boundary - vocalization,
    }


# The Deuteronomy תחתון pair's decomposition under the criterion in the module docstring, pinned
# so the prose of all three pages can state these numbers as words and still not be able to drift
# from them.  The Exodus pair is pinned beside it because the Koren and Simanim pages both turn on
# its "nothing in the Sabbath commandment": with 4 boundary sites and 1 vocalization site there is
# no remainder, which is exactly why an Exodus Decalogue cannot adjudicate that commandment.
DT_TAXTON_DECOMPOSITION = {
    "total": 12,
    "boundary": 4,
    "sabbath": 7,
    "vocalization": 1,
}
EX_TAXTON_DECOMPOSITION = {
    "total": 5,
    "boundary": 4,
    "sabbath": 0,
    "vocalization": 1,
}


def dt_taxton_diff_counts(results: list[pd.VersionResult]) -> dict[str, int]:
    """The Deuteronomy decomposition, derived live and checked against the pin above.

    Two things are checked, not one.  The counts must match ``DT_TAXTON_DECOMPOSITION``; and the
    seven non-boundary, non-vocalization sites must be exactly the sites found inside the Sabbath
    chanted verse, which is what verifies the pages' claim that the differences CLUSTER there
    rather than merely that seven of them exist somewhere.
    """
    counts = _classify(taxton_diff_sites(results, "dt"))
    if counts != DT_TAXTON_DECOMPOSITION:
        raise AssertionError(
            f"the two dt תחתון strands now part at {counts}, not "
            f"{DT_TAXTON_DECOMPOSITION} -- the vendored readings drifted, and the prose of all "
            "three printed-Decalogue pages states these numbers"
        )
    in_sabbath = len(
        diff_sites(
            sabbath_verse_words(results, "manuscript"),
            sabbath_verse_words(results, "printed"),
        )
    )
    if in_sabbath != counts["sabbath"]:
        raise AssertionError(
            f"{counts['sabbath']} dt תחתון differences fall outside the boundary words and the "
            f"vocalization, but {in_sabbath} fall inside the Sabbath chanted verse -- they no "
            "longer cluster there, and the pages say they do"
        )
    ex_counts = _classify(taxton_diff_sites(results, "ex"))
    if ex_counts != EX_TAXTON_DECOMPOSITION:
        raise AssertionError(
            f"the two ex תחתון strands now part at {ex_counts}, not "
            f"{EX_TAXTON_DECOMPOSITION} -- the vendored readings drifted, and the Koren and "
            "Simanim pages say an Exodus Decalogue reaches no Shabbat difference"
        )
    return counts
