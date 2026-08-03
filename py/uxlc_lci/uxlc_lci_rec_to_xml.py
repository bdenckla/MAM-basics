"""Exports get_etree"""

import xml.etree.ElementTree as ET


def get_etree(lci_recs_dot_json):
    """Get an ElementTree from contents of lci_recs.json."""
    root = ET.Element("lcindex")
    header_elem = ET.SubElement(root, "header")
    body = ET.SubElement(root, "body")
    #
    header_dic = lci_recs_dot_json["header"]
    _fill_elem_with_dict(header_elem, header_dic)
    #
    analysis_dic = {"type-counts": {}, "val-reports": {}}
    for lci_rec_f in lci_recs_dot_json["body"]:
        # 'f' suffix means flat, i.e. this is not a real lci_rec
        lci_rec_f_elem = ET.SubElement(body, "lci_rec")
        _fill_elem_with_dict(lci_rec_f_elem, lci_rec_f)
        _analyze(analysis_dic, lci_rec_f)
    #
    analysis_elem = ET.SubElement(header_elem, "column-analysis")
    _fill_col_analysis_elem(analysis_elem, analysis_dic)
    #
    tree = ET.ElementTree(root)
    ET.indent(tree)
    return tree


def _analyze(accum, lci_rec_f):
    for key, val in lci_rec_f.items():
        if isinstance(val, str):
            _record(accum, key, val, "string")
        elif isinstance(val, int):
            _record(accum, key, val, "integer")
        else:
            _record(accum, key, val, "none")
    return accum


def _record(accum, key, val, type_str):
    _increment(accum["type-counts"], key, type_str)
    if key == "bkid":
        _increment(accum["val-reports"], key, val)


def _increment(atc, key, val):
    # avr: accum['type-counts']
    if key not in atc:
        atc[key] = {}
    if val not in atc[key]:
        atc[key][val] = 0
    atc[key][val] += 1


def _fill_elem_with_dict(elem, dic):
    for key, val in dic.items():
        subelem = ET.SubElement(elem, key)
        if isinstance(val, dict):
            _fill_elem_with_dict(subelem, val)
        elif isinstance(val, str):
            subelem.text = val
        elif isinstance(val, int):
            subelem.text = str(val)
        else:
            assert val is None


def _fill_col_analysis_elem(ca_elem, ca_dic):
    tc_elem = ET.SubElement(ca_elem, "type-counts")
    tc_dic = ca_dic["type-counts"]
    for col_name, col_type_counts in tc_dic.items():
        cai = ET.SubElement(tc_elem, "type-count")
        cai.set("col-name", col_name)
        for type_str, count in col_type_counts.items():
            assert isinstance(type_str, str)
            assert isinstance(count, int)
            cai.set(type_str, str(count))
    bvc_elem = ET.SubElement(ca_elem, "bkid-val-counts")
    bvc_dic = ca_dic["val-reports"]["bkid"]
    for bkid, bkid_count in bvc_dic.items():
        if bkid is None:
            continue
        cai = ET.SubElement(bvc_elem, "bkid-val-count")
        cai.set("bkid", bkid)
        assert isinstance(bkid_count, int)
        cai.set("count", str(bkid_count))
