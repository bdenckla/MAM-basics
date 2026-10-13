"""Read MAM-simple JSON shapes without choosing a Scripture projection."""

import json

_PARASHAH_TYPES = {"spi-pe2", "spi-pe3", "spi-samekh2", "spi-samekh3"}


def attributes(node):
    """Return the string fields beside type and contents, checking the node shape."""
    if not isinstance(node, dict) or not isinstance(node.get("type"), str):
        raise ValueError(f"MAM-simple node has no string type: {node!r}")
    attrs = {
        key: value for key, value in node.items() if key not in {"type", "contents"}
    }
    if any(not isinstance(value, str) for value in attrs.values()):
        raise ValueError(f"Non-string fields in MAM-simple {node['type']}: {attrs}")
    if "text" in node and "contents" in node:
        raise ValueError(f"MAM-simple {node['type']} has both text and contents")
    if "contents" in node and not isinstance(node["contents"], list):
        raise ValueError(f"MAM-simple {node['type']} contents is not an array")
    return attrs


def children(node):
    """Return a node's children after checking its storage shape."""
    attributes(node)
    return node.get("contents", [])


def find_child(node, kind):
    """Find a direct child by its explicit type, rejecting duplicates."""
    matches = [child for child in children(node) if child["type"] == kind]
    if len(matches) > 1:
        raise ValueError(f"Multiple {kind} children in MAM-simple {node['type']}")
    return matches[0] if matches else None


def read_book_group(path):
    """Read the documented four-field envelope as a structural book24 node."""
    with open(path, encoding="utf-8") as source:
        root = json.load(source)
    if not isinstance(root, dict) or set(root) != {
        "provenance",
        "consumer_notice",
        "versification-tradition",
        "contents",
    }:
        raise ValueError(f"Unexpected MAM-simple JSON envelope in {path}")
    if not isinstance(root["provenance"], str) or not isinstance(
        root["consumer_notice"], dict
    ):
        raise ValueError(f"Unexpected MAM-simple metadata in {path}")
    node = {
        "type": "book24",
        "versification-tradition": root["versification-tradition"],
        "contents": root["contents"],
    }
    attributes(node)
    return node


def structural_children(node, kind):
    """Read one hierarchy level, allowing only its children and free parashah markers."""
    for child in children(node):
        attrs = attributes(child)
        if child["type"] == kind:
            yield child
        elif child["type"] in _PARASHAH_TYPES:
            if attrs or children(child):
                raise ValueError(f"Unexpected free parashah marker: {child}")
        else:
            raise ValueError(f"Unhandled {node['type']} child {child['type']}")


def verses(root):
    """Yield every verse through the explicit book24/book39/chapter hierarchy."""
    for book in structural_children(root, "book39"):
        for chapter in structural_children(book, "chapter"):
            yield from structural_children(chapter, "verse")
