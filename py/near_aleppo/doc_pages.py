"""Divide documentation sections among eight linked pages.

Each identified heading has one explicit owner; a new or missing identifier
fails generation. Sections retain their text, figures and assets. Local links
are routed to their owners, and section-links.js preserves old overview anchors.
"""

import copy
import json
import urllib.parse

from near_aleppo import doc_page
from near_aleppo.doc_html import link
from mb_misc import mb_html

_PAGES = {
    "index.html": ("The near-Aleppo dataset", ("what-the-dataset-is",)),
    "reading-json.html": (
        "Near-Aleppo JSON reference",
        (
            "reading-the-json",
            "templates",
            "own-templates",
            "gav-display",
            "added-parameters",
            "characters",
            "consumer-notice",
        ),
    ),
    "editorial-policies.html": (
        "Editorial policies",
        (
            "what-the-dataset-changes",
            "qamats-size",
            "divine-name-holam",
            "divine-title-holam",
            "elohim-vowel",
            "revia-mugrash",
            "ole-and-yored",
            "ketiv-qere-apparatus",
            "maqaf",
            "hataf",
            "stress-helpers",
            "codex-readings",
            "pointed-ketiv",
            "kept-as-mam-has-it",
            "not-represented",
        ),
    ),
    "coverage-and-status.html": (
        "Coverage and limitations",
        ("where-the-codex-survives", "limitations", "pending", "manual-task"),
    ),
    "choices.html": ("Choices and alternatives", ("choices",)),
    "ketiv-qere-mobile-he.html": ("Mobile he and the patah", ("mobile-he",)),
    "ketiv-qere-daniel.html": (
        "Ketiv/qere cases in Daniel",
        ("daniel-final-sheva", "daniel-yod-vav"),
    ),
    "ketiv-qere-genesis-43-28.html": ("Genesis 43:28", ("genesis-pointed-ketiv",)),
}
_SINGLE_CASE_PAGES = {
    "ketiv-qere-mobile-he.html",
    "ketiv-qere-genesis-43-28.html",
}
_CASE_PAGES = _SINGLE_CASE_PAGES | {"ketiv-qere-daniel.html"}
_SCRIPT = "section-links.js"


def _owners():
    owners = {}
    for path, (_, identifiers) in _PAGES.items():
        for identifier in identifiers:
            if identifier in owners:
                raise AssertionError(f"section has two owners: {identifier}")
            owners[identifier] = path
    return owners


_OWNERS = _owners()


def _sections(body):
    """Split only at the documentation's explicitly owned heading identifiers."""
    sections = {}
    current = None
    for node in body:
        if isinstance(node, dict) and node["_htel_tag"] in ("h2", "h3"):
            identifier = (node.get("attr") or {}).get("id")
            if identifier:
                if identifier not in _OWNERS or identifier in sections:
                    raise AssertionError(f"unexpected section: {identifier}")
                current = sections[identifier] = []
        if current is not None:
            current.append(node)
    if set(sections) != set(_OWNERS):
        raise AssertionError(f"missing sections: {set(_OWNERS) - set(sections)}")
    return sections


def _heading_text(section):
    return section[0]["contents"]


def _navigation():
    contents = []
    for path, (title, _) in _PAGES.items():
        if contents:
            contents.append(" · ")
        contents.append(link("Overview" if path == "index.html" else title, path))
    return mb_html.htel_mk(
        "nav",
        attr={"aria-label": "Documentation"},
        flex_contents=mb_html.para(contents),
    )


def _contents(identifiers, sections):
    return [
        mb_html.para("Contents:"),
        mb_html.unordered_list(
            [link(_heading_text(sections[ident]), "#" + ident) for ident in identifiers]
        ),
    ]


def _overview_extra():
    return [
        mb_html.heading_level_2("Documentation"),
        mb_html.unordered_list(
            [
                link(title, path)
                for path, (title, _) in _PAGES.items()
                if path != "index.html"
            ]
        ),
    ]


def _route_links(node, current_page):
    """Route existing local section links without touching assets or edition URLs."""
    if isinstance(node, str) or mb_html.is_raw_html(node):
        return
    attrs = node.get("attr") or {}
    if node["_htel_tag"] == "a" and (href := attrs.get("href")):
        address = urllib.parse.urlsplit(href)
        if (
            not address.scheme
            and not address.netloc
            and address.path in ("", "index.html")
        ):
            if address.fragment:
                identifier = urllib.parse.unquote(address.fragment)
                owner = _OWNERS[identifier]
                attrs["href"] = (
                    ("" if owner == current_page else owner) + "#" + identifier
                )
    for child in node.get("contents") or ():
        _route_links(child, current_page)


def pages(numbers):
    """Return each documentation page's title and body, plus its redirect script."""
    _, original = doc_page.page(numbers)
    sections = _sections(original)
    pages = {}
    for path, (title, identifiers) in _PAGES.items():
        body = [mb_html.heading_level_1(title)]
        if path == "index.html":
            body.append(copy.deepcopy(original[1]))
        else:
            body.append(_navigation())
            if len(identifiers) > 1:
                body += _contents(identifiers, sections)
        for identifier in identifiers:
            nodes = copy.deepcopy(sections[identifier])
            if path in {"index.html", "choices.html"}:
                # Run straight from the introduction, keeping the old fragment
                # on the first paragraph without a redundant heading and rule.
                nodes = nodes[1:]
                nodes[0]["attr"] = {"id": identifier}
            if path in _CASE_PAGES:
                for node in nodes:
                    if isinstance(node, dict) and node["_htel_tag"] == "h3":
                        node["_htel_tag"] = "h2"
            if path in _SINGLE_CASE_PAGES:
                nodes[0]["_htel_tag"] = "h1"
                body = [nodes[0], _navigation(), *nodes[1:]]
            else:
                body += nodes
        if path == "index.html":
            body += _overview_extra()
            body.append(
                mb_html.htel_mk("script", attr={"src": _SCRIPT, "defer": "defer"})
            )
        if path in _CASE_PAGES:
            body.append(
                mb_html.para(
                    link(
                        "General policy for the pointed ketiv",
                        "editorial-policies.html#pointed-ketiv",
                    )
                )
            )
        for node in body:
            _route_links(node, path)
        pages[path] = (title, body)
    return pages


def redirect_script(comment):
    routes = {
        ident: path + "#" + ident
        for ident, path in _OWNERS.items()
        if path != "index.html"
    }
    return (
        f"// {comment}\n"
        "(() => {\n"
        f"  const routes = {json.dumps(routes, indent=2, ensure_ascii=True)};\n"
        "  function followSection() {\n"
        "    let identifier;\n"
        "    try { identifier = decodeURIComponent(location.hash.slice(1)); }\n"
        "    catch { return; }\n"
        "    if (Object.hasOwn(routes, identifier)) location.replace(routes[identifier]);\n"
        "  }\n"
        "  followSection();\n"
        "  window.addEventListener('hashchange', followSection);\n"
        "})();\n"
    )


def script_name():
    return _SCRIPT
