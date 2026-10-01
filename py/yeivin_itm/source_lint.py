"""Reject duplicated numerical claims in Ben's two survey-backed footnotes."""

import ast
from pathlib import Path
import re

FOOTNOTE_MODULES = (
    "my_yeivin_amisc_sec_320_footnotes.py",
    "my_yeivin_amisc_sec_322_footnotes.py",
)
_CLAIM_PREFIXES = ("_CNT_", "_FR_SURPRISE_", "_CONJ_SURPRISE_", "_SLIGHTLY_", "_XAFR1_")


def check_source(source, filename):
    """Lint real source; only citations, pattern names, and Yeivin's estimates stay literal."""
    tree = ast.parse(source)
    allowed_section_refs = set()
    structural_keys = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            structural_keys.update(id(key) for key in node.keys)
        if (
            isinstance(node, ast.Subscript)
            and isinstance(node.value, ast.Attribute)
            and isinstance(node.value.value, ast.Name)
            and node.value.value.id == "sub"
        ):
            allowed_section_refs.add(id(node.slice))
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "hlp"
            and node.func.attr == "rtn"
        ):
            allowed_section_refs.update(id(arg) for arg in node.args)
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id.startswith(
                    _CLAIM_PREFIXES
                ):
                    if not (
                        isinstance(node.value, ast.Call)
                        and isinstance(node.value.func, ast.Name)
                        and node.value.func.id == "claim_text"
                    ):
                        raise ValueError(f"Hard-coded claim {target.id} in {filename}")
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant):
            continue
        if type(node.value) in (int, float) and id(node) not in allowed_section_refs:
            raise ValueError(f"Hard-coded claim number at {filename}:{node.lineno}")
        if not isinstance(node.value, str):
            continue
        if id(node) in structural_keys:
            continue
        value = node.value
        if re.fullmatch(r"@[A-Za-z0-9ḤḥŠš -]+ \d+:\d+", value):
            continue
        if value.startswith("yeivin_itm-huge-ftnt-") and value.endswith(".html"):
            continue
        # These are Yeivin's quoted estimates, not Ben's measured figures.
        value = value.replace("this estimate of 90%", "this estimate")
        value = value.replace("this estimate of 200", "this estimate")
        value = re.sub(r"\b(?:X?AFR|FR)[1-4]\b", "pattern", value)
        if re.search(r"\d", value) or "only a single $gaya" in value:
            raise ValueError(f"Hard-coded claim text at {filename}:{node.lineno}")


def check():
    """Lint both maintained source modules without importing them."""
    content = Path(__file__).with_name("content")
    for filename in FOOTNOTE_MODULES:
        check_source((content / filename).read_text(encoding="utf-8"), filename)
