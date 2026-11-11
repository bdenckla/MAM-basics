"""Mechanical lint: a page of the published site links the site's other pages relatively.

Every tracked HTML file under ``gh-pages/`` is read.  An ``href`` or ``src`` that begins with
the site's own address, ``mb_cmn.site_links.SITE_URL``, is a finding, unless its page is
listed in ``_PAGES_KEEPING_THE_SITE_ADDRESS`` with the reason it keeps the address.  Ben,
2026-11-11: "Fix it to be a relative link and fix any other inappropriately-absolute links
please".  py/mb_cmn/site_links.py says why a link within the site is relative, and computes
it.
"""

import re
import subprocess

from mb_cmn import paths
from mb_cmn.site_links import SITE_URL

_PAGES_PREFIX = "gh-pages/"

# An href or src attribute, either quote, whose value begins with the site's address.
_SITE_ADDRESS_ATTR_RE = re.compile(
    r"""\b(?:href|src)\s*=\s*["']""" + re.escape(SITE_URL)
)

# gh-pages/ held 1,684 tracked HTML files when this floor was set on 2026-11-11.  It guards
# against a broken walk, not an inventory: do not raise it to the exact count.
_MIN_TRACKED_PAGES = 1000

# Pages, as paths below gh-pages/, that keep an href or src to the site's own address, each
# with the reason.
_PAGES_KEEPING_THE_SITE_ADDRESS: dict[str, str] = {
    "MAM-for-Sefaria/index.html": (
        "it quotes, link and all, the Version Notes value that MAM-for-Sefaria's CSV files"
        " carry to Sefaria's readers, off the site (py/mb_sefaria/sef_header.py)"
    ),
}


def _tracked_html_pages() -> list[str]:
    """Every tracked HTML file under gh-pages/, as its path below that prefix."""
    result = subprocess.run(
        ["git", "ls-files", "-z", "--", _PAGES_PREFIX],
        cwd=paths.repo_root(),
        capture_output=True,
        encoding="utf-8",
        check=True,
    )
    return sorted(
        entry[len(_PAGES_PREFIX) :]
        for entry in result.stdout.split("\0")
        if entry.endswith(".html")
    )


def test_no_page_links_the_site_by_its_address():
    """A link from a page of the site to the same site is relative."""
    pages = _tracked_html_pages()
    assert (
        len(pages) >= _MIN_TRACKED_PAGES
    ), f"only {len(pages)} tracked HTML files under {_PAGES_PREFIX}: wrong repo root?"
    gh_pages = paths.gh_pages_dir()
    findings = {}
    for page in pages:
        text = (gh_pages / page).read_text(encoding="utf-8")
        count = len(_SITE_ADDRESS_ATTR_RE.findall(text))
        if count and page not in _PAGES_KEEPING_THE_SITE_ADDRESS:
            findings[page] = count
    assert not findings, (
        f"page(s) linking the site by its address, {SITE_URL}, with the number of such"
        f" hrefs and srcs: {findings}. Have the page's generator compute a relative href"
        " with mb_cmn.site_links.site_href, or, if a reader meets the address off the"
        " site, list the page in _PAGES_KEEPING_THE_SITE_ADDRESS with the reason."
    )


def test_every_page_keeping_the_site_address_is_tracked():
    """The register names only pages that are still published."""
    stale = sorted(set(_PAGES_KEEPING_THE_SITE_ADDRESS) - set(_tracked_html_pages()))
    assert not stale, (
        "_PAGES_KEEPING_THE_SITE_ADDRESS names page(s) no longer tracked under"
        f" {_PAGES_PREFIX}: {stale}. Drop the entry, or repoint it at the page's new name;"
        " a register nothing prunes stops saying anything."
    )
