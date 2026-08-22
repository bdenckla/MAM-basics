"""Generate index-flat-annotated.json from index-flat-corrected.json.

Adds two fields to each page record in the body:

  de_start_whole: True  — the start verse is completely present on this page.
                  False — the start verse is only partially present (the page
                          begins mid-verse).
                  None  — cannot be determined from available evidence.

  de_end_whole:   True  — the end verse is completely present on this page.
                  False — the end verse is only partially present (the page
                          ends mid-verse).
                  None  — cannot be determined from available evidence.

Inference rules
---------------
For **non-gap boundaries** the wholeness is inferred from adjacent records:

  * A page's *end* verse is partial if the next page's *start* verse is the
    same triple [book, ch, v] and no gap intervenes.  Otherwise it is whole.
  * A page's *start* verse is partial if the previous page's *end* verse is
    the same triple and no gap intervenes.  Otherwise it is whole.

For **gap-boundary verses** (start verse after a "Before" gap, end verse
before an "After" gap) the wholeness is resolved from the gh-pages/ directory,
which records the exact Hebrew words at which each missing section begins and
ends.  The resolved values are encoded in _GAP_WHOLENESS below.

Usage
-----
    .venv/Scripts/python.exe py/main_ac_gen_index_flat_annotated.py [INPUT [OUTPUT]]

Defaults:
    INPUT  = aleppo-wiki/index-flat-corrected.json
    OUTPUT = index-flat-annotated.json

Both defaults were wrong until 2026-08-22, and in two different ways.  The Usage
block named ``../codex-index/aleppo/`` for each -- a sibling repo whose ``aleppo/``
directory became this repo's ``aleppo-wiki/`` in ``9025037`` (2026-03-28).  Of the
two, only DEFAULT_INPUT was really spelled that way in the code, so the input was as
dead as the four literals in ``aleppo-wiki/main_make_wikisource_page.py``, dead the
same way and since the same day.  DEFAULT_OUTPUT was already this repo's root, so
there the Usage block was simply describing something the code did not do.
"""

import json
import sys
from pathlib import Path

import ac_paths

DEFAULT_INPUT = ac_paths.flat_index_corrected_path()
DEFAULT_OUTPUT = ac_paths.flat_index_annotated_path()

# ---------------------------------------------------------------------------
# Gap-boundary wholeness table
#
# Each entry maps (leaf, "start"|"end") to True (whole) or False (partial).
#
# Sources:
#   * gh-pages/missing_sections_torah.html  — Torah gaps
#   * gh-pages/missing_sections_nakh.html   — Nakh gaps (incl. mgketer footnote)
# ---------------------------------------------------------------------------
_GAP_WHOLENESS = {
    # Torah — the codex begins mid-Deut 28:17 ("וּמִשְׁאַרְתֶּֽךָ")
    ("1r", "start"): False,
    # Kings — gap begins mid-2 Kgs 14:21 ("אֶת־עֲזַרְיָ֔ה וְה֕וּא...")
    ("99v", "end"): False,
    # Kings — gap ends mid-2 Kgs 18:13 ("...וּבְאַרְבַּע֩ עֶשְׂרֵ֨ה שָׁנָ֜ה")
    ("100r", "start"): False,
    # Jeremiah — gap begins at end of Jer 29:9 ("יְהֹוָֽה׃...")
    ("147v", "end"): False,
    # Jeremiah — the missing section ends mid-verse (opening words of the
    # "sun for light by day" verse, "...כֹּ֣ה ׀ אָמַ֣ר יְהֹוָ֗ה נֹתֵ֥ן",
    # cited as 31:34 in gh-pages); 148r begins with the remainder of that verse
    ("148r", "start"): False,
    # Jeremiah — the missing section (per mgketer, 32:14–19) begins mid-verse
    ("148r", "end"): False,
    # Jeremiah — the missing section (per mgketer, 32:14–19) ends mid-verse
    ("148v", "start"): False,
    # Amos — gap begins at Amos 8:13; Amos 8:12 is therefore whole on 197v
    ("197v", "end"): True,
    # Micah — gap ends mid-Mic 5:1 ("...וּמוֹצָאֹתָ֥יו מִקֶּ֖דֶם")
    ("198r", "start"): False,
    # Zephaniah — gap begins mid-Zeph 3:20 ("הָאָ֔רֶץ בְּשׁוּבִ֧י...")
    ("201v", "end"): False,
    # Zechariah — gap ends mid-Zech 9:17 ("...וּמַה־יׇּפְי֑וֹ דָּגָן֙")
    ("202r", "start"): False,
    # Psalms — gap begins at Ps 15:1; Ps 14:7 is therefore whole on 243v
    ("243v", "end"): True,
    # Psalms — gap ends at end of Ps 25:1; Ps 25:2 begins fresh and whole
    ("244r", "start"): True,
    # Song of Songs — codex ends mid-Song 3:11 ("בְּנ֥וֹת צִיּ֖וֹן" survives;
    # "בַּמֶּ֣לֶךְ שְׁלֹמֹ֑ה" onwards is missing)
    ("294v", "end"): False,
}


def _has_before_gap(rec):
    g = rec.get("de_gap")
    return g == "Before" or (isinstance(g, list) and "Before" in g)


def _has_after_gap(rec):
    g = rec.get("de_gap")
    return g == "After" or (isinstance(g, list) and "After" in g)


def _start_verse(rec):
    return rec["de_text_range"][0]


def _end_verse(rec):
    return rec["de_text_range"][1]


def annotate(records):
    """Return a new list of records with de_start_whole / de_end_whole added."""
    out = []
    n = len(records)

    for i, rec in enumerate(records):
        leaf = rec["de_leaf"]
        new_rec = dict(rec)

        # --- de_start_whole ---
        if _has_before_gap(rec):
            new_rec["de_start_whole"] = _GAP_WHOLENESS.get((leaf, "start"))
        elif i == 0:
            # First record, no before-gap — treat as whole (codex started here)
            new_rec["de_start_whole"] = True
        else:
            prev = records[i - 1]
            if _end_verse(prev) == _start_verse(rec):
                new_rec["de_start_whole"] = False  # verse spans the page turn
            else:
                new_rec["de_start_whole"] = True

        # --- de_end_whole ---
        if _has_after_gap(rec):
            new_rec["de_end_whole"] = _GAP_WHOLENESS.get((leaf, "end"))
        elif i == n - 1:
            # Last record, no after-gap — treat as whole
            new_rec["de_end_whole"] = True
        else:
            nxt = records[i + 1]
            if _end_verse(rec) == _start_verse(nxt):
                new_rec["de_end_whole"] = False  # verse spans the page turn
            else:
                new_rec["de_end_whole"] = True

        out.append(new_rec)

    return out


def main():
    in_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_INPUT
    out_path = Path(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_OUTPUT

    data = json.loads(in_path.read_text(encoding="utf-8"))
    data["body"] = annotate(data["body"])

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="",
    )
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
