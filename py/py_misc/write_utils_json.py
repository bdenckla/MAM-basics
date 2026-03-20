"""Exports write_root_in_json_fmt"""

from pycmn import file_io


def write_root_in_json_fmt(out_path, root):
    """Write root JSON dict in JSON format"""
    file_io.json_dump_to_file_path(root, out_path)
