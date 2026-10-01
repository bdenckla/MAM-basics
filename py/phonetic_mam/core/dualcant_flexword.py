import mb_cmn.my_utils as my_utils


def dispatch_on_flexword(fn_simple, fn_multi, fn_qamats, flexword):
    assert isinstance(flexword, dict)
    key, val = my_utils.first_and_only(list(flexword.items()))
    if key == "word-simple":
        return fn_simple(val)
    if key == "word-multi":
        assert len(val) == 2
        return fn_multi(val)
    if key == "dcargs-qamats":
        assert len(val) == 2
        return fn_qamats(val)
    assert False, flexword
