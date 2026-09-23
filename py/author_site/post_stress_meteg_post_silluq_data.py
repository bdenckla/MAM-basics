"""Authored-ledger loading and form comparison for the post-silluq page."""

from __future__ import annotations

from datetime import date
import json
from pathlib import Path
import xml.etree.ElementTree as ET

from accgram import mam_simple_verse
from accgram import post_stress_meteg_model as psm
from accgram.almost_errors_html_shared import wrap_hebrew_runs
from mb_author import author
from mb_cmn import paths
from py_uxlc import my_uxlc
from py_wlc_json_and_unicode import wlc_uword
from uxlc_misc import my_uxlc as uxlc_source
from wlc_cmn.wlc_book_codes import wlc_bb_codes, wlc_bb_to_bk39id

from author_site.post_stress_meteg_shared import (
    _FULL_REF,
    _KOREN_POSITIONS,
    _KOREN_SHEVA_STATES,
    _KOREN_STATUSES,
    _MAM_POST_SILLUQ_VERSE,
    _POST_SILLUQ_CASES_JSON,
    _POST_SILLUQ_CASE_STATUSES,
    _POST_SILLUQ_FORM_SOURCES,
    _POST_SILLUQ_IMAGE_IDS,
    _POST_SILLUQ_IMAGE_REFS,
    _POST_SILLUQ_IMAGE_SEQUENCES,
    _POST_SILLUQ_KOREN_JSON,
    _POST_SILLUQ_SOURCE_STATES,
    _POST_SILLUQ_VERSE,
    _ROM_METEG,
    _ROM_SILLUQ,
    _post_silluq_sources_for_bcv,
    _ref_link,
    _split,
)


def _letters_of(word: str) -> tuple[str, ...]:
    """The base letters of each atom of a chanted word, as a tuple, one string per atom.

    The house pattern for finding a form without retyping its accents: search by letters,
    render what the corpus has.  ``maqaf_nonfinal_accents_page._find_span`` is the other
    instance.
    """
    atoms = word.replace(psm.MAQAF, " ").split(" ")
    return tuple(
        "".join(char for char in atom if "א" <= char <= "ת") for atom in atoms if atom
    )


def _focus_word(
    survey: dict, bcv: str, letters: tuple[str, ...], *, must_have: str = ""
) -> str:
    """The one chanted word of a focus verse whose atoms have these letters.

    A focus verse is one the page names outside its tables, and the survey records its
    chanted words as MAM has them today.  Searching by letters is what keeps the accents
    lifted from the corpus rather than typed here, and the exactly-one assertion is what
    makes the search a check rather than a guess.

    ``must_have`` narrows a verse that has the same letters twice: 1 Samuel 17:5 has נחשת
    both in the middle and at the end, and it is the verse-final one -- the one with sof
    pasuq -- that the post-silluq section is about.
    """
    return _source_focus_word(
        survey["currency"]["focus_verses"][bcv]["chanted_words"],
        bcv,
        letters,
        must_have=must_have,
        source="MAM",
    )


def _source_focus_word(
    words: list[str],
    bcv: str,
    letters: tuple[str, ...],
    *,
    must_have: str,
    source: str,
) -> str:
    """The one source form at a page-named verse that has these letters and mark."""
    hits = [
        word for word in words if _letters_of(word) == letters and must_have in word
    ]
    assert (
        len(hits) == 1
    ), f"{source} {bcv}: {len(hits)} chanted words with letters {letters} and {must_have!r}"
    return hits[0]


def _uxlc_words(bcv: str) -> list[str]:
    """The UXLC atoms at one verse, lifted from its vendored XML source."""
    bb, chnu, vrnu = _split(bcv)
    bk39id = wlc_bb_to_bk39id(bb)
    xml_name = f"{my_uxlc._UXLC_BOOK_FILE_NAMES[bk39id]}.xml"
    xml_path = paths.in_dir() / "UXLC-39" / xml_name
    root = ET.parse(xml_path).getroot()
    chapters = [node for node in root.iter("c") if node.attrib.get("n") == str(chnu)]
    assert len(chapters) == 1, f"{xml_path}: {len(chapters)} chapter {chnu} elements"
    verses = [
        node
        for node in chapters[0]
        if node.tag == "v" and node.attrib.get("n") == str(vrnu)
    ]
    assert len(verses) == 1, f"{xml_path}: {len(verses)} verse {chnu}:{vrnu} elements"
    return [
        atom.text.strip()
        for atom in verses[0]
        if atom.tag in {"w", "q"} and atom.text is not None
    ]


def _wlc_words(bcv: str) -> list[str]:
    """The WLC 4.22 atoms at one verse, decoded from its vendored M-C source."""
    assert bcv.startswith("1s"), bcv
    json_path = paths.out_dir() / "wlc422" / "1verses_03_jsju1s.json"
    rows = json.loads(json_path.read_text(encoding="utf-8"))
    assert isinstance(rows, list), f"Expected a list in {json_path}"
    rows_at_verse = [
        row for row in rows if isinstance(row, dict) and row.get("bcv") == bcv
    ]
    assert len(rows_at_verse) == 1, f"WLC 4.22: {len(rows_at_verse)} rows for {bcv}"
    vels = rows_at_verse[0].get("vels")
    assert isinstance(vels, list) and all(
        isinstance(atom, str) for atom in vels
    ), f"WLC 4.22 {bcv}: non-string vels"
    return [wlc_uword.uword(atom) for atom in vels]


def _require_exact_keys(
    record: dict, *, required: set[str], allowed: set[str], where: str
) -> None:
    """Reject missing and unknown keys in one authored JSON object."""
    missing = sorted(required - set(record))
    unknown = sorted(set(record) - allowed)
    if missing or unknown:
        raise ValueError(f"{where}: missing keys {missing}; unknown keys {unknown}")


def _require_nonempty_string(value: object, *, where: str) -> str:
    """Return one nonempty authored string, or fail with its JSON location."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{where}: expected a nonempty string")
    return value


def _full_ref_to_bcv(ref: str) -> str:
    """Convert the tracked full-English reference to the survey's compact BCV."""
    match = _FULL_REF.fullmatch(ref)
    if match is None:
        raise ValueError(f"Malformed reference: {ref!r}")
    english_to_bb = {}
    for bb in wlc_bb_codes():
        parts = uxlc_source.book_basename(wlc_bb_to_bk39id(bb)).split("_")
        english_name = (
            f"{parts[-1]} {' '.join(parts[:-1])}"
            if parts[-1] in {"1", "2"}
            else " ".join(parts)
        )
        english_to_bb[english_name] = bb
    try:
        bb = english_to_bb[match["book"]]
    except KeyError as exc:
        raise ValueError(f"Unknown book in reference: {ref!r}") from exc
    return f"{bb}{int(match['chapter'])}:{int(match['verse'])}"


def _validate_iso_date(value: object, *, where: str) -> str:
    """Validate one historical observation date without generating a clock date."""
    text = _require_nonempty_string(value, where=where)
    try:
        parsed = date.fromisoformat(text)
    except ValueError as exc:
        raise ValueError(f"{where}: expected an ISO date, got {text!r}") from exc
    if parsed.isoformat() != text:
        raise ValueError(f"{where}: date is not canonical ISO form: {text!r}")
    return text


def _validate_string_list(
    value: object, *, where: str, allow_empty: bool = False
) -> list[str]:
    """Validate a duplicate-free list of nonempty strings."""
    if not isinstance(value, list) or (not allow_empty and not value):
        raise ValueError(
            f"{where}: expected a {'possibly empty' if allow_empty else 'nonempty'} list"
        )
    strings = [
        _require_nonempty_string(item, where=f"{where}[{index}]")
        for index, item in enumerate(value)
    ]
    if len(strings) != len(set(strings)):
        raise ValueError(f"{where}: duplicate entries")
    return strings


def _validate_post_silluq_sources(value: object, *, bcv: str, where: str) -> dict:
    """Validate the source mapping for this explicitly recognized case."""
    expected = _post_silluq_sources_for_bcv(bcv)
    if not isinstance(value, dict) or set(value) != set(expected):
        raise ValueError(f"{where}: expected exactly {expected}")
    for source, state in value.items():
        if state not in _POST_SILLUQ_SOURCE_STATES:
            raise ValueError(f"{where}/{source}: unknown state {state!r}")
    return value


def load_post_silluq_cases() -> list[dict]:
    """Load and validate the curated cross-source case ledger."""
    path = paths.in_dir() / _POST_SILLUQ_CASES_JSON
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected a root object")
    _require_exact_keys(
        payload,
        required={"about", "cases"},
        allowed={"about", "cases"},
        where=str(path),
    )
    _require_nonempty_string(payload["about"], where=f"{path}#about")
    cases = payload["cases"]
    if not isinstance(cases, list) or not cases:
        raise ValueError(f"{path}#cases: expected a nonempty list")

    seen_refs: set[str] = set()
    seen_bcvs: set[str] = set()
    for index, case in enumerate(cases):
        where = f"{path}#cases/{index}"
        if not isinstance(case, dict):
            raise ValueError(f"{where}: expected an object")
        required = {"ref", "bcv", "status", "form_source", "reports", "images"}
        allowed = required | {
            "sources",
            "additional_sources",
            "transcriptions",
            "mam_editorial_basis",
        }
        _require_exact_keys(case, required=required, allowed=allowed, where=where)

        ref = _require_nonempty_string(case["ref"], where=f"{where}/ref")
        bcv = _require_nonempty_string(case["bcv"], where=f"{where}/bcv")
        if _full_ref_to_bcv(ref) != bcv:
            raise ValueError(f"{where}: ref {ref!r} does not match bcv {bcv!r}")
        if ref in seen_refs or bcv in seen_bcvs:
            raise ValueError(f"{where}: duplicate reference {ref!r} or bcv {bcv!r}")
        seen_refs.add(ref)
        seen_bcvs.add(bcv)

        status = case["status"]
        if status not in _POST_SILLUQ_CASE_STATUSES:
            raise ValueError(f"{where}/status: unknown status {status!r}")
        if case["form_source"] not in _POST_SILLUQ_FORM_SOURCES:
            raise ValueError(
                f"{where}/form_source: unknown source {case['form_source']!r}"
            )

        reports = _validate_string_list(case["reports"], where=f"{where}/reports")
        for report in reports:
            report_path = Path(report)
            if (
                report_path.is_absolute()
                or "\\" in report
                or not report.startswith("doc/")
                or not (paths.repo_root() / report_path).is_file()
            ):
                raise ValueError(f"{where}/reports: invalid report path {report!r}")

        images = _validate_string_list(
            case["images"], where=f"{where}/images", allow_empty=True
        )
        unknown_images = sorted(set(images) - _POST_SILLUQ_IMAGE_IDS)
        if unknown_images:
            raise ValueError(f"{where}/images: unknown identifiers {unknown_images}")
        mismatched_images = [
            image_id for image_id in images if _POST_SILLUQ_IMAGE_REFS[image_id] != ref
        ]
        if mismatched_images:
            raise ValueError(
                f"{where}/images: identifiers belong to another reference: "
                f"{mismatched_images}"
            )
        expected_sequence = _POST_SILLUQ_IMAGE_SEQUENCES.get(ref)
        if expected_sequence is not None and tuple(images) != expected_sequence:
            raise ValueError(
                f"{where}/images: expected exact sequence {expected_sequence}"
            )

        if status == "open-candidate":
            if "additional_sources" in case or "mam_editorial_basis" in case:
                raise ValueError(
                    f"{where}: open candidates do not take additions or an editorial basis"
                )
            _validate_string_list(
                case.get("transcriptions"), where=f"{where}/transcriptions"
            )
            if "sources" in case:
                _validate_post_silluq_sources(
                    case["sources"], bcv=bcv, where=f"{where}/sources"
                )
        else:
            if "transcriptions" in case or "sources" not in case:
                raise ValueError(
                    f"{where}: known cases require sources, not transcriptions"
                )
            _validate_post_silluq_sources(
                case["sources"], bcv=bcv, where=f"{where}/sources"
            )
            additions = case.get("additional_sources", [])
            if not isinstance(additions, list):
                raise ValueError(f"{where}/additional_sources: expected a list")
            addition_names: set[str] = set()
            for add_index, addition in enumerate(additions):
                add_where = f"{where}/additional_sources/{add_index}"
                if not isinstance(addition, dict):
                    raise ValueError(f"{add_where}: expected an object")
                _require_exact_keys(
                    addition,
                    required={"source", "state"},
                    allowed={"source", "state"},
                    where=add_where,
                )
                source = _require_nonempty_string(
                    addition["source"], where=f"{add_where}/source"
                )
                if source in addition_names:
                    raise ValueError(f"{add_where}: duplicate source {source!r}")
                addition_names.add(source)
                if addition["state"] not in _POST_SILLUQ_SOURCE_STATES:
                    raise ValueError(
                        f"{add_where}/state: unknown state {addition['state']!r}"
                    )
            editorial_basis = case.get("mam_editorial_basis")
            if editorial_basis is not None and (
                bcv != _MAM_POST_SILLUQ_VERSE or editorial_basis != "aleppo-default"
            ):
                raise ValueError(
                    f"{where}/mam_editorial_basis: unsupported value "
                    f"{editorial_basis!r} for {bcv}"
                )
    return cases


def load_post_silluq_koren_observations() -> list[dict]:
    """Load Koren observations, preserving incomplete states as non-results.

    Missing ``status`` is the backward-compatible spelling of ``complete``. A completed
    observation has a closed ``koren`` classification; an incomplete, deferred or skipped
    observation must not have one. Additional marks and notes remain separate from that
    classification.
    """
    path = paths.in_dir() / _POST_SILLUQ_KOREN_JSON
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected a root object")
    _require_exact_keys(
        payload,
        required={"about", "readings"},
        allowed={"about", "readings"},
        where=str(path),
    )
    _require_nonempty_string(payload["about"], where=f"{path}#about")
    readings = payload["readings"]
    if not isinstance(readings, list) or not readings:
        raise ValueError(f"{path}#readings: expected a nonempty list")

    normalized = []
    seen_refs: set[str] = set()
    seen_bcvs: set[str] = set()
    allowed = {
        "ref",
        "bcv",
        "status",
        "koren",
        "sheva",
        "additional_marks",
        "note",
        "date",
    }
    for index, raw in enumerate(readings):
        where = f"{path}#readings/{index}"
        if not isinstance(raw, dict):
            raise ValueError(f"{where}: expected an object")
        _require_exact_keys(
            raw,
            required={"ref", "date"},
            allowed=allowed,
            where=where,
        )
        ref = _require_nonempty_string(raw["ref"], where=f"{where}/ref")
        bcv = _full_ref_to_bcv(ref)
        if "bcv" in raw and raw["bcv"] != bcv:
            raise ValueError(f"{where}/bcv: does not match {ref!r}")
        if ref in seen_refs or bcv in seen_bcvs:
            raise ValueError(f"{where}: duplicate reference {ref!r}")
        seen_refs.add(ref)
        seen_bcvs.add(bcv)

        status = raw.get("status", "complete")
        if status not in _KOREN_STATUSES:
            raise ValueError(f"{where}/status: unknown status {status!r}")
        if status == "complete":
            if raw.get("koren") not in _KOREN_POSITIONS:
                raise ValueError(
                    f"{where}/koren: completed observation needs a position"
                )
        elif "koren" in raw:
            raise ValueError(
                f"{where}/koren: non-complete observation cannot be classified"
            )

        if "sheva" in raw and raw["sheva"] not in _KOREN_SHEVA_STATES:
            raise ValueError(f"{where}/sheva: unknown state {raw['sheva']!r}")
        if "additional_marks" in raw:
            _validate_string_list(
                raw["additional_marks"], where=f"{where}/additional_marks"
            )
        if "note" in raw:
            _require_nonempty_string(raw["note"], where=f"{where}/note")
        _validate_iso_date(raw["date"], where=f"{where}/date")
        normalized.append({**raw, "bcv": bcv, "status": status})
    return normalized


def _verse_final_chanted_word(words: list[str], *, bcv: str, source: str) -> str:
    """Locate the complete verse-final chanted word in a source's atom stream."""
    final_indexes = [index for index, word in enumerate(words) if psm.SOF_PASUQ in word]
    if len(final_indexes) != 1:
        raise ValueError(
            f"{source} {bcv}: expected one verse-final atom, found "
            f"{len(final_indexes)}"
        )
    final_index = final_indexes[0]
    first_index = final_index
    while first_index and words[first_index - 1].endswith(psm.MAQAF):
        first_index -= 1
    return "".join(words[first_index : final_index + 1])


def _mam_final_forms(bcvs: set[str]) -> dict[str, str]:
    """Lift each complete verse-final chanted word from tracked MAM-simple."""
    refs_by_book: dict[str, set[tuple[int, int]]] = {}
    for bcv in bcvs:
        bb, chnu, vrnu = _split(bcv)
        refs_by_book.setdefault(bb, set()).add((chnu, vrnu))
    loaded = mam_simple_verse.load_mam_simple_for_refs(
        paths.require_mam_simple_dir(), refs_by_book
    )
    missing = sorted(bcvs - set(loaded))
    if missing:
        raise ValueError(f"MAM-simple lacks requested references: {missing}")
    return {
        bcv: _verse_final_chanted_word(
            [
                word
                for word in payload["mam_simple_verse"]["vels"]
                if isinstance(word, str)
            ],
            bcv=bcv,
            source="MAM-simple",
        )
        for bcv, payload in loaded.items()
    }


def _case_forms(cases: list[dict], mam_forms: dict[str, str]) -> dict[str, str]:
    """Lift each case form from the ledger-declared tracked corpus."""
    forms = {}
    for case in cases:
        bcv = case["bcv"]
        if case["form_source"] == "mam":
            forms[bcv] = mam_forms[bcv]
        elif case["form_source"] == "uxlc":
            forms[bcv] = _verse_final_chanted_word(
                _uxlc_words(bcv), bcv=bcv, source="UXLC 3.9"
            )
        else:  # closed validation above makes this unreachable
            raise ValueError(f"Unknown case form source: {case['form_source']!r}")
    return forms


def _post_silluq_comparison(survey: dict) -> tuple[tuple[str, str], ...]:
    """The MAM and BHS forms relevant to 1 Samuel 17:5's post-silluq question.

    The row labelled "BHS" is UXLC 3.9's form, asserted equal to WLC 4.22's; no BHS
    text is read here. The page's claim that BHS has the form rests on Ben's reading of
    the printed BHS on 2026-09-09, which confirms the two marks, meteg after silluq.
    Ben's decision, the same day: the page's wording stands and takes no "checked"
    clause; this docstring and the review records are where the reading is recorded
    (doc/review-findings-2026-09-08.md, finding 3 and its State line).
    """
    letters = ("נחשת",)
    bhs_form_from_uxlc = _source_focus_word(
        _uxlc_words(_POST_SILLUQ_VERSE),
        _POST_SILLUQ_VERSE,
        letters,
        must_have=psm.SOF_PASUQ,
        source="UXLC 3.9",
    )
    bhs_form_from_wlc = _source_focus_word(
        _wlc_words(_POST_SILLUQ_VERSE),
        _POST_SILLUQ_VERSE,
        letters,
        must_have=psm.SOF_PASUQ,
        source="WLC 4.22",
    )
    assert (
        bhs_form_from_uxlc == bhs_form_from_wlc
    ), "the two BHS-derived transcriptions differ at 1 Samuel 17:5"
    return (
        (
            "MAM",
            _focus_word(survey, _POST_SILLUQ_VERSE, letters, must_have=psm.SOF_PASUQ),
        ),
        ("BHS", bhs_form_from_uxlc),
    )


def _mam_post_silluq_form(survey: dict) -> str:
    """MAM's verse-final form at 1 Kings 7:37, lifted from the survey."""
    return _focus_word(
        survey,
        _MAM_POST_SILLUQ_VERSE,
        ("לכלהנה",),
        must_have=psm.SOF_PASUQ,
    )


def _mam_post_silluq_statement(survey: dict, *, starts_sentence: bool = True) -> tuple:
    """The 1 Kings 7:37 MAM case, and what "ignore" means there.

    The definition is Ben's wording of 2026-09-09: the research deliberately reads the
    word as meteg-then-silluq, which is what the survey's stress oracle does, so the
    word counts as MBS_O and ``post_silluq.in_mam`` stays 0.
    """
    return (
        "At " if starts_sentence else "at ",
        _ref_link(_MAM_POST_SILLUQ_VERSE),
        ", in MAM, there is a ",
        _ROM_METEG,
        " after ",
        _ROM_SILLUQ,
        " in ",
        wrap_hebrew_runs(_mam_post_silluq_form(survey)),
        ". We ignore it for the purposes of this research. ",
        author.dquote("Ignore"),
        " means treat this word as a ",
        _ROM_METEG,
        "-then-",
        _ROM_SILLUQ,
        " word, i.e. deliberately misinterpret the marks. How we treat this mark has"
        " little effect on our census and no effect on the bulk of the results of this"
        " research, since they concern ",
        _ROM_METEG,
        " immediately after a conjunctive on the primary stress of the word.",
    )
