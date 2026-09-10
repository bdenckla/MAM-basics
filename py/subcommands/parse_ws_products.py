"""Write candidate plain/plus products from committed Wikisource downloads."""

from pathlib import Path

from mb_cmn import bib_locales as tbn
from mb_cmn import file_io
from mb_cmn import mam_bknas_and_std_bknas as names
from mb_cmn import paths
from py_misc import check_mpplus
from py_misc import mam_parsed_plain
from py_misc import mam_parsed_plus
from ws import ws_get_bk_in_both_fmts as wsin
from ws import ws_plain


def add_args(parser):
    """Require a destination separate from the production product tree."""
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Candidate directory for plain/ and plus/ JSON; no documentation is written.",
    )
    parser.set_defaults(func=run)


def run(args):
    """Generate and validate candidate products without production writes."""
    output_dir = args.output_dir.resolve()
    production = paths.mam_parsed_dir().resolve()
    if output_dir == production or production in output_dir.parents:
        raise ValueError("Candidate output must be outside MAM-parsed.")
    return generate(output_dir)


def generate(output_dir):
    """Write every complete book24 group and return its product paths."""
    grouped = {}
    for bkid in tbn.ALL_BK39_IDS:
        book = wsin.get_bk_in_fmt_2(paths.repo_root() / "in/mam-ws", bkid)
        light_book = ws_plain.convert_book(book)
        grouped.setdefault(tbn.bk24id(bkid), {})[
            names.BK39ID_TO_MAM_HBNP[bkid]
        ] = light_book
        print(f"Parsed Wikisource {bkid}", flush=True)
    out_paths = []
    for bk24id, light_books in grouped.items():
        plain = mam_parsed_plain.add_header(light_books)
        plus = mam_parsed_plus.add_plus_stuff(plain)
        filename = tbn.ordered_short_dash_full_24(bk24id) + ".json"
        book_paths = {}
        for kind, data in (("plain", plain), ("plus", plus)):
            book_paths[kind] = str(Path(output_dir) / kind / filename)
            file_io.json_dump_to_file_path(data, book_paths[kind])
        out_paths.append(book_paths)
    errors = check_mpplus.check_mpplus([book["plus"] for book in out_paths])
    if errors:
        raise ValueError(errors)
    print(f"Validated {len(out_paths)} candidate plus books.", flush=True)
    return out_paths
