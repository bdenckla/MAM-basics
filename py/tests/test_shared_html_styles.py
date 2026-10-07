"""Mechanical lint for the published stylesheet and font dependency graph."""

from html.parser import HTMLParser
import re
from urllib.parse import unquote, urlsplit

from mb_cmn import paths

_PROSE_SHEETS = (
    "style.css",
    "MAM-parsed/style.css",
    "MAM-with-doc/misc/style.css",
    "MAM-with-doc/misc/aliyot-styles.css",
    "book-of-job/style.css",
    "near-aleppo/style.css",
    "phonetic-mam/style.css",
    "yeivin-itm/style.css",
    "wlc/style.css",
    "uxlc/style.css",
    "MAM-simple/versification-and-cantillation.css",
)
_REPORT_SHEETS = (
    "holman/table_data_findings.css",
    "holman/uxlc_corrections.css",
    "MAM-with-doc/change-log/style.css",
)
_CSS_URL = re.compile(r"""url\(\s*(?:"([^"]*)"|'([^']*)'|([^\s)'";]+))\s*\)""")


class _Stylesheets(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "link" and "stylesheet" in attrs.get("rel", "").lower().split():
            self.hrefs.append(attrs["href"])


def _local_target(source, reference, root):
    url = urlsplit(reference)
    if url.scheme or url.netloc:
        return None
    assert url.path, f"Empty asset path in {source}: {reference!r}"
    target = (source.parent / unquote(url.path)).resolve()
    assert target.is_relative_to(root), f"Asset leaves the publish tree: {target}"
    assert target.is_file(), f"Missing asset from {source}: {reference}"
    return target


def test_published_stylesheet_and_font_dependencies():
    root = paths.gh_pages_dir().resolve()
    pages = sorted(root.rglob("*.html"))
    assert pages, "The published HTML tree is missing or empty"
    common = root / "document.css"
    assert common.is_file()
    report_base = root / "report.css"
    assert report_base.is_file()
    families = (
        (common, {root / name for name in _PROSE_SHEETS}),
        (report_base, {root / name for name in _REPORT_SHEETS}),
    )
    sheets = set()
    for page in pages:
        parser = _Stylesheets()
        parser.feed(page.read_text(encoding="utf-8"))
        targets = [
            target
            for href in parser.hrefs
            if (target := _local_target(page, href, root)) is not None
        ]
        sheets.update(targets)
        for base, family_sheets in families:
            if extensions := family_sheets.intersection(targets):
                assert base in targets, f"Missing shared base {base.name}: {page}"
                assert all(
                    targets.index(base) < targets.index(extension)
                    for extension in extensions
                ), f"Family styles load before the shared base: {page}"
    assert sheets, "Published HTML declares no local stylesheets"
    for sheet in sheets:
        css = re.sub(r"/\*.*?\*/", "", sheet.read_text(encoding="utf-8"), flags=re.S)
        for match in _CSS_URL.finditer(css):
            reference = next(value for value in match.groups() if value is not None)
            _local_target(sheet, reference, root)
