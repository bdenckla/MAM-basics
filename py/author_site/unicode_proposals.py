"""``gh-pages/unicode-proposals.html`` -- Ben's Unicode and ISO proposals.

WHERE THIS CAME FROM, and it has moved twice.  It was a Google Doc until 2026-05-02, when
``1b7454a`` ported it into ``document-index/Unicode-and-ISO-Proposals.md`` and ``1e79349``
marked the Google Doc deprecated; that Markdown file is what this module now renders,
document-index having been evacuated into this repo on 2026-08-31
(``doc/PLAN-unify-the-document-index.md``).  The deprecation note survives as an HTML
comment on the page, because a reader who finds the old Google Doc needs to know it is not
the live copy.

A LOOSE PAGE AT THE DEPLOY ROOT, NOT A SUBTREE.  It sits beside ``index.html`` rather than
under a directory of its own.  Until 2026-08-31 that mattered: a derivation named
``published_subtrees`` built the index's last section from the tracked
``gh-pages/<subtree>/index.html`` files, and this page was correctly invisible to it, being
one page rather than a subtree.  Ben deleted that section and the derivation with it, so
the index now reaches every document, this one included, through ``site_data``'s authored
entries alone.  The two pages at the root share ``gh-pages/style.css``, ``site_data``'s
``CSS_HREF``, which is where the reason for that file is written down.

WHAT LGD AND LWD MEAN is on the page, because they are the source's own abbreviations and
half the entries would be unreadable without them.
"""

from __future__ import annotations

from pathlib import Path

from mb_cmn import paths
from mb_cmn import provenance
from mb_misc import mb_html

from author_site import site_data
from author_site.entries import Anchor

_FNAME = site_data.UNICODE_PROPOSALS_FNAME
_TITLE = site_data.UNICODE_PROPOSALS_TITLE

# Carried over from the Markdown this page replaced, which carried it over from the
# Google Doc IT replaced: a reader who finds that doc needs to know it is not the live
# copy.  The generator path is already in the breadcrumb this is appended to.
_ORIGIN_COMMENT = (
    "Originally created from a Google Doc, which is deprecated. This page is the"
    " canonical form and location for this information."
)

_L2 = "https://www.unicode.org/L2/L2025"
_GDOC = "https://docs.google.com/document/u/0/d"
_ONEDRIVE = "https://1drv.ms/w/c/1a2a340dcdf04d04"

# One tuple per proposal, in the source's order: the proposal's name, its "latest
# document" link, its L2 number and PDF if it reached one, and an optional status
# suffix.  A proposal with no L2 number has not been submitted under one.
_CURRENT_PROPOSALS = (
    (
        "Re-documenting ZARQA and ZINOR",
        Anchor("LGD", f"{_GDOC}/1qJby64wXq9ueTUHXFlIlYdgohRFlnUqT4SkyNEFWMKU/edit"),
        None,
        None,
    ),
    (
        "Errors about QAMATS QATAN in WG2 N4502",
        Anchor(
            "LGD",
            "https://docs.google.com/document/d/"
            "14ys4CwlF5IsOgBmUB9kvtxDZLrqrV1pnqBdj-JMaJZM/edit?usp=sharing",
        ),
        Anchor("L2/25-237", f"{_L2}/25237-qamats-qatan.pdf"),
        "ISO: This was later determined to be an ISO rather than a Unicode issue,"
        " and therefore this proposal was later made to an ISO working group rather"
        " than a Unicode working group.",
    ),
    (
        "Adding ALTERNATE PASEQ to Hebrew",
        Anchor("LGD", f"{_GDOC}/1VDVtngW9VJMD2er8V5JOFkUNp6BlSjjdgvcR9QDOpIE/edit"),
        Anchor("L2/25-243", f"{_L2}/25243-paseq-hebrew.pdf"),
        None,
    ),
    (
        "Adding ALTERNATE YERAH BEN YOMO to Hebrew",
        Anchor("LGD", f"{_GDOC}/1M7-sVTuKEJLdFRDXLpOeKEjtynSTvY2EM6Lj1uK4ylA/edit"),
        None,
        None,
    ),
    (
        "Forced helper forms of Hebrew accents",
        Anchor(
            "LWD",
            f"{_ONEDRIVE}/Eaik4ZX61L9HnM45cob2gHEBHRm5le8FVgMbhgRpIHH1pw?e=T9CBLU",
        ),
        None,
        None,
    ),
)

_DISCONTINUED_PROPOSALS = (
    (
        "Regarding the name HEAVY SHEVA",
        Anchor("LGD", f"{_GDOC}/18Zq9eJMREv8JtdMpME0zXtddA2FHDLpVXpa7gNvedEU/edit"),
        Anchor("L2/25-160", f"{_L2}/25160-heavy-sheva.pdf"),
        None,
    ),
    (
        "Documenting U+05C8 (originally SHEVA NA)",
        Anchor("LGD", f"{_GDOC}/1__REyYHTss_Rn4mhd2C-LycL1Mdn7imtTDqOdk6IVKo/edit"),
        None,
        None,
    ),
    (
        "Adding DAGESH HAZAQ to Hebrew",
        Anchor("LGD", f"{_GDOC}/1vhiBY7-PxxYcatxh44f-AJ91dVI72DgMHvqqyTMeoaM/edit"),
        Anchor("L2/25-175", f"{_L2}/25175-dagesh-xazaq.pdf"),
        None,
    ),
    (
        "Adding Hebrew stress helper accents",
        Anchor(
            "LWD",
            f"{_ONEDRIVE}/Eaap-g_IPGhFtNJczt9mXhwBTjLYp6XS9RUsRurnD6-HHQ?e=ldC6GM",
        ),
        Anchor("L2/25-242", f"{_L2}/25242-hebrew-accents.pdf"),
        "Withdrawn: I withdrew this proposal upon receiving feedback that it was"
        " unlikely to be accepted.",
    ),
)

_LEGEND = (
    "LGD = Latest Google Doc",
    "LWD = Latest (Microsoft) Word Doc (on OneDrive)",
)

_DISCONTINUED_INTRO = (
    "These proposals are retained only for historical interest because they have"
    " reached terminal states such as accepted, rejected, or withdrawn. The first"
    " three proposals in this section concern one of the two Hebrew points added in"
    " Unicode 18: U+05C8 HEBREW POINT SHEVA NA MUDGASH and U+05C9 HEBREW POINT"
    " DAGESH HAZAQ MUDGASH."
)


def gen_html_file(out_dir: Path | None = None) -> str:
    """Write the proposals page.  Returns the path written."""
    top_dir = paths.gh_pages_dir() if out_dir is None else Path(out_dir)
    out_path = str(top_dir / _FNAME)
    write_ctx = mb_html.WriteCtx(
        _TITLE,
        out_path,
        css_hrefs=(site_data.CSS_HREF,),
        html_comment=f"{provenance.generated_html_comment(__file__)} {_ORIGIN_COMMENT}",
    )
    mb_html.write_html_to_file(build_body(), write_ctx)
    return out_path


def build_body():
    """The page: current proposals, the legend, then discontinued proposals."""
    return [
        mb_html.heading_level_1(_TITLE),
        mb_html.ordered_list([_proposal_licont(one) for one in _CURRENT_PROPOSALS]),
        *[mb_html.para(one) for one in _LEGEND],
        mb_html.heading_level_2("Discontinued"),
        mb_html.para(_DISCONTINUED_INTRO),
        mb_html.ordered_list(
            [_proposal_licont(one) for one in _DISCONTINUED_PROPOSALS]
        ),
    ]


def _proposal_licont(proposal):
    name, latest, l2_doc, status = proposal
    links = [latest] if l2_doc is None else [latest, l2_doc]
    licont = [name, " "]
    for index, anchor in enumerate(links):
        licont.append(", " if index else "")
        licont.append(mb_html.anchor_h(anchor.text, anchor.href))
    if status is not None:
        licont.extend((" — ", status))
    return [one for one in licont if one != ""]
