"""Write MAM-parsed-plus products from committed Wikisource downloads."""

from pathlib import Path

from mb_cmn import bib_locales as tbn
from mb_cmn import file_io
from mb_cmn import mam_bknas_and_std_bknas as names
from mb_cmn import paths
import main_authored
from py_misc import check_mpplus
from py_misc import mam_parsed_copy_py_files
from py_misc import mam_parser_stage
from py_misc import mam_parsed_plus
from verify_mp import parser_stage as parser_stage_validation
from ws import ws_get_bk_in_both_fmts as wsin
from ws import ws_plain


def add_args(parser):
    """Require a destination separate from the production product tree."""
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Candidate directory for plus/ JSON; no documentation is written.",
    )
    parser.set_defaults(func=run)


def run(args):
    """Generate and validate candidate products without production writes."""
    output_dir = args.output_dir.resolve()
    production = paths.mam_parsed_dir().resolve()
    if output_dir == production or production in output_dir.parents:
        raise ValueError("Candidate output must be outside MAM-parsed.")
    return generate(output_dir)


def generate_production(bkids, parsed_books):
    """Write affected production groups, support files, and documentation."""
    plus_paths = generate(paths.mam_parsed_dir(), bkids, parsed_books)
    mam_parsed_copy_py_files.copy_support_files()
    main_authored.cmd_gen_mam_parsed_docs(None)
    return plus_paths


def generate(output_dir, bkids=None, parsed_books=None):
    """Write complete affected book24 groups and return their plus paths."""
    selected_bkids = tuple(tbn.ALL_BK39_IDS if bkids is None else bkids)
    affected_bk24ids = {tbn.bk24id(bkid) for bkid in selected_bkids}
    parsed_books = parsed_books or {}
    grouped = {}
    for bkid in tbn.ALL_BK39_IDS:
        if tbn.bk24id(bkid) not in affected_bk24ids:
            continue
        book = parsed_books.get(bkid)
        if book is None:
            book = wsin.get_bk_in_fmt_2(paths.repo_root() / "in/mam-ws", bkid)
        light_book = ws_plain.convert_book(book)
        grouped.setdefault(tbn.bk24id(bkid), {})[
            names.BK39ID_TO_MAM_HBNP[bkid]
        ] = light_book
        print(f"Parsed Wikisource {bkid}", flush=True)
    plus_paths = []
    for bk24id, light_books in grouped.items():
        parser_stage = mam_parser_stage.add_header(light_books)
        validation = parser_stage_validation.validate(parser_stage)
        plus = mam_parsed_plus.add_plus_stuff(parser_stage)
        parser_stage_validation.validate_plus_conversion(parser_stage, validation, plus)
        filename = tbn.ordered_short_dash_full_24(bk24id) + ".json"
        plus_path = str(Path(output_dir) / "plus" / filename)
        file_io.json_dump_to_file_path(plus, plus_path)
        plus_paths.append(plus_path)
    errors = check_mpplus.check_mpplus(plus_paths)
    if errors:
        raise ValueError(errors)
    print(f"Validated {len(plus_paths)} Wikisource-derived plus books.", flush=True)
    return plus_paths
