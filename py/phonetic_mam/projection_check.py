"""Independent DOM projection of either pronunciation from generated chapters.

The frozen hashes come from the old public pages, not from the new renderer or
from source records. This check validates displayed rows, attributes and inline
elements after selection; release disclosure review remains a separate gate.
"""

import hashlib
import json
from pathlib import Path

from lxml import html

from phonetic_mam.display_schema import PRONUNCIATIONS, require


def _append(nodes, text):
    if not text:
        return
    text = text.replace("\n", " ")
    if nodes and isinstance(nodes[-1], str):
        nodes[-1] += text
    else:
        nodes.append(text)


def _contents(element, pronunciation, unified):
    result = []
    _append(result, element.text)
    for child in element:
        klass = child.get("class")
        if (
            unified
            and child.tag == "span"
            and klass in ("pronunciation-sephardic", "pronunciation-ashkenazic")
        ):
            if klass == "pronunciation-" + pronunciation:
                for node in _contents(child, pronunciation, unified):
                    if isinstance(node, str):
                        _append(result, node)
                    else:
                        result.append(node)
        else:
            require(child.tag in ("span", "sup"), "unexpected chapter inline element")
            result.append(
                {
                    "tag": child.tag,
                    "attributes": dict(sorted(child.attrib.items())),
                    "children": _contents(child, pronunciation, unified),
                }
            )
        _append(result, child.tail)
    return result


def chapter_projection(text, pronunciation, *, unified):
    """Extract selected table cells without importing the release renderer."""
    require(pronunciation in PRONUNCIATIONS, "unknown projection pronunciation")
    document = html.fromstring(text)
    parent = document.find("body/main") if unified else document.find("body")
    require(parent is not None, "missing chapter body")
    number = 1
    verses = []
    for element in parent:
        if element.tag == "h2":
            number = int(element.text)
            require(
                element.attrib == {"class": "verse-number", "id": f"v{number}"},
                "verse identity differs",
            )
        elif element.tag == "table":
            require(not element.attrib, "unexpected table attributes")
            rows = []
            for row in element:
                require(row.tag == "tr" and not row.attrib, "unexpected chapter row")
                cells = []
                for cell in row:
                    require(cell.tag == "td", "unexpected chapter cell")
                    attributes = dict(cell.attrib)
                    klass = attributes.pop("class", None)
                    if klass is not None:
                        require(
                            unified
                            and klass
                            in ("column-sephardic-only", "column-ashkenazic-only"),
                            "unknown column selector",
                        )
                        if klass != f"column-{pronunciation}-only":
                            continue
                    cells.append(
                        {
                            "attributes": attributes,
                            "children": _contents(cell, pronunciation, unified),
                        }
                    )
                rows.append(cells)
            verses.append({"number": number, "rows": rows})
        elif not (unified and element.tag == "nav"):
            raise ValueError("unexpected chapter structure")
    require(bool(verses), "empty chapter projection")
    require(
        [v["number"] for v in verses] == list(range(1, len(verses) + 1)),
        "chapter verse sequence differs",
    )
    return verses


def projection_sha256(projection):
    data = json.dumps(
        projection, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def verify_site(site, oracle):
    """Compare every unified chapter to both independent frozen projections."""
    require(set(oracle) == {"schema", "source", "chapters"}, "unknown oracle fields")
    require(oracle["schema"] == "phonetic-mam-projection-sha256-v1", "unknown oracle")
    require(
        set(oracle["chapters"]) == set(PRONUNCIATIONS), "missing oracle pronunciation"
    )
    expected_paths = None
    for pronunciation in PRONUNCIATIONS:
        chapter_hashes = oracle["chapters"][pronunciation]
        require(len(chapter_hashes) == 929, "missing or empty canonical chapter oracle")
        if expected_paths is None:
            expected_paths = set(chapter_hashes)
        require(
            set(chapter_hashes) == expected_paths, "pronunciation oracle paths differ"
        )
        for relative, expected_hash in chapter_hashes.items():
            text = (Path(site) / relative).read_text(encoding="utf-8")
            projection = chapter_projection(text, pronunciation, unified=True)
            require(
                projection_sha256(projection) == expected_hash,
                f"projection differs: {pronunciation}/{relative}",
            )
    actual = {
        path.relative_to(site).as_posix()
        for path in (Path(site) / "tnkh").glob("*/*.html")
    }
    require(actual == expected_paths, "unified chapter path set differs")
