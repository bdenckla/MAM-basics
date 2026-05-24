"""Find verse locations for exact template stack paths in plain/plus parsed data."""

import json
import sys

from mb_cmn import bib_locales as tbn
from mb_cmn import ws_tmpl1 as wtp1
from mb_cmn import ws_tmpl2 as wtp2
from tmpl_survey import stack_path_verbose_payload as spvp


def add_parser_args(parser):
    parser.add_argument(
        "--find-stack-path",
        help=(
            "Find locations where an exact stack path occurs, e.g. "
            "D/נוסח/ש. "
            "When provided, survey generation is skipped."
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
            "Variant of --find-stack-path that includes path-root context. "
            "Each hit includes the same fields as non-verbose, plus "
            "path_root_wikitext and path_root_json."
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


def _child_stack_symbols(parent_subtype, arg_key):
    _ = arg_key
    return (parent_subtype,)


def _path_matches(stack, subtype, target_path):
    return (*stack, subtype) == tuple(target_path.split("/"))


def _build_hit_payload(dataset_key, bscv, stack, subtype, template_chain, verbose):
    hit = {
        "dataset": dataset_key,
        "bk24na": bscv["bk24na"],
        "sub_bkna": bscv["sub_bkna"],
        "chnu": bscv["chnu"],
        "psv_psn": bscv["psv_psn"],
        "stack_path": f"{'/'.join(stack)}/{subtype}",
    }
    if verbose:
        hit.update(spvp.build_root_payload(dataset_key, template_chain))
        return hit
    return hit


def _record_hit_if_match(
    hits,
    dataset_key,
    bscv,
    stack,
    subtype,
    target_path,
    limit,
    template_chain,
    verbose=False,
):
    if len(hits) >= limit:
        return
    if not _path_matches(stack, subtype, target_path):
        return
    hits.append(
        _build_hit_payload(
            dataset_key,
            bscv,
            stack,
            subtype,
            template_chain,
            verbose,
        )
    )


def _walk_wtel_plain(
    wtel,
    stack,
    target_path,
    hits,
    dataset_key,
    bscv,
    limit,
    template_chain=(),
    verbose=False,
):
    if isinstance(wtel, str):
        return
    assert isinstance(wtel, dict)
    if not wtp1.is_template(wtel):
        return
    subtype = wtp1.template_name(wtel)
    chain_with_cur = (*template_chain, (subtype, wtel))
    _record_hit_if_match(
        hits,
        dataset_key,
        bscv,
        stack,
        subtype,
        target_path,
        limit,
        chain_with_cur,
        verbose=verbose,
    )
    for arg_idx, arg in enumerate(wtp1.template_arguments(wtel), start=1):
        new_stack = (*stack, *_child_stack_symbols(subtype, arg_idx))
        for arg_wtel in arg:
            _walk_wtel_plain(
                arg_wtel,
                new_stack,
                target_path,
                hits,
                dataset_key,
                bscv,
                limit,
                template_chain=chain_with_cur,
                verbose=verbose,
            )


def _walk_wtel_plus(
    wtel,
    stack,
    target_path,
    hits,
    dataset_key,
    bscv,
    limit,
    template_chain=(),
    verbose=False,
):
    if isinstance(wtel, str):
        return
    assert isinstance(wtel, dict)
    if not wtp2.is_template(wtel):
        return
    subtype = wtp2.template_name(wtel)
    chain_with_cur = (*template_chain, (subtype, wtel))
    _record_hit_if_match(
        hits,
        dataset_key,
        bscv,
        stack,
        subtype,
        target_path,
        limit,
        chain_with_cur,
        verbose=verbose,
    )
    for param_key in wtp2.template_param_keys(wtel):
        new_stack = (*stack, *_child_stack_symbols(subtype, param_key))
        for arg_wtel in wtp2.template_param_val(wtel, param_key):
            _walk_wtel_plus(
                arg_wtel,
                new_stack,
                target_path,
                hits,
                dataset_key,
                bscv,
                limit,
                template_chain=chain_with_cur,
                verbose=verbose,
            )


def _find_stack_path_in_dataset(target_path, dataset_key, limit, verbose=False):
    hits = []
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
                        if len(hits) >= limit:
                            break
                        for wtel in wtseq:
                            if len(hits) >= limit:
                                break
                            walker(
                                wtel,
                                (col,),
                                target_path,
                                hits,
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


def _write_stdout_text(text):
    try:
        sys.stdout.write(text)
        if not text.endswith("\n"):
            sys.stdout.write("\n")
    except UnicodeEncodeError:
        # Some Windows terminals expose stdout with cp1252; write UTF-8 bytes
        # directly when available so Hebrew and niqqud are preserved.
        stdout_buffer = getattr(sys.stdout, "buffer", None)
        if stdout_buffer is None:
            escaped = text.encode("ascii", "backslashreplace").decode("ascii")
            sys.stdout.write(escaped)
            if not escaped.endswith("\n"):
                sys.stdout.write("\n")
            return
        stdout_buffer.write(text.encode("utf-8"))
        if not text.endswith("\n"):
            stdout_buffer.write(b"\n")
        stdout_buffer.flush()


def print_results(target_path, dataset_key, limit, hits, verbose=False):
    text = json.dumps(
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
    _write_stdout_text(text)
