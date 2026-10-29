"""The site's one Taamey D font, checked against its pin, and its same-host support files.

Every published stylesheet that sets Hebrew in Taamey D loads ``gh-pages/woff2/Taamey_D.woff2``
by a relative URL. That tracked file is the canonical font: no code writes it, and
``font_bytes`` refuses it unless it is the pinned binary, Taamey D 1.2. ``site_font_assets``
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
_VERSION = "taamey-d-1.2"
_FONT_HASH = "34e415bd2a28d4d0d407aa2138a43a1a87d9519a6df39933ec05976051032b2c"
# Taamey_D-sources.zip of the release snapshot 1.2-MAM-basics-1f1be97138d5, renamed.
_ARCHIVE = "Taamey_D-1.2-sources.zip"
_ARCHIVE_HASH = "a4b6eaad0a7335d1e878ac874fe52b6305c9d5204fd7c54f7358ff95da49cb89"
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
    "SOURCE-INVENTORY.json": "4258f29e112e00b8a9ae912503f1c156841d40e7b80057c66dfeabcdf4ab1609",
    "BUILD.txt": "01d510f50b273db3cb694ff5b0c9580939554c765dc7f48dd03eb3c0f1231a10",
    "SOURCE.txt": "88fbb9a955d8457f7952577b98cc952af4a18ba87a2d6b6cf55d3f76a04da34f",
    "PRODUCT-WOFF2-SOURCE.txt": "0eef02ddce7ec009d1bffa2462bf9b88d524c901154ca10e6989315f86f8afc9",
}


def font_path():
    """Return the path of the site's one tracked copy of the font."""
    return paths.gh_pages_dir() / FONT


def font_bytes():
    """Return the site's font, refusing any file that is not the pinned binary."""
    font = font_path().read_bytes()
    if hashlib.sha256(font).hexdigest() != _FONT_HASH:
        raise ValueError(f"gh-pages/{FONT} differs from the pinned Taamey D 1.2")
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
