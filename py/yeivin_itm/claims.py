"""Project Ben's approved meteg claims from the independent public survey.

Population definitions and exclusions are named here; the renderer reads only
the minimized tracked claim product. No workbook-era filters are inferred.
"""

from __future__ import annotations

import json
from typing import NamedTuple

from accgram.meteg_before_stress import FULLY_REGULAR
from mb_cmn import bib_locales, cantsys, hebrew_accents as ha
from mb_cmn import hebrew_punctuation as hpu
from mb_cmn import uni_denorm
from yeivin_itm import paths, claim_schema, quoted_forms


class Measurement(NamedTuple):
    """One named fraction: its numerator and denominator records, as the analysis
    holds them, its definition and its own exclusions."""

    name: str
    numerator: list
    denominator: list
    definition: str
    exclusions: tuple


def read():
    """Read and pin the minimized tracked product, without reading the analysis."""
    allowed = {
        "LICENSE.md",
        "README.md",
        "meteg-claims.json",
        "schema/meteg-claims-v2.schema.json",
    }
    found = {
        path.relative_to(paths.product_dir()).as_posix()
        for path in paths.product_dir().rglob("*")
        if path.is_file()
    }
    if found != allowed:
        raise ValueError(f"Unexpected Yeivin product files: {found ^ allowed}")
    result = _read_json((paths.product_dir() / "meteg-claims.json").read_bytes())
    claim_schema.validate(result)
    return result


def from_analysis():
    """Project the independent public input, then enforce the approved prose pins
    and Ben's quoted forms."""
    result, failures = projection()
    claim_schema.validate(result)
    if failures:
        raise ValueError(
            "Ben's quoted forms no longer hold; review his footnotes: "
            + "; ".join(failures)
        )
    return result


def projection():
    """The claims projected from the analysis, and how Ben's quoted forms fail of it.

    Neither is checked against the approved pins: ``from_analysis`` enforces them, and
    ``publication.review_claims`` reports how a changed analysis would differ.
    """
    source = paths.product_dir().parent / claim_schema.INPUT_IDENTITY
    survey = _read_json(source.read_bytes())
    measurements = measured(survey)
    result = _claims(measurements, input_identity=claim_schema.INPUT_IDENTITY)
    claim_schema.validate_shape(result)
    return result, quoted_form_failures(survey, measurements)


def quoted_form_failures(survey, measurements):
    """Each way that Ben's quoted forms fail of the analysis, as one line of text.

    For each of quoted_forms.QUOTED_FORMS, exactly one ordinary record at its verse
    must have its form. Both are compared in MAM-normal mark order, the record's gray
    maqaf read as a maqaf, since the footnote at Psalms 137:1 quotes a maqaf there.
    That record must have the form's pattern, and be in the numerator of each
    measurement of its ``member_of`` and of none of its ``not_member_of``.
    ``measurements`` is what ``measured(survey)`` returns. The forms that enumerate
    a measurement must be exactly that measurement's numerator records.
    """
    cases = survey["ordinary"]["cases"]
    numerators = {
        measurement.name: measurement.numerator for measurement in measurements
    }
    failures = []
    for quoted in quoted_forms.QUOTED_FORMS:
        where = f"quoted form {quoted.module} {quoted.sloc} {quoted.form}"
        verse = quoted_forms.verse(quoted.sloc)
        at_verse = [case for case in cases if _verse(case) == verse]
        found = [
            case
            for case in at_verse
            if _record_form(case) == uni_denorm.give_std_mark_order(quoted.form)
        ]
        if len(found) != 1:
            failures.append(
                f"{where}: {len(found)} ordinary records at the verse have the form, "
                f"not 1; the verse's records are {[c['hebrew'] for c in at_verse]}"
            )
            continue
        (case,) = found
        if case["pattern"] != quoted.pattern:
            failures.append(
                f"{where}: its pattern is {case['pattern']}, not {quoted.pattern}"
            )
        for name in quoted.member_of:
            if not any(record is case for record in numerators[name]):
                failures.append(f"{where}: not counted in {name}")
        for name in quoted.not_member_of:
            if any(record is case for record in numerators[name]):
                failures.append(f"{where}: counted in {name}")
    enumerated = sorted(
        {quoted.enumerates for quoted in quoted_forms.QUOTED_FORMS if quoted.enumerates}
    )
    for name in enumerated:
        listed = {
            (
                quoted_forms.verse(quoted.sloc),
                uni_denorm.give_std_mark_order(quoted.form),
            )
            for quoted in quoted_forms.QUOTED_FORMS
            if quoted.enumerates == name
        }
        counted = {(_verse(case), _record_form(case)) for case in numerators[name]}
        if listed != counted:
            failures.append(
                f"enumerated measurement {name}: the footnote lists "
                f"{sorted(listed)}, the analysis counts {sorted(counted)}"
            )
    return failures


def _verse(case):
    return bib_locales.parse_short_bcv(case["bcv"])


def _record_form(case):
    """A record's chanted word in MAM-normal mark order, its gray maqaf a maqaf."""
    return uni_denorm.give_std_mark_order(case["hebrew"].replace(hpu.NU_GMAQ, hpu.MAQ))


def survey():
    """Write only the minimized claim file after all pins and quoted forms pass."""
    result = from_analysis()
    destination = paths.product_dir() / "meteg-claims.json"
    data = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    if not destination.is_file() or destination.read_bytes() != data:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)


def check():
    """Require the tracked claim data to equal its public-input projection."""
    if read() != from_analysis():
        raise ValueError(
            "Yeivin meteg claims differ from the independent public analysis"
        )


def _read_json(data):
    """Reject duplicate object keys instead of silently overwriting their values."""

    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"Duplicate meteg claim/input key: {key}")
            result[key] = value
        return result

    return json.loads(data, object_pairs_hook=unique_object)


def _select(cases, patterns, *, accent=None, meteg=None):
    """One named structural population, optionally restricted by accent/meteg."""
    return [
        case
        for case in cases
        if case["pattern"] in patterns
        and (accent is None or case["accent_class"] == accent)
        and (meteg is None or case["target_meteg"] == meteg)
    ]


def _primary_accent(case):
    """Read the accent grammar of the generic Hebrew already in the analysis."""
    from phonetic_mam.core import bccvecs_that_are_known as knowns
    from phonetic_mam.core import separate_accents, vowar_and_accar

    book, chapter, verse = bib_locales.parse_short_bcv(case["bcv"])
    bcvt = bib_locales.mk_bcvtmam(book, chapter, verse)
    system = cantsys.get_cantsys_from_is_poetcant(bib_locales.is_poetcant(bcvt))
    _vowels, accents = vowar_and_accar.vowar_and_accar(case["hebrew"])
    _letters, bccvec = separate_accents.get_sepacc(system, accents)
    return bccvec[knowns.CS_GET_STRESS_INFO_FROM_BCCVEC[system][bccvec]]


_COMMON_EXCLUSIONS = (
    "The bet cantillation strand is excluded; the alef strand is counted once.",
    "Samekh-qamats alternatives are excluded; the ordinary dalet projection is used.",
    "Chanted words not classified by the maintained FR/AFR algorithm are excluded.",
    "No historical workbook exclusion is inferred or added to fit a published value.",
)


def _claims(measurements, *, input_identity: str) -> dict:
    """The claim file's value: named populations and exact integer fractions."""
    populations = {}
    fractions = {}
    for measurement in measurements:
        n_count, d_count = len(measurement.numerator), len(measurement.denominator)
        if not d_count:
            raise ValueError(f"Empty claim population: {measurement.name}")
        populations[measurement.name] = {
            "definition": measurement.definition,
            "exclusions": [*_COMMON_EXCLUSIONS, *measurement.exclusions],
        }
        fractions[measurement.name] = {
            "numerator": n_count,
            "denominator": d_count,
            "percentage": 100 * n_count / d_count,
        }
    return {
        "schema": claim_schema.SCHEMA,
        "input": {"identity": input_identity},
        "populations": populations,
        "measurements": fractions,
    }


def measured(survey: dict) -> list:
    """Every named measurement of the survey, in order, with its records.

    The one list feeds both the claim file and the check of Ben's quoted forms.
    """
    if survey["schema"] != "meteg-before-stress-v1":
        raise ValueError("Unknown independent pre-stress-meteg survey schema")
    cases = survey["ordinary"]["cases"]
    fr = _select(cases, FULLY_REGULAR)
    fr_dsg = _select(cases, FULLY_REGULAR, accent="disj", meteg=False)
    fr_cwg = _select(cases, FULLY_REGULAR, accent="conj", meteg=True)
    measurements = []

    def add(name, numerator, denominator, definition, *, exclusions=()):
        measurements.append(
            Measurement(name, numerator, denominator, definition, tuple(exclusions))
        )

    add(
        "fully-regular.all",
        fr,
        fr,
        "All classified FR1, FR2, and FR3 chanted words, both accent classes.",
        exclusions=("AFR1–AFR4, XAFR1, and MISC are excluded.",),
    )
    add(
        "fully-regular.disjunctive-without-target-meteg",
        fr_dsg,
        fr,
        "FR1–FR3 disjunctives lacking meteg on the target main syllable, over all FR1–FR3.",
    )
    add(
        "fully-regular.conjunctive-with-target-meteg",
        fr_cwg,
        fr,
        "FR1–FR3 conjunctives with meteg on the target main syllable, over all FR1–FR3.",
    )
    add(
        "fully-regular.exceptions",
        [*fr_dsg, *fr_cwg],
        fr,
        "The disjoint union of FR1–FR3 disjunctives without and conjunctives with target meteg, over all FR1–FR3.",
    )
    for name, key, value in (
        ("other-meteg", "other_meteg_count", None),
        ("qadma-or-metigah", "accent_on_target", "(qom)"),
        ("merkha", "accent_on_target", "(mer)"),
    ):
        selected = (
            [case for case in fr_dsg if case[key]]
            if value is None
            else [case for case in fr_dsg if case[key] == value]
        )
        add(
            f"fully-regular.disjunctive-without-target-meteg.{name}",
            selected,
            fr_dsg,
            f"FR1–FR3 disjunctives without target meteg whose {key} "
            + ("is nonzero" if value is None else f"equals {value}")
            + ", over all FR1–FR3 disjunctives without target meteg.",
        )
    for name, target_accent, primary_accent, label in (
        ("metigah", "(qom)", ha.ZAQ_Q, "metigah with zaqef qatan"),
        (
            "merkha-with-azla-legarmeh",
            "(mer)",
            ha.NU_AZL_LEG,
            "merkha paired with azla legarmeh",
        ),
    ):
        add(
            f"fully-regular.disjunctive-without-target-meteg.{name}",
            [
                case
                for case in fr_dsg
                if case["accent_on_target"] == target_accent
                and _primary_accent(case) == primary_accent
            ],
            fr_dsg,
            f"FR1–FR3 disjunctives without target meteg, with {label} at the target, over all FR1–FR3 disjunctives without target meteg.",
            exclusions=(
                "The footnote's stated primary-accent qualification is required; other primary accents are excluded.",
            ),
        )
    for pattern in FULLY_REGULAR:
        add(
            f"{pattern}.conjunctive-with-target-meteg",
            _select(cases, (pattern,), accent="conj", meteg=True),
            _select(cases, (pattern,), accent="conj"),
            f"{pattern} conjunctives with target meteg, over all {pattern} conjunctives.",
        )
    for name, patterns in (
        ("fully-regular", FULLY_REGULAR),
        ("AFR1", ("AFR1",)),
        ("AFR4", ("AFR4",)),
    ):
        add(
            f"{name}.disjunctive-exception-rate",
            _select(cases, patterns, accent="disj", meteg=False),
            _select(cases, patterns, accent="disj"),
            f"{name} disjunctives without target meteg, over all {name} disjunctives.",
            exclusions=("Conjunctives and other structural patterns are excluded.",),
        )
        add(
            f"{name}.target-meteg-rate",
            _select(cases, patterns, meteg=True),
            _select(cases, patterns),
            f"{name} chanted words with target meteg, over all {name} chanted words regardless of accent class.",
        )
    for present in (True, False):
        state = "with" if present else "without"
        add(
            f"XAFR1.disjunctive-{state}-target-meteg",
            _select(cases, ("XAFR1",), accent="disj", meteg=present),
            _select(cases, ("XAFR1",), accent="disj"),
            f"XAFR1 disjunctives {state} target meteg, over all XAFR1 disjunctives; these remain excluded from AFR1.",
        )
    return measurements
