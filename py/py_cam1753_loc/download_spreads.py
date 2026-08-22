"""Download pages 77-90 from Cambridge Ms. Add. 1753 on archive.org."""

import os
from urllib.request import urlopen, Request

import cam1753_paths

BASE_URL = (
    "https://ia800901.us.archive.org/BookReader/BookReaderImages.php"
    "?zip=/28/items/ketuvim-cambridge-ms-add-1753-images"
    "/Ketuvim_Cambridge_MS_Add_1753_jp2.zip"
    "&file=Ketuvim_Cambridge_MS_Add_1753_jp2"
    "/Ketuvim_Cambridge_MS_Add_1753_{page:04d}.jp2"
    "&id=ketuvim-cambridge-ms-add-1753-images"
    "&scale=2&rotate=0"
)


def main():
    """Fetch spreads 77-90 into codex-index-cam1753's ``cam1753-spreads/``.

    Those fourteen JPEGs are DOWNLOADED rather than generated, so no check
    regenerates them; nothing in this repo calls this module, and each page already
    on disk is skipped.

    WHY THIS FILE HAS A ``main()`` NOW.  The whole of it -- the ``os.makedirs``, the
    loop, the network reads -- ran at MODULE SCOPE in codex-index-cam1753, with no
    ``main()`` and no ``if __name__`` guard, until Phase 3 of
    ``doc/PLAN-evacuate-python-from-codex-index-trio.md`` on 2026-08-22.  Harmless in
    a repo whose only entry into it was to run it; not harmless in MAM-basics, where
    importing a top-level module to inspect it is ordinary and would have started
    fourteen downloads.  This is the THIRD such module in this repo's Python, after
    ``gutter_profile`` and ``split_spreads``, where Phase 1 predicted two --
    codex-index-aleppo's ``download_aleppo_pages.py`` had the identical shape and
    became ``main_ac_download_pages.py`` the day before.
    """
    out_dir = cam1753_paths.spreads_dir()
    os.makedirs(out_dir, exist_ok=True)

    for page in range(77, 91):
        url = BASE_URL.format(page=page)
        out_path = os.path.join(out_dir, f"cam1753-page-{page:04d}.jpg")
        if os.path.exists(out_path):
            print(f"  Already exists: {out_path}")
            continue
        print(f"  Downloading page {page} ...")
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=60) as resp:
            data = resp.read()
        with open(out_path, "wb") as f:
            f.write(data)
        print(f"    Saved {len(data)} bytes -> {out_path}")

    print("Done.")
