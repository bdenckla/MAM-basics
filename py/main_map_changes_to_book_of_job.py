"""
Map UXLC change entries (changeset 2026.02.05) to book-of-job quirkrecs.

This script establishes and verifies a correspondence between:
  - The 162 change entries in the 2026.02.05 changeset of
    "uxlc/in/UXLC-misc/2026.04.01 - Changes.xml"
  - The 160 "quirkrecs" in the retained book-of-job tree's
    "book-of-job/out/enriched-quirkrecs.json"

It produces two outputs:
  1. A JSON mapping file:
     uxlc/in/UXLC-misc/2026.04.01-map-to-book-of-job.json
  2. A deep comparison report printed to stdout

The mapping is done in two phases:
  Phase 1 (align): Walk both sequences in order, aligning by verse
    reference (e.g. "Job 8:16"). A two-pointer approach with lookahead
    handles the 2 XML entries that have no quirkrec counterpart.
  Phase 2 (verify): For each matched pair, compare LC location, Hebrew
    text, and semantic topic to confirm the entries are truly about the
    same thing.

Line number conventions differ between the two sources:
  - The XML uses positive line numbers, not counting blank lines.
  - The quirkrecs use either positive (top-down, counting blank lines)
    or negative (bottom-up from line 28) line numbers. The field
    "including-blank-lines" in qr-lc-loc records how many blank lines
    are included in a positive count. For negative counts, blank lines
    are already excluded.
"""

import xml.etree.ElementTree as ET
import json
import re
import sys

from mb_cmn import paths

import uxlc_paths

XML_PATH = uxlc_paths.uxlc_misc_dir() / "2026.04.01 - Changes.xml"
QR_PATH = paths.repo_root() / "book-of-job" / "out" / "enriched-quirkrecs.json"
HTML_DIR = paths.gh_pages_dir() / "book-of-job" / "jobn-details"
MAP_OUT_PATH = uxlc_paths.uxlc_misc_dir() / "2026.04.01-map-to-book-of-job.json"

CHANGESET = "2026.02.05"
HTML_START = "0119.html"
LINES_PER_COLUMN = 28


def _lc_text(lc, tag):
    """The text of one <lc> sub-element, stripped of surrounding whitespace.

    deep_compare() below compares these values against the quirkrecs as
    strings, so a stray space makes two values that agree read as differing.
    That is not hypothetical: across the 1398 changes of the seventeen
    changes files under uxlc/in/UXLC-misc/, <column> has a trailing space
    twice -- 2024.07.08 #6 and 2026.02.05 #63, both "1 " -- and #63 is in
    this changeset, where it produced the sole LC COL issue. <folio> and
    <line> are clean in all 1398; they are stripped here because they are
    compared the same way, not on evidence of their own. "reftext" and
    "changetext" below were already stripped where they are read.

    Returning "" for a missing element also covers an element present with
    no text, which the "lc_page" expression this replaced would have hit
    with an AttributeError.
    """
    elem = lc.find(tag)
    if elem is None or elem.text is None:
        return ""
    return elem.text.strip()


def parse_xml_entries():
    tree = ET.parse(XML_PATH)
    root = tree.getroot()
    entries = []
    for date_elem in root.iter("date"):
        date_text = date_elem.find("date")
        if date_text is not None and date_text.text == CHANGESET:
            for change in date_elem.findall("change"):
                cit = change.find("citation")
                lc = change.find("lc")
                notes = [n.text for n in change.findall("notes/note") if n.text]
                entries.append(
                    {
                        "n": int(change.find("n").text),
                        "ref": f"{cit.find('book').text} {cit.find('c').text}:{cit.find('v').text}",
                        "cv": f"{cit.find('c').text}:{cit.find('v').text}",
                        "pos": cit.find("position").text,
                        "desc": change.find("description").text or "",
                        "reftext": (change.find("reftext").text or "").strip(),
                        "changetext": (change.find("changetext").text or "").strip(),
                        "lc_page": _lc_text(lc, "folio").replace("Folio_", ""),
                        "lc_col": _lc_text(lc, "column"),
                        "lc_line": _lc_text(lc, "line"),
                        "notes": notes,
                    }
                )
            break
    return entries


def walk_html_chain():
    """Follow the 'next' links starting from HTML_START."""
    entries = []
    current = HTML_START
    while current and len(entries) < 200:
        fpath = HTML_DIR / current
        if not fpath.exists():
            entries.append({"file": current, "ref": "FILE NOT FOUND", "desc": ""})
            break
        text = fpath.read_text(encoding="utf-8")
        m = re.search(r"<title>(.*?)</title>", text)
        title = m.group(1) if m else "?"
        tds = re.findall(r"<td[^>]*>(.*?)</td>", text, re.DOTALL)
        desc = ""
        if len(tds) >= 3:
            desc = re.sub(r"<[^>]+>", "", tds[2]).strip()
            desc = re.sub(r"\s+", " ", desc)
        entries.append({"file": current, "ref": title, "desc": desc})
        m = re.search(r'href="([^"]+)">next', text)
        current = m.group(1) if m else None
    return entries


def align_sequences(xml_entries, html_entries):
    """Align two sequences by verse reference using a two-pointer approach."""
    xi, hi = 0, 0
    matched, xml_only, html_only = [], [], []

    while xi < len(xml_entries) and hi < len(html_entries):
        xe, he = xml_entries[xi], html_entries[hi]
        if xe["ref"] == he["ref"]:
            matched.append((xe, he))
            xi += 1
            hi += 1
        else:
            found_in_html = next(
                (
                    look
                    for look in range(1, 4)
                    if hi + look < len(html_entries)
                    and xml_entries[xi]["ref"] == html_entries[hi + look]["ref"]
                ),
                None,
            )
            found_in_xml = next(
                (
                    look
                    for look in range(1, 4)
                    if xi + look < len(xml_entries)
                    and xml_entries[xi + look]["ref"] == html_entries[hi]["ref"]
                ),
                None,
            )
            if found_in_html is not None and (
                found_in_xml is None or found_in_html <= found_in_xml
            ):
                for skip in range(found_in_html):
                    html_only.append(html_entries[hi + skip])
                hi += found_in_html
            elif found_in_xml is not None:
                for skip in range(found_in_xml):
                    xml_only.append(xml_entries[xi + skip])
                xi += found_in_xml
            else:
                xml_only.append(xe)
                xi += 1

    xml_only.extend(xml_entries[xi:])
    html_only.extend(html_entries[hi:])
    return matched, xml_only, html_only


def _repo_relative(path):
    """Spell a path as this repository names it, for the labels below."""
    return path.relative_to(paths.repo_root()).as_posix()


def write_mapping(matched, xml_only, html_only):
    # "xml_source" and "html_base" are documentation for whoever reads the
    # mapping: where its input came from, and the prefix that turns each
    # entry's bare "html" filename into a locatable page.  No program reads
    # either -- this module writes them and nothing else in the tree mentions
    # them -- so they are repo-root-relative for a reader rather than paths
    # anything opens.  Both are DERIVED from XML_PATH and HTML_DIR because the
    # spelled-out pair went stale unnoticed: 8a04ad54 (2026-09-03) repointed
    # those two constants into this repository and left the labels naming
    # UXLC-utils' layout and a book-of-job clone that belongs on no machine.
    output = {
        "xml_source": _repo_relative(XML_PATH),
        "html_base": _repo_relative(HTML_DIR) + "/",
        "changeset": CHANGESET,
        "matched": [
            {"n": xe["n"], "ref": xe["ref"], "pos": xe["pos"], "html": he["file"]}
            for xe, he in matched
        ],
        "xml_only": [
            {"n": xe["n"], "ref": xe["ref"], "pos": xe["pos"], "desc": xe["desc"]}
            for xe in xml_only
        ],
        "html_only": [{"html": he["file"], "ref": he["ref"]} for he in html_only],
    }
    MAP_OUT_PATH.write_text(
        json.dumps(output, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="",
    )
    print(f"Wrote {MAP_OUT_PATH}")
    return output


# --- Deep comparison helpers ---


def extract_letter_refs(text):
    """Extract Hebrew letter names mentioned in English text."""
    letters = [
        "alef",
        "bet",
        "gimmel",
        "dalet",
        "he",
        "vav",
        "zayin",
        "het",
        "tet",
        "yod",
        "kaf",
        "lamed",
        "mem",
        "nun",
        "samekh",
        "ayin",
        "pe",
        "tsadi",
        "qof",
        "resh",
        "shin",
        "sin",
        "tav",
    ]
    low = text.lower()
    return {letter for letter in letters if letter in low}


def extract_mark_refs(text):
    """Extract diacritical/accent mark names from text (English or Hebrew)."""
    marks_en = [
        "dagesh",
        "mapiq",
        "meteg",
        "merkha",
        "dehi",  # translit-ok: the source texts' own mark names
        "tipeha",  # translit-ok: the source texts' own mark names
        "revia",
        "geresh",
        "munah",  # translit-ok: the source texts' own mark names
        "etnachta",  # translit-ok: the source texts' own mark names
        "siluq",
        "shuruq",
        "holam",
        "hiriq",
        "patah",
        "qamats",
        "segol",
        "sheva",
        "hataf",
        "paseq",
        "maqaf",
        "ole",
        "mahapakh",
        "geresh-muqdam",
    ]
    marks_he = {
        "דגש": "dagesh",
        "מפיק": "mapiq",
        "געיה": "meteg",
        "מרכא": "merkha",
        "דחי": "dehi",  # translit-ok: the source texts' own mark names
        "טרחא": "tipeha",  # translit-ok: the source texts' own mark names
        "רביע": "revia",
        "גרש": "geresh",
        "מונח": "munah",  # translit-ok: the source texts' own mark names
        "אתנח": "etnachta",  # translit-ok: the source texts' own mark names
        "סילוק": "siluq",
        "שורוק": "shuruq",
        "חולם": "holam",
        "חיריק": "hiriq",
        "פתח": "patah",
        "קמץ": "qamats",
        "סגול": "segol",
        "שווא": "sheva",
        "חטף": "hataf",
        "פסק": "paseq",
        "מקף": "maqaf",
        "עולה": "ole",
        "גרש מוקדם": "geresh-muqdam",
    }
    low = text.lower()
    found = {m for m in marks_en if m in low}
    for heb, eng in marks_he.items():
        if heb in text:
            found.add(eng)
    return found


def extract_hebrew_letters(word):
    return [c for c in word if "\u05d0" <= c <= "\u05ea"]


def _coerce_str(val):
    if isinstance(val, list):
        return " ".join(str(x) for x in val if x)
    return val if isinstance(val, str) else str(val)


def normalize_qr_line(qr_loc):
    """Convert a quirkrec line number to the XML convention (positive, no blanks)."""
    raw = qr_loc.get("line", "")
    blanks = qr_loc.get("including-blank-lines", 0)
    if isinstance(raw, int) and raw < 0:
        normalized = LINES_PER_COLUMN + raw
    else:
        normalized = raw
    if isinstance(raw, int) and raw > 0 and isinstance(blanks, int):
        adjusted = normalized - blanks
    else:
        adjusted = normalized
    return adjusted, raw, blanks


def deep_compare(xml_entries, mapping, quirkrecs):
    """Compare matched entries on location, Hebrew text, and semantic topic."""
    n_to_qr = {}
    for i, m in enumerate(mapping["matched"]):
        n_to_qr[m["n"]] = quirkrecs[i]

    issues = []
    ok_count = 0

    for xe in xml_entries:
        if xe["n"] not in n_to_qr:
            continue
        qr = n_to_qr[xe["n"]]
        entry_issues = []

        # 1. Verse reference
        if xe["cv"] != qr["qr-cv"]:
            entry_issues.append(f"CV MISMATCH: xml={xe['cv']} qr={qr['qr-cv']}")

        # 2. LC location
        qr_loc = qr.get("qr-lc-loc", {})
        qr_page = str(qr_loc.get("page", ""))
        qr_col = str(qr_loc.get("column", ""))
        qr_line_adj, qr_line_raw, qr_blanks = normalize_qr_line(qr_loc)
        qr_line = str(qr_line_adj)

        if xe["lc_page"] and qr_page and xe["lc_page"] != qr_page:
            entry_issues.append(f"LC PAGE: xml={xe['lc_page']} qr={qr_page}")
        if xe["lc_col"] and qr_col and xe["lc_col"] != qr_col:
            entry_issues.append(f"LC COL: xml={xe['lc_col']} qr={qr_col}")
        if xe["lc_line"] and qr_line and xe["lc_line"] != qr_line:
            entry_issues.append(
                f"LC LINE: xml={xe['lc_line']} qr={qr_line} (raw={qr_line_raw}, blanks={qr_blanks})"
            )

        # 3. Hebrew text
        qr_cons = qr.get("qr-consensus", "")
        qr_prop = qr.get("qr-lc-proposed", "")
        xml_ref = xe["reftext"]
        texts_match = False
        if xml_ref and (
            xml_ref in qr_cons
            or xml_ref in qr_prop
            or qr_cons in xml_ref
            or qr_prop in xml_ref
        ):
            texts_match = True
        if not texts_match and xml_ref:
            xl = extract_hebrew_letters(xml_ref)
            if xl and (
                xl == extract_hebrew_letters(qr_cons)
                or xl == extract_hebrew_letters(qr_prop)
            ):
                texts_match = True
        if not texts_match and xml_ref:
            entry_issues.append(
                f"HEBREW: xml='{xml_ref}' qr-cons='{qr_cons}' qr-prop='{qr_prop}'"
            )

        # 4. Semantic topic
        xml_desc = xe["desc"]
        qr_weird = _coerce_str(qr.get("qr-what-is-weird", ""))
        qr_autodiff = " ".join(str(x) for x in qr.get("qr-auto-diff", []) if x)
        qr_comment = _coerce_str(qr.get("qr-generic-comment", ""))

        xml_marks = extract_mark_refs(xml_desc)
        qr_marks = extract_mark_refs(qr_weird + " " + qr_autodiff + " " + qr_comment)
        xml_letters = extract_letter_refs(xml_desc)
        qr_letters = extract_letter_refs(qr_weird)

        if (
            not (xml_marks & qr_marks)
            and not (xml_letters & qr_letters)
            and xml_marks
            and qr_marks
        ):
            entry_issues.append(
                f"TOPIC: xml marks={sorted(xml_marks)} qr marks={sorted(qr_marks)}"
            )

        if entry_issues:
            issues.append((xe, qr, entry_issues))
        else:
            ok_count += 1

    return ok_count, issues


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    xml_entries = parse_xml_entries()
    html_entries = walk_html_chain()
    print(f"XML entries: {len(xml_entries)}, HTML entries: {len(html_entries)}")

    matched, xml_only, html_only = align_sequences(xml_entries, html_entries)
    print(
        f"Matched: {len(matched)}, XML-only: {len(xml_only)}, HTML-only: {len(html_only)}"
    )
    print()

    mapping = write_mapping(matched, xml_only, html_only)
    print()

    quirkrecs = json.loads(QR_PATH.read_text(encoding="utf-8"))
    ok_count, issues = deep_compare(xml_entries, mapping, quirkrecs)
    print(f"Deep comparison: {ok_count + len(issues)} entries compared")
    print(f"  OK: {ok_count}")
    print(f"  Issues: {len(issues)}")
    print()

    for xe, qr, entry_issues in issues:
        print(f"--- #{xe['n']} {xe['ref']}.{xe['pos']} ---")
        print(f"  XML desc: {xe['desc']}")
        print(f"  QR weird: {qr.get('qr-what-is-weird', '')}")
        for iss in entry_issues:
            print(f"  ** {iss}")
        print()


if __name__ == "__main__":
    main()
