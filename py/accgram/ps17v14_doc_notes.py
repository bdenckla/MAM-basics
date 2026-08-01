"""Generate gh-pages/accgram/ps17v14-mam-doc-notes.html -- an English rendering of
MAM's four documentation notes on Psalms 17:14 (one per chanted word -- one of the four
lemmas, מִ֥מְתִֽים־יָדְךָ֨, is a maqaf compound).

Formerly hand-authored; now generated so it shares the look and feel of the other
accgram pages.  The page body is replayed byte-exactly from the committed
``ps17v14_mam_doc_notes_body`` module (migrated from the original JSON) through the
shared shell in ``ps17v14_replay``.  It is the Psalms 17:14 sibling of
telg-doc-notes.html, and is linked from ps17v14-double-tsinnor.html.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from accgram import ps17v14_mam_doc_notes_body as _body
from accgram import ps17v14_replay

import wlc_paths

_OUT_NAME = "ps17v14-mam-doc-notes.html"


def default_html_out_path(repo_root: Path) -> Path:
    return wlc_paths.gh_pages_dir() / "accgram" / _OUT_NAME


def add_args(parser: argparse.ArgumentParser, repo_root: Path) -> None:
    ps17v14_replay.add_html_out_arg(parser, default_html_out_path(repo_root))


def run(args: argparse.Namespace) -> None:
    ps17v14_replay.write_replayed(args.html_out, _body, __file__)


def main() -> None:
    ps17v14_replay.main_for(
        body_module=_body,
        out_name=_OUT_NAME,
        generator_file=__file__,
        description=__doc__,
    )


if __name__ == "__main__":
    main()
