"""Independent DOM projection of either pronunciation from generated chapters.

The frozen hashes come from the old public pages, not from the new renderer or
from source records. This check validates displayed rows, attributes and inline
elements after selection; release disclosure review remains a separate gate.

The old pages cannot be produced again, so they are evidence only for text that MAM
has not changed since. A chapter is compared only while its MAM-parsed plus input
matches the fingerprint recorded in in/phonetic_mam_legacy_projection_inputs.json
when the frozen hashes still held; a chapter whose input a refresh has changed
leaves the comparison, and ``chapters_left`` names it. No code writes either record.
"""

import hashlib
import json
from pathlib import Path

from lxml import html

from mb_cmn import bib_locales
from mb_cmn import mam_bknas_and_std_bknas as mbkn
from phonetic_mam.display_schema import PRONUNCIATIONS, require

INPUTS_SCHEMA = "phonetic-mam-projection-inputs-v1"


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


def input_fingerprints(plus_dir):
    """Each chapter page's fingerprint of the MAM-parsed plus input its display rests on.

    The plus reader attaches each verse's successor's cell C across chapter boundaries
    (``mb_cmn.read_books_from_mam_parsed_plus``), so a fingerprint covers the verse
    before the chapter, the chapter's verses and the verse after it, each as its plus
    record of cells C, D and E, in reading order within one plus file, with None at
    that file's edges. It is the SHA-256 of that sequence's canonical JSON, keyed by
    the chapter page's path in the site.
    """
    result = {}
    files = sorted(Path(plus_dir).glob("*.json"))
    require(bool(files), f"missing MAM-parsed plus input: {plus_dir}")
    for path in files:
        book24 = json.loads(path.read_text(encoding="utf-8"))
        sequence = []
        for book39 in book24["book39s"]:
            bk39id = mbkn.MAM_HBNP_TO_BK39ID[
                (book39["book24_name"], book39["sub_book_name"])
            ]
            for chapter, verses in book39["chapters"].items():
                for verse, record in verses.items():
                    # The plus reader's two pseudo-verses, which hold no verse.
                    if verse in ("0", "תתת"):
                        continue
                    sequence.append(((bk39id, int(chapter)), record))
        indices = {}
        for index, (key, _record) in enumerate(sequence):
            indices.setdefault(key, []).append(index)
        for (bk39id, chapter), positions in indices.items():
            first, last = positions[0], positions[-1]
            require(
                positions == list(range(first, last + 1)), "discontiguous plus chapter"
            )
            before = sequence[first - 1][1] if first > 0 else None
            after = sequence[last + 1][1] if last + 1 < len(sequence) else None
            window = [before, *(sequence[i][1] for i in positions), after]
            stem = bib_locales.ordered_short_dash_full_39(bk39id)
            relative = f"tnkh/{stem}/{chapter:02d}.html"
            require(relative not in result, f"duplicate plus chapter: {relative}")
            result[relative] = projection_sha256(window)
    return result


def report_chapters_left():
    """Print the chapter pages that have left the legacy projection comparison."""
    from mb_cmn import paths

    inputs = json.loads(
        (paths.in_dir() / "phonetic_mam_legacy_projection_inputs.json").read_text(
            encoding="utf-8"
        )
    )
    left = chapters_left(inputs, input_fingerprints(paths.mam_parsed_plus_dir()))
    print(
        f"{len(left)} of {len(inputs['chapters'])} chapters have left the legacy"
        " projection comparison, their MAM-parsed input having changed since"
        f" {inputs['source_commit']}."
    )
    for relative in left:
        print(f"  {relative}")


def chapters_left(inputs, fingerprints):
    """The chapter pages whose current input differs from its recorded fingerprint."""
    require(
        set(inputs) == {"schema", "source_commit", "chapters"},
        "unknown input-record fields",
    )
    require(inputs["schema"] == INPUTS_SCHEMA, "unknown input record")
    recorded = inputs["chapters"]
    require(len(recorded) == 929, "missing or empty chapter input record")
    require(set(fingerprints) == set(recorded), "chapter input paths differ")
    return sorted(path for path in recorded if fingerprints[path] != recorded[path])


def verify_site(site, oracle, inputs, fingerprints):
    """Compare each unified chapter whose input is unchanged to both frozen projections.

    Returns the chapter pages that have left the comparison because a refresh changed
    their input; a chapter whose input is unchanged must still match.
    """
    require(set(oracle) == {"schema", "source", "chapters"}, "unknown oracle fields")
    require(oracle["schema"] == "phonetic-mam-projection-sha256-v1", "unknown oracle")
    require(
        set(oracle["chapters"]) == set(PRONUNCIATIONS), "missing oracle pronunciation"
    )
    left = chapters_left(inputs, fingerprints)
    require(len(left) < len(inputs["chapters"]), "every chapter left the comparison")
    skipped = set(left)
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
            if relative in skipped:
                continue
            text = (Path(site) / relative).read_text(encoding="utf-8")
            projection = chapter_projection(text, pronunciation, unified=True)
            require(
                projection_sha256(projection) == expected_hash,
                f"projection differs: {pronunciation}/{relative}",
            )
    require(set(inputs["chapters"]) == expected_paths, "input-record paths differ")
    actual = {
        path.relative_to(site).as_posix()
        for path in (Path(site) / "tnkh").glob("*/*.html")
    }
    require(actual == expected_paths, "unified chapter path set differs")
    return left
