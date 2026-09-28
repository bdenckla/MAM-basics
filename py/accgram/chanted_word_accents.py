r"""Survey: chanted words with two or more accent TOKENS, over the prose verses of the Tanakh.

A chanted word normally has one accent.  ``maqaf_nonfinal_accents`` measured one corner of the
exceptions -- an accent on a non-final atom of a maqaf compound -- and left the larger half
unmeasured, because a chanted word can also have two accents while being a single atom, and can
have both of them on a compound's final atom.  This module measures all of it, and sets Yeivin's
own inventory of the phenomenon beside the measurement so each checks the other.

Pure computation and a JSON writer -- no HTML, and DELIBERATELY none.  Run via
``main_accgram.py survey-chanted-word-accents``.  A rendered page of this was built and then
dropped (2026-07-29): ``maqaf-nonfinal-accents.html`` had meanwhile widened to ask the same
question of all three printed compounds, and the plan's own thrust is a chanted-word rule in the
checker rather than a page.  The Yeivin cross-check is recorded here, in the JSON, which is the
form it wanted.  Issue wlc-utils#86 holds the questions the survey raises and does not settle.

THE SURVEY AND THE FLAGGING PATH are both here.  ``build_survey`` measures the three corpora and
sets Yeivin's inventory beside MAM; ``classify_verse`` asks the same question of one verse at a
time, for the two paths that write verdicts -- ``prose_run._verse_record`` and
``printed_decalogue.parse_marks_body``, the second of which carries the eight Wikisource strands
and all twelve hand transcriptions.  It reads its whitelist straight off the entries the survey
checks, keyed on the TOKEN SEQUENCE and never on a verse reference: Yeivin's closed lists are the
differential check the survey runs against him, and a checker that consulted them would name a
chanted word by where it stands rather than by what it has.  What ``classify_verse`` feeds is an
additive field; ``status`` and ``tree`` are left alone.

WHETHER A CHANTED WORD NEITHER BOOK NAMES IS UNGRAMMATICAL WAS ANSWERED ON 2026-08-03, and the
answer for MAM is no, for the time being: such a chanted word is recorded and grammatical (§6
decision 5 of ``doc/PLAN-two-accents-on-one-chanted-word.md``).  ``MAM_ALLOWANCES`` is that
ruling as the flagging path reads it -- the second half of the whitelist, keyed on the chanted
word's MARK RUN with its token sequence, which is what a per-verse allowance takes so that it
cannot spread to a chanted word that merely shares the pair.  The ruling decides verdicts and
retires no measurement: ``mam_residue`` is closed against ``YEIVIN_ENTRIES`` alone, so every
divergence stays in it, and the ruling covers MAM alone, so ``wlc_chanted_word_residue_page`` is
closed the same way.

TOKENS, NOT MARKS, and that choice is the design.  The prose scanner already fuses several
written pairs into one token: a doubled stress helper (pashta, telisha qetana), the zarqa's own
helper with its zarqa, the same-letter ``mahapakh!qadma`` cluster, munax + U+05C0 as legarmeh, and
qadma...zaqef as ``METHIGAZAQEF``.  It also swallows meteg, emitting ``SILLUQ`` only for a
verse-final U+05BD before sof pasuq.  Counting tokens therefore disposes of every confound that
would otherwise have to be special-cased -- a stress helper written twice is not two accents, and
neither is a metigah-zaqef.  The METHIGAZAQEF fuse crosses a maqaf and stops at a space, so a fused
pair is always one chanted word and the survey never counts one token for two: ITM §223's leading
example is the compound Ex 35:9 ואבני־שהם, while both that section and CoS Ch. 5 §§4-6 restrict
the metigah to the chanted word of the zaqef.  ``_methigazaqef_crossings`` is the
lint that holds the scanner to it.  One confound survives and is handled here: a geresh or gershayim
written twice on one chanted word is ONE accent written twice, and the scanner does not fuse it.
``_fold_repeated_geresh`` folds such a repeat, and ``geresh_folds`` names every place it fired.

ATOM AND CHANTED WORD (issue wlc-utils#81).  An atom is one written word, between spaces or maqafs; a
chanted word is a lone atom or a whole maqaf compound, and is the unit an accent marks.  Yeivin
states outright that the two take the same rules -- ITM §302, quoted in ``YEIVIN_ENTRIES`` -- so
this survey counts both together and records which kind each hit is, rather than treating the
compound as a separate phenomenon.  Maqaf is the last rung of the one scale of separating force
(``maqaf_nonfinal_accents``' ``MAQAF_IS_THE_LAST_RUNG`` in ``printed_decalogue_strands``), not a
second ledger.

THE MARK BODY IS BUILT HERE, ATOM BY ATOM, and the WLC build is checked against
``uni_to_marks.verse_to_marks``.  The scanner reads a mark body, and a token's position is an
offset into it, so the chanted-word boundaries have to be offsets into the same string: a space
ends a chanted word and a maqaf (``-``) is an atom boundary inside one.  ``verse_to_marks``
returns the body alone, with no way back to the Unicode a chanted word came from, so
``_verse_units`` rebuilds it fragment by fragment and keeps each fragment's Unicode beside its
marks.  For WLC the rebuild is asserted equal to ``verse_to_marks``' own output, which makes the
alignment a checked fact rather than a claim.  ``word_to_marks`` is applied per ATOM in all three
corpora, as ``verse_to_marks`` applies it per verse element, so its front-loading of a prepositive
accent never crosses an atom boundary and never moves an accent onto a neighbouring atom.

THE THREE CORPORA, and what each can be asked.  WLC 4.22 and UXLC are diplomatic -- the
Westminster transcription of the Leningrad Codex, and that same transcription corrected -- so
neither is a second hand.  MAM-simple is a consensus text.  A claim about what the accentuation
DOES therefore takes MAM, and the Yeivin cross-check below is run against MAM alone; WLC's and
UXLC's counts are here so the divergence between a manuscript and a consensus text can be read
off, not so that three columns can be averaged.

NOT EVERY MAQAF HERE IS THERE FOR THE SAME REASON, and that is what ``maqaf_after_gaya`` is
about.  Both books describe a maqaf written after a word that already has an accent, where a
gaʿya falls after that accent: Yeivin ITM §357 ("Maqqef after Gaʿya"), Breuer CoS Ch. 1 §43.
What §357 settles is where the non-final atom's accent comes from -- the atom keeps the accent
it has, the gaʿya written after that accent having had to be marked -- and not what the maqaf
signifies, which neither book settles: Yeivin writes these very compounds with a SPACE at §354,
Breuer's Ch. 1 §43 records that "different views have been expressed" and leaves the maqaf out
of the book, and his Ch. 9 §37 points the other way.  Nothing here turns on that.  A compound of
this kind IS a chanted word, on the only test there is for one -- a maqaf is written in it -- so
this survey's mechanical criterion counts it as one compound with two accents.  Thirteen of
MAM's twenty-two compounds with their accents split across atoms are of that kind, across five
different accent pairs, and the signature is checkable: the accented non-final atom also has a
meteg after its accent.  Issue wlc-utils#86.

Prose verses only, routed by ``prose_filter.should_keep_line``.  Yeivin's inventory is his
prose inventory; the poetic system puts two accents on one chanted word far more readily and
systematically (Breuer, Chapter 9 §§20-26), so a merged count would say nothing about either.

THE SURVEY IS THREE MODULES, and this docstring is the design of all three.  This one holds the
per-corpus scan, the report's sections, the flagging path and the JSON writer.
``chanted_word_accents_units`` builds each corpus's fragments, the mark body and its chanted
words, and attributes each accent token to its chanted word -- the geresh fold included -- which
is the machinery the paragraphs above on tokens, atoms and the mark body describe.
``chanted_word_accents_inventory`` holds Yeivin's and Breuer's inventories and Ben's allowances,
and derives the whitelist from them.  Neither of those two imports the other or this module.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path

from accgram import accent_marks as am
from accgram import maqaf_nonfinal_accents as mna
from accgram import prose_filter
from accgram.chanted_word_accents_inventory import (
    BREUER_ENTRIES,
    BREUER_NAMED_SEQUENCES,
    MAM_ALLOWANCES,
    NAMED_TOKEN_SEQUENCES,
    YEIVIN_ENTRIES,
    _ALLOWANCE_INDEX,
    _COS,
    _ITM,
    _RULING,
)
from accgram.chanted_word_accents_units import (
    KIND_COMPOUND_SPLIT,
    Frag,
    Unit,
    _atom_index,
    _by_chanted_word,
    _display,
    _gaya_after_accent,
    _kind_of,
    _unit_at,
    _verse_units,
    mam_frags,
    units_from_body,
    uxlc_frags,
    wlc_frags,
)
from accgram.prose_scanner import HasLegarmeh, Token, scan_accents
from wlc_cmn.wlc_book_codes import wlc_bb_codes
from mb_cmn import file_io
from mb_cmn import paths
from mb_cmn import provenance

CORPUS_KIND = mna.CORPUS_KIND


def _methigazaqef_crossings(
    body: str, tokens: list[Token], units: list[Unit]
) -> list[dict]:
    """Every METHIGAZAQEF token whose qadma and zaqef sit in different chanted words.

    A MECHANICAL LINT, and it must read 0 in all three corpora.  ``prose_scanner``'s rule crosses
    a maqaf, so that ITM §223's metigah-zaqef on the compound Ex 35:9 ואבני־שהם is one token, and
    stops at a space, because §223 and CoS Ch. 5 §§4-6 restrict the metigah to the chanted word of
    the zaqef.  A non-zero count therefore means the fuse has reached across a
    chanted-word boundary again -- the regression this function exists to catch -- so the places
    it reaches are named rather than assumed away.  It read 5 in WLC and 3 in UXLC until the space
    went into ``_METHIGA_MID``; the counts themselves live in the JSON, not in this docstring.
    """
    out: list[dict] = []
    for token in tokens:
        if token.type != "METHIGAZAQEF":
            continue
        zaqef_at = body.index(am.ZAQEF_QATAN, token.start)
        if " " not in body[token.start : zaqef_at]:
            continue
        qadma_unit = _unit_at(units, token.start)
        zaqef_unit = _unit_at(units, zaqef_at)
        out.append(
            {
                "qadma_on": _display(qadma_unit) if qadma_unit else "",
                "zaqef_on": _display(zaqef_unit) if zaqef_unit else "",
            }
        )
    return out


def _bb_order() -> dict[str, int]:
    return {bb: i for i, bb in enumerate(wlc_bb_codes())}


def _sort_key(bcv: str) -> tuple[int, int, int]:
    bb, chnu, vrnu = mna.split_bcv(bcv)
    return (_bb_order()[bb], chnu, vrnu)


# --- the per-corpus scan ------------------------------------------------------


def scan_corpus(frags_by_bcv: dict[str, list[Frag]]) -> dict:
    """Every prose chanted word of one corpus, and the ones with two or more accent tokens."""
    bcvs = sorted(
        (b for b in frags_by_bcv if prose_filter.should_keep_line(*mna.split_bcv(b))),
        key=_sort_key,
    )
    hits: list[dict] = []
    geresh_folds: list[dict] = []
    crossings: list[dict] = []
    # Index-aligned with ``MAM_ALLOWANCES``: the verses this corpus has whose chanted word an
    # allowance's key matches.  Collected here because the key is the MARK RUN, which a hit does
    # not carry -- and must not start carrying, ``mam_residue``'s occurrences being an artifact
    # the plan's Phase 4 requires to come out unchanged.  ``build_survey`` takes these out of the
    # corpus result and hands them to ``mam_allowances``, so no corpus record grows a field.
    allowance_matches: list[list[str]] = [[] for _ in MAM_ALLOWANCES]
    n_verses = n_atomic = n_compound = 0
    n_methigazaqef = 0
    has_legarmeh: HasLegarmeh | None = None
    current_bb: str | None = None
    for bcv in bcvs:
        bb, chnu, vrnu = mna.split_bcv(bcv)
        if bb != current_bb:
            # One instance per book, as ``prose_scanner.scan_book`` holds one: the 17-passage
            # list is walked monotonically and the 1Sam 14:47 counter resets per book.
            has_legarmeh, current_bb = HasLegarmeh(), bb
        n_verses += 1
        body, units = _verse_units(frags_by_bcv[bcv])
        # The flagging path has only the body, and reads the chanted words off it.  Assert here
        # that the two derivations agree, so the field ``classify_verse`` feeds the verdict
        # paths cannot drift from the survey the whitelist is closed against.
        assert units_from_body(body) == [
            Unit(text="", marks=u.marks, start=u.start, is_word=u.is_word)
            for u in units
        ], bcv
        tokens = scan_accents(body, bb, chnu, vrnu, has_legarmeh)
        n_methigazaqef += sum(1 for t in tokens if t.type == "METHIGAZAQEF")
        crossings.extend(
            {"bcv": bcv, **c} for c in _methigazaqef_crossings(body, tokens, units)
        )
        for unit, folded, unfolded in _by_chanted_word(units, tokens):
            if unit.is_compound:
                n_compound += 1
            else:
                n_atomic += 1
            if unfolded is not None:
                geresh_folds.append(
                    {
                        "bcv": bcv,
                        "chanted_word": _display(unit),
                        "as_scanned": unfolded,
                        "as_counted": " ".join(t.leaf for t in folded),
                    }
                )
            if len(folded) < 2:
                continue
            atom_indices = [_atom_index(unit, t.start) for t in folded]
            kind = _kind_of(unit, atom_indices)
            sequence = " ".join(t.leaf for t in folded)
            allowance = _ALLOWANCE_INDEX.get((unit.marks, sequence))
            if allowance is not None:
                allowance_matches[allowance].append(bcv)
            hit = {
                "bcv": bcv,
                "chanted_word": _display(unit),
                "sequence": sequence,
                "kind": kind,
            }
            if kind == KIND_COMPOUND_SPLIT:
                # Only where the accents are split does the question arise, and recording the
                # flag on every hit would put a field on 1,600 of them to say nothing.
                gaya = _gaya_after_accent(unit, folded)
                # The two surveys must not answer one compound differently, ANFA-reason (c) in
                # ``maqaf_nonfinal_accents`` being decided by the same signature read off the
                # Unicode rather than off the mark body.  Asserted rather than assumed: the two
                # derivations have nothing in common but the corpus.
                assert gaya == mna.gaya_after_the_nonfinal_accent(unit.text), (
                    bcv,
                    unit.text,
                )
                hit["gaya_after_the_nonfinal_accent"] = gaya
            hits.append(hit)
    hits.sort(key=lambda h: (h["sequence"], _sort_key(h["bcv"])))
    return {
        "verses": n_verses,
        "chanted_words": n_atomic + n_compound,
        "atomic_chanted_words": n_atomic,
        "maqaf_compounds": n_compound,
        "hits": len(hits),
        "by_kind": dict(Counter(h["kind"] for h in hits).most_common()),
        "by_sequence": dict(Counter(h["sequence"] for h in hits).most_common()),
        "geresh_folds": geresh_folds,
        "methigazaqef": {
            "tokens": n_methigazaqef,
            "crossing_a_chanted_word_boundary": len(crossings),
            "crossings": crossings,
        },
        "occurrences": hits,
        "allowance_matches": allowance_matches,
    }


# --- each table beside what MAM measures --------------------------------------


def breuer_notes(mam: dict) -> list[dict]:
    """Breuer's sections, and -- where one gives a closed list -- MAM asserted against it.

    Ch. 3 §2 is the only entry with a list, and it RAISES on drift rather than warning: the
    treatment ``yeivin_inventory`` gives a closed list, for the reason it gives it, that a
    warning in a generator's output is a warning nobody reads.  Here it is load-bearing twice
    over.  ``mam_residue`` sets that section's chanted words aside, so a second MAM chanted word
    with the pair would be set aside under a list of one that does not name it; and ne8:7 takes
    no allowance precisely because §2 names it, which is a claim about what MAM has as much as
    about what Breuer wrote.
    """
    rows: list[dict] = []
    for entry in BREUER_ENTRIES:
        row = {
            k: v
            for k, v in (
                ("section", entry.section),
                ("names", entry.names),
                ("quote", entry.quote),
                ("source", _COS),
                ("note", entry.note),
            )
            if v
        }
        if entry.sequences:
            measured = sorted(
                {h["bcv"] for h in _measured(mam["occurrences"], entry.sequences)},
                key=_sort_key,
            )
            if measured != list(entry.verses):
                raise AssertionError(
                    f"CoS {entry.section}: Breuer's list is closed at"
                    f" {list(entry.verses)}, and MAM measures {measured} for"
                    f" {list(entry.sequences)}"
                )
            row["token_sequences"] = list(entry.sequences)
            row["breuer_verses"] = list(entry.verses)
            row["breuer_list_is_closed_and_matches_exactly"] = True
        rows.append(row)
    return rows


def mam_allowances(matches: dict[str, list[list[str]]]) -> list[dict]:
    """Ben's ruling beside what each corpus measures for it, asserting MAM on the way through.

    ``matches`` is what ``scan_corpus`` collected per corpus: for each entry of
    ``MAM_ALLOWANCES``, in that order, the verses whose chanted word the entry's key matched.
    MAM's list must equal the entry's ``verses`` exactly, and this RAISES where it does not --
    the same treatment ``yeivin_inventory`` gives a closed list, and for the same reason, that a
    warning in a generator's output is a warning nobody reads.

    WLC's and UXLC's lists are reported and not asserted. They are here because §10 of the plan
    rests ca8:6's allowance on all three corpora having the chanted word alike, so a divergence
    is a finding worth seeing; but the ruling covers MAM, and a diplomatic transcription is not
    the corpus a grammatical claim takes.
    """
    rows: list[dict] = []
    for index, entry in enumerate(MAM_ALLOWANCES):
        measured = {name: found[index] for name, found in matches.items()}
        if measured["mam_simple"] != list(entry.verses):
            raise AssertionError(
                f"MAM allowance for {entry.sequence!r}: written for"
                f" {list(entry.verses)}, and MAM measures {measured['mam_simple']}"
            )
        row = {
            "names": entry.names,
            "token_sequence": entry.sequence,
            "source": _RULING,
            "mam_verses": list(entry.verses),
            "mam_matches_exactly": True,
            "same_key_in_the_other_corpora": {
                name: found for name, found in measured.items() if name != "mam_simple"
            },
        }
        if entry.note:
            row["note"] = entry.note
        rows.append(row)
    return rows


def _measured(hits: list[dict], sequences: tuple[str, ...]) -> list[dict]:
    wanted = frozenset(sequences)
    return [h for h in hits if h["sequence"] in wanted]


def yeivin_inventory(mam: dict) -> list[dict]:
    """Yeivin's prose inventory, each entry beside what MAM measures for it.

    Where Yeivin gives a closed list this RAISES on drift rather than warning: a warning in a
    generator's output is a warning nobody reads, and the whole value of transcribing the list is
    that it is a differential check against a source outside this repo.  An entry marked ``exact``
    must match his verses exactly; every entry with a list must at least contain them.
    """
    hits = mam["occurrences"]
    rows: list[dict] = []
    for entry in YEIVIN_ENTRIES:
        row: dict = {
            "section": entry.section,
            "names": entry.names,
            "yeivin_count": entry.stated_count,
            "quote": entry.quote,
            "source": _ITM,
        }
        if entry.note:
            row["note"] = entry.note
        if entry.sequences:
            measured = _measured(hits, entry.sequences)
            row["token_sequences"] = list(entry.sequences)
            row["mam_measured"] = len(measured)
            if entry.verses:
                listed = set(entry.verses)
                measured_bcvs = {h["bcv"] for h in measured}
                missing = sorted(listed - measured_bcvs, key=_sort_key)
                extra = [h for h in measured if h["bcv"] not in listed]
                if missing:
                    raise AssertionError(
                        f"ITM {entry.section}: verses Yeivin lists that MAM does not"
                        f" measure for {entry.sequences}: {missing}"
                    )
                if entry.exact and extra:
                    raise AssertionError(
                        f"ITM {entry.section}: Yeivin's list is closed, but MAM measures"
                        f" {[h['bcv'] for h in extra]} beyond it"
                    )
                row["yeivin_verses"] = list(entry.verses)
                row["yeivin_verses_all_measured"] = not missing
                row["yeivin_list_is_closed_and_matches_exactly"] = entry.exact
                if extra:
                    row["measured_beyond_yeivin"] = extra
        rows.append(row)
    return rows


def mam_residue(mam: dict) -> dict:
    """MAM prose chanted words whose token sequence no entry above names.

    The point of the survey stated as a finding: after Yeivin's whole prose inventory, this is
    what the consensus text has left over.

    CLOSED AGAINST ``YEIVIN_ENTRIES`` ALONE, and it stays that way now that Ben has ruled these
    chanted words grammatical (2026-08-03).  "All divergences ... should continue to be
    recorded, for possible future return to (for further research)" is half of that ruling, so
    an allowance written under it must not take its chanted word out of this list: ca8:6 is
    named by ``MAM_ALLOWANCES`` and is still here, under ``left_over_after_all_three``.  A residue
    that shrank as the whitelist grew would be the measurement following the verdict.

    THREE GROUPS ARE SET ASIDE INSIDE IT, AND SETTING ASIDE IS NOT REMOVING: ``total`` counts
    every chanted word all the same, and each group says which section or which other page
    accounts for its members.  The third arrived on 2026-08-18 --
    ``accounted_for_by_breuer_ch3_s2``, ne8:7's legarmeh with its servant in one chanted word --
    and it is the first group a section of BREUER's accounts for rather than one of Yeivin's.
    That is why this list stays closed against ``YEIVIN_ENTRIES`` even so: a Breuer section
    grouping the residue is a different act from a Yeivin section shrinking it, and only the
    second reaches ``NAMED_TOKEN_SEQUENCES`` and the checker.
    """
    named = {seq for entry in YEIVIN_ENTRIES for seq in entry.sequences}
    left = [h for h in mam["occurrences"] if h["sequence"] not in named]
    gaya = [h for h in left if h.get("gaya_after_the_nonfinal_accent")]
    telisha = [h for h in left if "telishagedola" in h["sequence"]]
    breuer = [
        h
        for h in left
        if h["sequence"] in BREUER_NAMED_SEQUENCES
        and h not in gaya
        and h not in telisha
    ]
    rest = [h for h in left if h not in gaya and h not in telisha and h not in breuer]
    return {
        "what": (
            "MAM prose chanted words with two accent tokens whose token sequence is named"
            " by no section of Yeivin's prose inventory above."
        ),
        "total": len(left),
        "by_sequence": dict(Counter(h["sequence"] for h in left).most_common()),
        "already_documented_elsewhere": (
            "The geresh-family-with-telisha-gedola words are not unaccounted for: they are"
            " the five words ``uni_to_marks.word_to_marks`` keeps both marks on, whitelisted"
            " by ``lexical_validation`` and set out in the telisha gedola exhibit of"
            " gh-pages/wlc/accgram/almost-errors.html. A geresh or gershayim written twice on"
            " one of them is folded above, so each counts as two accents, not three. They are"
            " deliberately not named in mam_allowances, and the comment above MAM_ALLOWANCES"
            " carries the four measurements that settled it on 2026-08-17: that whitelist is"
            " over one chanted word's tokens, in order, where lexical_validation's is over two"
            " accents on one letter, order-lessly, and the three corpora do not write these"
            " five alike."
        ),
        "accounted_for_by_maqaf_after_gaya": {
            "what": (
                "These are chanted words whose maqaf is the one ITM §357 describes, written"
                " after an atom that has its own accent and a gaʿya after that accent. Each"
                " IS a chanted word -- a maqaf is written in it, which is the whole test --"
                " and each does have two accent tokens. What §357 settles is that the second"
                " token is the non-final atom's retained accent rather than a secondary"
                " accent of the kind §§233 and 241 describe. What that maqaf SIGNIFIES is"
                " unsettled in both books, and nothing here turns on it: Yeivin writes the"
                " same compounds with a space at §354, Breuer CoS Ch. 1 §43 records that"
                " 'different views have been expressed' and leaves it out, and Ch. 9 §37"
                " points the other way. See ``maqaf_after_gaya``."
            ),
            "total": len(gaya),
            "occurrences": gaya,
        },
        "accounted_for_by_breuer_ch3_s2": {
            "what": (
                "A legarmeh and its servant in one chanted word. Breuer CoS Ch. 3 §2 names"
                " this by verse -- 'In one place, the servant of the legarmeih appears"
                " with it in its word' -- and gives the servant as a merkha, on a syllable"
                " fit for a light gaʿya, by Ch. 3 §1's rule that the servant next to a"
                " legarmeh is a merkha. Yeivin does not name the pair anywhere: ITM cites"
                " Ne 8:7 at §279.4 only as one of two places a legarmeh stands before a"
                " pazer, and §§281-282 put legarmeh's servi on preceding chanted words."
                " So a section of one book accounts for this and no allowance is owed --"
                " the disposition §10 of doc/PLAN-two-accents-on-one-chanted-word.md gave"
                " ek16:12 when ITM §357 turned out to account for it (Ben's decision,"
                " 2026-08-18). The pair reached this survey only when issue #215 was fixed"
                " the same day: until then MAM tokenized no legarmeh at all and this"
                " chanted word measured as merkha munax. See ``breuer_notes``, which"
                " asserts Breuer's closed list of one against MAM and raises on drift."
            ),
            "total": len(breuer),
            "occurrences": breuer,
        },
        "left_over_after_all_three": {
            "what": (
                "What is left when the telisha gedola words, the maqaf-after-gaʿya"
                " compounds and Breuer's Ch. 3 §2 chanted word are set aside: the atomic"
                " chanted words of MAM's prose verses that have two accents no section of"
                " either book names."
            ),
            "total": len(rest),
            "occurrences": rest,
        },
        "occurrences": left,
    }


# --- the flagging path --------------------------------------------------------


def classify_verse(body: str, tokens: list[Token]) -> list[dict]:
    """One verse's chanted words with two or more accent tokens, each named or left unnamed.

    ``body`` is the mark body the scanner read and ``tokens`` the stream it emitted, so a caller
    passes what it already has.  Each hit carries the chanted word's run of the body, its token
    sequence, whether it is an atom or a maqaf compound, and the ITM section that names the
    sequence -- ``None`` where no section of Yeivin's prose inventory does.  A ``None`` is the
    finding: it is the pair for which the inventory, closed against MAM in the survey above,
    offers no precedent.

    A hit that an entry of ``MAM_ALLOWANCES`` matches carries ``mam_allowance`` as well, and its
    ``itm_section`` stays ``None``, which is the honest reading: Yeivin does not name the pair,
    and what names the chanted word is Ben's ruling of 2026-08-03.  The two keys are kept apart
    so that a reader can tell a section transcribed from Yeivin from a ruling about MAM.

    Nothing here reads a verdict or writes one.  The caller records the result beside
    ``status`` and ``tree``, which stay as the grammar left them.
    """
    hits: list[dict] = []
    units = units_from_body(body)
    for unit, folded, _unfolded in _by_chanted_word(units, tokens):
        if len(folded) < 2:
            continue
        sequence = " ".join(t.leaf for t in folded)
        atom_indices = [_atom_index(unit, t.start) for t in folded]
        hit = {
            "marks": unit.marks,
            "sequence": sequence,
            "kind": _kind_of(unit, atom_indices),
            "itm_section": NAMED_TOKEN_SEQUENCES.get(sequence),
        }
        allowance = _ALLOWANCE_INDEX.get((unit.marks, sequence))
        if allowance is not None:
            hit["mam_allowance"] = MAM_ALLOWANCES[allowance].names
        hits.append(hit)
    return hits


def _split_hits(corpus: dict) -> list[dict]:
    return [h for h in corpus["occurrences"] if h["kind"] == KIND_COMPOUND_SPLIT]


def maqaf_after_gaya(scanned: dict[str, dict]) -> dict:
    """The compounds whose accents are split across atoms, partitioned by ITM §357's signature.

    A compound reaches this survey because a maqaf stands inside it, and the maqafs it finds
    are not all written for the same reason.  Yeivin ITM §357 and Breuer CoS Ch. 1 §43 both
    describe a maqaf written after a word that has its own accent and a gaʿya after that
    accent; §357 gives its purpose as saying the slowed syllable makes no break, and what it
    signifies beyond that is disputed in both books.  The partition here does not depend on
    that: the signature is mechanical -- ``_gaya_after_accent`` -- so it is a measurement
    rather than a reading, and each side of it is set out for the reader to check.

    This replaces the narrower ``merkha_tipexa_discrepancy`` block, whose open question this
    answers: the four MAM chanted words beyond §233's eight are neither §233 cases Yeivin left
    out nor §293's scribal habit.  The §233 and §241 arithmetic is kept below, since it is what
    put the question, and both surpluses turn out to be of the one kind.
    """
    mam = scanned["mam_simple"]
    per_corpus: dict[str, dict] = {}
    for name, corpus in scanned.items():
        split = _split_hits(corpus)
        with_gaya = [h for h in split if h["gaya_after_the_nonfinal_accent"]]
        per_corpus[name] = {
            "accents_split_across_atoms": len(split),
            "of_them_with_a_gaya_after_the_nonfinal_accent": len(with_gaya),
            "with_a_gaya_by_sequence": dict(
                Counter(h["sequence"] for h in with_gaya).most_common()
            ),
            "without_a_gaya_by_sequence": dict(
                Counter(
                    h["sequence"]
                    for h in split
                    if not h["gaya_after_the_nonfinal_accent"]
                ).most_common()
            ),
            "with_a_gaya": with_gaya,
        }

    def _arithmetic(section: str) -> dict:
        entry = next(e for e in YEIVIN_ENTRIES if e.section == section)
        listed = set(entry.verses)
        measured = _measured(mam["occurrences"], entry.sequences)
        beyond = [h for h in measured if h["bcv"] not in listed]
        return {
            "yeivin_stated": entry.stated_count,
            "yeivin_listed": len(listed),
            "mam_measured": len(measured),
            "yeivin_verses_by_kind": dict(
                Counter(h["kind"] for h in measured if h["bcv"] in listed).most_common()
            ),
            "beyond_yeivin": beyond,
            "beyond_yeivin_all_have_a_gaya_after_the_nonfinal_accent": all(
                h.get("gaya_after_the_nonfinal_accent") for h in beyond
            ),
        }

    return {
        "what": (
            "A maqaf written after a word that has its own accent and a gaʿya after that"
            " accent. ITM §357 gives its purpose -- the slowed syllable makes no break --"
            " and CoS Ch. 1 §43 gives its conditions: after a servant, on a word accented"
            " on its penultimate syllable, with the gaʿya on its last. A compound found by"
            " it IS a chanted word, on the only test there is for one -- a maqaf is written"
            " in it -- and it does have two accent tokens. What §357 settles is that the"
            " second token is the non-final atom's retained accent rather than a secondary"
            " accent of the kind §§233 and 241 describe. What the maqaf SIGNIFIES is"
            " unsettled in both books and nothing here turns on it: Yeivin writes the same"
            " compounds with a space at §354, CoS Ch. 1 §43 records that 'different views"
            " have been expressed' and leaves it out of the book, and Ch. 9 §37 points the"
            " other way."
        ),
        "how_it_is_told_apart": (
            "Mechanically, off the mark body: the accented non-final atom also has a meteg"
            " between that accent and the maqaf. Nothing here reads a verse reference. On"
            " MAM the signature partitions the compounds exactly, the nine without it"
            " being the mayela ones and nothing else. It is a signature and not a"
            " definition, though, and Isaiah 8:17 וקויתי־לו is where that shows: WLC and"
            " UXLC have a meteg after the mayela there and MAM has none, so the same"
            " compound answers differently by corpus while staying the mayela case CoS"
            " Ch. 9 §37 names by verse."
        ),
        "verses_the_books_name_that_this_survey_measures": {
            "ITM §354": ["ek1:4"],
            "ITM §357": ["is59:16"],
            "CoS Ch. 1 §43": ["is63:5"],
        },
        "which_corpus_has_it": (
            "MAM's, and hardly L's -- which is what both books' manuscript labels predict."
            " Yeivin's §357 examples are in C, in S, in A and C, and in L3; Breuer's is"
            " ancient manuscripts generally. The counts below are the check on that."
        ),
        "by_corpus": per_corpus,
        "what_the_others_are": (
            "The compounds with no gaʿya after the non-final accent are the mayela ones,"
            " which both books name outright: ITM §§210 and 216, and CoS Ch. 9 §37, whose"
            " two examples -- Isaiah 8:17 וקויתי־לו and Genesis 8:18 ויצא־נח -- are two of"
            " MAM's nine. There a secondary mark stands in a hyphenated atom, and Breuer's"
            " rule at Ch. 9 §37 is that the hyphenation is not cancelled after such a mark."
        ),
        "itm_233_arithmetic": _arithmetic("§233"),
        "itm_241_arithmetic": _arithmetic("§241"),
        "answer": (
            "The four chanted words beyond ITM §233's eight, and the three beyond §241's"
            " five, are neither cases those sections left out nor ITM §293's habit of a"
            " maqaf written after an atom that keeps its own conjunctive. They are §357's"
            " maqaf after gaʿya, and so are the four merkha-with-silluq שלף־חרב and the"
            " one munax-with-zaqef Isaiah 40:7 נבל־ציץ. Both books put the class outside"
            " their inventories of secondary accents -- Yeivin under gaʿya, Breuer by"
            " declining to discuss it -- and between them they name three of the thirteen"
            " by verse. §233's own eight and §241's own five all have both marks on ONE"
            " atom, on a syllable fit for a gaʿya, which is Breuer's stated criterion for"
            " a same-word servant at Ch. 3 §28."
        ),
        "recorded_not_flagged": (
            "Breuer says of this maqaf that 'there is no trace of it in the accepted"
            " editions of Scripture', and MAM has thirteen. That divergence is recorded"
            " here for future research and is not a verdict; nothing in this survey"
            " promotes it to a finding about MAM's accentuation. Issue wlc-utils#86."
        ),
    }


# --- the survey ---------------------------------------------------------------


def build_survey() -> dict:
    """The whole survey: three corpora, prose verses only, plus Yeivin's inventory beside MAM."""
    wlc = wlc_frags(paths.out_dir() / "wlc422-kq-u")
    refs: dict[str, set[tuple[int, int]]] = defaultdict(set)
    for bcv in wlc:
        bb, chnu, vrnu = mna.split_bcv(bcv)
        refs[bb].add((chnu, vrnu))

    corpora = {
        "wlc422": wlc,
        "uxlc": uxlc_frags(paths.in_dir() / "UXLC-39"),
        "mam_simple": mam_frags(dict(refs)),
    }
    scanned: dict[str, dict] = {}
    # Taken out of each corpus result rather than published with it: what the allowance keys
    # matched belongs beside the ruling, in one place a reader can read the whole of it, and a
    # corpus record that grew a field would move an artifact this phase promised not to move.
    allowance_matches: dict[str, list[list[str]]] = {}
    for name, frags in corpora.items():
        result = scan_corpus(frags)
        allowance_matches[name] = result.pop("allowance_matches")
        scanned[name] = {"kind": CORPUS_KIND[name], **result}
    return {
        "criterion": (
            "A chanted word -- an atom, or a whole maqaf compound -- carrying two or more"
            " accent TOKENS as the prose scanner emits them. Tokens rather than marks: the"
            " scanner already fuses a doubled stress helper, the zarqa's own helper with"
            " its zarqa, the same-letter mahapakh!qadma cluster, munax with a following U+05C0 as"
            " legarmeh, and qadma...zaqef as metigah-zaqef, and it swallows meteg. A geresh"
            " or gershayim written twice on one chanted word is folded here, since that is"
            " one accent written twice and the scanner does not fuse it."
        ),
        "scope": (
            "Prose verses only, routed by prose_filter.should_keep_line. Yeivin's inventory"
            " below is his prose inventory, and the poetic system puts two accents on one"
            " chanted word far more readily (Breuer, Chapter 9 §§20-26), so a merged count"
            " would say nothing about either."
        ),
        "which_corpus_answers_what": (
            "A claim about what the accentuation does takes MAM, a consensus text, so the"
            " Yeivin cross-check runs against MAM alone. WLC 4.22 and UXLC are the"
            " Westminster transcription of the Leningrad Codex and that transcription"
            " corrected, so they are one hand, not two, and their counts are here to be"
            " read against MAM rather than averaged with it."
        ),
        "yeivin_inventory": yeivin_inventory(scanned["mam_simple"]),
        "breuer_notes": breuer_notes(scanned["mam_simple"]),
        "mam_allowances": mam_allowances(allowance_matches),
        "maqaf_after_gaya": maqaf_after_gaya(scanned),
        "mam_residue": mam_residue(scanned["mam_simple"]),
        "corpora": scanned,
    }


def default_json_out_path() -> Path:
    return paths.out_dir() / "accgram" / "chanted-word-accents.json"


def write_json(survey: dict, path: Path) -> None:
    payload = provenance.with_json_provenance(survey, __file__)
    # Through file_io for the temp-file write and the PermissionError retry; it makes
    # the directory too. LF is preserved as maqaf_nonfinal_accents preserves it -- the
    # repo's line-ending policy is LF in the workdir as well as in git, and a plain
    # text-mode write would translate to CRLF on Windows and leave every regeneration
    # looking like a whole-file diff. file_io's default newline="" translates nothing,
    # so it holds the line the old explicit newline="\n" held.
    file_io.json_dump_to_file_path(payload, str(path), indent=1)


def add_args(parser, *, repo_root: Path) -> None:
    # repo_root is unused: the default comes from ``default_json_out_path``, which composes
    # off ``paths.out_dir()`` -- the same value ``run`` falls back to, so the flag's
    # default and its absence can no longer answer differently.  The parameter is kept
    # because the entry point wires every subcommand the same way.
    del repo_root
    parser.add_argument(
        "--json-out",
        type=Path,
        default=default_json_out_path(),
        help="Where to write the survey JSON.",
    )


def run(args) -> None:
    survey = build_survey()
    out_path = getattr(args, "json_out", None) or default_json_out_path()
    write_json(survey, out_path)
    print(f"wrote {out_path}")
