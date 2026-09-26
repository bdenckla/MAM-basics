"""For every reading difference of the Aleppo comparison, find HBCE's Leningrad transcription of
the same chanted word, and say which side it agrees with.

Reads ``out/compare_MA.tsv``; writes ``out/candidates_with_ML.tsv``.
"""

from collections import Counter

from hbce_psalms import hbce_paths
from hbce_psalms.candidates import is_candidate, load
from hbce_psalms.compare import load_hbce, skeleton
from mb_cmn import hebrew_punctuation as hpu
from mb_cmn.uni_denorm import give_std_mark_order

SHOWN_PASEQ = " " + hpu.PASOLEG
HEADER = (
    "ref\tMAM\tAleppo(HBCE)\tLeningrad(HBCE)\tML-agrees-with\tlabels\tdocnote\tintro"
    "\tflags"
)


def index_tokens(verses: dict) -> dict:
    """ref -> list of (skeleton, token)."""
    return {
        ref: [(skeleton(t.text), t) for t in toks if t.text]
        for ref, toks in verses.items()
    }


def find_token(indexed: dict, ref: str, mam_text: str, alt_text: str):
    """The token, or list of tokens, of ``ref`` whose letters match either probe."""
    cands = indexed.get(ref, [])
    for probe in (mam_text, alt_text):
        if not probe or probe == "—":
            continue
        sk = skeleton(probe)
        for tsk, t in cands:
            if tsk == sk:
                return t
        # the probe may be a maqaf compound whose atoms are separate tokens on this side
        halves = [skeleton(h) for h in probe.split(hpu.MAQ) if skeleton(h)]
        if len(halves) > 1:
            joined = [t for tsk, t in cands if tsk in halves]
            if len(joined) == len(halves):
                return joined
    return None


def fmt(tok) -> str:
    if tok is None:
        return "(not found)"
    if isinstance(tok, list):
        return " ".join(t.text + (SHOWN_PASEQ if t.paseq else "") for t in tok)
    return tok.text + (SHOWN_PASEQ if tok.paseq else "")


def write_candidates_with_ml() -> None:
    """Write ``out/candidates_with_ML.tsv``."""
    ml = index_tokens(load_hbce("ML", Counter()))
    out = hbce_paths.out_dir()
    rows = [r for r in load(out / "compare_MA.tsv") if is_candidate(r)]
    lines = [HEADER]
    for r in rows:
        mam_form = r["MAM"].replace(SHOWN_PASEQ, "")
        ma_form = r["Aleppo"].replace(SHOWN_PASEQ, "")
        ml_tok = find_token(ml, r["ref"], mam_form, ma_form)
        ml_text = fmt(ml_tok)
        mam_n = give_std_mark_order(mam_form)
        ma_n = give_std_mark_order(ma_form)
        ml_n = give_std_mark_order(ml_text.replace(SHOWN_PASEQ, ""))
        if ml_tok is None:
            agrees = "?"
        elif ml_n == ma_n and ml_n == mam_n:
            agrees = "both"
        elif ml_n == ma_n:
            agrees = "Aleppo(HBCE)"
        elif ml_n == mam_n:
            agrees = "MAM"
        else:
            agrees = "neither"
        fields = [r["ref"], r["MAM"], r["Aleppo"], ml_text, agrees, r["labels"]]
        fields += [r["docnote"], r["intro"], r["orig|flags"]]
        lines.append("\t".join(fields))
    text = "".join(line + "\n" for line in lines)
    (out / "candidates_with_ML.tsv").write_text(text, encoding="utf-8", newline="\n")
