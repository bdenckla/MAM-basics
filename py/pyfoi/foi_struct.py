import collections


def record_fois_for_1_verse(all_fois, bcvt, verse_fois):
    """Record verse_fois into all_fois."""
    # The var "target" usually consists of a start and stop.
    # These are are word indexes.
    # The stop index is of the classic "one past last" variety.
    for foi_path, *target in verse_fois:
        target2 = target[0] if len(target) == 1 else target
        all_fois[foi_path].append(_make(bcvt, target2))


def record_fois_for_1_bk(all_fois, out_for_1_bk):
    """Record out_for_1_bk into all_fois."""
    for bcvt, fois_for_this_verse in out_for_1_bk.items():
        record_fois_for_1_verse(all_fois, bcvt, fois_for_this_verse)


def make_qtarget(target_proper, qualifier):
    """Make a qualified target, for use in a foi_struct."""
    assert isinstance(qualifier, dict), qualifier
    return {"_foi_qtar_proper": target_proper, "_foi_qtar_qual": qualifier}


def qtar_proper(qtar):
    """Return the target proper of a qualified target."""
    return qtar["_foi_qtar_proper"]


def qtar_qual(qtar):
    """Return the qualifier of a qualified target."""
    return qtar["_foi_qtar_qual"]


def make_empty_all_fois():
    """Make an empty all_fois structure"""
    return collections.defaultdict(list)


def get_bcvt(foi_struct):
    """Get the bcv part of the given foi_struct."""
    return foi_struct["_foi_struct_bcvt"]


def get_target(foi_struct):
    """
    Get the target part of the given foi_struct.
    The target is expected to be one of the following four things:
        a pair of word indexes (start and stop)
        some other kind of tuple (assumed to be an htseq)
        a string (which will be turned into a singleton tuple)
        a qualified target (defined elsewhere)
    """
    target = foi_struct["_foi_struct_target"]
    if _is_a_list_of_2_ints(target):
        return "foi-target-type-word-index-range", target
    if isinstance(target, tuple):
        return "foi-target-type-htseq", target
    if isinstance(target, str):
        return "foi-target-type-htseq", (target,)
    if _is_a_qualified_target(target):
        return "foi-target-type-htseq-qual", target
    assert False, target


def _make(bcvt, target):
    return {"_foi_struct_bcvt": bcvt, "_foi_struct_target": target}


def _is_a_qualified_target(obj):
    return isinstance(obj, dict) and obj.keys() == _KOQT


def _keys_of_qualified_target():
    dummy_qual = {"dummy-qual-key": "dummy-qual-val"}
    example = make_qtarget("dummy-target-proper", dummy_qual)
    return example.keys()


_KOQT = _keys_of_qualified_target()


def _is_a_list_of_2_ints(obj):
    return (
        isinstance(obj, list)
        and len(obj) == 2
        and isinstance(obj[0], int)
        and isinstance(obj[1], int)
    )
