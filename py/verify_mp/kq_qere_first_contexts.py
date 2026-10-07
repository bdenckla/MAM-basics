"""Verify what each qere-first ketiv/qere template follows in the plus corpus.

MAM shows the qere before the ketiv at every קו״כ and at the מ:כו״ק מיוחד types
whose סוג the claim names. The plus guide says where MAM uses them: after a
maqaf and, at the verses the claim lists, a קו״כ after a narrow-sense paseq
(מ:פסק). This re-derives both statements from the corpus.

The walk is closed. A qere-first template may stand in the E column, or in the
parameter of a נוסח that holds MAM's text, whose first element takes the
נוסח's place in the text; one anywhere else fails. What precedes it must be a
string ending in a maqaf, or a מ:פסק; anything else fails.
"""

from dataclasses import dataclass

from mb_author.claim import ClaimRecord
from mb_cmn import hebrew_punctuation as hpu
from verify_mp.corpus import Context, iter_template_objects, iter_verses

_Q2_TO_G2 = str.maketrans({'"': hpu.GERSHAYIM})
_SUBTYPES_CLAIM_ID = "mp.plus.templates.kq-special.subtypes"
_COLUMN_E = 2


@dataclass(frozen=True)
class _Spec:
    qk_name: str
    special_name: str
    qere_first_sugs: frozenset
    all_sugs: frozenset
    text_wrapper_name: str
    text_wrapper_param: str
    paseq_name: str
    after_paseq: frozenset

    def is_target(self, tmpl) -> bool:
        name = tmpl["tmpl_name"]
        if name == self.qk_name:
            return True
        if name != self.special_name:
            return False
        sug = _sug(tmpl)
        if sug in self.qere_first_sugs:
            return True
        assert sug in self.all_sugs, f"undeclared סוג of {name}: {sug!r}"
        return False


def verify(record: ClaimRecord, ctx: Context) -> None:
    """Verify the contexts the plus guide states for qere-first ketiv/qere."""
    spec = _make_spec(record, ctx)
    found = []
    for book39, ch_key, v_key, verse in iter_verses(ctx.corpus):
        where = (book39["book24_name"], book39["sub_book_name"], ch_key, v_key)
        for col_idx, col in enumerate(verse):
            if col_idx == _COLUMN_E:
                _scan(spec, col, None, False, where, found)
                continue
            for tmpl in iter_template_objects(col):
                assert not spec.is_target(tmpl), (_label(where), col_idx, tmpl)

    bad = []
    after_paseq = set()
    qk_count = 0
    sugs_seen = set()
    for where, tmpl, prev, foreign in found:
        name = tmpl["tmpl_name"]
        if name == spec.qk_name:
            qk_count += 1
        else:
            sugs_seen.add(_sug(tmpl))
        if foreign:
            bad.append(f"{_label(where)}: {name} in a parameter not holding MAM's text")
        elif isinstance(prev, str) and prev.endswith(hpu.MAQ):
            continue
        elif _is_paseq(spec, prev) and name == spec.qk_name:
            after_paseq.add(where)
        else:
            bad.append(f"{_label(where)}: {name} follows {prev!r}")
    assert not bad, f"qere-first ketiv/qere in an undeclared context: {bad[:5]}"
    assert qk_count, f"no {spec.qk_name} in the plus corpus"
    unseen = spec.qere_first_sugs - sugs_seen
    assert not unseen, f"qere-first types not in the plus corpus: {sorted(unseen)}"
    assert after_paseq == spec.after_paseq, (
        f"{spec.qk_name} after a narrow-sense paseq at"
        f" {sorted(map(_label, after_paseq))},"
        f" declared at {sorted(map(_label, spec.after_paseq))}"
    )


def _make_spec(record: ClaimRecord, ctx: Context) -> _Spec:
    assert ctx.claim_records is not None, "verifier context has no claim records"
    data = record.data
    all_sugs = frozenset(
        v.translate(_Q2_TO_G2)
        for v in ctx.claim_records[_SUBTYPES_CLAIM_ID].data["values"]
    )
    qere_first_sugs = frozenset(
        v.translate(_Q2_TO_G2) for v in data["special_qere_first_sug_values"]
    )
    assert qere_first_sugs <= all_sugs, sorted(qere_first_sugs - all_sugs)
    return _Spec(
        qk_name=data["template"],
        special_name=data["special_template"],
        qere_first_sugs=qere_first_sugs,
        all_sugs=all_sugs,
        text_wrapper_name=data["text_wrapper"]["template"],
        text_wrapper_param=data["text_wrapper"]["param"],
        paseq_name=data["paseq_template"],
        after_paseq=frozenset(
            (d["book24_name"], d["sub_book_name"], d["chapter"], d["verse"])
            for d in data["after_narrow_sense_paseq"]
        ),
    )


def _scan(spec, seq, prev_of_start, foreign, where, found):
    """Record each qere-first template in seq with what precedes it in the text.

    prev_of_start is what precedes seq's first element. foreign is true inside
    any parameter other than the one in which a נוסח holds MAM's text.
    """
    for idx, node in enumerate(seq):
        prev = seq[idx - 1] if idx else prev_of_start
        if isinstance(node, str):
            continue
        assert isinstance(node, dict) and "tmpl_name" in node, (_label(where), node)
        if spec.is_target(node):
            found.append((where, node, prev, foreign))
        for key, val in node.get("tmpl_params", {}).items():
            holds_text = (
                node["tmpl_name"] == spec.text_wrapper_name
                and key == spec.text_wrapper_param
            )
            _scan(
                spec, _as_seq(where, val), prev, foreign or not holds_text, where, found
            )


def _as_seq(where, val):
    if isinstance(val, list):
        return val
    assert isinstance(val, (str, dict)), (_label(where), val)
    return [val]


def _is_paseq(spec, node) -> bool:
    return isinstance(node, dict) and node.get("tmpl_name") == spec.paseq_name


def _sug(tmpl) -> str:
    raw = tmpl["tmpl_params"]["סוג"]
    if isinstance(raw, list) and len(raw) == 1:
        raw = raw[0]
    assert isinstance(raw, str), tmpl
    return raw.translate(_Q2_TO_G2)


def _label(where) -> str:
    book24_name, sub_book_name, ch_key, v_key = where
    return f"{sub_book_name or book24_name} {ch_key}:{v_key}"
