"""Shared constants and HTML primitives for the post-stress-meteg pages."""

from __future__ import annotations

import re

from accgram import post_stress_meteg_model as psm
from mb_cmn import hebrew_punctuation as hpu
from accgram import printed_decalogue_strands as pds
from accgram.almost_errors_html_shared import ref_abbrev, wrap_hebrew_runs
from accgram import rtms_report
from author_site import site_data
from mb_author import author
from mb_misc import mb_html
from py_html.my_html_span_romanized import rmn
from wlc_cmn.wlc_book_codes import wlc_bb_codes

_FNAME = site_data.POST_STRESS_METEG_FNAME

_TITLE = site_data.POST_STRESS_METEG_TITLE

_METHODS_FNAME = site_data.POST_STRESS_METEG_METHODS_FNAME

_METHODS_TITLE = site_data.POST_STRESS_METEG_METHODS_TITLE

_CASES_FNAME = site_data.POST_STRESS_METEG_CASES_FNAME

_CASES_TITLE = site_data.POST_STRESS_METEG_CASES_TITLE

_MISC_FNAME = site_data.POST_STRESS_METEG_MISC_FNAME

_MISC_TITLE = site_data.POST_STRESS_METEG_MISC_TITLE

_LACKS_MAS_FNAME = site_data.POST_STRESS_METEG_LACKS_MAS_FNAME

_LACKS_MAS_TITLE = site_data.POST_STRESS_METEG_LACKS_MAS_TITLE

_NOT_FIT_FNAME = site_data.POST_STRESS_METEG_NOT_FIT_FNAME

_NOT_FIT_TITLE = site_data.POST_STRESS_METEG_NOT_FIT_TITLE

_POST_SILLUQ_FNAME = site_data.POST_STRESS_METEG_POST_SILLUQ_FNAME

_POST_SILLUQ_TITLE = site_data.POST_STRESS_METEG_POST_SILLUQ_TITLE

_CHRONICLES_8_11_FNAME = site_data.POST_STRESS_METEG_2CHRONICLES_8_11_FNAME

_CHRONICLES_8_11_TITLE = site_data.POST_STRESS_METEG_2CHRONICLES_8_11_TITLE

_NEXT_CONJUNCTIVE_FNAME = site_data.POST_STRESS_METEG_NEXT_CONJUNCTIVE_FNAME

_NEXT_CONJUNCTIVE_TITLE = site_data.POST_STRESS_METEG_NEXT_CONJUNCTIVE_TITLE

_PHONETIC_MAM_URL = "https://bdenckla.github.io/phonetic-hbo/"

_POST_SILLUQ_FOOTNOTE_ID = "footnote-1"

_POST_SILLUQ_DISTINCT_STROKE_FOOTNOTE_ID = "distinct-stroke-footnote"

_POST_SILLUQ_MAM_POLICY_FOOTNOTE_ID = "mam-policy-footnote"

_NONFINAL_MAS_FOOTNOTE_ID = "footnote-2"

_JEREMIAH_FOOTNOTE_ID = "footnote-3"

_NEXT_CONJUNCTIVE_FOOTNOTE_ID = "footnote-4"

_SOURCES_FOR_TYPES_FOOTNOTE_ID = "footnote-5"

_TYPE_2_TYPE_3_FOOTNOTE_ID = "footnote-6"

_VOCAL_SHEWA_FOOTNOTE_ID = "footnote-7"

_PASHTA_STRESS_HELPER_FOOTNOTE_ID = "footnote-8"

_FIT_TYPE_2_NO_IVS_FOOTNOTE_ID = "footnote-9"

_FIT_FOR_MAS_SECTION_ID = "fit-for-mas"


def _author_romanization(key: str) -> object:
    """One standard author-wide dollar substitution, already wrapped as romanized text."""
    (rendered,) = author.dollar_sub(f"${key}")
    return rendered


_METSIL = "metsil"  # Portmanteau, not a romanized Hebrew mark name.


# Each visible romanization is a module-level HTML node, so the shared ``romanized`` class
# italicizes it.  Existing ``ROM_*`` spellings stay single-sourced; the author-wide dollar
# substitutions supply the additional standard spellings this page needs.
_ROM_METEG = rmn(pds.ROM_METEG)

_ROM_METEG_MERKHA = rmn(f"{pds.ROM_METEG}/{pds.ROM_MERKHA}")

_ROM_METEG_CAP = rmn(pds.ROM_METEG.capitalize())

_ROM_SILLUQ = rmn(pds.ROM_SILLUQ)

_ROM_PASEQ = rmn(pds.ROM_PASEQ)

_ROM_PATAH = rmn(pds.ROM_PATAX)

_ROM_MAQAF = rmn(pds.ROM_MAQAF)

_ROM_TSERE = _author_romanization("tsere")

_ROM_HOLAM = _author_romanization("xolam")

_ROM_GAYA = _author_romanization("gaya_with_half_ring_for_ayin")

_ROM_OLEH = _author_romanization("oleh")

_ROM_ALEF = _author_romanization("alef")

_ROM_BET = _author_romanization("bet")

_ROM_HE = _author_romanization("hehe")

_ROM_MAPPIQ = rmn("mappiq")

_ROM_VAYOMER = rmn("vayomer")

_ROM_SHEWA = rmn("shewa")

_ROM_PASHTA = rmn(pds.ROM_PASHTA)


def _visible_title(title: str, *, lowercase: bool = False) -> tuple:
    """A page title whose visible meteg and silluq take the standard italics."""
    assert title.startswith("Meteg "), title
    rest = title.removeprefix("Meteg")
    head = _ROM_METEG if lowercase else _ROM_METEG_CAP
    before, silluq, after = rest.partition(pds.ROM_SILLUQ)
    if silluq:
        return (head, before, _ROM_SILLUQ, after)
    return (head, rest)


# Every Hebrew cell says so, whatever else it says.  The whole-column rule: blank cells
# included, the English heading left alone, no class and no stylesheet rule.
_HEBREW_CELL = {"dir": "rtl"}

_NUMERIC_CELL = {"class": "numeric"}

_POST_SILLUQ_BCV_CELL = {"class": "post-silluq-bcv"}

# No excerpt from either book appears on this page.  Kept as a structure rather than as a bare
# absence so the accounting below has something to count, and so an excerpt added later is
# added in one place with its source beside it.
_EXCERPTS: tuple[tuple[str, str], ...] = ()

_MAX_WORDS_PER_EXCERPT = 150

_MAX_WORDS_IN_ALL_EXCERPTS = 300

_PROSE = psm.SYSTEM_PROSE

_POETIC = psm.SYSTEM_POETIC

_MBS_O_CENSUS_GLOSS = (
    "count of words with one or more meteg marks before the stress and none after it"
)

_MAS_CENSUS_GLOSS = (
    "count of words with one or more meteg marks after the stress and any number"
    " (including zero) before it"
)

# This page names each book's author in the hover title, where the accgram pages that share
# ``almost_errors_html_shared``'s ITM_TITLE and COS_TITLE do not.  Ben's decision, 2026-09-08,
# after the divergence was put to him with the option of ending it either way: "that slight
# divergence (author's names shown in some cases, not shown in other cases) is acceptable to me."
# So do not unify the four pages on either spelling; the difference is chosen, not overlooked.
_ITM_GLOSS = "Yeivin's Introduction to the Tiberian Masorah"

_COS_GLOSS = "Breuer's The Cantillation of Scripture"

_CHB_GLOSS = "Jacobson's Chanting the Hebrew Bible"

# The one verse the page names outside its tables.  The survey records its chanted words as MAM
# has them today, under ``currency.focus_verses``, so the form shown here is lifted like every
# other form on the page.
_POST_SILLUQ_VERSE = "1s17:5"

_MAM_POST_SILLUQ_VERSE = "1k7:37"

_UXLC_CHANGE_VERSE = "1k14:14"

_URJ_DISTINCT_STROKE_VERSE = "nu23:26"

_UXLC_CHANGE_URL = (
    "https://tanach.us/Changes/2022.12.07%20-%20Changes/"
    "2022.12.07%20-%20Changes.html?2022.08.31-17"
)

_PLAUT_STEIN_TORAH_URL = (
    "https://www.ccarpress.org/"
    "documentation-for-the-revised-edition-of-the-torah-a-modern-commentary/"
)

# Every visible spelling of these references comes from ``ref_abbrev``, the
# short-but-not-super-short prose form built on ``mb_misc/osis_book_abbrevs.py``'s
# OSIS list -- "Gen. 2:7", "1 Sam. 17:5", "1 Kgs. 7:37".  Ben's rule of 2026-09-08:
# no reference is typed out, here or in a figure caption or an alt text.
_POST_SILLUQ_REF = ref_abbrev(_POST_SILLUQ_VERSE)

_MAM_POST_SILLUQ_REF = ref_abbrev(_MAM_POST_SILLUQ_VERSE)

_UXLC_CHANGE_REF = ref_abbrev(_UXLC_CHANGE_VERSE)

_URJ_DISTINCT_STROKE_REF = ref_abbrev(_URJ_DISTINCT_STROKE_VERSE)

_PSALMS_60_REF = ref_abbrev("ps60:10")

_PSALMS_70_REF = ref_abbrev("ps70:2")

_PSALMS_72_REF = ref_abbrev("ps72:15")

_JOB_4_REF = ref_abbrev("jb4:12")

_POST_SILLUQ_LC_CROP_URL = "img/LC-159A-col-3-line-8-1S-17v5.png"

_POST_SILLUQ_LC_CROP_SOURCE_URL = "https://github.com/bdenckla/phonetic-hbo/issues/78"

_POST_SILLUQ_ALEPPO_CROP_URL = "img/Aleppo-Codex-1S-17v5-no-post-silluq-meteg.png"

_POST_SILLUQ_CAIRO_COTP_CROP_URL = "img/cairo-cotp-p110-image103-1S17v5-nexoshet.png"

_POST_SILLUQ_CAIRO_COTP_SOURCE_URL = "https://simurg.csic.es/view/9918494052404201"

_POST_SILLUQ_SASSOON_CROP_URL = "img/sassoon-1053-1S17v5-nexoshet.png"

_POST_SILLUQ_SASSOON_SOURCE_URL = (
    "https://www.masoretica.org/?book=1+Samuel&chapter=17&verse=5&manuscript=sassoon"
)

_MAM_POST_SILLUQ_ALEPPO_CROP_URL = "img/Aleppo-Codex-1K-7v37.png"

_MAM_POST_SILLUQ_LENINGRAD_CROP_URL = "img/Leningrad-Codex-1K-7v37.png"

_MAM_POST_SILLUQ_SASSOON_CROP_URL = "img/sassoon-1053-1K7v37-final-word.png"

_MAM_POST_SILLUQ_SASSOON_SOURCE_URL = (
    "https://www.masoretica.org/?book=1+Kings&chapter=7&verse=37&manuscript=sassoon"
)

_FIRST_KINGS_14_ALEPPO_CROP_URL = "img/aleppo-083r-1K14v14-atta.png"

_FIRST_KINGS_14_LENINGRAD_CROP_URL = "img/leningrad-195B-col2-line27-1K14v14-atta.jpg"

_FIRST_KINGS_14_CAIRO_COTP_CROP_URL = "img/cairo-cotp-image204-1K14v14-atta.png"

_FIRST_KINGS_14_SASSOON_CROP_URL = "img/sassoon-1053-1K14v14-atta.png"

_FIRST_KINGS_14_SASSOON_SOURCE_URL = (
    "https://www.masoretica.org/?book=1+Kings&chapter=14&verse=14&manuscript=sassoon"
)

_PSALMS_60_ALEPPO_CROP_URL = "img/aleppo-251r-Ps60v10-HFRV33Y.png"

_PSALMS_60_LENINGRAD_CROP_URL = "img/leningrad-377B-Ps60v10-HFRV33Y.png"

_PSALMS_60_CAM1753_CROP_URL = "img/cam1753-unlocated-Ps60v10-HFRV33Y.png"

_PSALMS_60_SASSOON_CROP_URL = "img/sassoon-1053-Ps60v10-HFRV33Y.png"

_PSALMS_60_SASSOON_SOURCE_URL = (
    "https://www.masoretica.org/?book=Psalms&chapter=60&verse=10&manuscript=sassoon"
)

_PSALMS_70_ALEPPO_CROP_URL = "img/aleppo-253r-Ps70v2-xushah.png"

_PSALMS_70_LENINGRAD_CROP_URL = "img/leningrad-379B-Ps70v2-xushah.png"

_PSALMS_70_CAM1753_CROP_URL = "img/cam1753-unlocated-Ps70v2-xushah.png"

_PSALMS_70_SASSOON_CROP_URL = "img/sassoon-1053-Ps70v2-xushah.png"

_PSALMS_70_SASSOON_SOURCE_URL = (
    "https://www.masoretica.org/?book=Psalms&chapter=70&verse=2&manuscript=sassoon"
)

_PSALMS_72_ALEPPO_CROP_URL = "img/aleppo-253v-Ps72v15-yevarkhenhu.png"

_PSALMS_72_LENINGRAD_CROP_URL = "img/leningrad-380A-col2-line3-Ps72v15-yevarkhenhu.png"

_PSALMS_72_CAM1753_CROP_URL = "img/cam1753-unlocated-Ps72v15-yevarkhenhu.png"

_PSALMS_72_SASSOON_CROP_URL = "img/sassoon-1053-Ps72v15-yevarkhenhu.png"

_PSALMS_72_SASSOON_SOURCE_URL = (
    "https://www.masoretica.org/?book=Psalms&chapter=72&verse=15&manuscript=sassoon"
)

_JOB_4_ALEPPO_CROP_URL = "img/aleppo-271r-col2-line5-Job4v12-menhu.png"

_JOB_4_LENINGRAD_CROP_URL = "img/leningrad-398A-Job4v12-menhu.png"

_JOB_4_CAM1753_CROP_URL = "img/cam1753-0073B-col2-line13-Job4v12-menhu.png"

_JOB_4_SASSOON_CROP_URL = "img/sassoon-1053-Job4v12-menhu.png"

_JOB_4_SASSOON_SOURCE_URL = (
    "https://www.masoretica.org/?book=Job&chapter=4&verse=12&manuscript=sassoon"
)

_URJ_DISTINCT_STROKE_CROP_URL = "img/urj-2005-Num23v26-eeseh.png"

_POST_SILLUQ_CASES_JSON = "meteg_after_silluq_cases.json"

_POST_SILLUQ_KOREN_JSON = "meteg_after_silluq_koren_readings.json"

_POST_SILLUQ_CASE_STATUSES = frozenset({"last-metsil-contrast", "open-candidate"})

_POST_SILLUQ_BOOK_ORDER = {bb: index for index, bb in enumerate(wlc_bb_codes())}

_POST_SILLUQ_FORM_SOURCES = frozenset({"mam", "uxlc"})

_POST_SILLUQ_SOURCE_STATES = frozenset(
    {
        "later-meteg",
        "no-later-mark",
        "both-strokes",
        "first-position-only",
        "tracked-observation",
        "not-recorded",
    }
)

_POST_SILLUQ_CAIRO_COTP_BCVS = frozenset({"1s17:5", "1k7:37", "1k14:14"})
_POST_SILLUQ_CAIRO_COTP_SOURCES = (
    "aleppo",
    "leningrad",
    "cairo_cotp",
    "sassoon_1053",
    "koren",
    "simanim",
)
_POST_SILLUQ_CAM1753_BCVS = frozenset({"ps60:10", "ps70:2", "ps72:15", "jb4:12"})
_POST_SILLUQ_CAM1753_SOURCES = (
    "aleppo",
    "leningrad",
    "cam1753",
    "sassoon_1053",
    "koren",
    "simanim",
)


def _post_silluq_sources_for_bcv(bcv: str) -> tuple[str, ...]:
    """Use ALC5KS for the Prophets cases and AL75KS for the other four."""
    if bcv in _POST_SILLUQ_CAIRO_COTP_BCVS:
        return _POST_SILLUQ_CAIRO_COTP_SOURCES
    if bcv in _POST_SILLUQ_CAM1753_BCVS:
        return _POST_SILLUQ_CAM1753_SOURCES
    raise ValueError(f"Unknown post-silluq source set for {bcv!r}")


_POST_SILLUQ_SOURCE_CODES = {
    "aleppo": "A",
    "leningrad": "L",
    "cairo_cotp": "C",
    "cam1753": "7",
    "sassoon_1053": "5",
    "koren": "K",
    "simanim": "S",
}

_POST_SILLUQ_IMAGE_REFS = {
    "aleppo-1s17-5": "1 Samuel 17:5",
    "lc-1s17-5": "1 Samuel 17:5",
    "cairo-cotp-1s17-5": "1 Samuel 17:5",
    "sassoon-1053-1s17-5": "1 Samuel 17:5",
    "aleppo-ps72-15": "Psalms 72:15",
    "leningrad-ps72-15": "Psalms 72:15",
    "cam1753-ps72-15": "Psalms 72:15",
    "sassoon-1053-ps72-15": "Psalms 72:15",
    "aleppo-1k7-37": "1 Kings 7:37",
    "leningrad-1k7-37": "1 Kings 7:37",
    "sassoon-1053-1k7-37": "1 Kings 7:37",
    "aleppo-1k14-14": "1 Kings 14:14",
    "leningrad-1k14-14": "1 Kings 14:14",
    "cairo-cotp-1k14-14": "1 Kings 14:14",
    "sassoon-1053-1k14-14": "1 Kings 14:14",
    "aleppo-ps60-10": "Psalms 60:10",
    "leningrad-ps60-10": "Psalms 60:10",
    "cam1753-ps60-10": "Psalms 60:10",
    "sassoon-1053-ps60-10": "Psalms 60:10",
    "aleppo-ps70-2": "Psalms 70:2",
    "leningrad-ps70-2": "Psalms 70:2",
    "cam1753-ps70-2": "Psalms 70:2",
    "sassoon-1053-ps70-2": "Psalms 70:2",
    "aleppo-jb4-12": "Job 4:12",
    "leningrad-jb4-12": "Job 4:12",
    "cam1753-jb4-12": "Job 4:12",
    "sassoon-1053-jb4-12": "Job 4:12",
}

_POST_SILLUQ_IMAGE_IDS = frozenset(_POST_SILLUQ_IMAGE_REFS)

_POST_SILLUQ_IMAGE_SEQUENCES = {
    "1 Samuel 17:5": (
        "aleppo-1s17-5",
        "lc-1s17-5",
        "cairo-cotp-1s17-5",
        "sassoon-1053-1s17-5",
    ),
    "Psalms 72:15": (
        "aleppo-ps72-15",
        "leningrad-ps72-15",
        "cam1753-ps72-15",
        "sassoon-1053-ps72-15",
    ),
    "1 Kings 7:37": (
        "aleppo-1k7-37",
        "leningrad-1k7-37",
        "sassoon-1053-1k7-37",
    ),
    "1 Kings 14:14": (
        "aleppo-1k14-14",
        "leningrad-1k14-14",
        "cairo-cotp-1k14-14",
        "sassoon-1053-1k14-14",
    ),
    "Psalms 60:10": (
        "aleppo-ps60-10",
        "leningrad-ps60-10",
        "cam1753-ps60-10",
        "sassoon-1053-ps60-10",
    ),
    "Psalms 70:2": (
        "aleppo-ps70-2",
        "leningrad-ps70-2",
        "cam1753-ps70-2",
        "sassoon-1053-ps70-2",
    ),
    "Job 4:12": (
        "aleppo-jb4-12",
        "leningrad-jb4-12",
        "cam1753-jb4-12",
        "sassoon-1053-jb4-12",
    ),
}

_KOREN_STATUSES = frozenset({"complete", "incomplete", "deferred", "skipped-family"})

_KOREN_POSITIONS = frozenset({"first", "last", "both"})

_KOREN_SHEVA_STATES = frozenset({"vocal", "silent"})

_FULL_REF = re.compile(r"(?P<book>.+) (?P<chapter>[0-9]+):(?P<verse>[0-9]+)")

_CHRONICLES_8_11_VERSE = "2c8:11"

_CHRONICLES_8_11_REF = ref_abbrev(_CHRONICLES_8_11_VERSE)

# site_data spells this page title by hand, being a plain data module with no accgram import.
# This assertion keeps its reference at ref_abbrev's form.
assert _CHRONICLES_8_11_REF in _CHRONICLES_8_11_TITLE, (
    _CHRONICLES_8_11_TITLE,
    _CHRONICLES_8_11_REF,
)

_CHRONICLES_8_11_ALEPPO_CROP_URL = "img/Aleppo-Codex-2Chr-8v11.png"

_CHRONICLES_8_11_LENINGRAD_CROP_URL = "img/Leningrad-Codex-2Chr-8v11.png"

_CHRONICLES_8_11_L1 = "אֲשֶׁר־בָּ֥אָֽה"

_CHRONICLES_8_11_L2 = "אֲשֶׁר־בָּֽאָ֥ה"

_CHRONICLES_8_11_LENINGRAD_NEXT_WORD = "אֲלֵיהֶ֖ם"

_CHRONICLES_8_11_LENINGRAD_GLOSSES = {
    "L-1": "merkha-meteg interpretation of Leningrad",
    "L-2": "meteg-merkha interpretation of Leningrad",
}

_ITM_ADAPTATION_URL_BY_SECTION = {
    325: "https://bdenckla.github.io/phonetic-hbo/yeivin_itm-318_344.html#ns325",
    332: "https://bdenckla.github.io/phonetic-hbo/yeivin_itm-318_344.html#ns332",
    338: "https://bdenckla.github.io/phonetic-hbo/yeivin_itm-318_344.html#ns338",
    354: "https://bdenckla.github.io/phonetic-hbo/yeivin_itm-345_357.html#ns354",
}

_ITM_SECTION_REFERENCE = re.compile(r"§(?P<section>[0-9]+)")

# A section range takes an en dash, matching the ranges already rendered on these
# pages.  Spelled by name so it stays legible in source.
_EN_DASH = "\N{EN DASH}"

# Yeivin and Breuer on each of the three types, and how each book grades it.  The pairing is
# the M23 evidence note's, doc/holman-meteg-m23-isaiah-23-12.md; both books are cited for
# every type, so no row rests on one source.  The Ch. 14 pairing below was added 2026-09-07
# and is CoS's alone: ITM states nothing poetic-specific about a gaʿya after the stress, so
# the ITM column stays as it was and the page claims nothing about ITM in either direction.
_TYPE_SOURCES = {
    psm.TYPE_OPEN: ("§332", f"§3(j), §§46{_EN_DASH}47"),
    psm.TYPE_GUTTURAL: ("§354", f"§3(b), §§9{_EN_DASH}10"),
    psm.TYPE_CLOSED_TSERE: ("§338", f"§3(a), §§5{_EN_DASH}8"),
}

# Each number is the printed page on which the cited Ch. 8 section begins.  How to read one
# off the scans, recorded 2026-09-07 because nothing recorded it when 14023ae4 added these
# numbers on 2026-09-05: the 719 images at ~/OneDrive/Documents/ScansOfBooks/The Cantillation
# of Scripture - English/ carry the printed page number in the filename, so
# C354-P1-C8-Ga-aya.jpg is p. 354, which is where §46's heading stands.  A roman-numbered
# page is a B name, B16.jpg being p. xvi; py/cos/fix_diacritics.py's SCAN_REPAIRS in
# masorah-books already relies on the same convention.
_COS_PAGE_STARTS_BY_TYPE = {
    psm.TYPE_OPEN: "300; 354; 355",
    psm.TYPE_GUTTURAL: "299; 308; 309",
    psm.TYPE_CLOSED_TSERE: "299; 301; 302; 306; 307",
}

_COS_CH_8_PAGE_GLOSS = (
    "printed page in Wengrov's English translation of CoS on which the cited Ch. 8 section"
    " begins"
)

# Ch. 14 §8's item (b) concerns type 2.  The source table reports that item and leaves the
# other Ch. 14 cells blank.  Read off C14-S001.md's <!-- §8 --> anchor and off the scans,
# 2026-09-07.
_COS_CH_14_BY_TYPE = {
    psm.TYPE_OPEN: "",
    psm.TYPE_GUTTURAL: "(b)",
    psm.TYPE_CLOSED_TSERE: "",
}

# §8 runs from the Ga'aya heading on p. 547 to the closing "On rare occasions" sentence on
# p. 549; p. 550 is blank, C551 and C552 are the Part III title leaves, and Ch. 15 opens on
# p. 553.  Item (b) is on p. 547.
_COS_CH_14_PAGES_BY_TYPE = {
    psm.TYPE_OPEN: "",
    psm.TYPE_GUTTURAL: "547",
    psm.TYPE_CLOSED_TSERE: "",
}

_TYPE_CODES = {
    psm.TYPE_OPEN: ("1", "the MAS syllable is open and final"),
    psm.TYPE_GUTTURAL: ("2", "the MAS word is closed by a guttural"),
    psm.TYPE_CLOSED_TSERE: (
        "3",
        "the MAS syllable is closed, final, and tsere-voweled",
    ),
}

_TYPE_1_SUBTYPE_CODES = {
    psm.TYPE_1_SUBTYPE_A: "1A",
    psm.TYPE_1_SUBTYPE_B: "1B",
    psm.TYPE_1_SUBTYPE_C: "1C",
    None: "1D",
}

_TYPE_2_SUBTYPE_SPECS = (
    ("lamed", "2A", "2A: The next word begins with ל (lamed)."),
    ("guttural", "2B", "2B: The next word begins with a guttural."),
    (
        "not-lamed-or-guttural",
        "2C",
        "2C: The next word begins with neither ל nor a guttural.",
    ),
)

_TYPE_2_SUBTYPE_CODE_BY_FILTER_GROUP = {
    group: code for group, code, _description in _TYPE_2_SUBTYPE_SPECS
}

# Each subtype tooltip restates its visible bullet, as the type tooltips do.  The type-2
# descriptions are taken from the spec tuple the subtype table itself renders, so those two
# cannot drift apart; the type-1 bullets carry a romanized span, which a title attribute
# cannot hold, so their plain-text spellings are written out here.
_TYPE_1_SUBTYPE_DESCRIPTIONS = {
    "1A": "1A: The next word has initial stress and an initial vocal shewa.",
    "1B": "1B: The next word has a pashta stress helper on its first letter.",
    "1C": "1C: Like 1B, but with some accent other than pashta.",
    "1D": "1D: The next word does not have initial stress.",
}

_SUBTYPE_DESCRIPTIONS = {
    **_TYPE_1_SUBTYPE_DESCRIPTIONS,
    **{code: description for _group, code, description in _TYPE_2_SUBTYPE_SPECS},
}

_CASE_FILTER_OPTIONS = (
    ("all", "All types"),
    ("1", "Type 1 (all subtypes)"),
    ("1A", "Subtype 1A"),
    ("1B", "Subtype 1B"),
    ("1C", "Subtype 1C"),
    ("1D", "Subtype 1D"),
    ("2", "Type 2 (all subtypes)"),
    ("2A", "Subtype 2A"),
    ("2B", "Subtype 2B"),
    ("2C", "Subtype 2C"),
    ("3", "Type 3"),
    ("other", "misc"),
)

_LACKS_MAS_FILTER_OPTIONS = tuple(
    (fit_type, f"Subtype {fit_type}")
    for fit_type in (
        psm.FIT_TYPE_1_A,
        psm.FIT_TYPE_1_B,
        psm.FIT_TYPE_2_AF,
        psm.FIT_TYPE_2_BF,
    )
)

_NOT_FIT_FILTER_OPTIONS = (
    ("all", "All (sub)types"),
    *_CASE_FILTER_OPTIONS[1:],
)

_CASE_TABLE_ID = "post-stress-meteg-cases"

_CASE_TYPE_FILTER_ID = "post-stress-meteg-type-filter"

_CASE_SELECTED_COUNT_ID = "post-stress-meteg-selected-count"

_CASE_TABLE_CLASS = "post-stress-meteg-cases-table"

_CASE_STRIPED_ROW_CLASS = "post-stress-meteg-cases-striped-row"

_NEXT_WORD_CLASS = "post-stress-meteg-next-word"

_LACKS_MAS_TABLE_ID = "post-stress-meteg-lacks-mas-cases"

_LACKS_MAS_SUBTYPE_FILTER_ID = "post-stress-meteg-lacks-mas-subtype-filter"

_LACKS_MAS_SELECTED_COUNT_ID = "post-stress-meteg-lacks-mas-selected-count"

_NOT_FIT_FAILURE_CLASS = "post-stress-meteg-not-fit-failure"

_NOT_FIT_TABLE_ID = "post-stress-meteg-not-fit-cases"

_NOT_FIT_TYPE_FILTER_ID = "post-stress-meteg-not-fit-type-filter"

_NOT_FIT_SELECTED_COUNT_ID = "post-stress-meteg-not-fit-selected-count"

_HEBREW_SPACING_CHECKBOX_ID = "post-stress-meteg-expanded-hebrew"

_HEBREW_SPACING_BODY_CLASS = "post-stress-meteg-expanded-hebrew"

_HEBREW_SPACING_STORAGE_KEY = "post-stress-meteg-expanded-hebrew"

_HEBREW_SPACING_INDIVIDUAL_EXPANDED_CLASS = (
    "post-stress-meteg-individually-expanded-hebrew"
)

_HEBREW_SPACING_INDIVIDUAL_NORMAL_CLASS = "post-stress-meteg-individually-normal-hebrew"

_MISC_TABLE_ID = "post-stress-meteg-misc-cases"

_FIT_FOR_MAS_TYPE_CRITERION = (
    "The next word conforms to (sub)type 1A, 1B, 2Af, 2Bf, or 3"
)

_FIT_FOR_MAS_CRITERIA = (
    "Its word has penultimate stress from a conjunctive accent.",
    "The next word has initial stress from a disjunctive accent.",
    f"{_FIT_FOR_MAS_TYPE_CRITERION}.",
)

_RED_X = "\N{CROSS MARK}"

_HEBREW_SPACING_OPTION = f"""<p class="post-stress-meteg-spacing-control"><label><input type="checkbox" id="{_HEBREW_SPACING_CHECKBOX_ID}" checked>
__SPACING_TEXT__</label> __TOGGLE_TEXT__</p>
<script>
(() => {{
  const checkbox = document.getElementById("{_HEBREW_SPACING_CHECKBOX_ID}");
  const bodyClass = "{_HEBREW_SPACING_BODY_CLASS}";
  const storageKey = "{_HEBREW_SPACING_STORAGE_KEY}";
  const individualExpandedClass = "{_HEBREW_SPACING_INDIVIDUAL_EXPANDED_CLASS}";
  const individualNormalClass = "{_HEBREW_SPACING_INDIVIDUAL_NORMAL_CLASS}";
  const hebrewSelector = '[lang="hbo"]';
  let saved = null;
  try {{
    saved = localStorage.getItem(storageKey);
  }} catch (_error) {{
    // The checkbox still works for the open page if its browser has no page storage.
  }}
  if (saved !== null) {{
    checkbox.checked = saved === "true";
    document.body.classList.toggle(bodyClass, checkbox.checked);
  }}
  checkbox.addEventListener("change", () => {{
    for (const hebrew of document.querySelectorAll(hebrewSelector)) {{
      hebrew.classList.remove(individualExpandedClass, individualNormalClass);
    }}
    document.body.classList.toggle(bodyClass, checkbox.checked);
    try {{
      localStorage.setItem(storageKey, String(checkbox.checked));
    }} catch (_error) {{
      // The page's in-memory preference remains usable without page storage.
    }}
  }});
  document.addEventListener("click", (event) => {{
    if (!(event.target instanceof Element)) {{
      return;
    }}
    const hebrew = event.target.closest(hebrewSelector);
    if (hebrew === null) {{
      return;
    }}
    event.preventDefault();
    const isExpanded = hebrew.classList.contains(individualExpandedClass) ||
      (!hebrew.classList.contains(individualNormalClass) &&
       document.body.classList.contains(bodyClass));
    hebrew.classList.toggle(individualExpandedClass, !isExpanded);
    hebrew.classList.toggle(individualNormalClass, isExpanded);
  }});
}})();
</script>
"""

_CASE_FILTER_SCRIPT = f"""<script>
const typeFilter = document.getElementById("{_CASE_TYPE_FILTER_ID}");
const caseRows = document.querySelectorAll("#{_CASE_TABLE_ID} tr[data-type]");
const selectedCount = document.getElementById("{_CASE_SELECTED_COUNT_ID}");

function updateCaseRows() {{
  let visibleCount = 0;
  for (const row of caseRows) {{
    const isSelected = typeFilter.value === "all" ||
      row.dataset.type === typeFilter.value ||
      row.dataset.subtype === typeFilter.value;
    row.hidden = !isSelected;
    row.classList.toggle(
      "{_CASE_STRIPED_ROW_CLASS}",
      isSelected && visibleCount % 2 === 1,
    );
    if (isSelected) {{
      visibleCount += 1;
    }}
  }}
  selectedCount.textContent = "Showing " + visibleCount + " row" +
    (visibleCount === 1 ? "" : "s") + ".";
}}

typeFilter.addEventListener("change", () => {{
  updateCaseRows();
}});
updateCaseRows();
</script>
"""

_LACKS_MAS_FILTER_SCRIPT = f"""<script>
const lacksMasSubtypeFilter = document.getElementById("{_LACKS_MAS_SUBTYPE_FILTER_ID}");
const lacksMasRows = document.querySelectorAll("#{_LACKS_MAS_TABLE_ID} tr[data-subtype]");
const lacksMasSelectedCount = document.getElementById("{_LACKS_MAS_SELECTED_COUNT_ID}");

function updateLacksMasRows() {{
  let visibleCount = 0;
  for (const row of lacksMasRows) {{
    const isSelected = lacksMasSubtypeFilter.value === "all" ||
      row.dataset.subtype === lacksMasSubtypeFilter.value;
    row.hidden = !isSelected;
    row.classList.toggle(
      "{_CASE_STRIPED_ROW_CLASS}",
      isSelected && visibleCount % 2 === 1,
    );
    if (isSelected) {{
      visibleCount += 1;
    }}
  }}
  lacksMasSelectedCount.textContent = "Showing " + visibleCount + " row" +
    (visibleCount === 1 ? "" : "s") + ".";
}}

lacksMasSubtypeFilter.addEventListener("change", () => {{
  updateLacksMasRows();
}});
updateLacksMasRows();
</script>
"""

_NOT_FIT_FILTER_SCRIPT = f"""<script>
const notFitTypeFilter = document.getElementById("{_NOT_FIT_TYPE_FILTER_ID}");
const notFitRows = document.querySelectorAll("#{_NOT_FIT_TABLE_ID} tr[data-type-codes]");
const notFitSelectedCount = document.getElementById("{_NOT_FIT_SELECTED_COUNT_ID}");

function updateNotFitRows() {{
  let visibleCount = 0;
  for (const row of notFitRows) {{
    const isSelected = notFitTypeFilter.value === "all" ||
      row.dataset.typeCodes.split(" ").includes(notFitTypeFilter.value);
    row.hidden = !isSelected;
    row.classList.toggle(
      "{_CASE_STRIPED_ROW_CLASS}",
      isSelected && visibleCount % 2 === 1,
    );
    if (isSelected) {{
      visibleCount += 1;
    }}
  }}
  notFitSelectedCount.textContent = "Showing " + visibleCount + " row" +
    (visibleCount === 1 ? "" : "s") + ".";
}}

notFitTypeFilter.addEventListener("change", () => {{
  updateNotFitRows();
}});
updateNotFitRows();
</script>
"""

# --- rendering helpers ---------------------------------------------------------


def itm_sections(reference: str) -> tuple:
    """An ITM reference whose adapted section numbers open the corresponding section."""
    out = []
    end = 0
    for match in _ITM_SECTION_REFERENCE.finditer(reference):
        out.append(reference[end : match.start()])
        section = int(match["section"])
        url = _ITM_ADAPTATION_URL_BY_SECTION[section]
        out.extend(
            (
                "§",
                mb_html.anchor(
                    str(section),
                    {"href": url, "target": "_blank", "rel": "noopener"},
                ),
            )
        )
        end = match.end()
    out.append(reference[end:])
    return tuple(out)


def itm() -> object:
    """The abbreviated book name, with Yeivin's title on hover."""
    return mb_html.abbr("ITM", {"title": _ITM_GLOSS})


def cos() -> object:
    """The abbreviated book name, with Breuer's title on hover."""
    return mb_html.abbr("CoS", {"title": _COS_GLOSS})


def chb() -> object:
    """The abbreviated book name, with Jacobson's title on hover."""
    return mb_html.abbr("CHB", {"title": _CHB_GLOSS})


def _para(text: str) -> object:
    """One paragraph, its pointed Hebrew runs wrapped so they take the Hebrew font."""
    return mb_html.para(wrap_hebrew_runs(text))


def _spelled(count: int) -> str:
    """A count in prose: spelled out below five, a numeral from five up."""
    return {1: "one", 2: "two", 3: "three", 4: "four"}.get(count, f"{count:,}")


def _hebrew_cell(form: str | None) -> tuple:
    """A pointed reader-facing Hebrew form wrapped as an hbo run for an RTL table cell."""
    return wrap_hebrew_runs((form or "").replace(hpu.NU_GMAQ, psm.MAQAF))


def _ref_link(bcv: str, text: str | None = None) -> object:
    """The reference, linked to the verse in MAM with doc."""
    bb, chnu, vrnu = _split(bcv)
    return mb_html.anchor_h(
        text or ref_abbrev(bcv),
        rtms_report.mam_with_doc_url(bb=bb, chnu=chnu, vrnu=vrnu),
    )


def _footnote_callout(number: int, footnote_id: str) -> object:
    """The in-line phi marker that links down to one footnote."""
    return mb_html.anchor_h(f"φ{number}", f"#{footnote_id}")


def _split(bcv: str) -> tuple[str, int, int]:
    bb = bcv[:2]
    chnu, _colon, vrnu = bcv[2:].partition(":")
    return bb, int(chnu), int(vrnu)


def _scriptural_bcv_key(bcv: str) -> tuple[int, int, int]:
    """Sort one compact BCV in the repository's canonical scriptural order."""
    bb, chnu, vrnu = _split(bcv)
    return _POST_SILLUQ_BOOK_ORDER[bb], chnu, vrnu


def _table(headers: tuple, rows: list, attr: dict | None = None) -> object:
    return mb_html.table(
        [mb_html.table_row_of_headers(headers), *rows],
        attr or {"class": "limited-width post-stress-meteg-table"},
    )


def _singleton_example_table(bcv: str, form: tuple) -> object:
    """One example displayed in the same two-column table as a multi-row example set."""
    return mb_html.table(
        [
            mb_html.table_row_of_data(
                (_ref_link(bcv), form),
                (None, _HEBREW_CELL),
            )
        ],
        {"class": "limited-width post-stress-meteg-table"},
    )


def _cantillation_label(cantillation: str) -> tuple:
    """One visible cantillation-branch label, with its Hebrew letter name italicized."""
    by_cantillation = {
        psm.CANT_ALEF: _ROM_ALEF,
        psm.CANT_BET: _ROM_BET,
    }
    return ("cant-", by_cantillation[cantillation])


def _hebrew_spacing_option() -> object:
    """The page-wide control for the pointed Hebrew's letter spacing."""
    return mb_html.raw_html(
        _HEBREW_SPACING_OPTION.replace(
            "__SPACING_TEXT__",
            "This checkbox controls whether Hebrew letter spacing is expanded in this"
            " document.",
        ).replace(
            "__TOGGLE_TEXT__",
            "Alternatively, you can click on an individual Hebrew word to toggle only that word's"
            " spacing.",
        )
    )
