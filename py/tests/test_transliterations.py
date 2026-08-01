"""Guard: no known-undesirable transliteration variant in our Python source.

Two checks run over every ``py/**/*.py`` in this repo (``__pycache__`` aside); any
single line may opt out with an inline ``# translit-ok`` pragma (self-documenting,
travels with the line, cf. ``# noqa``).  ``mb_cmn``, ``mb_misc`` and ``mb_diff_mpu``
used to be skipped as "vendored from a sibling repo, not ours to normalize"; they are
native here, they are the SOURCE the other repos vendor FROM, and the exclusion was
hiding half the hits, so it is gone.  The two checks:

1. ``test_no_undesirable_transliterations`` -- a denylist of spelling variants
   that the #13 standardization retired: ``zinor``->``tsinnor`` (#30),
   ``merka``->``merkha``, ``atnach``->``atnax``, ``sinnor``->``tsinnor``, the
   het-as-plain-``h`` forms, and a few Goerwitz/legacy capitalizations.  No
   lookahead is needed to shield the good form: the preferred spellings are
   precomposed ``ḥ`` (U+1E25), which shares no ASCII substring with a pattern
   like ``munah``, so the good spelling can never trip it.

2. ``test_no_decomposed_composites_tree_wide`` -- #49 inverts the polarity
   #27 established: the repo standard is now NFC (precomposed), so any
   decomposed base+combining-mark pair with a single-codepoint NFC
   composition (e.g. ``h`` + U+0323) is flagged.

Legitimate exemptions (external vocabularies / verbatim citations), each tagged
``# translit-ok`` in the source and enumerated in issue #26:

* UXLC external vocab -- the readers that match UXLC's own spellings
  ``etnahta`` / ``etnachta`` / ``zinor`` (``main_uxlc_grammar_test.py``,
  ``main_find_uxlc_accent_changes.py``, ``py_uxlc/my_uxlc_unicode_names.py``).
* Unicode-name citations of ``zinor`` (``accgram/mam_poetic_accents.py``,
  ``accgram/poetic_accent_names.py``).
* Finding-aid citations -- Goerwitz "MEREKA"/"MAHPAK", Yeivin "mehuppak",
  Breuer "mahpakh" (``accgram/poetic_accent_names.py``).

This module is itself excluded from the *denylist* scan: its patterns
necessarily spell out every retired variant.  (It is still covered by the
decomposed-composite scan, so the real het glyph it does use stays precomposed.)

Run:
    .venv/Scripts/python.exe -m pytest py/tests/test_transliterations.py -v
"""

from __future__ import annotations

import re
import unicodedata

from mb_cmn import paths

# Lines bearing this pragma are exempt from the denylist scan.
_PRAGMA = re.compile(r"#\s*translit-ok")

# (compiled pattern, preferred spelling, short label).  Patterns are anchored so the
# good precomposed forms and the genuine Unicode names never match; see the per-row
# notes in issue #26's research comment.
_DENYLIST: list[tuple[re.Pattern[str], str, str]] = [
    (re.compile(r"\b[Zz]inor\b"), "tsinnor", "zinor"),
    (re.compile(r"(?<![tT])\b[sS]innor"), "tsinnor(it)", "sinnor"),
    (re.compile(r"\b[mM]unah"), "munaḥ (U+1E25)", "munah"),
    (re.compile(r"\b[tT]arha"), "tarḥa (U+1E25)", "tarha"),
    (re.compile(r"\b[aA]tnah"), "atnaḥ (U+1E25)", "atnah"),
    (re.compile(r"\b[dD]ehi"), "deḥi (U+1E25)", "dehi"),
    (re.compile(r"\b[yY]erah"), "yeraḥ (U+1E25)", "yerah"),
    (re.compile(r"\b[tT]ipeha"), "tipeḥa (U+1E25)", "tipeha"),
    # "kh"-for-xet forms (Wengrov/Breuer-style): xet takes x, never kh (kh is kaf only).
    (re.compile(r"\b[tT]arkha\b"), "tarxa / TARXA", "tarkha"),
    (re.compile(r"\b[mM]unakh\b"), "munaḥ / MUNAX", "munakh"),
    (re.compile(r"\b[aA]tnakh\b"), "atnaḥ / ATNAX", "atnakh"),
    (re.compile(r"\b[tT]ipekha\b"), "tipeḥa / TIPEXA", "tipekha"),
    (re.compile(r"\b[dD]ekhi\b"), "deḥi / DEXI", "dekhi"),
    (re.compile(r"\b[yY]erakh\b"), "yeraḥ / YERAX", "yerakh"),
    (re.compile(r"\b[mM]unaH\b"), "munaḥ (U+1E25)", "munaH"),
    (re.compile(r"\b[tT]ipeHa\b"), "tipeḥa (U+1E25)", "tipeHa"),
    (re.compile(r"\bmehuppak\b"), "mahapakh", "mehuppak"),
    (re.compile(r"\bmahpakh?\b"), "mahapakh", "mahpak(h)"),
    (re.compile(r"\bmereka\b"), "merkha", "mereka"),
    (re.compile(r"\bmerka\b"), "merkha", "merka"),
    (
        re.compile(r"\b(?:MUNACH|MEREKA|MAHPAK|ATNACH|TIFCHA)\b"),
        "adopted caps",
        "legacy CAPS",
    ),
    (re.compile(r"\b(?:ethnakhta|etnahta|etnachta)\b"), "atnaḥ / ATNAX", "etna*ta"),
    (re.compile(r"\batnach\b"), "atnaḥ (U+1E25)", "atnach"),
]


def _scan_targets():
    py_root = paths.repo_root() / "py"
    for path in py_root.rglob("*.py"):
        if "__pycache__" in path.relative_to(py_root).parts:
            continue
        yield py_root, path


def test_no_undesirable_transliterations() -> None:
    import pathlib

    this_file = pathlib.Path(__file__).resolve()
    offenders: list[str] = []
    for py_root, path in _scan_targets():
        if path.resolve() == this_file:  # the denylist necessarily names every variant
            continue
        rel = path.relative_to(py_root).as_posix()
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if _PRAGMA.search(line):
                continue
            for pattern, preferred, label in _DENYLIST:
                if pattern.search(line):
                    offenders.append(f"{rel}:{lineno}  {label} -> {preferred}")
    assert not offenders, (
        "Undesirable transliteration variants (use the preferred form, or add a"
        " `# translit-ok` pragma if the line legitimately cites an external"
        " vocabulary / Unicode name):\n  " + "\n  ".join(offenders)
    )


# --- decomposed-composite guard (#49 inverts the polarity #27 folded in here) --


def _decomposed_composites(text: str):
    """Yield (line, mark, precomposed_target) for every base+combining-mark
    pair in ``text`` whose NFC composition collapses to one code point."""
    line = 1
    for i, ch in enumerate(text):
        if ch == "\n":
            line += 1
            continue
        if i == 0 or not unicodedata.combining(ch):
            continue
        comp = unicodedata.normalize("NFC", text[i - 1] + ch)
        if len(comp) == 1:
            yield line, ch, comp


def test_no_decomposed_composites_tree_wide() -> None:
    offenders: list[str] = []
    for py_root, path in _scan_targets():
        rel = path.relative_to(py_root).as_posix()
        text = path.read_text(encoding="utf-8")
        for line, mark, comp in _decomposed_composites(text):
            name = unicodedata.name(mark, "?")
            offenders.append(
                f"{rel}:{line}  U+{ord(mark):04X} {name} -> write precomposed U+{ord(comp):04X}"
            )
    assert not offenders, (
        "Use precomposed (NFC) forms, not decomposed base+combining-mark"
        " sequences:\n  " + "\n  ".join(offenders)
    )
