"""
Load MPP plus/ JSON from git revisions and extract EP column body text.

Exports:
    diff_all_books  — compare all books between two revisions
    flatten_ep      — flatten EP column to body text string
"""

import difflib
import json
import subprocess

from pycmn import hebrew_verse_numerals as hvn

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
        [
            "git",
            "-C",
            MAM_PARSED_DIR,
            "-c",
            "core.quotePath=false",
            "ls-tree",
            "--name-only",
            rev,
            "plus/",
        ],
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


def _get_param(tmpl, key):
    """Look up a single template parameter by key.

    Handles all historical formats:
      - tmpl_params dict  (current: {"1": ..., "ד": ...})
      - tmpl_args_dic dict (transitional, same shape)
      - tmpl_args list (oldest: positional for integer keys,
        "key=value" strings for named keys like "ד=...",
        or ["key=", value] lists when value is complex)

    Returns the value, or _MISSING if the key is absent.
    """
    for dict_key in ("tmpl_params", "tmpl_args_dic"):
        d = tmpl.get(dict_key)
        if d is not None and key in d:
            return d[key]
    args = tmpl.get("tmpl_args")
    if args is not None:
        # Integer keys → positional lookup
        if key.isdigit():
            idx = int(key) - 1
            if 0 <= idx < len(args):
                return args[idx]
        else:
            # Named keys → scan for "key=value" string or list starting
            # with "key=..." (possibly fused with the start of the value)
            prefix = key + "="
            for arg in args:
                if isinstance(arg, str) and arg.startswith(prefix):
                    return arg[len(prefix) :]
                if (
                    isinstance(arg, list)
                    and arg
                    and isinstance(arg[0], str)
                    and arg[0].startswith(prefix)
                ):
                    head = arg[0][len(prefix) :]
                    tail = arg[1:]
                    if not head and len(tail) == 1:
                        return tail[0]
                    return ([head] if head else []) + tail
    return _MISSING


_MISSING = object()


_PARASHAH_NAMES = {"סס", "ססס", "פפ", "פפפ"}


def _is_parashah_template(name):
    """Check if template is a parashah marker (רN, סס, ססס, פפ, פפפ).

    These templates contribute a space to body text; their param "1"
    (e.g. "פסקא באמצע פסוק") is a structural annotation, not verse content.
    """
    if name in _PARASHAH_NAMES:
        return True
    return len(name) >= 2 and name[0] == "ר" and name[1:].isdigit()


def _flatten_template(tmpl):
    name = tmpl["tmpl_name"]
    if _is_parashah_template(name):
        return " "
    if name == "נוסח":
        p1 = _get_param(tmpl, "1")
        return _flatten_element(p1) if p1 is not _MISSING else ""
    if name in ('קו"כ', 'כו"ק'):
        parts = []
        p1 = _get_param(tmpl, "1")
        if p1 is not _MISSING:
            parts.append(_flatten_element(p1))
        p2 = _get_param(tmpl, "2")
        if p2 is not _MISSING:
            parts.append(_flatten_element(p2))
        return "".join(parts)
    if name == "מ:קמץ":
        pd = _get_param(tmpl, "ד")
        return _flatten_element(pd) if pd is not _MISSING else ""
    if name in ("מ:לגרמיה-2", "מ:לגרמיה"):
        return "׀"  # paseq/legarmeih character
    if name == "מ:פסק":
        return "׀"  # paseq/legarmeih character
    if name == "מ:כפול":
        pk = _get_param(tmpl, "כפול")
        return _flatten_element(pk) if pk is not _MISSING else ""
    # Generic: try param "1" if present
    p1 = _get_param(tmpl, "1")
    if p1 is not _MISSING:
        return _flatten_element(p1)
    return ""


# ── Position-tracking flattener (for נוסח overlap detection) ──


def _flatten_ep_with_nusach(ep):
    """Flatten EP column and track נוסח templates that have param 2.

    Returns (text, nusach_notes) where nusach_notes is a list of
    {"start": int, "end": int, "param2": value} dicts.
    """
    parts = []
    notes = []
    for el in ep:
        _flatten_tracking(el, parts, notes)
    return "".join(parts), notes


def _flatten_tracking(obj, parts, notes):
    """Flatten element while tracking נוסח template positions."""
    if isinstance(obj, str):
        parts.append(obj)
    elif isinstance(obj, dict):
        _flatten_template_tracking(obj, parts, notes)
    elif isinstance(obj, list):
        for item in obj:
            _flatten_tracking(item, parts, notes)


def _flatten_template_tracking(tmpl, parts, notes):
    """Flatten template while tracking נוסח positions."""
    name = tmpl["tmpl_name"]
    if _is_parashah_template(name):
        parts.append(" ")
        return
    if name == "נוסח":
        start = sum(len(p) for p in parts)
        p1 = _get_param(tmpl, "1")
        if p1 is not _MISSING:
            _flatten_tracking(p1, parts, notes)
        end = sum(len(p) for p in parts)
        p2 = _get_param(tmpl, "2")
        if p2 is not _MISSING:
            notes.append({"start": start, "end": end, "param2": p2})
        return
    if name in ('קו"כ', 'כו"ק'):
        p1 = _get_param(tmpl, "1")
        if p1 is not _MISSING:
            _flatten_tracking(p1, parts, notes)
        p2 = _get_param(tmpl, "2")
        if p2 is not _MISSING:
            _flatten_tracking(p2, parts, notes)
        return
    if name == "מ:קמץ":
        pd = _get_param(tmpl, "ד")
        if pd is not _MISSING:
            _flatten_tracking(pd, parts, notes)
        return
    if name in ("מ:לגרמיה-2", "מ:לגרמיה"):
        parts.append("׀")
        return
    if name == "מ:פסק":
        parts.append("׀")
        return
    if name == "מ:כפול":
        pk = _get_param(tmpl, "כפול")
        if pk is not _MISSING:
            _flatten_tracking(pk, parts, notes)
        return
    p1 = _get_param(tmpl, "1")
    if p1 is not _MISSING:
        _flatten_tracking(p1, parts, notes)


def _changed_new_positions(old_text, new_text):
    """Return set of character positions in new_text that are changed/added."""
    sm = difflib.SequenceMatcher(None, old_text, new_text, autojunk=False)
    changed = set()
    for op, _i1, _i2, j1, j2 in sm.get_opcodes():
        if op in ("replace", "insert"):
            changed.update(range(j1, j2))
    return changed


def _find_relevant_nusach(old_text, new_text, notes, text_changed):
    """Filter nusach notes to those relevant to the change.

    Returns list of note dicts with start, end, and param2 fields
    so that downstream code can distribute notes across sub-diffs
    by position overlap.
    """
    if not notes:
        return []
    if not text_changed:
        # For structural changes, include all nusach notes
        return list(notes)
    # For text changes, find changed character positions in new_text
    changed = _changed_new_positions(old_text, new_text)
    result = []
    for note in notes:
        note_positions = range(note["start"], note["end"])
        if any(pos in note_positions for pos in changed):
            result.append(note)
    return result


# ── Book-level diffing ───────────────────────────────────────

# Map canonical plus/ stems (current OSDF-24 naming) to book39 display names.
_CANONICAL_STEM_TO_BOOK39S = {
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

# Map bare names (pre-OSDF-24 era) to canonical stems.
_BARE_NAME_TO_CANONICAL = {
    stem.partition("-")[2]: stem for stem in _CANONICAL_STEM_TO_BOOK39S
}


def _canonical_stem(filename):
    """Normalize any historical plus/ filename to its canonical OSDF-24 stem.

    Handles three eras:
      - Current: "A1-Genesis.json" → "A1-Genesis"
      - Mid-era: "FA-Ezra-Neḥemiah.json" → "FA-Ezra-Nexemiah"  (ḥ→x)
      - Oldest:  "Genesis.json" → "A1-Genesis"  (no prefix)
    """
    stem = filename.removesuffix(".json").replace("ḥ", "x")
    if stem in _CANONICAL_STEM_TO_BOOK39S:
        return stem
    return _BARE_NAME_TO_CANONICAL[stem]


def _book39_names_for_stem(canonical):
    return _CANONICAL_STEM_TO_BOOK39S[canonical]


def _get_he_to_int(book_json):
    """Return the he_to_int mapping, building it on the fly if absent."""
    he_to_int = book_json["header"].get("he_to_int")
    if he_to_int is not None:
        return he_to_int
    he_keys = set()
    for bk39 in book_json["book39s"]:
        for he_ch, ch_contents in bk39["chapters"].items():
            he_keys.add(he_ch)
            for he_vr in ch_contents:
                he_keys.add(he_vr)
    return {he: hvn.STR_TO_INT_DIC[he] for he in he_keys}


def _diff_one_file(old_json, new_json, canonical_stem):
    """Compare two revisions of a single plus/ JSON file."""
    diffs = []
    book39_names = _book39_names_for_stem(canonical_stem)
    he_to_int = _get_he_to_int(new_json)
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
    """Recursively collect template names relevant to body text.

    Skips נוסח templates entirely: their name is excluded (since
    adding/removing a נוסח wrapper doesn't change body text) and
    param 2 (manuscript annotations) is not recursed into, so templates
    nested there (e.g. ש) are also excluded.
    """
    names = []
    if isinstance(obj, dict):
        if "tmpl_name" in obj:
            if obj["tmpl_name"] == "נוסח":
                # Only recurse into param 1 (body text), skip param 2 (annotations)
                p1 = _get_param(obj, "1")
                if p1 is not _MISSING:
                    names.extend(_collect_template_names(p1))
                return names
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
    new_text, new_nusach = _flatten_ep_with_nusach(new_ep)
    text_changed = old_text != new_text
    if not text_changed:
        old_names = set(_collect_template_names(old_ep))
        new_names = set(_collect_template_names(new_ep))
        if old_names == new_names:
            return None  # No meaningful change
    nusach_notes = _find_relevant_nusach(old_text, new_text, new_nusach, text_changed)
    return {
        "book": book_name,
        "chapter": chapter,
        "verse": verse,
        "old_text": old_text,
        "new_text": new_text,
        "old_ep": old_ep,
        "new_ep": new_ep,
        "text_changed": text_changed,
        "nusach_notes": nusach_notes,
    }


def diff_all_books(old_rev, new_rev):
    """Compare all plus/ books between two git revisions.

    Matches files across historical renames by normalising each filename
    to its canonical OSDF-24 stem before pairing.

    Returns a list of diff dicts, sorted in reading order.
    """
    old_files = _list_plus_files(old_rev)
    new_files = _list_plus_files(new_rev)
    # Build canonical-stem → actual-filename maps
    old_by_stem = {_canonical_stem(f): f for f in old_files}
    new_by_stem = {_canonical_stem(f): f for f in new_files}
    common_stems = sorted(old_by_stem.keys() & new_by_stem.keys())
    all_diffs = []
    for stem in common_stems:
        old_json = _git_show_json(old_rev, f"plus/{old_by_stem[stem]}")
        new_json = _git_show_json(new_rev, f"plus/{new_by_stem[stem]}")
        if old_json is None or new_json is None:
            continue
        all_diffs.extend(_diff_one_file(old_json, new_json, stem))
    return all_diffs
