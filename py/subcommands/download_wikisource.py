"""Download revision-checked MAM chapters and rebuild affected production books.

Run from the repository root with main_download.py fr-wikisource. All existing
book/chapter selectors apply; --force-download retrieves every selected chapter.
"""

import time

from mb_cmn import polite_download
from mb_misc import ws_urls
from subcommands import parse_ws
from ws import ws_download_selector as wsds
from ws import ws_chapter_download as chapters
from ws import ws_revision_api as api


def run(book_plans, *, force_download=False):
    """Download selected chapters, then always run the affected-book product hook."""
    book_plans = [(he_bn_sbn, list(selected)) for he_bn_sbn, selected in book_plans]
    start = time.monotonic()
    session = api.CountingSession()
    try:
        with polite_download.PoliteDownloader(
            _WIKISOURCE_DOWNLOAD_CONFIG, session=session
        ) as downloader:
            stats = chapters.download_books(
                book_plans,
                downloader,
                endpoint=_WIKISOURCE_API_PHP,
                out_path=_OUT_PATH,
                metadata_path=_METADATA_PATH,
                force_download=force_download,
            )
    finally:
        elapsed = time.monotonic() - start
        print(
            f"Wikisource download: {elapsed:.2f}s; transport requests "
            f"metadata={session.metadata_requests}, content={session.content_requests}, "
            f"total={session.metadata_requests + session.content_requests}"
        )
    print(
        f"Wikisource chapters: selected={stats['selected']}, reused={stats['reused']}, "
        f"fetched={stats['fetched']}; batches metadata={stats['metadata_batches']}, "
        f"content={stats['content_batches']}"
    )
    parse_ws.almost_main(wsds.affected_bkids(book_plans))
    return {
        **stats,
        "download_seconds": elapsed,
        "metadata_requests": session.metadata_requests,
        "content_requests": session.content_requests,
    }


def run_from_args(args):
    run(wsds.selected_book_plans(args), force_download=args.force_download)


_OUT_PATH = "in/mam-ws"
_METADATA_PATH = "in/mam-ws-revisions.json"
_WIKISOURCE_USER_PAGE = ws_urls.he_url("משתמש:Bdenckla")
_WIKISOURCE_API_PHP = "https://he.wikisource.org/w/api.php"
_WIKISOURCE_DOWNLOAD_CONFIG = polite_download.PoliteDownloadConfig(
    user_agent=f"Denckla-Dowload-MAM-Bot/1.1 ({_WIKISOURCE_USER_PAGE})",
    default_timeout_s=30.0,
    throttle=polite_download.ThrottleConfig(min_delay_s=1.5, mean_delay_s=3.0),
    retry=polite_download.RetryConfig(max_attempts=4),
    cache=polite_download.CacheConfig(dir_path=".novc/http-cache/wikisource"),
    obey_robots_txt=False,
)
