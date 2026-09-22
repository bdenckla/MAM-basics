r"""Survey: MAM's metegs by position relative to the chanted word's one primary stress.

A meteg normally stands BEFORE the stress.  Both Yeivin and Breuer describe a meteg after it
as a named class -- ITM §§332, 338 and 354, CoS Ch. 8 types (a), (b) and (j) -- and neither
book gives a count.  This module supplies one, over every chanted word of MAM, and records
each occurrence so the page can list them rather than assert a total.  Issue #260's M23 at
Isaiah 23:12 is one such meteg, which is the occasion for the survey and not its subject.

Pure computation and a JSON writer -- no HTML.  ``author_site/post_stress_meteg`` renders it,
and ``main_accgram.py survey-post-stress-meteg`` runs it standalone.

THE STRESS ORACLE IS PHONETIC MAM, whose ``jta`` field marks the one stressed syllable with
``!``.  ``py/tests/test_final_stress_vs_phonetic_mam.py`` reads the same files for the same
reason: which syllable the stress falls on is not derivable from the pointing without a real
stress model, and al-hatorah's ``py/aht_phon`` has one.  A U+05BD's position is NEVER used to
infer the stress -- that would make the survey's question answer itself.

THE CORPUS IS PHONETIC MAM'S TEXT, and it is a SNAPSHOT of MAM rather than MAM's current
state.  Phonetic MAM is regenerated on al-hatorah's schedule, so the standard set
here can be older than the MAM-simple beside it -- and on 2026-09-04 it was, the thirty Holman
meteg suggestions of ``doc/PLAN-holman-meteg-rollout-programme.md`` among the differences.
``currency`` below MEASURES that rather than assuming it away: it counts U+05BD per numbered verse on
both sides and names every verse where the two disagree, so the page can say which MAM its
figures describe.  Refreshing the oracle is al-hatorah's business; re-running this survey
afterwards is one command.

NUCLEI, AND WHERE THIS PARTS FROM ``final_stress``.  A syllable's nucleus is a point written
in the text, so the Hebrew's syllable count can be had without syllabifying it: a full vowel
or a xataf is a nucleus, a sheva is not, and a xolam male or shuruq written on a vav belongs
to the consonant before it.  ``accgram.final_stress`` counts NO nucleus for a furtive patax,
because it asks only whether the stress is final; this module counts one, because Phonetic
MAM does -- מזבח is ``miz.!bE.ax`` there, three syllables -- and a meteg on the guttural of
יָנ֥וּחַֽ is after the stress only under that convention.  ``final_stress``'s public
``ends_in_furtive_patax`` is where the other convention is stated, and the differential test
holds the two steady against each other.

THE TWO SIDES ARE CHECKED AGAINST EACH OTHER, per chanted word: the number of nuclei found in
the Hebrew must equal the number of non-sheva syllables in the ``jta``.  A chanted word where
they disagree is recorded as a MISMATCH and left out of the provisional counts. At the end,
_problems returns the collected problems and build_survey raises if any remain, so no survey
with a mismatch is emitted.

THE SILLUQ BOUNDARY IS TWO CONDITIONS, BOTH OF THEM, AND NO THIRD.  A U+05BD is the silluq
when it is in the stressed syllable of a chanted word that has sof pasuq. Sof pasuq identifies
the last chanted word directly; a parsed entry's position within a numbered verse is not
evidence of silluq.  The untracked census
script this module replaces (``doc/post-stress-meteg-census-2026-09-03.md`` is its report)
treated the last parsed entry of a NUMBERED verse as verse-final whether or not it had sof
pasuq, which is a silluq fallback rather than a test.

A NUMBERED VERSE AND A CHANTED VERSE ARE NOT THE SAME UNIT, and dual-cantillation numbered
verses are where the units can differ. The source contains dual structures in eighteen numbered
verses: Genesis 35:22 and seventeen verses in the two Decalogues. Before classification, the
survey selects one complete cantillation strand for each such verse and then selects one qamats
reading for each qamats-variant row. The selected form of every numbered verse ends with sof
pasuq, measured 2026-09-08. Finality nevertheless comes only from sof pasuq, never from entry
position. ``numbered_verses_whose_last_entry_lacks_sof_pasuq`` records any future violation;
the run fails unless every recorded violation is both explained by dual cantillation and free
of U+05BD.

A METEG AND AN ACCENT ON ONE LETTER HAVE NO DEFINED ORDER (Ben, 2026-09-03), so the run fails
rather than guessing -- except where the accent sharing the letter marks no stress, since then
nothing about the stress turns on which mark came first.  The prepositives, the postpositives,
ole and geresh muqdam are written at a fixed edge of the chanted word rather than on its
stress, which is what ``final_stress.NOT_IMPOSITIVE`` says of the same set; such a meteg is
classified by its syllable like any other and tallied separately as an overlap.

Prose verses and poetic verses are routed by ``poetic_filter.should_keep_line``, so Job's
prose frame goes with the 21 books. For a dual-cantillation passage, this census selects the
cant-alef strand and counts the passage as though it were read once. A second scan over
cant-bet is retained in the JSON for the rendered appendix.

THE STRESS-LETTER ACCENT CHECK retains one result from the 2026-09-03 census table.  The
table read the accents on the initial Hebrew letter of the one ``jta`` syllable marked ``!``;
``stress_accent_classification`` implements that exact rule and establishes only that every
MAS has a conjunctive accent there.  The four ``misc-vayomer`` records have a narrow-sense
paseq after the chanted word, so that stroke leaves the underlying accent conjunctive.  In a
poetic verse, U+05A5 can be yored in an oleh-we-yored whose ole is in the same chanted word or
the preceding chanted word.  The check refuses either future shape rather than silently calling
U+05A5 either merkha or yored.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from functools import cache
from pathlib import Path

from accgram import maqaf_nonfinal_accents as mna
from accgram import poetic_accent_names as pan
from accgram import poetic_filter
from accgram import poetic_scanner
from accgram import prose_scanner
from accgram import uni_to_marks
from accgram import chanted_word_accents as cwa
from accgram.almost_errors_html_shared import accents_and_letters
from accgram.uni_to_marks import is_accent
from mb_cmn import bib_locales as tbn
from mb_cmn import file_io
from mb_cmn import hebrew_accents as ha
from mb_cmn import hebrew_letters as hl
from mb_cmn import hebrew_points as hpo
from mb_cmn import hebrew_punctuation as hpu
from mb_cmn import paths
from mb_cmn import provenance
from wlc_cmn.wlc_book_codes import wlc_bb_codes, wlc_bb_to_bk39id

from accgram.post_stress_meteg_model import (
    CANT_ALEF,
    CANT_BET,
    FIT_TYPE_1_A,
    FIT_TYPE_1_B,
    FIT_TYPE_2_AF,
    FIT_TYPE_2_BF,
    FIT_TYPE_3,
    MAQAF,
    METEG,
    PASOLEG,
    SILLUQ_RULE,
    SOF_PASUQ,
    SUBTYPE_MISC_ALMOST_TYPE_3,
    SUBTYPE_MISC_VAYOMER,
    SYSTEM_POETIC,
    SYSTEM_PROSE,
    SurveyProblem,
    TYPE_1_SUBTYPE_A,
    TYPE_1_SUBTYPE_B,
    TYPE_1_SUBTYPE_C,
    TYPE_2_NEXT_WORD_FILTER_GROUPS,
    TYPE_CLOSED_TSERE,
    TYPE_GUTTURAL,
    TYPE_OPEN,
    TYPE_UNCLASSIFIED,
    type_2_next_filter_group,
)

from accgram.post_stress_meteg_sources import (
    _mam_words_by_bcv,
)

from accgram.post_stress_meteg_classification import (
    stress_accent_classification,
)

from accgram.post_stress_meteg_survey import (
    build_survey,
)


def default_json_out_path() -> Path:
    return paths.out_dir() / "accgram" / "post-stress-meteg.json"


def load_survey(path: Path | None = None) -> dict:
    """The tracked JSON, for a caller rendering the page without the MAM-private clone."""
    json_path = path or default_json_out_path()
    if not json_path.exists():
        raise SurveyProblem(
            f"{json_path} is absent; run `main_accgram.py survey-post-stress-meteg` to"
            " write it, which needs the MAM-private clone"
        )
    return json.loads(json_path.read_text(encoding="utf-8"))


def write_json(survey: dict, path: Path) -> None:
    payload = provenance.with_json_provenance(survey, __file__)
    # Through file_io for the temp-file write and the PermissionError retry; it makes the
    # directory too, and its default newline="" translates nothing, which is what keeps a
    # regeneration from looking like a whole-file diff on Windows.
    file_io.json_dump_to_file_path(payload, str(path), indent=1)


def add_args(parser, *, repo_root: Path) -> None:
    # repo_root is unused: the default comes from ``default_json_out_path``, which composes
    # off ``paths.out_dir()``, so the flag's default and its absence cannot answer
    # differently.  The parameter is kept because the entry point wires every subcommand the
    # same way.
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
