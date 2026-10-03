"""Lint: the parser-stage keys that plus must not hold are the keys the parser admits.

``verify_mp.parser_stage._validate_no_parser_stage_encoding`` refuses any dict in plus with a
key in ``PARSER_STAGE_NODE_KEYS``.  ``node_type_and_subtype`` admits a parser-stage node only
through ``ws_tmpl1.is_template``, which is ``dic_is_template``, and ``ws_tmpl1.is_abtag``, so
the keys those two predicates test, read here from their source, must be exactly that set.
A missing function or a second ``return`` fails rather than reading as agreement.
"""

import ast

from mb_cmn import paths
from verify_mp import parser_stage


def _function(rel, name):
    tree = ast.parse((paths.repo_root() / rel).read_text(encoding="utf-8"))
    found = [
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == name
    ]
    assert len(found) == 1, f"{rel} defines {name} {len(found)} times"
    return found[0]


def _return_string_constants(function):
    returns = [node for node in ast.walk(function) if isinstance(node, ast.Return)]
    assert len(returns) == 1, f"{function.name} has {len(returns)} return statements"
    return {
        node.value
        for node in ast.walk(returns[0])
        if isinstance(node, ast.Constant) and isinstance(node.value, str)
    }


def test_parser_stage_node_keys_are_the_keys_the_parser_admits():
    classifier = _function("py/verify_mp/parser_stage.py", "node_type_and_subtype")
    called = []
    for statement in classifier.body:
        if isinstance(statement, ast.If):
            assert isinstance(statement.test, ast.Call), ast.unparse(statement.test)
            called.append(ast.unparse(statement.test.func))
    assert called == ["wtp1.is_template", "wtp1.is_abtag"], called
    keys = set()
    for name in ("dic_is_template", "is_abtag"):
        keys |= _return_string_constants(_function("py/mb_cmn/ws_tmpl1.py", name))
    assert keys == {"tmpl", "stmpl", "custom_tag"}, keys
    assert keys == parser_stage.PARSER_STAGE_NODE_KEYS
