"""Template declarations specific to the MAM-parsed-plus representation."""

from author_misc import mp_cmn_claims_core as _claims_core
from mb_cmn import template_names as tmpln

_claim_def = _claims_core.claim_def

PLUS_SPECIFIC = "Templates produced specifically for MAM-parsed-plus."

CLAIM_DEFS = (
    _claim_def(
        "mp.plus.templates.plus-specific.set",
        PLUS_SPECIFIC,
        kind="enum",
        subject="mp:plus",
        data={"templates": [tmpln.SCRDFF_TAR, tmpln.SLH_WORD]},
    ),
)
