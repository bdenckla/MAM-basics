"""Read the explicitly supported content inside dual-template arguments."""

from mb_cmn import hebrew_punctuation as hpu
from mb_cmn.my_utils import first_and_only
from phonetic_mam.core import dualcant_templates as templates


def get_dcargs_for_wtseq(wtseq):
    outs = list(map(_get_dcargs_for_wtel, wtseq))
    return sum(outs, [])


def is_dcargs_qamats(obj):
    return isinstance(obj, dict) and list(obj.keys()) == ["dcargs-qamats"]


def dcargs_qamats_dalet(obj):
    return dcargs_qamats_das(obj)[0]


def dcargs_qamats_samekh(obj):
    return dcargs_qamats_das(obj)[1]


def dcargs_qamats_das(obj):
    assert is_dcargs_qamats(obj)
    return first_and_only(list(obj.values()))


def _get_dcargs_for_wtel(wtel):
    if isinstance(wtel, str):
        return [wtel]
    name = templates.validate_template(wtel)
    handler = _HANDLERS[name]
    return handler(wtel.get("tmpl_params", {}))


def _doc(params):
    # Only parameter 1 supplies the dual template's content; 2 is documentation.
    return get_dcargs_for_wtseq(templates.sequence(params["1"]))


def _paseq(_params):
    return [" "]


def _legarmeh(_params):
    return [hpu.PASOLEG]


def _qamats(params):
    values = [first_and_only(templates.sequence(params[key])) for key in ("ד", "ס")]
    if not all(isinstance(value, str) for value in values):
        raise ValueError("expected textual qamats alternatives")
    return [{"dcargs-qamats": values}]


def _ignore(_params):
    return []


_HANDLERS = {
    "נוסח": _doc,
    "מ:קמץ": _qamats,
    "מ:פסק": _paseq,
    "מ:לגרמיה-2": _legarmeh,
    "פפ": _ignore,
    "סס": _ignore,
}
