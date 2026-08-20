def short_id(quirkrec):
    """Compute a short identifier like "0119" or "0816-HVA" from a quirkrec.

    Args:
        quirkrec: dict with at least qr-cv (e.g. "1:19"); if qr-word-id
            is present, it is appended after a hyphen.
    """
    cv_str = quirkrec["qr-cv"]
    chnu, vrnu = tuple(int(part) for part in cv_str.split(":"))
    cn02vn02 = f"{chnu:02d}{vrnu:02d}"
    wid = quirkrec.get("qr-word-id")
    wid_str = f"-{wid}" if wid else ""
    return cn02vn02 + wid_str
