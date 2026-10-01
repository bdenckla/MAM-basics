"""Closed, transient NDJSON interface to the source-independent phonetic core.

This is a computation protocol, not a release-data format. Requests and replies
may contain intermediate values; no operation reads data files or writes files.
Callers own their input adapters and any separately authorized output projection.
"""

import json
import sys

# A compute invocation is write-neutral, including Python's import cache.
sys.dont_write_bytecode = True

from mb_cmn import bib_locales
from phonetic_mam.core import bccvecs_that_are_known as knowns
from phonetic_mam.core import deep_latin
from phonetic_mam.core import dtx_struct
from phonetic_mam.core import dualcant_prepare
from phonetic_mam.core import ipa
from phonetic_mam.core import jtech_ascii
from phonetic_mam.core import sas_from_phrase
from phonetic_mam.core import separate_accents
from phonetic_mam.core import stress_2_cmn
from phonetic_mam.core import udl_from_he

SCHEMA = "phonetic-mam-compute-v1"
MAX_REQUEST_CHARS = 16 * 1024 * 1024
_CANTSYS = ("cant-sys-prose", "cant-sys-poetic")


class ProtocolError(ValueError):
    """A request does not belong to the closed computation protocol."""


def _object(value, required, optional=()):
    if not isinstance(value, dict):
        raise ProtocolError("expected an object")
    if set(value) - set(required) - set(optional) or set(required) - set(value):
        raise ProtocolError("unknown or missing object field")
    return value


def _string(value):
    if not isinstance(value, str):
        raise ProtocolError("expected a string")
    return value


def _strings(value):
    if not isinstance(value, list) or not all(isinstance(x, str) for x in value):
        raise ProtocolError("expected an array of strings")
    return value


def _bcvt(value):
    if (
        not isinstance(value, list)
        or len(value) != 5
        or value[0] != "_bcvt"
        or value[1] not in bib_locales.ALL_BK39_IDS
        or any(type(x) is not int or x < 1 for x in value[2:4])
        or value[4] != "vtmam"
    ):
        raise ProtocolError("expected a MAM verse identity")
    return tuple(value)


def _untanglers(value):
    if not isinstance(value, dict):
        raise ProtocolError("expected an untangler object")
    for key, pair in value.items():
        _string(key)
        if not isinstance(pair, list) or len(pair) != 2:
            raise ProtocolError("expected two untangled strands")
        for strand in pair:
            if not _strings(strand):
                raise ProtocolError("an untangled strand cannot be empty")
    return value


def _lookup_keys(value):
    if not isinstance(value, dict):
        raise ProtocolError("expected a lookup-key object")
    for key, target in value.items():
        _string(key)
        _string(target)
    return value


def _transcription(sas):
    return {
        "sephardic": jtech_ascii.get_jtech_ascii("jta-dialect-sefarad", sas),
        "ashkenazic": jtech_ascii.get_jtech_ascii("jta-dialect-ashkenaz", sas),
    }


def _transcription_of_sod(sod):
    if sod is None:
        return None
    if sas_from_phrase.is_sas(sod):
        return _transcription(sod)
    return {
        "alef": [_transcription(sas) for sas in sod["sasdc-ot-alef"]],
        "bet": [_transcription(sas) for sas in sod["sasdc-ot-bet"]],
    }


def _phrase(args):
    _object(
        args,
        ("phrase", "bcvt", "untanglers"),
        ("lookup-keys", "qamats", "include-in-edition-census"),
    )
    phrase = _string(args["phrase"])
    bcvt = _bcvt(args["bcvt"])
    untanglers = _untanglers(args["untanglers"])
    lookup_keys = _lookup_keys(args.get("lookup-keys", {}))
    if any(target not in untanglers for target in lookup_keys.values()):
        raise ProtocolError("lookup target has no untangler")
    qamats = args.get("qamats")
    if qamats not in (None, "qamats-dal", "qamats-sam"):
        raise ProtocolError("unknown qamats alternative")
    include = args.get("include-in-edition-census", True)
    if type(include) is not bool:
        raise ProtocolError("expected a census boolean")
    dtx = dtx_struct.make_context(untanglers, lookup_keys=lookup_keys)
    dtx = dtx_struct.mk_dtx_with_bcvt(dtx, bcvt)
    dtx = dtx_struct.mk_dtx_with_qamats(dtx, qamats)
    if not include:
        dtx = dtx_struct.suppress_edition_census(dtx)
    sods = sas_from_phrase.list_of_sods_from_phrase(dtx, phrase)
    census = []
    for cantsys, counts in dtx["dtx-out-cs-hccvec-seen-counts"].items():
        examples = dtx["dtx-out-cs-hccvec-seen-examples"][cantsys]
        for bccvec, count in counts.items():
            census.append(
                {
                    "cantsys": cantsys,
                    "bccvec": list(bccvec),
                    "count": count,
                    "examples": examples[bccvec],
                }
            )
    return {
        "sods": sods,
        "transcriptions": [_transcription_of_sod(sod) for sod in sods],
        "census": census,
        "untangler-use-counts": dtx["dtx-out-dualcant-untanglers-use-counts"],
    }


def _prepare_untanglers(args):
    _object(args, ("verses",))
    return dualcant_prepare.prepare(args["verses"])


def _word(args):
    _object(args, ("word", "format"))
    word = _string(args["word"])
    if args["format"] == "generic":
        return udl_from_he.get_eudlcw_from_cw_ndns(word)
    if args["format"] == "annotated":
        return udl_from_he.get_eudlcw_from_cw_ydys(word)
    raise ProtocolError("unknown word format")


def _ipa(args):
    _object(args, ("values",))
    return [ipa.get_ipa(value) for value in _strings(args["values"])]


def _accents(args):
    _object(args, ("cantsys", "values"))
    if args["cantsys"] not in _CANTSYS:
        raise ProtocolError("unknown accent system")
    cantsys = args["cantsys"]
    result = []
    for value in _strings(args["values"]):
        letters, vector = separate_accents.get_sepacc(cantsys, value)
        index = knowns.CS_GET_STRESS_INFO_FROM_BCCVEC[cantsys].get(vector)
        result.append({"letters": letters, "bccvec": vector, "stress-index": index})
    return result


def _accent_names(args):
    _object(args, ("values",))
    return [stress_2_cmn.get_hcc_from_bcc(x) for x in _strings(args["values"])]


def _accent_vectors(args):
    _object(args, ("cantsys",))
    if args["cantsys"] not in _CANTSYS:
        raise ProtocolError("unknown accent system")
    return [
        {
            "bccvec": vector,
            "stress-index": index,
            "name": stress_2_cmn.get_hccvec_from_bccvec(vector),
        }
        for vector, index in knowns.CS_GET_STRESS_INFO_FROM_BCCVEC[
            args["cantsys"]
        ].items()
    ]


def _symbols(args):
    _object(args, ())
    return {
        name: value
        for name, value in vars(deep_latin).items()
        if name.isupper() and not name.startswith("_") and isinstance(value, str)
    }


def _transcriptions(args):
    _object(args, ("values",))
    if not isinstance(args["values"], list):
        raise ProtocolError("expected an array of syllable structures")
    result = []
    for value in args["values"]:
        _object(value, ("syllables", "stress"))
        atoms = value["syllables"]
        if not isinstance(atoms, list) or not atoms:
            raise ProtocolError("expected nonempty atoms")
        for atom in atoms:
            if not isinstance(atom, list) or not atom:
                raise ProtocolError("expected nonempty syllables")
            for syl in atom:
                _object(
                    syl,
                    ("sylrec-udl",),
                    ("sylrec-next-syl-swp1g", "sylrec-this-syl-swp2g"),
                )
                _string(syl["sylrec-udl"])
                if "sylrec-next-syl-swp1g" in syl:
                    _string(syl["sylrec-next-syl-swp1g"])
                if (
                    "sylrec-this-syl-swp2g" in syl
                    and type(syl["sylrec-this-syl-swp2g"]) is not bool
                ):
                    raise ProtocolError("expected a syllable boolean")
        stress = value["stress"]
        if stress is not None:
            if (
                not isinstance(stress, list)
                or len(stress) != 2
                or any(type(i) is not int or i < 0 for i in stress)
            ):
                raise ProtocolError("expected a stress-index pair")
            if stress[0] >= len(atoms) or stress[1] >= len(atoms[stress[0]]):
                raise ProtocolError("stress index outside syllable structure")
        result.append(
            _transcription({"sas-syls-per-atom": atoms, "sas-isps-two-d": stress})
        )
    return result


_OPERATIONS = {
    "phrase": _phrase,
    "prepare-untanglers": _prepare_untanglers,
    "word": _word,
    "ipa": _ipa,
    "accents": _accents,
    "accent-names": _accent_names,
    "accent-vectors": _accent_vectors,
    "symbols": _symbols,
    "transcriptions": _transcriptions,
}


def execute(request):
    """Validate one request and calculate one result without filesystem access."""
    _object(request, ("schema", "operation", "arguments"))
    if request["schema"] != SCHEMA:
        raise ProtocolError("unknown computation schema")
    operation = _string(request["operation"])
    if operation not in _OPERATIONS:
        raise ProtocolError("unknown computation operation")
    return _OPERATIONS[operation](request["arguments"])


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ProtocolError("duplicate JSON field")
        result[key] = value
    return result


def _reject_constant(_value):
    raise ProtocolError("non-finite JSON number")


def serve(stdin=None, stdout=None):
    """Serve one response per NDJSON line until EOF; retain no request state."""
    stdin = sys.stdin if stdin is None else stdin
    stdout = sys.stdout if stdout is None else stdout
    while line := stdin.readline(MAX_REQUEST_CHARS + 1):
        if len(line) > MAX_REQUEST_CHARS:
            raise ProtocolError("request exceeds the computation limit")
        try:
            request = json.loads(
                line, object_pairs_hook=_unique_object, parse_constant=_reject_constant
            )
            result = execute(request)
            response = {"schema": SCHEMA, "result": result}
            encoded = json.dumps(response, ensure_ascii=False, allow_nan=False)
        except Exception as exc:  # The pipe boundary must not echo a source value.
            encoded = json.dumps(
                {
                    "schema": SCHEMA,
                    "error": {
                        "type": type(exc).__name__,
                        "message": "computation rejected",
                    },
                }
            )
        stdout.write(encoded + "\n")
        stdout.flush()
    return 0
