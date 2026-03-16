"""
Load MPP plus/ JSON from git revisions and extract EP column body text.

Exports:
    diff_all_books  — compare all books between two revisions
    flatten_ep      — flatten EP column to body text string
"""

import json
import subprocess

MAM_PARSED_DIR = "../MAM-parsed"

# ── Git helpers ──────────────────────────────────────────────


def _git_show(rev, path):
    """Read a file from a specific git revision of MAM-parsed."""
    result = subprocess.run(
        ["git", "-C", MAM_PARSED_DIR, "show", f"{rev}:{path}"],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode != 0:
        return None
    return result.stdout


def _git_show_json(rev, path):
    text = _git_show(rev, path)
    if text is None:
        return None
    return json.loads(text)


def _list_plus_files(rev):
    """List plus/ filenames (without the 'plus/' prefix) at a revision."""
    result = subprocess.run(
        ["git", "-C", MAM_PARSED_DIR, "ls-tree", "--name-only", rev, "plus/"],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    lines = result.stdout.strip().split("\n")
    return [line.strip().removeprefix("plus/") for line in lines if line.strip()]


# ── EP column body text extraction ───────────────────────────


def flatten_ep(ep):
    """Flatten an EP column array to a body text string.

    Includes plain text and the body-text contribution of templates
    (e.g. נוסח param 1, קו"כ params, מ:קמץ dalet variant).
    Excludes נוסח param 2 (manuscript annotations).
    """
    return "".join(_flatten_element(el) for el in ep)


def _flatten_element(el):
    if isinstance(el, str):
        return el
    if isinstance(el, dict):
        return _flatten_template(el)
    if isinstance(el, list):
        return "".join(_flatten_element(x) for x in el)
    return ""


def _get_params(tmpl):
    """Get template params, handling both tmpl_params and tmpl_args formats."""
    if "tmpl_params" in tmpl:
        return tmpl["tmpl_params"]
    # Fall back to tmpl_args: arg[0] = param "1", subsequent args have "key=" prefix
    args = tmpl.get("tmpl_args", [])
    params = {}
    for i, arg in enumerate(args):
        if i == 0:
            params["1"] = arg
        elif isinstance(arg, str) and "=" in arg:
            key, _, val = arg.partition("=")
            params[key] = val
        elif isinstance(arg, list) and len(arg) >= 1:
            # Some tmpl_args entries are arrays; treat as param by index
            params[str(i + 1)] = arg
        else:
            params[str(i + 1)] = arg
    return params


def _flatten_template(tmpl):
    name = tmpl["tmpl_name"]
    params = _get_params(tmpl)
    if name == "נוסח":
        return _flatten_element(params["1"]) if "1" in params else ""
    if name in ('קו"כ', 'כו"ק'):
        parts = []
        if "1" in params:
            parts.append(_flatten_element(params["1"]))
        if "2" in params:
            parts.append(_flatten_element(params["2"]))
        return "".join(parts)
    if name == "מ:קמץ":
        return _flatten_element(params["ד"]) if "ד" in params else ""
    if name in ("מ:לגרמיה-2", "מ:לגרמיה"):
        return "\u05c0"  # paseq character
    if name == "מ:פסק":
        return "\u05c0"  # paseq character
    # Generic: try param "1" if present
    if "1" in params:
        return _flatten_element(params["1"])
    return ""


# ── Book-level diffing ───────────────────────────────────────

# Map plus/ filenames to display names for each book39 within them
_FILE_STEM_TO_BOOK39S = {
    "A1-Genesis": ["Genesis"],
    "A2-Exodus": ["Exodus"],
    "A3-Levit": ["Leviticus"],
    "A4-Numbers": ["Numbers"],
    "A5-Deuter": ["Deuteronomy"],
    "B1-Joshua": ["Joshua"],
    "B2-Judges": ["Judges"],
    "BA-Samuel": ["1 Samuel", "2 Samuel"],
    "BC-Kings": ["1 Kings", "2 Kings"],
    "C1-Isaiah": ["Isaiah"],
    "C2-Jeremiah": ["Jeremiah"],
    "C3-Ezekiel": ["Ezekiel"],
    "CA-The-12-Minor-Prophets": [
        "Hosea",
        "Joel",
        "Amos",
        "Obadiah",
        "Jonah",
        "Micah",
        "Nahum",
        "Habakkuk",
        "Zephaniah",
        "Haggai",
        "Zechariah",
        "Malachi",
    ],
    "D1-Psalms": ["Psalms"],
    "D2-Proverbs": ["Proverbs"],
    "D3-Job": ["Job"],
    "E1-Song of Songs": ["Song of Songs"],
    "E2-Ruth": ["Ruth"],
    "E3-Lamentations": ["Lamentations"],
    "E4-Ecclesiastes": ["Ecclesiastes"],
    "E5-Esther": ["Esther"],
    "F1-Daniel": ["Daniel"],
    "FA-Ezra-Nexemiah": ["Ezra", "Nehemiah"],
    "FC-Chronicles": ["1 Chronicles", "2 Chronicles"],
}


def _book39_names_for_file(filename):
    stem = filename.removesuffix(".json")
    return _FILE_STEM_TO_BOOK39S[stem]


def _diff_one_file(old_json, new_json, filename):
    """Compare two revisions of a single plus/ JSON file."""
    diffs = []
    book39_names = _book39_names_for_file(filename)
    he_to_int = old_json["header"]["he_to_int"]
    old_book39s = old_json["book39s"]
    new_book39s = new_json["book39s"]
    for b39_idx, (old_b39, new_b39) in enumerate(zip(old_book39s, new_book39s)):
        book_name = book39_names[b39_idx]
        old_chapters = old_b39["chapters"]
        new_chapters = new_b39["chapters"]
        for he_ch in old_chapters:
            if he_ch not in new_chapters:
                continue
            int_ch = he_to_int[he_ch]
            old_verses = old_chapters[he_ch]
            new_verses = new_chapters[he_ch]
            for he_vr in old_verses:
                if he_vr not in new_verses:
                    continue
                int_vr = he_to_int[he_vr]
                old_verse = old_verses[he_vr]
                new_verse = new_verses[he_vr]
                old_ep = old_verse[2]
                new_ep = new_verse[2]
                diff = _diff_ep(old_ep, new_ep, book_name, int_ch, int_vr)
                if diff is not None:
                    diffs.append(diff)
    return diffs


def _collect_template_names(obj):
    """Recursively collect all template names from a data structure."""
    names = []
    if isinstance(obj, dict):
        if "tmpl_name" in obj:
            names.append(obj["tmpl_name"])
        for v in obj.values():
            names.extend(_collect_template_names(v))
    elif isinstance(obj, list):
        for item in obj:
            names.extend(_collect_template_names(item))
    return names


def _diff_ep(old_ep, new_ep, book_name, chapter, verse):
    """Compare two EP columns. Returns a diff dict or None.

    Compares flattened body text first (catches real text changes),
    then template name lists (catches structural changes like
    legarmeih -> paseq). Ignores format differences like
    tmpl_args vs tmpl_params.
    """
    old_text = flatten_ep(old_ep)
    new_text = flatten_ep(new_ep)
    text_changed = old_text != new_text
    if not text_changed:
        old_names = set(_collect_template_names(old_ep))
        new_names = set(_collect_template_names(new_ep))
        if old_names == new_names:
            return None  # No meaningful change
    return {
        "book": book_name,
        "chapter": chapter,
        "verse": verse,
        "old_text": old_text,
        "new_text": new_text,
        "old_ep": old_ep,
        "new_ep": new_ep,
        "text_changed": text_changed,
    }


def diff_all_books(old_rev, new_rev):
    """Compare all plus/ books between two git revisions.

    Returns a list of diff dicts, sorted in reading order.
    """
    old_files = set(_list_plus_files(old_rev))
    new_files = set(_list_plus_files(new_rev))
    common = sorted(old_files & new_files)
    all_diffs = []
    for filename in common:
        path = f"plus/{filename}"
        old_json = _git_show_json(old_rev, path)
        new_json = _git_show_json(new_rev, path)
        if old_json is None or new_json is None:
            continue
        all_diffs.extend(_diff_one_file(old_json, new_json, filename))
    return all_diffs
