"""The forms that Ben's two survey-backed footnotes quote, and what each claims of them.

Each QuotedForm is one hlp.hboloc call of a module of source_lint.FOOTNOTE_MODULES:
the chanted word quoted at its verse, copied from the module by script, with the
pattern and measurement populations that the footnote's prose gives it, which the
analysis computes. claims.quoted_form_failures checks each against
out/accgram/meteg-before-stress.json: exactly one ordinary record at the verse has
the form, with that pattern, counted in the numerator of each measurement of
``member_of`` and in none of ``not_member_of``. A form with ``enumerates`` is one of
a footnote's hand-written list beside that measurement's generated count, so the
forms that name a measurement there must be exactly its numerator's records.
source_lint.check requires the footnote modules' hboloc calls to be exactly these.
"""

from typing import NamedTuple

from yeivin_itm import claim_schema
from yeivin_itm.content import my_yeivin_amisc_helpers_for_locales as locales

_SEC_320 = "my_yeivin_amisc_sec_320_footnotes.py"
_SEC_322 = "my_yeivin_amisc_sec_322_footnotes.py"
_DSG = "fully-regular.disjunctive-without-target-meteg"
_OTHER_METEG = _DSG + ".other-meteg"
_METIGAH = _DSG + ".metigah"
_MERKHA_AZLA = _DSG + ".merkha-with-azla-legarmeh"
_TARGET_METEG = "fully-regular.target-meteg-rate"
_XAFR1_WITH = "XAFR1.disjunctive-with-target-meteg"
_XAFR1_WITHOUT = "XAFR1.disjunctive-without-target-meteg"


class QuotedForm(NamedTuple):
    module: str
    sloc: str
    form: str
    pattern: str
    member_of: tuple
    not_member_of: tuple = ()
    enumerates: str | None = None


QUOTED_FORMS = (
    QuotedForm(_SEC_320, "@1K 6:22", "אֲֽשֶׁר־לַדְּבִ֖יר", "FR1", (_DSG, _OTHER_METEG)),
    QuotedForm(
        _SEC_320, "@Lev 27:32", "אֲשֶׁר־יַעֲבֹ֖ר", "FR3", (_DSG,), (_OTHER_METEG,)
    ),
    QuotedForm(
        _SEC_320, "@1K 20:22", "אֲשֶׁר־תַּעֲשֶׂ֑ה", "FR3", (_DSG,), (_OTHER_METEG,)
    ),
    QuotedForm(
        _SEC_320, "@Dan 11:16", "בְּאֶֽרֶץ־הַצְּבִ֖י", "FR1", (_DSG, _OTHER_METEG)
    ),
    QuotedForm(_SEC_320, "@1S 30:2", "וַיִּֽנְהֲג֔וּ", "FR2", (_DSG, _OTHER_METEG)),
    QuotedForm(_SEC_320, "@Jer 29:23", "וַיְנַֽאֲפוּ֙", "FR3", (_DSG, _OTHER_METEG)),
    QuotedForm(_SEC_320, "@Lev 25:7", "וְלִ֨בְהֶמְתְּךָ֔", "FR2", (_DSG, _METIGAH)),
    QuotedForm(
        _SEC_320,
        "@Ps 2:2",
        "יִ֥תְיַצְּב֨וּ׀",
        "FR1",
        (_DSG, _MERKHA_AZLA),
        (),
        _MERKHA_AZLA,
    ),
    QuotedForm(
        _SEC_320,
        "@Ps 137:1",
        "עַ֥ל־נַהֲר֨וֹת׀",
        "FR3",
        (_DSG, _MERKHA_AZLA),
        (),
        _MERKHA_AZLA,
    ),
    QuotedForm(_SEC_320, "@Ps 94:4", "יִ֝תְאַמְּר֗וּ", "FR1", (_DSG,)),
    QuotedForm(
        _SEC_320, "@Ps 106:35", "וַֽ֝יִּלְמְד֗וּ", "FR2", (_TARGET_METEG,), (_DSG,)
    ),
    QuotedForm(_SEC_322, "@Ez 3:15", "אֶֽל־נְהַר־כְּבָר֙", "XAFR1", (_XAFR1_WITH,)),
    QuotedForm(_SEC_322, "@Ez 43:3", "אֶל־נְהַר־כְּבָ֑ר", "XAFR1", (_XAFR1_WITHOUT,)),
)


def verse(sloc):
    """The (book, chapter, verse) of a footnote's reference, such as "@Lev 27:32"."""
    if not locales.sloc_okay(sloc):
        raise ValueError(f"Not a footnote reference: {sloc!r}")
    book, place = sloc[1:].split(" ")
    chapter, number = place.split(":")
    return dict(locales.YBKID_AND_STD_BKID_PAIRS)[book], int(chapter), int(number)


def _check_table():
    if not QUOTED_FORMS:
        raise ValueError("No quoted forms")
    for quoted in QUOTED_FORMS:
        verse(quoted.sloc)
        names = (*quoted.member_of, *quoted.not_member_of)
        if quoted.enumerates is not None:
            names += (quoted.enumerates,)
        unknown = [
            name for name in names if name not in claim_schema.APPROVED_FRACTIONS
        ]
        if unknown:
            raise ValueError(f"{quoted.sloc}: measurements without a pin: {unknown}")


_check_table()
