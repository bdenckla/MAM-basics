def image_urls(page_ddda):
    # page asssumed to be in DDDA format, meaning 3 digits followed by A or B, e.g. 043B.
    page_n = _get_page_n(page_ddda)
    return {
        "sefa": f"{_PRE_SEFA}BIB_LENCDX_F{page_ddda}.jpg",
        "lcci": f"{_PRE_LCCI}n{page_n}/mode/1up?view=theater",
    }


def cacb_hahb(page_ddda):
    # A (ca) (cap A) becomes א (ha) (Hebrew alef)
    # B (cb) (cap B) becomes ב (hb) (Hebrew bet)
    ddda_ddd, ddda_a = page_ddda[:3], page_ddda[3]
    return ddda_ddd + CACB_HAHB[ddda_a]


def _get_page_n(page_ddda):
    assert len(page_ddda) == 4
    ddda_ddd, ddda_a = page_ddda[:3], page_ddda[3]
    ddd_int = int(ddda_ddd)
    assert 1 <= ddd_int <= 491
    page_n_naive = 2 * ddd_int + _AB_INT[ddda_a]
    # Below, we substract 2 because "naively", ddda="001B" maps to n=3 (2*1 + 1)
    # but we want it to map to n=1.
    return page_n_naive - 2


CACB_HAHB = {"A": "א", "B": "ב"}
_AB_INT = {"A": 0, "B": 1}
_PRE_SEFA = "https://manuscripts.sefaria.org/leningrad-color/"
_PRE_LCCI = "https://archive.org/details/Leningrad_Codex_Color_Images/page/"
