"""Compare HBCE's transcriptions of the Aleppo Codex (MA) and the Leningrad Codex (ML) with
MAM, chanted word by chanted word.

MAM's text is ``MAM-simple/xml-vtrad-mam/Ps.xml``. Both sides are compared in MAM-normal mark
order through ``give_std_mark_order``, never through Unicode normalization. Each differing
chanted word is classified mark by mark against MAM's documented design policies (chapters 2
and 5 of MAM's introduction) and checked against MAM's doc-notes for its verse.

THE UNIT IS THE CHANTED WORD AS EACH SOURCE HAS IT: a lone atom, or atoms joined by a maqaf of
the text. MAM's gray maqaf is a reading aid rather than a maqaf of the text, so it does not
join atoms here.

U+05BD IS LABELLED BY ITS FUNCTION WHERE THE DATA SETTLES IT. In the final atom of a verse,
MAM's last U+05BD is the silluq, and a difference there is labelled ``silluq``. That holds for
every verse compared here, since both transcriptions stop at Psalm 51: MAM-basics'
``in/meteg_after_silluq_cases.json`` puts Psalms' meteg-after-silluq cases at 60:10, 70:2 and
72:15. An HBCE U+05BD elsewhere in that atom is labelled ``meteg-or-silluq`` when HBCE lacks
the mark on MAM's silluq syllable, because it may then be HBCE's silluq on another syllable.
Every other U+05BD difference is labelled ``meteg``. A U+05BD on one side against an accent
on the other, on the same letter, is also labelled ``stroke-shape``: one stroke under the
letter, read as a meteg or silluq on one side and as a merkha, tipexa or munax on the other.

THE REVIA-MUGRASH POLICY IS APPLIED AS MAM STATES IT. The introduction's chapter 2 says that
MAM has the revia of revia mugrash even in a chanted word stressed at its start, where the
Aleppo Codex usually lacks it, and chapter 5 lists the 260 verses of Psalms, Proverbs and Job
where MAM has both marks on one letter. So a missing revia is set aside only when MAM has it
on the geresh muqdam's letter; elsewhere it is a finding.

THE HATAF POLICY COVERS THE HATAFS MAM DOCUMENTS. Where MAM has a sheva and the Aleppo Codex
a hataf on a non-guttural letter (chapter 2, "חטפים באותיות לא גרוניות"), MAM normally has a
doc-note on the chanted word giving the codex's form, so a hataf row with no such note is
labelled ``hataf-without-mam-note`` and stays a finding.

Both readers dispatch closed: an element they do not recognize raises.

Writes ``out/compare_MA.tsv``, ``out/compare_ML_range.tsv`` (Psalms 15:1-25:1, where MAM
follows the Leningrad Codex), ``out/compare_ML.tsv`` and ``out/compare_summary.txt``.
"""

import difflib
import re
import unicodedata
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict

from hbce_psalms import hbce_paths
from mb_cmn import hebrew_accents as hac
from mb_cmn import hebrew_letters as hle
from mb_cmn import hebrew_points as hpo
from mb_cmn import hebrew_punctuation as hpu
from mb_cmn import hebrew_verse_numerals as hvn
from mb_cmn import str_defs as sd
from mb_cmn.uni_denorm import give_std_mark_order

TEI_NS = "{http://www.tei-c.org/ns/1.0}"

ZWNJ = "\N{ZERO WIDTH NON-JOINER}"
HATAFS = {hpo.XSEGOL, hpo.XPATAX, hpo.XQAMATS}
# A point, an accent, a CGJ or a varika: what may follow a letter in a cluster.
MARK_RE = f"[{hpo.RECC_APCV}]"
CLUSTER_RE = re.compile(f"([א-ת])({MARK_RE}*)")

# The rows labelled with a MAM design policy, or set aside as order only, as ketiv/qere
# handling, or as an unpointed first-hand reading with a pointed alternative. A row with
# any other label is a reading difference: a candidate finding.
NOISE_PREFIXES = ("policy", "order-only", "ketiv-qere", "unpointed-orig-with-alt")


def mark_kind(ch: str) -> str:
    """The kind of mark a code point is, as the labels name it."""
    o = ord(ch)
    if ch == hpo.MTGOSLQ:
        return "meteg"
    if 0x0591 <= o <= 0x05AE:  # ETNAHTA through ZINOR
        return "accent"
    if ch == hpo.DAGOMOSD:
        return "dagesh"
    if ch == hpo.RAFE:
        return "rafe"
    if ch in (hpo.SHIND, hpo.SIND):
        return "shin-sin-dot"
    if 0x05B0 <= o <= 0x05BB or ch == hpo.QAMATS_Q:  # SHEVA through QUBUTS
        return "vowel"
    return "other"


def uname(ch: str) -> str:
    """A code point's Unicode name, less its HEBREW prefix."""
    try:
        return unicodedata.name(ch).replace("HEBREW ", "")
    except ValueError:
        return f"U+{ord(ch):04X}"


def skeleton(s: str) -> str:
    """The letters of ``s``, and nothing else."""
    return hle.letters(s)


class Tok:
    """One chanted word of one side, with what the comparison needs to know about it."""

    __slots__ = (
        "text",
        "paseq",
        "unclear",
        "supplied",
        "orig",
        "gray_maqaf_after",
        "kq",
        "flags",
    )

    def __init__(self, text):
        self.text = text
        self.paseq = False
        self.unclear = False
        self.supplied = False
        self.orig = None  # inside an <app>: the first hand's reading (joined text)
        self.gray_maqaf_after = False
        self.kq = None
        self.flags = set()

    def __repr__(self):
        return f"Tok({self.text!r}{' ' + hpu.PASOLEG if self.paseq else ''})"


# ----------------------------------------------------------------------------- HBCE TEI side

# Elements that have layout or commentary and no text of the verse.
_HBCE_LAYOUT = {"space", "caesura", "lb", "cb", "pb", "note", "fw", "num"}
# Elements whose children are read as if they stood in the element's place.
_HBCE_WRAPPERS = {"unclear", "supplied", "hi", "ex", "abbr", "expan"}
# Elements a <w> may contain.
_HBCE_IN_W = {"unclear", "supplied"}
# Every <pc> in the snapshot is a sof pasuq, written three ways: as itself; once on the
# Aleppo pages as sof pasuq followed by "caes", evidently <pc>׃</pc><caesura/> mistyped; and
# 23 times on the Leningrad pages as an ASCII colon.
_PC_SOF_PASUQ_FORMS = (hpu.SOPA, hpu.SOPA + "caes", ":")


def hbce_w_text(w) -> tuple[str, bool, bool]:
    """A <w>'s text, and whether any of it is unclear or supplied."""
    for d in w.iter():
        if d is not w and d.tag.replace(TEI_NS, "") not in _HBCE_IN_W:
            raise ValueError(f"unrecognized element inside <w>: {d.tag}")
    unclear = w.find(f".//{TEI_NS}unclear") is not None
    supplied = w.find(f".//{TEI_NS}supplied") is not None
    return "".join(w.itertext()), unclear, supplied


def hbce_tokens(el, out: list, tagcount: Counter) -> None:
    """Append tokens for element ``el`` (an <ab> or a descendant) to ``out``."""
    for child in el:
        tag = child.tag.replace(TEI_NS, "")
        tagcount[tag] += 1
        if tag == "w":
            text, unclear, supplied = hbce_w_text(child)
            t = Tok(text)
            t.unclear, t.supplied = unclear, supplied
            out.append(t)
        elif tag == "app":
            rdgs = {}
            for rdg in child:
                rtag = rdg.tag.replace(TEI_NS, "")
                if rtag != "rdg":
                    raise ValueError(f"unrecognized element inside <app>: {rtag}")
                rtype = rdg.get("type", "?")
                if rtype not in ("orig", "corr", "alt"):
                    raise ValueError(f"unrecognized <rdg> type: {rtype}")
                toks = []
                hbce_tokens(rdg, toks, tagcount)
                rdgs.setdefault(rtype, []).append((rdg.get("hand"), toks))
            orig = rdgs.get("orig", [(None, [])])[0][1]
            corr_list = rdgs.get("corr")
            alt_list = rdgs.get("alt", [])
            chosen = corr_list[-1][1] if corr_list else orig
            alt_text = " / ".join(
                " ".join(x.text for x in toks) for _, toks in alt_list
            )
            for t in chosen:
                t.orig = " ".join(x.text for x in orig) if corr_list else None
                t.flags.add("app")
                if alt_text:
                    t.flags.add("alt=" + alt_text)
            if not chosen:  # a corrector deleted the word: keep a marker token
                marker = Tok("")
                marker.flags.add("app-deleted")
                marker.orig = " ".join(x.text for x in orig)
                out.append(marker)
            out.extend(chosen)
        elif tag == "seg":
            hbce_tokens(child, out, tagcount)
        elif tag == "pc":
            txt = "".join(child.itertext()).strip()
            if hpu.PASOLEG in txt and out:
                out[-1].paseq = True
            elif txt in _PC_SOF_PASUQ_FORMS:
                if out:
                    out[-1].flags.add("sof-pasuq-pc")
            else:
                raise ValueError(f"unrecognized <pc> text: {txt!r}")
        elif tag == "gap":
            if out:
                out[-1].flags.add("gap-after")
            else:
                marker = Tok("")
                marker.flags.add("gap")
                out.append(marker)
        elif tag in _HBCE_LAYOUT:
            pass
        elif tag in _HBCE_WRAPPERS or tag in ("div", "ab"):
            hbce_tokens(child, out, tagcount)
        else:
            raise ValueError(f"unrecognized TEI element: {tag}")


def hbce_finalize(tokens: list) -> list:
    """Join maqaf halves, detach paseq, strip sof pasuq and invisible characters."""
    out = []
    for t in tokens:
        text = t.text.replace(hpu.SOPA, "").replace(sd.ZWJ, "").replace(ZWNJ, "")
        text = text.replace(sd.CGJ, "")
        if hpo.XOLAM_XFV in text:
            t.flags.add("holam-haser-vav")
            text = text.replace(hpo.XOLAM_XFV, hpo.XOLAM)
        if text.endswith(hpu.PASOLEG):
            text = text[:-1]
            t.paseq = True
        if hpu.PASOLEG in text:
            t.flags.add("paseq-inside")
            text = text.replace(hpu.PASOLEG, "")
        t.text = text
        if out and out[-1].text.endswith(hpu.MAQ) and not out[-1].paseq:
            prev = out[-1]
            prev.text = prev.text + t.text
            prev.unclear |= t.unclear
            prev.supplied |= t.supplied
            prev.paseq = t.paseq
            prev.flags |= t.flags
            if t.orig is not None:
                prev.orig = (prev.orig or prev.text[: -len(t.text)]) + t.orig
            continue
        out.append(t)
    return [t for t in out if t.text or t.flags]


def load_hbce(siglum: str, tagcount: Counter) -> dict:
    """Each verse of one transcription, as a list of its chanted words."""
    verses = defaultdict(list)
    paths = sorted(
        hbce_paths.transcriptions_dir().glob(f"{siglum}_*.xml"),
        key=lambda p: int(p.stem.split("_")[1]),
    )
    for path in paths:
        root = ET.parse(path).getroot()
        for ab in root.iter(f"{TEI_NS}ab"):
            raw = ab.get("n")  # either "Ps.3.5" or "B25K3V5"
            m = re.fullmatch(r"Ps\.(\d+)\.(\d+)|B25K(\d+)V(\d+)", raw or "")
            if not m:
                raise ValueError(f"unrecognized <ab n>: {raw!r} in {path.name}")
            c, v = (m.group(1), m.group(2)) if m.group(1) else (m.group(3), m.group(4))
            ref = f"Ps.{c}.{v}"
            toks = []
            hbce_tokens(ab, toks, tagcount)
            verses[ref].extend(toks)
    return {ref: hbce_finalize(toks) for ref, toks in verses.items()}


# ----------------------------------------------------------------------------- MAM-simple side

_MAM_SPI = {"spi-pe2", "spi-pe3", "spi-samekh2", "spi-samekh3", "spi-invnun"}


def mam_split_text(text: str, out: list, flags=None) -> None:
    """Append one token per space-separated piece of ``text``."""
    for piece in text.split():
        t = Tok(piece)
        if flags:
            t.flags |= flags
        out.append(t)


def mam_slh_word(el) -> str:
    """The text of a MAM-simple <slh-word>: a word with a small, large or hung letter."""
    parts = []
    for child in el:
        if child.tag in ("letter-small", "letter-large", "letter-hung", "text"):
            parts.append(child.get("text", ""))
        else:
            raise ValueError(f"unrecognized element inside <slh-word>: {child.tag}")
    return "".join(parts)


def mam_ketiv(k) -> str:
    """The ketiv of a MAM-simple <kq-k>."""
    if k.get("text") is not None:
        return k.get("text")
    slh = k.find("slh-word")
    if slh is None:
        raise ValueError("a <kq-k> with neither text nor <slh-word>")
    return mam_slh_word(slh)


def mam_children_tokens(el, out: list, tagcount: Counter, flags=None) -> None:
    """Tokens for the children of a MAM-simple <verse> (or of a <kq-q>)."""
    for child in el:
        tag = child.tag
        tagcount[tag] += 1
        if tag == "text":
            mam_split_text(child.get("text", ""), out, flags)
        elif tag == "lp-legarmeih":
            if out:
                out[-1].paseq = True
                out[-1].flags.add("legarmeh")
        elif tag == "lp-paseq":
            if out:
                out[-1].paseq = True
                out[-1].flags.add("narpas")
        elif tag == "implicit-maqaf":
            if out:
                out[-1].gray_maqaf_after = True
        elif tag == "kq":
            k = child.find("kq-k")
            q = child.find("kq-q")
            if k is None or q is None:
                raise ValueError("a <kq> without both <kq-k> and <kq-q>")
            ketiv = mam_ketiv(k)
            start = len(out)
            if q.get("text") is not None:
                mam_split_text(q.get("text"), out, {"kq"})
            else:
                mam_children_tokens(q, out, tagcount, {"kq"})
            for t in out[start:]:
                t.kq = ketiv
        elif tag == "kq-trivial":
            if child.get("text") is not None:
                mam_split_text(child.get("text"), out, {"kq-trivial"})
            else:
                mam_children_tokens(child, out, tagcount, {"kq-trivial"})
        elif tag == "kq-k-velo-q":
            mam_split_text(child.get("text", ""), out, {"kq-k-velo-q"})
        elif tag == "kq-q-velo-k":
            mam_split_text(child.get("text", ""), out, {"kq-q-velo-k"})
        elif tag == "kq-k-velo-q-maq":
            if out:
                out[-1].text += hpu.MAQ
        elif tag == "slh-word":
            t = Tok(mam_slh_word(child))
            t.flags.add("slh-word")
            out.append(t)
        elif tag in _MAM_SPI:
            pass
        else:
            raise ValueError(f"unrecognized MAM-simple element: {tag}")


def mam_finalize(tokens: list) -> list:
    """Join tokens ending with a maqaf onto the next; strip sof pasuq and invisibles."""
    out = []
    for t in tokens:
        text = t.text.replace(hpu.SOPA, "").replace(sd.ZWJ, "").replace(ZWNJ, "")
        text = text.replace(sd.CGJ, "")
        text = text.replace(
            hpo.VARIKA, ""
        )  # MAM-simple has none; MAM-parsed/plus/ does
        if hpo.QAMATS_Q in text:
            t.flags.add("qamats-qatan")
            text = text.replace(hpo.QAMATS_Q, hpo.QAMATS)
        if hpo.XOLAM_XFV in text:
            t.flags.add("holam-haser-vav")
            text = text.replace(hpo.XOLAM_XFV, hpo.XOLAM)
        t.text = text
        if out and out[-1].text.endswith(hpu.MAQ):
            prev = out[-1]
            prev.text += t.text
            prev.paseq = t.paseq
            prev.flags |= t.flags
            prev.gray_maqaf_after = t.gray_maqaf_after
            continue
        out.append(t)
    return [t for t in out if t.text]


def load_mam(tagcount: Counter) -> dict:
    """Each verse of MAM's Psalms, as a list of its chanted words."""
    root = ET.parse(hbce_paths.mam_simple_psalms_xml()).getroot()
    verses = {}
    for verse in root.iter("verse"):
        ref = verse.get("osisID")
        toks = []
        if verse.get("text") is not None:
            mam_split_text(verse.get("text"), toks)
        mam_children_tokens(verse, toks, tagcount)
        verses[ref] = mam_finalize(toks)
    return verses


# ----------------------------------------------------------------------------- doc-notes, intro


def load_docnotes() -> dict:
    """Each verse's doc-notes, as (target, note) pairs, from the doc-note census."""
    notes = defaultdict(list)
    tsv = hbce_paths.out_dir() / "mam_psalms_docnotes.tsv"
    with tsv.open(encoding="utf-8") as f:
        next(f)
        for line in f:
            path, _tmpl, target, note, _other = line.rstrip("\n").split("\t")
            chapter, verse = path.split(".")
            notes[f"Ps.{chapter}.{verse}"].append((target, note))
    return notes


def load_intro_refs() -> dict:
    """Map (chapter, verse) -> set of introduction pages naming that Psalms verse."""
    refs = defaultdict(set)
    pat = re.compile(r"\[\[תהלים ([א-ת]+)/טעמים#([א-ת]+)[ ,]([א-ת]+)")
    for name in ("ch2", "ch5", "ch4", "appendices"):
        path = hbce_paths.mam_ws_intro_dir() / f"{name}.mediawiki"
        for m in pat.finditer(path.read_text(encoding="utf-8")):
            c = hvn.STR_TO_INT_DIC[m.group(2)]
            v = hvn.STR_TO_INT_DIC[m.group(3)]
            refs[(c, v)].add(name)
    return refs


# ----------------------------------------------------------------------------- comparison


def clusters(atom: str):
    """Return list of (letter, marks) for an atom; marks in MAM-normal order."""
    atom = give_std_mark_order(atom)
    result = []
    pos = 0
    for m in CLUSTER_RE.finditer(atom):
        if m.start() != pos:
            stray = atom[pos : m.start()]
            result.append(("", stray))
        result.append((m.group(1), m.group(2)))
        pos = m.end()
    if pos != len(atom):
        result.append(("", atom[pos:]))
    return result


def is_tetragrammaton(skel: str) -> bool:
    return skel in ("יהוה", "ליהוה", "ביהוה", "וליהוה", "ויהוה", "כיהוה", "מיהוה")


def _last_meteg_cluster(cl) -> int | None:
    found = None
    for i, (_, marks) in enumerate(cl):
        if hpo.MTGOSLQ in marks:
            found = i
    return found


def classify(mam: Tok, oth: Tok, verse_final: bool, other: str) -> tuple[list, list]:
    """Return (labels, details) for a differing pair. Labels prefixed 'policy:' are MAM
    design policies documented in the introduction; the rest are candidate findings.
    ``other`` names the non-MAM side in the labels: Aleppo or Leningrad."""
    labels, details = [], []
    m_text, a_text = mam.text, oth.text
    m_atoms, a_atoms = m_text.split(hpu.MAQ), a_text.split(hpu.MAQ)
    if len(m_atoms) != len(a_atoms):
        if skeleton(m_text) == skeleton(a_text):
            if len(m_atoms) > len(a_atoms):
                labels.append(f"maqaf:MAM-has-{other}-lacks")
            else:
                labels.append(f"maqaf:{other}-has-MAM-lacks")
            # compare marks on the whole compound below
            m_atoms = [m_text.replace(hpu.MAQ, "")]
            a_atoms = [a_text.replace(hpu.MAQ, "")]
        else:
            labels.append("letters-and-grouping")
            details.append(f"skel {skeleton(m_text)} vs {skeleton(a_text)}")
            return labels, details
    last_atom = len(m_atoms) - 1
    for atom_index, (m_atom, a_atom) in enumerate(zip(m_atoms, a_atoms)):
        if skeleton(m_atom) != skeleton(a_atom):
            is_kq = mam.kq is not None or "kq-trivial" in mam.flags
            labels.append("ketiv-qere" if is_kq else "letters")
            details.append(f"skel {skeleton(m_atom)} vs {skeleton(a_atom)}")
            continue
        mc, ac = clusters(m_atom), clusters(a_atom)
        if len(mc) != len(ac):
            labels.append("cluster-count")
            continue
        final_atom = verse_final and atom_index == last_atom
        m_silluq = _last_meteg_cluster(mc) if final_atom else None
        a_has_m_silluq = m_silluq is not None and hpo.MTGOSLQ in ac[m_silluq][1]

        def kind(ch, i, side):
            if ch != hpo.MTGOSLQ:
                return mark_kind(ch)
            if not final_atom:
                return "meteg"
            if side == "MAM":
                return "silluq" if i == m_silluq else "meteg"
            return "meteg" if a_has_m_silluq else "meteg-or-silluq"

        skel = skeleton(m_atom)
        m_ole_pos = [i for i, (_, mk) in enumerate(mc) if hac.OLE in mk]
        a_ole_pos = [i for i, (_, mk) in enumerate(ac) if hac.OLE in mk]
        if m_ole_pos and a_ole_pos and m_ole_pos != a_ole_pos:
            labels.append("oleh-position")
            details.append(f"oleh MAM@{m_ole_pos} {other}@{a_ole_pos}")
        order_only = True
        for i, ((ml, mm), (al, am)) in enumerate(zip(mc, ac)):
            if mm == am:
                continue
            m_only = list((Counter(mm) - Counter(am)).elements())
            a_only = list((Counter(am) - Counter(mm)).elements())
            if not m_only and not a_only:
                continue  # same multiset, different order
            order_only = False
            # ---- policy rules
            if (
                m_only == [hpo.XOLAM]
                and not a_only
                and ml == "ה"
                and is_tetragrammaton(skel)
            ):
                labels.append("policy:divine-name-holam")
                continue
            # MAM's revia-mugrash policy covers only a chanted word stressed at its start,
            # where geresh muqdam and revia share one letter; elsewhere a missing revia
            # is a finding.
            if m_only == [hac.REV] and not a_only and hac.GER_M in mm:
                labels.append("policy:revia-mugrash-dot")
                continue
            if m_only == [hac.OLE] and not a_only and not a_ole_pos:
                labels.append("policy:oleh-supplied")
                continue
            if hac.OLE in m_only or hac.OLE in a_only:
                if m_ole_pos != a_ole_pos and m_ole_pos and a_ole_pos:
                    m_only = [x for x in m_only if x != hac.OLE]
                    a_only = [x for x in a_only if x != hac.OLE]
                    if not m_only and not a_only:
                        continue
            if m_only == [hpo.SHEVA] and len(a_only) == 1 and a_only[0] in HATAFS:
                labels.append("policy:hataf-non-guttural")
                continue
            if a_only == [hpo.RAFE] and not m_only:
                labels.append("policy:rafe-omitted")
                continue
            if m_only == [hac.Z_OR_TSOR] and not a_only and hac.Z_OR_TSOR in am:
                labels.append("policy:tsinnor-doubled")
                continue
            # HBCE has U+05AA, the code point MAM's introduction assigns the galgal, for
            # the atnax hafukh as well.
            if m_only == [hac.ATN_H] and a_only == [hac.YBY]:
                labels.append("policy:atnax-hafukh-encoded-as-galgal")
                continue
            if m_only == [hac.DEX] and not a_only and hac.DEX in am:
                labels.append("policy:dexi-doubled")
                continue
            # ---- findings
            # One stroke under one letter, read as U+05BD on one side and as an accent on
            # the other: a meteg or silluq against a merkha, tipexa or munax.
            m_accent = any(mark_kind(c) == "accent" for c in m_only)
            a_accent = any(mark_kind(c) == "accent" for c in a_only)
            if (hpo.MTGOSLQ in m_only and a_accent) or (
                hpo.MTGOSLQ in a_only and m_accent
            ):
                labels.append("stroke-shape")
            for ch in m_only:
                labels.append(f"{kind(ch, i, 'MAM')}:MAM-has:{uname(ch)}")
            for ch in a_only:
                labels.append(f"{kind(ch, i, other)}:{other}-has:{uname(ch)}")
            m_names = ",".join(uname(c) for c in mm)
            a_names = ",".join(uname(c) for c in am)
            details.append(
                f"cluster {i} ({ml}): MAM[{m_names}] vs {other[0]}[{a_names}]"
            )
        if order_only and give_std_mark_order(m_atom) != give_std_mark_order(a_atom):
            labels.append("order-only")
    if mam.paseq != oth.paseq:
        labels.append("paseq:MAM-has" if mam.paseq else f"paseq:{other}-has")
        if mam.paseq:
            details.append(
                "MAM " + ("legarmeh" if "legarmeh" in mam.flags else "narpas")
            )
    return labels, details


def align(mam_toks: list, oth_toks: list):
    """Pair tokens; returns list of (mam_tok|None, oth_tok|None)."""
    if len(mam_toks) == len(oth_toks):
        return list(zip(mam_toks, oth_toks))
    m_sk = [skeleton(t.text) for t in mam_toks]
    a_sk = [skeleton(t.text) for t in oth_toks]
    sm = difflib.SequenceMatcher(a=m_sk, b=a_sk, autojunk=False)
    pairs = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal" or (op == "replace" and (i2 - i1) == (j2 - j1)):
            pairs.extend(zip(mam_toks[i1:i2], oth_toks[j1:j2]))
        else:
            for t in mam_toks[i1:i2]:
                pairs.append((t, None))
            for t in oth_toks[j1:j2]:
                pairs.append((None, t))
    return pairs


def ref_key(ref: str):
    _, c, v = ref.split(".")
    return int(c), int(v)


def note_matches(target: str, tok_text: str) -> bool:
    ts = skeleton(target.replace(hpu.MAQ, ""))
    ws = skeleton(tok_text.replace(hpu.MAQ, ""))
    if not ts or not ws:
        return False
    return ws in ts or ts in ws


def _shown(tok: Tok) -> str:
    return tok.text + (" " + hpu.PASOLEG if tok.paseq else "")


def compare(siglum, mam, notes, intro, say, other, tagcount, only_range=None) -> None:
    """Compare one transcription with MAM, write its TSV, and ``say`` its summary.

    ``tagcount`` counts the transcription's TEI elements as they are read.
    """
    hbce = load_hbce(siglum, tagcount)
    rows = []
    label_counter = Counter()
    verses_compared = 0
    pairs_compared = 0
    identical = 0
    for ref in sorted(hbce, key=ref_key):
        c, v = ref_key(ref)
        if only_range and not (only_range[0] <= (c, v) <= only_range[1]):
            continue
        a_toks = [t for t in hbce[ref] if t.text]
        if not a_toks:
            continue
        m_toks = mam.get(ref)
        if m_toks is None:
            rows.append((ref, "", "", "", "no-MAM-verse", "", "", "", ""))
            continue
        verses_compared += 1
        verse_notes = notes.get(ref, [])
        m_last = m_toks[-1] if m_toks else None
        for m, a in align(m_toks, a_toks):
            pairs_compared += 1
            if m is None:
                labels, details = ["extra-in-" + other], []
            elif a is None:
                labels, details = ["missing-in-" + other], []
            elif not re.search(MARK_RE, a.text) and any(
                f.startswith("alt=") for f in a.flags
            ):
                labels, details = ["unpointed-orig-with-alt"], []
            else:
                ms, as_ = give_std_mark_order(m.text), give_std_mark_order(a.text)
                if ms == as_ and m.paseq == a.paseq:
                    identical += 1
                    continue
                labels, details = classify(m, a, m is m_last, other)
                if not labels:
                    labels = ["order-only"]
            word_text = (m.text if m else "") or (a.text if a else "")
            noted_word = [n for n in verse_notes if note_matches(n[0], word_text)]
            if a is not None and a.orig and not noted_word:
                noted_word = [n for n in verse_notes if note_matches(n[0], a.orig)]
            # MAM's hataf policy covers the hatafs it documents, each in a doc-note on
            # the chanted word; a hataf with no such note is a question about the codex.
            if "policy:hataf-non-guttural" in labels and not noted_word:
                labels.append("hataf-without-mam-note")
            for lab in labels:
                label_counter[
                    lab.split(":")[0] if lab.startswith("policy") else lab
                ] += 1
            intro_files = ",".join(sorted(intro.get((c, v), [])))
            flags = ""
            if a is not None:
                flags = (a.orig or "") + ("|unclear" if a.unclear else "")
                flags += "|" + ",".join(sorted(a.flags)) if a.flags else ""
            if noted_word:
                note_status = "word-note"
            else:
                note_status = "verse-note" if verse_notes else "none"
            note_text = " || ".join(
                f"{t} => {n[:160]}" for t, n in (noted_word or verse_notes)[:2]
            )
            rows.append(
                (
                    ref,
                    _shown(m) if m else "—",
                    _shown(a) if a else "—",
                    flags,
                    "; ".join(labels),
                    "; ".join(details),
                    note_status,
                    intro_files,
                    note_text,
                )
            )
    suffix = "_range" if only_range else ""
    out_path = hbce_paths.out_dir() / f"compare_{siglum}{suffix}.tsv"
    with out_path.open("w", encoding="utf-8", newline="\n") as f:
        f.write(
            f"ref\tMAM\t{other}\torig|flags\tlabels\tdetails\tdocnote\tintro\tnote_text\n"
        )
        for r in rows:
            f.write("\t".join(r) + "\n")
    say("")
    say(f"=== {siglum} vs MAM ({other}) ===")
    say(
        f"verses compared: {verses_compared}; chanted-word pairs: {pairs_compared};"
        f" identical: {identical}; differing rows: {len(rows)}"
    )
    say("label counts:")
    for lab, n in label_counter.most_common():
        say(f"  {n:5d}  {lab}")


def write_comparisons() -> list[str]:
    """Write the three comparison TSVs and ``out/compare_summary.txt``; return its lines."""
    lines = []
    mam_tags = Counter()
    mam = load_mam(mam_tags)
    lines.append(f"MAM verses: {len(mam)} ; MAM-simple tag counts: {dict(mam_tags)}")
    notes = load_docnotes()
    intro = load_intro_refs()
    lines.append(
        f"doc-note verses: {len(notes)} ; intro-mentioned Psalms verses: {len(intro)}"
    )
    ma_tags = Counter()
    compare("MA", mam, notes, intro, lines.append, "Aleppo", ma_tags)
    lines.append(f"HBCE tag counts: {dict(ma_tags)}")
    ml_range = ((15, 1), (25, 1))
    compare("ML", mam, notes, intro, lines.append, "Leningrad", Counter(), ml_range)
    compare("ML", mam, notes, intro, lines.append, "Leningrad", Counter())
    summary = hbce_paths.out_dir() / "compare_summary.txt"
    summary.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return lines
