"""The site's one Taamey D font, checked against its pin, and its same-host support files.

Every published stylesheet that sets Hebrew in Taamey D loads ``gh-pages/woff2/Taamey_D.woff2``
by a relative URL. That tracked file is the canonical font: no code writes it, and
``font_bytes`` refuses it unless it is the pinned binary, Taamey D 1.1. ``site_font_assets``
returns bytes and performs no writes: the notices and ``SOURCE.txt`` that stand beside the font
in ``gh-pages/woff2/``, and the source package in ``gh-pages/font-sources/``. A publisher whose
pages link that ``SOURCE.txt`` must include the complete returned mapping in the same
publication; the Phonetic MAM and Yeivin ITM publishers both do. The source archive is the
release's immutable input, not executable repository code or a claim of an independently
reproduced font build.
"""

import hashlib
import io
import json
import posixpath
import zipfile

from mb_cmn import paths

# The Pages-root-relative path of the site's one copy of the font.
FONT = "woff2/Taamey_D.woff2"
_VERSION = "taamey-d-1.1"
_FONT_HASH = "388a38a23b22d038a8bc3b969158f79cb27aa5edaddddf2fead8969d07f21275"
# Taamey_D-sources.zip of the release snapshot 1.1-hbofonts-5d9d8d461f79, renamed.
_ARCHIVE = "Taamey_D-1.1-sources.zip"
_ARCHIVE_HASH = "97e33813adbfe17a9298696d3976bd6add82984e3b2c6f741527a6538a684d34"
_SHARED_FILES = (
    _ARCHIVE,
    "FONT-NOTICE.txt",
    "GPL-2.0.txt",
    "SOURCE-INVENTORY.json",
    "BUILD.txt",
    "SOURCE.txt",
)
# The archive holds the sources alone, so every support file is pinned here.
_SUPPORT_SHA256 = {
    "FONT-NOTICE.txt": "25f37bd8a9785e2112994bb0583e6068aab610546b195dfbeb8b93c4ef79b9e1",
    "GPL-2.0.txt": "edaef632cbb643e4e7a221717a6c441a4c1a7c918e6e4d56debc3d8739b233f6",
    "SOURCE-INVENTORY.json": "87bf1394fdd99be98a7aaf453a488ceb8c384721e51594aeb377c67cd52638fc",
    "BUILD.txt": "7c3ea65b81fe7bcf84af3d24b4990bf62167c02db14384aca379a71aea66035a",
    "SOURCE.txt": "710057ec8a5e9fb3e569aef0cf504d50d42aeb04deb3a86e31e30db720c2299f",
    "PRODUCT-WOFF2-SOURCE.txt": "bb60336e580c7a1419a847207827db1fcc2b586899564a98ad80235b53b70f6f",
}


def font_path():
    """Return the path of the site's one tracked copy of the font."""
    return paths.gh_pages_dir() / FONT


def font_bytes():
    """Return the site's font, refusing any file that is not the pinned binary."""
    font = font_path().read_bytes()
    if hashlib.sha256(font).hexdigest() != _FONT_HASH:
        raise ValueError(f"gh-pages/{FONT} differs from the pinned Taamey D 1.1")
    return font


def _archive_members(archive_bytes):
    """Each archive member's path, size and SHA-256, in archive order."""
    with zipfile.ZipFile(io.BytesIO(archive_bytes)) as archive:
        return [
            {
                "path": info.filename,
                "size": info.file_size,
                "sha256": hashlib.sha256(archive.read(info)).hexdigest(),
            }
            for info in archive.infolist()
        ]


def site_font_assets():
    """Return the Pages-root-relative support files of the site's one font."""
    font_bytes()
    support = paths.repo_root() / "in" / "font-support" / _VERSION
    shared = {name: (support / name).read_bytes() for name in _SHARED_FILES}
    template = (support / "PRODUCT-WOFF2-SOURCE.txt").read_bytes()
    if hashlib.sha256(shared[_ARCHIVE]).hexdigest() != _ARCHIVE_HASH:
        raise ValueError("Taamey D source archive differs from its reviewed input")
    for name, data in {**shared, "PRODUCT-WOFF2-SOURCE.txt": template}.items():
        if (
            name != _ARCHIVE
            and hashlib.sha256(data).hexdigest() != _SUPPORT_SHA256[name]
        ):
            raise ValueError(f"Taamey D {name} differs from its recorded SHA-256")
    inventory = json.loads(shared["SOURCE-INVENTORY.json"].decode("utf-8"))
    if _archive_members(shared[_ARCHIVE]) != inventory["source_archive"]["members"]:
        raise ValueError(
            "Taamey D source archive members differ from SOURCE-INVENTORY.json"
        )
    assets = {f"font-sources/{_VERSION}/{name}": data for name, data in shared.items()}
    beside_font = posixpath.dirname(FONT)
    for name in ("FONT-NOTICE.txt", "GPL-2.0.txt"):
        assets[f"{beside_font}/{name}"] = shared[name]
    assets[f"{beside_font}/SOURCE.txt"] = template
    return assets
