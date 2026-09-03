"""Dispatch Wikisource bot tools.

Subcommands:
    real
                Edit Hebrew Wikisource pages via pywikibot.  Unrecognized
                arguments are passed through to pywikibot (e.g. -dir:...).
    proto
                Run the same edit flow against local files instead of the live
                site.
    holman-meteg-spec
                Check the Holman meteg rollout's two edit specifications against
                the suggestions JSON and the current in/mam-ws text, and with
                --write rebuild them.  Item 2 of
                doc/PLAN-holman-meteg-rollout-programme.md.

Examples:
    .venv/Scripts/python.exe py/main_ws_bot.py proto --edits path.json
    .venv/Scripts/python.exe py/main_ws_bot.py real --edits path.json -dir:$env:USERPROFILE/.pywikibot
    .venv/Scripts/python.exe py/main_ws_bot.py real --edits path.json -dir:$env:USERPROFILE/.pywikibot --no-post-download
    .venv/Scripts/python.exe py/main_ws_bot.py real --edits path.json -dir:$env:USERPROFILE/.pywikibot --no-save
    .venv/Scripts/python.exe py/main_ws_bot.py real --edits path.json -dir:$env:USERPROFILE/.pywikibot --identity-run
    .venv/Scripts/python.exe py/main_ws_bot.py holman-meteg-spec
    .venv/Scripts/python.exe py/main_ws_bot.py holman-meteg-spec --write
"""

import argparse
import sys

from subcommands import ws_bot_proto
from subcommands import ws_bot_real
from ws import holman_meteg_edit_spec
from ws import ws_download_selector as wsds


def main() -> None:
    # Wikisource page titles are Hebrew, and they reach stderr: a --no-save run
    # names every chapter that would change. Redirected or piped on Windows,
    # those streams encode as cp1252 and the report dies of UnicodeEncodeError
    # instead of being read.
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    parser = build_parser()
    args, extra_args = parser.parse_known_args()
    if extra_args and not getattr(args, "allow_extra_args", False):
        parser.error(f"unrecognized arguments: {' '.join(extra_args)}")
    # A subcommand that selects no chapters -- holman-meteg-spec reads the whole
    # target set off the suggestions JSON -- registers no selector to validate.
    if getattr(args, "selector_parser", None) is not None:
        wsds.validate_selector_args(args, args.selector_parser)
    args.func(args, extra_args)


def build_parser() -> argparse.ArgumentParser:
    """The fully-configured parser, so a test can read the subcommands off it."""
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
    real_parser.add_argument(
        "--no-post-download",
        action="store_true",
        help=(
            "Skip the automatic post-run download of modified chapters " "to in/mam-ws"
        ),
    )
    save_mode_group = real_parser.add_mutually_exclusive_group()
    save_mode_group.add_argument(
        "--no-save",
        action="store_true",
        help=(
            "Process edits without saving pages; fail if any chapter would change "
            "(useful for dry-run validation of a targeted bot)"
        ),
    )
    save_mode_group.add_argument(
        "--identity-run",
        action="store_true",
        help=(
            "Run a true identity/null bot: no processing and no saves "
            "(useful for exercising non-edit run plumbing)"
        ),
    )
    wsds.add_selector_opts(real_parser)
    real_parser.set_defaults(
        func=_run_real,
        allow_extra_args=True,
        selector_parser=real_parser,
    )

    proto_parser = subparsers.add_parser(
        "proto",
        help="Run the local-file bot prototype.",
    )
    proto_parser.add_argument("--edits")
    wsds.add_selector_opts(proto_parser)
    proto_parser.set_defaults(
        func=_run_proto,
        allow_extra_args=False,
        selector_parser=proto_parser,
    )

    holman_parser = subparsers.add_parser(
        "holman-meteg-spec",
        help="Check (or --write) the Holman meteg rollout's two edit specs.",
    )
    holman_meteg_edit_spec.add_args(holman_parser)
    holman_parser.set_defaults(
        func=holman_meteg_edit_spec.run,
        allow_extra_args=False,
        selector_parser=None,
    )
    return parser


def _run_real(args: argparse.Namespace, pywikibot_args) -> None:
    ws_bot_real.run(
        args.edits,
        wsds.selected_book_plans(args),
        pywikibot_args,
        post_download=not args.no_post_download,
        no_save=args.no_save,
        identity_run=args.identity_run,
    )


def _run_proto(args: argparse.Namespace, _extra_args) -> None:
    ws_bot_proto.almost_main(args.edits, wsds.selected_book_plans(args))


if __name__ == "__main__":
    main()
