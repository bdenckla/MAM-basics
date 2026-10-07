"""Reject duplicated numerical claims in Ben's two survey-backed footnotes, and
require their quoted forms to be the ones quoted_forms.py checks."""

import ast
from collections import Counter
from pathlib import Path
import re

from yeivin_itm import quoted_forms

FOOTNOTE_MODULES = (
    "my_yeivin_amisc_sec_320_footnotes.py",
    "my_yeivin_amisc_sec_322_footnotes.py",
)
_CLAIM_PREFIXES = ("_CNT_", "_FR_SURPRISE_", "_CONJ_SURPRISE_", "_SLIGHTLY_", "_XAFR1_")
# The helpers besides hlp.hboloc that give a Hebrew form a location. The footnotes use
# none of them, so a form they quoted would escape quoted_forms.py's check.
_OTHER_LOCATED = frozenset(
    {
        ("hlp", "lhbo"),
        ("hlp", "some_hi"),
        ("hlp", "lns"),
        ("hlp", "hbo_loc_ms"),
        ("sub", "irrelevant_ketiv"),
    }
)


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


def quoted_calls(source, filename, fk_6_22):
    """The (module, reference, form) of each hlp.hboloc call of a footnote module.

    ``fk_6_22`` is substitutions.FK_6_22, which one call indexes. Any other helper of
    _OTHER_LOCATED raises, as does an hboloc argument that is not a literal.
    """
    found = []
    for node in ast.walk(ast.parse(source)):
        if not (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
        ):
            continue
        helper = (node.func.value.id, node.func.attr)
        if helper in _OTHER_LOCATED:
            raise ValueError(
                f"{filename}:{node.lineno}: {'.'.join(helper)} quotes a located form "
                "that quoted_forms.py does not check"
            )
        if helper == ("hlp", "hboloc"):
            form, sloc = (_literal(arg, fk_6_22, filename) for arg in node.args)
            found.append((filename, sloc, form))
    return found


def _literal(node, fk_6_22, filename):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if (
        isinstance(node, ast.Subscript)
        and isinstance(node.value, ast.Attribute)
        and isinstance(node.value.value, ast.Name)
        and (node.value.value.id, node.value.attr) == ("sub", "FK_6_22")
    ):
        return fk_6_22[ast.literal_eval(node.slice)]
    raise ValueError(
        f"{filename}:{node.lineno}: an hboloc argument that is not literal"
    )


def _fk_6_22():
    """substitutions.FK_6_22, by literal evaluation of its assignment."""
    path = Path(__file__).with_name("substitutions.py")
    for node in ast.parse(path.read_text(encoding="utf-8")).body:
        if isinstance(node, ast.Assign) and [
            target.id for target in node.targets if isinstance(target, ast.Name)
        ] == ["FK_6_22"]:
            return ast.literal_eval(node.value)
    raise ValueError(f"{path} has no FK_6_22")


def check():
    """Lint both maintained source modules without importing them."""
    content = Path(__file__).with_name("content")
    fk_6_22 = _fk_6_22()
    calls = Counter()
    for filename in FOOTNOTE_MODULES:
        source = (content / filename).read_text(encoding="utf-8")
        check_source(source, filename)
        calls.update(quoted_calls(source, filename, fk_6_22))
    declared = Counter(
        (quoted.module, quoted.sloc, quoted.form)
        for quoted in quoted_forms.QUOTED_FORMS
    )
    if calls != declared:
        raise ValueError(
            "The footnotes' quoted forms differ from quoted_forms.QUOTED_FORMS: "
            f"only in the footnotes {sorted(calls - declared)}, only in the table "
            f"{sorted(declared - calls)}"
        )
