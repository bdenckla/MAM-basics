def proposed(quirkrec):
    return quirkrec.get(key_for_proposed(quirkrec))


_KEY_FOR_PROPOSED = {
    ("qr-lc-proposed", False): "qr-lc-proposed",
    (False, "qr-ac-proposed"): "qr-ac-proposed",
}


def key_for_proposed(quirkrec):
    lcp = "qr-lc-proposed" in quirkrec and "qr-lc-proposed"
    acp = "qr-ac-proposed" in quirkrec and "qr-ac-proposed"
    return _KEY_FOR_PROPOSED[(lcp, acp)]
