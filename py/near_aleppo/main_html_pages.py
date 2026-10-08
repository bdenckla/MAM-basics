"""Render near-Aleppo documentation and example edition with the shared renderer.

Documentation figures come from the build's population file or are computed
from local MAM, near-Aleppo and the Aleppo coverage index. The shared MAM-with-doc
renderer writes the 39-book example edition and its long-note pages.

The output tree is gh-pages/near-aleppo. Generation owns its complete contents
except two hash-checked copies of Taamey D. Pages render entirely in memory before
writing. Beside them it writes out/render-tags-unused/near-aleppo.json, the render tags
the edition handles that no page uses. The public presentation ledger preserves
source notes and reviewed clause dispositions, with each note's evidence hash and a
full-build inventory differential.

Use py/main_near_aleppo.py --html, or add --check for a read-only comparison.
--refresh-note-review refreshes inventory and retains reviews only for unchanged
evidence; --check-note-review requires all changed-note presentations to be
reviewed and equal to a fresh source enumeration.
"""

import argparse
import hashlib
import json
import sys

from near_aleppo import build_expectations
from near_aleppo import build_paths
from near_aleppo import doc_figures
from near_aleppo import doc_he_transfer
from near_aleppo import doc_daniel_sheva
from near_aleppo import doc_pages
from near_aleppo import doc_style
from near_aleppo import edition
from near_aleppo import features_of_interest
from near_aleppo import doc_note_review
from near_aleppo.doc_html import Numbers
from mb_cmn import file_io
from mb_cmn import provenance
from mb_misc import mb_html
from mb_misc import mb_html_get_lines
from py_misc import ren_tag_survey as rts

_SHARED_STYLESHEET = "../MAM-parsed/style.css"
_STYLESHEET = "style.css"
_EDITION = "edition/"
_FONTS = ("woff2/Taamey_D.woff2", _EDITION + "woff2/Taamey_D.woff2")
# The SHA-256 of MAM-basics' gh-pages/MAM-with-doc/woff2/Taamey_D.woff2, 21,148 bytes,
# copied with git show at 732e9f124345306461336ee9873960d90d63b9b6. The file is the same
# at the shared renderer's pin, bfab23cbfd0d1928892dd23aab31da826d8836b3, as the re-pin of
# 2026-09-27 measured. Nothing here reads the font at the pin, so a re-pin compares it.
_FONT_SHA256 = "5cc8df8ae3311b91e506edbb294561f6f0e39ebe4260bdb972c90902186c2474"
# The render tags the edition handles that no page uses, written beside the pages.
_UNUSED_TAGS_REPORT = rts.unused_report_path("near-aleppo")


def render():
    """The pages this entry point writes, by path within html-pages/, as bytes, and the
    render tags the edition handles that no page uses."""
    snapshot = build_expectations.load()
    numbers = Numbers(snapshot, doc_figures.figures(snapshot))
    # Both modes render in memory. Documentation has its own navigation layout;
    # the edition adds its ruby stylesheet to MAM-with-doc's shared styles.
    comment = provenance.generated_html_comment(__file__)
    stylesheet = doc_style.css(comment)
    pages = {
        _STYLESHEET: stylesheet.encode("utf-8"),
        doc_pages.script_name(): doc_pages.redirect_script(comment).encode("utf-8"),
        _EDITION + "ketiv-qere.css": edition.ruby_css().encode("utf-8"),
    }
    for name, (title, body) in doc_pages.pages(numbers).items():
        pages[name] = _documentation_html(title, body, comment).encode("utf-8")
    edition_pages, unused_tags = edition.render_edition()
    for name, text in edition_pages.items():
        pages[_EDITION + name] = text.encode("utf-8")
    pages.update(features_of_interest.render())
    pages.update(doc_he_transfer.assets())
    pages.update(doc_daniel_sheva.assets())
    return pages, unused_tags


def _documentation_html(title, body, comment):
    html_el = mb_html.html_el2(
        title,
        body,
        css_hrefs=("../document.css", _SHARED_STYLESHEET, _STYLESHEET),
    )
    policy = mb_html._HGL_POLICY
    options = {
        **policy,
        "hgl-add-wbr": False,
        "hgl-max-line-len": 100,
        "hgl-line-breaks-allowed": True,
        "hgl-lb1": {
            **policy["hgl-lb1"],
            "nav": "\n",
            "script": "",
        },
        "hgl-lb2": {
            **policy["hgl-lb2"],
            **{tag: "\n" for tag in ("nav", "script")},
        },
    }
    lines = mb_html_get_lines.get_lines_from_html_el(options, html_el)
    return f"<!doctype html>\n<!-- {comment} -->\n" + "\n".join(lines)


def _unexpected(pages):
    """The files in html-pages/ that are neither a page written here nor a font."""
    out_dir = build_paths.html_pages_dir()
    if not out_dir.is_dir():
        return []
    owned = set(pages) | set(_FONTS)
    return sorted(
        path.relative_to(out_dir).as_posix()
        for path in out_dir.rglob("*")
        if path.is_file() and path.relative_to(out_dir).as_posix() not in owned
    )


def _font_problems():
    problems = []
    for name in _FONTS:
        font = build_paths.html_pages_dir() / name
        if not font.is_file():
            problems.append(
                f"missing {name}: copy it with git show "
                "bfab23cb:gh-pages/MAM-with-doc/woff2/Taamey_D.woff2 from MAM-basics"
            )
        elif hashlib.sha256(font.read_bytes()).hexdigest() != _FONT_SHA256:
            problems.append(f"{name} is not the pinned copy of MAM-basics' font")
    return problems


def write(pages, unused_tags):
    out_dir = build_paths.html_pages_dir()
    problems = [f"unexpected {name}" for name in _unexpected(pages)]
    problems += _font_problems()
    if problems:
        raise AssertionError(f"{out_dir}: " + "; ".join(problems))
    for name, data in pages.items():
        path = out_dir / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    print(f"Wrote {len(pages)} files to {out_dir}")
    file_io.json_dump_to_file_path(unused_tags, str(_UNUSED_TAGS_REPORT))


def check(pages, unused_tags):
    out_dir = build_paths.html_pages_dir()
    problems = []
    for name, data in pages.items():
        path = out_dir / name
        if not path.exists():
            problems.append(f"missing {name}")
        elif path.read_bytes() != data:
            problems.append(f"differs {name}")
    if not _UNUSED_TAGS_REPORT.is_file():
        problems.append(f"missing {_UNUSED_TAGS_REPORT}")
    elif json.loads(_UNUSED_TAGS_REPORT.read_text(encoding="utf-8")) != unused_tags:
        problems.append(f"differs {_UNUSED_TAGS_REPORT}")
    problems += [f"unexpected {name}" for name in _unexpected(pages)]
    problems += _font_problems()
    if problems:
        print(f"The pages in {out_dir} are not current:")
        for problem in problems:
            print(f"  {problem}")
        return 1
    print(
        f"The pages in {out_dir} are current ({len(pages)} files and "
        f"{len(_FONTS)} copies of the font)"
    )
    return 0


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")
    parser = argparse.ArgumentParser(description=__doc__)
    operation = parser.add_mutually_exclusive_group()
    operation.add_argument(
        "--check",
        action="store_true",
        help="Regenerate in memory and compare with the tracked pages; write nothing.",
    )
    operation.add_argument(
        "--refresh-note-review",
        action="store_true",
        help=(
            "Refresh only the changed-note inventory, keeping each review whose "
            "evidence is unchanged."
        ),
    )
    operation.add_argument(
        "--check-note-review",
        action="store_true",
        help="Require a current inventory with a reviewed disposition for every note.",
    )
    args = parser.parse_args(argv)
    if args.refresh_note_review:
        doc_note_review.refresh()
        return
    if args.check_note_review:
        doc_note_review.check()
        return
    pages, unused_tags = render()
    if args.check:
        return check(pages, unused_tags)
    write(pages, unused_tags)
