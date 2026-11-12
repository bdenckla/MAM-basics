"""Read MAM-morphhb's structure from MAM-parsed plus/: titles, parashot and poetic lines.

Exports read_structure and the Structure it returns.

MAM-simple has none of these, so they come from plus/, by explicit template name:

- a book24's title, from מ:ספר חדש in column C of its first verse;
- the Twelve's prophet names, from מ:רווח בתרי עשר בפסוק הראשון;
- Psalms' five division names, from מ:רווח לספר בתהלים בפסוק הראשון;
- the 54 Torah parashot, from the מ:עלייה inside column D's מ:פסוק whose ב1 is ראשון,
  named by its ב0 as MAM has it;
- poetic line breaks, ר1, ר2 and ר3 in column E, or in column C at Psalms 70:2 and
  108:2, projected to tokens here and placed on MAM-simple's text by morphhb_poetry.

plus/ numbers verses as MAM does.  Every verse read here has the same number in BHS's
numbering, which MAM-morphhb uses; the callers check that against MAM-simple.
"""

import dataclasses

from mb_cmn import bib_locales as tbn
from mb_cmn import read_books_from_mam_parsed_plus as plus
from mb_cmn import template_names as tmpln
from mb_misc import osis_book_abbrevs

_NEW_BOOK = "מ:ספר חדש"
_TWELVE_NAME = "מ:רווח בתרי עשר בפסוק הראשון"
_PSALMS_DIVISION = "מ:רווח לספר בתהלים בפסוק הראשון"
_VERSE_TMPL = "מ:פסוק"
_ALIYAH_PARAM = "עלייה"
_ALIYAH = "מ:עלייה"
_FIRST_ALIYAH = "ראשון"
_TORAH = ("Gen", "Exod", "Lev", "Num", "Deut")

# ר1 starts a line at level 2, ר2 at level 3 and ר3 at level 1, as the 2014 file has
# them; a verse's first line is level 1.  ר0 is a space.
LINE_LEVELS = {"ר1": 2, "ר2": 3, "ר3": 1}
# The tokens of a ketiv/qere, a word with a special letter, or a silluq-before-meteg
# word, which morphhb_poetry also gives MAM-simple's counterparts.
KQ_TOKEN = "<KQ>"
SLH_TOKEN = "<SLH>"
SBM_TOKEN = "<SBM>"
_KQ_TMPLS = {"כו״ק", "קו״כ", "מ:כו״ק מיוחד", "מ:קו״כ-אם-2"}
# Song chapters whose column E has top-level ר3 line breaks.  They belong to the song
# layout, which MAM-morphhb leaves out for now (Ben, 2026-11-03: no song tables; song
# verses are ordinary verse lines), so these breaks go unused.
_SONG_CHAPTERS_WITH_LINE_BREAKS = {("Deut", 32), ("2Sam", 22), ("1Chr", 16)}
_SEP_TMPLS = {"ר0", "מ:לגרמיה-2", "מ:פסק", "מ:מקף אפור", "מ:נו״ן הפוכה"}


@dataclasses.dataclass(frozen=True)
class Structure:
    """What plus/ supplies, keyed by OSIS ids in BHS's (here also MAM's) numbering."""

    book24_titles: dict  # first bk39 OSIS abbreviation -> title
    twelve_titles: dict  # OSIS abbreviation -> prophet name
    psalms_divisions: dict  # chapter number -> division name
    parashot: dict  # osisID of the first verse -> name
    poetic_streams: dict  # osisID -> (column C start level or None, column E stream)


def read_structure(mam_parsed_path):
    """Read every book24 of plus/ and return its Structure."""
    books = plus.read_parsed_plus_bk39s(None, mam_parsed_path)
    book24_titles, twelve_titles, divisions, parashot, streams = {}, {}, {}, {}, {}
    for bk39id, book in books.items():
        abbrev = osis_book_abbrevs.BOOK_ABBREVS[bk39id]
        for bcvt, minirow in book["verses_plus"].items():
            chnu, vrnu = tbn.bcvt_get_chnu_vrnu(bcvt)
            osis_id = f"{abbrev}.{chnu}.{vrnu}"
            for tmpl in _top_templates(minirow.CP):
                name = tmpl["tmpl_name"]
                if name == _NEW_BOOK:
                    _put(book24_titles, abbrev, _only_param(tmpl), osis_id)
                elif name == _TWELVE_NAME:
                    _put(twelve_titles, abbrev, _only_param(tmpl), osis_id)
                elif name == _PSALMS_DIVISION:
                    _put(divisions, chnu, _only_param(tmpl), osis_id)
            if abbrev in _TORAH:
                name = _first_aliyah_name(minirow.DP)
                if name is not None:
                    _put(parashot, osis_id, name, osis_id)
            levels = _column_c_levels(minirow.CP, osis_id)
            column_e = minirow.EP
            if (abbrev, chnu) in _SONG_CHAPTERS_WITH_LINE_BREAKS:
                column_e = [x for x in column_e if not _is_tmpl(x, "ר3")]
            stream = []
            if is_poetic(osis_id):
                plus_stream(column_e, stream)
            elif _has_line_break(column_e) or levels:
                raise ValueError(f"Poetic line break outside poetry at {osis_id}")
            if levels and not is_poetic(osis_id):
                raise ValueError(f"Column C line level outside poetry at {osis_id}")
            if is_poetic(osis_id):
                streams[osis_id] = (levels[0] if levels else None, tuple(stream))
    if len(parashot) != 54:
        raise ValueError(f"Expected 54 parashot, found {len(parashot)}")
    if sorted(divisions) != [1, 42, 73, 90, 107]:
        raise ValueError(f"Unexpected Psalms divisions: {sorted(divisions)}")
    return Structure(book24_titles, twelve_titles, divisions, parashot, streams)


def is_poetic(osis_id):
    """Psalms, Proverbs, and Job 3:2-42:6 are written as poetic lines."""
    book, chnu, vrnu = osis_id.split(".")
    if book in ("Ps", "Prov"):
        return True
    if book == "Job":
        return (3, 2) <= (int(chnu), int(vrnu)) <= (42, 6)
    return False


def plus_stream(node, out):
    """Project plus/ column content to ("text", s), ("atom", token), ("sep", None)
    and ("break", level) items, by explicit template name.

    Each template's name and parameters are first checked by
    validate_current_plus_template, so a parameter this projection would not read
    raises rather than being discarded."""
    if isinstance(node, str):
        out.append(("text", node))
    elif isinstance(node, (list, tuple)):
        for item in node:
            plus_stream(item, out)
    elif isinstance(node, dict):
        params = tmpln.validate_current_plus_template(node)
        name = node["tmpl_name"]
        if name in LINE_LEVELS:
            out.append(("break", LINE_LEVELS[name]))
        elif name in _SEP_TMPLS:
            out.append(("sep", None))
        elif name in _KQ_TMPLS:
            out.append(("atom", KQ_TOKEN))
        elif name == "מ:אות-מיוחדת-במילה":
            out.append(("atom", SLH_TOKEN))
        elif name == "מ:סילוק לפני געיה":
            out.append(("atom", SBM_TOKEN))
        elif name in ("מ:דחי", "מ:צינור", "נוסח"):
            plus_stream(params["1"], out)
        elif name == "מ:קמץ":
            plus_stream(params["ד"], out)
        else:
            raise ValueError(f"Unhandled plus/ template in poetry: {name}")
    else:
        raise TypeError(f"Unexpected plus/ node: {node!r}")


def _top_templates(column):
    return [item for item in column if isinstance(item, dict)]


def _is_tmpl(item, name):
    return isinstance(item, dict) and item["tmpl_name"] == name


def _only_param(tmpl):
    params = tmpl["tmpl_params"]
    if set(params) != {"1"} or not isinstance(params["1"], str):
        raise ValueError(f"Unexpected parameters of {tmpl['tmpl_name']}: {params}")
    return params["1"]


def _put(dic, key, value, where):
    if key in dic:
        raise ValueError(f"Second {value!r} for {key!r} at {where}")
    dic[key] = value


def _verse_templates(column_d):
    """Column D's מ:פסוק calls: at top level, or as the reading of a נוסח, as at
    Numbers 19:1 and Deuteronomy 21:10 and 31:1, where a note follows in parameter 2."""
    for tmpl in _top_templates(column_d):
        if tmpl["tmpl_name"] == _VERSE_TMPL:
            yield tmpl
        elif tmpl["tmpl_name"] == "נוסח":
            reading = tmpl["tmpl_params"]["1"]
            for sub in reading if isinstance(reading, (list, tuple)) else [reading]:
                if _is_tmpl(sub, _VERSE_TMPL):
                    yield sub


def _first_aliyah_name(column_d):
    names = []
    for tmpl in _verse_templates(column_d):
        aliyah = (tmpl.get("tmpl_params") or {}).get(_ALIYAH_PARAM)
        if aliyah is None:
            continue
        if aliyah["tmpl_name"] != _ALIYAH:
            raise ValueError(f"Unexpected aliyah template: {aliyah['tmpl_name']}")
        params = aliyah["tmpl_params"]
        if params.get("ב1") == _FIRST_ALIYAH:
            names.append(params["ב0"])
    if len(names) > 1:
        raise ValueError(f"Two parashah starts in one verse: {names}")
    return names[0] if names else None


def _column_c_levels(column_c, osis_id):
    """Line levels that column C gives a verse's first line: ר1 at Psalms 70:2 and
    108:2, inside נוסח's parameter 1.  A line break anywhere else in column C raises."""
    levels = []
    for item in column_c:
        if not isinstance(item, dict):
            continue
        if item["tmpl_name"] in LINE_LEVELS:
            levels.append(LINE_LEVELS[item["tmpl_name"]])
        elif item["tmpl_name"] == "נוסח":
            reading = item["tmpl_params"]["1"]
            for sub in reading if isinstance(reading, (list, tuple)) else [reading]:
                if isinstance(sub, dict) and sub["tmpl_name"] in LINE_LEVELS:
                    levels.append(LINE_LEVELS[sub["tmpl_name"]])
            if _has_line_break(item["tmpl_params"].get("2", [])):
                raise ValueError(f"Line break in a note in column C at {osis_id}")
        elif _has_line_break(item.get("tmpl_params") or {}):
            raise ValueError(f"Nested line break in column C at {osis_id}")
    if len(levels) > 1:
        raise ValueError(f"Two column C line levels at {osis_id}: {levels}")
    return levels


def _has_line_break(node):
    if isinstance(node, (list, tuple)):
        return any(_has_line_break(item) for item in node)
    if isinstance(node, dict):
        if node.get("tmpl_name") in LINE_LEVELS:
            return True
        return any(_has_line_break(v) for v in node.values())
    return False
