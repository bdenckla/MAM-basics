"""Closed display documents for the five existing public example pages.

Only parsed public HTML contributes to this format. Adjacent text is coalesced,
so source-code string boundaries cannot become a second annotation channel.
The calculation inputs and source-specific test fixtures are not release data.
"""

import json
import re
from html.parser import HTMLParser

from phonetic_mam.display_schema import PublicReleaseError, require
from py_html import legacy_html
from py_html.forbidden_phonetic_marks import refuse_forbidden_phonetic_marks

SCHEMA_ID = "phonetic-mam-tests-v1"
PAGE_NAMES = (
    "testsuites.html",
    "testsuite-jacobson-not-interesting.html",
    "testsuite-jacobson-likely-typos.html",
    "testsuite-jacobson-more-serious-than-typos.html",
    "testsuite-misc.html",
)
IMAGE_NAMES = (
    "Jacobson-page-243-ultrashort-vs-normalshort.png",
    "Jacobson-page-273-mimmaḥorat-1-of-2.png",
    "Jacobson-page-273-mimmaḥorat-2-of-2.png",
    "Jacobson-page-275-exceptions-to-the-phonological-1-of-2.png",
    "Jacobson-page-275-exceptions-to-the-phonological-2-of-2.png",
)
_PLAIN_TAGS = frozenset(
    ("table", "tr", "ul", "li", "p", "div", "h1", "sup", "br", "hr")
)
_INLINE_TAGS = frozenset(("span", "sup", "a"))


def _attributes(tag, attributes):
    require(isinstance(attributes, dict), "display attributes must be an object")
    if tag in _PLAIN_TAGS:
        require(not attributes, "unexpected plain-element attributes")
    elif tag == "td":
        require(attributes in ({}, {"dir": "rtl"}), "unexpected cell attributes")
    elif tag == "span":
        require(
            attributes
            in (
                {"class": "jt-stressed"},
                {"class": "romanized"},
                {"lang": "hbo"},
                {"lang": "hbo", "class": "pre-or-post"},
            ),
            "unexpected inline attributes",
        )
    elif tag in ("h2", "h3"):
        require(
            attributes == {}
            or (
                set(attributes) == {"id"}
                and isinstance(attributes["id"], str)
                and re.fullmatch(r"note-[0-9]+-[0-9]+", attributes["id"])
            ),
            "unexpected note heading",
        )
    elif tag == "a":
        require(set(attributes) == {"href"}, "unexpected link attributes")
        href = attributes["href"]
        require(
            isinstance(href, str)
            and (href in PAGE_NAMES or re.fullmatch(r"#note-[0-9]+-[0-9]+", href)),
            "unexpected example link",
        )
    elif tag == "img":
        require(
            set(attributes) == {"src"}
            and attributes["src"] in ["img/" + name for name in IMAGE_NAMES],
            "unexpected image",
        )
    else:
        raise PublicReleaseError(f"unknown example display tag: {tag}")


def _validate_nodes(nodes):
    require(isinstance(nodes, list), "display children must be an array")
    was_text = False
    for node in nodes:
        if isinstance(node, str):
            require(bool(node) and "\n" not in node, "noncanonical display text")
            require(not was_text, "adjacent display text is not coalesced")
            refuse_forbidden_phonetic_marks(node, "example display text")
            was_text = True
            continue
        was_text = False
        require(
            isinstance(node, dict) and set(node) == {"tag", "attributes", "children"},
            "unknown display-node fields",
        )
        _attributes(node["tag"], node["attributes"])
        if node["tag"] in ("br", "hr", "img"):
            require(node["children"] == [], "void display element has children")
        else:
            _validate_nodes(node["children"])


def validate(payload):
    """Require all five pages and only their closed display vocabulary."""
    require(
        isinstance(payload, dict) and set(payload) == {"schema", "pages"},
        "example schema shape",
    )
    require(payload["schema"] == SCHEMA_ID, "unknown example schema")
    pages = payload["pages"]
    require(
        isinstance(pages, list) and len(pages) == len(PAGE_NAMES),
        "missing example pages",
    )
    names = []
    for page in pages:
        require(
            isinstance(page, dict) and set(page) == {"filename", "title", "body"},
            "example page shape",
        )
        names.append(page["filename"])
        require(
            isinstance(page["title"], str) and bool(page["title"]), "missing page title"
        )
        refuse_forbidden_phonetic_marks(page["title"], "example page title")
        require(bool(page["body"]), "empty example page")
        _validate_nodes(page["body"])
    require(tuple(names) == PAGE_NAMES, "example page order or identities differ")
    return payload


def canonical_bytes(payload):
    validate(payload)
    return (
        json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n"
    ).encode("utf-8")


class _DisplayParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.body = []
        self.stack = []
        self.in_body = False
        self.in_title = False
        self.title = ""

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        require(len(attributes) == len(attrs), "duplicate HTML attribute")
        if tag == "body":
            require(not attrs and not self.in_body, "unexpected body")
            self.in_body = True
        elif tag == "title":
            self.in_title = True
        elif self.in_body:
            _attributes(tag, attributes)
            node = {"tag": tag, "attributes": attributes, "children": []}
            self._children().append(node)
            if tag not in ("br", "hr"):
                self.stack.append(node)

    def _children(self):
        return self.stack[-1]["children"] if self.stack else self.body

    def handle_data(self, text):
        if self.in_title:
            self.title += text
        elif self.in_body:
            children = self._children()
            if text.startswith("\n") and (
                not children
                and (
                    not self.stack
                    or self.stack[-1]["tag"] in ("table", "tr", "ul", "div", "img")
                )
                or children
                and isinstance(children[-1], dict)
                and children[-1]["tag"] not in _INLINE_TAGS | {"br", "hr"}
            ):
                text = text[1:]
            if text.strip() == "" and "\n" in text:
                children = self._children()
                previous_inline = bool(children) and (
                    isinstance(children[-1], str) or children[-1]["tag"] in _INLINE_TAGS
                )
                if not previous_inline:
                    return
            text = text.replace("\n", " ")
            if not text:
                return
            children = self._children()
            if children and isinstance(children[-1], str):
                children[-1] += text
            else:
                children.append(text)

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag == "body":
            require(not self.stack, "unclosed display element")
            self.in_body = False
        elif self.in_body:
            require(
                bool(self.stack) and self.stack[-1]["tag"] == tag,
                "unbalanced display HTML",
            )
            self.stack.pop()


def page_from_html(filename, text):
    """Normalize a complete sanctioned page to display nodes, not source records."""
    require(filename in PAGE_NAMES, "unknown example filename")
    refuse_forbidden_phonetic_marks(text, filename)
    parser = _DisplayParser()
    parser.feed(text)
    parser.close()
    require(
        not parser.stack and not parser.in_body and bool(parser.body),
        "incomplete example HTML",
    )
    return {"filename": filename, "title": parser.title.strip(), "body": parser.body}


def _html_nodes(nodes):
    result = []
    for node in nodes:
        if isinstance(node, str):
            result.append(node)
        else:
            result.append(
                legacy_html.htel_mk(
                    node["tag"], node["attributes"], _html_nodes(node["children"])
                )
            )
    return result


def page_texts(payload):
    """Render validated public display documents through the preserved serializer."""
    validate(payload)
    output = {}
    for page in payload["pages"]:
        context = legacy_html.WriteCtx(
            page["title"],
            page["filename"],
            "./",
            icon_href="../favicon.svg",
            css_hrefs=("../document.css", "../yeivin-itm/style.css", "style.css"),
        )
        text = legacy_html.html_text(_html_nodes(page["body"]), context)
        refuse_forbidden_phonetic_marks(text, page["filename"])
        output[page["filename"]] = text
    return output
