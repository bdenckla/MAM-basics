def kqparse(parsed):
    kqparsed = {"header": parsed["header"], "verses": []}
    stacks = _STACKS_INIT
    for verse in parsed["verses"]:
        bcv = verse["bcv"]
        kqverse = {"bcv": bcv, "vels": []}
        kqparsed["verses"].append(kqverse)
        assert _stacks_are_clear(stacks)
        for velsod in verse["vels"]:
            word = _word(velsod)
            if word and word.startswith("**"):
                _stacks_push_q(stacks, velsod)
                continue
            if word and word.startswith("*"):
                if _stacks_has_qere(stacks):
                    _stacks_transfer(kqverse["vels"], stacks)
                _stacks_push_k(stacks, velsod)
                continue
            _stacks_transfer(kqverse["vels"], stacks)
            kqverse["vels"].append(velsod)
        _stacks_transfer(kqverse["vels"], stacks)
    return kqparsed


_STACKS_INIT = {"ketiv": [], "qere": []}


def _stacks_clear(io_stacks):
    io_stacks["ketiv"] = []
    io_stacks["qere"] = []


def _stacks_are_clear(stacks):
    return not stacks["ketiv"] and not stacks["qere"]


def _stacks_has_qere(stacks):
    return stacks["qere"]


def _stacks_push_k(io_stacks, velsod):
    io_stacks["ketiv"].append(velsod)


def _stacks_push_q(io_stacks, velsod):
    io_stacks["qere"].append(velsod)


def _stacks_transfer(io_kqvels, io_stacks):
    ketiv_stack = io_stacks["ketiv"]
    qere_stack = io_stacks["qere"]
    if not ketiv_stack and not qere_stack:
        return
    assert ketiv_stack and qere_stack
    if _two_sam_18_20(ketiv_stack, qere_stack):
        kqvel0 = _make_kqvel([ketiv_stack[0]], [qere_stack[0]])
        kqvel1 = _make_kqvel([ketiv_stack[1]], [qere_stack[1]])
        io_kqvels.extend([kqvel0, kqvel1])
    else:
        kqvel = _make_kqvel(ketiv_stack, qere_stack)
        io_kqvels.append(kqvel)
    _stacks_clear(io_stacks)


def _two_sam_18_20(ketiv, qere):
    return len(ketiv) == 2 and ketiv[1] == "*kk"


def _make_kqvel(ketiv, qere):
    ketiv_ie = _remove(ketiv, "*kk")  # ie: implicit empties
    qere_ie = _remove(qere, "**qq")  # ie: implicit empties
    ketiv_ie_ns = list(map(_strip_leading_star, ketiv_ie))  # ns: no stars
    qere_ie_ns = list(map(_strip_leading_starstar, qere_ie))  # ns: nostars
    return {"kq": (ketiv_ie_ns, qere_ie_ns)}


def _remove(the_list, unwanted_elem):
    out = []
    for elem in the_list:
        if elem == unwanted_elem:
            continue
        out.append(elem)
    return out


def _strip_leading_star(velsod):
    if isinstance(velsod, str):
        return _strip_leading_star_from_str(velsod)
    return {**velsod, "word": _strip_leading_star_from_str(velsod["word"])}


def _strip_leading_starstar(velsod):
    if isinstance(velsod, str):
        return _strip_leading_starstar_from_str(velsod)
    return {**velsod, "word": _strip_leading_starstar_from_str(velsod["word"])}


def _strip_leading_star_from_str(string):
    assert string.startswith("*")
    return string.removeprefix("*")


def _strip_leading_starstar_from_str(string):
    assert string.startswith("**")
    return string.removeprefix("**")


def _word(velsod):
    if isinstance(velsod, str):
        return velsod
    return velsod.get("word")
