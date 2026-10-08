"""Selected NAEE features, rendered from Scripture with the edition's policy.

The ordered cases are a reading guide, not an exhaustive template survey.
Examples select ruby units from the rendered Scripture, excluding note lemmas.
The shared renderer owns closed template dispatch and both reading forms.
Run py/main_near_aleppo.py --html to regenerate these pages.
"""

import copy
from dataclasses import dataclass

from mb_cmn import bib_locales as tbn
from mb_cmn import provenance
from mb_cmn import read_books_from_mam_parsed_plus as plus
from mb_cmn import verse_external_links as vel
from mb_misc import mb_html
from near_aleppo import build_paths, doc_html, edition
from py_misc import mam_doc_utils, mwd_utils
from py_misc import ren_html_for_renel as hfr
from render_wt import render_wikitext as rwt

INDEX = "foi/index.html"
KETIV_QERE = "foi/interesting-ketiv-qere.html"


@dataclass(frozen=True)
class Case:
    identifier: str
    title: str
    description: str
    references: tuple


# Ben's first four entries, in the order requested on 2026-10-08.
CASES = (
    Case(
        "2-samuel-8-3",
        "2 Samuel 8:3 — a wide qere",
        "The qere is a maqaf compound above a shorter ketiv atom. "
        "Look at the space reserved for the pair in the verse.",
        ((tbn.BK_SND_SAM, 8, 3),),
    ),
    Case(
        "isaiah-54-16",
        "Isaiah 54:16 — a wider single-atom qere",
        "The qere is a single atom wider than the ketiv beneath it.",
        ((tbn.BK_ISAIAH, 54, 16),),
    ),
    Case(
        "genesis-30-11",
        "Genesis 30:11 — two qere atoms",
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


def _examples():
    bkids = tuple(dict.fromkeys(ref[0] for case in CASES for ref in case.references))
    books = plus.read_parsed_plus_bk39s(bkids, str(build_paths.dataset_dir().parent))
    mode = edition.NEAR_ALEPPO_MODE
    ctx = hfr.HfrCtx(mode.ht_tac_for_ren_tag)
    rendered = {bkid: rwt.render(bkid, books, mode.renopts, {}) for bkid in bkids}
    examples = {}
    for case in CASES:
        for reference in case.references:
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
            examples[reference] = rubies
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


def _case_table(case, examples):
    rows = []
    for reference in case.references:
        bkid, chapter, verse = reference
        bcvt = tbn.mk_bcvtmam(bkid, chapter, verse)
        rows.append(
            (
                examples[reference],
                mb_html.anchor_h(
                    tbn.short_bcv_of_bcvt(bcvt),
                    "../" + vel.near_aleppo_href(bkid, chapter, verse),
                ),
                mb_html.anchor_h(
                    "Published", vel.near_aleppo_url(bkid, chapter, verse)
                ),
            )
        )
    return doc_html.table(
        ("Ketiv with qere above", "Verse in NAEE", "Website"),
        rows,
        (
            {"dir": "rtl", "lang": "hbo", "class": "pointed"},
            doc_html.BCV_CELL,
            None,
        ),
    )


def render():
    """Return the FOI index and its selected k/q guide as UTF-8 page bytes."""
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
                )
            ]
        ),
    ]
    examples = _examples()
    kq_title = "Interesting ketiv/qere cases in NAEE"
    kq_body = [
        mb_html.heading_level_1(kq_title),
        _navigation(),
        mb_html.para(
            "Ketiv is the primary text, with pointed qere above it at the same size. "
            "When qere is wider, the shorter ketiv is centered beneath it. "
            "Use the verse reference to open this copy of NAEE, or “Published” "
            "to open the website. The verse includes surrounding text and notes."
        ),
        mb_html.ordered_list(
            [mb_html.anchor_h(case.title, "#" + case.identifier) for case in CASES]
        ),
    ]
    for case in CASES:
        kq_body.extend(
            [
                mb_html.heading_level_2(case.title, {"id": case.identifier}),
                mb_html.para(case.description),
                _case_table(case, examples),
            ]
        )
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
        )
        pages[path] = mb_html.html_text(body, ctx).encode("utf-8")
    return pages
