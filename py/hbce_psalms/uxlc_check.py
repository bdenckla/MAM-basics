"""For each reading difference, give the UXLC's form of the same chanted word, and say whether
HBCE's Aleppo form equals it.

Where HBCE's Aleppo transcription equals the UXLC exactly where MAM differs, the transcribers'
Leningrad-like base text may explain the agreement; where it differs from the UXLC too, the
form is a deliberate one.

Reads ``out/candidates_with_ML.tsv`` and the UXLC's Psalms; writes
``out/candidates_with_ML_UXLC.tsv``.
"""

import xml.etree.ElementTree as ET
from collections import Counter

from hbce_psalms import hbce_paths
from hbce_psalms.candidates import load
from hbce_psalms.compare import skeleton
from mb_cmn import hebrew_points as hpo
from mb_cmn import hebrew_punctuation as hpu
from mb_cmn import str_defs as sd
from mb_cmn.uni_denorm import give_std_mark_order

SHOWN_PASEQ = " " + hpu.PASOLEG
HEADER = (
    "ref\tMAM\tAleppo(HBCE)\tLeningrad(HBCE)\tUXLC\tHBCE-Aleppo-vs-UXLC\tlabels"
    "\tdocnote\tintro"
)
# Children of a UXLC <v>: the written atoms, and what has no atom of the qere.
_UXLC_ATOMS = {"w", "q"}
_UXLC_SKIPPED = {"k", "pe", "samekh", "reversednun", "x"}


def uxlc_verses() -> dict:
    """Each verse of the UXLC's Psalms, as a list of its atoms' texts."""
    root = ET.parse(hbce_paths.uxlc_psalms_xml()).getroot()
    verses = {}
    for c in root.iter("c"):
        cn = c.get("n")
        for v in c.iter("v"):
            vn = v.get("n")
            toks = []
            for child in v:
                if child.tag in _UXLC_ATOMS:
                    toks.append("".join(t for t in child.itertext() if not t.isascii()))
                elif child.tag not in _UXLC_SKIPPED:
                    raise ValueError(
                        f"unrecognized UXLC element in a verse: {child.tag}"
                    )
            verses[f"Ps.{cn}.{vn}"] = [t.replace(hpu.SOPA, "") for t in toks if t]
    return verses


def find(verse_toks, probe: str):
    """The UXLC atom, or space-joined atoms, whose letters match ``probe``'s."""
    sk = skeleton(probe)
    if not sk:
        return None
    for t in verse_toks:
        if skeleton(t) == sk:
            return t
    halves = [skeleton(h) for h in probe.split(hpu.MAQ) if skeleton(h)]
    if len(halves) > 1:
        found = [t for t in verse_toks if skeleton(t) in halves]
        if len(found) == len(halves):
            return " ".join(found)
    return None


def _uxlc_comparable(u: str) -> str:
    u = u.replace(hpo.XOLAM_XFV, hpo.XOLAM).replace(sd.CGJ, "").replace(sd.ZWJ, "")
    return give_std_mark_order(u.replace(hpu.MAQ + " ", hpu.MAQ))


def write_candidates_with_ml_uxlc() -> Counter:
    """Write ``out/candidates_with_ML_UXLC.tsv``; return the verdicts on the rows with
    no doc-note on the chanted word."""
    ux = uxlc_verses()
    rows = load(hbce_paths.out_dir() / "candidates_with_ML.tsv")
    verdicts = Counter()
    lines = [HEADER]
    for r in rows:
        vt = ux.get(r["ref"], [])
        probe_m = r["MAM"].replace(SHOWN_PASEQ, "")
        probe_a = r["Aleppo(HBCE)"].replace(SHOWN_PASEQ, "")
        u = find(vt, probe_m) or find(vt, probe_a) or "(not found)"
        a_n = give_std_mark_order(probe_a)
        u_n = _uxlc_comparable(u)
        m_n = give_std_mark_order(probe_m)
        if u == "(not found)" or probe_a == "—":
            verdict = "?"
        elif a_n == u_n:
            verdict = "HBCE-Aleppo == UXLC"
        elif m_n == u_n:
            verdict = "MAM == UXLC"
        else:
            verdict = "all three differ"
        if r["docnote"] in ("none", "verse-note"):
            verdicts[verdict] += 1
        fields = [r["ref"], r["MAM"], r["Aleppo(HBCE)"], r["Leningrad(HBCE)"], u]
        fields += [verdict, r["labels"], r["docnote"], r["intro"]]
        lines.append("\t".join(fields))
    text = "".join(line + "\n" for line in lines)
    path = hbce_paths.out_dir() / "candidates_with_ML_UXLC.tsv"
    path.write_text(text, encoding="utf-8", newline="\n")
    return verdicts
