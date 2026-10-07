"""Record near-Aleppo's build populations and check them against the local census.

After every check passes, the build writes in/near-aleppo/build-populations.json:
each phase's counts and the verses where it recorded them. No count or site in
the file is pinned. Each section lists the labels of _SEEDS first, in that order,
zeros included, and then every other label the build tallied, in sorted order, so
that the file's diff shows whatever a change to MAM's text or to the build moved.

assert_census_agrees is a differential. The five census instruments of
py/near_aleppo/census/ count populations from MAM's text alone, and their tracked
results are in in/near-aleppo/census/. Each population they count must agree with
the build's own count of it, less, for the qamats qatan, the removals that phase 3
names in _KQ_QAMATS_QATAN_REMOVED_VERSES.
"""

import json
import os
import re
import tempfile
from pathlib import Path

from near_aleppo import build_paths
from near_aleppo import phase3_policies as phase3
from near_aleppo import phase5_readings as phase5
from near_aleppo import phase6_mam_targets as phase6

_NEAR_ALEPPO = build_paths.input_dir()
POPULATIONS_PATH = _NEAR_ALEPPO / "build-populations.json"
_CENSUS_EXPECTED = _NEAR_ALEPPO / "census"

_SCHEMA_VERSION = 5
_COUNT_SECTIONS = (
    "phase2_counts",
    "phase3_counts",
    "phase5_counts",
    "phase6_counts",
    "flag_counts",
)
_SITE_SECTIONS = ("phase3_sites", "phase5_sites", "flag_sites")
_SECTIONS = (
    "phase2_counts",
    "phase3_counts",
    "phase3_sites",
    "phase5_counts",
    "phase5_sites",
    "phase6_counts",
    "flag_counts",
    "flag_sites",
)

# These phase-2 counters are the settled column of template_inventory.py.
_CENSUS_PHASE2_LABELS = (
    "מ:קמץ",
    "מ:דחי",
    "מ:צינור",
    "מ:לגרמיה-2",
    "מ:פסק",
    "מ:מקף אפור",
    "נוסח",
    "מ:הערה-2",
    "מ:כפול",
    "מ:קו״כ-אם-2",
    "כו״ק",
    "קו״כ",
    "מ:כו״ק מיוחד",
    "כתיב ולא קרי",
    "קרי ולא כתיב",
)

# Each accent whose stress helpers phase 3 counts, with the census's name for it.
_STRESS_HELPER_CENSUS_NAMES = (
    (phase3.PASHTA, "pashta"),
    (phase3.SEGOLTA, "segolta"),
    (phase3.TELISHA_GEDOLA, "telisha gedolah"),
    (phase3.TELISHA_QETANA, "telisha qetanah"),
    (phase3.UNICODE_ZINOR, "zarqa"),
)
# What phase 3 can do with a stress helper; only the pashta's can be kept for a
# letter standing between, and phase 3 counts no other accent's that way.
_STRESS_HELPER_OUTCOMES = (
    phase3._STRIPPED,
    phase3._BETWEEN,
    phase3._KEPT_BY_CODEX,
    phase3._KEPT_BY_LENINGRAD,
)


def load():
    """Load the build's population file, checking its closed shape."""
    value = json.loads(POPULATIONS_PATH.read_text(encoding="utf-8"))
    if (
        list(value) != ["schema_version", *_SECTIONS]
        or value["schema_version"] != _SCHEMA_VERSION
    ):
        raise RuntimeError(
            f"{POPULATIONS_PATH}: expected schema_version {_SCHEMA_VERSION} and the "
            f"sections {list(_SECTIONS)}, found {list(value)}"
        )
    return value


def _single_int(path, pattern):
    text = path.read_text(encoding="utf-8")
    values = re.findall(pattern, text, flags=re.MULTILINE)
    if len(values) != 1:
        raise RuntimeError(
            f"Expected one match for {pattern!r} in {path}, found {len(values)}"
        )
    return int(values[0])


def _template_inventory():
    path = _CENSUS_EXPECTED / "template_inventory.txt"
    rows = {}
    pattern = re.compile(r"^(.+?)\s{2,}(\d+)\s+(\d+)\s{2,}", re.MULTILINE)
    for name, raw, settled in pattern.findall(path.read_text(encoding="utf-8")):
        rows[name.rstrip()] = {"raw": int(raw), "settled": int(settled)}
    missing = [name for name in _CENSUS_PHASE2_LABELS if name not in rows]
    if missing:
        raise RuntimeError(
            f"{path} lacks build populations: {', '.join(repr(x) for x in missing)}"
        )
    return rows


def assert_census_agrees(resolver, policies, readings, mam_targets):
    """Raise one error listing every population where the build and census disagree.

    ``resolver``, ``policies``, ``readings`` and ``mam_targets`` hold one build's
    counts, as main_build.build returns them.
    """
    problems = []

    def agree(what, build, census):
        if build != census:
            problems.append(f"{what}: build {build}, census {census}")

    inventory = _template_inventory()
    for label in _CENSUS_PHASE2_LABELS:
        agree(label, resolver.counts[label], inventory[label]["settled"])

    counts = policies.counts
    agree(
        phase3._QAMATS_QATAN,
        counts[phase3._QAMATS_QATAN],
        _single_int(
            _CENSUS_EXPECTED / "qamats_params.txt",
            r"^U\+05C7 in the whole base text taking ד: (\d+)$",
        )
        - len(phase3._KQ_QAMATS_QATAN_REMOVED_VERSES),
    )

    divine_path = _CENSUS_EXPECTED / "divine_name_split.txt"
    agree(
        phase3._ELOHIM_SHEVA,
        counts[phase3._ELOHIM_SHEVA],
        _single_int(divine_path, r"^\s*Elohim \(hiriq on vav\)\s+hataf segol\s+(\d+)$"),
    )
    agree(
        phase3._ELOHIM_BARE_YOD,
        counts[phase3._ELOHIM_BARE_YOD],
        _single_int(divine_path, r"^\s*Elohim \(hiriq on vav\)\s+none/other\s+(\d+)$"),
    )
    agree(
        "Adonai reading: holam stripped and kept",
        counts[phase3._ADONAI_HOLAM_STRIPPED] + counts[phase3._ADONAI_HOLAM_KEPT],
        _single_int(divine_path, r"^\s*Adonai \(qamats on vav\)\s+(\d+)$"),
    )

    adonai_path = _CENSUS_EXPECTED / "adonai_census.txt"
    title_total = _single_int(
        adonai_path, r"^\s*divine title \(qamats on nun\)\s+(\d+)$"
    )
    agree(
        "divine title: holam stripped and kept",
        counts[phase3._TITLE_HOLAM_STRIPPED] + counts[phase3._TITLE_HOLAM_KEPT],
        title_total,
    )
    agree(
        phase3._NOT_TITLE,
        counts[phase3._NOT_TITLE],
        _single_int(adonai_path, r"^\s*TOTAL (\d+)$") - title_total,
    )

    helper_path = _CENSUS_EXPECTED / "stress_helper_census.txt"
    pashta_stripped = phase3._stress_helper_label(phase3.PASHTA, phase3._STRIPPED)
    agree(
        pashta_stripped,
        counts[pashta_stripped],
        _single_int(
            helper_path,
            r"^  of those, with the stress helper on the second-to-last letter: "
            r".* total (\d+)$",
        ),
    )
    for accent, name in _STRESS_HELPER_CENSUS_NAMES:
        agree(
            f"stress helpers: {name}'s stress helpers, every outcome",
            sum(
                counts[phase3._stress_helper_label(accent, what)]
                for what in _STRESS_HELPER_OUTCOMES
            ),
            _single_int(
                helper_path,
                rf"^{re.escape(name)} atoms with a stress helper(?:, .*)?: "
                r".* total (\d+)$",
            ),
        )

    agree(phase5._NOTES, readings.counts[phase5._NOTES], inventory["נוסח"]["settled"])
    for name in ("נוסח", "מ:הערה-2"):
        label = name + phase6._REACHED
        agree(label, mam_targets.counts[label], inventory[name]["settled"])

    if problems:
        raise AssertionError(
            "The near-Aleppo build disagrees with its census: " + "; ".join(problems)
        )


def render(resolver, policies, readings, mam_targets, flags):
    """The text of the population file for one build's recorded counts and sites."""
    tallies = {
        "phase2_counts": resolver.counts,
        "phase3_counts": policies.counts,
        "phase3_sites": policies.sites,
        "phase5_counts": readings.counts,
        "phase5_sites": readings.sites,
        "phase6_counts": mam_targets.counts,
        "flag_counts": flags.counts,
        "flag_sites": flags.sites,
    }
    value = {"schema_version": _SCHEMA_VERSION}
    lines = ["{", f'  "schema_version": {_SCHEMA_VERSION},']
    for number, section in enumerate(_SECTIONS):
        tally = tallies[section]
        seeds = _SEEDS[section]
        labels = [*seeds, *sorted(set(tally) - set(seeds))]
        if section in _COUNT_SECTIONS:
            entries = [(label, tally[label]) for label in labels]
        else:
            entries = [
                (label, [list(site) for site in tally.get(label, [])])
                for label in labels
            ]
        value[section] = dict(entries)
        lines.append(f"  {json.dumps(section)}: {{")
        for index, (label, entry) in enumerate(entries):
            comma = "," if index < len(entries) - 1 else ""
            key = json.dumps(label, ensure_ascii=False)
            if section in _COUNT_SECTIONS:
                lines.append(f"    {key}: {entry}{comma}")
            elif not entry:
                lines.append(f"    {key}: []{comma}")
            else:
                lines.append(f"    {key}: [")
                lines += [
                    "      "
                    + json.dumps(site, ensure_ascii=False)
                    + ("," if site_index < len(entry) - 1 else "")
                    for site_index, site in enumerate(entry)
                ]
                lines.append(f"    ]{comma}")
        lines.append("  }" + ("," if number < len(_SECTIONS) - 1 else ""))
    lines.append("}")
    text = "\n".join(lines) + "\n"
    if json.loads(text) != value:
        raise AssertionError("The population file's layout changed its JSON value")
    return text


def write(text):
    """Atomically replace the population file with ``text``."""
    POPULATIONS_PATH.parent.mkdir(parents=True, exist_ok=True)
    handle = tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        newline="\n",
        prefix=POPULATIONS_PATH.name + ".",
        suffix=".tmp",
        dir=POPULATIONS_PATH.parent,
        delete=False,
    )
    temp_path = Path(handle.name)
    try:
        with handle:
            handle.write(text)
        os.replace(temp_path, POPULATIONS_PATH)
    finally:
        if temp_path.exists():
            temp_path.unlink()
    print(f"Build populations written: {POPULATIONS_PATH}")


# The labels each section of the population file lists first, in this order, so
# that a label the build no longer tallies stays in the file at zero, or with no
# sites, until this table drops it. They are the labels of the file as it stood at
# schema version 4, when the build began writing it; the documentation pages read
# several by key, among them five zeros of phase 3: the pashta's and segolta's stress
# helpers kept by a note citing the codex or ל, and the zarqa's kept by a note
# citing ל.
_SEEDS = {
    "phase2_counts": (
        "מ:קמץ",
        "מ:דחי",
        "מ:צינור",
        "מ:לגרמיה-2",
        "מ:פסק",
        "מ:מקף אפור",
        "נוסח",
        "מ:הערה-2",
        "מ:כפול",
        "מ:קו״כ-אם-2",
        "כו״ק",
        "קו״כ",
        "מ:כו״ק מיוחד",
        "כתיב ולא קרי",
        "קרי ולא כתיב",
        "special letter word flattened",
        "special letter word kept, large",
        "special letter word kept, suspended",
        "מ:קמץ (unselected parameter)",
        "מ:דחי (unselected parameter)",
        "מ:לגרמיה-2 (unselected parameter)",
        "special letter word flattened (unselected parameter)",
    ),
    "phase3_counts": (
        "HEBREW POINT QAMATS QATAN changed to HEBREW POINT QAMATS",
        "HEBREW POINT QAMATS QATAN changed to HEBREW POINT QAMATS (unselected parameter)",
        "Elohim reading: sheva for the hataf segol on the yod",
        "Elohim reading: sheva for the hataf segol on the yod (unselected parameter)",
        "Elohim reading: yod with no vowel, unchanged",
        "Elohim reading: yod with no vowel, unchanged (unselected parameter)",
        "Adonai reading: holam on the first he stripped",
        "Adonai reading: holam on the first he stripped (unselected parameter)",
        "Adonai reading: holam kept where a note records the codex's",
        "Adonai reading: holam kept where a note records the codex's (unselected parameter)",
        "divine title: holam on the dalet stripped",
        "divine title: holam on the dalet stripped (unselected parameter)",
        "divine title: holam kept where a note records the codex's",
        "divine title: holam kept where a note records the codex's (unselected parameter)",
        "atom ending in אדני without a qamats on the nun, unchanged",
        "atom ending in אדני without a qamats on the nun, unchanged (unselected parameter)",
        "revia mugrash: revia removed from the geresh muqdam's letter",
        "revia mugrash: revia removed from the geresh muqdam's letter (unselected parameter)",
        "revia mugrash: revia kept where chapter 5 records the codex's",
        "revia mugrash: revia kept where chapter 5 records the codex's (unselected parameter)",
        "revia mugrash: geresh muqdam moved to the compound's first atom",
        "revia mugrash: geresh muqdam moved to the compound's first atom (unselected parameter)",
        "geresh muqdam with the revia on another letter, unchanged",
        "geresh muqdam with the revia on another letter, unchanged (unselected parameter)",
        "revia mugrash: removal agreeing with a codex form its note quotes",
        "revia mugrash: removal whose note's codex form lacks the geresh muqdam too",
        "ole on the yored's letter: ole removed",
        "ole on the yored's letter: ole removed (unselected parameter)",
        "ole on a letter without the yored, unchanged",
        "ole on a letter without the yored, unchanged (unselected parameter)",
        "ole on the yored's letter: removal agreeing with the codex form its note quotes",
        "ketiv/qere apparatus: template replaced by the codex form its note quotes",
        "ketiv/qere apparatus: template replaced by its pointed ketiv",
        "ketiv/qere apparatus: template replaced by its pointed qere, the spelling its note's prose gives the codex",
        "ketiv/qere apparatus: template replaced by MAM's ketiv pointed by the transplant",
        "ketiv/qere apparatus: template kept where the codex form is doubt-marked",
        "ketiv/qere apparatus: transplant agreeing with the codex form a note quotes",
        "ketiv/qere apparatus: transplant agreeing with MAM's pointed ketiv",
        "ketiv/qere apparatus: pointed qere equal to the form its note's prose gives the codex, less the form's masorah circles",
        "hataf on a non-guttural: sheva and varika replaced by a hataf patah",
        "hataf on a non-guttural: sheva and varika replaced by a hataf qamats",
        "hataf on a non-guttural: varika replaced by a hiriq, the sheva kept",
        "hataf on a non-guttural: restoration agreeing with a form its note quotes",
        "stress helpers: pashta's stress helper stripped",
        "stress helpers: pashta's stress helper kept, a letter standing between",
        "stress helpers: pashta's stress helper kept by a note whose agreeing clause cites the codex for the doubling",
        "stress helpers: pashta's stress helper kept by a note whose agreeing clause cites ל for the doubling, no clause citing the codex",
        "stress helpers: segolta's stress helper stripped",
        "stress helpers: segolta's stress helper kept by a note whose agreeing clause cites the codex for the doubling",
        "stress helpers: segolta's stress helper kept by a note whose agreeing clause cites ל for the doubling, no clause citing the codex",
        "stress helpers: telisha qetanah's stress helper stripped",
        "stress helpers: telisha qetanah's stress helper kept by a note whose agreeing clause cites the codex for the doubling",
        "stress helpers: telisha qetanah's stress helper kept by a note whose agreeing clause cites ל for the doubling, no clause citing the codex",
        "stress helpers: telisha gedolah's stress helper stripped",
        "stress helpers: telisha gedolah's stress helper kept by a note whose agreeing clause cites the codex for the doubling",
        "stress helpers: telisha gedolah's stress helper kept by a note whose agreeing clause cites ל for the doubling, no clause citing the codex",
        "stress helpers: zarqa's stress helper stripped",
        "stress helpers: zarqa's stress helper kept by a note whose agreeing clause cites the codex for the doubling",
        "stress helpers: zarqa's stress helper kept by a note whose agreeing clause cites ל for the doubling, no clause citing the codex",
        "stress helpers: pashta's stress helper stripped (unselected parameter)",
        "stress helpers: pashta's stress helper kept, a letter standing between (unselected parameter)",
        "stress helpers: pashta's stress helper kept by a note whose agreeing clause cites the codex for the doubling (unselected parameter)",
        "stress helpers: pashta's stress helper kept by a note whose agreeing clause cites ל for the doubling, no clause citing the codex (unselected parameter)",
        "stress helpers: segolta's stress helper stripped (unselected parameter)",
        "stress helpers: segolta's stress helper kept by a note whose agreeing clause cites the codex for the doubling (unselected parameter)",
        "stress helpers: segolta's stress helper kept by a note whose agreeing clause cites ל for the doubling, no clause citing the codex (unselected parameter)",
        "stress helpers: telisha qetanah's stress helper stripped (unselected parameter)",
        "stress helpers: telisha qetanah's stress helper kept by a note whose agreeing clause cites the codex for the doubling (unselected parameter)",
        "stress helpers: telisha qetanah's stress helper kept by a note whose agreeing clause cites ל for the doubling, no clause citing the codex (unselected parameter)",
        "stress helpers: telisha gedolah's stress helper stripped (unselected parameter)",
        "stress helpers: telisha gedolah's stress helper kept by a note whose agreeing clause cites the codex for the doubling (unselected parameter)",
        "stress helpers: telisha gedolah's stress helper kept by a note whose agreeing clause cites ל for the doubling, no clause citing the codex (unselected parameter)",
        "stress helpers: zarqa's stress helper stripped (unselected parameter)",
        "stress helpers: zarqa's stress helper kept by a note whose agreeing clause cites the codex for the doubling (unselected parameter)",
        "stress helpers: zarqa's stress helper kept by a note whose agreeing clause cites ל for the doubling, no clause citing the codex (unselected parameter)",
        "stress helpers: geresh or gershayim removed with a telisha gedolah's stress helper",
        "stress helpers: geresh or gershayim removed with a telisha gedolah's stress helper (unselected parameter)",
        "stress helpers: telisha-gedolah word equal to the form its table names",
        "stress helpers: stripped stress helper's atom equal to a codex form its note quotes",
        "stress helpers: kept stress helper's atom doubled in a codex form its note quotes",
        "maqaf: maqafs added",
        "maqaf: clause form has a maqaf inside one target atom",
        "maqaf: clause form has a space where the target had a maqaf",
        "maqaf: undoubted clauses applied",
        "maqaf: bang-marked clauses applied",
    ),
    "phase3_sites": (
        "Elohim reading: yod with no vowel, unchanged",
        "Adonai reading: holam kept where a note records the codex's",
        "divine title: holam kept where a note records the codex's",
        "revia mugrash: revia kept where chapter 5 records the codex's",
        "revia mugrash: geresh muqdam moved to the compound's first atom",
        "revia mugrash: removal whose note's codex form lacks the geresh muqdam too",
        "ole on the yored's letter: ole removed",
        "ole on the yored's letter: removal in no note's target",
        "ketiv/qere apparatus: template replaced by the codex form its note quotes",
        "ketiv/qere apparatus: template replaced by its pointed ketiv",
        "ketiv/qere apparatus: template replaced by its pointed qere, the spelling its note's prose gives the codex",
        "ketiv/qere apparatus: template replaced by MAM's ketiv pointed by the transplant",
        "ketiv/qere apparatus: template kept where the codex form is doubt-marked",
        "hataf on a non-guttural: varika replaced by a hiriq, the sheva kept",
        "hataf on a non-guttural: vowel from the clause headed ל, the forms disagreeing",
        "hataf on a non-guttural: vowel from the forms of the note's agreeing clause",
        "stress helpers: kept by a note citing the codex",
        "stress helpers: kept by a note citing ל",
        "stress helpers: stripped in the target of a note whose agreeing clause speaks of doubling",
        "stress helpers: geresh or gershayim removed with a telisha gedolah's stress helper",
        "stress helpers: kept pashta's stress helper whose note quotes the codex's pashta alone",
        "maqaf: maqafs added",
        "maqaf: clause form has a maqaf inside one target atom",
        "maqaf: clause form has a space where the target had a maqaf",
        "maqaf: undoubted clauses applied",
        "maqaf: bang-marked clauses applied",
    ),
    "phase5_counts": (
        "codex readings: notes walked",
        "codex readings: empty clauses in note bodies",
        "codex readings: direct codex siglum elements",
        "codex readings: direct differing clauses",
        "codex readings: verses with a direct differing clause",
        "codex readings: prose-led heads ending in a codex siglum, held pending",
        "codex readings: apply-candidate (single-pointed-form)",
        "codex readings: apply-candidate (single-pointed-form), bang-marked",
        "codex readings: do-not-apply (doubt-siglum)",
        "codex readings: do-not-apply (doubt-siglum), bang-marked",
        "codex readings: do-not-apply (prose-description)",
        "codex readings: do-not-apply (prose-description), bang-marked",
        "codex readings: do-not-apply (doubt-form)",
        "codex readings: do-not-apply (doubt-form), bang-marked",
        "codex readings: policy-pending (ketiv-qere-plane)",
        "codex readings: policy-pending (ketiv-qere-plane), bang-marked",
        "codex readings: policy-pending (candidate-form-punctuation)",
        "codex readings: policy-pending (candidate-form-punctuation), bang-marked",
        "codex readings: policy-pending (candidate-form-count-0)",
        "codex readings: policy-pending (candidate-form-count-0), bang-marked",
        "codex readings: apply-candidate already in place",
        "codex readings: apply-candidate already in place, bang-marked",
        "codex readings: apply-candidate in place, its form lacking the paseq glyph that ends the target",
        "codex readings: apply-candidate in place, its form lacking the paseq glyph that ends the target, bang-marked",
        "codex readings: applied, the form replacing the whole of a plain target",
        "codex readings: applied, the form replacing the whole of a plain target, bang-marked",
        "codex readings: applied, the form replacing named atoms of a plain target",
        "codex readings: applied, the form replacing named atoms of a plain target, bang-marked",
        "codex readings: applied, the form written into the selected parameter of the one kept template that is the target",
        "codex readings: applied, the form written into the selected parameter of the one kept template that is the target, bang-marked",
        "codex readings: ketiv/qere plane reading in place in a qere parameter",
        "codex readings: ketiv/qere plane reading in place in a qere parameter, bang-marked",
        "codex readings: ketiv/qere plane reading in place through phase 3's ketiv/qere apparatus",
        "codex readings: ketiv/qere plane reading in place through phase 3's ketiv/qere apparatus, bang-marked",
        "codex readings: pointed ketiv written as the form stands",
        "codex readings: pointed ketiv written as the form stands, bang-marked",
        "codex readings: pointed ketiv written with a named adjustment",
        "codex readings: pointed ketiv written with a named adjustment, bang-marked",
        "codex readings: ketiv/qere plane reading pending by name",
        "codex readings: ketiv/qere plane reading pending by name, bang-marked",
        "codex readings: ketiv/qere plane reading at a one-sided template, left for later work",
        "codex readings: ketiv/qere plane reading at a one-sided template, left for later work, bang-marked",
        "codex readings: pointed ketiv ending in the qere's trailing maqaf",
        "codex readings: pending, the form stopping at the codex's space for a qere without ketiv",
        "codex readings: pending, the form stopping at the codex's space for a qere without ketiv, bang-marked",
        "codex readings: not applied, and flagged",
        "codex readings: not applied, and flagged, bang-marked",
        "codex readings: note targets changed",
        "codex readings: note targets changed, bang-marked",
        "codex readings: applied readings with a configuration a phase 3 policy removes",
        "codex readings: differing clauses whose head names שיטת-א",
        "codex readings: differing clauses whose head names שיטת-א, the head being prose",
        "codex readings: שיטת-א reading already in place",
        "codex readings: שיטת-א reading not applied",
        "codex readings: שיטת-א reading applied, the whole of a plain target",
    ),
    "phase5_sites": (
        "codex readings: empty clauses in note bodies",
        "codex readings: apply-candidate in place, its form lacking the paseq glyph that ends the target",
        "codex readings: applied, the form replacing the whole of a plain target",
        "codex readings: applied, the form replacing named atoms of a plain target",
        "codex readings: applied, the form written into the selected parameter of the one kept template that is the target",
        "codex readings: ketiv/qere plane reading in place in a qere parameter",
        "codex readings: ketiv/qere plane reading in place through phase 3's ketiv/qere apparatus",
        "codex readings: pointed ketiv written as the form stands",
        "codex readings: pointed ketiv written with a named adjustment",
        "codex readings: ketiv/qere plane reading pending by name",
        "codex readings: ketiv/qere plane reading at a one-sided template, left for later work",
        "codex readings: pointed ketiv ending in the qere's trailing maqaf",
        "codex readings: pending, the form stopping at the codex's space for a qere without ketiv",
        "codex readings: not applied, and flagged",
        "codex readings: applied readings with a configuration a phase 3 policy removes",
        "codex readings: שיטת-א reading already in place",
        "codex readings: שיטת-א reading not applied",
        "codex readings: שיטת-א reading applied, the whole of a plain target",
    ),
    "phase6_counts": (
        "נוסח: notes reached",
        "מ:הערה-2: notes reached",
        "נוסח: notes given MAM's target",
        "מ:הערה-2: notes given MAM's target",
    ),
    "flag_counts": (
        "qualification 2: doubt-marked clauses by codex siglum",
        "qualification 2: notes flagged",
        "qualification 2: clauses flagged",
        "flagged-not-applied",
        "qualification 2: clauses whose reading is already in the target",
        "named apparatus-silence sites",
        "qualification 3: named agreeing clauses",
        "applied-and-flagged",
        "qualification 2: doubt-marked clauses by quoted form",
        "qualification 3: differing clauses already applied",
        "named doubtful agreeing clause",
        "named codex reading phase 5 does not apply",
    ),
    "flag_sites": (
        "qualification 2: doubt-marked clauses by codex siglum",
        "qualification 2: notes flagged",
        "qualification 2: clauses flagged",
        "flagged-not-applied",
        "qualification 2: clauses whose reading is already in the target",
        "named apparatus-silence sites",
        "qualification 3: named agreeing clauses",
        "applied-and-flagged",
        "qualification 2: doubt-marked clauses by quoted form",
        "qualification 3: differing clauses already applied",
        "named doubtful agreeing clause",
        "named codex reading phase 5 does not apply",
    ),
}
