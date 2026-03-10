""" Exports main """

import xml.etree.ElementTree as ET
from pycmn import file_io


def _read_bk24s():
    xml_path = "../MAM-OSIS/MAPM-orig/MAPM.xml"
    tree = ET.parse(xml_path)
    root = tree.getroot()
    ons = {"ons": _ONS}
    level3_divs = root.findall("./ons:osisText/ons:div/ons:div/ons:div", ons)
    assert level3_divs
    return level3_divs


def _write_bk24(root):
    attrib_name_for_stem = {"book": "osisID", "bookGroup": "scope"}
    anfs = attrib_name_for_stem[root.attrib["type"]]
    stem = root.attrib[anfs]
    out_path = f"../MAM-OSIS/MAPM-orig-24/{stem}.xml"
    xml_elementtree = ET.ElementTree(root)
    ET.indent(xml_elementtree)
    ET.register_namespace("", _ONS)
    file_io.with_tmp_openw(out_path, {}, _write_callback, xml_elementtree)


def _write_callback(xml_elementtree, out_fp):
    xml_elementtree.write(out_fp, encoding="unicode", xml_declaration=True)
    out_fp.write("\n")


def main():
    """Split up MAPM.xml into 24 books."""
    bk24s = _read_bk24s()
    for bk24 in bk24s:
        _write_bk24(bk24)


_ONS = "http://www.bibletechnologies.net/2003/OSIS/namespace"


if __name__ == "__main__":
    main()
