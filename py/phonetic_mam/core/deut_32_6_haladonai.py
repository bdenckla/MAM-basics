POINTED_KETIV_AS_STR = "הַ לְיְהֹוָה֙"
POINTED_KETIV_AS_LIST = POINTED_KETIV_AS_STR.split(" ")
POINTED_QERE = POINTED_KETIV_AS_STR.replace(" ", "")


def join_haladonai(word_strs):
    if len(word_strs) < 2:
        return word_strs
    first_two_as_list = word_strs[:2]
    if first_two_as_list == POINTED_KETIV_AS_LIST:
        first_two_as_str = " ".join(word_strs[:2])
        word_strs = [first_two_as_str, *word_strs[2:]]
    return word_strs
