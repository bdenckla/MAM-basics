"""Dispatch Wikisource bot tools.

Subcommands:
    real   Edit Hebrew Wikisource pages via pywikibot.
    proto  Run the same edit flow against local files instead of the live site.

Examples:
    .venv/Scripts/python.exe py/main_ws_bot.py proto --edits path.json
    .venv/Scripts/python.exe py/main_ws_bot.py real --edits path.json -dir:$env:USERPROFILE/.pywikibot
"""

import argparse

from subcommands import ws_bot_proto
from subcommands import ws_bot_real
from ws import ws_download_selector as wsds


def main() -> None:
    parser = _build_parser()
    args, extra_args = parser.parse_known_args()
    if extra_args and not getattr(args, "allow_extra_args", False):
        parser.error(f"unrecognized arguments: {' '.join(extra_args)}")
    args.func(args, extra_args)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="subcommand", metavar="SUBCOMMAND")
    subparsers.required = True

    real_parser = subparsers.add_parser(
        "real",
        help="Edit Hebrew Wikisource pages via pywikibot.",
    )
    real_parser.add_argument("--edits", required=True)
    wsds.add_selector_opts(real_parser)
    real_parser.set_defaults(func=_run_real, allow_extra_args=True)

    proto_parser = subparsers.add_parser(
        "proto",
        help="Run the local-file bot prototype.",
    )
    proto_parser.add_argument("--edits")
    wsds.add_selector_opts(proto_parser)
    proto_parser.set_defaults(func=_run_proto, allow_extra_args=False)
    return parser


def _run_real(args: argparse.Namespace, pywikibot_args) -> None:
    wsds.validate_selector_args(args, _build_parser())
    ws_bot_real.run(args.edits, wsds.selected_book_plans(args), pywikibot_args)


def _run_proto(args: argparse.Namespace, _extra_args) -> None:
    wsds.validate_selector_args(args, _build_parser())
    ws_bot_proto.almost_main(args.edits, wsds.selected_book_plans(args))


if __name__ == "__main__":
    main()
