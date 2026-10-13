"""Mechanical lint for MAM-simple's HTML documentation and compatibility pointers."""

import re
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit

from mb_cmn import paths

ROOT = paths.repo_root()
SITE_ROOT = ROOT / "gh-pages"
DOC_ROOT = SITE_ROOT / "MAM-simple"
GUIDES = (
    "reading-mam-simple.html",
    "reading-mam-simple-xml.html",
    "reading-mam-simple-json.html",
    "versification-differences.html",
    "versification-and-cantillation.html",
)
SITE_PREFIX = "/MAM-basics/"
_VOID_TAGS = frozenset(
    {
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    }
)


class _Page(HTMLParser):
    def __init__(self, path, *, validate_markup=True):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.validate_markup = validate_markup
        self.ids = set()
        self.links = []
        self.stack = []
        self.feed(path.read_text(encoding="utf-8"))
        self.close()
        assert not self.stack, f"{path}: unclosed tags {self.stack}"

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if identifier := attrs.get("id"):
            if self.validate_markup:
                assert (
                    identifier not in self.ids
                ), f"{self.path}: duplicate id {identifier}"
            self.ids.add(identifier)
        for attr in ("href", "src"):
            if value := attrs.get(attr):
                self.links.append(value)
        if self.validate_markup and tag not in _VOID_TAGS:
            self.stack.append((tag, attrs))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in _VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if not self.validate_markup:
            return
        assert (
            self.stack and self.stack[-1][0] == tag
        ), f"{self.path}: unexpected </{tag}> at {self.getpos()}"
        self.stack.pop()

    def handle_data(self, data):
        if not self.validate_markup:
            return
        if not re.search(r"[\u05d0-\u05ea]", data):
            return
        cell_index = next(
            (i for i in range(len(self.stack) - 1, -1, -1) if self.stack[i][0] == "td"),
            None,
        )
        if cell_index is None:
            return
        cell = self.stack[cell_index][1]
        rtl_table = any(
            tag == "table" and attrs.get("dir") == "rtl" for tag, attrs in self.stack
        )
        # English prose cells keep LTR direction; Hebrew code labels are isolated.
        isolated_hebrew_in_english_cell = (
            cell.get("dir") == "ltr"
            and cell.get("lang") == "en"
            and any(
                tag == "bdi" and attrs.get("dir") == "rtl"
                for tag, attrs in self.stack[cell_index + 1 :]
            )
        )
        assert (
            cell.get("dir") == "rtl" or rtl_table or isolated_hebrew_in_english_cell
        ), f"{self.path}: Hebrew table text lacks RTL direction or isolation at {self.getpos()}"


def _local_target(source, url):
    parts = urlsplit(url)
    if parts.scheme or parts.netloc:
        if parts.netloc != "bdenckla.github.io" or not parts.path.startswith(
            SITE_PREFIX
        ):
            return None
        target = SITE_ROOT / unquote(parts.path.removeprefix(SITE_PREFIX))
    else:
        target = source.parent / unquote(parts.path) if parts.path else source
    if target.is_dir():
        target /= "index.html"
    return target.resolve(), unquote(parts.fragment)


def _check_link(source, url, pages):
    resolved = _local_target(source, url)
    if resolved is None:
        return
    target, fragment = resolved
    assert target.is_file(), f"{source}: missing target for {url}: {target}"
    if fragment:
        assert target.suffix == ".html", f"{source}: unsupported fragment target {url}"
        if target not in pages:
            pages[target] = _Page(target, validate_markup=False)
        assert fragment in pages[target].ids, f"{source}: missing fragment {url}"


def test_documentation_links_fragments_assets_and_rtl():
    required = [DOC_ROOT / name for name in ("index.html", *GUIDES)]
    assert all(
        path.is_file() for path in required
    ), "MAM-simple documentation is incomplete"
    pages = {path.resolve(): _Page(path) for path in required}
    for path in required:
        for url in pages[path.resolve()].links:
            _check_link(path, url, pages)
    stylesheets = tuple(DOC_ROOT.glob("*.css"))
    assert stylesheets, "No MAM-simple documentation stylesheets"
    for stylesheet in stylesheets:
        text = stylesheet.read_text(encoding="utf-8")
        for match in re.finditer(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)", text):
            _check_link(stylesheet, match[1], pages)
    pointers = tuple((ROOT / "MAM-simple" / "doc").glob("*.md"))
    assert pointers, "No MAM-simple compatibility pointers"
    for pointer in (*pointers, ROOT / "MAM-simple" / "README.md"):
        for url in re.findall(
            r"\]\((https://bdenckla\.github\.io/MAM-basics/[^)]+)\)",
            pointer.read_text(encoding="utf-8"),
        ):
            _check_link(pointer, url, pages)
