"""Guard: no known-banned wording in the prose we write about cantillation.

Sibling of ``test_transliterations.py``, and deliberately the same shape -- a
mechanical lint over the tree, which is one of the two kinds of test that have
ever found anything here (``doc/agent-planning-principles.md`` SS"Generated
Outputs Are the Tests").  A decidable property of the SOURCE TEXT, not of
behavior: does this line contain a phrase Ben has banned?

The rules themselves are not defined here.  Their canonical home is the
user-level ``hebrew-prose`` skill (``~/.claude/skills/hebrew-prose/``, tracked
in ``github-misc`` at ``dot-claude/skills/``); ``CLAUDE.md``'s opening section
points at it.  This file only enforces the subset that is mechanically
checkable, and each row cites the rule it comes from.

Any single line may opt out with an inline ``# prose-ok`` pragma (cf.
``# translit-ok`` next door), which is what a line legitimately CITING a banned
phrase in order to reject it needs -- the guardrail comments that record a
replaced convention are exactly that, and there is no way to write one without
naming the thing.

WHAT IS SCANNED.  Every non-vendored ``py/**/*.py``, plus the committed
renderings the page modules generate: ``gh-pages/wlc/accgram/*.html`` and
``out/accgram/**/*.json``, scanned as plain text (wlc-utils#87 item 19 -- the wlc-utils#80 sweep
of 2026-07-27 fixed the module sources but left
``out/accgram/dual-cant/_dual_cant.json`` holding the swept wording for two
days, because nothing linted the artifacts).  A hit in an artifact never means
"edit the artifact": either the generating module still produces the phrase
(fix it there) or the artifact is stale (regenerate it; the artifact then
clears on its own).  ``doc/*.md`` is deliberately NOT scanned: the
review-findings and plan docs quote banned phrasings in order to discuss and
reject them, so linting them would flag the quotations.

KNOWN, DELIBERATE LIMITATIONS (wlc-utils#87 item 20), recorded here so they are a
choice and not an unknown:

* ``_SUBJECTS`` hardcodes the edition names, so a rename (as the
  simanim -> simtiq/simtan rename did, in the very week this lint was new)
  silently NARROWS the lint instead of breaking it: the old name stops
  matching and nothing fails.  No existing constant holds these rendered
  short names -- ``printed_decalogue_strands.py`` has transcription stems and
  Hebrew words, not "Koren"/"SimTiq"/"SimTan" -- so there is nothing to derive
  the tuple from without building a constant just for this lint.  Whoever
  renames an edition must update ``_SUBJECTS`` by hand.
* The subject-anchored agentive pattern requires the verb to follow its
  subject directly and in the singular.  A plural subject with an interposed
  phrase -- "the seven chanted words before those marks carry ..." (wlc-utils#87 item
  6) -- escapes, and loosening the anchor enough to catch it would flag the
  honest uses the anchor exists to spare.  (Item 6's OTHER escape, subject
  and verb split across two source lines, IS caught: every scan below runs
  over adjacent line pairs.)

Run:
    .venv/Scripts/python.exe -m pytest py/tests/test_prose_conventions.py -v

DELIBERATELY NOT IN THE DENYLIST YET, with today's tree-wide counts, so a later
session knows these were weighed rather than missed.  Each needs a prose sweep
BEFORE its rule can be switched on, and a sweep is not a lint's job:

* ``witness`` (139 hits) -- banned outright (say edition / manuscript / the
  thing's own name).  The printed-Decalogue trio is clean; ``almost_errors``,
  ``poetic`` and ``telg-doc-notes`` are not, and they carry the bulk.
* ``prose books`` / ``poetic books`` (8 hits) -- the division is by VERSE, never
  by book, because Job's prose frame is poetically booked and prose cantillated.
  Held back because "the 21 books" as a NAME for the corpus stays fine, and
  telling the name from the division is a judgment call per site, not a regex.
* ``ga'ya`` (5 hits) -- wlc-utils standardizes on "meteg", but 3 of the 5 are
  quotations or the established phenomenon name "qadma-as-ga'ya", which are
  exempt by the rule itself.
* ``pasuq`` as a UNIT name (256 hits) -- say "chanted verse".  The count is
  dominated by the MARK name "sof pasuq", which stays; no anchored pattern
  separating the two survived review.
* the nameless possessive ``its strand`` / ``their strand`` (2026-07-27) --
  where a printed edition is compared against the vendored reference, NAME the
  reference: "Koren's Exodus תחתון has no difference from Wikisource", never
  "from its strand", which reads as though the edition owned a strand or as
  though which strand is "its" were settled rather than the finding under test.
  "its **Wikisource** strand" is the established phrasing and is fine.  The
  printed-Decalogue family has been swept, so a regex would pass today -- but it
  would pass by luck.  The same two words are RIGHT of the four idealized
  strands themselves (a reading's own strand, the pair that identifies it, the
  Hebrew word תחתון / עליון that ``render_reading_name`` returns), and telling an
  edition-vs-reference sentence from a strands-in-general one is a judgment call
  per site, exactly as with "prose books" above.  Marking the honest ones
  ``# prose-ok`` would misuse the pragma, which is for a line CITING a banned
  phrase in order to reject it.
"""

from __future__ import annotations

import pathlib
import re

from mb_cmn import paths

# Lines bearing this pragma are exempt.
_PRAGMA = re.compile(r"#\s*prose-ok")

# A corpus, manuscript, edition or unit of text is an OBJECT, not an agent, and
# the plain word for what it does with a mark is "has".  Ben, 2026-07-24: "you
# seem very averse to plain *has*: we've had to work hard to exterminate
# synonyms like *carries*, *reads*, and *prints*"; and 2026-07-26, on a fresh
# crop of *bears*: "simply *has* not *bears*".  Each of those was its own
# cleanup, which is why this is a lint and not a note.
#
# Anchored on the SUBJECT, so the many honest uses survive untouched: a function
# that writes JSON, a reader that reads a file, a scanner that carries state.
# Hardcoded by necessity; see KNOWN, DELIBERATE LIMITATIONS in the module
# docstring for what a rename does to this tuple.
_SUBJECTS = (
    "WLC",
    "UXLC",
    "MAM",
    "CTR",
    "Koren",
    "SimTiq",
    "SimTan",
    "the LC",
    "the manuscript",
    "the edition",
    "the atom",
    "the compound",
    "the chanted word",
)
# "shows" is allowed of a publisher or a site (Chabad shows X), where the agency
# is real -- but not of a text, which is why it is here rather than exempted.
_AGENTIVE = (
    "writes",
    "wrote",
    "codes",
    "coded",
    "carries",
    "carried",
    "reads",
    "prints",
    "bears",
    "shows",
    "displays",
    "presents",
)
_AGENTIVE_PATTERN = re.compile(
    r"\b(?:" + "|".join(_SUBJECTS) + r")(?:'s)?\s+(?:" + "|".join(_AGENTIVE) + r")\b"
)

# (compiled pattern, what to write instead, short label)
_DENYLIST: list[tuple[re.Pattern[str], str, str]] = [
    (_AGENTIVE_PATTERN, 'just say "has" (or "lacks")', "agentive verb"),
    # A maqaf JOINS atoms into a chanted word and sof pasuq ENDS a chanted verse;
    # only a space divides words.  Umbrella noun: punctuation, or grouping.
    (
        re.compile(r"\bword.division\b", re.IGNORECASE),
        "punctuation / grouping",
        "word-division",
    ),
    # "Proclitic" asserts a grammatical role nothing here checks, where the
    # atom's POSITION in the compound is what is measured.
    (
        re.compile(r"\bproclitics?\b", re.IGNORECASE),
        "a non-final atom of a compound",
        "proclitic",
    ),
]

# EVERY scan below runs over ADJACENT LINE PAIRS, not single lines, on quote-
# and whitespace-normalized text: a phrase splits across two source lines
# inside an implicitly concatenated string literal (`no cantillation\n"
# "accent`), and a subject parts from its verb at a line break ("There too
# Koren\nshows ..." -- wlc-utils#87 item 6), so a line-based grep misses both, and that
# is exactly how each has hidden before.  Pairing (rather than scanning the
# whole file as one string) keeps a real line number in the message and keeps
# the `# prose-ok` pragma usable.
_CANTILLATION_ACCENT = re.compile(r"\bcantillation\s+accents?\b", re.IGNORECASE)
_NOISE = re.compile(r"[\"'\s]+")


def _scan_targets():
    """Yield (root, path) pairs; offender paths are shown relative to root.

    ONE ROOT SINCE 2026-08-12.  The sources and the committed renderings they generate
    are both under this repo now.  They were two roots until then -- the renderings
    stayed in wlc-utils when the Python moved out of it, and came home at Phase 3 of
    ``doc/PLAN-evacuate-the-rest-of-wlc-utils.md``.  Each pair still carries a root, so
    an offender reads as a repo-relative path rather than an absolute one, and so the
    shape survives if a second tree is ever scanned again.
    """
    repo_root = paths.repo_root()
    py_root = repo_root / "py"
    this_file = pathlib.Path(__file__).resolve()
    for path in sorted(py_root.rglob("*.py")):
        if "__pycache__" in path.relative_to(py_root).parts:
            continue
        if path.resolve() == this_file:  # names every banned phrase by necessity
            continue
        yield repo_root, path
    # The committed artifacts (module docstring, WHAT IS SCANNED).  Missing
    # inputs FAIL rather than silently narrowing the scan (cf. the skip
    # policy: a missing input must never report green).
    html = sorted((paths.wlc_pages_dir() / "accgram").glob("*.html"))
    json_files = sorted((paths.out_dir() / "accgram").rglob("*.json"))
    assert html, "no gh-pages/wlc/accgram/*.html found -- artifact scan would be empty"
    assert json_files, "no out/accgram/**/*.json found -- artifact scan would be empty"
    for path in html + json_files:
        yield repo_root, path


def test_no_banned_prose_wording() -> None:
    offenders: list[str] = []
    for root, path in _scan_targets():
        rel = path.relative_to(root).as_posix()
        lines = path.read_text(encoding="utf-8").splitlines()
        for i, line in enumerate(lines):
            nxt = lines[i + 1] if i + 1 < len(lines) else ""
            if _PRAGMA.search(line) or _PRAGMA.search(nxt):
                continue
            head = _NOISE.sub(" ", line)
            pair = _NOISE.sub(" ", f"{line} {nxt}")
            for pattern, preferred, label in _DENYLIST:
                found = pattern.search(pair)
                # A match lying wholly inside ``nxt`` belongs to the NEXT pair,
                # which will report it -- otherwise every same-line hit is
                # reported twice.
                if found and found.start() <= len(head):
                    offenders.append(
                        f"{rel}:{i + 1}  {label} ({found.group(0).strip()})"
                        f" -> {preferred}"
                    )
    assert not offenders, (
        "Banned wording (see the `hebrew-prose` skill; or add a `# prose-ok`"
        " pragma if the line legitimately cites the phrase in order to reject"
        " it):\n  " + "\n  ".join(offenders)
    )


def test_no_cantillation_accent_phrase() -> None:
    """ "Cantillation accent" is redundant: in an accent-grammar context the
    subject is already cantillation, so the qualifier says nothing.  Distinct
    from -- and compatible with -- preferring the NOUN "cantillation" to
    "accentuation", which is Ben's other standing choice and is not linted."""
    offenders: list[str] = []
    for root, path in _scan_targets():
        rel = path.relative_to(root).as_posix()
        lines = path.read_text(encoding="utf-8").splitlines()
        for i, line in enumerate(lines):
            nxt = lines[i + 1] if i + 1 < len(lines) else ""
            if _PRAGMA.search(line) or _PRAGMA.search(nxt):
                continue
            found = _CANTILLATION_ACCENT.search(_NOISE.sub(" ", f"{line} {nxt}"))
            # A match lying wholly inside ``nxt`` belongs to the NEXT pair, which
            # will report it -- otherwise every same-line hit is reported twice.
            if found and found.start() <= len(_NOISE.sub(" ", line)):
                offenders.append(f"{rel}:{i + 1}  {found.group(0)!r} -> just 'accent'")
    assert (
        not offenders
    ), 'Drop the redundant "cantillation" before "accent":\n  ' + "\n  ".join(offenders)
