"""Exports write_root_in_xml_fmt"""

import xml.etree.ElementTree as ET
from mb_cmn import file_io
from mb_cmn import provenance


def write_root_in_xml_fmt(out_path, root, generator_file=None):
    """Write root XML node in XML format"""
    xml_elementtree = ET.ElementTree(root)
    ET.indent(xml_elementtree)
    file_io.with_tmp_openw(
        out_path, {}, _write_callback, xml_elementtree, generator_file
    )


def _write_callback(xml_elementtree, generator_file, out_fp):
    if generator_file is not None:
        out_fp.write(f"<!-- {provenance.generated_by_text(generator_file)} -->\n")
    xml_elementtree.write(out_fp, encoding="unicode")
    out_fp.write("\n")
