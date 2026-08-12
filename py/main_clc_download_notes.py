"""Exports main: download tanach.us note pages into committed files.

This is the *network* half of CLC notes, kept separate from the build on purpose
(like py/main_uxlc_download_changes.py downloads the core UXLC XML): the CLC build
itself (main_clc) reads only these committed local pages and never touches the
network, so its output is deterministic.

Usage (run from the repo root, network required, NOT part of the default build):

    python py/main_clc_download_notes.py            # all 39 books
    python py/main_clc_download_notes.py BookId      # just one book (dev/testing)
    python py/main_clc_download_notes.py --host <h>  # fetch from h, not tanach.us

For every atom carrying a UXLC ``<x>`` code -- every code, not just the note-
surfacing seed the build reads (clc_collect.NOTED_CODES); issue #25 wants the
complete note dataset on hand, including the codes (numeric / "X") that turn out
to have no page at all -- fetch
``https://tanach.us/Notes/<name>/<name>.<ch>.<v>.<position>-<code>.html`` -- where
``<name>`` is the canonical UXLC book name (my_uxlc.book_basename; e.g. id
"2Samuel" -> "Samuel_2"), the part that the build path historically got wrong --
and write the HTML to the committed
``in/UXLC-notes/<book_id>/<book_id>.<ch>.<v>.<position>-<code>.html``. A page
already present locally is left alone and not re-fetched -- this run is resumable
and re-runnable without re-hitting tanach.us for pages already on hand.

(The pages reference detail images, e.g. ``.../images/.../2-Detail.jpg``; pulling
those down can be added here later -- see the note in the loop.)
"""

import argparse
import sys

import requests

from mb_cmn import polite_download
import mb_cmn.file_io as my_open
import mb_cmn.bib_locales as tbn
import uxlc_misc.my_uxlc as my_uxlc
import clc.clc_collect as clc_collect
import clc.clc_note_pages as clc_note_pages
import clc.clc_read as clc_read
import uxlc_paths


def _download_one(session, book_id, ch, v, position, code, host=my_uxlc.UXLC_HOST):
    """Fetch one note page and write it locally; return True if now present.

    Returns True without touching the network if the page is already committed.
    Returns False if the page is missing (404 -- the note predates the change log,
    or tanach.us has none) or the request fails after retries.
    """
    out_path = clc_note_pages.local_page_path(book_id, ch, v, position, code)
    if out_path.exists():
        return True
    url = my_uxlc.note_page_url(book_id, ch, v, position, code, host)
    try:
        text = session.get_text(url, timeout=20, encoding="utf-8")
    except requests.RequestException:
        return False
    _show_progress(out_path)
    my_open.with_tmp_openw(out_path, {"newline": ""}, _write_callback, text)
    # (Future) parse <img src> from `text` and download referenced detail images.
    return True


def _write_callback(text, out_fp):
    out_fp.write(text)


def _show_progress(path):
    print(path)


def main():
    """Download note pages into in/UXLC-notes/ (network step).

    Defaults to all 39 books; an optional BookId argv restricts to one book (for
    dev/testing). Every ``<x>`` code is fetched (codes=None), not just the
    note-surfacing seed clc_collect.NOTED_CODES -- see the module docstring.
    """
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    args = _parse_args()
    if args.book_id is not None:
        assert args.book_id in tbn.ALL_BK39_IDS, f"unknown book id: {args.book_id!r}"
        book_ids = [args.book_id]
    else:
        book_ids = tbn.ALL_BK39_IDS
    total_found = total_missing = 0
    with polite_download.PoliteDownloader(_NOTES_CONFIG) as session:
        for book_id in book_ids:
            book = clc_read.read_book(book_id)
            found = missing = 0
            for ch, v, position, _atom, code in clc_collect.iter_noted_atoms(
                book, codes=None
            ):
                if _download_one(session, book_id, ch, v, position, code, args.host):
                    found += 1
                else:
                    missing += 1
            print(
                f"CLC note pages for {book_id}: {found} downloaded, "
                f"{missing} missing (404 / no page)"
            )
            total_found += found
            total_missing += missing
    if len(book_ids) > 1:
        print(
            f"CLC note pages overall: {total_found} downloaded, "
            f"{total_missing} missing (404 / no page)"
        )


def _parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "book_id",
        nargs="?",
        default=None,
        help="restrict to one book (dev/testing); default is all 39",
    )
    parser.add_argument(
        "--host",
        default=my_uxlc.UXLC_HOST,
        help=f"host to fetch from (default {my_uxlc.UXLC_HOST})",
    )
    return parser.parse_args()


_NOTES_CONFIG = polite_download.PoliteDownloadConfig(
    user_agent=(
        "Mozilla/5.0 (compatible; uxlc-clc-notes/1.0; +educational/personal-study)"
    ),
    default_timeout_s=30.0,
    accept_language="he,en;q=0.5",
    referer="https://tanach.us/",
    default_headers={
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Connection": "keep-alive",
    },
    throttle=polite_download.ThrottleConfig(min_delay_s=1.5, mean_delay_s=3.0),
    retry=polite_download.RetryConfig(max_attempts=4),
    # str(): CacheConfig.dir_path is declared str, and polite_download is vendored.
    cache=polite_download.CacheConfig(
        dir_path=str(uxlc_paths.tanach_us_http_cache_dir())
    ),
    obey_robots_txt=True,
)


if __name__ == "__main__":
    main()
