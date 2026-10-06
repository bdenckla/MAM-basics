"""Render MAM-with-doc and near-Aleppo through one shared MAM renderer.

MAM_MODE preserves MAM titles, index, options and render-tag checks. Its output
must match the independent tracked MAM-with-doc files at PIN on every HTML run.
NEAR_ALEPPO_MODE supplies edition titles, its index, added apparatus labels and
the selected paseq display. Closed data dispatch recognizes the additional
templates and pointings. Both modes return page text in memory for checking
before writing. The same shared modules serve the ordinary MAM-with-doc CLI.
"""

import json
import subprocess
from dataclasses import dataclass
from typing import Callable

from near_aleppo import build_paths
from near_aleppo import doc_page
from near_aleppo import phase2_templates as phase2
from near_aleppo import phase6_flags
from mb_cmn import bib_locales as tbn
from mb_cmn import provenance
from mb_cmn import read_books_from_mam_parsed_plus as plus
from mb_misc import mb_html
from mb_misc import styles_mam_with_doc
from mwd import mwd_write_book as mwdwb
from mwd import mwd_write_index_dot_html as mwdwidh
from near_aleppo.phase6_mam_targets import MAM_TARGET_PARAMETER
from near_aleppo.phase6_rename import RENAMED_NOTES
from py_misc import mwd_utils as mwdu
from py_misc import near_aleppo_params as nap
from py_misc import ren_html_from_ren_el_mapping as hfrm
from py_misc import ren_tag_survey as rts

# MAM-basics' commit that the copy is pinned at, and whose MAM-with-doc pages MAM_MODE
# must reproduce.
PIN = "6343c7bb62be0721b4ed4239077d37126f9bbbd1"
CSS_NAME = "two_col_style.css"
EDITION_CSS_HREF = "../../MAM-with-doc/two_col_style.css"
INDEX_NAME = "index.html"


@dataclass(frozen=True)
class Mode:
    """What differs between MAM-with-doc and the edition, passed in at the top."""

    edition: str  # the pages' titles begin with it
    renopts: dict
    ht_tac_for_ren_tag: dict  # each render tag's HTML tag and class
    index: Callable  # (edition, css_hrefs) -> the index page's text
    check_tags: Callable  # (render tags seen) -> raises unless they are as expected


def _check_mam_tags(seen):
    # main_mam_with_doc.py's _handle_survey_results: every tag of the mapping is seen.
    expected = set(hfrm.HT_TAC_FOR_RT_FOR_MAM_WITH_DOC)
    if missing := expected - seen:
        raise AssertionError(f"render tags expected but not seen: {sorted(missing)}")


# The render tags that the edition produces, measured on 2026-09-25 when the edition
# was first rendered, and pinned: a tag gained or lost is a change in what the pages
# show, and raises until this set is updated deliberately. That day it was every tag
# of MAM-with-doc's mapping and the two of the lines the edition adds to a note.
_EDITION_RENDER_TAGS = frozenset(
    (
        "mam-anchor",
        "mam-bold",
        "mam-br-after-pe",
        "mam-br-before-good-ending",
        "mam-doc-callout",
        "mam-doc-target-without-callout",
        "mam-dqq-stressed",
        "mam-dqq-unstressed",
        "mam-good-ending",
        "mam-implicit-maqaf",
        "mam-kq",
        "mam-kq-k",
        "mam-kq-k-velo-q",
        "mam-kq-k-velo-q-maq",
        "mam-kq-q",
        "mam-kq-q-velo-k",
        "mam-letter-hung",
        "mam-letter-large",
        "mam-letter-small",
        "mam-spi-invnun",
        "mam-spi-pe",
        "mam-spi-samekh",
        "near-aleppo-english",
        "near-aleppo-label",
        "ren-tag-no-break-space",
        "ren-tag-octo-space",
        "ren-tag-thin-space",
    )
)


def _check_edition_tags(seen):
    if seen != _EDITION_RENDER_TAGS:
        raise AssertionError(
            "the edition's render tags have changed: gained "
            f"{sorted(seen - _EDITION_RENDER_TAGS)}, lost "
            f"{sorted(_EDITION_RENDER_TAGS - seen)}"
        )


def _edition_index(edition, css_hrefs):
    """The edition's index page: what it is, the books, and where to read more.

    It keeps MAM's license and attribution as MAM-with-doc's index states them, the
    dataset being derived from MAM, and links MAM-with-doc's decoding of the sigla at
    its MAM-basics address; it leaves out the links to MAM-with-doc's other products.
    Its prose is written to the privacy criteria of the public runtime and source-attribution boundary.
    """
    body = (
        mb_html.heading_level_1("The near-Aleppo edition"),
        mb_html.para(
            [
                "These pages are an example HTML edition of the near-Aleppo "
                "dataset. The edition has each book's text with MAM's notes "
                "beside it, as MAM-with-doc does. ",
                "See the ",
                mb_html.anchor_h(
                    "documentation for the near-Aleppo dataset", "../index.html"
                ),
                ".",
            ]
        ),
        mb_html.para(
            [
                "Where near-Aleppo's text of a note's target differs from MAM's, the "
                "dataset already stores a reviewed source agreement with near-Aleppo's "
                "form where a clause was recast, retaining its explanations and qualifications. "
                "The edition places that clause beside near-Aleppo's form. The remaining "
                "original clauses follow a line labelled ",
                _hebrew(MAM_TARGET_PARAMETER),
                " giving MAM's text and keeping those clauses' original subject. "
                "Notes requiring uncertain interpretation keep the complete original "
                "note in that MAM context. This applies in surviving, missing and "
                "uncertain sections alike. A line labelled ",
                _english(phase2.APPLIED_AND_FLAGGED),
                " or ",
                _english(phase2.FLAGGED_NOT_APPLIED),
                " gives one of near-Aleppo's flags. Vowels and accents that the codex "
                "writes under no letter have GA artificial alef carriers or the "
                "GV artificial VAV + HOLAM carrier. The edition displays both "
                "between double guillemets, retaining their stored carrier meaning. "
                "The carriers are not written ketiv letters. See ",
                mb_html.anchor_h(
                    "GAV notation and display in practice",
                    "../reading-json.html#gav-display",
                ),
                " for other editions' display options. Every paseq glyph is shown as "
                "MAM-with-doc shows a legarmeh, a thin space and then the glyph, since "
                "near-Aleppo intentionally drops MAM's distinctions between "
                "paseq and legarmeh.",
            ]
        ),
        mb_html.para(
            "Near-Aleppo is derived from Miqra according to the Masorah (MAM), whose "
            "license and source attribution are these:"
        ),
        mwdwidh.license_para(),
        mwdwidh.unordered_list_of_sections(),
        mb_html.horizontal_rule(),
        mb_html.anchor_h("MAM-with-doc's sigil decoding", doc_page.SIGIL_DECODING),
    )
    write_ctx = mb_html.WriteCtx(
        edition + ": Book Links",
        INDEX_NAME,
        head_style=mwdwidh.INDEX_STYLE,
        css_hrefs=css_hrefs,
        html_comment=provenance.generated_html_comment(__file__),
    )
    return mb_html.html_text(body, write_ctx)


def _hebrew(text):
    return mb_html.bdi(text, {"lang": "hbo"})


def _english(text):
    return mb_html.bdi(text, {"lang": "en"})


MAM_MODE = Mode(
    "MAM with doc",
    mwdwb.RENOPTS_MAM_WITH_DOC,
    hfrm.HT_TAC_FOR_RT_FOR_MAM_WITH_DOC,
    mwdwidh.render_index_dot_html,
    _check_mam_tags,
)
NEAR_ALEPPO_MODE = Mode(
    "near-Aleppo edition",
    {
        **mwdwb.RENOPTS_MAM_WITH_DOC,
        "ro_paseq_glyph_as_legarmeih": True,
        "ro_english_flag_values": (
            phase6_flags._QERE_SILENCE,
            phase6_flags._MAQAF_SILENCE,
        ),
    },
    hfrm.HT_TAC_FOR_RT_FOR_NEAR_ALEPPO_EDITION,
    _edition_index,
    _check_edition_tags,
)


def render(mode, books_mpu, *, css_hrefs, css_outputs):
    """Every page of ``mode`` for ``books_mpu``, as text, keyed by its name.

    The caller supplies stylesheet links and the stylesheet files it owns.
    """
    pages = {
        **css_outputs,
        INDEX_NAME: mode.index(mode.edition, css_hrefs),
    }
    survey = rts.make()
    for bkid in tbn.ALL_BK39_IDS:
        ecb = mode.edition, css_hrefs, bkid
        names = mwdu.filename_for_bkid(bkid), mwdu.filename_for_bkid_for_bido(bkid)
        book_survey, book_pages = mwdwb.render_book(
            ecb, books_mpu, names, mode.renopts, mode.ht_tac_for_ren_tag
        )
        survey = rts.add(survey, book_survey)
        if clash := set(pages) & set(book_pages):
            raise AssertionError(f"pages rendered twice: {sorted(clash)}")
        pages.update(book_pages)
    mode.check_tags(rts.get_ren_tags_seen(survey))
    return pages


def render_edition():
    """The edition's pages, from near-Aleppo, each page's provenance comment checked."""
    _assert_names_are_the_builds()
    dataset_parent = build_paths.dataset_dir().parent
    books_mpu = plus.read_parsed_plus_bk39s(tbn.ALL_BK39_IDS, str(dataset_parent))
    pages = render(
        NEAR_ALEPPO_MODE,
        books_mpu,
        css_hrefs=(EDITION_CSS_HREF,),
        css_outputs={},
    )
    for name, text in pages.items():
        comment = text.split("\n")[1]
        if comment != _edition_comment(name):
            raise AssertionError(f"{name}: {comment}")
    return pages


def _edition_comment(name):
    """The provenance comment of the edition's page ``name``: this module names
    itself on the index page, and the shared renderer's book writer on every other."""
    if name == INDEX_NAME:
        generator = "MAM-basics/py/near_aleppo/edition.py"
    else:
        generator = "MAM-basics/py/mwd/mwd_write_book.py"
    return f"{_COMMENT_START}{generator}. -->"


def _assert_names_are_the_builds():
    """The copy's names for what near-Aleppo adds are those the build writes."""
    pairs = (
        (nap.MAM_TARGET, MAM_TARGET_PARAMETER),
        (nap.APPLIED_AND_FLAGGED, phase2.APPLIED_AND_FLAGGED),
        (nap.FLAGGED_NOT_APPLIED, phase2.FLAGGED_NOT_APPLIED),
        (nap.POINTED_KETIV, phase2.POINTED_KETIV_PARAMETER),
        (nap.RENAMED_DOC, RENAMED_NOTES["נוסח"]),
        (nap.RENAMED_SCRDFFTAR, RENAMED_NOTES["מ:הערה-2"]),
        (nap.MARKS_WITHOUT_LETTER, phase2.MARKS_WITHOUT_LETTER),
    )
    for copy_name, build_name in pairs:
        if copy_name != build_name:
            raise AssertionError(
                f"the copy names {copy_name!r}, the build {build_name!r}"
            )


# Independent differential oracle for MAM-with-doc.

_MWD_DIR = "gh-pages/MAM-with-doc/"
# A page's provenance comment, which names its generator: MAM-basics' on one side and
# near-Aleppo's copy on the other.
_COMMENT_START = "<!-- Do not edit by hand. This file was generated by "
_PLACEHOLDER = "<!-- the provenance comment -->"
# The top-level files of MAM-with-doc's directory that other generators own.
_NOT_THE_RENDERERS = frozenset(("sigil-decoding.html",))


def check_mam_mode():
    """How MAM_MODE's pages for MAM-parsed-plus at PIN differ from MAM-with-doc's.

    Both are read from MAM-basics' object store at PIN, so the check does not depend
    on MAM-basics' working tree; MAM-with-doc's tracked pages there are the
    independent oracle. Every page must match its tracked page byte for byte, but for
    its one provenance comment, which on each side is checked to name that side's
    generator and then replaced by a placeholder. Returns the problems, an empty list
    meaning that the shared renderer's changes are inert on MAM's input, and the pages' count.
    """
    tracked_names = sorted(_tracked_page_names() - _NOT_THE_RENDERERS)
    inputs = [f"MAM-parsed/plus/{name}" for name in _plus_file_names()]
    blobs = _blobs_at_pin(inputs + [_MWD_DIR + name for name in tracked_names])

    def load_json(path):
        return json.loads(blobs[path])

    books_mpu = plus.read_parsed_plus_bk39s(
        tbn.ALL_BK39_IDS, "MAM-parsed", load_json=load_json
    )
    pages = render(
        MAM_MODE,
        books_mpu,
        css_hrefs=(CSS_NAME,),
        css_outputs={CSS_NAME: styles_mam_with_doc.css_for_mwd()},
    )
    problems = []
    if missing := sorted(set(tracked_names) - set(pages)):
        problems.append(f"MAM-with-doc has pages MAM mode does not write: {missing}")
    if extra := sorted(set(pages) - set(tracked_names)):
        problems.append(f"MAM mode writes pages MAM-with-doc does not have: {extra}")
    for name in sorted(set(pages) & set(tracked_names)):
        ours = _without_comment(pages[name], "MAM-basics/py/", name)
        theirs = _without_comment(
            blobs[_MWD_DIR + name].decode("utf-8"), "MAM-basics/py/", name
        )
        if ours != theirs:
            problems.append(f"{name} differs from MAM-with-doc's")
    return problems, len(pages)


def _without_comment(text, generator_prefix, name):
    """``text`` with its provenance comment, which must name a generator under
    ``generator_prefix``, replaced by the placeholder; a stylesheet has none."""
    lines = text.split("\n")
    comments = [i for i, line in enumerate(lines) if line.startswith(_COMMENT_START)]
    if name == CSS_NAME:
        if comments:
            raise AssertionError(f"{name} has a provenance comment")
        return text
    if len(comments) != 1 or comments[0] != 1:
        raise AssertionError(f"{name}: provenance comments at lines {comments}")
    comment = lines[1]
    if not comment.startswith(_COMMENT_START + generator_prefix):
        raise AssertionError(f"{name}: {comment}")
    return "\n".join([lines[0], _PLACEHOLDER, *lines[2:]])


def _mam_basics():
    return build_paths.mam_basics_dir()


def _git(*args, input_bytes=None):
    repo = _mam_basics().resolve()
    return subprocess.run(
        ["git", "-c", f"safe.directory={repo.as_posix()}", "-C", str(repo), *args],
        input=input_bytes,
        check=True,
        capture_output=True,
    ).stdout


def _tracked_page_names():
    """The files at the top of MAM-with-doc's tracked directory at PIN."""
    out = _git("ls-tree", "-z", PIN, _MWD_DIR)
    names = set()
    for entry in out.split(b"\0"):
        if not entry:
            continue
        meta, path = entry.split(b"\t", 1)
        if meta.split()[1] == b"blob":
            names.add(path.decode("utf-8")[len(_MWD_DIR) :])
    return names


def _plus_file_names():
    """MAM-parsed-plus's book files at PIN."""
    out = _git("ls-tree", "-z", "--name-only", PIN, "MAM-parsed/plus/")
    names = [p.decode("utf-8") for p in out.split(b"\0") if p]
    return [path[len("MAM-parsed/plus/") :] for path in names if path.endswith(".json")]


def _blobs_at_pin(paths):
    """Each of ``paths`` at PIN, as bytes, read with one git cat-file --batch."""
    request = "".join(f"{PIN}:{path}\n" for path in paths).encode("utf-8")
    out = _git("cat-file", "--batch", input_bytes=request)
    blobs = {}
    position = 0
    for path in paths:
        header_end = out.index(b"\n", position)
        header = out[position:header_end].split()
        if len(header) != 3 or header[1] != b"blob":
            raise AssertionError(f"{path} at {PIN}: {out[position:header_end]!r}")
        size = int(header[2])
        start = header_end + 1
        blobs[path] = out[start : start + size]
        position = start + size + 1
    if position != len(out):
        raise AssertionError("git cat-file --batch returned more than was asked")
    return blobs
