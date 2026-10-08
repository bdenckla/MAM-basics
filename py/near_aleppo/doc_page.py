"""Assemble near-Aleppo documentation sections in their source order.

doc_pages.py assigns headings to the overview and reference pages. Prose comes
from this module and its section modules; measured figures come through
doc_html.Numbers from the build's population file or doc_figures.py. The overview
describes near-Aleppo's differences and links MAM-parsed-plus for shared roles.
"""

import json
import unicodedata

from near_aleppo import build_paths
from near_aleppo import consumer_notice
from near_aleppo import doc_changes
from near_aleppo import doc_choices
from near_aleppo import doc_registers
from near_aleppo import doc_policy_examples
from near_aleppo.doc_html import code
from near_aleppo.doc_html import english_book
from near_aleppo.doc_html import he_name
from near_aleppo.doc_html import he_display
from near_aleppo.doc_html import he_pointed
from near_aleppo.doc_html import isolated
from near_aleppo.doc_html import link
from near_aleppo.doc_html import table
from near_aleppo.doc_html import verse_refs
from near_aleppo.doc_html import NUMBER_CELL
from mb_misc import mb_html
from near_aleppo.phase2_templates import APPLIED_AND_FLAGGED
from near_aleppo.phase2_templates import FLAGGED_NOT_APPLIED
from near_aleppo.phase2_templates import MARKS_WITHOUT_LETTER
from near_aleppo.phase2_templates import POINTED_KETIV_FAMILIES
from near_aleppo.phase2_templates import POINTED_KETIV_PARAMETER
from near_aleppo.phase3_policies import _clauses
from near_aleppo.phase6_flags import _MAQAF_SILENCE
from near_aleppo.phase6_flags import _QERE_SILENCE
from near_aleppo.phase6_mam_targets import MAM_TARGET_PARAMETER
from py_misc import near_aleppo_params as nap
from near_aleppo.phase6_rename import RENAMED_NOTES

TITLE = "The near-Aleppo dataset"

MPPLUS_DOC = "../MAM-parsed/plus/html/mpplus.html"
SIGIL_DECODING = (
    "https://bdenckla.github.io/MAM-basics/MAM-with-doc/sigil-decoding.html"
)
ALEPPO_INDEX = (
    "https://github.com/bdenckla/MAM-basics/blob/main/aleppo/"
    "index-flat-annotated.json"
)
# The source and terms that aleppo/aleppo-wiki/LICENSE.txt gives for the index
# that ALEPPO_INDEX corrects and annotates.
STARK_INDEX = "https://learn.jdavidstark.com/aleppoindex"
CC_BY_4 = "https://creativecommons.org/licenses/by/4.0/"
EDITION_INDEX = "edition/index.html"

_NOTE = RENAMED_NOTES["נוסח"]
_NOTE_2 = RENAMED_NOTES["מ:הערה-2"]


def section_heading(section):
    identifier, title = section
    return mb_html.heading_level_2(title, {"id": identifier})


def subsection_heading(section):
    identifier, title = section
    return mb_html.heading_level_3(title, {"id": identifier})


WHAT = ("what-the-dataset-is", "What near-Aleppo is")
READING = ("reading-the-json", "How to read the JSON")
NOTICE = ("consumer-notice", "Notes for applications")
OWN_TEMPLATES = ("own-templates", "Templates specific to near-Aleppo")
GAV = ("gav-display", "GAV notation and display")
ADDED = ("added-parameters", "The parameters near-Aleppo adds")
CHARACTERS = ("characters", "A character MAM-parsed-plus has only in a note body")
SURVIVES = ("where-the-codex-survives", "Where the codex survives")

_SECTIONS = (
    (WHAT, ()),
    (READING, (OWN_TEMPLATES, GAV, ADDED, CHARACTERS, NOTICE)),
    (SURVIVES, ()),
    (doc_changes.SECTION, doc_changes.SUBSECTIONS),
    (doc_registers.KEPT, ()),
    (doc_registers.NOT_REPRESENTED, ()),
    (doc_registers.LIMITATIONS, ()),
    (doc_registers.PENDING, ()),
    (doc_registers.MANUAL_TASK, ()),
    (doc_choices.SECTION, ()),
)


def page(numbers):
    """The page's title and body contents."""
    body = [
        mb_html.heading_level_1(TITLE),
        mb_html.para(
            [
                "The ",
                link(
                    "near-Aleppo dataset",
                    "https://github.com/bdenckla/MAM-basics/tree/main/out/near-aleppo/",
                ),
                " is similar to MAM-parsed-plus (mpplus). "
                "This page describes what near-Aleppo changes relative "
                "to mpplus. For what is in common with mpplus, see ",
                link("the documentation for mpplus", MPPLUS_DOC),
                ".",
            ]
        ),
        mb_html.para("Contents:"),
        _contents(),
    ]
    body += _what(numbers)
    body += _reading(numbers)
    body += _survives(numbers)
    body += doc_changes.section(numbers)
    body += doc_registers.sections(numbers)
    body += doc_choices.section(numbers)
    return TITLE, body


def _contents():
    items = []
    for section, subsections in _SECTIONS:
        entry = [link(section[1], "#" + section[0])]
        if subsections:
            entry.append(
                mb_html.unordered_list(
                    [link(title, "#" + ident) for ident, title in subsections]
                )
            )
        items.append(entry)
    return mb_html.ordered_list(items)


def _what(numbers):
    verses = numbers.fig_value("verses")
    if numbers.fig_value("c_cells_changed") or numbers.fig_value("d_cells_changed"):
        raise AssertionError("near-Aleppo's C and D columns must remain MAM's")
    return [
        section_heading(WHAT),
        mb_html.para(
            "The mpplus dataset is a parsed form of the Wikitext sources "
            "for Miqra According to the Masorah (MAM). The Hebrew of near-Aleppo "
            "is nearer to the Aleppo Codex's body text than the Hebrew of mpplus."
        ),
        mb_html.para(
            "By “body text,” we mean the contents of Aleppo's main, "
            "large-letter columns. There are usually two or three such columns "
            "per page. We exclude Aleppo's small-letter content, such "
            "as its column-margin notes (Masorah qetannah) and its top- and "
            "bottom-margin notes (Masorah gedolah)."
        ),
        mb_html.para(
            "The one type of small-letter content we do include is the information "
            "in column-margin qere "
            "notes. We include that information and supply the qere letters "
            "with the pointing that we judge to be implied by the pointed "
            "ketiv words in the body text. Unlike mpplus, near-Aleppo "
            "provides pointed ketiv words rather than only their letters."
        ),
        mb_html.para(
            [
                "The near-Aleppo dataset differs from mpplus in more than just "
                "its Unicode strings. It also "
                "uses a slightly different set of templates to structure the "
                "string data. The ",
                link("JSON reference", "reading-json.html"),
                " describes those differences.",
            ]
        ),
        mb_html.para(
            [
                "Most changes to MAM that near-Aleppo makes are based on "
                "information found in MAM itself. Some of that information is in "
                "the general policies laid out in MAM's Introduction. When the "
                "Introduction describes a systematic, invertible difference "
                "between MAM and the Aleppo Codex, near-Aleppo applies the inverse "
                "to MAM's text. For example, MAM supplies stress helpers for all "
                "accents, whereas the Introduction describes Aleppo as generally "
                "lacking helpers for accents other than pashta. So, near-Aleppo "
                "inverts (in this case undoes) MAM's work by omitting those "
                "helpers except where MAM's notes justify keeping them. "
                "For example, at ",
                *verse_refs((("A1-Genesis", "2", "7"),)),
                ", we can see that near-Aleppo removes MAM's telishah qetannah "
                "stress helper:",
            ]
        ),
        *_stress_helper_example(),
        mb_html.para(
            [
                "Other changes that near-Aleppo makes to MAM are based on MAM's "
                "documentation notes. A MAM documentation note targets a particular "
                "word within a particular verse. When a note says that MAM diverges "
                "from Aleppo at a particular word, the note typically gives "
                "Aleppo's form, so in such cases near-Aleppo uses Aleppo's form "
                "of the word rather than MAM's form. For example, at ",
                *verse_refs((("C1-Isaiah", "27", "5"),)),
                ", MAM's note gives Aleppo's form without the dagesh on zayin, "
                "and near-Aleppo follows that form:",
            ]
        ),
        *_note_example(),
        mb_html.para(
            "The near-Aleppo dataset is not solely derived from mpplus and the "
            "Introduction to MAM; some external references were consulted as "
            "well. For instance, for tricky cases of ketiv pointing, we have "
            "consulted external references such as the Jerusalem Crown edition."
        ),
        mb_html.para(
            "Near-Aleppo aims to provide a continuous text that moves seamlessly "
            "between an Aleppo-diplomatic edition where the codex survives and "
            "an Aleppo-flavored edition where it is missing. In missing sections, "
            "preserved testimony and photographs taken before the loss remain "
            "evidence of the codex’s text. Where that evidence is lacking, we "
            "apply editorial policies reflecting our best guess of the Tiberian "
            "Masoretic consensus. We do not present these editorial guesses as "
            "a proposed reconstruction of the codex."
        ),
        mb_html.para(
            [
                "Near-Aleppo is ",
                numbers.fig("dataset_files"),
                " JSON files in this repository's ",
                link(
                    code("out/near-aleppo/plus/"),
                    "https://github.com/bdenckla/MAM-basics/tree/main/"
                    "out/near-aleppo/plus/",
                ),
                ", one for each of MAM-parsed-plus's book files, in its layout and "
                "its serialization. Of its ",
                numbers.fig("verses"),
                " verses, near-Aleppo's text differs from MAM-parsed-plus's at ",
                numbers.fig("e_cells_changed"),
                " (",
                numbers.percent(
                    numbers.fig_value("e_cells_changed"),
                    verses,
                    "doc_figures: e_cells_changed / verses",
                ),
                ").",
            ]
        ),
        mb_html.para(
            [
                "In addition to the JSON near-Aleppo dataset, we provide ",
                link("an example HTML edition", EDITION_INDEX),
                " to show one kind of human-readable edition that can be made "
                "from near-Aleppo.",
            ]
        ),
    ]


def _stress_helper_example():
    """Check the displayed Genesis 2:7 forms in direct Scripture strings of E."""
    forms = (
        (build_paths.mam_parsed_plus_dir(), "וַיִּ֩יצֶר֩"),
        (build_paths.dataset_dir(), "וַיִּיצֶר֩"),
    )
    for directory, form in forms:
        with (directory / "A1-Genesis.json").open(encoding="utf-8") as stream:
            book = json.load(stream)
        cell = book["book39s"][0]["chapters"]["2"]["7"][2]
        if not any(form in node.split() for node in cell if isinstance(node, str)):
            raise AssertionError(f"Genesis 2:7 example no longer in {directory}")
    return _example_table(tuple(form for _, form in forms), "\N{HEBREW LETTER YOD}")


def _note_example():
    """Read the Isaiah 27:5 targets and check the note's attributed Aleppo form."""
    ref = ("C1-Isaiah", "27", "5")
    params = []
    for directory, name, keys in (
        (build_paths.mam_parsed_plus_dir(), "נוסח", {"1", "2"}),
        (
            build_paths.dataset_dir(),
            _NOTE,
            {"1", "2", MAM_TARGET_PARAMETER, nap.MAM_NOTE},
        ),
    ):
        with (directory / "C1-Isaiah.json").open(encoding="utf-8") as stream:
            book = json.load(stream)
        if len(book["book39s"]) != 1:
            raise AssertionError(
                f"Isaiah example has an unexpected sub-book in {directory}"
            )
        note = book["book39s"][0]["chapters"]["27"]["5"][2][1]
        if note["tmpl_name"] != name or set(note["tmpl_params"]) != keys:
            raise AssertionError(
                f"Isaiah 27:5 example note changed shape in {directory}"
            )
        params.append(note["tmpl_params"])
    mam, data = params
    forms = (mam["1"], data["1"])
    if not all(isinstance(form, str) for form in forms):
        raise AssertionError("Isaiah 27:5 example targets must be strings")
    if mam["1"] != "בְּמָעוּזִּ֔י" or data[MAM_TARGET_PARAMETER] != mam["1"]:
        raise AssertionError("Isaiah 27:5 example must preserve the MAM target")
    if data["2"] != '=א (חסר דגש באות זי"ן)':
        raise AssertionError("Isaiah 27:5 example must contain the reviewed agreement")
    aleppo_clause = f'א={data["1"]} (חסר דגש באות זי"ן)'
    if aleppo_clause not in _clauses(mam["2"], ref):
        raise AssertionError(
            "Isaiah 27:5 note must attribute the displayed form to Aleppo"
        )
    zayin = "\N{HEBREW LETTER ZAYIN}"
    dotted_zayin = zayin + "\N{HEBREW POINT DAGESH OR MAPIQ}"
    if (
        mam["1"].count(dotted_zayin) != 1
        or mam["1"].replace(dotted_zayin, zayin, 1) != data["1"]
    ):
        raise AssertionError("Isaiah 27:5 example must differ only in zayin's dagesh")
    return _example_table(forms, zayin)


def _example_table(forms, letter):
    """Display two checked forms, highlighting the differing letter's cluster."""
    rows = tuple(
        mb_html.table_row(
            (
                mb_html.table_header(label, {"scope": "row"}),
                mb_html.table_datum(_example_display(form, letter), {"dir": "rtl"}),
            )
        )
        for label, form in zip(("mpplus", "Near-Aleppo"), forms)
    )
    return [mb_html.div(mb_html.table(rows), {"class": "table-wrap display-table"})]


def _example_display(form, letter):
    """Color the first given letter and all its marks without changing the text."""
    start = form.index(letter)
    end = start + 1
    while end < len(form) and unicodedata.category(form[end]).startswith("M"):
        end += 1
    return he_display(
        [
            form[:start],
            mb_html.span(form[start:end], {"class": "example-difference"}),
            form[end:],
        ]
    )


def _reading(numbers):
    notice = consumer_notice.NOTICE
    return [
        section_heading(READING),
        mb_html.para(
            [
                "Near-Aleppo largely shares MAM-parsed-plus's structure, so ",
                link("MAM-parsed-plus's documentation", MPPLUS_DOC),
                " is the reference for that shared structure and for the meanings "
                "of MAM's templates. This section describes "
                "near-Aleppo's template differences and added parameters.",
            ]
        ),
        mb_html.para(
            [
                "For guidance when writing code to use the data, see ",
                link("Notes for applications", "#consumer-notice"),
                ".",
            ]
        ),
        subsection_heading(OWN_TEMPLATES),
        *_own_templates(numbers),
        subsection_heading(GAV),
        *_gav_display(numbers),
        subsection_heading(ADDED),
        *_added_parameters(numbers),
        subsection_heading(CHARACTERS),
        *_characters(numbers),
        subsection_heading(NOTICE),
        mb_html.para(
            [
                "The notes below highlight common pitfalls when consuming the "
                "JSON data. For the full rules, see ",
                link("template definitions", "#own-templates"),
                ", ",
                link("GAV notation and display", "#gav-display"),
                ", and ",
                link("parameter roles", "#added-parameters"),
                ".",
            ]
        ),
        mb_html.para(isolated(notice["summary"])),
        mb_html.unordered_list([isolated(rule) for rule in notice["critical_rules"]]),
        mb_html.para(
            [
                "Every book file of near-Aleppo includes these notes in ",
                code("header.consumer_notice"),
                ", adapting MAM-parsed-plus's guidance to near-Aleppo. The ",
                code("documentation"),
                " field links this section at ",
                code(notice["documentation"]),
                ".",
            ]
        ),
    ]


def _own_templates(numbers):
    return [
        mb_html.para(
            [
                "Near-Aleppo uses three added templates, which MAM's text never "
                "has. Each name is specific to the near-Aleppo dataset, and none has "
                "the prefix ",
                he_name("מ:"),
                " that marks many of MAM's.",
            ]
        ),
        mb_html.para(
            [
                "Two are MAM's note templates under names specific to near-Aleppo. "
                "Where near-Aleppo changes a note's target, the JSON dataset stores "
                "the reviewed near-Aleppo clause in parameter 2 and MAM's target in an "
                "added parameter, ",
                he_name(MAM_TARGET_PARAMETER),
                ". The remaining original clauses are stored in ",
                he_name(nap.MAM_NOTE),
                " and describe that MAM target. Such a "
                "note is renamed, so that a consumer who knows only MAM's "
                "templates fails on it rather than misreading it: a ",
                he_name("נוסח"),
                " is named ",
                he_name(_NOTE),
                ", at ",
                numbers.snap("phase6_counts", "נוסח: notes given MAM's target"),
                " notes, and a ",
                he_name("מ:הערה-2"),
                " is named ",
                he_name(_NOTE_2),
                ", at ",
                numbers.snap("phase6_counts", "מ:הערה-2: notes given MAM's target"),
                ". Scroll-note parameter 3 and the evidence flags keep their "
                "existing roles. So every template of MAM's "
                "that near-Aleppo has keeps MAM's meaning.",
            ]
        ),
        mb_html.para(
            "The stored near-Aleppo clause is already recast "
            "as an agreement with that form, retaining its explanations and "
            "qualifications. Where a recast would require uncertain interpretation, "
            "parameter 2 is an empty array and the complete original note is "
            "stored in the MAM-note parameter. Consumers can render both note "
            "roles directly from the book JSON; no review-ledger lookup or "
            "clause transformation is required. The example HTML edition displays "
            "the near-Aleppo clause beside its form, then MAM's labelled form and "
            "the stored MAM clauses."
        ),
        mb_html.para(
            [
                "The third template represents marks without a written letter. "
                "Its position, accepted carrier forms, and display "
                "are explained in ",
                link("GAV notation and display", "#gav-display"),
                ".",
            ]
        ),
    ]


def _gav_display(numbers):
    rule8 = numbers.fig_value("rule8_sites")
    first = rule8[MARKS_WITHOUT_LETTER]
    second = rule8[consumer_notice.MARKS_WITHOUT_LETTER_OR_SPACE]
    return [
        mb_html.para(
            [
                "Position: the near-Aleppo dataset's ",
                he_name(MARKS_WITHOUT_LETTER),
                " represents marks at a position of nonzero width. Its name "
                "describes the position, not the carrier letter. The near-Aleppo "
                "dataset's ",
                he_name(consumer_notice.MARKS_WITHOUT_LETTER_OR_SPACE),
                " represents marks at a position of no width, including a medial "
                "position within a written atom. It inserts no separator. Existing "
                "pointings have not all been migrated to this positional distinction.",
            ]
        ),
        mb_html.para(
            [
                "Carrier forms: both templates accept GA ",
                mb_html.code(['{"1":"', he_pointed("אֵ"), '"}'], {"dir": "ltr"}),
                ". The original template also accepts GV ",
                mb_html.code(
                    ['{"1":"', he_pointed("וֹ"), '","carrier":"holam-male-vav"}'],
                    {"dir": "ltr"},
                ),
                " as its ",
                code("tmpl_params"),
                ". GA permits one or more artificial alefs, each followed by "
                "permitted marks. GV requires exactly VAV + HOLAM and the ",
                code("carrier=holam-male-vav"),
                " discriminator. Neither carrier permits a dagesh. The ",
                code("carrier"),
                " parameter is semantic metadata; it identifies the holam-male "
                "carrier and is not Scripture text.",
            ]
        ),
        mb_html.para(
            [
                "Display: GAV (guillemet-alef-vav) notation identifies artificial "
                "carriers, which are not written ketiv letters. JSON stores the "
                "template payload; the example edition supplies guillemets, as in ",
                he_pointed("«אֵ»"),
                " and ",
                he_pointed("«וֹ»"),
                ". An adopted GV retains ",
                he_pointed("«וֹ»"),
                "; converting it to ",
                he_pointed("«אֹ»"),
                " loses the chosen holam-male distinction. Surrounding separators "
                "remain explicit strings or whitespace templates; an orphan "
                "template inserts no automatic space.",
            ]
        ),
        mb_html.para(
            [
                "The supported nonzero-width template occurs at ",
                verse_refs(first),
                ", inside the pointed ketivs.",
                " The zero-width template occurs at ",
                verse_refs(second),
                ", with its GA carrier inside the written atom.",
            ]
        ),
        mb_html.para(
            [
                "The original GA example, at ",
                *verse_refs((("C1-Isaiah", "36", "12"),)),
                ", is ",
                he_pointed("«אֵאֵ֥»"),
                ". Near-Aleppo encodes the bracketed alef carriers supplied in "
                "MAM's note; they are not written ketiv letters.",
            ]
        ),
        mb_html.para(
            "For an orphan holam associated with a qere vav where the ketiv has "
            "yod, an edition can choose among these display options:"
        ),
        mb_html.unordered_list(
            [
                "Show GAV directly, retaining the GV carrier before the ketiv yod.",
                "Collapse the holam backwards onto the consonant before the ketiv yod.",
                "Attach U+05B9 HEBREW POINT HOLAM to the ketiv yod as a rendering "
                "accommodation, without asserting that the yod owns the mark.",
            ]
        ),
        mb_html.para(
            "These display accommodations preserve the stored carrier meaning. "
            "Their visual acceptability depends on the "
            "font and rendering system. Prepared markup could let CSS select "
            "among display forms or position the dot. CSS alone does not reorder "
            "the Unicode text, and hiding a carrier does not reliably reattach "
            "its combining mark to another letter."
        ),
        mb_html.para(
            [
                "Unicode's ",
                link(
                    "Hebrew specification, “Holam Male and Holam Haser”",
                    "https://www.unicode.org/versions/Unicode18.0.0/core-spec/chapter-9/",
                ),
                " uses U+05B9 for holam male on vav when the distinction is made. "
                "U+05BA HEBREW POINT HOLAM HASER FOR VAV distinguishes holam on "
                "consonantal vav; its use on other base letters is undefined. "
                "U+05B9 is also the ordinary holam on other letters. Unicode thus "
                "has no separate, letter-independent holam-male dot that would "
                "express the qere-vav role when attached to ketiv yod. Applying "
                "U+05B9 to yod can display the dot, but does not encode that role. "
                "A hypothetical letter-independent holam-male dot could make "
                "that intention explicit even on yod. The mismatch concerns "
                "encoded meaning, not a general Unicode ban on nonstandard "
                "letter-mark sequences.",
            ]
        ),
    ]


def _added_parameters(numbers):
    kq_by_family = numbers.fig_value("pointed_ketiv_by_family")
    families = [
        [
            numbers.record(kq_by_family[family], f"doc_figures: {family}"),
            " ",
            he_name(family),
        ]
        for family in POINTED_KETIV_FAMILIES
    ]
    return [
        mb_html.para(
            [
                "Near-Aleppo adds six parameters to templates. Five accompany MAM's "
                "parameters; the sixth identifies "
                "the explicit GV variant of near-Aleppo's own orphan-mark template.",
            ]
        ),
        mb_html.para(
            [
                "The parameter ",
                he_name(MAM_TARGET_PARAMETER),
                ", MAM's name for its text, holds MAM's target. Every note "
                "whose target near-Aleppo changes has it, and is renamed, as the "
                "previous subsection says: ",
                numbers.record(
                    numbers.snap_value(
                        "phase6_counts", "נוסח: notes given MAM's target"
                    )
                    + numbers.snap_value(
                        "phase6_counts", "מ:הערה-2: notes given MAM's target"
                    ),
                    "phase6_counts: the sum of the two counts of notes given MAM's "
                    "target",
                ),
                " notes. The original clauses in ",
                he_name(nap.MAM_NOTE),
                " have MAM's text as their subject. " "A clause opening with ",
                code("="),
                " in that parameter says that the sources it names agree with MAM. "
                "A clause opening with the same sign in parameter 2 instead "
                "describes agreement with near-Aleppo's target. The MAM-target "
                "parameter holds MAM-parsed-plus's target verbatim, templates "
                "included, so it has templates that occur nowhere else in "
                "near-Aleppo: ",
                *_joined(
                    [he_name(name) for name in numbers.fig_value("absent_in_copies")]
                ),
                ".",
            ]
        ),
        mb_html.para(
            [
                "The two flags mark a reading of the codex that one of MAM's notes "
                "gives and that near-Aleppo treats specially. ",
                code(APPLIED_AND_FLAGGED),
                " marks a reading near-Aleppo takes although the note marks it with "
                "a ",
                code("!"),
                " as a manifest error in the codex, so that near-Aleppo reproduces "
                "the scribe's slip and can be reversed: ",
                numbers.snap("flag_counts", APPLIED_AND_FLAGGED),
                " of them. ",
                code(FLAGGED_NOT_APPLIED),
                " marks a reading near-Aleppo does not take, being marked with a ",
                code("?"),
                " as doubtful, or outweighed by the note's prose, or a site where "
                "MAM's apparatus does not say what the codex has: ",
                numbers.snap("flag_counts", FLAGGED_NOT_APPLIED),
                " of them. A flag is a parameter of the note whose clause motivates "
                "it, and its value is that clause, copied from the note's body; at a "
                "site with no such clause, the flag is a parameter of the ketiv/qere "
                "template concerned, and its value is one of two fixed sentences: “",
                _QERE_SILENCE,
                "”, and “",
                _MAQAF_SILENCE,
                "”.",
            ]
        ),
        *doc_policy_examples.flag_examples(),
        mb_html.para(
            [
                "The parameter ",
                he_name(POINTED_KETIV_PARAMETER),
                " holds a pointed ketiv from MAM's notes, approved frozen "
                "inference, individual adjudication or a sealed reviewed portable "
                "decision, at a "
                "ketiv/qere template of the families ",
                *_joined([he_name(family) for family in POINTED_KETIV_FAMILIES]),
                ". It is the branch of the template that near-Aleppo's text follows, "
                "in place of MAM's pointed qere. Near-Aleppo has it at ",
                numbers.fig("pointed_ketiv_templates"),
                " templates, in ",
                numbers.fig("pointed_ketiv_verses"),
                " verses: ",
                *_joined(families),
                ".",
            ]
        ),
        mb_html.para(
            "The parameter carrier=holam-male-vav identifies the narrowly licensed "
            "GV variant of the orphan-mark template. Its parameter 1 must be exactly "
            "VAV + HOLAM. The carrier parameter is metadata; the artificial vav "
            "represents orphan holam and is not a written ketiv consonant."
        ),
    ]


def _characters(numbers):
    new = numbers.fig_value("new_characters")
    if len(new) != 1:
        raise AssertionError("the page's subsection names one new character")
    (character,) = new
    if character["code_point"] != "U+200C":
        raise AssertionError("the page's subsection is about the ZERO WIDTH NON-JOINER")
    return [
        mb_html.para(
            [
                "One character of near-Aleppo's text is a character that "
                "MAM-parsed-plus has only in a note body: ",
                character["code_point"],
                " ",
                character["name"],
                ", at ",
                verse_refs(character["verses"]),
                ", in the pointed ketiv that the note there gives the codex, between "
                "the ketiv's tav and he. The note's form has it, and it is there to "
                "keep fonts from treating the he's patah as a furtive patah.",
            ]
        ),
    ]


def _survives(numbers):
    verses = numbers.fig_value("verses")
    extant = numbers.fig_value("extant_verses")
    lost = numbers.fig_value("lost_verses")
    if extant + lost != verses:
        raise AssertionError("extant and lost verses do not make up near-Aleppo")
    lost_entire = numbers.fig_value("books_lost_entire")
    partly = numbers.fig_value("books_partly_lost")
    rows = [
        [
            english_book(book["book"]),
            numbers.record(book["lost"], f"doc_figures: lost verses of {book['book']}"),
            ", ".join(_run_text(run) for run in book["runs"]),
        ]
        for book in partly
    ]
    return [
        section_heading(SURVIVES),
        mb_html.para(
            [
                "A leaf of the codex survives at ",
                numbers.fig("extant_verses"),
                " of near-Aleppo's ",
                numbers.fig("verses"),
                " verses (",
                numbers.percent(extant, verses, "doc_figures: extant_verses / verses"),
                "), and none survives at ",
                numbers.fig("lost_verses"),
                " (",
                numbers.percent(lost, verses, "doc_figures: lost_verses / verses"),
                "), as MAM-basics' ",
                link("index of the codex's surviving text", ALEPPO_INDEX),
                ", which corrects and annotates ",
                link("J. David Stark's Aleppo Codex Index", STARK_INDEX),
                " (",
                link("CC BY 4.0", CC_BY_4),
                "), gives them, each of its ranges read as including both its ends. "
                "The codex is lost entire in ",
                numbers.record(len(lost_entire), "doc_figures: books_lost_entire"),
                " books, ",
                *_joined([english_book(book) for book in lost_entire]),
                ". It is lost in part in ",
                numbers.record(len(partly), "doc_figures: books_partly_lost"),
                " books, where the table shows, and survives whole in the others.",
            ]
        ),
        table(
            ["Book", "Verses lost", "Where"],
            rows,
            [None, NUMBER_CELL, None],
        ),
        mb_html.para(
            [
                "Near-Aleppo applies its general editorial policies at every "
                "verse. Where a leaf is lost, MAM's notes may still cite evidence "
                "of the codex's contents: testimony to its lost parts, "
                "under sigla such as ",
                he_name("א(ס)"),
                ", or photographs of its pages taken before they were lost. "
                "Near-Aleppo treats testimony and photographs as evidence of "
                "the codex's text. MAM's notes may also cite the codex's method, ",
                he_name("שיטת-א"),
                ", whose inferred forms near-Aleppo admits only where the "
                "codex is lost. ",
                link("MAM-with-doc's decoding of the sigla", SIGIL_DECODING),
                " says what each means. The clauses of MAM's notes that differ from "
                "MAM's text cite testimony or a photograph ",
                numbers.fig("testimony_citations_at_lost_verses"),
                " times, in ",
                numbers.fig("testimony_clauses_at_lost_verses"),
                " clauses, all where the codex is lost, and ",
                numbers.snap(
                    "phase5_counts",
                    "codex readings: differing clauses whose head names שיטת-א",
                ),
                " such clauses name the codex's method.",
            ]
        ),
    ]


def _run_text(run):
    first, last = run
    if first == last:
        return f"{first[1]}:{first[2]}"
    if first[1] == last[1]:
        return f"{first[1]}:{first[2]}–{last[2]}"
    return f"{first[1]}:{first[2]}–{last[1]}:{last[2]}"


def _joined(items):
    """``items`` joined as an English list: "a", "a and b", "a, b, and c"."""
    if not items:
        raise ValueError("nothing to join")
    out = []
    for index, item in enumerate(items):
        if index:
            if index == len(items) - 1:
                out.append(", and " if len(items) > 2 else " and ")
            else:
                out.append(", ")
        if isinstance(item, list):
            out.extend(item)
        else:
            out.append(item)
    return out
