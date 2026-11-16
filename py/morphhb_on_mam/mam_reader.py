"""MAM's atoms from MAM-simple's JSON in the BHS versification.

Written by Claude (Opus 5.5) on 2026-11-15 for the morphhb-on-MAM feasibility study, and moved
into this package on 2026-11-16, when the study was put on ice (morphhb-on-mam/README.md).

Closed dispatch on every element type that MAM-simple's JSON documentation lists
(gh-pages/MAM-simple/reading-mam-simple-json.html, "Child Object Types"); any other type, or a
documented type in an undocumented place, raises.  Nothing here changes MAM's text: an atom's
text is the exact characters MAM-simple stores, separators removed.

A verse becomes, for one chosen strand of each dual cantillation, two sides:
- the ketiv side: plain text, each ketiv (kq-k, kq-k-velo-q) and each trivial pair (kq-trivial);
- the qere side: plain text, each qere (kq-q, kq-q-velo-k) and each trivial pair.
Each atom records where its characters came from, so that an atom present on both sides (a
plain atom) is recognized as one atom: its "span" is the tuple of (segment, offset) of its
characters, identical on both sides for a plain atom.
"""

import unicodedata

from mb_cmn import mam_simple_json as msj
from mb_cmn import paths
from mb_cmn.mam_simple_book_group import resolve_book_group_path

MAQAF = "\N{HEBREW PUNCTUATION MAQAF}"
PASEQ = "\N{HEBREW PUNCTUATION PASEQ}"
SOF_PASUQ = "\N{HEBREW PUNCTUATION SOF PASUQ}"
NUN_HAFUKHA = "\N{HEBREW PUNCTUATION NUN HAFUKHA}"
STRANDS = ("cant-combined", "cant-alef", "cant-bet")

# The 24 book groups, as json-vtrad-mam names them; the BHS folder overrides some.
GROUPS = [
    "Gen",
    "Exod",
    "Lev",
    "Num",
    "Deut",
    "Josh",
    "Judg",
    "1Sam-2Sam",
    "1Kgs-2Kgs",
    "Isa",
    "Jer",
    "Ezek",
    "Hos-Mal",
    "Ps",
    "Prov",
    "Job",
    "Song",
    "Ruth",
    "Lam",
    "Eccl",
    "Esth",
    "Dan",
    "Ezra-Neh",
    "1Chr-2Chr",
]

# Characters a stored text may hold, by class.  Any other character raises.
LETTER = "letter"
MARK = "mark"
SEP = "sep"


def char_class(ch):
    if "\N{HEBREW LETTER ALEF}" <= ch <= "\N{HEBREW LETTER TAV}":
        return LETTER
    if ch in (" ", MAQAF, SOF_PASUQ, PASEQ):
        return SEP
    if "\N{HEBREW ACCENT ETNAHTA}" <= ch <= "\N{HEBREW POINT QAMATS QATAN}":
        if ch in (
            NUN_HAFUKHA,
            "\N{HEBREW PUNCTUATION GERESH}",
            "\N{HEBREW PUNCTUATION GERSHAYIM}",
        ):
            raise ValueError("unexpected punctuation %s" % unicodedata.name(ch))
        return MARK
    if ch in (
        "\N{COMBINING GRAPHEME JOINER}",
        "\N{ZERO WIDTH JOINER}",
        "\N{ZERO WIDTH NON-JOINER}",
    ):
        return MARK
    raise ValueError("unexpected character %r %s" % (ch, unicodedata.name(ch, "?")))


class Verse:
    """One MAM-simple verse read in one strand: segments and the atoms of each side."""

    def __init__(self, osis_id, node, strand):
        self.osis_id = osis_id
        self.strand = strand
        self.segments = []  # dicts: sides, text, kind, flags
        self.has_cant3 = False
        self.notes = []  # scrdfftar notes, for the record
        self._walk_verse(node)
        # MAM-simple's BHS file gives a verse that MAM lacks (Joshua 21:36 and 21:37) the
        # text EM DASH alone.
        whole = "".join(s["text"] for s in self.segments).strip()
        self.absent = whole == "\N{EM DASH}"
        if self.absent:
            if len(self.segments) != 1:
                raise ValueError("%s: an em dash with other content" % osis_id)
            self.sides = {"k": [], "q": []}
        else:
            self.sides = {side: self._atoms(side) for side in ("k", "q")}

    # ---------------------------------------------------------------- the walk

    def _seg(self, sides, text, kind, **flags):
        self.segments.append(
            {"sides": sides, "text": text, "kind": kind, "flags": flags}
        )

    def _walk_verse(self, node):
        attrs = msj.attributes(node)
        if "text" in attrs:
            self._seg("kq", attrs["text"], "plain")
            return
        for child in msj.children(node):
            self._walk(child, "kq", "plain")

    def _own(self, node, sides, kind):
        """A node whose content is either a text field or children."""
        attrs = msj.attributes(node)
        if "text" in attrs:
            self._seg(sides, attrs["text"], kind)
        else:
            kids = msj.children(node)
            if not kids:
                raise ValueError(
                    "%s: %s with neither text nor contents"
                    % (self.osis_id, node["type"])
                )
            for child in kids:
                self._walk(child, sides, kind)

    def _walk(self, node, sides, kind):
        t = node["type"]
        attrs = msj.attributes(node)
        where = "%s %s" % (self.osis_id, t)
        if t == "text":
            self._seg(sides, attrs["text"], kind)
        elif t == "silluq-before-meteg":
            self._seg(sides, attrs["text"], kind, silluq_before_meteg=True)
        elif t == "lp-legarmeih":
            # A mark that belongs with the preceding atom.
            self._seg(sides, PASEQ, kind, legarmeh=True)
        elif t == "lp-paseq":
            self._seg(sides, " " + PASEQ + " ", kind, paseq=True)
        elif t == "implicit-maqaf":
            self._seg(sides, MAQAF, kind, implicit_maqaf=True)
        elif t == "slh-word":
            # The children spell the atom; slhw-desc-0 is the same atom as one string.  Ruth
            # 3:13's slh-word also holds an lp-legarmeih, which belongs to the atom.
            desc0 = attrs["slhw-desc-0"]
            code = attrs["slhw-desc-2"].strip()
            spelled = []
            for c in msj.children(node):
                if c["type"] == "lp-legarmeih":
                    self._seg(sides, PASEQ, kind, legarmeh=True)
                    spelled.append(PASEQ)  # slhw-desc-0 holds the legarmeh's paseq
                    continue
                piece = self._slh_text(c, where)
                spelled.append(piece)
                self._seg(sides, piece, kind, slh=code)
            if "".join(spelled) != desc0:
                raise ValueError(
                    "%s: slh children %r differ from slhw-desc-0 %r"
                    % (where, spelled, desc0)
                )
        elif t == "kq":
            kids = msj.children(node)
            types = sorted(c["type"] for c in kids)
            if types != ["kq-k", "kq-q"] or sides != "kq" or kind != "plain":
                raise ValueError(
                    "%s: kq children %r in %s/%s" % (where, types, sides, kind)
                )
            first = kids[0]["type"]
            for c in kids:
                if c["type"] == "kq-k":
                    self._own(c, "k", "kq-k")
                else:
                    self._own(c, "q", "kq-q-first" if first == "kq-q" else "kq-q")
        elif t == "kq-trivial":
            if sides != "kq" or kind != "plain":
                raise ValueError("%s: kq-trivial inside %s/%s" % (where, sides, kind))
            self._own(node, "kq", "kq-trivial")
        elif t == "kq-k-velo-q":
            if sides != "kq" or kind != "plain":
                raise ValueError("%s: inside %s/%s" % (where, sides, kind))
            self._seg("k", attrs["text"], "kq-k-velo-q")
            self._seg("q", " ", "kq-k-velo-q-gap")
        elif t == "kq-k-velo-q-maq":
            if sides != "kq" or kind != "plain":
                raise ValueError("%s: inside %s/%s" % (where, sides, kind))
            self._seg("k", MAQAF, "kq-k-velo-q")
        elif t == "kq-q-velo-k":
            if sides != "kq" or kind != "plain":
                raise ValueError("%s: inside %s/%s" % (where, sides, kind))
            self._seg("q", attrs["text"], "kq-q-velo-k")
            self._seg("k", " ", "kq-q-velo-k-gap")
        elif t == "cant-all-three":
            kids = msj.children(node)
            if [c["type"] for c in kids] != list(STRANDS):
                raise ValueError("%s: strands %r" % (where, [c["type"] for c in kids]))
            self.has_cant3 = True
            (chosen,) = [c for c in kids if c["type"] == self.strand]
            self._own(chosen, sides, kind)
        elif t == "scrdfftar":
            kids = msj.children(node)
            if sorted(c["type"] for c in kids) != ["sdt-note", "sdt-target"]:
                raise ValueError("%s: children %r" % (where, [c["type"] for c in kids]))
            for c in kids:
                if c["type"] == "sdt-target":
                    # Exod.26.6's target is empty: the note is about a place, not a word.
                    if msj.attributes(c) or msj.children(c):
                        self._own(c, sides, kind)
                    else:
                        self.notes.append({"empty_target": True})
                else:
                    self.notes.append(c)
        elif t in ("shirah-space", "spi-pe2", "spi-pe3", "spi-samekh2", "spi-samekh3"):
            # Numbers 10:35's marker has class "nu10-invnun-neighbor"; no other field occurs.
            if set(attrs) - {"class"} or msj.children(node):
                raise ValueError("%s: unexpected fields %r" % (where, attrs))
            self._seg(sides, " ", kind, break_=t)
        elif t == "spi-invnun":
            if set(attrs) - {"class"} or msj.children(node):
                raise ValueError("%s: unexpected fields %r" % (where, attrs))
            self._seg(sides, " ", kind, invnun=True)
        elif t == "good-ending":
            pass  # a repetition after a book's last verse, not running text
        else:
            raise ValueError(
                "%s: unhandled MAM-simple element in %s/%s" % (where, sides, kind)
            )

    def _slh_text(self, node, where):
        t = node["type"]
        attrs = msj.attributes(node)
        if t in ("text", "letter-small", "letter-large", "letter-hung"):
            return attrs["text"]
        raise ValueError("%s: unhandled slh-word child %r" % (where, t))

    # ---------------------------------------------------------------- atoms

    def _atoms(self, side):
        chars = []  # (ch, segment index, offset)
        for si, seg in enumerate(self.segments):
            if side not in seg["sides"]:
                continue
            for off, ch in enumerate(seg["text"]):
                chars.append((ch, si, off))
        atoms, cur = [], []

        def close(after):
            if not cur:
                if after == MAQAF:
                    raise ValueError(
                        "%s %s: maqaf with no atom before it" % (self.osis_id, side)
                    )
                return
            text = "".join(c for c, _s, _o in cur)
            segs = sorted({s for _c, s, _o in cur})
            kinds = sorted({self.segments[s]["kind"] for s in segs})
            flags = {}
            for s in segs:
                for k, v in self.segments[s]["flags"].items():
                    if k not in (
                        "legarmeh",
                        "paseq",
                        "implicit_maqaf",
                        "break_",
                        "invnun",
                    ):
                        flags[k] = v
            atoms.append(
                {
                    "text": text,
                    "letters": "".join(c for c in text if char_class(c) == LETTER),
                    "span": tuple((s, o) for _c, s, o in cur),
                    "kinds": kinds,
                    "flags": flags,
                    "maqaf_after": False,
                    "implicit_maqaf": False,
                    "legarmeh": False,
                    "paseq_after": False,
                    "sof_pasuq": False,
                }
            )
            cur.clear()

        for ch, si, off in chars:
            cc = char_class(ch)
            if cc != SEP:
                if cc == MARK and not cur:
                    raise ValueError(
                        "%s %s: a mark %s with no letter"
                        % (self.osis_id, side, unicodedata.name(ch))
                    )
                if (
                    cur
                    and self.segments[cur[-1][1]]["sides"] != self.segments[si]["sides"]
                ):
                    # A one-sided segment (a ketiv or a qere) meets a two-sided one with no
                    # separator between them: on the ketiv side, MAM-simple writes a ketiv
                    # straight before the next word when the qere ends in a maqaf (for
                    # example Num.23.13).  Treated as an atom boundary, and flagged.
                    if cc == MARK:
                        raise ValueError(
                            "%s %s: a mark begins a segment" % (self.osis_id, side)
                        )
                    close("boundary")
                    atoms[-1]["boundary_added"] = True
                cur.append((ch, si, off))
                continue
            had = bool(cur)
            close(ch)
            seg = self.segments[si]
            if ch == MAQAF:
                if not had:
                    raise ValueError(
                        "%s %s: maqaf after a separator" % (self.osis_id, side)
                    )
                atoms[-1]["maqaf_after"] = True
                atoms[-1]["implicit_maqaf"] = bool(seg["flags"].get("implicit_maqaf"))
            elif ch == PASEQ:
                if not atoms:
                    raise ValueError(
                        "%s %s: paseq at verse start" % (self.osis_id, side)
                    )
                if seg["flags"].get("legarmeh"):
                    atoms[-1]["legarmeh"] = True
                else:
                    atoms[-1]["paseq_after"] = True
            elif ch == SOF_PASUQ:
                atoms[-1]["sof_pasuq"] = True
        close(None)
        for i, a in enumerate(atoms):
            a["i"] = i
        return atoms


def book_group_paths():
    root = paths.repo_root() / "MAM-simple"
    return [
        resolve_book_group_path(root, fmt="json", vtrad="bhs", stems=(g,))
        for g in GROUPS
    ]


def read_mam(strand="cant-combined"):
    """{osisID: Verse} for the whole of MAM, in the BHS versification, in `strand`."""
    out = {}
    for path in book_group_paths():
        root = msj.read_book_group(path)
        for v in msj.verses(root):
            osis_id = v["osisID"]
            if osis_id in out:
                raise ValueError("duplicate verse %s" % osis_id)
            out[osis_id] = Verse(osis_id, v, strand)
    return out


def raw_verses():
    """{osisID: MAM-simple verse node}, for rereading a verse in another strand."""
    out = {}
    for path in book_group_paths():
        root = msj.read_book_group(path)
        for v in msj.verses(root):
            out[v["osisID"]] = v
    return out
