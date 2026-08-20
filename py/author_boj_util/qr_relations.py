"""Author-curated relations between quirkrec records.

A *relation* ties together the quirkrec records that together constitute
**one** divergence between μL and the consensus reading. It is the principled
signal — distinct from "same verse" — that lets a consumer know that N records
must be synthesized *jointly* rather than independently.

The seed (and currently only) kind is ``"move"``: an accent that μL writes on
one word is, in the consensus reading, relocated to a different word in the
same verse. Accent count is conserved (1 → 1); only the host word changes.
That conservation is the defining signature of a move.

Direction convention for kind ``"move"``:

* ``"from"`` = the **μL host** — the record whose word carries the accent in
  μL (on its ``qr-lc-proposed`` side) but loses it in the consensus.
* ``"to"``   = the **consensus host** — the record whose word gains the accent
  in the consensus (on its ``qr-consensus`` side).

So a move reads: "the consensus moves the *accent* **from** *from-word*
**to** *to-word*." Seed case (22:21): the אתנח μL writes on עמו is, in the
consensus, relocated to ושלם.

Records are named by their ``short_id`` (``CCVV[-WORDID]``); see
``author_boj_util/short_id_etc.py``. ``QR_RELATIONS`` below is the single source
of truth: ``add_qr_rel_edges`` derives the two mirror-image, per-record
``qr-rel`` edges from each authored relation, so the mirrors can never desync.

``kind`` is kept as a field for extensibility (future split / merge / swap),
but only ``"move"`` is implemented today. Do **not** confuse a relation with:

* ``pgroup`` (a presentation group; orthogonal to "one divergence"),
* ``qr-cv`` (merely "same verse"; over-merges independent same-verse quirks),
* ``qr-auto-diff``'s intra-word "move" verb (a per-record, *within-one-word*
  diff; a relation here is *inter-word, across records*).
"""

from mb_cmn import hebrew_accents as hac
from author_boj_util.short_id_etc import short_id
from author_boj_util.proposed import proposed
from author_boj_util.author import consensus_to_bare_hebrew

# The authored relations (single source of truth). See module docstring for the
# direction convention and the short_id key format.
QR_RELATIONS = [
    {
        "kind": "move",  # only kind in scope; field kept for extensibility
        "accent": "atnax",  # the accent that relocates
        "from": "2221-3MV",  # μL's host (loses the accent in the consensus): עמו
        "to": "2221-VJL6",  # consensus's host (gains it): ושלם
    },
]

# Per-relation accent registry: key -> codepoint (for conservation checks) and
# Hebrew display name (for HTML). Keep keys in sync with the "accent" field of
# QR_RELATIONS.
ACCENT_INFO = {
    "atnax": {"char": hac.ATN, "he": "אתנח"},
}


def validate_relations(records):
    """Cross-record validation of QR_RELATIONS against a list of records.

    Works on raw or enriched records alike (it only reads qr-cv, qr-consensus,
    and the proposed field). Raises AssertionError on any problem. Returns the
    short_id -> record lookup it built, so callers can reuse it.

    For each relation it asserts:
      * the kind is supported and the accent is known;
      * both endpoints resolve to existing records sharing the same qr-cv;
      * accent conservation for kind "move": the accent is present on the
        `from` record's μL (proposed) side and absent from its consensus, and
        present on the `to` record's consensus and absent from its proposed
        side. This is exactly the conservation that bdenckla/wlc-utils#43 had
        to verify by hand.
    """
    by_sid = {short_id(qr): qr for qr in records}
    for rel in QR_RELATIONS:
        _validate_one_relation(rel, by_sid)
    return by_sid


def add_qr_rel_edges(records):
    """Return records with symmetric, resolved qr-rel edges attached.

    Validates QR_RELATIONS first, then for each relation appends a mirror-image
    edge to each of the two participating records. qr-rel is a list because a
    record may take part in more than one relation.
    """
    by_sid = validate_relations(records)
    edges_by_sid = {}
    for rel in QR_RELATIONS:
        from_edge, to_edge = _mirror_edges(rel, by_sid)
        # Mirror consistency is guaranteed by single-source derivation; assert
        # it anyway so a future refactor of _mirror_edges can't break it.
        assert from_edge["other"] == short_id(by_sid[rel["to"]])
        assert to_edge["other"] == short_id(by_sid[rel["from"]])
        edges_by_sid.setdefault(rel["from"], []).append(from_edge)
        edges_by_sid.setdefault(rel["to"], []).append(to_edge)
    return [_maybe_attach_edges(qr, edges_by_sid) for qr in records]


def _validate_one_relation(rel, by_sid):
    kind = rel["kind"]
    assert kind == "move", f"Unsupported relation kind {kind!r} in {rel}"
    accent = rel["accent"]
    assert accent in ACCENT_INFO, f"Unknown relation accent {accent!r} in {rel}"
    char = ACCENT_INFO[accent]["char"]
    from_sid, to_sid = rel["from"], rel["to"]
    assert from_sid in by_sid, f"Relation 'from' record not found: {from_sid}"
    assert to_sid in by_sid, f"Relation 'to' record not found: {to_sid}"
    from_qr, to_qr = by_sid[from_sid], by_sid[to_sid]
    assert from_qr["qr-cv"] == to_qr["qr-cv"], (
        f"Relation crosses verses: {from_sid} ({from_qr['qr-cv']}) "
        f"vs {to_sid} ({to_qr['qr-cv']})"
    )
    # Accent conservation (the move signature: 1 accent either way).
    assert char in proposed(
        from_qr
    ), f"{from_sid}: move accent {accent!r} absent from its μL (proposed) side"
    assert (
        char not in from_qr["qr-consensus"]
    ), f"{from_sid}: move accent {accent!r} unexpectedly present in its consensus"
    assert (
        char in to_qr["qr-consensus"]
    ), f"{to_sid}: move accent {accent!r} absent from its consensus"
    assert char not in proposed(
        to_qr
    ), f"{to_sid}: move accent {accent!r} unexpectedly present in its μL (proposed) side"


def _mirror_edges(rel, by_sid):
    from_qr, to_qr = by_sid[rel["from"]], by_sid[rel["to"]]
    from_edge = _edge(rel, "from", other_qr=to_qr)
    to_edge = _edge(rel, "to", other_qr=from_qr)
    return from_edge, to_edge


def _edge(rel, role, other_qr):
    return {
        "kind": rel["kind"],
        "accent": rel["accent"],
        "role": role,
        "other": short_id(other_qr),
        "other-cv": other_qr["qr-cv"],
        "other-word": consensus_to_bare_hebrew(other_qr["qr-consensus"]),
    }


def _maybe_attach_edges(qr, edges_by_sid):
    edges = edges_by_sid.get(short_id(qr))
    if edges is None:
        return qr
    return {**qr, "qr-rel": edges}
