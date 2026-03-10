""" Exports write_root_in_xml_fmt """

import xml.etree.ElementTree as ET
from pycmn import file_io


def write_root_in_xml_fmt(out_path, root):
    """Write root XML node in XML format"""
    xml_elementtree = ET.ElementTree(root)
    ET.indent(xml_elementtree)
    file_io.with_tmp_openw(out_path, {}, _write_callback, xml_elementtree)


def _write_callback(xml_elementtree, out_fp):
    xml_elementtree.write(out_fp, encoding="unicode")
    out_fp.write("\n")
