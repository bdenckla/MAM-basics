"""Generate gh-pages/wlc/accgram/ps17v14-double-tsinnor.html -- the double-tsinnor
oddity of Psalms 17:14: why it is unique, how the accent-grammar checker accepts
it, and what the manuscripts, MAM, and Breuer say.

Formerly hand-authored; now generated so it shares the look and feel of the other
accgram pages.  The page body is replayed byte-exactly from the committed
``ps17v14_double_tsinnor_body`` module (migrated from the original JSON) through
the shared shell in ``ps17v14_replay``.  Linked from index.html and the poetic
report; it links on to ps17v14-mam-doc-notes.html.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from accgram import ps17v14_double_tsinnor_body as _body
from accgram import ps17v14_replay

from mb_cmn import paths

_OUT_NAME = "ps17v14-double-tsinnor.html"


def default_html_out_path(repo_root: Path) -> Path:
    return paths.wlc_pages_dir() / "accgram" / _OUT_NAME


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
