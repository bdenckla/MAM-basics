"""Prepare untanglers from transient public MAM EP sequences, without file I/O."""

from mb_cmn import ws_tmpl2
from mb_cmn.shrink import shrink
from phonetic_mam.core import dualcant_align as align
from phonetic_mam.core import dualcant_arguments as arguments
from phonetic_mam.core import dualcant_flexword as flexword
from phonetic_mam.core import dualcant_templates as templates
from phonetic_mam.core import dualcant_words as words


def prepare(verses):
    """Calculate both strands and both qamats alternatives of every direct dual.

    Non-dual EP elements supply no alignment input. Their declared shapes are
    validated, including nested documentation, so an unknown or nested dual
    template fails rather than silently selecting or traversing a new branch.
    """
    if not isinstance(verses, (list, tuple)):
        raise ValueError("expected an array of EP sequences")
    aligned = []
    for verse in verses:
        templates.validate_sequence(verse, allow_dual=True)
        for element in verse:
            if isinstance(element, str):
                continue
            if ws_tmpl2.template_name(element) != "מ:כפול":
                continue
            params = element["tmpl_params"]
            dcargs = [
                arguments.get_dcargs_for_wtseq(
                    shrink([key, "=", *templates.sequence(params[key])])
                )
                for key in ("כפול", "א", "ב")
            ]
            aligned.extend(align.align_dcargs(dcargs))
    raw, _logs = words.get_untanglers(aligned)
    return _cook(raw)


def _cook(raw_uts):
    cooked_uts = {}
    for raw_ut in raw_uts:
        super = raw_ut["sab-word-cant-superimposed"]
        alef = raw_ut["sab-word-cant-alef"]
        bet = raw_ut["sab-word-cant-bet"]
        if arguments.is_dcargs_qamats(super):
            super_dalet, super_samekh = arguments.dcargs_qamats_das(super)
            alef_dalet, alef_samekh = arguments.dcargs_qamats_das(alef)
            bet_dalet, bet_samekh = arguments.dcargs_qamats_das(bet)
            cooked_uts[super_dalet] = [alef_dalet], [bet_dalet]
            cooked_uts[super_samekh] = [alef_samekh], [bet_samekh]
        else:
            utval_for_alef = _untangler_val(alef)
            utval_for_bet = _untangler_val(bet)
            cooked_uts[super] = utval_for_alef, utval_for_bet
    return cooked_uts


def _untangler_val(value):
    return flexword.dispatch_on_flexword(_singleton, _identity, None, value)


def _singleton(value):
    return [value]


def _identity(value):
    return value
