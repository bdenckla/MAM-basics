"""Fetch one URL from tanach.us politely, robots.txt obeyed, into a new directory.

Written for the concrete-transcription trial, 2026-11-03.  Usage, from the
MAM-basics clone's root:

    ./.venv/Scripts/python.exe py/main_concrete_transcription.py fetch
        <url> <out-dir> <out-name>

<out-dir> must not exist yet.  Writes <out-dir>/<out-name> and
<out-dir>/<out-name>.fetch.json, the fetch's record.
"""

import datetime
import hashlib
import json
from urllib.parse import urlsplit

from mb_cmn import polite_download
from uxlc_misc import my_uxlc


def run(url, out_dir, out_name):
    host = urlsplit(url).netloc
    if host != my_uxlc.UXLC_HOST:
        raise SystemExit(f"not {my_uxlc.UXLC_HOST}: {host}")
    out_dir.mkdir(parents=True, exist_ok=False)
    config = polite_download.PoliteDownloadConfig(
        user_agent=(
            "MAM-basics concrete-transcription trial "
            "(https://github.com/bdenckla/MAM-basics)"
        ),
        default_timeout_s=30.0,
        throttle=polite_download.ThrottleConfig(min_delay_s=1.5, mean_delay_s=3.0),
        retry=polite_download.RetryConfig(max_attempts=2),
        obey_robots_txt=True,
        robots_user_agent=my_uxlc.robots_user_agent(host),
    )
    fetched_at = datetime.datetime.now(datetime.timezone.utc)
    with polite_download.PoliteDownloader(config) as downloader:
        result = downloader._request("GET", url, allow_cache=False)
    body_path = out_dir / out_name
    body_path.write_bytes(result.body)
    record = {
        "url": url,
        "final_url": result.final_url,
        "encoding": result.encoding,
        "bytes": len(result.body),
        "sha256": hashlib.sha256(result.body).hexdigest().upper(),
        "fetched_at": fetched_at.isoformat(timespec="seconds"),
        "robots_user_agent": config.give_robots_user_agent(),
    }
    with open(
        out_dir / f"{out_name}.fetch.json", "w", encoding="utf-8", newline="\n"
    ) as fp:
        json.dump(record, fp, ensure_ascii=False, indent=2)
        fp.write("\n")
    print(json.dumps(record, ensure_ascii=False, indent=2))
