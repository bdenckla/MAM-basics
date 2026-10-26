"""The encoding of MAM for Sefaria: writes ``gh-pages/MAM-for-Sefaria/index.html``.

Ben's decision of 2026-10-24, which ``doc/PLAN-rewrite-MAM-for-Sefaria-encoding-page.md``
records, was to rewrite this page "from fresh perspective of just documenting what MAM for
Sefaria contains".  Until then it was a hand-authored page that documented MAM-for-Sefaria by
its differences from Sefaria's earlier Tanakh, with the figures of Sefaria's 2021 copy of MAM.
Now it describes the files as they are, and compares them with no other text.

WHAT IT COVERS.  The folder ``csv/``, the files that Sefaria imports.  The listings of
``misc/unicode-names/`` have a page of their own, to which this one links, and the AJF variant
has a page that no page of the documentation links to, so nothing here names its folders;
``mam4sef_common.py`` gives Ben's words for both, of 2026-10-26.

WHERE EVERYTHING COMES FROM.  ``mam4sef_survey`` reads the product's tracked files with closed
dispatch and counts what they have; every count, list and example here comes from it.  An
example is a lookup that must match exactly one place in the files, by a reference and the
letters of its atoms, as ``accgram.maqaf_nonfinal_accents_page._find_span`` and
``author_site.post_stress_meteg_post_silluq_data._source_focus_word`` look forms up, so no
pointed Hebrew on the page is typed here.  ``_pin_claims`` defends the sentences whose truth the
data could overturn, and raises rather than warns.

POINTED HEBREW KEEPS ITS VOWELS HERE.  The house rule shows a form by its letters and accents
alone (the ``hebrew-prose`` skill's ``core-rules.md``, "Show it in Unicode").  This page
documents how the files encode every mark, vowels among them, which is the exception that rule
allows where the vowel is the point.

NEVER A FORM WITHOUT ITS CGJ.  ``mam4sef_common.write_page`` refuses to write the page if any
Hebrew on it has two vowels on one letter, except where the files have them, with the COMBINING
GRAPHEME JOINER between them that keeps their order.  The old page's table of Sefaria's earlier
Exodus 20:4 had such a letter with no CGJ, and how it looked depended on the font.

THE FONT.  The page's ``styles.css`` loads the site's one copy of Taamey D,
``gh-pages/woff2/Taamey_D.woff2``, under the family name "Taamey D WOFF2", so a reader sees
MAM-basics' Taamey D with nothing installed and no locally installed Taamey D takes its place.

``py/tests/test_sefaria_silluq_documentation.py`` parses the meteg-after-silluq table that
``_meteg_after_silluq`` writes, and checks it against MAM-simple and both exporters' handlers:
keep its id, its ``data-osis-id`` column headers, its two ``data-version`` rows and their labels.
"""

import html.parser as html_parser
import re

from mb_author import author
from mb_cmn import hebrew_accents as ha
from mb_cmn import hebrew_points as hpo
from mb_cmn import hebrew_punctuation as hpu
from mb_cmn import str_defs as sd
from mb_cmn import unicode_data
from mb_misc import mb_html
from author_misc import mam4sef_common as mc
from author_misc import mam4sef_survey as ms

_MAM_SIMPLE_GUIDE = "../MAM-simple/reading-mam-simple-json.html"
_VERSIFICATION = "../MAM-simple/versification-differences.html"
_GRAY_MAQAF = "../MAM-with-doc/misc/he_ws_intro_to_mam_gray_maqaf_1.html"
_LISTINGS_HREF = f"{mc.LISTINGS_DIR}/index.html"

_PATAH = "\N{HEBREW POINT PATAH}"
_QAMATS = "\N{HEBREW POINT QAMATS}"
_HIRIQ = "\N{HEBREW POINT HIRIQ}"
_SHEVA = "\N{HEBREW POINT SHEVA}"
_LAMED = "\N{HEBREW LETTER LAMED}"
_QAMATS_QATAN = "\N{HEBREW POINT QAMATS QATAN}"
_HOLAM_HASER_FOR_VAV = "\N{HEBREW POINT HOLAM HASER FOR VAV}"

# THE EXAMPLES, each a lookup that must match exactly one place: a reference as the files
# write it, and the parts of the text there, each part either the letters of one atom or the
# literal characters between atoms.  Letters fix the grouping as well as the letters.
_EX_LEGARMEH = ("Genesis 2:5", ("וכל", sd.THSP + hpu.PASOLEG + " ", "שיח"))
_EX_PASEQ = ("Genesis 1:5", ("אלהים", sd.THSP + hpu.PASOLEG + sd.THSP, "לאור"))
_EX_TRIVIAL = ("Genesis 13:3", ("אהלה",))
_EX_LETTER_SIZES = (
    ("Daniel 6:20", ("בשפרפרא",), "a small letter and a large one"),
    ("Job 38:13", ("רשעים",), "a hung letter"),
)
# A ketiv/qere pair: a reference, the letters of each word of the ketiv, and those of the qere.
_EX_SMALL_IN_KETIV = ("Job 7:5", ("וגיש",), ("וגוש",))
_EX_KQ = {
    ("ketiv first", "space", 1, 1): ("Genesis 8:17", ("הוצא",), ("היצא",)),
    ("qere first", "space", 1, 1): ("Genesis 36:5", ("יעיש",), ("יעוש",)),
    ("ketiv first", "space", 2, 1): ("Judges 16:25", ("כי", "טוב"), ("כטוב",)),
    ("ketiv first", "space", 1, 2): ("Genesis 30:11", ("בגד",), ("בא", "גד")),
    ("ketiv first", "space", 2, 2): (
        "II Samuel 5:2",
        ("הייתה", "מוציא"),
        ("היית", "המוציא"),
    ),
    ("qere first", "space", 1, 2): ("II Kings 18:27", ("שניהם",), ("מימי", "רגליהם")),
    ("ketiv first", "space", 3, 3): (
        "II Samuel 21:12",
        ("תלום", "שם", "הפלשתים"),
        ("תלאום", "שמה", "פלשתים"),
    ),
    ("ketiv first", "maqaf", 1, 1): ("Isaiah 26:20", ("יעבור",), ("יעבר",)),
    ("ketiv first", "maqaf", 1, 2): ("I Chronicles 9:4", ("בנימן",), ("בני", "מן")),
}
_EX_KETIV_VELO_QERE = ("Ruth 3:12", "אם")
_EX_QERE_VELO_KETIV = ("Ruth 3:17", "אלי")
_EX_OWN_CODE_POINT = {
    _QAMATS_QATAN: ("Genesis 1:26", ("ובכל", hpu.MAQ, "הרמש")),
    _HOLAM_HASER_FOR_VAV: ("Genesis 4:13", ("עוני",)),
    ha.ATN_H: ("Psalms 1:1", ("בעצת",)),
}
# The zarqa's stress helper on an earlier letter than the ZINOR, and a ZINOR on a lamed.
_EX_ZARQA_HELPER = ("Genesis 19:4", ("טרם",))
_EX_ZARQA_LAMED = ("Leviticus 4:2", ("ישראל",))
# One example of each kind of Jerusalem atom, by the lamed's own vowel and the orphaned vowel.
_EX_JERUSALEM = {
    (_PATAH, _HIRIQ): ("Judges 1:7", ("ירושלם",)),
    (_QAMATS, _HIRIQ): ("Joshua 15:8", ("ירושלם",)),
    (_PATAH, _SHEVA): ("Isaiah 36:2", ("ירושלמה",)),
    (_QAMATS, _SHEVA): ("II Kings 9:28", ("ירושלמה",)),
}

# author.py has no key for silluq by design: U+05BD is silluq only on a verse-final atom, so
# no code point names it.  On this page MAM's annotation identifies each silluq it names.
_SILLUQ = mc.rom("silluq")


def _kq_element(ref: str, ketiv: tuple, qere: tuple, s):
    """The one ketiv/qere pair at ``ref`` with these letters in its two parts."""
    verse = s.verse(ref)

    def words(el):
        return tuple(ms.letters_of(w) for w in el.text()[1:-1].split(" "))

    hits = []
    for el in verse.elements:
        if el.kind == "kq":
            parts = {k.kind: k for k in el.kids if isinstance(k, ms.Element)}
            if words(parts["ketiv"]) == ketiv and words(parts["qere"]) == qere:
                hits.append(el)
    if len(hits) != 1:
        raise ValueError(f"{ref}: {len(hits)} ketiv/qere pairs {ketiv} {qere}")
    return verse, hits[0]


def _velo_element(ref: str, kind: str, letters: str, s):
    verse = s.verse(ref)
    hits = [
        el
        for el in verse.elements
        if el.kind == kind
        and el.parent_kind is None
        and ms.letters_of(el.text()) == letters
    ]
    if len(hits) != 1:
        raise ValueError(f"{ref}: {len(hits)} lone {kind} {letters}")
    return verse, hits[0]


# THE PAGE -------------------------------------------------------------------------------------


def _intro():
    return [
        author.heading_level_2("Introduction", {"id": "introduction"}),
        mc.p(
            "$MAM (Miqra According to the Masorah) is a digital edition of the Hebrew Bible,"
            " based on the Aleppo Codex and related manuscripts, whose text is on Hebrew"
            " Wikisource. $MAM-for-Sefaria is the extract of $MAM that Sefaria imports and"
            " shows as its default Tanakh. This page describes the files that Sefaria"
            " imports, what they have, and how they encode it.",
        ),
        mc.p(
            "The files are in the folder ",
            mc.code(f"{ms.FOLDER_CSV}/"),
            " of the ",
            mb_html.anchor_h(mc.code("MAM-for-Sefaria"), mc.PRODUCT_URL),
            " directory of the repository ",
            mc.code("MAM-basics"),
            ", whose ",
            mb_html.anchor_h("README", mc.README_URL),
            " says how current they are. Every example of $MAM-for-Sefaria on this page, and"
            " every count of what it has, is taken from those files.",
        ),
        *mc.conventions(attention=True),
    ]


def _files(s):
    headers = s.headers
    rows = [
        mc.tr([mc.td(mc.code("Index Title")), mc.td("the book's title on Sefaria")]),
        mc.tr(
            [mc.td(mc.code("Version Title")), mc.td(mc.code(headers["Version Title"]))]
        ),
        mc.tr([mc.td(mc.code("Language")), mc.td(mc.code(headers["Language"]))]),
        mc.tr(
            [
                mc.td(mc.code("Version Source")),
                mb_html.table_datum(
                    mb_html.anchor_h(
                        mc.code(headers["Version Source"]), headers["Version Source"]
                    )
                ),
            ]
        ),
        mc.tr([mc.td(mc.code("Version Notes")), mc.td("the paragraph of HTML below")]),
    ]
    first = s.verses[0]
    spaced_title = next(book for book in ms.BOOKS if " " in book)
    return [
        author.heading_level_2("The files", {"id": "files"}),
        mc.p(
            "The folder ",
            mc.code(f"{ms.FOLDER_CSV}/"),
            f" has a file for each of the {len(ms.BOOKS)} books, named by the book's title on"
            " Sefaria, as ",
            mc.code(f"{spaced_title}.csv"),
            " is, and a provenance note, ",
            mc.code(ms.PROVENANCE_NAME),
            ". Each book's file is a CSV file in UTF-8, with CRLF line ends and no byte-order"
            " mark. Its first five rows are a header, each row a key and its value. Every file"
            " has the same values, but for the first:",
        ),
        mc.table(["Key", "Value"], rows),
        mc.p("The value of ", mc.code("Version Notes"), ", rendered, is:"),
        mb_html.blockquote(_version_notes(headers["Version Notes"])),
        mc.p(
            f"After the header, each of the {mc.num(len(s.verses))} rows is a verse, with two"
            " fields: the verse's reference, such as ",
            mc.code(first.ref),
            ", and the verse's text, in HTML.",
        ),
        mc.p(
            "The folder ",
            mc.code(f"{ms.FOLDER_NAMES}/"),
            " has a listing for each book's file, which names each code point of each"
            " verse's text. The page ",
            mc.title_link(mc.LISTINGS_TITLE, _LISTINGS_HREF),
            " describes the listings, and gives the name and count of each of the"
            f" {len(s.code_points_csv)} code points that the files have.",
        ),
        *_numbering(s),
    ]


def _version_notes(html: str) -> list:
    """The header's Version Notes, re-emitted with closed dispatch on its three elements."""

    class Notes(html_parser.HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.stack = [("root", None, [])]

        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            if tag == "br" and not attrs:
                self.stack[-1][2].append(mb_html.line_break())
            elif tag == "i" and not attrs:
                self.stack.append(("i", None, []))
            elif tag == "a" and set(attrs) == {"href"}:
                self.stack.append(("a", attrs["href"], []))
            else:
                raise ValueError(f"Version Notes: unrecognized <{tag} {attrs}>")

        def handle_endtag(self, tag):
            name, href, kids = self.stack.pop()
            if name != tag:
                raise ValueError(f"Version Notes: </{tag}> closes <{name}>")
            el = mb_html.italic(kids) if tag == "i" else mb_html.anchor_h(kids, href)
            self.stack[-1][2].append(el)

        def handle_data(self, data):
            self.stack[-1][2].append(data)

    parser = Notes()
    parser.feed(html)
    parser.close()
    if len(parser.stack) != 1:
        raise ValueError("Version Notes: an unclosed element")
    return parser.stack[0][2]


def _numbering(s):
    return [
        author.heading_level_3("Verse numbering"),
        mc.p(
            "The verses are numbered as Sefaria numbers them. The page ",
            mb_html.anchor_h(
                "Versification Differences: MAM, BHS, and Sefaria", _VERSIFICATION
            ),
            " lists where that numbering differs from $MAM's and $BHS's.",
        ),
        mc.p(
            f"Sefaria's numbering has {mc.refs(s.em_dash_csv)}, for which $MAM has no text."
            " Each of these rows has only an ",
            mc.uname(ms.EM_DASH),
            " (",
            ms.EM_DASH,
            "), since an empty field would let the text of another version show at that"
            " verse on Sefaria. The files have no other ",
            mc.uname(ms.EM_DASH),
            ".",
        ),
    ]


def _markup(s):
    c = s.element_counts
    described = {
        ("span", "mam-spi-samekh"): ["a $samekh break, ", mc.code("{ס}")],
        ("span", "mam-spi-pe"): ["a $pe break, ", mc.code("{פ}")],
        ("span", "mam-spi-invnun"): ["an inverted $nun, ", mc.uname(hpu.NUN_HAF)],
        ("span", "mam-implicit-maqaf"): [
            "a gray $maqaf (see ",
            mb_html.anchor_h("Gray maqaf", _GRAY_MAQAF),
            ")",
        ],
        ("span", "mam-kq"): ["a $ketiv and its $qere"],
        ("span", "mam-kq-k"): ["a $ketiv, in parentheses"],
        ("span", "mam-kq-q"): ["a $qere, in square brackets"],
        ("span", "mam-kq-trivial"): ["a trivial $ketiv_qere pair, as one pointed atom"],
        ("span", "k-velo-q-maq"): ["a $maqaf after a $ketiv_velo_qere"],
        ("b", None): ["the ", mc.uname(hpu.PASOLEG), " of a $legarmeh"],
        ("small", None): [
            "the ",
            mc.uname(hpu.PASOLEG),
            f" of a $paseq ({mc.num(c['small paseq'])}), or a small letter"
            f" ({mc.num(c['small letter'])})",
        ],
        ("big", None): ["a large letter"],
        ("sup", None): ["a hung letter"],
        ("br", None): ["nothing: it follows each $pe break"],
    }
    if set(described) != set(ms.ELEMENT_ORDER):
        raise ValueError(
            "an element of the files that the markup table does not describe"
        )
    kinds = dict(
        zip(ms.ELEMENT_ORDER, (ms._ELEMENT_KINDS[k] for k in ms.ELEMENT_ORDER))
    )
    rows = [
        mc.tr(
            [
                mb_html.table_datum(mc.code(tag)),
                mb_html.table_datum(mc.code(cls) if cls else ""),
                mc.td_num(c[kinds[(tag, cls)]]),
                mc.td(described[(tag, cls)]),
            ]
        )
        for tag, cls in ms.ELEMENT_ORDER
    ]
    return [
        author.heading_level_2("Markup", {"id": "markup"}),
        mc.p(
            "The verse text of ",
            mc.code(f"{ms.FOLDER_CSV}/"),
            f" is HTML with {len({tag for tag, _ in ms.ELEMENT_ORDER})} elements, of which"
            " only ",
            mc.code("span"),
            " has an attribute, its class. These are all the elements and classes that the"
            " files have:",
        ),
        mc.table(["Element", "Class", "Count", "What it holds"], rows),
        *_legarmeh_and_paseq(s),
        *_spaces(s),
        *_breaks(s),
        *_letter_sizes(s),
        *_ketiv_qere(s),
    ]


def _legarmeh_and_paseq(s):
    rows = [
        mc.tr(
            [
                mc.td_he(mc.lift(_EX_LEGARMEH[0], _EX_LEGARMEH[1], s, whole=False)),
                mc.td_ref(_EX_LEGARMEH[0]),
                mc.td("$legarmeh"),
                mc.td(
                    [
                        mc.uname(sd.THSP),
                        ", then ",
                        mc.uname(hpu.PASOLEG),
                        " in ",
                        mc.code("<b>"),
                        ", then the space before the next atom",
                    ]
                ),
                mc.td_num(s.spacing["legarmeh"]),
            ]
        ),
        mc.tr(
            [
                mc.td_he(mc.lift(_EX_PASEQ[0], _EX_PASEQ[1], s, whole=False)),
                mc.td_ref(_EX_PASEQ[0]),
                mc.td("$paseq"),
                mc.td(
                    [
                        mc.uname(sd.THSP),
                        ", ",
                        mc.uname(hpu.PASOLEG),
                        " in ",
                        mc.code("<small>"),
                        ", ",
                        mc.uname(sd.THSP),
                        "; no other space comes before the next atom",
                    ]
                ),
                mc.td_num(s.spacing["paseq"]),
            ]
        ),
    ]
    return [
        author.heading_level_3(["$Legarmeh and $paseq"]),
        mc.p(
            "A $legarmeh and a $paseq are both the code point ",
            mc.uname(hpu.PASOLEG),
            ". The files tell them apart by markup and spacing:",
        ),
        mc.table(["Example", "Reference", "Mark", "Encoding", "Count"], rows),
        mc.p(
            "So the spacing keeps a $legarmeh with the atom before it, and puts a $paseq"
            " between two atoms.",
        ),
    ]


def _spaces(s):
    sp = s.spacing
    contexts = (
        ("before-break", "one", ["before a $samekh or $pe break"]),
        ("after-samekh", "eight", ["after a $samekh break"]),
        ("after-invnun", "one", ["after an inverted $nun"]),
        ("before-invnun", "one", ["before an inverted $nun"]),
        ("song-layout", "eight", ["a space of song spacing"]),
    )
    rows = [
        mc.tr([mc.td(where), mc.td(run), mc.td_num(sp[f"nbsp {key}"])])
        for key, run, where in contexts
    ]
    chapters = [
        (key[len("song-layout ") :], count)
        for key, count in sp.items()
        if key.startswith("song-layout ")
    ]
    order = {book: index for index, book in enumerate(ms.BOOKS)}

    def chapter_key(item):
        book, chapter = item[0].rsplit(" ", 1)
        return order[book], int(chapter)

    chapters.sort(key=chapter_key)
    total_runs = sum(sp[f"nbsp {key}"] for key, _run, _where in contexts)
    if total_runs != sum(len(re.findall(f"{sd.NBSP}+", v.text)) for v in s.verses):
        raise ValueError("a run of NO-BREAK SPACE that the table of spaces leaves out")
    return [
        author.heading_level_3("Spaces"),
        mc.p(
            "The files write ",
            mc.uname(sd.NBSP),
            " and ",
            mc.uname(sd.THSP),
            " as the character references ",
            mc.code("&nbsp;"),
            f" ({mc.num(s.entities['nbsp'])} times) and ",
            mc.code("&thinsp;"),
            f" ({mc.num(s.entities['thinsp'])} times), and have no other character"
            " reference. Each ",
            mc.uname(sd.THSP),
            " is beside the ",
            mc.uname(hpu.PASOLEG),
            " of a $legarmeh or a $paseq, as above. A ",
            mc.uname(sd.NBSP),
            " comes alone or in a run of eight:",
        ),
        mc.table(["Where", "Run", "Count"], rows),
        mc.p(
            "Song spacing, $MAM-simple's ",
            mc.code("shirah-space"),
            ", is in these chapters, with these numbers of spaces:",
        ),
        author.unordered_list(
            [
                f"{mc.short_ref(chapter)} ({mc.num(count)})"
                for chapter, count in chapters
            ]
        ),
    ]


def _breaks(s):
    c = s.element_counts
    invnun_refs = [v.ref for v in s.verses for el in v.elements if el.kind == "invnun"]
    return [
        author.heading_level_3(["Breaks and inverted $nun"]),
        mc.p(
            f"Each of the {mc.num(c['samekh'])} $samekh breaks is ",
            mc.code("{ס}"),
            " in a span of class ",
            mc.code("mam-spi-samekh"),
            ", with a ",
            mc.uname(sd.NBSP),
            f" before it and eight after it, and each of the {mc.num(c['pe'])} $pe breaks"
            " is ",
            mc.code("{פ}"),
            " in a span of class ",
            mc.code("mam-spi-pe"),
            ", with a ",
            mc.uname(sd.NBSP),
            " before it and a ",
            mc.code("<br>"),
            f" after it. Most end a verse, but {mc.num(c['samekh inside a verse'])} $samekh"
            f" and {mc.num(c['pe inside a verse'])} $pe breaks are inside one.",
        ),
        mc.p(
            f"Each of the {mc.num(c['invnun'])} inverted $nun marks is ",
            mc.unpointed(hpu.NUN_HAF),
            " (",
            mc.uname(hpu.NUN_HAF),
            ") in a span of class ",
            mc.code("mam-spi-invnun"),
            f", at {mc.refs(invnun_refs)}.",
        ),
    ]


def _letter_sizes(s):
    c = s.element_counts
    verse, kq = _kq_element(*_EX_SMALL_IN_KETIV, s)
    rows = [
        mc.tr([mc.td_he(mc.lift(ref, parts, s)), mc.td_ref(ref), mc.td(what)])
        for ref, parts, what in _EX_LETTER_SIZES
    ]
    rows.append(
        mc.tr(
            [
                mc.td_he(mc.lift_element(verse, kq)),
                mc.td_ref(verse.ref),
                mc.td("a small letter in a $ketiv"),
            ]
        )
    )
    hung_refs = [v.ref for v in s.verses for el in v.elements if el.kind == "hung"]
    return [
        author.heading_level_3("Small, large and hung letters"),
        mc.p(
            "A small letter is in ",
            mc.code("<small>"),
            f" ({mc.num(c['small letter'])} times), a large letter in ",
            mc.code("<big>"),
            f" ({mc.num(c['large'])} times) and a hung letter in ",
            mc.code("<sup>"),
            f" ({mc.num(c['hung'])} times, at {mc.refs(hung_refs)}). Each of these elements"
            " holds one letter and its marks:",
        ),
        mc.table(["Example", "Reference", "What it has"], rows),
    ]


def _ketiv_qere(s):
    shapes = s.kq_shapes
    if set(shapes) != set(_EX_KQ):
        raise ValueError(f"ketiv/qere shapes {sorted(set(shapes) ^ set(_EX_KQ))}")
    rows = []
    for shape in sorted(_EX_KQ, key=lambda k: (-shapes[k], k)):
        order, separator, words_k, words_q = shape
        verse, el = _kq_element(*_EX_KQ[shape], s)
        rows.append(
            mc.tr(
                [
                    mc.td_he(mc.lift_element(verse, el)),
                    mc.td_ref(verse.ref),
                    mc.td("q first" if order == "qere first" else ""),
                    mc.td(
                        "a space" if separator == "space" else ["a ", mc.uname(hpu.MAQ)]
                    ),
                    mc.td(f"{words_k}, {words_q}"),
                    mc.td_num(shapes[shape]),
                ]
            )
        )
    n_pairs = sum(shapes.values())
    qere_first = sum(n for k, n in shapes.items() if k[0] == "qere first")
    maqaf_separated = sum(n for k, n in shapes.items() if k[1] == "maqaf")
    velo = s.velo
    kvq_ref, kvq_letters = _EX_KETIV_VELO_QERE
    kvq_verse, kvq = _velo_element(kvq_ref, "ketiv", kvq_letters, s)
    qvk_ref, qvk_letters = _EX_QERE_VELO_KETIV
    qvk_verse, qvk = _velo_element(qvk_ref, "qere", qvk_letters, s)
    maq_refs = velo["k-velo-q-maq"]
    maq_verse = s.verse(maq_refs[0])
    maq_el = next(el for el in maq_verse.elements if el.kind == "k-velo-q-maq")
    trivial = mc.lift(_EX_TRIVIAL[0], _EX_TRIVIAL[1], s)
    velo_rows = [
        mc.tr(
            [
                mc.td_he(mc.lift_element(kvq_verse, kvq)),
                mc.td_ref(kvq_verse.ref),
                mc.td("a $ketiv_velo_qere"),
                mc.td_num(len(velo["ketiv"])),
            ]
        ),
        mc.tr(
            [
                mc.td_he(mc.lift_element(qvk_verse, qvk)),
                mc.td_ref(qvk_verse.ref),
                mc.td("a $qere_velo_ketiv"),
                mc.td_num(len(velo["qere"])),
            ]
        ),
        mc.tr(
            [
                mc.td_he(mc.lift_element(maq_verse, maq_el)),
                mc.td_ref(maq_verse.ref),
                mc.td("a $maqaf after a $ketiv_velo_qere"),
                mc.td_num(len(maq_refs)),
            ]
        ),
        mc.tr(
            [
                mc.td_he(trivial),
                mc.td_ref(_EX_TRIVIAL[0]),
                mc.td("a trivial pair"),
                mc.td_num(s.element_counts["trivial"]),
            ]
        ),
    ]
    q_first_header = mb_html.span(
        "q first?", {"title": "whether the qere comes before the ketiv"}
    )
    words_header = mb_html.span(
        "Words", {"title": "the number of words of the ketiv, then of the qere"}
    )
    return [
        author.heading_level_3(["$Ketiv and $qere"]),
        mc.p(
            f"Each of the {mc.num(n_pairs)} pairs of a $ketiv and its $qere is a span of"
            " class ",
            mc.code("mam-kq"),
            ", which holds the $ketiv, unpointed and in parentheses, in a span of class ",
            mc.code("mam-kq-k"),
            ", and the $qere, pointed and in square brackets, in a span of class ",
            mc.code("mam-kq-q"),
            ", with a separator between them: a space or, in ",
            mc.num(maqaf_separated),
            " pairs, a ",
            mc.uname(hpu.MAQ),
            ". The files keep the order that $MAM's pages on Hebrew Wikisource have, which"
            f" puts the $qere first in {mc.num(qere_first)} pairs,"
            f" {mc.num(s.kq_qere_first_after_maqaf)} of them right after a $maqaf. By"
            " order, separator, and the words of each part, the pairs are of these shapes:",
        ),
        mc.table(
            [
                "Example",
                "Reference",
                q_first_header,
                "Separator",
                words_header,
                "Count",
            ],
            rows,
        ),
        mc.p(
            "A $ketiv_velo_qere, a $ketiv that is written but not read, is a span of class ",
            mc.code("mam-kq-k"),
            " with no pair around it, at ",
            mc.refs([ref for ref, _ in velo["ketiv"]]),
            ". A $qere_velo_ketiv, a $qere that is read but not written, is likewise a span"
            " of class ",
            mc.code("mam-kq-q"),
            ", at ",
            mc.refs([ref for ref, _ in velo["qere"]]),
            ". A trivial pair, which ",
            mb_html.anchor_h("the guide to MAM-simple's JSON", _MAM_SIMPLE_GUIDE),
            " describes as a $ketiv_qere \N{LEFT DOUBLE QUOTATION MARK}whose two forms differ"
            " in a way that needs no separate display\N{RIGHT DOUBLE QUOTATION MARK}, is one"
            " pointed atom in a span of class ",
            mc.code("mam-kq-trivial"),
            ". An example of each, with its count:",
        ),
        mc.table(["Example", "Reference", "What it is", "Count"], velo_rows),
    ]


def _characters(s):
    return [
        author.heading_level_2("Characters", {"id": "characters"}),
        *_context_marks(s),
        *_own_code_points(s),
        *_geresh_telisha(s),
        *_zarqa(s),
        *_meteg_after_silluq(s),
        *_mark_order(s),
    ]


def _context_marks(s):
    by = s.by_system
    rows_spec = (
        (ha.ZSH_OR_TSIT, "prose", ["the $zarqa's stress helper"]),
        (ha.ZSH_OR_TSIT, "poetic", ["$tsinnorit"]),
        (ha.Z_OR_TSOR, "prose", ["$zarqa"]),
        (ha.Z_OR_TSOR, "poetic", ["$tsinnor"]),
        (hpu.PASOLEG, "b", ["$legarmeh"]),
        (hpu.PASOLEG, "small", ["$paseq"]),
    )
    rows = []
    for char, where, mark in rows_spec:
        if where in ("prose", "poetic"):
            count = by[(char, where)]
            where_cell = f"{where} verses"
        else:
            count = s.spacing["legarmeh" if where == "b" else "paseq"]
            where_cell = ["in ", mc.code(f"<{where}>")]
        if not count:
            raise ValueError(f"{unicode_data.name(char)} has no {where} row to show")
        rows.append(
            mc.tr(
                [
                    mb_html.table_datum(mc.uname(char)),
                    mc.td(where_cell),
                    mc.td_num(count),
                    mc.td(mark),
                ]
            )
        )
    return [
        author.heading_level_3("Code points that stand for more than one mark"),
        mc.p(
            "Some code points stand for different marks in different places: by the system"
            " of accents of the verse, prose or poetic, or, for ",
            mc.uname(hpu.PASOLEG),
            ", by its markup. As $MAM-for-Sefaria uses them:",
        ),
        mc.table(["Code point", "Where", "Count", "Mark"], rows),
    ]


def _own_code_points(s):
    meanings = {
        _QAMATS_QATAN: ["$qq"],
        _HOLAM_HASER_FOR_VAV: ["$xolam_xaser on a $vav that is a consonant"],
        ha.ATN_H: ["$ah, as opposed to ", mc.uname(ha.YBY)],
    }
    rows = []
    for char in ms.OWN_CODE_POINT_MARKS:
        ref, parts = _EX_OWN_CODE_POINT[char]
        form = mc.lift(ref, parts, s)
        rows.append(
            mc.tr(
                [
                    mc.td_he(form),
                    mc.td_ref(ref),
                    mb_html.table_datum(mc.uname(char)),
                    mc.td(meanings[char]),
                    mc.td_num(s.code_points_csv[char]),
                    mc.td_num(s.atoms[f"with {unicode_data.name(char)}"]),
                ]
            )
        )
    return [
        author.heading_level_3("Marks with code points of their own"),
        mc.p(
            "$MAM-for-Sefaria has each of these marks as a code point of its own. The counts"
            " are of the marks and of the atoms that have them:"
        ),
        mc.table(
            ["Example", "Reference", "Code point", "Mark", "Marks", "Atoms"], rows
        ),
    ]


def _geresh_telisha(s):
    rows = []
    for hit in s.geresh_telisha:
        verse = s.verse(hit["ref"])
        names = []
        for cluster in hit["clusters"]:
            if names:
                names.append(mb_html.line_break())
            names.extend(mc.name_list(cluster))
        start = verse.text.index(hit["atom"])
        if verse.text.count(hit["atom"]) != 1:
            raise ValueError(f"{hit['ref']}: {hit['atom']!r} is there more than once")
        span = mc.chanted_words(verse.text, start, start + len(hit["atom"]))
        rows.append(
            mc.tr(
                [
                    mc.td_he(mc.snippet(verse, *span)),
                    mc.td_ref(hit["ref"]),
                    mb_html.table_datum(names),
                ]
            )
        )
    two_letter = sum(1 for hit in s.geresh_telisha if len(hit["clusters"]) == 2)
    return [
        author.heading_level_3(
            ["A letter with $geresh or $gershayim and $telisha_gedolah"]
        ),
        mc.p(
            f"In {len(s.geresh_telisha)} atoms, a letter has a ",
            mc.uname(ha.GER),
            " or a ",
            mc.uname(ha.GER_2),
            " and then a ",
            mc.uname(ha.TEL_G),
            f"; in {two_letter} of them two letters do. The letters' code points, in"
            " order:",
        ),
        mc.table(["Example", "Reference", "Code points"], rows),
    ]


def _zarqa(s):
    z = s.zarqa
    rows = []
    clusters_of = {}
    for ref, parts in (_EX_ZARQA_HELPER, _EX_ZARQA_LAMED):
        atom = mc.lift_atom(ref, parts, s)
        verse = s.verse(ref)
        start, end = mc.find(verse.text, parts, ref)
        clusters_of[ref] = ms.CLUSTER_RE.findall(atom)
        names = []
        for cluster in clusters_of[ref]:
            if names:
                names.append(mb_html.line_break())
            names.extend(mc.name_list(cluster))
        rows.append(
            mc.tr(
                [
                    mc.td_he(
                        mc.snippet(verse, *mc.chanted_words(verse.text, start, end))
                    ),
                    mc.td_ref(ref),
                    mb_html.table_datum(names),
                ]
            )
        )
    helper = clusters_of[_EX_ZARQA_HELPER[0]]
    if (
        not any(ha.ZSH_OR_TSIT in c for c in helper[:-1])
        or ha.Z_OR_TSOR not in helper[-1]
    ):
        raise ValueError(f"{_EX_ZARQA_HELPER[0]}: not a stress helper before a ZINOR")
    lamed = clusters_of[_EX_ZARQA_LAMED[0]][-1]
    if lamed[0] != _LAMED or ha.Z_OR_TSOR not in lamed:
        raise ValueError(f"{_EX_ZARQA_LAMED[0]}: not a ZINOR on a lamed")
    return [
        author.heading_level_3(["The $zarqa and its stress helper"]),
        mc.p(
            f"Each of the {mc.num(z['z-or-tsor prose'] + z['z-or-tsor poetic'])} ",
            mc.uname(ha.Z_OR_TSOR),
            " marks is on the last letter of its atom: the $zarqa in prose verses and the"
            " $tsinnor in poetic verses. Of them,"
            f" {mc.num(z['z-or-tsor prose lamed'] + z['z-or-tsor poetic lamed'])} are on a"
            f" $lamed, as at {mc.short_ref(_EX_ZARQA_LAMED[0])} below. In prose verses,"
            f" each of the {mc.num(z['zsh-or-tsit prose'])} ",
            mc.uname(ha.ZSH_OR_TSIT),
            " marks is the $zarqa's stress helper, on an earlier letter of the atom than"
            " its ",
            mc.uname(ha.Z_OR_TSOR),
            f", as at {mc.short_ref(_EX_ZARQA_HELPER[0])}:",
        ),
        mc.table(["Example", "Reference", "Code points"], rows),
    ]


def _meteg_after_silluq(s):
    cases = s.silluq_cases
    heads = [mb_html.table_header("Version", {"scope": "col"})]
    sefaria_cells = []
    other_cells = []
    for case in cases:
        heads.append(
            mb_html.table_header(
                mc.short_ref(case["ref"]),
                {"scope": "col", "data-osis-id": case["osis_id"]},
            )
        )
        # The attention color runs from the letter whose meteg the Sefaria form lacks.
        full_clusters = ms.CLUSTER_RE.findall(case["full"])
        dropped = [
            i
            for i, cluster in enumerate(full_clusters)
            if i > case["silluq_index"] and hpo.MTGOSLQ in cluster
        ]
        for atom, cells in (
            (case["sefaria"], sefaria_cells),
            (case["full"], other_cells),
        ):
            cut = list(ms.CLUSTER_RE.finditer(atom))[dropped[0]].start()
            contents = [atom[:cut], mb_html.span_c(atom[cut:], "attention")]
            cells.append(mb_html.table_datum(contents, {"lang": "hbo", "dir": "rtl"}))
    table = mb_html.table(
        [
            mb_html.table_row(heads),
            mb_html.table_row(
                [mb_html.table_header("Sefaria", {"scope": "row"}), *sefaria_cells],
                {"data-version": "sefaria"},
            ),
            mb_html.table_row(
                [
                    mb_html.table_header(
                        author.dollar_sub("other versions of $MAM"), {"scope": "row"}
                    ),
                    *other_cells,
                ],
                {"data-version": "other-mam"},
            ),
        ],
        {"id": "meteg-after-silluq-cases", "class": "data"},
    )
    return [
        author.heading_level_3(
            ["A $meteg after the ", _SILLUQ], {"id": "meteg-after-silluq"}
        ),
        mc.p(
            f"In {len(cases)} atoms, $MAM's source identifies a ",
            _SILLUQ,
            " that has a $meteg after it, on a later letter of the atom. $MAM-for-Sefaria"
            " has the ",
            _SILLUQ,
            " and every other mark of each atom, but not that $meteg, which other versions"
            " of $MAM, $MAM-simple among them, have:",
        ),
        mb_html.div([table], {"class": "table-wrap"}),
    ]


def _mark_order(s):
    a = s.atoms
    return [
        author.heading_level_3("Mark order"),
        mc.p(
            "The marks of each letter are in $MAM's order, which is not Unicode's: a ",
            mc.uname(hpo.SHIND),
            " or ",
            mc.uname(hpo.SIND),
            " comes first, then a ",
            mc.uname("\N{HEBREW POINT DAGESH OR MAPIQ}"),
            ", then a ",
            mc.uname(hpo.RAFE),
            ", and then the other marks, in the order $MAM gives them. A ",
            mb_html.anchor_h("note in MAM-basics", mc.MARK_ORDER_URL),
            " says more. Unicode normalization puts the marks in Unicode's order, and would"
            f" change the order of the marks of {mc.num(a['changed by NFC'])} of the"
            f" {mc.num(a['atoms'])} atoms of ",
            mc.code(f"{ms.FOLDER_CSV}/"),
            ".",
        ),
    ]


def _left_out(_s):
    return [
        author.heading_level_2("What the files leave out", {"id": "left-out"}),
        mc.p(
            "The handlers of ",
            mb_html.anchor_h(
                mc.code("py/mb_sefaria/mam4sef_handlers.py"), mc.HANDLERS_URL
            ),
            " write nothing for these three things that $MAM-simple has:",
        ),
        author.ordered_list(
            [
                [
                    "Its ",
                    mb_html.anchor_h(
                        "notes on scroll differences",
                        f"{_MAM_SIMPLE_GUIDE}#scroll-differences-scrdfftar",
                    ),
                    " (",
                    mc.code("sdt-note"),
                    "). The files keep the text that each note is about, and have no"
                    " notes. $MAM's documentation notes, which $MAM-simple does not have"
                    " either, are in $MAM-with-doc, to which the files' ",
                    mc.code("Version Notes"),
                    " link.",
                ],
                [
                    "The ",
                    mb_html.anchor_h(
                        "verse that four books repeat",
                        f"{_MAM_SIMPLE_GUIDE}#repeated-endings-good-ending",
                    ),
                    " after their last (",
                    mc.code("good-ending"),
                    ").",
                ],
                [
                    "The ",
                    mb_html.anchor_h(
                        "two strands",
                        f"{_MAM_SIMPLE_GUIDE}#dual-cantillation-cant-all-three",
                    ),
                    " of each verse that has two cantillations (",
                    mc.code("cant-alef"),
                    " and ",
                    mc.code("cant-bet"),
                    "). The files keep the text that represents both strands at once (",
                    mc.code("cant-combined"),
                    ").",
                ],
            ]
        ),
    ]


def _cgj_rows_jerusalem(s):
    rows = []
    for kind in ("jerusalem-hiriq", "jerusalem-sheva"):
        by_type = {}
        for hit in s.cgj[kind]:
            by_type.setdefault((hit["before"][0], hit["after"]), []).append(hit)
        for key in sorted(by_type, key=lambda k: (k[1] != _HIRIQ, k[0] != _PATAH)):
            hits = by_type[key]
            ref, parts = _EX_JERUSALEM[key]
            verse = s.verse(ref)
            start, end = mc.find(verse.text, parts, ref)
            atom = verse.text[start:end]
            example = [h for h in hits if h["ref"] == ref and h["atom"] == atom]
            if len(example) != 1:
                raise ValueError(f"{ref}: the example is not one of its kind's atoms")
            index = len(ms.letters_of(atom)) - (2 if key[1] == _HIRIQ else 3)
            word_start, word_end = mc.chanted_words(verse.text, start, end)
            form = [
                verse.text[word_start:start],
                *mc.highlight(atom, index),
                verse.text[end:word_end],
            ]
            bare = sum(1 for h in hits if len(h["before"]) == 1)
            vowel_name = ms.short_name(key[0])
            count = [mc.num(len(hits))]
            if bare:
                count.extend(
                    [f" ({mc.num(bare)} with no accent or ", mc.uname(hpo.MTGOSLQ), ")"]
                )
            rows.append(
                mc.tr(
                    [
                        mc.td_he([part for part in form if part != ""]),
                        mc.td_ref(ref),
                        mb_html.table_datum(mc.name_list(example[0]["cluster"])),
                        mb_html.table_datum(count, {"class": "num"}),
                    ]
                )
            )
            if vowel_name not in ("PATAH", "QAMATS"):
                raise ValueError(f"{ref}: a Jerusalem lamed with {vowel_name}")
    return rows


def _cgj_rows_strands(s, kind):
    """One row for each atom of this kind, with the references of every verse it is in."""
    by_atom = {}
    for hit in s.cgj[kind]:
        by_atom.setdefault(hit["atom"], []).append(hit)
    rows = []
    for atom, hits in by_atom.items():
        verse = s.verse(hits[0]["ref"])
        form = mc.highlight_in(verse.text, atom, mc.cgj_index(atom), verse.ref)
        rows.append(
            mc.tr(
                [
                    mc.td_he(form),
                    mc.td_refs([h["ref"] for h in hits]),
                    mb_html.table_datum(mc.name_list(hits[0]["cluster"])),
                ]
            )
        )
    return rows


def _robust_unicode(s):
    cgj = s.cgj
    total = sum(len(hits) for hits in cgj.values())
    if total != s.code_points_csv[sd.CGJ]:
        raise ValueError("a CGJ of csv/ that no kind accounts for")
    two_vowel_kinds = ("jerusalem-hiriq", "jerusalem-sheva", "qupo")
    two_vowels = sum(len(cgj[k]) for k in two_vowel_kinds)
    if two_vowels != s.atoms["letters with two vowels"]:
        raise ValueError("a letter with two vowels that no CGJ kind accounts for")
    headers_j = [
        "Example",
        "Reference",
        ["The ", "$lamed", "'s code points"],
        "Count",
    ]
    headers_s = [
        "Example",
        "References",
        "The letter's code points",
    ]
    n_j_hiriq, n_j_sheva = len(cgj["jerusalem-hiriq"]), len(cgj["jerusalem-sheva"])
    n_j_bare = sum(
        1
        for kind in ("jerusalem-hiriq", "jerusalem-sheva")
        for hit in cgj[kind]
        if len(hit["before"]) == 1
    )
    if not 0 < n_j_bare < n_j_hiriq + n_j_sheva:
        raise ValueError(
            "the Jerusalem paragraph's exception has no atom, or every atom"
        )
    return [
        author.heading_level_2("Robust Unicode", {"id": "robust-unicode"}),
        mc.p(
            "Unicode normalization sorts the marks of each letter by their combining classes."
            " A ",
            mc.uname(sd.CGJ, full=True),
            " (",
            mc.cgj(),
            ") has combining class 0, so normalization moves no mark across one."
            f" $MAM-for-Sefaria has {mc.num(total)} of them, each on a letter whose marks"
            " normalization would otherwise put in another order: it keeps the vowel or ",
            mc.uname(hpo.MTGOSLQ),
            " after it in place after the marks before it. Every letter of the files that has"
            " two vowels has a ",
            mc.cgj(),
            " between them. The tables give, for each kind, the code points of the letter in"
            " order.",
        ),
        author.heading_level_3("Jerusalem"),
        mc.p(
            f"{mc.num(n_j_hiriq + n_j_sheva)} are in atoms spelled ",
            mc.unpointed("ירושלם"),
            f" ({mc.num(n_j_hiriq)}) or ",
            mc.unpointed("ירושלמה"),
            f" ({mc.num(n_j_sheva)}), with or without a prefix, on the $lamed. It has its own"
            " vowel, ",
            mc.uname(_PATAH),
            " or ",
            mc.uname(_QAMATS),
            f", then, in all but {mc.num(n_j_bare)} of them, an accent or ",
            mc.uname(hpo.MTGOSLQ),
            ", and after the ",
            mc.cgj(),
            " an orphaned ",
            mc.uname(_HIRIQ),
            " or ",
            mc.uname(_SHEVA),
            ", the vowel of the $yod that the spelling lacks:",
        ),
        mc.table(headers_j, _cgj_rows_jerusalem(s)),
        author.heading_level_3("Two strands on one letter"),
        mc.p(
            f"The other {mc.num(len(cgj['qupo']) + len(cgj['accent-meteg']))} are in verses"
            " with two cantillations, on a letter whose text represents both strands: the"
            " marks before the ",
            mc.cgj(),
            " are one strand's, and the marks after it are the other's. In"
            f" {mc.num(len(cgj['qupo']))} atoms, one strand has a ",
            mc.uname(_QAMATS),
            " and an accent or ",
            mc.uname(hpo.MTGOSLQ),
            " below the letter, and the other a ",
            mc.uname(_PATAH),
            " and an accent above it:",
        ),
        mc.table(headers_s, _cgj_rows_strands(s, "qupo")),
        mc.p(
            f"In {mc.num(len(cgj['accent-meteg']))} atoms, one strand has an accent below"
            " the letter, and the other a ",
            mc.uname(hpo.MTGOSLQ),
            ":",
        ),
        mc.table(headers_s, _cgj_rows_strands(s, "accent-meteg")),
    ]


def _pin_claims(s) -> None:
    """Fail the build if the data stops supporting a claim the prose states in words."""
    by = s.by_system
    # The table of marks by system lists PASEQ by markup; each PASEQ is one of the two.
    assert s.code_points_csv[hpu.PASOLEG] == s.spacing["legarmeh"] + s.spacing["paseq"]
    # "Sefaria's numbering has ..., for which MAM has no text": some rows have only that.
    assert s.em_dash_csv
    # "Each of the ZINOR marks is on the last letter of its atom": the survey raises otherwise,
    # and here every ZINOR is one of the counted ones.
    assert (
        s.code_points_csv[ha.Z_OR_TSOR]
        == s.zarqa["z-or-tsor prose"] + s.zarqa["z-or-tsor poetic"]
    )
    assert by[(ha.ZSH_OR_TSIT, "prose")] == s.zarqa["zsh-or-tsit prose"]
    # "the qere first in N pairs, M of them right after a maqaf": a part, not the whole.
    qere_first = sum(n for k, n in s.kq_shapes.items() if k[0] == "qere first")
    assert 0 < s.kq_qere_first_after_maqaf < qere_first
    # "The handlers ... write nothing for these three things."
    left_out = ms.check_handlers()
    assert set(left_out) == {"sdt-note", "good-ending", "cant-alef", "cant-bet"}
    # "ATNAH HAFUKH, as opposed to YERAH BEN YOMO": the files have both code points.
    assert s.code_points_csv[ha.ATN_H] and s.code_points_csv[ha.YBY]


def gen_html_file():
    """Write the page and return its path."""
    s = ms.survey()
    _pin_claims(s)
    cbody = [
        *mc.page_head(mc.INDEX_TITLE),
        *_intro(),
        *_files(s),
        *_markup(s),
        *_characters(s),
        *_left_out(s),
        *_robust_unicode(s),
    ]
    return mc.write_page(__file__, None, mc.INDEX_TITLE, cbody, s)
