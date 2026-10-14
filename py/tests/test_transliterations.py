"""Guard: no known-undesirable transliteration variant in our Python source.

Two checks run over every ``py/**/*.py`` in this repo (``__pycache__`` aside); any
single line may opt out with an inline ``# translit-ok`` pragma (self-documenting,
travels with the line, cf. ``# noqa``).  ``mb_cmn``, ``mb_misc`` and ``mb_diff_mpu``
used to be skipped as "vendored from a sibling repo, not ours to normalize"; they are
native here, they are the SOURCE the other repos vendor FROM, and the exclusion was
hiding half the hits, so it is gone.  The two checks:

1. ``test_no_undesirable_transliterations`` -- a denylist of spelling variants
   that the wlc-utils#13 standardization retired: ``zinor``->``tsinnor`` (wlc-utils#30),
   ``merka``->``merkha``, ``atnach``->``atnax``, ``sinnor``->``tsinnor``, the
   het-as-plain-``h`` forms, and a few Goerwitz/legacy capitalizations.  No
   lookahead is needed to shield the good form: the preferred spellings are
   precomposed ``ḥ`` (U+1E25), which shares no ASCII substring with a pattern
   like ``munah``, so the good spelling can never trip it.

2. ``test_no_decomposed_composites_tree_wide`` -- wlc-utils#49 inverts the polarity
   wlc-utils#27 established: the repo standard is now NFC (precomposed), so any
   decomposed base+combining-mark pair with a single-codepoint NFC
   composition (e.g. ``h`` + U+0323) is flagged.

Legitimate exemptions (external vocabularies / verbatim citations), each tagged
``# translit-ok`` in the source and enumerated in issue wlc-utils#26:

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

The separate rendered-prose check below enforces only the four approved noun
spellings, using the plural lint's quotation/adaptation/identifier boundaries.

Run:
    .venv/Scripts/python.exe py/main_test.py py/tests/test_transliterations.py -v
"""

from __future__ import annotations

import re
import subprocess
import unicodedata

from mb_cmn import paths, unicode_data
from mb_cmn import hebrew_name_plurals as html_prose
from mb_cmn.git_process import git_command

# Lines bearing this pragma are exempt from the denylist scan.
_PRAGMA = re.compile(r"#\s*translit-ok")

# (compiled pattern, preferred spelling, short label).  Patterns are anchored so the
# good precomposed forms and the genuine Unicode names never match; see the per-row
# notes in issue wlc-utils#26's research comment.
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


# --- decomposed-composite guard (wlc-utils#49 inverts the polarity wlc-utils#27 folded in here) --


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


# This distinct HTML check covers only Ben's four approved spelling choices.
# Other source spellings retain the existing denylist and its own exemptions.
# Each variant maps to its chosen singular and plural, the plural taking the
# plural lint's default noun or, for parashah, the accepted parashot.
_RENDERED_VARIANTS = {
    "qeri": ("qere", "qere words"),
    "aliya": ("aliyah", "aliyah portions"),
    "parasha": ("parashah", "parashot"),
    "masora": ("masorah", "masorah notes"),
}
_RENDERED_VARIANT_PATTERN = re.compile(
    r"\b(" + "|".join(_RENDERED_VARIANTS) + r")(s|es|im|ot)?\b", re.I
)


def _rendered_variant_findings(html: str, rel: str) -> list[html_prose.Finding]:
    if not _RENDERED_VARIANT_PATTERN.search(html):
        return []
    text, lines = html_prose.authored_html_text(html, rel)
    # An exact Unicode name is literal vocabulary, not our prose spelling.
    unicode_name = unicode_data.name("\u05af")
    text = text.replace(unicode_name, " " * len(unicode_name))
    found = []
    for match in _RENDERED_VARIANT_PATTERN.finditer(text):
        if html_prose.is_technical_reference(text, match):
            continue
        singular, plural = _RENDERED_VARIANTS[match[1].lower()]
        preferred = plural if match[2] else singular
        if match[1].isupper():
            preferred = preferred.upper()
        elif match[1][0].isupper():
            preferred = preferred.capitalize()
        found.append(html_prose.Finding(lines[match.start()], match[0], preferred))
    return found


def test_no_nonstandard_noun_transliterations_in_rendered_prose() -> None:
    root = paths.repo_root()
    tracked = (
        subprocess.check_output(git_command(root, "ls-files", "-z", "--", "gh-pages"))
        .decode("utf-8")
        .split("\0")
    )
    html = [rel for rel in tracked if rel.endswith(".html")]
    assert html, "no tracked gh-pages HTML: transliteration lint would be empty"
    offenders = []
    for rel in html:
        for finding in _rendered_variant_findings(
            (root / rel).read_text(encoding="utf-8"), rel
        ):
            offenders.append(
                f"{rel}:{finding.line}: {finding.term} -> {finding.preferred}"
            )
    assert (
        not offenders
    ), "Use the chosen transliteration in authored prose:\n" + "\n".join(offenders)


def test_rendered_variant_quotes_adaptations_and_identifiers() -> None:
    scan = _rendered_variant_findings
    rel = "gh-pages/example.html"
    assert [f.preferred for f in scan("<p>qeri, aliya, parasha, masora.</p>", rel)] == [
        "qere",
        "aliyah",
        "parashah",
        "masorah",
    ]
    assert [f.preferred for f in scan("<p>qeris and masoras.</p>", rel)] == [
        "qere words",
        "masorah notes",
    ]
    assert not scan(
        "<q>qeri maqafs</q><blockquote>aliya metegs</blockquote>"
        '<span data-hebrew-plural-ok="literal source">parasha shewas</span>'
        "<code>qeri</code><p>unit.qeri qeri_key qeri.txt /aliya/</p>"
        '<a href="parasha.html" class="masora" id="qeri">link</a>',
        rel,
    )
    assert not html_prose.html_findings("<q>qeri maqafs</q><p>qere forms</p>", rel)
    assert html_prose.html_findings("<p>maqafs</p>", rel)
    assert scan("<p>qeri</p>", rel)
    assert not scan(
        "<p>qeri aliya parasha masora</p>", "gh-pages/yeivin-itm/adapted-prose.html"
    )
    assert scan("<p>qeri</p>", "gh-pages/MAM-with-doc/misc/notes_on_aliyot.html")
    clc = "gh-pages/clc/Genesis.html"
    phrase = (
        "The Masora Circle over the word refers to the number '4' in the left margin."
    )
    assert not scan("<p>" + phrase + "</p>", clc)
    assert scan("<p>" + phrase + "</p><p>masora</p>", clc)
    unicode_name = unicode_data.name("\u05af")
    assert not scan("<p>" + unicode_name + "</p>", rel)
    assert [f.term for f in scan("<p>" + unicode_name + " and MASORA.</p>", rel)] == [
        "MASORA"
    ]


def test_bhs_ketib_regions_exempt_only_the_retained_source_wording() -> None:
    rel = "gh-pages/MAM-with-doc/misc/urwotm_2_saying_the_quiet_part_out_loud.html"
    html = (paths.repo_root() / rel).read_text(encoding="utf-8")
    regions = list(
        re.finditer(
            r'<(?P<tag>p|span|em) data-hebrew-plural-ok="[^"]+">'
            r"(?P<body>.*?)</(?P=tag)>",
            html,
            re.S,
        )
    )
    assert len(regions) == 3
    assert all("Ketib" in region["body"] for region in regions)
    authored, _ = html_prose.authored_html_text(html, rel)
    assert "Ketib" not in authored
    assert "which I take to mean:" in authored
    assert "unpointed" in authored  # our gloss remains checked outside its Latin term
    for region in regions:
        changed = (
            html[: region.start("body")]
            + region["body"].replace("Ketib", "qeri maqafs")
            + html[region.end("body") :]
        )
        assert not html_prose.html_findings(changed, rel)
        assert not _rendered_variant_findings(changed, rel)
        # Identical words in new authored prose on this page must still fail.
        changed += "\n<p>qeri maqafs</p>"
        assert [f.term for f in html_prose.html_findings(changed, rel)] == ["maqafs"]
        spellings = _rendered_variant_findings(changed, rel)
        assert [f.term for f in spellings] == ["qeri"]
        assert spellings[0].line == changed.count("\n") + 1
