"""Selected NAEE features, rendered from Scripture with the edition's policy.

The ordered cases are a reading guide, not an exhaustive template survey.
Examples show complete rendered verses, excluding note lemmas.
The shared renderer owns closed template dispatch and both reading forms.
Run py/main_near_aleppo.py --html to regenerate these pages.
"""

import copy
from dataclasses import dataclass

from hkq_cmn import uxlc_external_links
from mb_cmn import bib_locales as tbn
from mb_cmn import provenance
from mb_cmn import read_books_from_mam_parsed_plus as plus
from mb_cmn import verse_external_links as vel
from mb_misc import mb_html
from near_aleppo import build_paths, edition
from near_aleppo import foi_qere_without_ketiv
from py_misc import mam_doc_utils, mwd_utils
from py_misc import ren_html_for_renel as hfr
from render_wt import render_wikitext as rwt

INDEX = "foi/index.html"
KETIV_QERE = "foi/interesting-ketiv-qere.html"
# Leave room for ruby annotations on adjacent wrapped lines of the verse.
_GUIDE_STYLE = ".pointed.foi-verse { line-height: 2.7; }"


@dataclass(frozen=True)
class Case:
    identifier: str
    label: str
    description: str
    references: tuple

    @property
    def title(self):
        if len(self.references) == 1:
            return f"{_reference_text(self.references[0])} — {self.label}"
        return self.label


# Ben's first four entries keep their requested order; later additions follow.
CASES = (
    Case(
        "2-samuel-8-3",
        "a wide qere",
        "The qere is a maqaf compound above a shorter ketiv atom. "
        "Look at the space reserved for the pair in the verse.",
        ((tbn.BK_SND_SAM, 8, 3),),
    ),
    Case(
        "isaiah-54-16",
        "a final dalet carrier",
        "The single-atom qere has an additional he. The ketiv's final-nun "
        "dagesh, tsere and mahapakh are displayed on an artificial dalet carrier "
        "immediately after the nun, without a space.",
        ((tbn.BK_ISAIAH, 54, 16),),
    ),
    Case(
        "genesis-30-11",
        "two qere atoms",
        "The qere has two atoms separated by a space above one ketiv atom.",
        ((tbn.BK_GENESIS, 30, 11),),
    ),
    Case(
        "qere-without-ketiv",
        "Qere without ketiv",
        "Ruth 3:5 and Judges 20:13 show qere without ketiv. "
        "NAEE puts the editorial label “no ketiv” on the baseline. "
        "That label occupies space beneath the qere.",
        ((tbn.BK_RUTH, 3, 5), (tbn.BK_JUDGES, 20, 13)),
    ),
    Case(
        "isaiah-26-20",
        "a yod in the ketiv",
        "The ketiv דלתיך has a yod absent from the qere דלתך. "
        "Compare the pointing and width of the two readings.",
        ((tbn.BK_ISAIAH, 26, 20),),
    ),
    Case(
        "1-chronicles-9-4",
        "a two-atom qere inside a maqaf compound",
        "The single ketiv atom בנימן has a two-atom qere. "
        "The pair sits inside a longer maqaf compound, with maqafs on both sides; "
        "inspect the space between the qere atoms and the connections "
        "to neighboring atoms.",
        ((tbn.BK_FST_CHR, 9, 4),),
    ),
)


def _rubies(node):
    """Select ruby from an already-rendered HTML tree, preserving its contents."""
    if isinstance(node, str):
        return []
    if isinstance(node, (tuple, list)):
        return [ruby for child in node for ruby in _rubies(child)]
    if mb_html.htel_get_tag(node) == "ruby":
        return [copy.deepcopy(node)]
    return _rubies(node.get("contents") or ())


def _verses(references=None):
    references = references or tuple(ref for case in CASES for ref in case.references)
    bkids = tuple(dict.fromkeys(ref[0] for ref in references))
    books = plus.read_parsed_plus_bk39s(bkids, str(build_paths.dataset_dir().parent))
    mode = edition.NEAR_ALEPPO_MODE
    ctx = hfr.HfrCtx(mode.ht_tac_for_ren_tag)
    rendered = {bkid: rwt.render(bkid, books, mode.renopts, {}) for bkid in bkids}
    examples = {}
    for reference in references:
        bkid, chapter, verse = reference
        bcvt = tbn.mk_bcvtmam(bkid, chapter, verse)
        veraf = rendered[bkid][bcvt]
        nondoc = veraf.map_over(mam_doc_utils.mark_doc_targets)
        docs = veraf.map_over(mam_doc_utils.extract_docs)
        ver_ndd = mwd_utils.VerseNdd(bcvt, nondoc, docs)
        scripture = mwd_utils._html_for_nondoc(ctx, ver_ndd).verse
        rubies = _rubies(scripture)
        if not rubies:
            raise ValueError(f"FOI case has no Scripture ruby: {reference}")
        examples[reference] = scripture
    return examples


def _navigation():
    return mb_html.para(
        [
            mb_html.anchor_h("Features of interest", "index.html"),
            " · ",
            mb_html.anchor_h("NAEE book links", "../edition/index.html"),
            " · ",
            mb_html.anchor_h("Dataset documentation", "../index.html"),
        ]
    )


def _reference_text(reference):
    book, chapter, verse = reference
    return f"{uxlc_external_links.book_display_name(book)} {chapter}:{verse}"


def _reference_link(reference):
    return mb_html.anchor_h(
        _reference_text(reference), "../" + vel.near_aleppo_href(*reference)
    )


def _case_contents(case, verses):
    title = (
        [_reference_link(case.references[0]), " — ", case.label]
        if len(case.references) == 1
        else case.label
    )
    contents = [
        mb_html.heading_level_2(title, {"id": case.identifier}),
        mb_html.para(case.description),
    ]
    if case.identifier == "qere-without-ketiv":
        contents.append(
            mb_html.para(
                mb_html.anchor_h(
                    "Qere without ketiv: manuscript readings and crops",
                    "qere-without-ketiv.html",
                )
            )
        )
    for reference in case.references:
        if len(case.references) > 1:
            contents.append(mb_html.heading_level_3(_reference_link(reference)))
        contents.append(
            mb_html.para(
                verses[reference],
                {"dir": "rtl", "lang": "hbo", "class": "pointed foi-verse"},
            )
        )
    return contents


def render():
    """Return the FOI pages and their evidence images as bytes."""
    index_title = "Near-Aleppo features of interest"
    index_body = [
        mb_html.heading_level_1(index_title),
        _navigation(),
        mb_html.para(
            "Selected features to inspect in the near-Aleppo example edition (NAEE)."
        ),
        mb_html.ordered_list(
            [
                mb_html.anchor_h(
                    "Interesting ketiv/qere cases", "interesting-ketiv-qere.html"
                ),
                mb_html.anchor_h("Qere without ketiv", "qere-without-ketiv.html"),
            ]
        ),
    ]
    study_records = foi_qere_without_ketiv.records()
    references = tuple(
        dict.fromkeys(
            [ref for case in CASES for ref in case.references]
            + [tuple(row["reference"]) for row in study_records]
        )
    )
    verses = _verses(references)
    kq_title = "Interesting ketiv/qere cases in NAEE"
    kq_body = [
        mb_html.heading_level_1(kq_title),
        _navigation(),
        mb_html.para(
            "Ketiv is the primary text, with pointed qere above it at the same size "
            "and CLC's box around the pair. "
            "When qere is wider, the shorter ketiv is centered beneath it. "
            "Each heading's verse reference opens the verse in NAEE, "
            "with its surrounding text and notes."
        ),
        mb_html.ordered_list(
            [mb_html.anchor_h(case.title, "#" + case.identifier) for case in CASES]
        ),
    ]
    for case in CASES:
        kq_body.extend(_case_contents(case, verses))
    comment = provenance.generated_html_comment(__file__)
    pages = {}
    for path, title, body in (
        (INDEX, index_title, index_body),
        (KETIV_QERE, kq_title, kq_body),
    ):
        ctx = mb_html.WriteCtx(
            title,
            path,
            css_hrefs=(
                "../../document.css",
                "../../MAM-parsed/style.css",
                "../style.css",
                "../edition/ketiv-qere.css",
            ),
            html_comment=comment,
            head_style=_GUIDE_STYLE if path == KETIV_QERE else None,
        )
        pages[path] = mb_html.html_text(body, ctx).encode("utf-8")
    pages.update(foi_qere_without_ketiv.render(verses, study_records))
    return pages
