import re


def my_re_split(patt_for_split, string):
    s_split = re.split(patt_for_split, string)
    if s_split[-1] == "":
        s_split = s_split[:-1]
    if s_split[0] == "":
        s_split = s_split[1:]
    return s_split
