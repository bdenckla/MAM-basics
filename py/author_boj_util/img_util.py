from author_boj_util.lenin_img_too_tall import LENIN_IMG_SCALE
from author_boj_util.short_id_etc import short_id

INFO_ABOUT_OPTIONAL_IMAGES = [
    ("qr-aleppo-img", "Aleppo/Aleppo-CCVV.png"),
    ("qr-cam1753-img", "cam1753/cam1753-CCVV.png"),
    ("qr-jc-img", "Jerusalem-Crown-CCVV.png"),
]


def get_auto_imgs(jobn_top, quirkrec):
    """Auto-detect LC, Aleppo, and Cam1753 images if files exist on disk.

    Args:
        jobn_top: path to the jobn directory (boj_paths.jobn_dir()).
        quirkrec: quirkrec dict (must have at least qr-cv; qr-word-id
            is used if present to form the short ID).

    Returns:
        Dict of image-field keys (e.g. "qr-lc-img", "qr-aleppo-img")
        mapped to filename strings, for images that exist on disk.
    """
    out = {}
    sid = short_id(quirkrec)
    out["qr-lc-img"] = f"Lenin/Lenin-{sid}.png"
    if sid in LENIN_IMG_SCALE:
        out["qr-lc-img-scale"] = LENIN_IMG_SCALE[sid]
    # Auto-detect Aleppo, cam1753, and other optional images
    for field, example_filename in INFO_ABOUT_OPTIONAL_IMAGES:
        auto_img = example_filename.replace("-CCVV.png", f"-{sid}.png")
        auto_path = jobn_top / "img" / auto_img
        if auto_path.exists():
            out[field] = auto_img
    return out
