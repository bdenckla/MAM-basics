r"""Generate gh-pages/accgram/dual-under-bars-in-leningrad-decalogues.html (issue #53).

An evidence page backing the "Supplied accents" Asides on supplied-marks.html (Exodus 20:3,
Deuteronomy 5:17), which speculate that the Leningrad naqdan may have meant one vertical
under-bar stroke (design doc §2, UXLC-utils repo) to serve both the taxton and elyon strands
at once. It shows three manuscript crops where the naqdan clearly did write two separate
under-bars on one letter, and deliberately draws no conclusion. The intro paragraph carries
that argument in full; the crops and captions live in ``_IMAGES``.

Run via ``main_accgram.py generate-html``.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from accgram import rtms_report
from accgram.almost_errors_html_shared import link, text_para
from wlc_cmn.utf8_io import force_utf8_io
from mb_cmn import provenance
from py_html import my_html_for_img
from py_html import wlc_utils_html as H

import wlc_paths

PAGE_TITLE = "Dual Under-Bars in the Leningrad Decalogues"
_WIDTH_CLASS = "goerwitz-tms-width-limited"

# (image file, reference label, caption) for each of the three crops, in reading order.
_IMAGES: tuple[tuple[str, str, str], ...] = (
    (
        "LC-043A-Exod-20v13-lo.png",
        "Exodus 20:13 לא",
        "Merkha and  tipeḥa under the ל.",
    ),
    (
        "LC-043A-Exod-20v13-tirtsach.png",
        "Exodus 20:13 תרצח",
        "Tipeḥa and silluq under the צ --"
        " the twin of Deuteronomy 5:17's תרצח."
        " The tipeḥa's angle here is weirdly close to horizontal,"
        " probably because of the lack of vertical space.",
    ),
    (
        "LC-102B-Deut-5v17-lo.png",
        "Deuteronomy 5:17 לא",
        "Merkha and  tipeḥa under the ל, matching Exodus 20:13's לא above.",
    ),
)


def default_html_out_path(repo_root: Path) -> Path:
    return (
        wlc_paths.gh_pages_dir()
        / "accgram"
        / "dual-under-bars-in-leningrad-decalogues.html"
    )


def add_args(parser: argparse.ArgumentParser, repo_root: Path) -> None:
    parser.add_argument(
        "--html-out",
        type=Path,
        default=default_html_out_path(repo_root),
        help="Output HTML path for the dual-under-bars page.",
    )


def _intro() -> tuple[object, ...]:
    return (
        H.heading_level_1(PAGE_TITLE),
        H.para(
            (
                "Two of the",
                *[" ", link("Supplied accents", "supplied-marks.html"), " page's"],
                " “Aside” paragraphs (Exodus 20:3, Deuteronomy 5:17) speculate that the"
                " Leningrad Codex's naqdan (pointing-scribe) may have intended a single"
                " vertical under-bar stroke to serve both the taḥton and elyon strands'"
                " readings at once, rather than the mark being genuinely absent for one"
                " strand.",
            )
        ),
        text_para(
            "The three photos below, from elsewhere in the very same two Decalogue"
            " passages, show the naqdan certainly could and did write two separate"
            " under-bar marks on one letter when two were meant: Exodus 20:13's"
            " לא and תרצח (that תרצח the direct twin of Deuteronomy 5:17's תרצח),"
            " and Deuteronomy 5:17's לא."
        ),
        H.para(
            "Whether that argues for or against the Asides' “one stroke, two purposes”"
            " speculation is for the reader to weigh -- this page's job is just to show"
            " the evidence, not to conclude for them."
        ),
    )


def _image_block(img_file: str, ref_label: str, caption_text: str) -> object:
    para = my_html_for_img.html_for_single_img(
        img_file, img_para_attr={"class": "goerwitz-tms-image"}, img_base="img/"
    )
    caption = H.figcaption(
        (H.bold(ref_label), ": ", caption_text),
        {"class": "goerwitz-tms-image-caption"},
    )
    return H.figure((para, caption), {"class": "goerwitz-tms-figure"})


def render_body_contents() -> tuple[object, ...]:
    sections: list[object] = [*_intro()]
    for img_file, ref_label, caption_text in _IMAGES:
        sections.append(_image_block(img_file, ref_label, caption_text))
    wrapper = H.div(tuple(sections), {"class": _WIDTH_CLASS})
    return (wrapper,)


def run(args: argparse.Namespace) -> None:
    html_out: Path = args.html_out
    html_out.parent.mkdir(parents=True, exist_ok=True)
    H.write_html_to_file(
        body_contents=render_body_contents(),
        write_ctx=H.WriteCtx(
            title=PAGE_TITLE,
            path=str(html_out),
            html_comment=provenance.generated_html_comment(__file__),
        ),
        path_to_style=rtms_report.path_to_gh_pages_style(html_out),
    )
    print(f"HTML: {html_out} ({len(_IMAGES)} images)")


def main() -> None:
    force_utf8_io()
    repo_root = wlc_paths.wlc_data_root()
    parser = argparse.ArgumentParser(description=__doc__)
    add_args(parser, repo_root=repo_root)
    run(parser.parse_args())


if __name__ == "__main__":
    main()
