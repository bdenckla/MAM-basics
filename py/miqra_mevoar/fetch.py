"""Download Avi's pCloud folder of Rabbi Kokhav's Word files into a new directory.

pCloud's public-link API needs no login: showpublink lists the folder, and
getpublinkdownload gives the hosts and path of a file's download. The link, which Avi
shared with Ben by email, is read from a file and written nowhere, so that neither it
nor its code reaches Git. Every request goes out alone, at least _GAP_S seconds after
the previous one ended, with a User-Agent naming MAM-basics, and robots.txt is obeyed.

Each file goes into .novc/miqra-mevoar/pcloud/<timestamp>/, a directory that must not
exist yet, with manifest.json: each file's name, pCloud file id, size, modification time
and SHA-256. A download whose size differs from the listing's is refused, and so is a
.docx that is not a sound zip or that would expand to more than _MAX_EXPANSION times its
own size. A lock file that LibreOffice or Word leaves beside an open document is skipped
and named, and any other file name that is not a plain one stops the fetch.
"""

import datetime
import hashlib
import io
import re
import time
import zipfile
from urllib.parse import parse_qs
from urllib.parse import urlsplit

from mb_cmn import file_io
from mb_cmn import paths
from mb_cmn import polite_download
from mb_cmn.new_york_time import NEW_YORK


def run(link_file):
    """Fetch the folder whose public link link_file holds."""
    with open(link_file, encoding="utf-8") as link_fp:
        code = _link_code(link_fp.read().strip())
    stamp = datetime.datetime.now(NEW_YORK).strftime("%Y%m%d-%H%M%S-%f%z")
    out_dir = paths.novc_dir() / "miqra-mevoar" / "pcloud" / stamp
    out_dir.mkdir(parents=True, exist_ok=False)
    spacer = _Spacer()
    manifest = []
    with polite_download.PoliteDownloader(_CONFIG) as downloader:
        host, listing = _listing(downloader, spacer, code)
        for meta in _files(listing["metadata"]):
            body = _download(downloader, spacer, host, code, meta)
            (out_dir / meta["name"]).write_bytes(body)
            entry = {
                "name": meta["name"],
                "fileid": meta["fileid"],
                "size": len(body),
                "modified": meta["modified"],
                "sha256": hashlib.sha256(body).hexdigest(),
            }
            manifest.append(entry)
            print(
                f"{entry['size']:>10} {entry['sha256'][:16]} {entry['modified']} {entry['name']}"
            )
    file_io.json_dump_to_file_path(manifest, str(out_dir / "manifest.json"), indent=1)
    print(f"{len(manifest)} files: {out_dir}")


def _link_code(link):
    """The code of a pCloud public link, the only part of it the API needs."""
    parts = urlsplit(link)
    host = parts.hostname or ""
    if parts.scheme != "https" or not (
        host.endswith(".pcloud.link") or host.endswith(".pcloud.com")
    ):
        raise SystemExit("The link file does not hold an https pCloud link")
    codes = parse_qs(parts.query).get("code", [])
    if len(codes) != 1 or not _CODE.fullmatch(codes[0]):
        raise SystemExit("The link file's pCloud link has no single plain code")
    return codes[0]


def _listing(downloader, spacer, code):
    """The folder's listing, and the API host that gave it; the link's region decides."""
    refusals = []
    for host in _API_HOSTS:
        data = spacer.call(
            downloader.get_json,
            f"https://{host}/showpublink",
            params={"code": code},
            allow_cache=False,
        )
        if data.get("result") == 0:
            return host, data
        refusals.append(f"{host}: {data.get('result')} {data.get('error', '')}")
    raise SystemExit(f"pCloud listed no folder: {refusals}")


def _files(folder):
    """The folder's files but lock files; a subfolder, or any other odd name, is refused."""
    if not folder.get("isfolder"):
        raise SystemExit("The pCloud link is not a folder's link")
    names = set()
    for meta in folder["contents"]:
        name = meta["name"]
        if meta.get("isfolder"):
            raise SystemExit(f"The pCloud folder has a subfolder, {name!r}")
        if _LOCK_FILE.fullmatch(name):
            print(f"skipped {name}: a lock file, left while its document is open")
            continue
        if not _FILE_NAME.fullmatch(name) or name in names:
            raise SystemExit(
                f"The pCloud folder has a file name fetch refuses: {name!r}"
            )
        if meta["size"] > _MAX_FILE_BYTES:
            raise SystemExit(f"{name} is {meta['size']} bytes, over {_MAX_FILE_BYTES}")
        names.add(name)
        yield meta


def _download(downloader, spacer, host, code, meta):
    link = spacer.call(
        downloader.get_json,
        f"https://{host}/getpublinkdownload",
        params={"code": code, "fileid": meta["fileid"]},
        allow_cache=False,
    )
    if link.get("result") != 0:
        raise SystemExit(
            f"pCloud gave no download of {meta['name']}: {link.get('error')}"
        )
    body = spacer.call(
        downloader.get_bytes,
        f"https://{link['hosts'][0]}{link['path']}",
        allow_cache=False,
    )
    if len(body) != meta["size"]:
        raise SystemExit(f"{meta['name']}: {len(body)} bytes, listed as {meta['size']}")
    if meta["name"].endswith(".docx"):
        _require_sound_docx(body, meta["name"])
    return body


def _require_sound_docx(body, name):
    try:
        with zipfile.ZipFile(io.BytesIO(body)) as zf:
            expanded = sum(info.file_size for info in zf.infolist())
            if expanded > _MAX_EXPANSION * len(body):
                raise SystemExit(
                    f"{name} would expand to {expanded} bytes from {len(body)}"
                )
            if (bad := zf.testzip()) is not None:
                raise SystemExit(f"{name}: its member {bad} fails its CRC check")
            if "word/document.xml" not in zf.namelist():
                raise SystemExit(f"{name} has no word/document.xml")
    except zipfile.BadZipFile as error:
        raise SystemExit(f"{name} is not a sound zip: {error}") from error


class _Spacer:
    """Start each call at least _GAP_S seconds after the previous call ended."""

    def __init__(self):
        self._last_end = None

    def call(self, function, *args, **kwargs):
        if self._last_end is not None:
            time.sleep(max(_GAP_S - (time.monotonic() - self._last_end), 0.0))
        try:
            return function(*args, **kwargs)
        finally:
            self._last_end = time.monotonic()


_API_HOSTS = ("api.pcloud.com", "eapi.pcloud.com")
_GAP_S = 2.0
_MAX_FILE_BYTES = 20_000_000
# The six Word files of 2026-11-02 expand 7 to 15 times; a zip bomb, a thousand or more.
_MAX_EXPANSION = 50
_CODE = re.compile("[A-Za-z0-9]+")
_FILE_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9 ._-]*")
# The lock files that LibreOffice (.~lock.<name>#) and Word (~$ and the name's tail) leave
# beside a document while it is open. On 2026-11-03 the folder held .~lock.yehoshua.docx#.
_LOCK_FILE = re.compile(r"\.~lock\..+#|~\$.+")
_CONFIG = polite_download.PoliteDownloadConfig(
    user_agent="MAM-basics Miqra Mevoar fetch (https://github.com/bdenckla/MAM-basics)",
    # Requests to one host within a call, such as a robots.txt read and the download
    # after it, are spaced too.
    throttle=polite_download.ThrottleConfig(min_delay_s=_GAP_S),
    obey_robots_txt=True,
)
