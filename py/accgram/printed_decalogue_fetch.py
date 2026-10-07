r"""Read the eight Decalogue accentuations of he.wikisource's base page (issue wlc-utils#52).

``build_payload`` reads the readings out of ``עשרת הדברות בסיס/טעמים`` -- the base page
every printed-vs-manuscript comparison table on Wikisource transcludes -- for the
grammaticality checker (``printed_decalogue.py``) and the transcription harness
(``edition_transcription.py``). ``printed_decalogue.load_source`` gives it the page as
the Wikisource download mirrors it, ``in/mam-ws-special/decalogue-base.mediawiki``.
Until 2026-10-07 a network subcommand of this module wrote the payload to a vendored
``in/accgram/printed_decalogue_teamim.json``; by Ben's decision of that day every
reader moved to the mirror, the same page at the same revision.

The base page spells out, fully accented, all eight versions:

    {שמות, דברים} × {טעם תחתון, טעם עליון} × {(טבריה), (דפוסים)}
    = {Exodus, Deuteronomy} × {taxton (lower), elyon (upper)} × {manuscript, printed}

TWO REPRESENTATIONS PER VERSION, and the distinction between them is the whole point of issue
wlc-utils#74:

  * ``chanted_verses`` -- the FOLDED, scanner-ready form.  Every wiki template is resolved to
    plain pointed text (see ``_resolve_templates``), so what a consumer reads is exactly what
    the old single-representation fetch produced.  Issue wlc-utils#74 left this field
    byte-for-byte unchanged, so every existing consumer kept its behaviour.
  * ``faithful_chanted_verses`` -- the FAITHFUL form.  Only the ``<קטע>`` section tags are
    stripped; the templates below are left in place, so it preserves three distinctions the
    fold discards.  ``chanted_verses`` is *derived* from it (``_fold_verse``), and the build
    fails if the two disagree -- so the faithful field cannot drift from the folded one.

The three distinctions the fold discards and the faithful field keeps:

  * ``{{מ:לגרמיה}}`` vs ``{{מ:פסק}}`` -- BOTH fold to a paseq (U+05C0) glued onto the
    preceding word (WLC's attached convention; a munax+paseq is then read as legarmeh by the
    scanner), so the folded form cannot say WHICH kind of vertical stroke stands there.  The
    faithful form can, which is what lets a printed-tradition transcription's legarmeh/paseq
    claims be checked against the p-trad strand's OWN reference (issue wlc-utils#74).  For the m-trad
    half, issue wlc-utils#68 checked this field against MAM-parsed-plus -- which carries the same
    distinction in its own ``מ:לגרמיה-2``/``מ:פסק`` templates -- and found the two agree on
    every stroke, so either may be used; ``decalogue_m_trad`` is the comparison.
    ``edition_transcription.reference_pasoleg_kinds`` reads them back out.
  * ``{{כו"ק|ketiv|qere}}`` -- folds to the qere (the accented form the reading chants); the
    faithful form keeps the ketiv too.
  * paragraph / pisqa markers ``{{ססס}}`` ``{{סס2}}`` ``{{סס}}`` ``{{פפ}}`` -- fold to nothing
    (they carry no accent; a pisqa be'emtsa pasuq sits *inside* a chanted verse, which is
    delimited only by sof pasuq).  The faithful form keeps them, setumah/petuxah and all.

  * ``{{מ:קמץ|ד=X|ס=Y}}`` -- resolved to the ``ד`` (default) qamats-qatan display form ``X`` in
    BOTH forms.  This is not one of the three preserved distinctions (the ``ס`` alternate is a
    display choice, not a masoretic fact the harness checks), so the faithful field keeps the
    template only incidentally, as the least-processing rule that also keeps the three above.

The payload records the source page's revision id and revision timestamp for provenance,
which ``printed_decalogue.load_source`` takes from the mirror's manifest.
"""

from __future__ import annotations

import re

PASEQ = "\N{HEBREW PUNCTUATION PASEQ}"
SOF_PASUQ = "\N{HEBREW PUNCTUATION SOF PASUQ}"

PAGE_TITLE = "עשרת הדברות בסיס/טעמים"

# (book, reading, tradition, wikisource section name).  ``book`` is the WLC 2-char code.
_SECTIONS: tuple[tuple[str, str, str, str], ...] = (
    ("ex", "taxton", "manuscript", "שמות טעם תחתון (טבריה)"),
    ("ex", "elyon", "manuscript", "שמות טעם עליון (טבריה)"),
    ("ex", "taxton", "printed", "שמות טעם תחתון (דפוסים)"),
    ("ex", "elyon", "printed", "שמות טעם עליון (דפוסים)"),
    ("dt", "taxton", "manuscript", "דברים טעם תחתון (טבריה)"),
    ("dt", "elyon", "manuscript", "דברים טעם עליון (טבריה)"),
    ("dt", "taxton", "printed", "דברים טעם תחתון (דפוסים)"),
    ("dt", "elyon", "printed", "דברים טעם עליון (דפוסים)"),
)


def _extract_section(text: str, name: str) -> str:
    start = f"<קטע התחלה={name}/>"
    end = f"<קטע סוף={name}/>"
    i = text.index(start) + len(start)
    j = text.index(end, i)
    return text[i:j]


def _strip_section_tags(section: str) -> str:
    """Remove the ``<קטע התחלה=.../>`` / ``<קטע סוף=.../>`` transclusion markers.

    Pure structure, no accent or masoretic content, so stripping them is the one resolution
    the FAITHFUL form shares with the folded one -- everything else the fold does is discarded
    information the faithful form keeps.
    """
    section = re.sub(r"<קטע התחלה=[^/]*/>", "", section)
    section = re.sub(r"<קטע סוף=[^/]*/>", "", section)
    return section


def _resolve_templates(section: str) -> str:
    section = _strip_section_tags(section)
    section = section.replace("{{מ:לגרמיה}}", PASEQ + " ")
    section = section.replace("{{מ:פסק}}", PASEQ + " ")
    section = re.sub(r"\{\{מ:קמץ\|ד=([^|]*)\|ס=[^}]*\}\}", r"\1", section)
    section = re.sub(r'\{\{כו"ק\|[^|]*\|([^}]*)\}\}', r"\1", section)
    for marker in ("{{ססס}}", "{{סס2}}", "{{סס}}", "{{פפ}}", "{{פ}}"):
        section = section.replace(marker, " ")
    if "{{" in section:
        raise ValueError(f"Unresolved template remains in section: {section[:120]!r}")
    return section


def _split_at_sof_pasuq(section: str) -> list[str]:
    """Split into chanted verses (whitespace-normalized, empties dropped), at sof pasuq only.

    Shared by the folded and faithful passes: a wiki template never contains a sof pasuq and
    the fold never adds or removes one, so segmenting before resolving (the faithful pass) and
    after resolving (the folded pass) yield the same verse list -- which ``build_payload``
    checks verse for verse."""
    out: list[str] = []
    cur: list[str] = []
    for ch in section:
        cur.append(ch)
        if ch == SOF_PASUQ:
            out.append("".join(cur))
            cur = []
    tail = "".join(cur).strip()
    if tail:
        out.append(tail)
    return [cv for cv in (re.sub(r"\s+", " ", c).strip() for c in out) if cv]


def _segment_chanted_verses(section: str) -> list[str]:
    """The folded chanted verses: resolve every template, then split at sof pasuq."""
    return _split_at_sof_pasuq(_resolve_templates(section))


def _faithful_verses(section: str) -> list[str]:
    """The faithful chanted verses: strip only the section tags, then split at sof pasuq.

    The legarmeh/paseq, ketiv/qere and paragraph/pisqa templates survive, so nothing the
    fold discards is lost.  Index-aligned with ``_segment_chanted_verses`` on the same section
    (both split at sof pasuq); ``_fold_verse`` turns each entry back into its folded twin.
    """
    return _split_at_sof_pasuq(_strip_section_tags(section))


def _fold_verse(faithful_verse: str) -> str:
    """One faithful verse -> its folded form, the derived step existing consumers see.

    A chanted verse holds exactly one sof pasuq (at its end), so resolving templates cannot
    introduce a verse split; this is ``_segment_chanted_verses``'s per-verse work without the
    re-split."""
    return re.sub(r"\s+", " ", _resolve_templates(faithful_verse)).strip()


def build_payload(wikitext: str, provenance: dict[str, object]) -> dict[str, object]:
    versions: list[dict[str, object]] = []
    for book, reading, tradition, name in _SECTIONS:
        section = _extract_section(wikitext, name)
        chanted_verses = _segment_chanted_verses(section)
        faithful_chanted_verses = _faithful_verses(section)
        # The faithful field must fold back to the folded one exactly, or ``chanted_verses``
        # -- the field every existing consumer reads -- would no longer be the derived twin of
        # the page's text.  Build-fails-on-drift, in the style of resolve_readings.
        refolded = [_fold_verse(fv) for fv in faithful_chanted_verses]
        if refolded != chanted_verses:
            raise ValueError(
                f"{book}/{reading}/{tradition}: faithful verses do not fold to the folded "
                f"ones ({len(refolded)} vs {len(chanted_verses)} verses)"
            )
        versions.append(
            {
                "book": book,
                "reading": reading,
                "tradition": tradition,
                "section": name,
                "chanted_verses": chanted_verses,
                "faithful_chanted_verses": faithful_chanted_verses,
            }
        )
    provenance = dict(provenance)
    provenance["resolution_notes"] = (
        "Two representations per version. chanted_verses is the FOLDED, scanner-ready form: "
        "{{מ:לגרמיה}}/{{מ:פסק}} -> U+05C0 paseq folded onto the preceding word; "
        '{{מ:קמץ|ד=X|ס=Y}} -> X; {{כו"ק|ketiv|qere}} -> qere; paragraph/pisqa markers dropped; '
        "inner <קטע> tags stripped. faithful_chanted_verses strips ONLY the <קטע> tags, "
        "keeping those templates in place, so legarmeh vs narrow-sense paseq, ketiv/qere and "
        "the setumah/petuxah breaks are preserved (issue wlc-utils#74); chanted_verses is derived from "
        "it by folding. Both split into chanted verses at sof pasuq."
    )
    return {"provenance": provenance, "versions": versions}
