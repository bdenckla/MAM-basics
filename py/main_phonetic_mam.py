"""Closed export, rendering, validation and transient computation interfaces.

Subcommands:
    export
        Regenerate the public display release through the private source adapter.
    render
        Render the tracked public display release, without private inputs.
    check
        Validate the complete public release without writing, and list the
        chapters that have left the legacy projection comparison.
    compute
        Serve transient, versioned NDJSON computations on stdin and stdout.
"""

import argparse
import sys


def build_parser():
    """Describe the closed command set without running an operation."""
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("export", help="Export the public display release")
    commands.add_parser("render", help="Render only the tracked public display release")
    commands.add_parser("check", help="Validate the tracked release without writing")
    commands.add_parser(
        "compute", help="Serve transient NDJSON computations on stdin/stdout"
    )
    return parser


def almost_main(argv=None):
    """Dispatch one explicit operation; imports preserve the private-input boundary."""
    args = build_parser().parse_args(argv)
    if args.command == "compute":
        from phonetic_mam.compute import serve

        return serve()
    if args.command == "export":
        from phonetic_mam.exporter import export_release

        return export_release()
    if args.command == "render":
        from phonetic_mam.publication import render

        return render()
    if args.command == "check":
        from phonetic_mam.projection_check import report_chapters_left
        from phonetic_mam.release import validate_complete_release

        validate_complete_release()
        return report_chapters_left()
    raise ValueError("unknown Phonetic MAM operation")


def main():
    """Use UTF-8 for both Windows and POSIX pipes.

    Standard input keeps an undecodable byte as an escape, so that the compute
    stream rejects only the line that holds it (``compute.serve``).
    """
    # No command-line run writes import caches into either repository, as
    # doc/phonetic-mam-compute.md promises of compute. Set here, before almost_main
    # imports anything, rather than at import, so that an importer such as
    # py/main_0_mega.py keeps its own bytecode caching.
    sys.dont_write_bytecode = True
    sys.stdin.reconfigure(encoding="utf-8", errors="surrogateescape")
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")
    return almost_main()


if __name__ == "__main__":
    main()
