"""The near-Aleppo consumer notice shared by dataset headers and documentation.

The notice describes the dataset's template roles, projections, spacing and mark
order. set_in_header checks the source MAM notice hash before replacing it, so
upstream consumer rules require a deliberate update rather than disappearing.
The documentation renders the same NOTICE object used in every book header.
"""

import copy
import hashlib
import json

from near_aleppo.phase2_templates import APPLIED_AND_FLAGGED
from near_aleppo.phase2_templates import FLAGGED_NOT_APPLIED
from near_aleppo.phase2_templates import MARKS_WITHOUT_LETTER
from near_aleppo.phase2_templates import POINTED_KETIV_PARAMETER
from near_aleppo.phase6_mam_targets import MAM_TARGET_PARAMETER
from near_aleppo.phase6_rename import RENAMED_NOTES
from py_misc import orphan_marks
from py_misc.near_aleppo_params import MAM_NOTE

# Rule 8's planned template for marks at a position of no width, at the join inside
# a maqaf compound, specific to the near-Aleppo dataset. The pending-work section
# and original decision retain its name; the current consumer notice omits it.
# No site uses it yet, so phase 2 has no rule for it.
MARKS_WITHOUT_LETTER_OR_SPACE = "ניקוד בלי אות ובלי רווח"

# The SHA-256 of MAM-parsed-plus's notice, serialized as a book file serializes it,
# derived again on 2026-10-05: all 24 input notices now qualify poetic stress-helper
# alternatives and omit the redundant parser-boundary rule. NOTICE reflects those
# changes and the current documented template and projection roles.
# The selected MAM-parsed/plus tree is 612b667282c197a65e85bef3d624b4d970d7b084.
_MAM_NOTICE_SHA256 = "a372309e14dfc5c623a29ae7f3ef2e7f043a5be9876a357e5601548625bac959"

_NOTE, _NOTE_2 = RENAMED_NOTES["נוסח"], RENAMED_NOTES["מ:הערה-2"]

NOTICE = {
    "summary": (
        "The near-Aleppo dataset is similar to MAM-parsed-plus. The Hebrew of "
        "near-Aleppo is nearer to the Aleppo Codex's body text than the Hebrew "
        "of MAM-parsed-plus. Like MAM-parsed-plus, it is a "
        "structured dataset, not ready-to-display Scripture; interpret each "
        "structure by its documented role and choose a projection wherever the "
        "payload presents alternatives."
    ),
    "critical_rules": [
        (
            "Use a closed, role-aware template dispatch: recurse only through "
            "documented Scripture-bearing fields, and fail on an unknown template "
            "instead of guessing from its parameters or skipping it. Beside MAM's "
            f"templates, near-Aleppo uses three added templates: {_NOTE} and {_NOTE_2}, "
            "which are MAM's נוסח and מ:הערה-2 where near-Aleppo has changed the "
            "note's target. Their parameter 1 is near-Aleppo Scripture, and "
            "parameter 2 already contains the reviewed near-Aleppo clause, or an "
            "empty array when the complete original note remains in MAM context. "
            f"{MAM_NOTE} holds the remaining original MAM clauses, in their "
            "original order, or that complete note. Consumers need no review "
            "ledger or editorial recasting to render these roles. The third "
            "added template is "
            f"{MARKS_WITHOUT_LETTER}, which holds marks without a written letter "
            "at a position of nonzero width. It accepts "
            "GA: one or more artificial alefs, each followed by permitted marks; "
            "or GV: parameter 1 exactly VAV + HOLAM, with "
            f"{orphan_marks.GV_PARAMETER}={orphan_marks.GV_VARIANT}. Neither carrier "
            "permits a dagesh. Carrier letters are not written ketiv consonants. "
            "JSON stores the carrier payload; the example edition supplies "
            "guillemets, retaining an adopted GV as VAV + HOLAM. Converting it to "
            "ALEF + HOLAM loses the chosen holam-male distinction. Surrounding "
            "separators remain explicit; no automatic space is inserted."
        ),
        (
            "Near-Aleppo adds six parameters. Five are not Scripture: "
            f"{MAM_TARGET_PARAMETER}, on the two renamed notes, holds MAM's "
            f"target; {MAM_NOTE} contains the source clauses about that target; "
            f"and {APPLIED_AND_FLAGGED} "
            f"and {FLAGGED_NOT_APPLIED}, on a note or a ketiv/qere template, are "
            f"apparatus; {orphan_marks.GV_PARAMETER}, on the explicitly licensed "
            "orphan-mark variant, is semantic metadata identifying its artificial "
            "carrier. Use it to interpret the payload; do not collect it as "
            "Scripture text. The sixth, "
            f"{POINTED_KETIV_PARAMETER}, on a ketiv/qere "
            "template, holds a pointed ketiv from MAM's notes or the approved "
            "frozen inference from MAM's ketiv and pointed qere, or an individually "
            "adjudicated codex reading, or a sealed reviewed portable decision, and "
            "is Scripture."
        ),
        (
            "Choose one documented branch of each choice-bearing structure; do not "
            "concatenate the branches. Near-Aleppo has evaluated away MAM's "
            "templates for dual cantillation, qamats, and poetic stress-helper "
            "alternatives, so the branches left in near-Aleppo's text are those "
            "of the ketiv/qere templates, "
            f"{POINTED_KETIV_PARAMETER} among them, and of "
            "the special-letter words it keeps. A copy of MAM's target in "
            f"{MAM_TARGET_PARAMETER} keeps all of MAM's alternatives."
        ),
        (
            "A special-letter template's interrupted spelling and uninterrupted "
            "word-form are two representations of one word-form; select one text "
            "representation rather than collecting both."
        ),
        (
            "Reassemble text fragments before identifying words or maqaf compounds; "
            "array, template, and element boundaries are not segmentation "
            "boundaries."
        ),
        (
            "A whitespace template can be the only separator between adjacent "
            "Scripture strings: for example, מ:ששש and ססס can have no literal "
            "whitespace at that boundary. Do not drop the template or collect a "
            "descriptive parameter as Scripture. A plain-text projection that does "
            "not preserve layout must supply a separator; a layout-preserving "
            "renderer must implement the documented space or break."
        ),
        (
            "Outside note bodies, flag values, and the copies of MAM's target, which "
            "quote MAM, near-Aleppo writes U+05C0 HEBREW PUNCTUATION PASEQ for both "
            "narrow-sense paseq and legarmeh, erasing the distinction present in MAM. "
            "Near-Aleppo writes U+05C0 directly after its word and followed by a "
            "space or a whitespace template. U+05C0 forms no compound: only maqaf "
            "joins words into a chanted word. This describes the JSON; the example "
            "HTML edition adds a thin space before U+05C0 for display."
        ),
        (
            "Outside note bodies, flag values, and the copies of MAM's target, which "
            "quote MAM, near-Aleppo has no HEBREW POINT QAMATS QATAN, the codex "
            "having no separate sign for the qamats qatan, so its HEBREW POINT "
            "QAMATS is an ambiguous qamats, not a qamats gadol."
        ),
        (
            "For literal search, byte comparison, or MAM-compatible output, "
            "preserve MAM mark order or transform both sides deliberately; "
            "Unicode-normalized text can look identical while comparing "
            "differently. Near-Aleppo runs no normalization over MAM's strings, and "
            "keeps MAM's mark order and its COMBINING GRAPHEME JOINERs outside "
            "the added inferred-pointing parameters, which preserve their frozen "
            "source-owned output order."
        ),
    ],
    "documentation": "https://bdenckla.github.io/MAM-basics/near-aleppo/reading-json.html#consumer-notice",
}


def set_in_header(header, label):
    """Replace MAM-parsed-plus's notice in ``header`` by NOTICE, in place.

    ``label`` names the book file in the error raised when MAM's notice is not the
    one NOTICE was derived from.
    """
    serialized = json.dumps(header["consumer_notice"], ensure_ascii=False, indent=2)
    digest = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
    if digest != _MAM_NOTICE_SHA256:
        raise AssertionError(
            f"{label}: MAM-parsed-plus's consumer notice is not the one "
            "consumer_notice.py was derived from; re-derive NOTICE from it and "
            "update _MAM_NOTICE_SHA256"
        )
    header["consumer_notice"] = copy.deepcopy(NOTICE)
