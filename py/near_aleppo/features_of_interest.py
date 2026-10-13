"""Selected NAEE features, rendered from Scripture with the edition's policy.

The ordered cases are a reading guide, not an exhaustive template survey.
Examples use rendered Scripture, excluding note lemmas.
The shared renderer owns closed template dispatch and both reading forms.
Run py/main_near_aleppo.py --html to regenerate these pages.
"""

import copy
from dataclasses import dataclass
import struct

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
_SHIN_IMAGE = "aleppo-2K18-27-shin.png"


@dataclass(frozen=True)
class Case:
    identifier: str
    label: str
    description: str
    references: tuple
    compare_mam: bool = False

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
        "The qere is a maqaf compound above a shorter ketiv atom.",
        ((tbn.BK_SND_SAM, 8, 3),),
    ),
    Case(
        "isaiah-54-16",
        "a final dalet carrier",
        "The single-atom qere has an additional he. The ketiv's final-nun "
        "dagesh, tsere and mahapakh are displayed on an artificial dalet carrier "
        "immediately after the nun, without a space. "
        "Carrier notation usually indicates that marks are orphaned or that the "
        "letter they belong to is unclear. In this case, a strong argument can "
        "be made that the marks belong to the final nun. We use carrier (orphan) "
        "syntax mainly because many fonts have difficulty displaying these "
        "marks on a final nun.",
        ((tbn.BK_ISAIAH, 54, 16),),
    ),
    Case(
        "genesis-30-11",
        "two qere atoms",
        "The qere has two space-separated atoms above one ketiv atom.",
        ((tbn.BK_GENESIS, 30, 11),),
    ),
    Case(
        "qere-without-ketiv",
        "Qere without ketiv",
        "Ruth 3:5 and Judges 20:13 show qere without ketiv; "
        "in Ruth 3:5 there is no orphan niqqud for the qere "
        "whereas in Judges 20:13 there is.",
        ((tbn.BK_RUTH, 3, 5), (tbn.BK_JUDGES, 20, 13)),
    ),
    Case(
        "isaiah-26-20",
        "MAM ketiv/qere inside a three-atom maqaf compound",
        "In MAM, the ketiv יעבור and qere יַעֲבׇר occupy the middle atom "
        "of a compound starting with עַד־ and ending with זָֽעַם. "
        "NAEE displays עַד־יַעֲבָור־זָֽעַם, with no qere above the middle atom. "
        "This follows MAM's note, which reports the ketiv and no qere note "
        "in the Aleppo Codex. In forming the near-Aleppo dataset, we inferred "
        "the ketiv's pointing from the qere.",
        ((tbn.BK_ISAIAH, 26, 20),),
        compare_mam=True,
    ),
    Case(
        "1-chronicles-9-4",
        "a two-atom qere inside a maqaf compound",
        "The single ketiv atom בנימן has a two-atom qere.",
        ((tbn.BK_FST_CHR, 9, 4),),
    ),
    Case(
        "2-kings-18-27",
        "a euphemistic qere and no shin dot",
        "The ketiv has a two-atom euphemistic qere. "
        "The Aleppo Codex has no dot of any kind above the ketiv's shin. "
        "The manuscript is well preserved here, so the absence is clear. "
        "Near-Aleppo retains its current pointing without a shin dot. "
        "The shin dot in the Introduction's list needs correction.",
        ((tbn.BK_SND_KGS, 18, 27),),
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


def _isaiah_26_20_excerpt(scripture):
    """Omit the first half and color the final compound in rendered Scripture."""
    prefix, middle, ending = scripture[-3:]
    if not isinstance(prefix, str) or not isinstance(ending, str):
        raise ValueError("Isaiah 26:20 excerpt boundaries are not plain text")
    before, separator, first = prefix.rpartition(" ")
    boundary, space, remaining = before.lstrip().partition(" ")
    maqaf = "\N{HEBREW PUNCTUATION MAQAF}"
    sof_pasuq = "\N{HEBREW PUNCTUATION SOF PASUQ}"
    if (
        not separator
        or not space
        or "\N{HEBREW ACCENT ETNAHTA}" not in boundary
        or not first.endswith(maqaf)
        or not ending.endswith(sof_pasuq)
        or not isinstance(middle, dict)
        or mb_html.htel_get_tag(middle) != "span"
    ):
        raise ValueError("Isaiah 26:20 excerpt no longer has the expected boundaries")
    compound = mb_html.span(
        [first, middle, ending.removesuffix(sof_pasuq)],
        {"class": "example-difference"},
    )
    return ["… ", remaining, " ", compound, sof_pasuq]


def _shin_figure(raw):
    """Show Ben's unchanged supplied Aleppo crop; provenance is in the study."""
    if raw[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("The 2 Kings 18:27 evidence image is not PNG")
    width, height = struct.unpack(">II", raw[16:24])
    return [
        mb_html.para(
            mb_html.img(
                {
                    "src": "../img/" + _SHIN_IMAGE,
                    "alt": "Aleppo Codex, 2 Kings 18:27: no dot above shin in the ketiv שניהם",
                    "width": str(width),
                    "height": str(height),
                    "style": "max-width: 100%; height: auto;",
                }
            )
        ),
        mb_html.para(
            "The shin has no dot above it in this Aleppo Codex crop at 2 Kings 18:27."
        ),
        mb_html.para(
            mb_html.anchor_h(
                "Manuscript observation, screenshot provenance and Introduction comparison",
                "https://github.com/bdenckla/MAM-basics/blob/main/"
                "doc/near-aleppo-avi-ketiv-investigation.html",
            )
        ),
        mb_html.para(
            [
                "The Introduction correction is tracked in ",
                mb_html.anchor_h(
                    "MAM-basics issue 305",
                    "https://github.com/bdenckla/MAM-basics/issues/305",
                ),
                ".",
            ]
        ),
    ]


def _case_contents(case, verses, shin_image):
    title = (
        [_reference_link(case.references[0]), " — ", case.label]
        if len(case.references) == 1
        else case.label
    )
    contents = [
        mb_html.heading_level_2(title, {"id": case.identifier}),
        mb_html.para(case.description),
    ]
    if case.identifier == "2-kings-18-27":
        contents.extend(_shin_figure(shin_image))
    if case.compare_mam:
        contents.append(
            mb_html.para(
                mb_html.anchor_h(
                    "Compare this verse in MAM-with-doc",
                    vel.mam_with_doc_url(*case.references[0]),
                )
            )
        )
    if case.identifier == "qere-without-ketiv":
        contents.append(
            mb_html.para(
                mb_html.anchor_h(
                    "Qere without ketiv: manuscript readings and crops",
                    "qere-without-ketiv.html",
                )
            )
        )
    if case.identifier == "1-chronicles-9-4":
        display_attrs = {"dir": "rtl", "lang": "hbo", "class": "pointed center"}
        maqaf = "\N{HEBREW PUNCTUATION MAQAF}"
        # Orange and yellow take darker shades in light mode to stay legible on white.
        red = "color: red"
        orange = "color: light-dark(#b35900, orange)"
        yellow = "color: light-dark(#806600, yellow)"
        green = "color: green"
        contents.extend(
            [
                mb_html.para(
                    "When viewed in context, the ketiv forms a four-atom maqaf compound:"
                ),
                mb_html.para(
                    [
                        mb_html.span("בֶן" + maqaf, {"style": red}),
                        mb_html.span("בָּנִ֔ימִן" + maqaf, {"style": orange}),
                        mb_html.span("בְּנֵי" + maqaf, {"style": yellow}),
                        mb_html.span("פֶ֖רֶץ", {"style": green}),
                    ],
                    display_attrs,
                ),
                mb_html.para(
                    "In contrast, the qere forms a two-atom maqaf compound "
                    "followed by a three-atom maqaf compound:"
                ),
                mb_html.para(
                    [
                        mb_html.span("בֶן" + maqaf, {"style": red}),
                        mb_html.span("בָּנִ֔י", {"style": orange}),
                        " ",
                        mb_html.span("מִן" + maqaf, {"style": red}),
                        mb_html.span("בְּנֵי" + maqaf, {"style": orange}),
                        mb_html.span("פֶ֖רֶץ", {"style": yellow}),
                    ],
                    display_attrs,
                ),
            ]
        )
    for reference in case.references:
        if len(case.references) > 1:
            contents.append(mb_html.heading_level_3(_reference_link(reference)))
        scripture = verses[reference]
        if case.identifier == "isaiah-26-20":
            scripture = _isaiah_26_20_excerpt(scripture)
        contents.append(
            mb_html.para(
                scripture,
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
            "In NAEE (the Near-Aleppo example edition), "
            "the pointed ketiv is the primary text, "
            "with the pointed qere above it "
            'and a curved box or "cartouche" around the ketiv/qere pair. '
            "When the qere is wider, the ketiv is centered beneath it."
        ),
        mb_html.ordered_list(
            [mb_html.anchor_h(case.title, "#" + case.identifier) for case in CASES]
        ),
    ]
    shin_image = (build_paths.asset_dir() / _SHIN_IMAGE).read_bytes()
    for case in CASES:
        kq_body.extend(_case_contents(case, verses, shin_image))
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
    pages["img/" + _SHIN_IMAGE] = shin_image
    pages.update(foi_qere_without_ketiv.render(verses, study_records))
    return pages
