"""
Base Usage:
.venv/Scripts/python.exe py/main_uxlc_download_changes.py

Fetches from my_uxlc.UXLC_DOWNLOAD_HOST -- hcanat.us, not tanach.us, and see that
constant for why.  ``--host`` fetches from somewhere else again, and a run with it
does NOT go on to rebuild: see main().
"""

import argparse
import sys
from pathlib import Path
import zipfile

import main_uxlc_mega
from mb_cmn import polite_download
from mb_cmn.uxlc_change_url import uxlc_release_xml_filename, uxlc_release_xml_url
import mb_cmn.file_io as my_open
import uxlc_misc.my_uxlc as my_uxlc
import uxlc_misc.my_uxlc_changes as my_uxlc_changes
import uxlc_paths

_DELAY_MIN = 1.5
_DELAY_MEAN = 3.0
_REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; uxlc-download-changes/1.0; "
        "+educational/personal-study)"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "he,en;q=0.5",
    "Referer": "https://tanach.us/Books/",
    "Connection": "keep-alive",
}


def _uxlc_zip_url(host):
    return f"https://{host}/Books/Tanach.xml.zip"


def _do_one_download(session, date, host=my_uxlc.UXLC_DOWNLOAD_HOST):
    filename = uxlc_release_xml_filename(date)
    url = uxlc_release_xml_url(date, host)
    out_path = uxlc_paths.uxlc_misc_dir() / filename
    _show_progress(out_path)
    text = session.get_text(url, timeout=10, encoding="utf-8")
    my_open.with_tmp_openw(out_path, {"newline": ""}, _write_callback, text)


def _write_callback(text, out_fp):
    out_fp.write(text)


def _download_latest_uxlc(session, host=my_uxlc.UXLC_DOWNLOAD_HOST):
    uxlc_paths.uxlc_39_dir().mkdir(parents=True, exist_ok=True)
    uxlc_paths.uxlc_rest_dir().mkdir(parents=True, exist_ok=True)
    uxlc_paths.novc_dir().mkdir(parents=True, exist_ok=True)
    zip_path = uxlc_paths.novc_dir() / "Tanach.xml.zip"
    _show_progress(zip_path)
    with open(zip_path, "wb") as out_fp:
        out_fp.write(session.get_bytes(_uxlc_zip_url(host), timeout=30))
    _extract_uxlc_zip(zip_path)


def _extract_uxlc_zip(zip_path):
    with zipfile.ZipFile(zip_path) as zip_fp:
        for zip_info in zip_fp.infolist():
            if zip_info.is_dir():
                continue
            member_name = Path(zip_info.filename).name
            if not member_name.endswith(".xml"):
                continue
            out_dir = _target_dir_for_member(member_name)
            out_path = out_dir / member_name
            _show_progress(out_path)
            with zip_fp.open(zip_info) as in_fp, open(out_path, "wb") as out_fp:
                out_fp.write(in_fp.read())


def _target_dir_for_member(member_name):
    if member_name in my_uxlc.CANONICAL_XML_FILE_NAMES:
        return uxlc_paths.uxlc_39_dir()
    return uxlc_paths.uxlc_rest_dir()


def _show_progress(path):
    print(f"{Path(__file__).name} {path}")


def main():
    """Download UXLC inputs, then rebuild downstream derived outputs.

    The default run fetches from my_uxlc.UXLC_DOWNLOAD_HOST and DOES rebuild.  A
    ``--host`` run naming any other host stops after downloading and does not:
    what a third host serves under ``/Books/`` and ``/Changes/`` is that host's,
    and rebuilding from it would put those bytes into the tracked outputs
    silently.

    Until 2026-08-12 this guard read ``!= UXLC_HOST``, and the rebuilding host was
    the publishing host, tanach.us.  Those are two hosts now -- see
    UXLC_DOWNLOAD_HOST -- and it is the DOWNLOAD host a default run rebuilds from.
    """
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    args = _parse_args()
    with polite_download.PoliteDownloader(_UXLC_DOWNLOAD_CONFIG) as session:
        _download_latest_uxlc(session, args.host)
        for filename in my_uxlc_changes.FILENAMES:
            if "fake" in filename:
                continue
            date = filename[:10]
            _do_one_download(session, date, args.host)
    if args.host != my_uxlc.UXLC_DOWNLOAD_HOST:
        print(f"--host {args.host}: downloaded only, not rebuilding")
        return
    main_uxlc_mega.main()


def _parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--host",
        default=my_uxlc.UXLC_DOWNLOAD_HOST,
        help=f"host to fetch from (default {my_uxlc.UXLC_DOWNLOAD_HOST})",
    )
    return parser.parse_args()


_UXLC_DOWNLOAD_CONFIG = polite_download.PoliteDownloadConfig(
    user_agent=(
        "Mozilla/5.0 (compatible; uxlc-download-changes/1.0; "
        "+educational/personal-study)"
    ),
    default_timeout_s=30.0,
    accept_language="he,en;q=0.5",
    referer="https://tanach.us/Books/",
    default_headers={
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Connection": "keep-alive",
    },
    throttle=polite_download.ThrottleConfig(
        min_delay_s=_DELAY_MIN, mean_delay_s=_DELAY_MEAN
    ),
    retry=polite_download.RetryConfig(max_attempts=4),
    # str(): CacheConfig.dir_path is declared str, and polite_download is vendored.
    cache=polite_download.CacheConfig(
        dir_path=str(uxlc_paths.tanach_us_http_cache_dir())
    ),
    obey_robots_txt=True,
)


if __name__ == "__main__":
    main()
