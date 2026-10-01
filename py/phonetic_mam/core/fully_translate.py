def fully_translate(string, dic):
    for c in string:
        assert c in dic
    return "".join(dic[c] for c in string)


def fully_translate_nj(string, dic):  # nj: no join
    for c in string:
        assert c in dic
    return [dic[c] for c in string if dic[c]]
