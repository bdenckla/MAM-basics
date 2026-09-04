r"""``gh-pages/post-stress-meteg.html`` -- MAM's metegs after the primary stress.

The page for ``accgram.post_stress_meteg``'s survey.  That module measures; this one renders,
and takes every figure it prints from the survey rather than from a constant of its own.
``pin_claims`` re-derives each figure the prose states and raises on drift, which is the shape
``maqaf_nonfinal_accents_page.pin_claims`` established.

A LOOSE PAGE AT THE DEPLOY ROOT, beside ``index.html`` and ``unicode-proposals.html``, which
is Ben's decision of 2026-09-03 (``doc/PLAN-post-stress-meteg-page-and-holman-m23.md``).  Not
under ``gh-pages/wlc/``: that prefix exists so wlc-utils' frozen redirect stubs can rewrite
onto ``MAM-basics/wlc/<path>``, a page published here after the 2026-08-17 move earns no stub,
and this page's corpus is MAM rather than WLC.

IT LINKS TWO STYLESHEETS, and the second is the accgram one.  ``gh-pages/style.css`` is the
deploy root's own, whose whole job is the light/dark switching; ``gh-pages/wlc/style.css``
supplies the ``lang="hbo"`` font at the size that makes accents legible, the italic for a
romanized accent name, and the numeric-cell alignment.  A stylesheet's ``@font-face`` URL
resolves against the stylesheet, so ``woff2/Taamey_D.woff2`` reaches the font from here too.

WHY THIS PAGE SHOWS POINTED HEBREW where the accgram pages show letters and accents alone.
``accents_and_letters`` drops U+05BD along with the vowels, and U+05BD is this page's whole
subject; and what the page is about is which SYLLABLE a mark falls in, which a reader cannot
see without the vowels that make the syllables.  Both of the page's three structural types
are named for a vowel or a syllable shape, so the vowel is the point of the comparison here in
the sense the house rule allows for.  Every form is lifted from the corpus at generation time
-- ``mam_form``, MAM's text -- and none is typed here.

THE PAGE QUOTES NEITHER YEIVIN NOR BREUER.  The plan permits bounded excerpts and does not
require them; the sections are cited by number and their content paraphrased, so no private
source text reaches a public page.  ``_EXCERPTS`` is empty and ``_excerpt_accounting`` asserts
that it is, which is the plan's requirement for a page with no excerpts.
"""

from __future__ import annotations

from pathlib import Path

from accgram import post_stress_meteg as psm
from accgram.almost_errors_html_shared import ref_abbrev, wrap_hebrew_runs
from accgram import rtms_report
from author_site import site_data
from mb_cmn import paths
from mb_cmn import provenance
from mb_misc import mb_html
from py_html.my_html_span_romanized import rmn
from wlc_cmn.wlc_book_codes import wlc_bb_to_bk39id
from mb_cmn import bib_locales as tbn

_FNAME = site_data.POST_STRESS_METEG_FNAME
_TITLE = site_data.POST_STRESS_METEG_TITLE
_DUAL_CANTILLATION_APPENDIX_ID = "dually-cantillated-passages"

# The M23 card's link lands here, so the identifier is half of that card's href and cannot be
# renamed alone: py/py_render/rt_suggestion_context.py builds the other half from the same
# site_data constant.
M23_SECTION_ID = site_data.POST_STRESS_METEG_M23_ID

# Every Hebrew cell says so, whatever else it says.  The whole-column rule: blank cells
# included, the English heading left alone, no class and no stylesheet rule.
_HEBREW_CELL = {"dir": "rtl"}
_NUMERIC_CELL = {"class": "numeric"}

# No excerpt from either book appears on this page.  Kept as a structure rather than as a bare
# absence so the accounting below has something to count, and so an excerpt added later is
# added in one place with its source beside it.
_EXCERPTS: tuple[tuple[str, str], ...] = ()

_MAX_WORDS_PER_EXCERPT = 150
_MAX_WORDS_IN_ALL_EXCERPTS = 300

_PROSE = psm.SYSTEM_PROSE
_POETIC = psm.SYSTEM_POETIC

# The two verses the page names outside its tables.  The survey records their chanted words as
# MAM has them today, under ``currency.focus_verses``, so the forms shown here are lifted like
# every other form on the page.
_M23_VERSE = "is23:12"
_POST_SILLUQ_VERSE = "1s17:5"

_ITM_GLOSS = "Yeivin's Introduction to the Tiberian Masorah"
_COS_GLOSS = "Breuer's The Cantillation of Scripture"

# Yeivin and Breuer on each of the three types, and how each book grades it.  The pairing is
# the M23 evidence note's, doc/holman-meteg-m23-isaiah-23-12.md; both books are cited for
# every type, so no row rests on one source.
_TYPE_SOURCES = {
    psm.TYPE_OPEN: ("§332", "§3(j), §§46-47", "optional in both books"),
    psm.TYPE_GUTTURAL: ("§354", "§3(b), §§9-10", "obligatory in Breuer"),
    psm.TYPE_CLOSED_TSERE: (
        "§338, fed by §308",
        "§3(a), §§5-8",
        "obligatory in both books",
    ),
}


def gen_html_file(out_dir: Path | None = None, *, trust_survey: bool = False) -> str:
    """Write the page.  Returns the path written.

    ``trust_survey`` reads the tracked ``out/accgram/post-stress-meteg.json`` instead of
    recomputing, which is how ``main_0_mega.py`` renders this page without the MAM-private
    clone the survey needs.  Off by hand, so a standalone run still derives the page from the
    corpus rather than from a file.
    """
    survey = psm.load_survey() if trust_survey else psm.build_survey()
    pin_claims(survey)
    top_dir = paths.gh_pages_dir() if out_dir is None else Path(out_dir)
    out_path = str(top_dir / _FNAME)
    write_ctx = mb_html.WriteCtx(
        _TITLE,
        out_path,
        css_hrefs=(site_data.CSS_HREF, site_data.ACCGRAM_CSS_HREF),
        body_class="centered-page",
        html_comment=provenance.generated_html_comment(__file__),
    )
    mb_html.write_html_to_file(build_body(survey), write_ctx)
    return out_path


def build_body(survey: dict) -> list:
    """The page, section by section, every figure in it read off ``survey``."""
    return [
        mb_html.heading_level_1(_TITLE),
        *_opening(survey),
        *_census(survey),
        *_by_type(survey),
        *_every_case(survey),
        *_m23(survey),
        *_post_silluq(survey),
        *_sources_and_limits(survey),
        *_dual_cantillation_appendix(survey),
    ]


# --- the numbers, all of them read off the survey ------------------------------


def _count(survey: dict, system: str, category: str) -> int:
    return survey["counts"][system][category]


def _post_stress(survey: dict, system: str | None = None) -> list[dict]:
    return [
        one
        for one in survey["post_stress"]
        if system is None or one["system"] == system
    ]


def _both(survey: dict, category: str) -> int:
    return _count(survey, _PROSE, category) + _count(survey, _POETIC, category)


def _dual_cantillation_facts(survey: dict, bcv: str) -> dict:
    """The source-derived facts for one numbered verse with both cantillation strands."""
    return survey["dual_cantillation"]["facts_by_numbered_verse"][bcv]


def _dual_cantillation(survey: dict) -> dict:
    """The one-reading method and cant-alef/cant-bet comparison."""
    return survey["dual_cantillation"]


def _by_type_count(survey: dict, kind: str) -> int:
    return sum(
        survey["post_stress_by_structural_type"][system][kind]
        for system in (_PROSE, _POETIC)
    )


def _following_example(record: dict, kind: str) -> tuple:
    """The following MAM chanted word where the source-derived type requires it."""
    if kind not in (psm.TYPE_OPEN, psm.TYPE_GUTTURAL):
        return _hebrew_cell(None)
    following = record["following_mam_form"]
    assert (
        following is not None
    ), f"{record['bcv']}: no MAM form for the following chanted word of {kind}"
    return _hebrew_cell(following)


def _example_of(survey: dict, kind: str) -> dict:
    """The first record of a type, in the corpus's order, as that type's specimen.

    First rather than chosen: a hand-picked specimen is a claim with nothing behind it, and
    the whole set is on the page below anyway.
    """
    for record in survey["post_stress"]:
        if record["structural_type"] == kind:
            return record
    raise AssertionError(f"no post-stress record of type {kind!r} to show")


def pin_claims(survey: dict) -> None:
    """Re-derive every figure the prose states, and raise on drift.

    The page's sentences say things like "231 chanted words"; each such figure is computed
    from the survey here as well as where it is rendered, so a corpus that moves under the
    page fails the build rather than publishing a stale number.
    """
    post_stress = survey["post_stress"]
    assert len(post_stress) == _both(
        survey, "meteg after the stressed syllable"
    ), "the post-stress records and the post-stress count disagree"
    by_type = sum(_by_type_count(survey, kind) for kind in _TYPE_SOURCES)
    assert by_type + _by_type_count(survey, psm.TYPE_UNCLASSIFIED) == len(
        post_stress
    ), "the structural types do not partition the post-stress records"
    assert survey["post_silluq"]["in_mam"] == sum(
        1 for one in post_stress if one["has_sof_pasuq"]
    ), "the post-silluq count and the records disagree"
    exodus = _dual_cantillation_facts(survey, "ex20:2")
    assert exodus["same_chanted_word_group_count"]
    assert all(len(branch) == 1 for branch in exodus["first_same_chanted_word_group"])
    genesis = _dual_cantillation_facts(survey, "gn35:22")
    assert genesis["same_chanted_word_group_count"] == 5
    dual_cantillation = _dual_cantillation(survey)
    comparison = dual_cantillation["comparison_counts"]
    assert dual_cantillation["counted_cantillation"] == psm.CANT_ALEF
    for category in (
        "chanted words checked",
        "meteg before the stressed syllable",
        "meteg after the stressed syllable",
    ):
        assert comparison[psm.CANT_ALEF][category] == _both(survey, category)
    assert (
        comparison[psm.CANT_ALEF]["meteg after the stressed syllable"]
        == comparison[psm.CANT_BET]["meteg after the stressed syllable"]
    )
    for kind in (*_TYPE_SOURCES, psm.TYPE_UNCLASSIFIED):
        if _by_type_count(survey, kind):
            _example_of(survey, kind)
    for bcv in (_M23_VERSE, _POST_SILLUQ_VERSE):
        assert bcv in survey["currency"]["focus_verses"], (
            f"{bcv} is named in the page's prose but the survey records no chanted word"
            " for it; add it to post_stress_meteg._FOCUS_VERSES"
        )
    _excerpt_accounting()


def _excerpt_accounting() -> tuple[int, int]:
    """The page's quotation accounting: every excerpt's length, and the sum of them.

    The plan's decision 2 caps one excerpt at 150 words and all of them together at 300, and
    requires the generator to enforce both whenever it has excerpts.  This page has none, so
    what is enforced is that the list is empty and the accounting reads zero.
    """
    lengths = [len(text.split()) for _source, text in _EXCERPTS]
    for (source, _text), length in zip(_EXCERPTS, lengths):
        assert length <= _MAX_WORDS_PER_EXCERPT, f"{source}: {length} words"
    assert sum(lengths) <= _MAX_WORDS_IN_ALL_EXCERPTS, sum(lengths)
    assert not _EXCERPTS, "this page quotes neither book; see the module docstring"
    return len(_EXCERPTS), sum(lengths)


# --- rendering helpers ---------------------------------------------------------


def itm() -> object:
    """The abbreviated book name, with Yeivin's title on hover."""
    return mb_html.abbr("ITM", {"title": _ITM_GLOSS})


def cos() -> object:
    """The abbreviated book name, with Breuer's title on hover."""
    return mb_html.abbr("CoS", {"title": _COS_GLOSS})


def _para(text: str) -> object:
    """One paragraph, its pointed Hebrew runs wrapped so they take the Hebrew font."""
    return mb_html.para(wrap_hebrew_runs(text))


def _hebrew_cell(form: str | None) -> tuple:
    """A pointed Hebrew form wrapped as an hbo run for an RTL table cell."""
    return wrap_hebrew_runs(form or "")


def _ref_link(bcv: str) -> object:
    """The reference, linked to the verse in MAM with doc."""
    bb, chnu, vrnu = _split(bcv)
    return mb_html.anchor_h(
        ref_abbrev(bcv), rtms_report.mam_with_doc_url(bb=bb, chnu=chnu, vrnu=vrnu)
    )


def _split(bcv: str) -> tuple[str, int, int]:
    bb = bcv[:2]
    chnu, _colon, vrnu = bcv[2:].partition(":")
    return bb, int(chnu), int(vrnu)


def _book_name(bcv: str) -> str:
    return tbn.ordered_short_dash_full_39(wlc_bb_to_bk39id(bcv[:2]))[3:]


def _table(headers: tuple, rows: list, attr: dict | None = None) -> object:
    return mb_html.table(
        [mb_html.table_row_of_headers(headers), *rows],
        attr or {"class": "limited-width post-stress-meteg-table"},
    )


# --- the sections --------------------------------------------------------------


def _opening(survey: dict) -> list:
    """Section 1: what is counted, and where the silluq boundary falls."""
    total = _both(survey, "meteg after the stressed syllable")
    words = _both(survey, "chanted words checked")
    return [
        mb_html.para(
            (
                "A meteg almost always appears before the stressed syllable of its chanted",
                " word, but it can also come after the stress. Both",
                *[" ", itm(), " and ", cos()],
                " discuss post-stress meteg. Neither book says how often PSM (post-stress",
                " meteg) happens; we find that MAM has ",
                f"{total:,} of them, over {words:,} chanted words.)",
            )
        ),
        _para(
            "First, some definitions:"
            " a chanted word can be either a simple word"
            " (a word of just one atom)"
            " or it can be a compound word"
            " (a word of two or more atoms connected by maqaf marks)."
            " An atom is a sequence of letters uninterrupted by space, maqaf, or any other punctuation."
        ),
        _para(
            "Which syllable a chanted word is stressed on is not always obvious,"
            " so for our survey of PSM,"
            " we use Phonetic MAM, an edition"
            " of MAM that marks the stressed syllable of every chanted word."
        ),
    ]


def _census(survey: dict) -> list:
    """Section 2: the counts, prose verses beside poetic verses."""
    categories = (
        "chanted words checked",
        "meteg before the stressed syllable",
        "meteg after the stressed syllable",
    )
    headers = (
        mb_html.abbr("cant-sys", {"title": "cantillation system"}),
        mb_html.abbr("c-words", {"title": "count of chanted words"}),
        ("Pre-stress", mb_html.line_break(), "meteg"),
        ("Post-stress", mb_html.line_break(), "meteg"),
    )
    numeric = (None, _NUMERIC_CELL, _NUMERIC_CELL, _NUMERIC_CELL)
    labels = {_PROSE: "prose", _POETIC: "poetic"}
    rows = [
        mb_html.table_row_of_data(
            (labels[system], *[f"{_count(survey, system, c):,}" for c in categories]),
            numeric,
        )
        for system in (_PROSE, _POETIC)
    ]
    rows.append(
        mb_html.table_row_of_data(
            ("all", *[f"{_both(survey, c):,}" for c in categories]), numeric
        )
    )
    before = _both(survey, "meteg before the stressed syllable")
    after = _both(survey, "meteg after the stressed syllable")
    return [
        mb_html.heading_level_2("MAM census by verse system"),
        mb_html.para(
            (
                "The “prose verses” row in the table below is for the 21 books plus with"
                " Job's prose frame; the “poetic verses” row is Job's main, poetic section"
                " plus all Psalms and the entire book of Proverbs. See the ",
                mb_html.anchor_h(
                    "appendix on dually-cantillated passages",
                    f"#{_DUAL_CANTILLATION_APPENDIX_ID}",
                ),
                " for how this census handles them.",
            )
        ),
        _table(headers, rows),
        _para(
            f"So a meteg comes before the stress {before:,} times and after it {after:,}"
            " times."
        ),
        _para(
            f"Only about {after / (before + after):.1%} of the {before + after:,} meteg marks"
            " counted here come after the stress."
        ),
    ]


def _by_type(survey: dict) -> list:
    """Section 3: the three types the two books describe, and what is left over."""
    headers = (
        "Type",
        "Prose",
        "Poetic",
        itm(),
        cos(),
        "Example",
        "Following chanted word, if relevant",
    )
    rows = []
    for kind, (yeivin, breuer, _grading) in _TYPE_SOURCES.items():
        example = _example_of(survey, kind)
        rows.append(
            mb_html.table_row_of_data(
                (
                    kind,
                    str(survey["post_stress_by_structural_type"][_PROSE][kind]),
                    str(survey["post_stress_by_structural_type"][_POETIC][kind]),
                    yeivin,
                    breuer,
                    _hebrew_cell(example["mam_form"] or example["chanted_word"]),
                    _following_example(example, kind),
                ),
                (
                    None,
                    _NUMERIC_CELL,
                    _NUMERIC_CELL,
                    None,
                    None,
                    _HEBREW_CELL,
                    _HEBREW_CELL,
                ),
            )
        )
    unclassified = psm.TYPE_UNCLASSIFIED
    rows.append(
        mb_html.table_row_of_data(
            (
                "misc (not one of the three types above)",
                str(survey["post_stress_by_structural_type"][_PROSE][unclassified]),
                str(survey["post_stress_by_structural_type"][_POETIC][unclassified]),
                "",
                "",
                _hebrew_cell(_example_of(survey, unclassified)["mam_form"]),
                _hebrew_cell(None),
            ),
            (
                None,
                _NUMERIC_CELL,
                _NUMERIC_CELL,
                None,
                None,
                _HEBREW_CELL,
                _HEBREW_CELL,
            ),
        )
    )
    return [
        mb_html.heading_level_2("Post-stress meteg marks by structural type"),
        mb_html.para(
            (
                "Three types of PSM are described in both ",
                itm(),
                " and ",
                cos(),
                ". Each of the three types is named for the shape of the"
                " syllable the meteg falls in:",
            )
        ),
        mb_html.ordered_list(
            (
                "an open syllable;",
                "a syllable closed by a guttural at the end of the chanted word; and",
                "a closed syllable whose vowel is tsere.",
            )
        ),
        _para(
            "The counts below are mechanical, and a chanted word that doesn't fit"
            " one of the three types is left in the “misc” row rather than pushed into the nearest type."
        ),
        _table(headers, rows),
        mb_html.para(
            (
                "For the open-syllable type, ",
                itm(),
                " §332 describes a chanted word stressed on its penultimate syllable,"
                " ending in an open syllable, before a chanted word stressed on its first."
                " Yeivin calls it rarely marked, commonest in early manuscripts and absent"
                " from printed texts, and ",
                cos(),
                " Ch. 8 grades it optional — which for Breuer means that no tradition"
                " settles it and each naqdan decided for himself.",
            )
        ),
        mb_html.para(
            (
                "The guttural type is described in ",
                itm(),
                " §354 and ",
                cos(),
                " Ch. 8 type (b), where the last syllable of the chanted word ends in ḥet,"
                " ayin or he. A furtive pataḥ counts as a separate syllable here, as it"
                " is in Phonetic MAM, so a meteg on that guttural comes out after the stress"
                " rather than in it. Breuer calls the type obligatory; Yeivin's statement is"
                " narrower, that the mark is sometimes used when the chanted word after it"
                " begins with lamed or nun.",
            )
        ),
        mb_html.para(
            (
                "The tsere type is described in ",
                itm(),
                " §338, fed by §308's account of retracted stress: where the stress retracts"
                " and a final closed syllable keeps its tsere, that syllable takes the mark,"
                " and Yeivin says it is marked in manuscripts and printed texts alike. ",
                cos(),
                " Ch. 8's matching type (a) is wider than tsere — it is the big vowel"
                " in a closed syllable — so one or two of the records in the last row"
                " belong to Breuer's type without belonging to Yeivin's section.",
            )
        ),
    ]


def _every_case(survey: dict) -> list:
    """Every post-stress meteg, so the counts above can be read rather than believed."""
    headers = ("Verse", "Chanted word", "Type", "Accent on the stressed letter")
    rows = [
        mb_html.table_row_of_data(
            (
                _ref_link(record["bcv"]),
                _hebrew_cell(record["mam_form"] or record["chanted_word"]),
                record["structural_type"],
                rmn(record["accent_on_the_stressed_letter"]),
            ),
            (None, _HEBREW_CELL, None, None),
        )
        for record in survey["post_stress"]
    ]
    return [
        mb_html.heading_level_2("Every PSM in MAM"),
        _para(
            "In the order the corpus has them, prose verses and poetic verses together. Each"
            " reference links to the verse in MAM with doc, and each chanted word is MAM's"
            " text."
        ),
        _table(headers, rows, {"class": "accent-pair-table post-stress-meteg-table"}),
    ]


def _m23(survey: dict) -> list:
    """Section 4: the Isaiah 23:12 suggestion, and what kind of meteg it added."""
    qumi = _focus_word(survey, _M23_VERSE, ("קומי",))
    yanuax = _record_at(survey, _M23_VERSE)
    same_shape = _same_shape_as_qumi(survey)
    open_count = _by_type_count(survey, psm.TYPE_OPEN)
    return [
        mb_html.heading_level_2(
            "The M23 comparison at Isaiah 23:12", {"id": M23_SECTION_ID}
        ),
        _para(
            "Daniel Holman wrote that the Aleppo Codex has a meteg under the mem of the"
            f" chanted word {qumi} at Isaiah 23:12, where MAM had none. The suggestion was"
            " taken, so MAM has the meteg there now, and the comparison forms on his card"
            " are what he was sent, frozen at the date of his message."
        ),
        _para(
            f"The mark is of the open-syllable type: {qumi} is stressed on its first"
            " syllable, ends in an open syllable, and the chanted word after it is stressed"
            " on its first full syllable. That is the type both books call optional, and"
            f" at {open_count} occurrences it is also the commonest of the three in MAM."
        ),
        _para(
            "The same verse already had a PSM of another type:"
            f" {yanuax['mam_form']}, whose last syllable a guttural closes. So Isaiah 23:12"
            " now has two of them, one of each of the two commonest types."
        ),
        _para(
            "MAM has one other chanted word of exactly this shape, and the table above holds"
            f" it: {same_shape['mam_form']} at {ref_abbrev(same_shape['bcv'])}, with the"
            " same accent on the stress, the same open final syllable, and the same kind of"
            " chanted word after it."
        ),
        _para(
            f"The counts above do not include the meteg of {qumi}. They are taken from the"
            " Phonetic MAM edition, which has not been regenerated since MAM gained it, so"
            " Isaiah 23:12 is one of the verses where the two texts have parted."
        ),
    ]


def _record_at(survey: dict, bcv: str) -> dict:
    """The one post-stress record at a verse the page names, or a failure saying so."""
    records = [one for one in survey["post_stress"] if one["bcv"] == bcv]
    assert len(records) == 1, f"{bcv} has {len(records)} post-stress records, not one"
    return records[0]


def _same_shape_as_qumi(survey: dict) -> dict:
    """MAM's other open-syllable post-stress meteg on a chanted word whose letters are קומי.

    Found rather than named, so the sentence that calls it the only other one is checked by
    the search that produces it: two hits, or none, stop the build.
    """
    hits = [
        one
        for one in survey["post_stress"]
        if one["structural_type"] == psm.TYPE_OPEN
        and _letters_of(one["mam_form"] or one["chanted_word"]) == ("קומי",)
    ]
    assert len(hits) == 1, f"{len(hits)} chanted words of the M23 shape, not one"
    return hits[0]


def _letters_of(word: str) -> tuple[str, ...]:
    """The base letters of each atom of a chanted word, as a tuple, one string per atom.

    The house pattern for finding a form without retyping its accents: search by letters,
    render what the corpus has.  ``maqaf_nonfinal_accents_page._find_span`` is the other
    instance.
    """
    atoms = word.replace(psm.MAQAF, " ").split(" ")
    return tuple(
        "".join(char for char in atom if "א" <= char <= "ת") for atom in atoms if atom
    )


def _focus_word(
    survey: dict, bcv: str, letters: tuple[str, ...], *, must_have: str = ""
) -> str:
    """The one chanted word of a focus verse whose atoms have these letters.

    A focus verse is one the page names outside its tables, and the survey records its
    chanted words as MAM has them today.  Searching by letters is what keeps the accents
    lifted from the corpus rather than typed here, and the exactly-one assertion is what
    makes the search a check rather than a guess.

    ``must_have`` narrows a verse that has the same letters twice: 1 Samuel 17:5 has נחשת
    both in the middle and at the end, and it is the verse-final one -- the one with sof
    pasuq -- that the post-silluq section is about.
    """
    words = survey["currency"]["focus_verses"][bcv]["chanted_words"]
    hits = [
        word for word in words if _letters_of(word) == letters and must_have in word
    ]
    assert len(hits) == 1, f"{bcv}: {len(hits)} chanted words with letters {letters}"
    return hits[0]


def _post_silluq(survey: dict) -> list:
    """Section 5: a meteg after the silluq, which MAM does not have."""
    nexoshet = _focus_word(
        survey, _POST_SILLUQ_VERSE, ("נחשת",), must_have=psm.SOF_PASUQ
    )
    return [
        mb_html.heading_level_2("The post-silluq case at 1 Samuel 17:5"),
        _para(
            "A meteg after the silluq would be a harder case than any of the above, since"
            " the two marks are one codepoint and the rule that tells them apart is about"
            " the stressed syllable. MAM has no such meteg: of the PSMs"
            " counted here, none is in a chanted word that has sof pasuq."
        ),
        _para(
            "The place the question comes from is 1 Samuel 17:5, whose verse-final chanted"
            f" word MAM has as {nexoshet} — one U+05BD, the silluq, on the stressed"
            " syllable. UXLC 3.9 and WLC 4.22 each record two U+05BD there, the second on"
            " the final syllable. Those are transcriptions of the Leningrad Codex and are"
            " evidence about themselves; what the manuscript has is a question for the"
            " manuscript, whose folio F159A, column 3, line 8 is where the word stands."
        ),
        _para(
            "Neither book has a rule that would cover such a mark. The open-syllable type"
            " and the guttural type each require a following chanted word, which a"
            " verse-final chanted word does not have, so both are out of reach there by"
            " construction rather than by silence."
        ),
    ]


def _sources_and_limits(survey: dict) -> list:
    """Section 6: what was read, what the corpus is, and what the page does not claim."""
    currency = survey["currency"]
    overlap = _both(survey, "meteg sharing a letter with a non-stress-marking accent")
    excerpts, words = _excerpt_accounting()
    return [
        mb_html.heading_level_2("Sources and limits"),
        mb_html.para(
            (
                "The sections behind the three types are ",
                itm(),
                " §§308, 332, 338 and 354, and ",
                cos(),
                " Ch. 8 §§2–10 and §§46–47, whose §3 is the ten-type taxonomy the"
                " three rows are drawn from and whose §2 says what makes a meteg optional."
                " Yeivin's §325, the meteg before a paseq, is deliberately not among them:"
                " he calls that one marked in early manuscripts and rare even there. Both"
                " books call the mark a ga'ya; this page says meteg throughout.",
            )
        ),
        _para(
            f"This page quotes neither book: {excerpts} excerpts, {words} words of quoted"
            " source text."
        ),
        _para(
            "The corpus is MAM as the Phonetic MAM standard set has it, which is where the"
            " stress marking comes from and is therefore the text the counts describe. That"
            " edition is regenerated when al-hatorah regenerates it, which is not when MAM"
            f" changes: measured against MAM as it stands today, {currency['verses_differing']}"
            f" of its {currency['verses_compared']:,} numbered verses differ in how many"
            f" meteg marks they have — {currency['metegs_in_the_surveyed_snapshot']:,} in the"
            " surveyed"
            f" text against {currency['metegs_in_mam_simple_today']:,} today. Isaiah 23:12 is"
            " one of them, which is why the meteg this page's M23 section is about is not"
            " among the counts above."
        ),
        _para(
            "One diagnostic overlaps the three positions rather than adding a fourth: a meteg"
            " can share a letter with an accent that marks no stress, which the prepositives,"
            " the postpositives, ole and geresh muqdam all do. There are"
            f" {overlap} such meteg marks, and each is counted in the group its syllable puts it"
            " in, before or after the stress, rather than beside them."
        ),
        _para(
            "Nothing here says that MAM follows a rule of Breuer's or of Yeivin's. MAM is a"
            " consensus text; the two books describe the phenomenon, and the counts are"
            " measurements of MAM set beside their descriptions."
        ),
    ]


def _dual_cantillation_appendix(survey: dict) -> list:
    """The method for passages Phonetic MAM records with two cantillations."""
    dual_cantillation = _dual_cantillation(survey)
    comparison = dual_cantillation["comparison_counts"]
    alef = comparison[psm.CANT_ALEF]
    bet = comparison[psm.CANT_BET]
    exodus_forms = _dual_cantillation_facts(survey, "ex20:2")[
        "first_same_chanted_word_group"
    ]
    genesis_pair_count = _dual_cantillation_facts(survey, "gn35:22")[
        "same_chanted_word_group_count"
    ]
    headers = ("Census result", "cant-alef, used", "cant-bet")
    categories = (
        ("Chanted words", "chanted words checked"),
        ("Pre-stress meteg", "meteg before the stressed syllable"),
        ("Post-stress meteg", "meteg after the stressed syllable"),
    )
    rows = [
        mb_html.table_row_of_data(
            (label, f"{alef[category]:,}", f"{bet[category]:,}"),
            (None, _NUMERIC_CELL, _NUMERIC_CELL),
        )
        for label, category in categories
    ]
    return [
        mb_html.heading_level_2(
            "Appendix: dually-cantillated passages",
            {"id": _DUAL_CANTILLATION_APPENDIX_ID},
        ),
        _para(
            "Phonetic MAM records two cantillations for the two Decalogue passages and"
            f" Genesis 35:22, across {len(dual_cantillation['numbered_verses'])} numbered"
            " verses. These census totals use the cant-alef cantillation strand for each"
            " such passage, as though the passage were read once."
        ),
        mb_html.para(
            (
                "For example, Phonetic MAM has ",
                *wrap_hebrew_runs(exodus_forms[0][0]),
                " in cant-alef at Exodus 20:2 and ",
                *wrap_hebrew_runs(exodus_forms[1][0]),
                " in cant-bet. The two forms are the same chanted word with different"
                " accents. Genesis 35:22 has ",
                f"{genesis_pair_count} such pairs.",
            )
        ),
        _table(headers, rows),
        _para(
            "Cant-alef and cant-bet give exactly the same post-stress-meteg count:"
            f" {alef['meteg after the stressed syllable']:,}. Cant-alef has one more chanted"
            " word, while cant-bet has one more pre-stress meteg."
        ),
    ]


def add_args(parser, *, repo_root: Path) -> None:
    del repo_root
    parser.add_argument(
        "--html-out-dir",
        type=Path,
        default=None,
        help="Directory to write the page into (default: this repo's gh-pages).",
    )
    parser.add_argument(
        "--trust-survey",
        action="store_true",
        help=(
            "Read out/accgram/post-stress-meteg.json instead of recomputing the survey."
            " Only for a caller that cannot reach the MAM-private clone."
        ),
    )


def run(args) -> None:
    out_path = gen_html_file(
        getattr(args, "html_out_dir", None),
        trust_survey=bool(getattr(args, "trust_survey", False)),
    )
    print(f"Generated {out_path}")
