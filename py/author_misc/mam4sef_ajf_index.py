"""The AJF variant of MAM for Sefaria: writes ``gh-pages/MAM-for-Sefaria/ajf/index.html``.

The AJF variant, ``csv-ajf/`` and its listings in ``misc/unicode-names-ajf/``, was described in
"The encoding of MAM for Sefaria" until Ben's decision of 2026-10-26 to give it a page of its
own that no page of the documentation links to; ``mam4sef_common.py`` has his words.  So this
page links to the other two, and neither of them names it or its folders.  "AJF" stays
unexpanded until Ben supplies its meaning.

The page describes the variant by what it shares with ``csv/`` and how it differs, every
statement of which ``mam4sef_survey`` checks: the counts of what both folders have, the spelling
of each thing that ``csv/`` marks up, and the strands of each letter that has a COMBINING
GRAPHEME JOINER in a verse with two cantillations.
"""

import re

from mb_author import author
from mb_cmn import bib_locales as tbn
from mb_cmn import hebrew_points as hpo
from mb_cmn import hebrew_punctuation as hpu
from mb_cmn import str_defs as sd
from mb_misc import mb_html
from author_misc import mam4sef_common as mc
from author_misc import mam4sef_survey as ms

_INDEX_HREF = "../index.html"
_LISTINGS_HREF = f"../{mc.LISTINGS_DIR}/index.html"
_MAM_SIMPLE_GUIDE = "../../MAM-simple/reading-mam-simple-json.html"
_VERSIFICATION = "../../MAM-simple/versification-differences.html"
_QAMATS = "\N{HEBREW POINT QAMATS}"
_PATAH = "\N{HEBREW POINT PATAH}"
# The verse with two cantillations outside the Decalogues.
_EX_SAGA_OF_REUBEN = "Genesis 35:22"


def _intro():
    return [
        author.heading_level_2("Introduction", {"id": "introduction"}),
        mc.p(
            "Beside its files for Sefaria, ",
            mb_html.anchor_h(mc.code("MAM-for-Sefaria"), mc.PRODUCT_URL),
            " has an AJF variant of them: the folder ",
            mc.code(f"{ms.FOLDER_AJF}/"),
            ", and the folder ",
            mc.code(f"{ms.FOLDER_NAMES_AJF}/"),
            ", which lists its code points. This page describes the two. It tells them"
            " apart from the folders ",
            mc.code(f"{ms.FOLDER_CSV}/"),
            " and ",
            mc.code(f"{ms.FOLDER_NAMES}/"),
            ", which the pages ",
            mc.title_link(mc.INDEX_TITLE, _INDEX_HREF),
            " and ",
            mc.title_link(mc.LISTINGS_TITLE, _LISTINGS_HREF),
            " describe. Every count and example on it is taken from the files.",
        ),
        *mc.conventions(attention=True),
    ]


def _files(s):
    t = s.ajf_text
    spellings = [
        (
            ["a ", "$samekh", " break"],
            [
                mc.uname(sd.NBSP),
                ", then ",
                mc.code("{ס}"),
                " in a span, then eight more",
            ],
            [mc.uname(" "), ", ", mc.code("{ס}"), ", ", mc.uname(" ")],
        ),
        (
            ["a ", "$pe", " break"],
            [
                mc.uname(sd.NBSP),
                ", then ",
                mc.code("{פ}"),
                " in a span, then ",
                mc.code("<br>"),
            ],
            [mc.uname(" "), ", ", mc.code("{פ}"), ", ", mc.uname(" ")],
        ),
        (
            ["a ", "$legarmeh"],
            [
                mc.uname(sd.THSP),
                ", then ",
                mc.uname(hpu.PASOLEG),
                " in ",
                mc.code("<b>"),
            ],
            [mc.uname(hpu.PASOLEG), ", right after its atom"],
        ),
        (
            ["a ", "$paseq"],
            [
                mc.uname(sd.THSP),
                ", ",
                mc.uname(hpu.PASOLEG),
                " in ",
                mc.code("<small>"),
                ", ",
                mc.uname(sd.THSP),
            ],
            ["two ", mc.uname(hpu.PASOLEG), " marks, with no space on either side"],
        ),
        (
            ["a space of song spacing"],
            ["eight ", mc.uname(sd.NBSP), " characters"],
            [mc.uname(" ")],
        ),
        (
            ["a $ketiv and its $qere"],
            ["in the order $MAM has them"],
            ["the $ketiv first"],
        ),
        (
            ["a trivial pair, an implicit $maqaf, or a small, large or hung letter"],
            ["in a span or element of its own"],
            ["the text alone"],
        ),
    ]
    rows = [
        mc.tr([mc.td(what), mc.td(in_csv), mc.td(in_ajf)])
        for what, in_csv, in_ajf in spellings
    ]
    spaced_title = next(book for book in ms.BOOKS if " " in book)
    cases = s.silluq_cases
    return [
        author.heading_level_2("The files", {"id": "files"}),
        mc.p(
            "The folder ",
            mc.code(f"{ms.FOLDER_AJF}/"),
            f" has a file for each of the {len(ms.BOOKS)} books, named as the file of ",
            mc.code(f"{ms.FOLDER_CSV}/"),
            " for that book is, as ",
            mc.code(f"{spaced_title}.csv"),
            " is, and a provenance note, ",
            mc.code(ms.PROVENANCE_NAME),
            ". Each book's file is a CSV file in UTF-8, with CRLF line ends and no"
            " byte-order mark, as those of ",
            mc.code(f"{ms.FOLDER_CSV}/"),
            f" are, but it has no header. Each of its {mc.num(len(s.ajf_rows))} rows is a"
            " verse, with four fields: the verse's reference, its text, and its ",
            mc.code("cant-alef"),
            " and ",
            mc.code("cant-bet"),
            f" strands, which are empty but in the {len(s.dual_cant_refs)} verses that have"
            f" two cantillations: {mc.refs(s.dual_cant_refs)}.",
        ),
        mc.p(
            "In those verses the second field has the text that represents both strands, as ",
            mc.code(f"{ms.FOLDER_CSV}/"),
            " has it too. The third and fourth fields have the strands themselves, which are,"
            " as ",
            mb_html.anchor_h(
                "the guide to MAM-simple's JSON",
                f"{_MAM_SIMPLE_GUIDE}#dual-cantillation-cant-all-three",
            ),
            " says, the ",
            mc.he("תחתון"),
            " and ",
            mc.he("עליון"),
            " strands in the Decalogues, and the ",
            mc.he("פשוטה"),
            " and ",
            mc.he("מדרשית"),
            f" strands at {mc.short_ref(_EX_SAGA_OF_REUBEN)}.",
        ),
        mc.p(
            "The text is plain: it has no HTML, and neither of the two spaces that ",
            mc.code(f"{ms.FOLDER_CSV}/"),
            " writes as character references. So the two folders spell some things"
            " differently:",
        ),
        mc.table(
            ["", mb_html.code(f"{ms.FOLDER_CSV}/"), mb_html.code(f"{ms.FOLDER_AJF}/")],
            rows,
        ),
        mc.p(
            "In the text field of ",
            mc.code(f"{ms.FOLDER_AJF}/"),
            ", each of these has the count it has in ",
            mc.code(f"{ms.FOLDER_CSV}/"),
            f": {mc.num(t['combined legarmeh'])} $legarmeh and"
            f" {mc.num(t['combined paseq'])} $paseq marks, {mc.num(t['combined samekh'])}"
            f" $samekh and {mc.num(t['combined pe'])} $pe breaks, and"
            f" {mc.num(t['combined pairs'])} pairs of a $ketiv and its $qere.",
        ),
        mc.p(
            f"At each of the {len(cases)} atoms where $MAM's source identifies a ",
            mc.rom("silluq"),
            " with a $meteg after it, the text field has the atom that ",
            mc.code(f"{ms.FOLDER_CSV}/"),
            " has, without that $meteg. The section ",
            mb_html.anchor_h(
                author.dollar_sub(["A $meteg after the ", mc.rom("silluq")]),
                f"{_INDEX_HREF}#meteg-after-silluq",
            ),
            " of ",
            mc.title_link(mc.INDEX_TITLE, _INDEX_HREF),
            " shows them.",
        ),
        *_numbering(s),
    ]


def _numbering(s):
    return [
        author.heading_level_3("Verse numbering"),
        mc.p(
            "The verses of ",
            mc.code(f"{ms.FOLDER_AJF}/"),
            " are numbered as $BHS numbers them, and those of ",
            mc.code(f"{ms.FOLDER_CSV}/"),
            " as Sefaria numbers them, so a reference can name different text in the two"
            " folders. The page ",
            mb_html.anchor_h(
                "Versification Differences: MAM, BHS, and Sefaria", _VERSIFICATION
            ),
            " lists the differences. Every reference of ",
            mc.code(f"{ms.FOLDER_CSV}/"),
            " is also in ",
            mc.code(f"{ms.FOLDER_AJF}/"),
            f", which has {len(s.refs_only_ajf)} more: {mc.refs(s.refs_only_ajf)}.",
        ),
        mc.p(
            "As in ",
            mc.code(f"{ms.FOLDER_CSV}/"),
            f", the rows of {mc.refs(s.em_dash_ajf)}, for which $MAM has no text, have"
            " only an ",
            mc.uname(ms.EM_DASH),
            " (",
            ms.EM_DASH,
            ") as their text, and the files have no other ",
            mc.uname(ms.EM_DASH),
            ".",
        ),
    ]


def _listings(s):
    row = next(row for row in s.ajf_rows if row.bk39id != row.book)
    head = f"{row.bk39id} {row.chapter}:{row.verse} in vtrad {tbn.VT_BHS}"
    strands = [mc.code(strand) for strand in ms.AJF_STRANDS]
    chars = sorted(s.code_points_ajf)
    rows = [
        mc.tr(
            [
                mb_html.table_datum(mc.code(f"U+{ord(c):04X}")),
                mb_html.table_datum(mc.uname(c, full=True)),
                mb_html.table_datum(mc.code(ms.short_name_in_listings(c))),
                mc.td_num(s.code_points_ajf[c]),
            ]
        )
        for c in chars
    ]
    return [
        author.heading_level_2("The listings", {"id": "listings"}),
        mc.p(
            "The folder ",
            mc.code(f"{ms.FOLDER_NAMES_AJF}/"),
            " has a listing for each file of ",
            mc.code(f"{ms.FOLDER_AJF}/"),
            ", named and written as those of ",
            mc.code(f"{ms.FOLDER_NAMES}/"),
            " are, which the page ",
            mc.title_link(mc.LISTINGS_TITLE, _LISTINGS_HREF),
            " describes, but for three things:",
        ),
        author.ordered_list(
            [
                [
                    "The line that names a verse gives $BHS's numbering, as ",
                    mc.code(head),
                    " does.",
                ],
                [
                    "The text has no HTML, so no line has ",
                    mc.code("START"),
                    " or ",
                    mc.code("STOP"),
                    ".",
                ],
                [
                    "A verse with two cantillations lists each of its three texts after a"
                    " line that names it, ",
                    *mc.join(strands, "or"),
                    ", with the text's lines indented by four spaces.",
                ],
            ]
        ),
        mc.p(
            f"In {s.listings['ajf stripped']} of those verses, the listing's ",
            strands[-1],
            " text ends with a ",
            mc.code("SPACE"),
            " line that the file lacks: the strand ends with a $samekh break, and the"
            " writer of the CSV files strips spaces from the end of a row's last field,"
            " while the listings are written from the unstripped text.",
        ),
        mc.p(
            f"These are all {len(chars)} code points that the text and strand fields of ",
            mc.code(f"{ms.FOLDER_AJF}/"),
            " have, with the short name that each has in the listings, and how many times"
            " the fields have it:",
        ),
        mc.table(["Code point", "Unicode name", "In the listings", "Count"], rows),
    ]


def _aligned_words(fields: list, position: int) -> list:
    """For aligned texts, the chanted words around atom ``position``, whole in every text."""
    atoms = [list(ms.ATOM_RE.finditer(f)) for f in fields]

    def word_of(field, match):
        return len(re.findall(r"\s+", field[: match.start()].lstrip()))

    word_ids = [[word_of(f, m) for m in found] for f, found in zip(fields, atoms)]
    lo = hi = position
    while True:
        new_lo, new_hi = lo, hi
        for ids in word_ids:
            new_lo = min(new_lo, min(i for i, w in enumerate(ids) if w == ids[lo]))
            new_hi = max(new_hi, max(i for i, w in enumerate(ids) if w == ids[hi]))
        if (new_lo, new_hi) == (lo, hi):
            break
        lo, hi = new_lo, new_hi
    out = []
    for field, found in zip(fields, atoms):
        start, end = mc.chanted_words(field, found[lo].start(), found[hi].end())
        out.append(field[start:end])
    return out


def _cgj_rows_strands(s, kind):
    by_atom = {}
    for hit in s.cgj[kind]:
        by_atom.setdefault(hit["atom"], []).append(hit)
    rows = []
    for atom, hits in by_atom.items():
        strands = hits[0]["strands"]
        row = s.ajf_row(strands["ref"])
        fields = [row.combined, row.alef, row.bet]
        combined_atoms = [m.group() for m in ms.ATOM_RE.finditer(row.combined)]
        position = combined_atoms.index(atom)
        combined, alef, bet = _aligned_words(fields, position)
        cluster_index = mc.cgj_index(atom)

        def shown(text, strand_atom):
            start, end = mc.find_atom(text, strand_atom, row.ref)
            parts = [
                text[:start],
                *mc.highlight(strand_atom, cluster_index),
                text[end:],
            ]
            return [part for part in parts if part != ""]

        # The three forms one above the other in one cell, in the order the header names.
        forms = [
            *shown(combined, atom),
            mb_html.line_break(),
            *shown(alef, strands["alef"]),
            mb_html.line_break(),
            *shown(bet, strands["bet"]),
        ]
        rows.append(
            mc.tr(
                [
                    mc.td_he(forms),
                    mc.td_refs([h["strands"]["ref"] for h in hits]),
                    mc.td_refs([h["ref"] for h in hits]),
                    mb_html.table_datum(mc.name_list(hits[0]["cluster"])),
                ]
            )
        )
    return rows


def _strands(s):
    cgj = s.cgj
    headers = [
        [
            "Both strands",
            mb_html.line_break(),
            mb_html.code("cant-alef"),
            mb_html.line_break(),
            mb_html.code("cant-bet"),
        ],
        ["In ", mb_html.code(f"{ms.FOLDER_AJF}/")],
        ["In ", mb_html.code(f"{ms.FOLDER_CSV}/")],
        "The letter's code points",
    ]
    n_strands = len(cgj["qupo"]) + len(cgj["accent-meteg"])
    return [
        author.heading_level_2("Two strands on one letter", {"id": "two-strands"}),
        mc.p(
            "Every atom of ",
            mc.code(f"{ms.FOLDER_CSV}/"),
            " that has a ",
            mc.uname(sd.CGJ, full=True),
            " (",
            mc.cgj(),
            ") is in the text field of ",
            mc.code(f"{ms.FOLDER_AJF}/"),
            " as often, and the strand fields have no ",
            mc.cgj(),
            f". In the verses with two cantillations, {mc.num(n_strands)} letters have a ",
            mc.cgj(),
            ", and on each of them the marks before it are one strand's, and the marks"
            " after it the other's. Each strand field has that letter with its own marks"
            " alone, which the tables show in the attention color. They give each atom's"
            " references in both folders, since the two numberings differ in the"
            f" Decalogues. In {mc.num(len(cgj['qupo']))} atoms, one strand has a ",
            mc.uname(_QAMATS),
            " and an accent or ",
            mc.uname(hpo.MTGOSLQ),
            " below the letter, and the other a ",
            mc.uname(_PATAH),
            " and an accent above it:",
        ),
        mc.table(headers, _cgj_rows_strands(s, "qupo")),
        mc.p(
            f"In {mc.num(len(cgj['accent-meteg']))} atoms, one strand has an accent below"
            " the letter, and the other a ",
            mc.uname(hpo.MTGOSLQ),
            ":",
        ),
        mc.table(headers, _cgj_rows_strands(s, "accent-meteg")),
    ]


def _pin_claims(s) -> None:
    """Fail the build if the data stops supporting a claim the prose states in words."""
    # "Every reference of csv/ is also in csv-ajf/."
    assert not s.refs_only_csv
    # "As in csv/, the rows of ..., for which MAM has no text": the same references.
    assert s.em_dash_ajf == s.em_dash_csv and s.em_dash_ajf
    # The verse with two cantillations outside the Decalogues is the one named.
    assert _EX_SAGA_OF_REUBEN in s.dual_cant_refs
    # "a listing for each file of csv-ajf/": every row is listed.
    assert s.listings["ajf verses"] == len(s.ajf_rows)
    # "In N of those verses ...": some, which the survey checks one by one.
    assert s.listings["ajf stripped"]
    # The strands and the table of spellings: check_handlers raises if a handler changes.
    ms.check_handlers()


def gen_html_file():
    """Write the page and its font, and return the page's path."""
    s = ms.survey()
    _pin_claims(s)
    cbody = [
        *mc.page_head(mc.AJF_TITLE),
        *_intro(),
        *_files(s),
        *_listings(s),
        *_strands(s),
    ]
    return mc.write_page(__file__, mc.AJF_DIR, mc.AJF_TITLE, cbody, s)
