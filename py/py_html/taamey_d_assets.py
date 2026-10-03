"""Prepare the frozen font and its same-host source support as one asset set.

This module returns bytes and performs no writes. A product publisher must include
the complete returned mapping in the same publication and link its font SOURCE.txt
from a product page. The upstream source archive is immutable input, not executable
repository code or a claim of an independently reproduced font build.
"""

import hashlib
import io
import zipfile

from mb_cmn import paths

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
    "PRODUCT-WOFF2-SOURCE.txt": "5da2baf9ac4cc80596e21149d8b876aecd5268376b6c98301167a2bbf233278f",
}


def product_font_assets(product):
    """Return Pages-root-relative assets for one explicitly supported product."""
    if product not in ("phonetic-mam", "yeivin-itm"):
        raise ValueError(f"Unknown font asset owner: {product!r}")
    root = paths.repo_root()
    support = root / "in" / "font-support" / _VERSION
    font = (root / "doc" / "woff2" / "Taamey_D.woff2").read_bytes()
    if hashlib.sha256(font).hexdigest() != _FONT_HASH:
        raise ValueError("Taamey D differs from the source package's frozen font")
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
    prefix = f"{product}/woff2"
    assets[f"{prefix}/Taamey_D.woff2"] = font
    for name in ("FONT-NOTICE.txt", "GPL-2.0.txt"):
        assets[f"{prefix}/{name}"] = shared[name]
    assets[f"{prefix}/SOURCE.txt"] = unarchived["PRODUCT-WOFF2-SOURCE.txt"]
    return assets
