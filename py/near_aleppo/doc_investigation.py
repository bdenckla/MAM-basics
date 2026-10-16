"""Publish the maintained investigation with its images and usable source links.

The authored source stays in doc/. Relative repository evidence links become
GitHub links; image links and image bytes are published together. The source's
font URL already names the near-Aleppo documentation font.
"""

import posixpath
import re
from urllib.parse import quote, urlsplit

from mb_cmn import paths, provenance

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
    published = published.replace(
        "<!doctype html>",
        "<!doctype html>\n<!-- " + provenance.generated_html_comment(__file__) + " -->",
        1,
    )
    pages[PAGE] = published.encode("utf-8")
    return pages
