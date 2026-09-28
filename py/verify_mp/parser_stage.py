"""Validate transient parser-stage data before MAM-parsed-plus conversion."""

import collections
import json

from mb_cmn import kq_special_templates as kqst
from mb_cmn.my_utils import first_and_only_and_str
from mb_cmn import paths
from mb_cmn import parser_stage_template_schema
from mb_cmn import ws_tmpl1 as wtp1
from mb_cmn import ws_tmpl_named_params as wtnp
from tmpl_survey import column_d_0_process_all_mpasuq_calls as cdp
from tmpl_survey import column_d_0_store_the_mpasuq_call as cds
from tmpl_survey import column_d_0_store_the_mpasuq_call_plus as cds_plus
from tmpl_survey import nesting_normal_form

_EXPANDED_STACK_GRAMMAR_LOCK_PATH = (
    paths.repo_root() / "py/verify_mp/expanded_stack_grammar_parser_stage.lock.json"
)
_EXPECTED_ARGC = {
    "כו״ק": 2,
    "מ:אות מנוקדת": 1,
    kqst.UNIFIED_SPECIAL_KQ_TEMPLATE_NAME: (2, 3, 4, 5, 6),
}
_MID_VERSE_PARAGRAPH_TEMPLATES = frozenset({"סס", "פפ", "פפפ"})
_RANK_MAPS = {
    "C": nesting_normal_form.build_rank_map(
        nesting_normal_form.RANK_GROUPS_FOR_PLAIN_C
    ),
    "D": nesting_normal_form.build_rank_map(
        nesting_normal_form.RANK_GROUPS_FOR_PLAIN_D
    ),
    "E": nesting_normal_form.build_rank_map(
        nesting_normal_form.RANK_GROUPS_FOR_PLAIN_E
    ),
}


def node_type_and_subtype(node):
    """Validate and classify one non-string parser-stage node."""
    if wtp1.is_template(node):
        template_name = parser_stage_template_schema.validate_parser_stage_template(
            node
        )
        if kqst.is_special_kq_template_name(template_name):
            assert kqst.is_unified_special_kq_template_name(
                template_name
            ), template_name
        return "tmpl", template_name
    if wtp1.is_abtag(node):
        return (
            "custom_tag",
            parser_stage_template_schema.validate_parser_stage_custom_tag(node),
        )
    raise TypeError(f"unclassified current parser-stage node: {node!r}")


def validate_template_arg_count(template_name, arg_count):
    """Validate the constrained argument counts in parser-stage templates."""
    expected = _EXPECTED_ARGC.get(template_name)
    if isinstance(expected, int):
        expected = (expected,)
    assert expected is None or arg_count in expected


def child_stack_symbols(parent_template_name, argument_index):
    """Return the stack symbols contributed by one template argument."""
    _ = argument_index
    return (parent_template_name,)


def _validate_special_kq(template, template_name):
    if template_name != kqst.UNIFIED_SPECIAL_KQ_TEMPLATE_NAME:
        return
    params = wtnp.get_tmpl_params_ss(wtp1.template_arguments(template))
    ketiv = params["1"]
    qere = params["2"]
    sug = first_and_only_and_str(params["סוג"])
    assert isinstance(ketiv, list) and ketiv
    assert isinstance(qere, list) and qere
    kqst.canonical_special_kq_type_from_name_and_sug(template_name, sug)


def _validate_mid_verse_paragraph_argument(template, template_name):
    if template_name not in _MID_VERSE_PARAGRAPH_TEMPLATES:
        return
    arguments = wtp1.template_arguments(template)
    if arguments:
        assert arguments == [["פסקא באמצע פסוק"]]


def _stack_rest(stack):
    return "/".join(stack)


def _validate_node(stack_counts, stack, node, *, nested=False):
    if isinstance(node, str):
        return
    assert isinstance(node, dict)
    node_type, node_subtype = node_type_and_subtype(node)
    if nested:
        assert node_type == "tmpl"
    if node_type != "tmpl":
        return
    _validate_special_kq(node, node_subtype)
    _validate_mid_verse_paragraph_argument(node, node_subtype)
    stack_counts[(node_subtype, _stack_rest(stack))] += 1
    arguments = wtp1.template_arguments(node)
    validate_template_arg_count(node_subtype, len(arguments))
    for argument_index, argument in enumerate(arguments, start=1):
        child_stack = *stack, *child_stack_symbols(node_subtype, argument_index)
        for child in argument:
            _validate_node(stack_counts, child_stack, child, nested=True)


def _validate_book39(book39, stack_counts, mpasuq_calls):
    assert set(book39) == {"book24_name", "sub_book_name", "chapters"}
    book24_name = book39["book24_name"]
    sub_book_name = book39["sub_book_name"]
    chapters = book39["chapters"]
    assert isinstance(book24_name, str)
    assert sub_book_name is None or isinstance(sub_book_name, str)
    assert isinstance(chapters, dict)
    for chapter_number, chapter in chapters.items():
        assert isinstance(chapter_number, str)
        assert isinstance(chapter, dict) and chapter
        pseudo_verse_numbers = tuple(chapter)
        assert pseudo_verse_numbers[0] == "0"
        assert pseudo_verse_numbers[-1] == "תתת"
        for pseudo_verse_number, columns in chapter.items():
            assert isinstance(pseudo_verse_number, str)
            assert pseudo_verse_number in ("0", "תתת") or pseudo_verse_number.isdigit()
            assert isinstance(columns, (list, tuple)) and len(columns) == 3
            bscv = book24_name, sub_book_name, chapter_number, pseudo_verse_number
            for column_letter, column in zip(("C", "D", "E"), columns):
                assert isinstance(column, (list, tuple))
                for node in column:
                    _validate_node(stack_counts, (column_letter,), node)
            cds.store_the_mpasuq_call(mpasuq_calls, bscv, columns[1])


def _validate_header(header, book39s):
    assert set(header) == {"book24_name", "sub_book_names", "chapter_counts"}
    assert isinstance(header["book24_name"], str)
    assert isinstance(header["sub_book_names"], list)
    assert isinstance(header["chapter_counts"], list)
    assert all(book39["book24_name"] == header["book24_name"] for book39 in book39s)
    expected_sub_book_names = [
        book39["sub_book_name"]
        for book39 in book39s
        if book39["sub_book_name"] is not None
    ]
    assert header["sub_book_names"] == expected_sub_book_names
    assert len(header["chapter_counts"]) == len(book39s)
    for chapter_count, book39 in zip(header["chapter_counts"], book39s):
        assert set(chapter_count) == {"sub_book_name", "chapter_count"}
        assert chapter_count["sub_book_name"] == book39["sub_book_name"]
        assert chapter_count["chapter_count"] == len(book39["chapters"])


def _validate_normal_form(stack_counts):
    for column_letter, rank_map in _RANK_MAPS.items():
        column_counts = {
            key: count
            for key, count in stack_counts.items()
            if key[1].split("/", maxsplit=1)[0] == column_letter
        }
        nesting_normal_form.assert_stack_counts_in_normal_form(
            column_counts,
            dataset_name=f"parser stage ({column_letter} column)",
            rank_map=rank_map,
        )


def _validate_expanded_stack_grammar(stack_counts):
    with _EXPANDED_STACK_GRAMMAR_LOCK_PATH.open(encoding="utf-8") as fp:
        grammar = json.load(fp)
    nesting_normal_form.assert_stack_counts_follow_expanded_grammar(
        stack_counts,
        grammar,
        dataset_name="parser stage",
    )


def validate(section):
    """Validate one transient book24 group and return relationship data."""
    assert set(section) == {"header", "book39s"}
    book39s = section["book39s"]
    assert isinstance(book39s, list) and book39s
    _validate_header(section["header"], book39s)
    stack_counts = collections.defaultdict(int)
    mpasuq_calls = []
    for book39 in book39s:
        _validate_book39(book39, stack_counts, mpasuq_calls)
    _validate_normal_form(stack_counts)
    _validate_expanded_stack_grammar(stack_counts)
    return {
        "mpasuq": cdp.process_all_mpasuq_calls(mpasuq_calls),
        "stack_counts": stack_counts,
    }


def _validate_no_parser_stage_encoding(node):
    if isinstance(node, dict):
        assert "stmpl" not in node
        for value in node.values():
            _validate_no_parser_stage_encoding(value)
    elif isinstance(node, list):
        for item in node:
            _validate_no_parser_stage_encoding(item)


def _validate_plus_structure_and_collect_mpasuq(parser_stage_section, plus_section):
    mpasuq_calls = []
    parser_stage_book39s = parser_stage_section["book39s"]
    plus_book39s = plus_section["book39s"]
    assert len(plus_book39s) == len(parser_stage_book39s)
    for parser_stage_book39, plus_book39 in zip(parser_stage_book39s, plus_book39s):
        assert plus_book39["book24_name"] == parser_stage_book39["book24_name"]
        assert plus_book39["sub_book_name"] == parser_stage_book39["sub_book_name"]
        parser_stage_chapters = parser_stage_book39["chapters"]
        plus_chapters = plus_book39["chapters"]
        assert tuple(plus_chapters) == tuple(parser_stage_chapters)
        book24_name = plus_book39["book24_name"]
        sub_book_name = plus_book39["sub_book_name"]
        for chapter_number, chapter in plus_chapters.items():
            expected_verses = tuple(
                number
                for number in parser_stage_chapters[chapter_number]
                if number not in ("0", "תתת")
            )
            assert tuple(chapter) == expected_verses
            for verse_number, columns in chapter.items():
                assert verse_number not in ("0", "תתת")
                assert isinstance(columns, (list, tuple)) and len(columns) == 3
                _validate_no_parser_stage_encoding(columns)
                bscv = book24_name, sub_book_name, chapter_number, verse_number
                cds_plus.store_the_mpasuq_call(mpasuq_calls, bscv, columns[1])
    return cdp.process_all_mpasuq_calls(mpasuq_calls)


def validate_plus_conversion(
    parser_stage_section, parser_stage_validation, plus_section
):
    """Validate retained raw-to-plus relationships before either value is written."""
    plus_mpasuq = _validate_plus_structure_and_collect_mpasuq(
        parser_stage_section, plus_section
    )
    assert plus_mpasuq == parser_stage_validation["mpasuq"]
