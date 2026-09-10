"""Lint: this repo's hand-authored prose must be in MAM's mark order.

WHY THIS EXISTS

``CLAUDE.md``'s first section says a cluster in Unicode-normal order "is always
something hand-authored", names the way in -- "a paste through anything that
normalizes, a browser above all" -- and, until this file, ended "so the check is
yours to run". On 2026-09-09 someone ran it, and 132 clusters in 16 tracked prose
files were in the other order: 22 in the three files the report named, and 110 more
the same scan turned up, spread over ``doc/`` (13 files), ``holman/doc/``,
``leningrad/page-snips/`` and ``uxlc/doc/clc-design.md``. No letter and no mark
differed, only their order, so nothing rendered wrong and only a byte comparison
could see it -- which is exactly the failure mode that section warns about, and
exactly why a lint beats a reader.

The prose was the gap, not the data. ``py/py_misc/uni_check.py`` asserts the order
on every element sequence a generator renders, and MAM's shipped data was checked
clean on 2026-08-04. Three mark-order checks already existed, and between them they
missed every one of those 16 files:

  * ``test_mam_simple_mark_order.py`` -- MAM-simple's non-corpus tree, plus
    ``py/versification_and_cantillation/doc.py`` and the page it generates.
  * ``check_mark_order.py`` -- the ``.py`` of the four repos ``py/repo_scopes.py``
    named then, and the Ben-authored ``.json`` of three of them, that module's
    ``corpus_roots()`` omitting the Leningrad tree, which "contributes no mark-order
    scope". Since 2026-09-10, when the Leningrad code was deleted, both lists name
    the same three repos.
  * ``test_aleppo_page_mark_order.py`` -- ``gh-pages/aleppo/*.html``, which
    ``main_ac_gen_index_flat_annotated.py`` generates, so output rather than source.

WHAT IT COVERS, AND WHY NOT MORE

Every tracked ``.md`` in the repo, the ``.html`` under ``doc/``, and the ``.txt``
under ``in/accgram/edition_transcriptions/`` -- 203 files at ``5e7f0d6b``, one second
to check, so there is no cost argument for narrowing it. Re-establish with
``git ls-files -- "*.md" "doc/*.html" "in/accgram/edition_transcriptions/*.txt"``
rather than trusting that figure: it rises with every ``.md`` added, so a larger
number is growth and not a mismatch.

Widening BY FILE TYPE is what fails, and each way fails for the same reason -- what
the wider type catches is not hand-authored prose. All ``.html`` would take in 67
offending files: 36 under ``uxlc/in/UXLC-notes/``, an input capture and the majority
of them; 28 generated under ``gh-pages/``; and 3 byte-verbatim under
``misc/*/img-sources/``. All ``.txt`` would take in 15 offending files, and 11 of
those are genuine captures: 6 under ``uxlc/out/UXLC-misc/`` and 1 under
``uxlc/in/UXLC-misc/``, the UXLC change lists; 2 under ``aleppo/aleppo-wiki/``,
snapshots of hand work as it was published on Wikisource; and 2 under
``misc/zarqa-table-diff/``, two external sources captured so they can be diffed
against each other.

THE TRANSCRIPTION DIRECTORY IS A NAMED EXCEPTION, AND NOT THAT BLANKET WIDENING.
The remaining 4 of those 15 are the ``in/accgram/edition_transcriptions/*.txt``
whose hand-written ``#`` headers carry Ben's notes on what each printed edition does
at a given place, quoting pointed Hebrew -- prose pasted through something that
normalized it, the same defect as the 132 clusters above rather than a different
kind. Ben's decision, 2026-09-09, was to cover them, and the pathspec names that one
directory rather than the file type. It takes in no capture: all 12 ``.txt`` there
are Ben-authored, and the derived body beneath each header is built from the
``.json`` beside it by ``py/main_edition_transcription.py``, which stores accent
names in Hebrew abbreviations and no vowel point at all -- so a derived body holds no
cluster that could tell the two orders apart. The argument above therefore stands
unweakened: 11 of the 15 offending ``.txt`` are captures, and this pathspec reaches
none of them.

The data trees carry their source's order by design and must never be repaired:
``in/mam-ws/`` is a download that is inherently normalized (Ben, 2026-09-09),
``out/mam-ws-bot/proto/`` and ``out/mam-ws-parsed-fmt-2/`` are its faithful
intermediates -- their per-book cluster counts match it exactly -- and the pipeline
denormalizes downstream, which is why ``MAM-parsed/`` and ``MAM-for-Sefaria/`` are
clean. ``in/mam-ws-intro/`` is exempted by name in ``CLAUDE.md`` on the same ground.
None of those is ``.md``, so the file-type scope excludes them without an exclusion
list, and ``py/repo_scopes.py`` records why a repo-wide sweep has no meaning here.

So a future capture that arrives as ``.md`` is the one case that needs an entry in
``_EXCLUDED``, with the reason it is byte-verbatim. It is NOT a reason to loosen the
lint, and never a reason to normalize.

A MISSING INPUT FAILS RATHER THAN SKIPS

``CLAUDE.md`` "Writing tests" requires it, and this lint has two ways it could go
quiet rather than one. ``_FLOOR`` catches a listing that collapsed altogether; the
separate ``absent`` assertion catches the narrower case of a path ``git ls-files``
reports that the working tree does not hold. That case cannot arise in an ordinary
checkout -- 0 of the 203 files in scope at ``5e7f0d6b`` -- but until 2026-09-09 it
was passed over in silence, which is the shape that section warns about. It is
deliberately its own assertion rather than another entry in ``offenders``: a file
that is not there has no Hebrew to be in the wrong order, so reporting it under the
mark-order message would be a true failure carrying a false reason. Ben's decision,
2026-09-09.

WHAT MAM'S MARK ORDER IS, AND WHAT IT IS NOT

``mb_cmn/uni_denorm.py`` is the authority. Four marks come first -- shin dot, sin
dot, dagesh/mapiq, rafe -- and every other mark keeps the relative order it already
had, so only those four have a declared place. A vowel and an accent pass in either
order, and ``has_std_mark_order`` says nothing about which of them comes first. This
lint is therefore not a canonical-form check and must not be read as one.
"""

import subprocess

from mb_cmn import paths, uni_denorm

# Byte-verbatim captures that happen to be .md. Empty on 2026-09-09: every capture in
# the tree is .txt, .html, .json, .xml or .mediawiki. An entry here needs the reason
# it is verbatim, not merely the fact that it fails.
_EXCLUDED: frozenset[str] = frozenset()

# Far below the number of files in scope, and here only to catch a pathspec that
# swallowed everything -- not to assert a tree size. It deliberately carries no
# absolute figure, because the scope grows with every .md added; the docstring above
# gives that count with the revision it was measured at.
_FLOOR = 100


def _tracked_prose_files() -> list[str]:
    """Every tracked ``.md``, the ``.html`` under ``doc/``, the transcription ``.txt``.

    A git pathspec's ``*`` crosses ``/``, so ``*.md`` reaches every depth and
    ``doc/*.html`` reaches every depth under ``doc/``. The third element names one
    directory outright; the docstring above says why that directory and no other
    ``.txt``.
    """
    result = subprocess.run(
        [
            "git",
            "ls-files",
            "--",
            "*.md",
            "doc/*.html",
            "in/accgram/edition_transcriptions/*.txt",
        ],
        cwd=paths.repo_root(),
        capture_output=True,
        encoding="utf-8",
        check=True,
    )
    return [
        rel
        for rel in (
            line.strip().replace("\\", "/") for line in result.stdout.split("\n")
        )
        if rel and rel not in _EXCLUDED
    ]


def test_hand_authored_prose_is_in_mam_mark_order():
    in_scope = _tracked_prose_files()
    assert len(in_scope) > _FLOOR, (
        f"Only {len(in_scope)} prose files in scope (floor {_FLOOR}) --"
        " the pathspec or the exclusion set may be too broad."
    )

    absent = []
    offenders = []
    for rel in in_scope:
        full = paths.repo_root() / rel
        if not full.is_file():
            absent.append(rel)
            continue
        text = full.read_text(encoding="utf-8")
        if uni_denorm.has_std_mark_order(text):
            continue
        for num, line in enumerate(text.split("\n"), 1):
            if not uni_denorm.has_std_mark_order(line):
                offenders.append(f"{rel}:{num}")

    # Asserted before the mark-order result, not after: a working tree out of step
    # with the index makes that result untrustworthy rather than merely incomplete.
    assert not absent, (
        "git ls-files lists these prose files and the working tree does not hold"
        " them, so this lint checked fewer files than it listed. That is a working"
        " tree out of step with the index, NOT a mark-order defect: restore the"
        f" files, or narrow the pathspec if they are gone for good. {absent}"
    )

    assert not offenders, (
        "Found hand-authored Hebrew not in MAM's mark order. Do NOT fix this by"
        " running unicodedata.normalize, which is what puts it in the wrong order in"
        " the first place: pass the text through uni_denorm.give_std_mark_order, or"
        " lift the word from MAM-simple/xml-vtrad-mam, which has it already."
        f" {offenders}"
    )
