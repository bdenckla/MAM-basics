"""Current-MAM loading and form matching for the post-stress-meteg survey."""

from __future__ import annotations

import json
from functools import cache

from accgram import maqaf_nonfinal_accents as mna
from mb_cmn import hebrew_points as hpo
from mb_cmn import hebrew_punctuation as hpu
from mb_cmn import paths

from accgram.post_stress_meteg_model import (
    MAQAF,
    METEG,
    PASOLEG,
    SurveyProblem,
    _bare,
    _bb_of_stem,
    _fold_phonetic_mam_annotations,
    _fold_qamats_qatan,
    _mam_join_key,
    _phonetic_mam_join_key,
    _validate_phonetic_word,
)

# The verses the page names outside its tables, whose chanted words it therefore has to show
# as MAM has them TODAY rather than as the surveyed snapshot has them.  Isaiah 23:12 is
# where the two differ -- suggestion M23 added a meteg there after the snapshot was taken --
# and 1 Samuel 17:5 is the Leningrad Codex post-silluq case, where the page's claim is about
# what MAM lacks.  First Kings 7:37 is MAM's post-silluq case, which the research ignores
# in the sense the Methods page defines (Ben, 2026-09-09): the word is deliberately read as
# meteg-then-silluq, as the stress oracle reads it, so it counts as MBS_O.
# 2 Chronicles 8:11 supplies MAM's form beside a possible different interpretation of the
# Leningrad Codex.  Named here rather than in the page module so the form is lifted from the
# corpus at generation time and reaches the page through the tracked JSON, as every other form
# does.
_FOCUS_VERSES = ("is23:12", "1s17:5", "1k7:37", "2c8:11")


def _mam_words_by_bcv(cantillation: str | None = None) -> dict[str, list[str]]:
    """MAM-simple's chanted words per numbered verse, in MAM's versification.

    MAM's numbering rather than the BHS one this repo's other surveys read, because Phonetic
    MAM numbers its verses MAM's way; ``test_final_stress_vs_phonetic_mam._measured`` reaches
    for the same tree for the same reason. ``cantillation`` selects an individual
    dual-cantillation projection; otherwise this returns MAM-simple's combined representation.
    """
    from accgram import mam_simple_verse

    mam_dir = paths.require_mam_simple_vtrad_mam_dir()
    refs_by_book = mam_simple_verse.mam_simple_refs(mam_dir)
    if cantillation is None:
        return mna.mam_words(refs_by_book, mam_dir)
    return mna.mam_words_for_cantillation(refs_by_book, cantillation, mam_dir)


def _join_mam_context_tokens(atoms: list[object]) -> list[object]:
    """MAM-simple atoms folded into chanted words, retaining native PASOLEG markers."""
    from accgram import mam_simple_verse

    out: list[object] = []
    pending = ""
    for atom in atoms:
        if isinstance(atom, mam_simple_verse.MAMNativePaseq):
            if pending:
                raise SurveyProblem(
                    "MAM native paseq/legarmeh occurs before its preceding atom has ended: "
                    f"{pending!r}"
                )
            out.append(atom)
            continue
        if not isinstance(atom, str):
            raise SurveyProblem(f"unexpected MAM-simple atom: {atom!r}")
        pending += atom
        if not pending.endswith(MAQAF):
            out.append(pending)
            pending = ""
    if pending:
        out.append(pending)
    return out


def _mam_context_by_bcv() -> dict[str, list[object]]:
    """MAM chanted-word streams with MAM's native paseq/legarmeh categories retained."""
    from accgram import mam_simple_verse

    mam_dir = paths.require_mam_simple_vtrad_mam_dir()
    refs_by_book = mam_simple_verse.mam_simple_refs(mam_dir)
    loaded = mam_simple_verse.load_mam_simple_for_refs(
        mam_dir, refs_by_book, include_native_paseq_roles=True
    )
    return {
        bcv: _join_mam_context_tokens(payload["mam_simple_verse"]["vels"])
        for bcv, payload in loaded.items()
    }


@cache
def _snapshot_forms() -> dict[str, tuple[str, list[str]]]:
    """Index first fva forms to their selected snapshot spelling and source locations.

    Matching needs the snapshot's first rep, or its first unannotated fva. The raw
    classifier inputs and serialized survey stay intact. Nothing outside this module calls
    it: the page renderer raises on a displayed record that has no MAM form rather than look
    a spelling up here (CLAUDE.md, "A code path reads MAM-private every time it runs, or
    never").
    """
    directory = paths.require_al_hatorah_phonetic_dir()
    files = sorted(directory.glob("*.json"))
    if {path.stem for path in files} != set(_bb_of_stem()):
        raise SurveyProblem(f"{directory}: incomplete or unexpected snapshot file set")
    forms = {}

    def visit(node: object, location: str) -> None:
        if isinstance(node, dict):
            _validate_phonetic_word(node)
            raw = node["fva"].split(" ")[0]
            field = "rep" if node.get("rep") else "fva"
            selected = node[field].split(" ")[0]
            source = f"{location}/{field} (first form)"
            if field == "fva" and _fold_phonetic_mam_annotations(selected) != selected:
                raise SurveyProblem(f"{source}: annotated fva has no rep")
            if raw in forms:
                previous, sources = forms[raw]
                if previous != selected:
                    raise SurveyProblem(
                        f"{source}: ambiguous snapshot spelling; also {sources}"
                    )
                sources.append(source)
            else:
                forms[raw] = (selected, [source])
        elif isinstance(node, list):
            for index, value in enumerate(node):
                visit(value, f"{location}/{index}")
        elif node is None:
            return
        elif not isinstance(node, str):
            raise TypeError(f"{location}: unclassified Phonetic MAM node: {node!r}")

    for path in files:
        root = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(root, dict):
            raise SurveyProblem(f"{path}: Phonetic MAM book root is not an object")
        for bcv, payload in root.items():
            if not isinstance(bcv, str):
                raise SurveyProblem(
                    f"{path}: Phonetic MAM verse key is not text: {bcv!r}"
                )
            escaped_bcv = bcv.replace("~", "~0").replace("/", "~1")
            visit(payload, f"{path}#/{escaped_bcv}")
    return forms


def _snapshot_unannotated_form(word: str) -> str:
    """Select the source spelling; never reconstruct it by deleting Hebrew marks."""
    forms = _snapshot_forms()
    if word not in forms:
        raise SurveyProblem(f"No snapshot source for first fva form {word!r}")
    return forms[word][0]


def _as_mam_would_write_it(word: str) -> str:
    """The selected snapshot form with the transformations needed only for matching.

    VARIKA removal remains necessary to reproduce the existing record matching.
    The selected form itself keeps VARIKA and every other Hebrew mark; only this copy,
    made for matching, loses VARIKA.
    """
    return (
        _snapshot_unannotated_form(word)
        .replace(hpo.VARIKA, "")
        .replace(hpu.NU_GMAQ, MAQAF)
    )


def _settle(matches: list[str], snapshot: str) -> tuple[str | None, str]:
    """Which of several candidate MAM chanted words a record's is, or none.

    A verse can hold two chanted words with the same letters and points -- Proverbs 12:1's two
    אֹהֵב, Psalms 135:1's two הללו, one with a deḥi and one with a geresh muqdam -- and the
    join key cannot tell them apart, since what separates them is exactly what it drops.  Two
    tests do: the candidate identical to the snapshot's, annotations aside, and
    failing that the one candidate whose meteg count agrees.  Neither test assumes an answer;
    both ask which chanted word this is, of the ones MAM has in that verse.
    """
    forms = list(dict.fromkeys(matches))
    if not forms:
        return None, "no match"
    if len(forms) == 1:
        return forms[0], "one candidate in the verse"
    written = _as_mam_would_write_it(snapshot)
    if written in forms:
        return written, f"the one of {len(forms)} identical to the snapshot"
    agreeing = [one for one in forms if one.count(METEG) == snapshot.count(METEG)]
    if len(agreeing) == 1:
        return agreeing[0], f"the one of {len(forms)} whose metegs agree"
    return None, f"{len(forms)} candidates, none of them settled"


def _matching_mam_words(record: dict, words: list[str]) -> tuple[list[str], str]:
    """The MAM chanted words a record's spelling can be matched to, and how it matched."""
    keys = [_phonetic_mam_join_key(record["chanted_word"])]
    if record.get("snapshot_before_qere"):
        keys.append(_phonetic_mam_join_key(record["snapshot_before_qere"]))
    for index, key in enumerate(keys):
        matches = [word for word in words if _mam_join_key(word) == key]
        if matches:
            return matches, "the qere it stands for" if index else "as written"
    for key in keys:
        folded = _fold_qamats_qatan(key)
        matches = [
            word for word in words if _fold_qamats_qatan(_mam_join_key(word)) == folded
        ]
        if matches:
            return matches, "with qamats qatan read as qamats"
    return [], "no match"


def _next_mam_context(
    record: dict, stream: list[object]
) -> tuple[str | None, tuple[dict[str, str], ...] | None]:
    """The next MAM chanted word and its native punctuation context, if resolved.

    MAM-simple distinguishes the two PASOLEG meanings structurally: ``lp-paseq`` and
    ``lp-legarmeih``.  The page needs that distinction to put a narrow-sense paseq with the
    next chanted word and a legarmeh with the preceding chanted word, so this routine keeps
    MAM's native category rather than reconstructing one from an accent grammar or the glyph.
    """
    from accgram import mam_simple_verse

    current = record["mam_form"]
    next_word = record["next_chanted_word"]
    if current is None or next_word is None:
        return None, None
    snapshot_next_as_mam = _as_mam_would_write_it(next_word)
    source_punctuation = tuple(record.get("intervening_punctuation", ()))
    candidates: list[tuple[str, tuple[dict[str, str], ...]]] = []
    source_matched_candidates: list[tuple[str, tuple[dict[str, str], ...]]] = []
    for index, word in enumerate(stream):
        if word != current:
            continue
        punctuation: list[dict[str, str]] = []
        next_stream_index = index + 1
        while next_stream_index < len(stream) and isinstance(
            stream[next_stream_index], mam_simple_verse.MAMNativePaseq
        ):
            marker = stream[next_stream_index]
            if marker.kind not in {"paseq", "legarmeh"}:
                raise SurveyProblem(
                    f"{record['bcv']} {current!r}: MAM has unclassified native punctuation"
                    f" {marker.kind!r} before the next chanted word"
                )
            punctuation.append({"kind": marker.kind, "glyph": marker.glyph})
            next_stream_index += 1
        if next_stream_index == len(stream):
            continue
        next_item = stream[next_stream_index]
        if next_item == PASOLEG:
            raise SurveyProblem(
                f"{record['bcv']} {current!r}: a MAM paseq/legarmeh glyph before the next chanted"
                " chanted word lacks MAM's native paseq/legarmeh category"
            )
        if not isinstance(next_item, str):
            raise SurveyProblem(
                f"{record['bcv']} {current!r}: unexpected MAM context item before the"
                f" next chanted word: {next_item!r}"
            )
        candidate = (next_item, tuple(punctuation))
        candidates.append(candidate)
        if (
            tuple(marker["glyph"] for marker in punctuation) == source_punctuation
            and next_item == snapshot_next_as_mam
        ):
            source_matched_candidates.append(candidate)
    source_settled = []
    for candidate in source_matched_candidates:
        if candidate not in source_settled:
            source_settled.append(candidate)
    if len(source_settled) == 1:
        return source_settled[0]
    if source_settled:
        return None, None
    settled = []
    for candidate in candidates:
        if candidate not in settled:
            settled.append(candidate)
    return settled[0] if len(settled) == 1 else (None, None)


def _attach_mam_forms(
    records: list[dict],
    words_by_bcv: dict[str, list[str]],
    context_by_bcv: dict[str, list[object]] | None = None,
) -> list[dict]:
    """Give each record the form MAM has today, found by join key, or say why it has none.

    THE PAGE SHOWS ``mam_form`` AND NOT ``chanted_word``, and this is where the difference is
    made.  Phonetic MAM's text has two annotations absent from MAM -- U+05C8 in place of U+05B0
    for a shewa it resolves as vocal, and U+05C9 in place of U+05BC for a dagesh it reads as
    xazaq -- so a page showing its forms verbatim would put marks in front of a reader that
    MAM's text does not have.  The join key drops exactly what the two sides may legitimately
    differ in, this
    including the survey's subject, so a chanted word that has GAINED or LOST a meteg since
    the snapshot still matches, and the record says so in ``metegs_in_mam_today``.

    TWO IDENTICAL CANDIDATES ARE ONE ANSWER, and are accepted: a verse with two byte-identical
    chanted words -- Proverbs 12:1's two אֹהֵב, Psalms 135:1's two הללו -- leaves the position
    ambiguous and the FORM certain, which is all the page shows.  Two candidates that differ
    are refused, since then the form is a choice.

    A record with no form is named in ``records_without_a_mam_form``.  The page renderer
    raises if it is asked to display one, rather than look up a substitute spelling in
    MAM-private (CLAUDE.md, "A code path reads MAM-private every time it runs, or never").
    """
    context_by_bcv = context_by_bcv or {}
    out = []
    for record in records:
        matches, keyed_by = _matching_mam_words(
            record, words_by_bcv.get(record["bcv"], [])
        )
        settled, settled_by = _settle(matches, record["chanted_word"])
        record["mam_form"] = settled
        record["mam_form_matched_by"] = f"{keyed_by}; {settled_by}"
        record["mam_form_candidates"] = len(set(matches))
        record["metegs_in_mam_today"] = settled.count(METEG) if settled else None
        record["metegs_in_the_snapshot"] = record["chanted_word"].count(METEG)
        next_mam_form, intervening_mam_punctuation = (
            _next_mam_context(record, context_by_bcv.get(record["bcv"], []))
            if settled is not None
            else (None, None)
        )
        record["next_mam_form"] = next_mam_form
        record["intervening_mam_punctuation"] = intervening_mam_punctuation
        if settled is not None:
            # Recomputed from MAM's form, so that every Hebrew string the page can render
            # from this record comes from one text rather than two.
            record["accents_and_letters"] = _bare(settled)
        else:
            out.append(record)
    return out


def _focus_verses(words_by_bcv: dict[str, list[str]]) -> dict:
    """Each focus verse's chanted words, as MAM has them today."""
    return {
        bcv: {
            "chanted_words": list(words_by_bcv[bcv]),
            "metegs": sum(word.count(METEG) for word in words_by_bcv[bcv]),
        }
        for bcv in _FOCUS_VERSES
    }
