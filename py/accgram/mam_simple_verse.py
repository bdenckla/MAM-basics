from __future__ import annotations

import json
from pathlib import Path

from mb_cmn import bib_locales as tbn
from mb_cmn import hebrew_punctuation as hpunc
from mb_misc import osis_book_abbrevs as oba

from wlc_cmn.wlc_book_codes import wlc_bb_codes, wlc_bb_to_bk39id

from mb_cmn import paths

# The three single-cantillation projections of a dually-cantillated span (issue wlc-utils#36).
# A ``cant-all-three`` node carries one child of each type: ``cant-combined`` (the
# dual/merged form, analogous to what WLC stores) and the two detangled strands
# ``cant-alef`` / ``cant-bet``.  ``_normalize_mam_simple_node`` is parameterized by which
# of these to descend into, so the loader can expose each strand as its own
# position-correct token stream (interleaved with the single-cant ``text`` around it).
CANT_COMBINED = "cant-combined"
CANT_ALEF = "cant-alef"
CANT_BET = "cant-bet"
_CANT_ALL_THREE = "cant-all-three"


def require_mam_simple(mam_simple_dir: Path) -> None:
    """Fail clearly when a caller-supplied MAM-simple XML directory is absent.

    The ordinary path is the local MAM-simple product. A caller may still supply
    ``--mam-simple-dir`` for an alternate input, and the exception therefore names the
    exact directory that the caller asked this loader to read.
    """
    if not mam_simple_dir.is_dir():
        raise FileNotFoundError(
            f"MAM-simple XML directory does not exist: {mam_simple_dir}"
        )


def default_mam_simple_dir(repo_root: Path) -> Path:
    # ``repo_root`` is retained so CLI ``--mam-simple-dir`` flags keep their
    # signature; the local-product lookup is delegated to the repository-root resolver.
    return paths.mam_simple_dir()


def load_mam_simple_for_refs(
    mam_simple_dir: Path,
    refs_by_book: dict[str, set[tuple[int, int]]],
    *,
    include_strands: bool = False,
) -> dict[str, dict[str, object]]:
    """Load the requested MAM-simple verses, keyed by compact bcv.

    ``include_strands`` (issue wlc-utils#36) additionally exposes each dually-cantillated span's
    two detangled strands as ``vels_cant_alef`` / ``vels_cant_bet`` streams (for the
    dual-cantillation detangler).  It is off by default so existing consumers keep
    receiving the plain ``{"vels": ...}`` shape unchanged."""
    require_mam_simple(mam_simple_dir)

    by_bcv: dict[str, dict[str, object]] = {}
    for bb, ref_pairs in refs_by_book.items():
        bk39id = wlc_bb_to_bk39id(bb)
        json_path = _mam_simple_json_path(mam_simple_dir, bk39id)
        if json_path is None:
            continue

        root = _read_json(json_path)
        if not isinstance(root, dict):
            raise ValueError(f"Expected root object in MAM-simple file: {json_path}")

        target_set = set(ref_pairs)
        for verse_node in _iter_dict_nodes(root):
            if verse_node.get("type") != "verse":
                continue

            osis_id = verse_node.get("osisID")
            osis_prefix = oba.BOOK_ABBREVS.get(bk39id)
            if (
                not isinstance(osis_id, str)
                or osis_prefix is None
                or not osis_id.startswith(f"{osis_prefix}.")
            ):
                continue

            chnu, vrnu = _parse_osis_id(osis_id)
            if (chnu, vrnu) not in target_set:
                continue

            bcv = f"{bb}{chnu}:{vrnu}"
            by_bcv[bcv] = {
                "mam_simple_json_file": json_path.name,
                "mam_simple_verse": _normalize_mam_simple_verse(
                    verse_node, include_strands=include_strands
                ),
            }

    return by_bcv


def mam_simple_refs(mam_simple_dir: Path) -> dict[str, set[tuple[int, int]]]:
    """Every verse the tree at ``mam_simple_dir`` has, in the shape ``load_mam_simple_for_refs``
    takes.

    Reading MAM-simple otherwise means knowing its verse list in advance, which is exactly what a
    caller working in a versification other than the one it came for does not have: this repo's
    surveys are keyed to WLC's refs and so read ``json-vtrad-bhs``, and a caller reaching for
    ``json-vtrad-mam`` has no WLC refs to ask it with.
    """
    require_mam_simple(mam_simple_dir)

    refs: dict[str, set[tuple[int, int]]] = {}
    for bb in wlc_bb_codes():
        bk39id = wlc_bb_to_bk39id(bb)
        json_path = _mam_simple_json_path(mam_simple_dir, bk39id)
        if json_path is None:
            continue
        osis_prefix = oba.BOOK_ABBREVS.get(bk39id)
        if osis_prefix is None:
            continue
        for verse_node in _iter_dict_nodes(_read_json(json_path)):
            if verse_node.get("type") != "verse":
                continue
            osis_id = verse_node.get("osisID")
            if not isinstance(osis_id, str) or not osis_id.startswith(
                f"{osis_prefix}."
            ):
                continue
            refs.setdefault(bb, set()).add(_parse_osis_id(osis_id))
    return refs


def _mam_simple_json_path(mam_simple_dir: Path, bk39id: str) -> Path | None:
    candidate_names = [_mam_simple_json_file_for_bk39id(bk39id), f"{bk39id}.json"]
    for candidate_name in candidate_names:
        candidate_path = mam_simple_dir / candidate_name
        if candidate_path.is_file():
            return candidate_path
    return None


def _mam_simple_json_file_for_bk39id(bk39id: str) -> str:
    bk24id = tbn.bk24id(bk39id)
    bk39ids = tbn.bk39ids_of_bk24(bk24id)
    if not bk39ids:
        return f"{bk39id}.json"

    first_prefix = oba.BOOK_ABBREVS.get(bk39ids[0])
    last_prefix = oba.BOOK_ABBREVS.get(bk39ids[-1])
    if first_prefix is None or last_prefix is None:
        return f"{bk39id}.json"

    if len(bk39ids) == 1:
        return f"{first_prefix}.json"
    return f"{first_prefix}-{last_prefix}.json"


def _read_json(path: Path):
    with path.open("r", encoding="utf-8") as f_in:
        return json.load(f_in)


def _iter_dict_nodes(value: object):
    if isinstance(value, dict):
        yield value
        contents = value.get("contents")
        if isinstance(contents, list):
            for child in contents:
                yield from _iter_dict_nodes(child)
    elif isinstance(value, list):
        for child in value:
            yield from _iter_dict_nodes(child)


def _parse_osis_id(osis_id: str) -> tuple[int, int]:
    parts = osis_id.split(".")
    if len(parts) != 3:
        raise ValueError(f"Malformed MAM-simple osisID: {osis_id}")

    try:
        chnu = int(parts[1])
        vrnu = int(parts[2])
    except ValueError as exc:
        raise ValueError(f"Malformed MAM-simple osisID: {osis_id}") from exc

    return chnu, vrnu


def _normalize_mam_simple_verse(
    verse_node: dict[str, object], *, include_strands: bool = False
) -> dict[str, object]:
    """Normalize a verse into ``vels`` (and, when requested, the two detangled strands).

    ``vels`` uses the ``cant-combined`` projection of any dual span (the single,
    WLC-analogous representation) -- so the default shape is unchanged for every
    consumer.  With ``include_strands`` it also carries ``vels_cant_alef`` /
    ``vels_cant_bet``, the ``cant-alef`` / ``cant-bet`` strands (issue wlc-utils#36).  In a verse
    with no dual span all three are identical, so a single-cantillation verse in a
    Decalogue range yields a shared stream automatically.
    """
    verse: dict[str, object] = {
        "vels": _normalize_mam_simple_node(verse_node, CANT_COMBINED),
    }
    if include_strands:
        verse["vels_cant_alef"] = _normalize_mam_simple_node(verse_node, CANT_ALEF)
        verse["vels_cant_bet"] = _normalize_mam_simple_node(verse_node, CANT_BET)
    return verse


class _Boundary:
    """A node that separates the text either side of it without contributing any.

    Dropping such a node by returning an empty string would FUSE the atoms either side
    into one, because a MAM-simple ``text`` run carries its own spaces and a structural
    node standing between two runs is often the only thing between them: Exodus 15:1 has
    ``...לֵאמֹ֑ר``, a ``shirah-space``, then ``אָשִׁ֤ירָה``, with no space in either run.
    So a dropped node yields one of these instead, and ``_tokens_from_fragments`` splits
    there.
    """

    def __repr__(self) -> str:  # pragma: no cover - debugging aid only
        return "<boundary>"


_BOUNDARY = _Boundary()

# Nodes that stand BETWEEN atoms and contribute no text of their own.  Each yields a
# boundary rather than nothing at all -- see ``_Boundary``.
_DROPPED_NODE_TYPES = frozenset(
    (
        "good-ending",
        "spi-pe2",
        "spi-pe3",
        "spi-samekh2",
        "spi-samekh3",
        "spi-invnun",
        "shirah-space",
    )
)


def _normalize_mam_simple_node(
    node: object, cant_strand: str = CANT_COMBINED
) -> list[object]:
    """The ATOMS of one node's subtree -- one written word each, between spaces or maqafs
    -- with every maqaf kept on the atom it follows, plus a lone PASOLEG token for each
    paseq/legarmeh.

    Atoms and not chanted words: ``maqaf_nonfinal_accents._join_on_maqaf`` and the
    scanners fold a maqaf compound into one chanted word downstream, an atom that ends in
    a maqaf continuing into the next.
    """
    return _tokens_from_fragments(_mam_simple_fragments(node, cant_strand))


def _mam_simple_fragments(
    node: object, cant_strand: str = CANT_COMBINED
) -> list[object]:
    """One node's subtree as text fragments and ``_BOUNDARY`` separators.

    Tokenizing each node's text separately would be simpler, and is what this loader did
    until issue wlc-utils#91.  It cannot be right, because several of MAM-simple's node types sit
    INSIDE an atom rather than between atoms, and per-node tokenization splits the atom
    at each of them:

    * ``letter-large`` / ``letter-small`` / ``letter-hung`` -- a letter written large,
      small or suspended, wrapped with the rest of its atom in an ``slh-word``.  Genesis
      1:1 came out as בְּ and רֵאשִׁ֖ית, Leviticus 13:33 as וְהִ֨תְ, גַּ and לָּ֔ח.  These
      need no case below: the fall-through concatenates their text, which is what
      MAM-simple's own reference handlers do with them (``py-examples/osis/
      osis_handlers.py`` passes each straight into the surrounding run).
    * ``implicit-maqaf`` -- MAM's gray maqaf, which belongs on the END of the atom before
      it.  Emitted as a token of its own it reached ``_join_on_maqaf`` after that atom had
      been closed, and so attached FORWARD: Psalms 106:1 came out as הַ֥לְלוּ and ־יָ֨הּ,
      two chanted words with the maqaf at the front of the second, where MAM has the one
      chanted word הַ֥לְלוּ־יָ֨הּ.

    And ``sdt-note`` is not verse text at all -- it is the note half of a ``scrdfftar``, a
    targeted scroll-difference note, whose unpointed commentary and pointed specimen both
    reached the stream as tokens.  Exodus 17:16's one-atom כֵּ֣סְיָ֔הּ is a specimen quoted
    from the Aleppo Codex inside such a note, and it read as a chanted word of the verse;
    the running text there is the two-atom כֵּ֣ס יָ֔הּ every other corpus has.  The
    reference handlers map ``sdt-note`` to empty as well.
    """
    if not isinstance(node, dict):
        return []

    node_type = node.get("type")
    if isinstance(node_type, str):
        if node_type in _DROPPED_NODE_TYPES:
            return [_BOUNDARY]
        if node_type == "sdt-note":
            # Nothing, and NOT a boundary: a scroll-difference note is an editorial
            # aside written inside the running text rather than between two atoms, and
            # at Genesis 4:13, Numbers 1:17, Numbers 25:12 and Deuteronomy 11:21 the
            # ``text`` run right after it holds that verse's sof pasuq alone -- which
            # belongs to the atom the note interrupted.  Every other note is followed by
            # a run that opens with a space, so dropping it outright fuses nothing.
            return []
        if node_type in {"lp-paseq", "lp-legarmeih"}:
            # A token of its own, as it has always been: the mark stands between two
            # atoms rather than inside either.
            return [_BOUNDARY, hpunc.PASOLEG, _BOUNDARY]
        if node_type == "implicit-maqaf":
            # No boundary before it, so it lands on the atom it follows.
            return [hpunc.MAQ]
        if node_type == _CANT_ALL_THREE:
            # A dual-cantillation span: descend into the requested strand only, so each
            # projection (combined / alef / bet) is a complete, position-correct word
            # sequence interleaved with the surrounding single-cant ``text``.
            contents = node.get("contents")
            if isinstance(contents, list):
                for child in contents:
                    if isinstance(child, dict) and child.get("type") == cant_strand:
                        return _mam_simple_fragments(child, cant_strand)
            return []
        if node_type in {"kq", "kq-trivial", "kq-q-velo-k"}:
            return _mam_simple_kq_qere_fragments(node, cant_strand)
        if node_type in {"kq-k", "ketiv", "kq-k-velo-q"}:
            return [_BOUNDARY]

    contents = node.get("contents")
    if isinstance(contents, list):
        out_fragments: list[object] = []
        for child in contents:
            out_fragments.extend(_mam_simple_fragments(child, cant_strand))
        return out_fragments

    text = node.get("text")
    if isinstance(text, str):
        return [text]

    return []


def _mam_simple_kq_qere_fragments(
    node: dict[str, object], cant_strand: str = CANT_COMBINED
) -> list[object]:
    """A ketiv/qere node's QERE side, spliced into the run around it.

    The qere is the side that has the marks the scanners read; a ketiv is unpointed and
    never accented, so it can only add spurious unaccented atoms.

    No boundary either side, because the runs around a qere carry their own spacing, and in
    two shapes there is nothing at all between a qere and the rest of its atom.  Proverbs 23:5
    has an ``implicit-maqaf`` right after one, and MAM has הֲתָ֤עִיף־עֵינֶ֥יךָ as a single
    chanted word; a boundary would strand that maqaf as a token of its own and hand it to
    the atom after it.  And a verse-final qere is followed by a ``text`` run holding the
    sof pasuq alone -- 101 verses of it, ``וַיִּֽשְׁתַּחֲוֽוּ׃`` at Genesis 43:28 among them -- so
    a boundary made the sof pasuq a chanted word in its own right and left the verse's
    real last chanted word looking mid-verse, where a U+05BD is a meteg and not silluq.
    """
    contents = node.get("contents")
    if not isinstance(contents, list):
        text = node.get("text")
        return [text] if isinstance(text, str) else []

    qere_nodes = [
        child for child in contents if isinstance(child, dict) and _is_qere_node(child)
    ]
    chosen = qere_nodes or [
        child
        for child in contents
        if not (isinstance(child, dict) and _is_ketiv_node(child))
    ]
    out_fragments: list[object] = []
    for child in chosen:
        out_fragments.extend(_mam_simple_fragments(child, cant_strand))
    return out_fragments


def _tokens_from_fragments(fragments: list[object]) -> list[object]:
    """Concatenate the text fragments between boundaries, then split each run into atoms.

    Splitting a RUN rather than a node is the whole point: a run is however much of the
    verse no structural node interrupts, so a special letter and a gray maqaf are inside
    the atom they belong to by the time the split happens.
    """
    out_tokens: list[object] = []
    run: list[str] = []
    for fragment in fragments:
        if fragment is _BOUNDARY:
            if run:
                out_tokens.extend(_split_mam_simple_text("".join(run)))
                run = []
        else:
            run.append(fragment)
    if run:
        out_tokens.extend(_split_mam_simple_text("".join(run)))
    return out_tokens


def _is_qere_node(node: dict[str, object]) -> bool:
    node_type = node.get("type")
    return isinstance(node_type, str) and node_type in {
        "qere",
        "kq-q",
        "kq-trivial",
        "kq-q-velo-k",
    }


def _is_ketiv_node(node: dict[str, object]) -> bool:
    node_type = node.get("type")
    return isinstance(node_type, str) and node_type in {"ketiv", "kq-k", "kq-k-velo-q"}


def _split_mam_simple_text(text: str) -> list[object]:
    out_tokens: list[object] = []
    current = []
    for ch in text:
        if ch == " ":
            if current:
                out_tokens.append("".join(current))
                current = []
            continue

        current.append(ch)
        if ch == hpunc.MAQ:
            out_tokens.append("".join(current))
            current = []

    if current:
        out_tokens.append("".join(current))

    return out_tokens
