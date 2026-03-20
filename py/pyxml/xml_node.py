"""Exports to_dic"""

import re


def to_dic(node):
    """Turn an ElementTree node into a dict"""
    dic = {}
    for child in node:
        child_result = to_dic(child)
        if child_result is None and child.tag == "note":
            # empty note elements are common
            # and we want to ignore them
            continue
        if child.tag in dic:
            if not isinstance(dic[child.tag], list):
                dic[child.tag] = [dic[child.tag]]
            dic[child.tag].append(child_result)
        else:
            dic[child.tag] = child_result
    if dic:
        return dic
    if isinstance(node.text, str):
        node_text = node.text
        node_text = re.sub(r"[\n\t ]+", " ", node_text)
        return node_text.strip()
    assert node.text is None
    return None
