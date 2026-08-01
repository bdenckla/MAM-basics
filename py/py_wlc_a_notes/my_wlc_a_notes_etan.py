"""Exports top_elem, sub_elem_text, sub_elem."""

import xml.etree.ElementTree as ET


def top_elem(parent_elem, tag):
    """Return a top-level (root) etan"""
    # etan: ET [element] and native [Python data structure]
    return {
        "ET": ET.SubElement(parent_elem, tag),
        "native": {},
        "native-counts": {},
        "stack": [],
    }


def sub_elem_text(io_parent_etan, tag, text):
    """Create a sub-etan and set its text."""
    ET.SubElement(io_parent_etan["ET"], tag).text = text
    stack = [*io_parent_etan["stack"], tag]
    stack_str = ":".join(stack)
    stack_str_unique = _get_unique(io_parent_etan, stack_str)
    native = io_parent_etan["native"]
    assert stack_str_unique not in native
    native[stack_str_unique] = text


def _get_unique(io_parent_etan, stack_str):
    native = io_parent_etan["native"]
    if stack_str not in native:
        return stack_str
    native_counts = io_parent_etan["native-counts"]
    if stack_str not in native_counts:
        native_counts[stack_str] = 1
    native_counts[stack_str] += 1
    count = native_counts[stack_str]
    return f"{stack_str}-{count}"


def sub_elem(io_parent_etan, tag):
    """Create a sub-etan and, for convenience, return it."""
    etan = {
        "ET": ET.SubElement(io_parent_etan["ET"], tag),
        "native": io_parent_etan["native"],
        "native-counts": io_parent_etan["native-counts"],
        "stack": [*io_parent_etan["stack"], tag],
    }
    return etan
