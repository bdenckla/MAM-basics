"""Publish the maintained investigation with its images and usable source links.

The authored source stays in doc/. Relative repository evidence links become
GitHub links; image links and image bytes are published together. The source's
one font URL names the site's one copy of Taamey D, gh-pages/woff2/Taamey_D.woff2,
relative to doc/; publishing rewrites it relative to the published page.
"""

import posixpath
import re
from urllib.parse import quote, urlsplit

from mb_cmn import paths, provenance
from near_aleppo import build_paths
from py_html import taamey_d_assets

PAGE = "avi-ketiv-investigation.html"
_SOURCE = "doc/near-aleppo-avi-ketiv-investigation.html"
_GITHUB = "https://github.com/bdenckla/MAM-basics/blob/main/"


def render():
    """Return the published HTML and unchanged evidence images as bytes."""
    root = paths.repo_root()
    source = (root / _SOURCE).read_text(encoding="utf-8")
    pages = {}

    def address(match):
        attribute, value = match.groups()
        url = urlsplit(value)
        if url.scheme or url.netloc or not url.path:
            return match[0]
        target = posixpath.normpath(posixpath.join("doc", url.path))
        if target.startswith("../") or not (root / target).is_file():
            raise ValueError(f"Investigation link has no repository file: {value}")
        if target.startswith("in/near-aleppo/img/"):
            destination = "img/" + target.removeprefix("in/near-aleppo/img/")
            pages[destination] = (root / target).read_bytes()
        elif attribute == "src":
            raise ValueError(f"Unexpected investigation image: {value}")
        elif target == "doc/sigil-decoding.md":
            destination = "../MAM-with-doc/sigil-decoding.html"
        else:
            destination = _GITHUB + quote(target)
        if url.fragment:
            destination += "#" + url.fragment
        return f'{attribute}="{destination}"'

    published = re.sub(r'\b(href|src)="([^"]+)"', address, source)
    published = _republish_font_url(published)
    published = published.replace(
        "<!doctype html>",
        "<!doctype html>\n<!-- " + provenance.generated_html_comment(__file__) + " -->",
        1,
    )
    pages[PAGE] = published.encode("utf-8")
    return pages


def _republish_font_url(text):
    """Rewrite the source's one CSS url(), the site font's, for the published page."""
    font = "gh-pages/" + taamey_d_assets.FONT
    page_dir = posixpath.dirname(
        (build_paths.html_pages_dir() / PAGE).relative_to(paths.repo_root()).as_posix()
    )

    def rewrite(match):
        target = posixpath.normpath(posixpath.join("doc", match[1]))
        if target != font or not (paths.repo_root() / font).is_file():
            raise ValueError(f"Unexpected investigation stylesheet URL: {match[1]}")
        return f'url("{posixpath.relpath(font, page_dir)}")'

    published, count = re.subn(r'url\("([^"]+)"\)', rewrite, text)
    if count != 1:
        raise ValueError(f"Expected one stylesheet URL in {_SOURCE}, found {count}")
    return published
