"""Prepare the frozen font and its same-host source support as one asset set.

This module returns bytes and performs no writes. A product publisher must include
the complete returned mapping in the same publication and link its font SOURCE.txt
from a product page. The upstream source archive is immutable input, not executable
repository code or a claim of an independently reproduced font build.
"""

import hashlib

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
    if any(not data for data in shared.values()):
        raise ValueError("Taamey D source support contains an empty file")
    assets = {f"font-sources/{_VERSION}/{name}": data for name, data in shared.items()}
    prefix = f"{product}/woff2"
    assets[f"{prefix}/Taamey_D.woff2"] = font
    for name in ("FONT-NOTICE.txt", "GPL-2.0.txt"):
        assets[f"{prefix}/{name}"] = shared[name]
    source = (support / "PRODUCT-WOFF2-SOURCE.txt").read_bytes()
    if not source:
        raise ValueError("Taamey D product source notice is empty")
    assets[f"{prefix}/SOURCE.txt"] = source
    return assets
