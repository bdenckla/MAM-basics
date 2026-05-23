"""Find verse locations for exact template stack paths in plain/plus parsed data."""

import json

from mb_cmn import bib_locales as tbn
from mb_cmn import ws_tmpl1 as wtp1
from mb_cmn import ws_tmpl2 as wtp2
from tmpl_survey import stack_path_verbose_payload as spvp

_DOCNOTE_TEMPLATE_SYMBOL = "נוסח"
_DOCNOTE_SYMBOL_BY_SLOT = {
    "1": "נוסח@1",
    "2": "נוסח@2",
}


def add_parser_args(parser):
    parser.add_argument(
        "--find-stack-path",
        help=(
            "Find locations where an exact stack path occurs, e.g. "
            "D/נוסח/נוסח@2/ש. When provided, survey generation is skipped."
        ),
    )
    parser.add_argument(
        "--find-stack-path-dataset",
        choices=("plain", "plus", "both"),
        default="plus",
        help=(
            "Dataset to scan when --find-stack-path or "
            "--find-stack-path-verbose is used. Default: plus."
        ),
    )
    parser.add_argument(
        "--find-stack-path-limit",
        type=int,
        default=10,
        help=(
            "Maximum number of locations to return when --find-stack-path "
            "or --find-stack-path-verbose is used. Default: 10."
        ),
    )
    parser.add_argument(
        "--find-stack-path-verbose",
        metavar="FIND_STACK_PATH_VERBOSE",
        help=(
            "Verbose variant of --find-stack-path. Provide a stack path, and "
            "include each matching subtree as raw JSON and as de-parsed "
            "Wikitext."
        ),
    )


def maybe_handle_cli(parser, args):
    if args.find_stack_path and args.find_stack_path_verbose:
        parser.error(
            "Use either --find-stack-path or --find-stack-path-verbose, not both"
        )
    target_path = args.find_stack_path
    verbose = False
    if args.find_stack_path_verbose:
        target_path = args.find_stack_path_verbose
        verbose = True
    if not target_path:
        return False
    if args.find_stack_path_limit < 1:
        parser.error("--find-stack-path-limit must be >= 1")
    hits = search_stack_path(
        target_path,
        args.find_stack_path_dataset,
        args.find_stack_path_limit,
        verbose=verbose,
    )
    print_results(
        target_path,
        args.find_stack_path_dataset,
        args.find_stack_path_limit,
        hits,
        verbose=verbose,
    )
    return True


def _dataset_folder(dataset_key):
    assert dataset_key in {"plain", "plus"}, dataset_key
    return f"../MAM-parsed/{dataset_key}"


def _dataset_file_paths(dataset_key):
    folder = _dataset_folder(dataset_key)
    paths = []
    for bk24id in tbn.ALL_BK24_IDS:
        osdf24 = tbn.ordered_short_dash_full_24(bk24id)
        paths.append(f"{folder}/{osdf24}.json")
    return paths


def _docnote_child_stack_symbols(parent_subtype, arg_key):
    if parent_subtype != _DOCNOTE_TEMPLATE_SYMBOL:
        return (parent_subtype,)
    slot = str(arg_key)
    assert slot in _DOCNOTE_SYMBOL_BY_SLOT, (
        f"Unexpected נוסח arg slot {slot!r}; expected one of "
        f"{sorted(_DOCNOTE_SYMBOL_BY_SLOT.keys())}"
    )
    return (_DOCNOTE_TEMPLATE_SYMBOL, _DOCNOTE_SYMBOL_BY_SLOT[slot])


def _path_matches(stack, subtype, target_path):
    return f"{'/'.join(stack)}/{subtype}" == target_path


def _verse_key(dataset_key, bscv):
    return (
        dataset_key,
        bscv["bk24na"],
        bscv["sub_bkna"],
        bscv["chnu"],
        bscv["psv_psn"],
    )


def _record_hit_if_match(
    hits,
    hit_lookup,
    seen_verses,
    dataset_key,
    bscv,
    stack,
    subtype,
    target_path,
    limit,
    wtel,
    verbose=False,
):
    if len(hits) >= limit and not verbose:
        return
    if not _path_matches(stack, subtype, target_path):
        return
    key = _verse_key(dataset_key, bscv)
    if key in seen_verses:
        if verbose:
            hit_lookup[key]["matches"].append(
                spvp.build_match_payload(dataset_key, stack, subtype, wtel)
            )
        return
    seen_verses.add(key)
    hit = {
        "dataset": dataset_key,
        "bk24na": bscv["bk24na"],
        "sub_bkna": bscv["sub_bkna"],
        "chnu": bscv["chnu"],
        "psv_psn": bscv["psv_psn"],
    }
    if verbose:
        hit["matches"] = [spvp.build_match_payload(dataset_key, stack, subtype, wtel)]
    hits.append(hit)
    hit_lookup[key] = hit


def _walk_wtel_plain(
    wtel,
    stack,
    target_path,
    hits,
    hit_lookup,
    seen_verses,
    dataset_key,
    bscv,
    limit,
    verbose=False,
):
    if isinstance(wtel, str):
        return
    assert isinstance(wtel, dict)
    if not wtp1.is_template(wtel):
        return
    subtype = wtp1.template_name(wtel)
    _record_hit_if_match(
        hits,
        hit_lookup,
        seen_verses,
        dataset_key,
        bscv,
        stack,
        subtype,
        target_path,
        limit,
        wtel,
        verbose=verbose,
    )
    for arg_idx, arg in enumerate(wtp1.template_arguments(wtel), start=1):
        new_stack = (*stack, *_docnote_child_stack_symbols(subtype, arg_idx))
        for arg_wtel in arg:
            _walk_wtel_plain(
                arg_wtel,
                new_stack,
                target_path,
                hits,
                hit_lookup,
                seen_verses,
                dataset_key,
                bscv,
                limit,
                verbose=verbose,
            )


def _walk_wtel_plus(
    wtel,
    stack,
    target_path,
    hits,
    hit_lookup,
    seen_verses,
    dataset_key,
    bscv,
    limit,
    verbose=False,
):
    if isinstance(wtel, str):
        return
    assert isinstance(wtel, dict)
    if not wtp2.is_template(wtel):
        return
    subtype = wtp2.template_name(wtel)
    _record_hit_if_match(
        hits,
        hit_lookup,
        seen_verses,
        dataset_key,
        bscv,
        stack,
        subtype,
        target_path,
        limit,
        wtel,
        verbose=verbose,
    )
    for param_key in wtp2.template_param_keys(wtel):
        new_stack = (*stack, *_docnote_child_stack_symbols(subtype, param_key))
        for arg_wtel in wtp2.template_param_val(wtel, param_key):
            _walk_wtel_plus(
                arg_wtel,
                new_stack,
                target_path,
                hits,
                hit_lookup,
                seen_verses,
                dataset_key,
                bscv,
                limit,
                verbose=verbose,
            )


def _find_stack_path_in_dataset(target_path, dataset_key, limit, verbose=False):
    hits = []
    hit_lookup = {}
    seen_verses = set()
    walker = _walk_wtel_plain if dataset_key == "plain" else _walk_wtel_plus
    for in_path in _dataset_file_paths(dataset_key):
        if len(hits) >= limit:
            break
        with open(in_path, encoding="utf-8") as json_in_fp:
            bk24_contents = json.load(json_in_fp)
        for book39 in bk24_contents["book39s"]:
            if len(hits) >= limit:
                break
            bk24na = book39["book24_name"]
            sub_bkna = book39["sub_book_name"]
            for chnu, chapter in book39["chapters"].items():
                if len(hits) >= limit:
                    break
                for psv_psn, psv_contents in chapter.items():
                    if len(hits) >= limit:
                        break
                    bscv = {
                        "bk24na": bk24na,
                        "sub_bkna": sub_bkna,
                        "chnu": chnu,
                        "psv_psn": psv_psn,
                    }
                    for col, wtseq in zip(("C", "D", "E"), psv_contents):
                        if len(hits) >= limit and not verbose:
                            break
                        for wtel in wtseq:
                            if len(hits) >= limit and not verbose:
                                break
                            walker(
                                wtel,
                                (col,),
                                target_path,
                                hits,
                                hit_lookup,
                                seen_verses,
                                dataset_key,
                                bscv,
                                limit,
                                verbose=verbose,
                            )
    return hits


def search_stack_path(target_path, dataset_key, limit, verbose=False):
    if dataset_key == "both":
        datasets = ("plain", "plus")
    else:
        datasets = (dataset_key,)
    hits = []
    for name in datasets:
        remaining = limit - len(hits)
        if remaining <= 0:
            break
        hits.extend(
            _find_stack_path_in_dataset(
                target_path,
                name,
                remaining,
                verbose=verbose,
            )
        )
    return hits


def print_results(target_path, dataset_key, limit, hits, verbose=False):
    print(
        json.dumps(
            {
                "mode": "find-stack-path-verbose" if verbose else "find-stack-path",
                "target_path": target_path,
                "dataset": dataset_key,
                "limit": limit,
                "count": len(hits),
                "hits": hits,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
