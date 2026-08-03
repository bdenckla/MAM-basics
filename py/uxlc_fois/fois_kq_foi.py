def init():
    full = {
        "type-counts": _init_helper(int),  # zero
        "exotic-cases-by-type": _init_helper(list),  # []
        "exotic-cases-flat": [],
    }
    del full["exotic-cases-by-type"]["k1q1"]  # k1q1 is not exotic
    return full


def collect_for_verse(fois, bcv, verse):
    state = {"k_stack": [], "q_stack": []}
    for atidx, atom in enumerate(verse):
        assert isinstance(atom, list)
        assert len(atom) >= 2
        assert atom[0] in ("w", "k", "q")
        bcvp = *bcv, atidx + 1
        _collect_for_atom(state, fois, bcvp, atom)
    _record_and_clear(state, fois, bcvp)


def _init_helper(constructor):
    return {
        "k0q1": constructor(),
        "k1q0": constructor(),
        "k1q1": constructor(),
        "k1q2": constructor(),
        "k2q1": constructor(),
        "k2q2": constructor(),
    }


def _quad(state):
    k_stack, q_stack = state["k_stack"], state["q_stack"]
    numk, numq = len(k_stack), len(q_stack)
    return k_stack, q_stack, numk, numq


def _collect_for_atom(state, fois, bcvp, atom):
    if atom[0] == "w":
        _record_and_clear(state, fois, bcvp)
        return
    if atom[0] == "k":
        if state["q_stack"]:
            _record_and_clear(state, fois, bcvp)
        state["k_stack"].append(atom[1])
        return
    if atom[0] == "q":
        state["q_stack"].append(atom[1])
        return
    assert False


def _record_and_clear(state, fois, bcvp):
    k_stack, q_stack, numk, numq = _quad(state)
    if (numk, numq) == (0, 0):
        return
    kq_type = _knqm_str(numk, numq)
    fois["type-counts"][kq_type] += 1
    if (numk, numq) != (1, 1):
        case_dic = _case_dic(state, bcvp)
        fois["exotic-cases-by-type"][kq_type].append(case_dic)
        fois["exotic-cases-flat"].append(case_dic)
    state["k_stack"] = []
    state["q_stack"] = []


def _case_dic(state, bcvp):
    k_stack, q_stack, numk, numq = _quad(state)
    return {
        "knqm": _knqm_str(numk, numq),
        "bcvp": _bcvp_str(bcvp),
        "k1": _my_get(k_stack, 0),
        "k2": _my_get(k_stack, 1),
        "q1": _my_get(q_stack, 0),
        "q2": _my_get(q_stack, 1),
    }


def _my_get(the_list, the_idx):
    return the_list[the_idx] if len(the_list) > the_idx else None


def _knqm_str(numk, numq):
    return f"k{numk}q{numq}"


def _bcvp_str(bcvp):
    bkid, chnu, vrnu, atnu = bcvp
    return f"{bkid} {chnu}:{vrnu}.{atnu}"
