"""Fetch the four published Google Docs into the .novc cache.

Every re-render of a published doc **reshuffles the ``.cN`` class names**:
three consecutive fetches of Part 1 gave three different names for the italic
class, the bold class and the title paragraph's class, and even differed
slightly in length. Nothing downstream may key on a class name, and the
importer must work from a single pinned snapshot rather than re-fetching per
subcommand -- otherwise two runs of the emitter see two different documents.
So ``fetch`` writes ``part{N}.html`` once, and everything else reads that.
"""

from mb_cmn import polite_download
from urwotm_import import parts


def download_all(part_nums=None):
    """Download each part's /pub HTML and pin it to the cache."""
    part_nums = part_nums or parts.PART_NUMS
    out = {}
    snap_dir = parts.snapshot_dir()
    snap_dir.mkdir(parents=True, exist_ok=True)
    with polite_download.PoliteDownloader(download_config()) as downloader:
        for part in part_nums:
            html = downloader.get_text(
                parts.pub_url(part),
                timeout=30,
                encoding="utf-8",
                # These are Ben's own published documents. Google's
                # robots.txt disallows /document/ wholesale, which would
                # block fetching one's own published-to-web pages.
                obey_robots=False,
            )
            snapshot_path(part).write_text(html, encoding="utf-8", newline="\n")
            out[part] = html
    return out


def read_all(part_nums=None):
    """Read the pinned snapshots; download any that are missing."""
    part_nums = part_nums or parts.PART_NUMS
    missing = [p for p in part_nums if not snapshot_path(p).exists()]
    if missing:
        download_all(missing)
    return {p: snapshot_path(p).read_text(encoding="utf-8") for p in part_nums}


def snapshot_path(part: int):
    return parts.snapshot_dir() / f"part{part}.html"


def download_config():
    parts.http_cache_dir().mkdir(parents=True, exist_ok=True)
    return polite_download.PoliteDownloadConfig(
        user_agent="Denckla-Import-Own-Docs-Bot/1.0 (https://bdenckla.github.io/)",
        default_timeout_s=30.0,
        referer="https://docs.google.com/document/",
        throttle=polite_download.ThrottleConfig(min_delay_s=1.5, mean_delay_s=3.0),
        retry=polite_download.RetryConfig(max_attempts=4),
        cache=polite_download.CacheConfig(dir_path=str(parts.http_cache_dir())),
        obey_robots_txt=False,
    )
