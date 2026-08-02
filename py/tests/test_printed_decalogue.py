"""Issue wlc-utils#52: grammar-check the printed-tradition Decalogue accentuations.

Feeds the eight vendored Decalogue readings ({Exodus, Deuteronomy} x {taxton, elyon} x
{manuscript, printed}) through the prose grammar and pins the verdict, and then pins the
``transcriptions`` section in which the output file records the same verdict for the twelve
hand-transcribed real editions:

  * every taxton chanted verse parses clean, both books and both traditions;
  * the manuscript elyon parses clean in both books (MAM's own authoritative text);
  * the *printed* elyon of *each* Decalogue has exactly one ungrammatical chanted verse --
    its opening verse, where the printed tradition merges the first two commandments into a
    single verse (nine verses total vs the manuscript's ten). That merged verse is far the
    longest of its version.

The vendored source JSON is committed here as ``in/accgram/printed_decalogue_teamim.json``, so
these FAIL rather than skip if it is absent -- printed_decalogue_fetch.py regenerates it, but a
tracked file being gone is a deletion to shout about, not an optional dependency.  See
``wlc_paths.require_sibling`` for the argument.

Run:
    .venv/Scripts/python.exe -m pytest py/tests/test_printed_decalogue.py -v
"""

from __future__ import annotations


from accgram import printed_decalogue as pd
from accgram import transcription_parse as tp

_SOF_PASUQ = "\N{HEBREW PUNCTUATION SOF PASUQ}"


def _results() -> list[pd.VersionResult]:
    return pd.check_all(pd.load_source())


def _by_key(
    results: list[pd.VersionResult],
) -> dict[tuple[str, str, str], pd.VersionResult]:
    return {(vr.book, vr.reading, vr.tradition): vr for vr in results}


def test_eight_versions_present() -> None:
    results = _results()
    keys = set(_by_key(results))
    expected = {
        (book, reading, tradition)
        for book in ("ex", "dt")
        for reading in ("taxton", "elyon")
        for tradition in ("manuscript", "printed")
    }
    assert keys == expected


def test_taxton_all_clean() -> None:
    """taxton parses clean in both books and both traditions."""
    results = _results()
    for vr in results:
        if vr.reading == "taxton":
            assert (
                vr.ungrammatical == ()
            ), f"{vr.book} taxton {vr.tradition} unexpectedly bad"


def test_manuscript_elyon_all_clean() -> None:
    """MAM's own manuscript elyon parses clean in both books."""
    results = _results()
    by_key = _by_key(results)
    for book in ("ex", "dt"):
        vr = by_key[(book, "elyon", "manuscript")]
        assert vr.ungrammatical == (), f"{book} elyon manuscript unexpectedly bad"


def test_printed_elyon_one_ungrammatical_merged_first_verse() -> None:
    """The printed elyon of each Decalogue has exactly one ungrammatical chanted verse: its
    opening verse, where the printed tradition merges the first two commandments into one
    (giving nine chanted verses vs the manuscript's ten). Note the failure is NOT mere
    length -- Deuteronomy's 55-word Sabbath elyon verse parses clean, while this merged
    verse (51 words) does not; it is the merged structure, not the size, that defeats the
    grammar."""
    results = _results()
    by_key = _by_key(results)
    for book in ("ex", "dt"):
        vr = by_key[(book, "elyon", "printed")]
        bad = vr.ungrammatical
        assert (
            len(bad) == 1
        ), f"{book} printed elyon: expected 1 ungrammatical, got {len(bad)}"
        offender = bad[0]
        assert (
            offender.index == 1
        ), f"{book} printed elyon: offender is not the first verse"
        # The merged verse runs from אנכי (commandment 1) through the end of commandment 2.
        assert offender.words[0].startswith("אָֽנֹכִי")
        assert offender.words[-1].endswith(_SOF_PASUQ)
        # The merge yields nine chanted verses (vs the manuscript's ten).
        assert len(vr.chanted_verses) == 9
        assert by_key[(book, "elyon", "manuscript")].chanted_verses.__len__() == 10


def test_total_ungrammatical_is_two() -> None:
    results = _results()
    total = sum(len(vr.ungrammatical) for vr in results)
    assert total == 2


# --------------------------------------------------------------------------- #
# The output file's transcriptions section (issue wlc-utils#52)
# --------------------------------------------------------------------------- #
def test_the_transcriptions_section_records_every_page_against_its_strand() -> None:
    """The recorded verdict for the REAL editions, which is this issue's definition of done.

    The strands' verdicts have been in this file all along; the twelve hand-transcribed printed
    Decalogues' were only ever pinned in ``test_edition_transcriptions``. So pin the section that
    records them: one entry per transcription, its Wikisource strand named, and both counts. The
    single departure is pinned exactly -- Simanim's Tiqqun Exodus appendix taḥton, chanted verse
    3, ungrammatical where its Wikisource strand is clean -- and the other eleven must show none,
    which is the
    half that would fail if a re-vendoring quietly made some other page depart.
    """
    results = _results()
    section = tp.payload_objs(tp.check_all(results))
    assert len(section) == 12
    by_stem = {entry["stem"]: entry for entry in section}
    assert by_stem["simtiq_ex_taxton"]["departures"] == [
        {"index": 3, "strand_status": "clean", "status": "ungrammatical"}
    ]
    assert [s for s, e in by_stem.items() if e["departures"]] == ["simtiq_ex_taxton"]
    # Every entry names the Wikisource strand it was checked against, and carries one chanted
    # verse record
    # per chanted verse, each with the strand's own status beside its own.
    for entry in section:
        key = (entry["book"], entry["reading"], entry["tradition"])
        assert key in _by_key(results)
        verses = entry["chanted_verses"]
        assert len(verses) == entry["chanted_verse_count"]
        assert [cv["index"] for cv in verses] == list(range(1, len(verses) + 1))
        assert all("strand_status" in cv for cv in verses)
        bad = [cv for cv in verses if cv["status"] != "clean"]
        assert len(bad) == entry["ungrammatical_count"]


def test_the_four_ungrammatical_pages_are_the_ones_printing_the_merged_verse() -> None:
    """Five ungrammatical chanted verses across the twelve, and only one is an edition's own.

    The other four are the p-trad עליון's merged opening verse, printed as the strand has it --
    which is what makes "ungrammatical somewhere" the wrong summary and ``departures`` the right
    one. Pinned because both satellite pages now say this in prose.
    """
    verdicts = tp.check_all(_results())
    shared = {
        r.stem: [cv.index for cv in r.ungrammatical]
        for r in verdicts
        if r.ungrammatical and not r.departures
    }
    assert shared == {
        "koren_dt_elyon": [1],
        "koren_ex_elyon": [1],
        "simtiq_dt_elyon": [1],
        "simtiq_ex_elyon": [1],
    }
    assert all(r.key[1:] == ("elyon", "printed") for r in verdicts if r.stem in shared)
