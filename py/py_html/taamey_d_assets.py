"""The site's one Taamey D font, checked against its pin, and its same-host support files.

Every published stylesheet that sets Hebrew in Taamey D loads ``gh-pages/woff2/Taamey_D.woff2``
by a relative URL. That tracked file is the canonical font: no code writes it, and
``font_bytes`` refuses it unless it is the pinned binary. ``site_font_assets`` returns bytes and
performs no writes: the notices and ``SOURCE.txt`` that stand beside the font in
``gh-pages/woff2/``, and the source package in ``gh-pages/font-sources/``. A publisher whose pages
link that ``SOURCE.txt`` must include the complete returned mapping in the same publication; the
Phonetic MAM and Yeivin ITM publishers both do. The upstream source archive is immutable input,
not executable repository code or a claim of an independently reproduced font build.
"""

import hashlib
import io
import posixpath
import zipfile

from mb_cmn import paths

# The Pages-root-relative path of the site's one copy of the font.
FONT = "woff2/Taamey_D.woff2"
_VERSION = "taamey-d-0.921"
_FONT_HASH = "5cc8df8ae3311b91e506edbb294561f6f0e39ebe4260bdb972c90902186c2474"
_ARCHIVE = "Taamey_D-0.921-source-40115a364a4e.zip"
_ARCHIVE_HASH = "fef946da31c894f5ce6d2c35f1b8a15359bbb1366bdb6ba9b63c7b4a9d67057e"
_SHARED_FILES = (
    _ARCHIVE,
    "FONT-NOTICE.txt",
    "GPL-2.0.txt",
    "SOURCE-INVENTORY.json",
    "BUILD.txt",
    "SOURCE.txt",
)
# Support files that the hash-checked source archive also holds: each must equal its copy there.
_ARCHIVED_COMPANIONS = (
    "FONT-NOTICE.txt",
    "GPL-2.0.txt",
    "SOURCE-INVENTORY.json",
    "BUILD.txt",
)
# The two support files that neither the archive nor its inventory records.
_UNARCHIVED_SHA256 = {
    "SOURCE.txt": "6e4497069cb52456348480bb75964019ae4cbcb0c4bbf839e8d24b9adc699c37",
    "PRODUCT-WOFF2-SOURCE.txt": "4dc079cc8b47739b4e6cfc0e5a2a54bcef53aea722d471d37ba550f103870cc4",
}


def font_path():
    """Return the path of the site's one tracked copy of the font."""
    return paths.gh_pages_dir() / FONT


def font_bytes():
    """Return the site's font, refusing any file that is not the pinned binary."""
    font = font_path().read_bytes()
    if hashlib.sha256(font).hexdigest() != _FONT_HASH:
        raise ValueError(
            f"gh-pages/{FONT} differs from the source package's frozen font"
        )
    return font


def site_font_assets():
    """Return the Pages-root-relative support files of the site's one font."""
    font_bytes()
    support = paths.repo_root() / "in" / "font-support" / _VERSION
    shared = {name: (support / name).read_bytes() for name in _SHARED_FILES}
    if hashlib.sha256(shared[_ARCHIVE]).hexdigest() != _ARCHIVE_HASH:
        raise ValueError("Taamey D source archive differs from its reviewed input")
    with zipfile.ZipFile(io.BytesIO(shared[_ARCHIVE])) as archive:
        for name in _ARCHIVED_COMPANIONS:
            member = f"{_ARCHIVE.removesuffix('.zip')}/{name}"
            if archive.read(member) != shared[name]:
                raise ValueError(
                    f"Taamey D {name} differs from its copy in the archive"
                )
    unarchived = {
        "SOURCE.txt": shared["SOURCE.txt"],
        "PRODUCT-WOFF2-SOURCE.txt": (support / "PRODUCT-WOFF2-SOURCE.txt").read_bytes(),
    }
    for name, data in unarchived.items():
        if hashlib.sha256(data).hexdigest() != _UNARCHIVED_SHA256[name]:
            raise ValueError(f"Taamey D {name} differs from its recorded SHA-256")
    assets = {f"font-sources/{_VERSION}/{name}": data for name, data in shared.items()}
    beside_font = posixpath.dirname(FONT)
    for name in ("FONT-NOTICE.txt", "GPL-2.0.txt"):
        assets[f"{beside_font}/{name}"] = shared[name]
    assets[f"{beside_font}/SOURCE.txt"] = unarchived["PRODUCT-WOFF2-SOURCE.txt"]
    return assets
