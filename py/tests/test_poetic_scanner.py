"""Tests for the poetic (Three Books) scanner.

Pins the decoded token stream of a few real Psalms verses whose Michigan-Claremont
encoding was checked by hand against the M-C accent table (wlc420/supplmt.wts,
column II) and Yeivin ITM #358-374.  These exercise the tricky cases: the
revia mugrash geresh muqdam (11+81), oleh-we-yored (60 ole + 71 yored merkha),
azla/mahapakh legarmeh (63/70 + 05 paseq), the galgal servus of oleh-we-yored
(93), and the revia gadol/qatan/mugrash disambiguation.

Token-type names come from accgram.poetic_accent_names (no re-typed literals).

Run:
    .venv/Scripts/python.exe -m pytest py/tests/test_poetic_scanner.py -v
"""

from accgram import accent_marks as am
from accgram import poetic_accent_names as pan
from accgram.poetic_scanner import scan_accents
from accgram.poetic_ply_grammar import build_parser, parse_tokens
from accgram.poetic_scanner import scan_verse
from tests.mc_marks import mc_to_marks

# The fixtures are written in the legacy M-C encoding (checked by hand against the
# accent table) and converted to the Phase-2 mark alphabet here (issue wlc-utils#9).


def _types(body):
    return [t for t, _ in scan_accents(mc_to_marks(body))]


def _types_marks(body):
    """Token types for a body already in the Phase-2 mark alphabet (not M-C)."""
    return [t for t, _ in scan_accents(body)]


def test_ps_1_1_revia_mugrash_geresh_muqdam():
    # ... 11L"CI81YM = geresh muqdam (11) + revia (81) -> one revia mugrash.
    body = (
        r')A71$:75R"Y-HF/)I81Y$]c ):A$E70R05 LO71) HFLAK:02 B.A/(:ACA93T '
        r"R:$F60(I71YM W./B:/DE74REK: 13XA+.F)IYM LO71) (FMF92D "
        r'W./B:/MOW$A71B 11L"CI81YM LO74) YF$F75B00'
    )
    types = _types(body)
    assert types[-1] == pan.SOFPASUQ
    assert types[-2] == pan.SILLUQ  # 75 before 00
    assert pan.REVIA_MUGRASH in types  # the 11(+81)
    assert pan.ATNAX in types  # 92
    assert pan.TSINNOR in types  # 02 (no zarqa in poetic)
    assert pan.DEXI in types  # 13


def test_ps_2_2_azla_legarmeh():
    # YI71T:YAC.:B63W.05 = azla (63) + paseq (05) -> azla legarmeh.
    body = (
        r"YI71T:YAC.:B63W.05 MAL:K\"Y-)E81REC W:/ROWZ:NI71YM "
        r"NO75WS:DW.-YF92XAD (AL-11Y:HWFH W:/(AL-M:$IYX/O75W00"
    )
    types = _types(body)
    assert pan.LEGARMEH in types
    # the revia after the legarmeh (81 on )EREC, next disjunctive atnax) is gadol
    assert pan.REVIA_GADOL in types
    assert pan.ATNAX in types


def test_ps_3_3_oleh_weyored_with_galgal_servus():
    # )OM:RI93YM = galgal servus; L:/NA60P:$/I71Y = ole (60) + yored merkha (71).
    body = (
        r"RAB.IYM02 )OM:RI93YM L:/NA60P:$/I71Y )\"70YN "
        r"Y:75$W.(F65T/FH L./O64W B\"75/)LOHI64YM SE75LFH00"
    )
    types = _types(body)
    assert pan.OLEH_WEYORED in types
    assert pan.TSINNOR in types  # 02 on RAB.IYM
    # the galgal (93) precedes oleh-we-yored as its servus
    assert types.index(pan.GALGAL) < types.index(pan.OLEH_WEYORED)
    # the yored merkha (71) is folded into OLEH_WEYORED, not emitted separately just
    # before it: no MERKHA sits between GALGAL and OLEH_WEYORED
    g, o = types.index(pan.GALGAL), types.index(pan.OLEH_WEYORED)
    assert pan.MERKHA not in types[g + 1 : o]


def test_ps_37_28_revia_gadol_then_dexi_then_atnax():
    # Yeivin's legarmeh-under-revia-gadol example; second half has dexi before atnax.
    body = (
        r"K.I70Y Y:HWF63H05 )O82H\"70B MI$:P.F81+ W:/LO)-YA(:AZO74B "
        r")ET-13X:ASIYDFY/W L:/(OWLF74M NI$:MF92RW. W:/ZE73RA( R:$F(I74YM NIK:RF75T00"
    )
    types = _types(body)
    assert pan.LEGARMEH in types  # 63+05 on YHWH
    assert pan.REVIA_GADOL in types  # 81 on MI$:P.F+ (next disjunctive is atnax)
    assert pan.DEXI in types  # 13
    assert pan.ATNAX in types
    assert types[-2:] == [pan.SILLUQ, pan.SOFPASUQ]


def test_unmarked_oleh_recovered_after_galgal():
    # Ps 30:12: L omits the ole (#363), writing only the yored merkha (L/I71Y);
    # the galgal servus (93) immediately precedes it, so the bare merkha is
    # recovered as oleh-we-yored rather than read as a servus.  MAM-cross-checked.
    body = (
        r"HFPA74K:T.F MIS:P.:D/IY02 L:/MFXO93WL L/I71Y P.IT.A71X:T.F "
        r'&AQ./I92Y WA75/T.:)AZ.:R/"71NIY &IM:XF75H00'
    )
    types = _types(body)
    assert pan.OLEH_WEYORED in types
    # the galgal stays as the oleh-we-yored's servus, directly before it
    g, o = types.index(pan.GALGAL), types.index(pan.OLEH_WEYORED)
    assert o == g + 1
    # the verse now parses (it was a NO_PARSE before the recovery)
    parser = build_parser()
    toks = scan_verse("Psalms 30:12", mc_to_marks(body)).tokens
    assert parse_tokens(parser, toks) is not None


def test_galgal_then_marked_oleh_not_doubly_recovered():
    # When the ole IS marked (60+71), the yored is already folded into
    # OLEH_WEYORED by the rule table, so there is no bare MERKHA after the galgal
    # to misread (Ps 1:1: B.A/(:ACA93T R:$F60(I71YM).
    body = r"B.A/(:ACA93T R:$F60(I71YM W./B:/DE74REK: LO74) YF$F75B00"
    types = _types(body)
    assert types.count(pan.OLEH_WEYORED) == 1
    g, o = types.index(pan.GALGAL), types.index(pan.OLEH_WEYORED)
    assert o == g + 1
    assert pan.MERKHA not in types[g:o]


def test_revia_qatan_before_oleh():
    # A bare revia (81) whose next disjunctive is oleh-we-yored is revia qatan.
    body = r"FOO81 BAR60BAZ71 QUX75X00"
    assert pan.REVIA_QATAN in _types(body)


def test_ps124_4_plain_geresh_charity_to_revia_mugrash():
    # ps124:4: revia (U+0597) + plain geresh (U+059C) on ONE letter -- the only plain
    # geresh in the Three Books.  Read charitably as a single revia mugrash: the geresh
    # is *consumed* into the fused token, not silently swallowed by the catch-all (which
    # would leave a bare revia that only incidentally reclassifies to revia mugrash).
    # Body mirrors the real verse's shape: ... revia+geresh word (with a ]1 note) ...
    # then a meteg-before-sofpasuq silluq.
    body = (
        "X" + am.DEXI + "XX XX" + am.MUNAX + "XX XXX" + am.ATNAX + "XXX "
        "X" + am.REVIA + am.GERESH + "XXX]1 XX" + am.MERKHA + "X "
        "XX-XXX" + am.METEG + "XX" + am.SOF_PASUQ
    )
    types = _types_marks(body)
    assert pan.REVIA_MUGRASH in types
    assert types.count(pan.REVIA_MUGRASH) == 1
    # the geresh is consumed, so no spurious extra disjunctive appears
    assert pan.REVIA not in types and pan.REVIA_GADOL not in types
    assert types[-2:] == [pan.SILLUQ, pan.SOFPASUQ]


def test_revia_then_geresh_only_fuses_same_letter():
    # The charity is same-letter only (adjacency, no X between).  Trailing atnax makes a
    # *bare* revia reclassify to revia GADOL, so fusion (same-letter) vs swallow
    # (cross-letter) is visible in the output: were the trailing disjunctive silluq,
    # the bare revia would reclassify to mugrash too and hide the difference.
    tail = "X XX" + am.ATNAX + "X XX" + am.METEG + am.SOF_PASUQ
    same = _types_marks("X" + am.REVIA + am.GERESH + tail)
    cross = _types_marks("X" + am.REVIA + "X" + am.GERESH + tail)
    assert same.count(pan.REVIA_MUGRASH) == 1  # fused, regardless of what follows
    assert (
        pan.REVIA_GADOL in cross and pan.REVIA_MUGRASH not in cross
    )  # geresh swallowed


def test_intra_atom_tsinnorit_fuses_to_metsunnar():
    # Plan C: tsinnorit (U+0598) + its mahapakh / merkha partner on ONE chanted word
    # (same atom) -> one MAHAPAKH_METSUNNAR / MERKHA_METSUNNAR conjunctive; the
    # tsinnorit is consumed (fused), not swallowed.
    tail = "X XX" + am.ATNAX + "X XX" + am.METEG + am.SOF_PASUQ
    mah = _types_marks("X" + am.TSINNORIT + "X" + am.MAHAPAKH + "X" + tail)
    assert pan.MAHAPAKH_METSUNNAR in mah
    assert pan.MAHAPAKH not in mah  # the bare partner is gone (fused into metsunnar)
    assert pan.STRAY_ACCENT not in mah
    mer = _types_marks("X" + am.TSINNORIT + "X" + am.MERKHA + "X" + tail)
    assert pan.MERKHA_METSUNNAR in mer
    assert pan.MERKHA not in mer


def test_omitted_maqaf_tsinnorit_fuses_across_space():
    # Plan C / Breuer §22 (Ps 49:15 shape): a tsinnorit-ONLY atom (no main accent of
    # its own), then the omitted-hyphen space, then the atom completing the chanted
    # word and carrying the partner -> one metsunnar across the space.
    tail = "X XX" + am.ATNAX + "X XX" + am.METEG + am.SOF_PASUQ
    types = _types_marks("XX" + am.TSINNORIT + "X X" + am.MAHAPAKH + "X" + tail)
    assert types.count(pan.MAHAPAKH_METSUNNAR) == 1
    assert pan.MAHAPAKH not in types


def test_intra_atom_partner_wins_over_next_atom():
    # The omitted-maqaf rule fires only for a tsinnorit-ONLY atom: when the tsinnorit's
    # own atom already carries the partner, fusion takes that same-atom partner and
    # never reaches across the space to a following atom's conjunctive.
    tail = "X XX" + am.ATNAX + "X XX" + am.METEG + am.SOF_PASUQ
    types = _types_marks(
        "X" + am.TSINNORIT + "X" + am.MAHAPAKH + "X X" + am.MERKHA + "X" + tail
    )
    assert pan.MAHAPAKH_METSUNNAR in types  # fused with the same-atom mahapakh
    assert pan.MERKHA_METSUNNAR not in types  # did NOT reach the next atom's merkha
    assert pan.MERKHA in types  # which stays a plain servus


def test_bare_shalshelet_emits_qetannah():
    # Plan C: bare shalshelet (U+0593, no following paseq) is the conjunctive
    # qetannah, now emitted as a real servus instead of swallowed.
    tail = "X XX" + am.ATNAX + "X XX" + am.METEG + am.SOF_PASUQ
    bare = _types_marks("X" + am.SHALSHELET + "X" + tail)
    assert pan.SHALSHELET_QETANNAH in bare
    assert pan.SHALSHELET_GEDOLAH not in bare
    # shalshelet + paseq (same atom) is still the disjunctive gedolah (longest match)
    ged = _types_marks("X" + am.SHALSHELET + "X" + am.PASEQ + tail)
    assert pan.SHALSHELET_GEDOLAH in ged
    assert pan.SHALSHELET_QETANNAH not in ged


def test_same_letter_merkha_azla_fuses_to_bang():
    # Plan D (ps56:10): merkha (U+05A5) + qadma/azla (U+05A8) on ONE base letter (no X
    # between) is two co-equal conjunctive servi with no natural order -> one order-less
    # MERKHA_AZLA bang, not a reorderable MERKHA AZLA sequence.
    tail = "X XX" + am.ATNAX + "X XX" + am.METEG + am.SOF_PASUQ
    same = _types_marks("X" + am.MERKHA + am.QADMA + "X" + tail)
    assert pan.MERKHA_AZLA in same
    # the two bare servi are gone -- consumed into the one bang
    assert pan.MERKHA not in same and pan.AZLA not in same


def test_cross_letter_merkha_then_azla_stays_a_sequence():
    # The bang is same-letter only: a genuine cross-letter merkha...azla chain (an X
    # between the two marks -> two letters, meaningful reading order) must NOT fuse.
    tail = "X XX" + am.ATNAX + "X XX" + am.METEG + am.SOF_PASUQ
    cross = _types_marks("X" + am.MERKHA + "X" + am.QADMA + "X" + tail)
    assert pan.MERKHA_AZLA not in cross
    assert pan.MERKHA in cross and pan.AZLA in cross


def test_non_whitelisted_pair_fuses_to_bang():
    # Plan D guard is a WHITELIST: any two adjacent same-letter accents NOT on the
    # whitelist fuse to an a!b bang (type/leaf derived per pair), not just merkha+qadma.
    # munax+merkha is not whitelisted -> MUNAX_MERKHA / "munax!merkha".
    tail = "X XX" + am.ATNAX + "X XX" + am.METEG + am.SOF_PASUQ
    toks = scan_accents("X" + am.MUNAX + am.MERKHA + "X" + tail)
    leaves = [leaf for _t, leaf in toks]
    assert "munax!merkha" in leaves
    assert ("MUNAX_MERKHA", "munax!merkha") in toks
    # the two bare servi are consumed into the one bang
    types = [t for t, _ in toks]
    assert pan.MUNAX not in types and pan.MERKHA not in types
    # and it is unparseable (no grammar terminal for the dynamic bang type)
    parser = build_parser()
    assert (
        parse_tokens(
            parser, scan_verse("t 1:1", "X" + am.MUNAX + am.MERKHA + "X" + tail).tokens
        )
        is None
    )


def test_whitelisted_pairs_not_flagged():
    # The whitelisted same-letter pairs must NOT become a bang: dexi+munax stays a
    # dexi/munax sequence (the lone whitelisted pair that reaches the guard, spared by
    # _WHITELISTED_ADJACENT_PAIRS), and tsinnorit+mahapakh is the metsunnar fusion (a
    # cross-letter pair consumed upstream), not a bang.
    tail = "X XX" + am.ATNAX + "X XX" + am.METEG + am.SOF_PASUQ
    dexi = _types_marks("X" + am.DEXI + am.MUNAX + "X" + tail)
    assert pan.DEXI in dexi and pan.MUNAX in dexi
    assert not any(
        "!" in leaf for _t, leaf in scan_accents("X" + am.DEXI + am.MUNAX + "X" + tail)
    )
    metsun = _types_marks("X" + am.TSINNORIT + "X" + am.MAHAPAKH + "X" + tail)
    assert pan.MAHAPAKH_METSUNNAR in metsun


def test_same_letter_oleh_weyored_fuses_not_banged():
    # Issue wlc-utils#42: MAM stacks oleh-we-yored on ONE base letter (stress word-initial), stored
    # merkha-THEN-ole (e.g. Ps 30:12 לִ֥֫י), where WLC 4.22 writes it cross-letter (ole on
    # the pre-stress letter, yored merkha on the stress letter -- 0 same-letter in WLC).
    # The same-letter merkha+ole must fuse to the one OLEH_WEYORED disjunctive, not fall
    # through to the bang guard as merkha!ole -> NO_PARSE.
    tail = "X XX" + am.ATNAX + "X XX" + am.METEG + am.SOF_PASUQ
    same = _types_marks("X" + am.MERKHA + am.OLE + "X " + tail)
    assert pan.OLEH_WEYORED in same
    assert pan.MERKHA not in same  # the yored merkha is consumed, not a servus
    assert "MERKHA_OLE" not in same  # not banged
    assert not any(
        "!" in leaf for _t, leaf in scan_accents("X" + am.MERKHA + am.OLE + "X " + tail)
    )
    # and the verse parses cleanly
    parser = build_parser()
    toks = scan_verse("test 1:1", "X" + am.MERKHA + am.OLE + "X " + tail).tokens
    assert parse_tokens(parser, toks) is not None
    # the ole-first same-letter order (already handled by the OLE...MERKHA rule) also fuses
    same2 = _types_marks("X" + am.OLE + am.MERKHA + "X " + tail)
    assert pan.OLEH_WEYORED in same2 and pan.MERKHA not in same2


def test_cross_letter_merkha_then_oleh_not_fused():
    # The same-letter merkha+ole fusion is adjacency-only: a merkha servus on one letter
    # followed by an ole (a separate oleh-we-yored) on the NEXT letter (an X between them)
    # must stay a MERKHA servus + OLEH_WEYORED, never collapse into one token.
    tail = "X XX" + am.ATNAX + "X XX" + am.METEG + am.SOF_PASUQ
    cross = _types_marks("X" + am.MERKHA + "X" + am.OLE + "X " + tail)
    assert pan.MERKHA in cross and pan.OLEH_WEYORED in cross


def test_stray_accent_fails_fast_not_swallowed():
    # Plan C fail-fast guard: a prose-only accent (segolta, U+0592) has no poetic rule;
    # rather than let the catch-all swallow it silently, the scanner emits STRAY_ACCENT,
    # which the grammar cannot parse -> the verse becomes a NO_PARSE.
    body = "X" + am.SEGOLTA + "X XX" + am.METEG + am.SOF_PASUQ
    types = _types_marks(body)
    assert pan.STRAY_ACCENT in types
    parser = build_parser()
    toks = scan_verse("test 1:1", body).tokens
    assert parse_tokens(parser, toks) is None


def test_these_verses_parse():
    parser = build_parser()
    for body in (
        r')A71$:75R"Y-HF/)I81Y$]c ):A$E70R05 LO71) HFLAK:02 B.A/(:ACA93T '
        r"R:$F60(I71YM W./B:/DE74REK: 13XA+.F)IYM LO71) (FMF92D "
        r'W./B:/MOW$A71B 11L"CI81YM LO74) YF$F75B00',
    ):
        v = scan_verse("test 1:1", mc_to_marks(body))
        assert parse_tokens(parser, v.tokens) is not None
