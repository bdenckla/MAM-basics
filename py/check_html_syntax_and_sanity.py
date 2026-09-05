#!/usr/bin/env python3
"""
Lint the generated HTML files in gh-pages/.

Checks performed:
  1. HTML5 structure: doctype, <html lang="en">, <meta charset="utf-8">
  2. Broken internal links: href targets resolve to actual files
  3. Broken fragment links: #id targets exist in the referenced file
  4. Broken local image references: <img src="..."> files exist on disk
  5. Orphan images: files in img/ not referenced from any HTML
  6. CSS class validation: class values are defined in style.css
  7. Font file existence: woff2 font files referenced from CSS exist
  8. Stale files: unexpected files (e.g., extensionless, 0-byte)
  9. Duplicate IDs: no duplicate id attributes within a single file
 10. Orphan HTML: HTML files not linked from any other HTML file
 11. W3C Nu HTML conformance (optional, via --w3c flag)

Exit codes:
  0 - No issues found
  1 - Issues found

Usage:
    python check_html_syntax_and_sanity.py [pages_dir] [--w3c]

If no pages_dir given, defaults to book-of-job's own gh-pages tree
(boj_paths.gh_pages_dir()), whatever the working directory.
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

import boj_paths


def main(argv=None):
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
    # The default was the cwd-relative "gh-pages", which check_all.py always took.
    docs_dir = Path(args.pages_dir) if args.pages_dir else boj_paths.gh_pages_dir()

    if not docs_dir.is_dir():
        print(f"Error: {docs_dir} is not a directory", file=sys.stderr)
        return 1

    # Discover HTML and CSS files
    html_files = sorted(docs_dir.rglob("*.html"))
    css_files = sorted(docs_dir.rglob("*.css"))

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

    # Build internal-hrefs map for orphan-HTML check
    all_internal_hrefs: dict[Path, list[tuple[str | None, str | None]]] = {}
    for hf, info in parsed.items():
        all_internal_hrefs[hf] = info.internal_hrefs

    # Collect CSS classes from all CSS files
    css_classes: set[str] = set()
    for cf in css_files:
        css_classes |= _extract_css_classes(cf)

    # Run checks
    all_issues: list[str] = []
    referenced_images: set[Path] = set()

    for hf in html_files:
        info = parsed[hf]
        rel = str(hf.relative_to(docs_dir))
        html_dir = hf.parent

        all_issues.extend(_check_structure(rel, info))
        all_issues.extend(_check_duplicate_ids(rel, info))
        all_issues.extend(_check_internal_links(rel, info, html_dir, all_ids))
        all_issues.extend(_check_images(rel, info, html_dir, referenced_images))
        all_issues.extend(_check_css_classes(rel, info, css_classes))
        all_issues.extend(_check_css_links(rel, info, html_dir))

    # Cross-file checks
    for cf in css_files:
        all_issues.extend(_check_font_files(cf, docs_dir))
    all_issues.extend(_check_orphan_images(docs_dir, referenced_images))
    all_issues.extend(_check_stale_files(docs_dir))
    all_issues.extend(_check_orphan_html(docs_dir, html_files, all_internal_hrefs))

    # Optional W3C conformance check
    if args.w3c:
        print("Running W3C Nu HTML Checker ...")
        all_issues.extend(_check_w3c(html_files, docs_dir, strict=args.w3c_strict))

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
            if "#" in href:
                path_part, frag = href.split("#", 1)
                self.internal_hrefs.append((path_part or None, frag))
            else:
                self.internal_hrefs.append((href, None))


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
) -> list[str]:
    """Check internal hrefs resolve to files, and fragments to IDs."""
    issues = []
    for path_part, fragment in info.internal_hrefs:
        if path_part is not None:
            target_path = (html_dir / path_part).resolve()
            if not target_path.is_file():
                issues.append(f'{rel}: broken link to "{path_part}"')
                continue
            # Check fragment in target file
            if fragment is not None:
                target_ids = all_ids.get(target_path, [])
                if fragment not in target_ids:
                    issues.append(
                        f"{rel}: broken fragment #{fragment}" f' in "{path_part}"'
                    )
        else:
            # Fragment-only link (#foo) — check in same file
            if fragment is not None:
                same_path = (html_dir / rel).resolve()
                target_ids = all_ids.get(same_path, [])
                if fragment not in target_ids:
                    issues.append(f"{rel}: broken fragment #{fragment}" " (same-file)")
    return issues


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
        img_path = (html_dir / src).resolve()
        referenced_images.add(img_path)
        if not img_path.is_file():
            issues.append(f'{rel}: broken image "{src}"')
    return issues


def _check_orphan_images(
    docs_dir: Path,
    referenced_images: set[Path],
) -> list[str]:
    """Find image files not referenced from any HTML."""
    issues = []
    for img_dir in _find_img_dirs(docs_dir):
        for img_file in sorted(img_dir.rglob("*")):
            if img_file.is_file() and img_file.resolve() not in referenced_images:
                rel = img_file.relative_to(docs_dir)
                issues.append(f"orphan image: {rel}")
    return issues


def _find_img_dirs(docs_dir: Path) -> list[Path]:
    """Find all img/ subdirectories under docs_dir."""
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
        css_path = (html_dir / href).resolve()
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


def _check_stale_files(docs_dir: Path) -> list[str]:
    """Flag unexpected files: 0-byte, extensionless, etc."""
    issues = []
    expected_exts = {".html", ".css", ".png", ".jpg", ".jpeg", ".woff2"}
    for path in sorted(docs_dir.rglob("*")):
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
    all_internal_hrefs: dict[Path, list[tuple[str | None, str | None]]],
) -> list[str]:
    """Find HTML files not linked from any other HTML file."""
    # Collect the set of HTML files that are linked to
    linked_targets: set[Path] = set()
    for source_path, hrefs in all_internal_hrefs.items():
        source_dir = source_path.parent
        for path_part, _frag in hrefs:
            if path_part is not None:
                target = (source_dir / path_part).resolve()
                linked_targets.add(target)
    # Entry point is index.html — it doesn't need to be linked to
    index_path = (docs_dir / "index.html").resolve()
    issues = []
    for html_file in sorted(html_files):
        resolved = html_file.resolve()
        if resolved == index_path:
            continue
        if resolved not in linked_targets:
            rel = html_file.relative_to(docs_dir)
            issues.append(f"orphan HTML (not linked from any page): {rel}")
    return issues


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
