"""Dispatch Wikisource bot tools.

Subcommands:
    real
                Edit Hebrew Wikisource pages via pywikibot.  Unrecognized
                arguments are passed through to pywikibot (e.g. -dir:...).
    proto
                Run the same edit flow against local files instead of the live
                site.
    intro
                Edit pages of MAM's introduction via pywikibot, selecting them by
                their in/mam-ws-intro/manifest.json keys rather than by book.

Examples:
    .venv/Scripts/python.exe py/main_ws_bot.py proto --edits path.json
    .venv/Scripts/python.exe py/main_ws_bot.py intro --edits path.json -dir:$env:USERPROFILE/.pywikibot --no-save
    .venv/Scripts/python.exe py/main_ws_bot.py real --edits path.json -dir:$env:USERPROFILE/.pywikibot
    .venv/Scripts/python.exe py/main_ws_bot.py real --edits path.json -dir:$env:USERPROFILE/.pywikibot --no-post-download
    .venv/Scripts/python.exe py/main_ws_bot.py real --edits path.json -dir:$env:USERPROFILE/.pywikibot --no-save
    .venv/Scripts/python.exe py/main_ws_bot.py real --edits path.json -dir:$env:USERPROFILE/.pywikibot --identity-run
"""

import argparse
import sys

from subcommands import ws_bot_intro
from subcommands import ws_bot_proto
from subcommands import ws_bot_real
from ws import ws_download_selector as wsds


def main() -> None:
    # Wikisource page titles are Hebrew, and they reach stderr: a --no-save run
    # names every chapter that would change. Redirected or piped on Windows,
    # those streams encode as cp1252 and the report dies of UnicodeEncodeError
    # instead of being read.
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")
    parser = build_parser()
    args, extra_args = parser.parse_known_args()
    if extra_args and not getattr(args, "allow_extra_args", False):
        parser.error(f"unrecognized arguments: {' '.join(extra_args)}")
    # The intro subcommand selects pages by key and has no chapter selector.
    if args.selector_parser is not None:
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
            "Skip the automatic post-run download, which, when the run changed a"
            " chapter, refreshes the 36 declared special pages and downloads the"
            " modified chapters to in/mam-ws"
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

    intro_parser = subparsers.add_parser(
        "intro",
        help="Edit pages of MAM's introduction via pywikibot.",
    )
    intro_parser.add_argument("--edits", required=True)
    intro_parser.add_argument(
        "--no-post-download",
        action="store_true",
        help="Skip refreshing in/mam-ws-intro/ after a run that saved a page",
    )
    intro_parser.add_argument(
        "--no-save",
        action="store_true",
        help="Apply the edits without saving; fail if any page would change",
    )
    intro_parser.set_defaults(
        func=_run_intro,
        allow_extra_args=True,
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


def _run_intro(args: argparse.Namespace, pywikibot_args) -> None:
    ws_bot_intro.run(
        args.edits,
        pywikibot_args,
        post_download=not args.no_post_download,
        no_save=args.no_save,
    )


if __name__ == "__main__":
    main()
