#!/usr/bin/env python3
"""
Lint the generated HTML files in gh-pages/.

Checks performed:
  1. HTML5 structure: doctype, <html lang="en">, <meta charset="utf-8">
  2. Broken internal links: href targets resolve to actual files
  3. Broken fragment links: #id targets exist in the referenced file
  4. Broken local image references: <img src="..."> files exist on disk
  5. Orphan images: files in img/ not referenced from any HTML
  6. CSS class inventory: undefined class values are reported but are not fatal
  7. Font file existence: woff2 font files referenced from CSS exist
  8. Stale files: unexpected files (e.g., extensionless, 0-byte)
  9. Duplicate IDs: no duplicate id attributes within a single file
 10. Orphan HTML: HTML files that no page of the sub-site, and no page directly at the
     deploy root, links
 11. W3C Nu HTML conformance (optional, via --w3c flag)

Exit codes:
  0 - No issues found
  1 - Issues found

Usage:
    python check_html_syntax_and_sanity.py [pages_dir] [--deploy-root] [--w3c]

If no pages_dir given, defaults to book-of-job's own gh-pages tree
(boj_paths.gh_pages_dir()), whatever the working directory.
The repository's multi-site ``gh-pages/`` root is accepted only through the explicit
``--deploy-root`` mode. That mode checks the HTML and CSS files directly at the deploy
root, however many there are, and runs the stale-file check over every file at that
level. It folds no sub-site's pages or CSS vocabulary into the root, although a root
page's link into a sub-site must still resolve.
Without ``--deploy-root``, the root is refused and one sub-site is checked recursively.
The orphan-HTML check alone also reads the pages directly at the deploy root, such as
the site index, because they link into the sub-sites.
Undefined CSS classes are informational because the current ownership model cannot
distinguish a shared or external CSS vocabulary from a defect.
The --w3c flag sends each HTML file to the W3C Nu HTML Checker API
for full conformance validation (requires internet access).
"""

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

import boj_paths
from mb_cmn import paths
from mb_cmn import site_links

# The published site's own address.  Until 2026-11-11 the site index linked into the
# sub-sites by absolute URLs below it, and _linked_targets still reads such a URL as the file
# it serves.  Links within the site are relative now (mb_cmn/site_links.py), and
# py/tests/test_site_links_relative.py keeps them so.
_SITE_URL = site_links.SITE_URL

# Pages that no page of the site links by design, because they are kept for links from
# outside it: each path below the deploy root, with the reason it stays.  The orphan-HTML
# check exempts them and reports an entry whose page is gone.  Ben, 2026-11-10, of the
# first entry: "can you make this a known exception?"
_PAGES_FOR_OUTSIDE_LINKS = {
    "MAM-with-doc/tsinnorit_oleh/tsinnorit_and_oleh_on_ivs.html": (
        "a moved-page stub kept at its old URL, which Unicode's L2/25-242,"
        " https://www.unicode.org/L2/L2025/25242-hebrew-accents.pdf, links"
    ),
    "post-stress-meteg.html": (
        "the forwarding stub left at the main post-stress-meteg page's address when the"
        " pages moved into post-stress-meteg/ on 2026-11-11, the one page of theirs that Ben"
        " thought might be linked from outside the site"
    ),
    "post-stress-meteg-post-silluq-1s17v5.html": (
        "the forwarding stub left at the address of the 1 Samuel 17:5 post-silluq case page"
        " when the pages moved into post-stress-meteg/ on 2026-11-11, an address that"
        " MAM-private's review of BHL Appendix A links"
    ),
    "stress-helpers/koren.html": "the old address of the Koren stress-helper report",
    "stress-helpers/simanim-tanakh.html": (
        "the old address of the Feldheim Simanim Tanakh stress-helper report"
    ),
    # The seven CLC stubs that py/clc/clc_index.py's write_legacy_redirects writes.  Ben,
    # 2026-11-11, of a report recommending these entries: "I authorize you to do those
    # improvements you recommend."
    **{
        f"uxlc/clc/{name}": (
            "a stub that py/main_clc.py all writes at the address this CLC page had from"
            " 2026-09-03 until its move to clc/ on 2026-10-08; UXLC-utils' frozen redirect"
            " stubs (in/uxlc_utils_redirect_pages.json) forward the page's older address"
            " here, so py/tests/test_redirect_manifest.py requires it"
        )
        for name in (
            "Genesis.html",
            "Exodus-20.html",
            "Exodus-20-long-notes.html",
            "Deuter-5.html",
            "Deuter-5-long-notes.html",
            "2Samuel.html",
            "Proverbs.html",
        )
    },
}


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")
    parser = argparse.ArgumentParser(
        description="Lint the generated HTML files in gh-pages/.",
    )
    parser.add_argument(
        "pages_dir",
        nargs="?",
        default=None,
        help="path to the Pages directory (default: book-of-job's own gh-pages)",
    )
    parser.add_argument(
        "--deploy-root",
        action="store_true",
        help="check only HTML and CSS files directly under MAM-basics' deploy root",
    )
    parser.add_argument(
        "--w3c",
        action="store_true",
        help="also validate each file via the W3C Nu HTML Checker API",
    )
    parser.add_argument(
        "--w3c-strict",
        action="store_true",
        help="with --w3c, show all messages (don't suppress known issues)",
    )
    args = parser.parse_args(argv)
    deploy_root = paths.gh_pages_dir().resolve()
    if args.deploy_root:
        docs_dir = Path(args.pages_dir) if args.pages_dir else deploy_root
        if docs_dir.resolve() != deploy_root:
            print(
                f"Error: --deploy-root requires MAM-basics' deploy root: {deploy_root}",
                file=sys.stderr,
            )
            return 2
    else:
        # The default was the cwd-relative "gh-pages", which check_all.py always took.
        docs_dir = Path(args.pages_dir) if args.pages_dir else boj_paths.gh_pages_dir()

    if not args.deploy_root and docs_dir.resolve() == deploy_root:
        print(
            "Error: use --deploy-root for MAM-basics' multi-site gh-pages root, or"
            f" use {boj_paths.gh_pages_dir()} for the Book-of-Job checks",
            file=sys.stderr,
        )
        return 2

    if not docs_dir.is_dir():
        print(f"Error: {docs_dir} is not a directory", file=sys.stderr)
        return 1

    # A sub-site is one recursive document tree. The deploy root is only the files
    # directly at that level; every directory below it is a separate sub-site.
    recursive = not args.deploy_root
    html_files = sorted(
        docs_dir.rglob("*.html") if recursive else docs_dir.glob("*.html")
    )
    css_files = sorted(docs_dir.rglob("*.css") if recursive else docs_dir.glob("*.css"))

    if not html_files:
        print(f"No HTML files found in {docs_dir}")
        return 0

    # Parse all HTML files
    parsed: dict[Path, _HTMLInfo] = {}
    for hf in html_files:
        parsed[hf] = _parse_html(hf)

    # Build ID map (resolved path → list of IDs)
    all_ids: dict[Path, list[str]] = {}
    for hf, info in parsed.items():
        all_ids[hf.resolve()] = info.ids

    # The pages whose links the orphan-HTML check counts: the sub-site's, and those
    # directly at the deploy root, the site index among them.
    linkers: dict[Path, _HTMLInfo] = {hf.resolve(): info for hf, info in parsed.items()}
    for root_page in sorted(deploy_root.glob("*.html")):
        if root_page.resolve() not in linkers:
            linkers[root_page.resolve()] = _parse_html(root_page)

    # Collect CSS classes from all CSS files
    css_classes: set[str] = set()
    for cf in css_files:
        css_classes |= _extract_css_classes(cf)

    # Run checks
    all_issues: list[str] = []
    unknown_css_references: list[str] = []
    referenced_images: set[Path] = set()
    # The IDs of each page outside the checked pages that a fragment link reaches, parsed
    # once however many links reach it: hundreds of verse links reach one book's page.
    outside_ids: dict[Path, set[str]] = {}

    for hf in html_files:
        info = parsed[hf]
        rel = str(hf.relative_to(docs_dir))
        html_dir = hf.parent

        all_issues.extend(_check_structure(rel, info))
        all_issues.extend(_check_duplicate_ids(rel, info))
        all_issues.extend(
            _check_internal_links(rel, info, html_dir, all_ids, outside_ids)
        )
        all_issues.extend(_check_images(rel, info, html_dir, referenced_images))
        unknown_css_references.extend(_check_css_classes(rel, info, css_classes))
        all_issues.extend(_check_css_links(rel, info, html_dir))

    # Cross-file checks
    for cf in css_files:
        all_issues.extend(_check_font_files(cf, docs_dir))
    all_issues.extend(
        _check_orphan_images(docs_dir, referenced_images, recursive=recursive)
    )
    all_issues.extend(_check_stale_files(docs_dir, recursive=recursive))
    all_issues.extend(
        _check_orphan_html(
            docs_dir, html_files, linkers, deploy_root, recursive=recursive
        )
    )

    # Optional W3C conformance check
    if args.w3c:
        print("Running W3C Nu HTML Checker ...")
        all_issues.extend(_check_w3c(html_files, docs_dir, strict=args.w3c_strict))

    if unknown_css_references:
        print(
            "Informational: "
            f"{len(unknown_css_references)} undefined CSS class reference(s); "
            "not fatal until CSS ownership distinguishes shared/external classes."
        )

    # Report
    if all_issues:
        for issue in all_issues:
            print(issue)
        print(f"\nFound {len(all_issues)} issue(s).")
        return 1
    else:
        print("No HTML output issues found.")
        return 0


# ── HTML Parser ──────────────────────────────────────────────────────


class _HTMLInfo(HTMLParser):
    """Collect structural info from an HTML file."""

    def __init__(self):
        super().__init__()
        self.has_doctype = False
        self.html_lang = None
        self.has_meta_charset_utf8 = False
        self.css_hrefs = []  # stylesheet <link> hrefs
        self.internal_hrefs = []  # (href, fragment_or_None)
        self.external_hrefs = []  # full URLs
        self.img_srcs = []  # <img src="...">
        self.ids = []  # all id attribute values
        self.classes = []  # all class attribute values (split)
        self._in_head = False

    def handle_decl(self, decl):
        if decl.lower() == "doctype html":
            self.has_doctype = True

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if tag == "html":
            self.html_lang = attr_dict.get("lang")
        if tag == "head":
            self._in_head = True
        if tag == "meta":
            if attr_dict.get("charset", "").lower() == "utf-8":
                self.has_meta_charset_utf8 = True
        if tag == "link":
            if attr_dict.get("rel") == "stylesheet":
                href = attr_dict.get("href")
                if href:
                    self.css_hrefs.append(href)
            elif attr_dict.get("rel") == "icon":
                href = attr_dict.get("href")
                if href:
                    self._categorize_href(href)
        if tag == "a":
            href = attr_dict.get("href")
            if href:
                self._categorize_href(href)
        if tag == "img":
            src = attr_dict.get("src")
            if src:
                self.img_srcs.append(src)
        # Collect IDs
        id_val = attr_dict.get("id")
        if id_val:
            self.ids.append(id_val)
        # Collect classes
        class_val = attr_dict.get("class")
        if class_val:
            for cls in class_val.split():
                self.classes.append(cls)

    def handle_endtag(self, tag):
        if tag == "head":
            self._in_head = False

    def _categorize_href(self, href):
        if href.startswith(("http://", "https://", "mailto:")):
            self.external_hrefs.append(href)
        else:
            # The server percent-decodes the path to find the file, so a file whose
            # name has a space, like MAM-with-doc's "E1-Song of Songs.html", is linked
            # with %20 in its place.
            # A query selects page state; it is not part of the local filename.
            # Split before decoding so an encoded question mark remains in a path.
            parsed = urlsplit(href)
            fragment = parsed.fragment if "#" in href else None
            self.internal_hrefs.append((unquote(parsed.path) or None, fragment))


def _parse_html(path: Path) -> _HTMLInfo:
    info = _HTMLInfo()
    text = path.read_text(encoding="utf-8")
    info.feed(text)
    return info


# ── CSS Parser (minimal) ─────────────────────────────────────────────


def _extract_css_classes(css_path: Path) -> set[str]:
    """Extract class names from CSS selectors (e.g., .foo, tag.foo)."""
    text = css_path.read_text(encoding="utf-8")
    # Match .classname in selectors (before the { block)
    classes = set()
    for m in re.finditer(r"\.([a-zA-Z_][\w-]*)", text):
        classes.add(m.group(1))
    return classes


def _extract_css_font_urls(css_path: Path) -> list[str]:
    """Extract url("...") references from CSS."""
    text = css_path.read_text(encoding="utf-8")
    urls = []
    for m in re.finditer(r'url\(["\']?([^"\'()]+)["\']?\)', text):
        urls.append(m.group(1))
    return urls


# ── Check Functions ──────────────────────────────────────────────────


def _check_structure(rel: str, info: _HTMLInfo) -> list[str]:
    """Check HTML5 structural requirements."""
    issues = []
    if not info.has_doctype:
        issues.append(f"{rel}: missing <!doctype html>")
    if info.html_lang != "en":
        issues.append(f"{rel}: <html> lang is {info.html_lang!r}, expected 'en'")
    if not info.has_meta_charset_utf8:
        issues.append(f'{rel}: missing <meta charset="utf-8">')
    return issues


def _check_duplicate_ids(rel: str, info: _HTMLInfo) -> list[str]:
    """Check for duplicate id attributes in a single file."""
    issues = []
    seen = {}
    for id_val in info.ids:
        if id_val in seen:
            seen[id_val] += 1
        else:
            seen[id_val] = 1
    for id_val, count in seen.items():
        if count > 1:
            issues.append(f'{rel}: duplicate id "{id_val}" ({count} times)')
    return issues


def _check_internal_links(
    rel: str,
    info: _HTMLInfo,
    html_dir: Path,
    all_ids: dict[Path, list[str]],
    outside_ids: dict[Path, set[str]],
) -> list[str]:
    """Check internal hrefs resolve to files, and fragments to IDs.

    ``outside_ids`` caches the IDs of pages outside ``all_ids``, filled as links reach them.
    """
    issues = []
    for path_part, fragment in info.internal_hrefs:
        if path_part is not None:
            target_path = (html_dir / path_part).resolve()
            if not target_path.is_file():
                issues.append(f'{rel}: broken link to "{path_part}"')
                continue
            # Check fragment in target file
            if fragment is not None:
                target_ids = all_ids.get(target_path)
                if target_ids is None and target_path.suffix.lower() == ".html":
                    if target_path not in outside_ids:
                        outside_ids[target_path] = set(_parse_html(target_path).ids)
                    target_ids = outside_ids[target_path]
                if target_ids is None:
                    target_ids = []
                if not _fragment_found(fragment, target_ids):
                    issues.append(
                        f"{rel}: broken fragment #{fragment}" f' in "{path_part}"'
                    )
        else:
            # Fragment-only link (#foo) — check in same file
            if fragment is not None:
                same_path = (html_dir / Path(rel).name).resolve()
                target_ids = all_ids.get(same_path, [])
                if not _fragment_found(fragment, target_ids):
                    issues.append(f"{rel}: broken fragment #{fragment}" " (same-file)")
    return issues


def _fragment_found(fragment: str, ids) -> bool:
    """Whether a browser finds ``fragment`` among ``ids``.  The HTML standard, "find a
    potential indicated element", tries the fragment as written and then its UTF-8
    percent-decoding, so an id with non-ASCII characters or parentheses may be linked either
    way.  Found 2026-11-11, when the links that the FOI pages' percent-encoded fragments
    reach became relative and so faced this check."""
    return fragment in ids or unquote(fragment) in ids


def _check_images(
    rel: str,
    info: _HTMLInfo,
    html_dir: Path,
    referenced_images: set[Path],
) -> list[str]:
    """Check local <img src="..."> targets exist; leave remote assets to the browser."""
    issues = []
    for src in info.img_srcs:
        if src.startswith(("http://", "https://", "data:")):
            continue
        # Decoded as an internal href's path is: the images under MAM-with-doc's misc/
        # have spaces in their names, so their srcs have %20 in their place.
        img_path = (html_dir / unquote(src)).resolve()
        referenced_images.add(img_path)
        if not img_path.is_file():
            issues.append(f'{rel}: broken image "{src}"')
    return issues


def _check_orphan_images(
    docs_dir: Path,
    referenced_images: set[Path],
    *,
    recursive: bool,
) -> list[str]:
    """Find image files not referenced from any HTML."""
    issues = []
    for img_dir in _find_img_dirs(docs_dir, recursive=recursive):
        for img_file in sorted(img_dir.rglob("*")):
            if img_file.is_file() and img_file.resolve() not in referenced_images:
                rel = img_file.relative_to(docs_dir)
                issues.append(f"orphan image: {rel}")
    return issues


def _find_img_dirs(docs_dir: Path, *, recursive: bool) -> list[Path]:
    """Find all img/ subdirectories under docs_dir."""
    if not recursive:
        return []
    return sorted(p for p in docs_dir.rglob("img") if p.is_dir())


def _check_css_classes(
    rel: str,
    info: _HTMLInfo,
    css_classes: set[str],
) -> list[str]:
    """Check that all class attributes reference classes defined in CSS."""
    issues = []
    for cls in info.classes:
        if cls not in css_classes:
            issues.append(f'{rel}: unknown CSS class "{cls}"')
    return issues


def _check_css_links(
    rel: str,
    info: _HTMLInfo,
    html_dir: Path,
) -> list[str]:
    """Check that stylesheet hrefs resolve to existing files."""
    issues = []
    for href in info.css_hrefs:
        # Decoded as an img src is, although no stylesheet's name has a space yet.
        css_path = (html_dir / unquote(href)).resolve()
        if not css_path.is_file():
            issues.append(f'{rel}: broken CSS link "{href}"')
    return issues


def _check_font_files(css_path: Path, docs_dir: Path) -> list[str]:
    """Check that font URLs referenced in CSS exist."""
    issues = []
    css_dir = css_path.parent
    rel = css_path.relative_to(docs_dir)
    for url in _extract_css_font_urls(css_path):
        font_path = (css_dir / url).resolve()
        if not font_path.is_file():
            issues.append(f'{rel}: broken font URL "{url}"')
    return issues


def _check_stale_files(docs_dir: Path, *, recursive: bool) -> list[str]:
    """Flag unexpected files: 0-byte, extensionless, etc."""
    issues = []
    # JSON is published as data, such as each FOI page's JSON output and the change log's
    # per-release diffs, and Markdown as a directory's provenance note or README.  Ben,
    # 2026-11-10: "please update the check's extension list".
    expected_exts = {
        ".html",
        ".css",
        ".js",
        ".json",
        ".md",
        ".txt",
        ".png",
        ".jpg",
        ".jpeg",
        ".woff2",
        ".svg",
    }
    paths_in_scope = docs_dir.rglob("*") if recursive else docs_dir.glob("*")
    for path in sorted(paths_in_scope):
        if not path.is_file():
            continue
        rel = path.relative_to(docs_dir)
        if path.suffix == "" and path.name != ".gitkeep":
            issues.append(f"stale file (no extension): {rel}")
        elif path.stat().st_size == 0 and path.suffix != "":
            issues.append(f"stale file (0 bytes): {rel}")
        elif path.suffix.lower() not in expected_exts:
            issues.append(f"unexpected file type: {rel}")
    return issues


def _check_orphan_html(
    docs_dir: Path,
    html_files: list[Path],
    linkers: dict[Path, _HTMLInfo],
    deploy_root: Path,
    *,
    recursive: bool,
) -> list[str]:
    """Find HTML files that no page of ``linkers`` links.

    ``linkers`` holds the sub-site's pages and the pages directly at the deploy root.
    Until 2026-11-10 only the sub-site's own pages counted, so a page that only the site
    index lists was reported as an orphan.  Ben, 2026-11-10, of five such pages: "can you
    change the scope or keep the scope but add these as particular exceptions?"  The
    sub-site's landing page and the pages that ``_PAGES_FOR_OUTSIDE_LINKS`` names are
    exempt.
    """
    linked_targets = _linked_targets(linkers, deploy_root)
    # Preserve the Yeivin product's canonical historical landing filename.
    # Every other site's directory landing remains index.html.
    landing = "index.html"
    if docs_dir.resolve() == (paths.gh_pages_dir() / "yeivin-itm").resolve():
        landing = "yeivin_itm.html"
    index_path = (docs_dir / landing).resolve()
    issues = []
    for html_file in sorted(html_files):
        resolved = html_file.resolve()
        if resolved == index_path:
            continue
        if _deploy_rel(resolved, deploy_root) in _PAGES_FOR_OUTSIDE_LINKS:
            continue
        if resolved not in linked_targets:
            rel = html_file.relative_to(docs_dir)
            issues.append(f"orphan HTML (not linked from any page): {rel}")
    # An entry whose page is gone would exempt nothing, silently.  A sub-site run checks the
    # entries below the sub-site, and a deploy-root run the entries directly at the root.
    scope = docs_dir.resolve()
    for rel in sorted(_PAGES_FOR_OUTSIDE_LINKS):
        page = (deploy_root / rel).resolve()
        in_scope = page.is_relative_to(scope) if recursive else page.parent == scope
        if in_scope and not page.is_file():
            issues.append(f"_PAGES_FOR_OUTSIDE_LINKS names a missing page: {rel}")
    return issues


def _linked_targets(linkers: dict[Path, _HTMLInfo], deploy_root: Path) -> set[Path]:
    """Every file that a page of ``linkers`` links, by relative path or by the site's URL.

    A site URL that ends in a slash names that directory's index.html, which is what the
    server sends for it.
    """
    targets = set()
    for source_path, info in linkers.items():
        for path_part, _frag in info.internal_hrefs:
            if path_part is not None:
                targets.add((source_path.parent / path_part).resolve())
        for href in info.external_hrefs:
            if href.startswith(_SITE_URL):
                # Split before decoding, as _categorize_href does.
                rel = unquote(urlsplit(href[len(_SITE_URL) :]).path)
                if rel == "" or rel.endswith("/"):
                    rel += "index.html"
                targets.add((deploy_root / rel).resolve())
    return targets


def _deploy_rel(path: Path, deploy_root: Path) -> str | None:
    """``path`` below the deploy root, with forward slashes, or None if outside it."""
    try:
        return path.relative_to(deploy_root).as_posix()
    except ValueError:
        return None


# ── W3C Nu HTML Checker ───────────────────────────────────────────────

_W3C_NU_URL = "https://validator.w3.org/nu/?out=json"
_W3C_DELAY_SECS = 1.0  # be polite to the public service

# Messages matching any of these substrings are suppressed by default.
# Use --w3c-strict to show them.
_W3C_SUPPRESS = [
    "element must have an",  # missing alt attribute (curly quotes vary)
    "Text run is not in Unicode Normalization Form C",
]


def _is_suppressed(text: str) -> bool:
    return any(pat in text for pat in _W3C_SUPPRESS)


def _check_w3c(
    html_files: list[Path], docs_dir: Path, *, strict: bool = False
) -> list[str]:
    """Validate each HTML file via the W3C Nu HTML Checker API."""
    issues = []
    suppressed_count = 0
    total = len(html_files)
    for i, hf in enumerate(html_files):
        rel = str(hf.relative_to(docs_dir))
        html_bytes = hf.read_bytes()
        print(f"  W3C checking [{i + 1}/{total}]: {rel} ...", flush=True)
        try:
            req = urllib.request.Request(
                _W3C_NU_URL,
                data=html_bytes,
                headers={
                    "Content-Type": "text/html; charset=utf-8",
                    "User-Agent": "check_html_syntax_and_sanity.py/1.0",
                },
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read())
        except (urllib.error.URLError, OSError) as exc:
            issues.append(f"{rel}: W3C check failed: {exc}")
            continue
        for msg in result.get("messages", []):
            msg_type = msg.get("type", "")
            if msg_type == "info" and msg.get("subType") != "warning":
                continue  # skip pure informational messages
            text = msg.get("message", "")
            if not strict and _is_suppressed(text):
                suppressed_count += 1
                continue
            line = msg.get("lastLine", "?")
            label = "error" if msg_type == "error" else "warning"
            issues.append(f"{rel}:{line}: W3C {label}: {text}")
        if i < total - 1:
            time.sleep(_W3C_DELAY_SECS)
    if suppressed_count:
        print(
            f"  ({suppressed_count} suppressed W3C messages;"
            " use --w3c-strict to show all)"
        )
    return issues


if __name__ == "__main__":
    sys.exit(main())
