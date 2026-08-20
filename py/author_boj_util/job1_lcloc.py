"""Format Leningrad Codex location references."""

from boj_render import boj_html

__all__ = ["lcloc"]


def lcloc(lcloc):
    page = lcloc["page"]
    line = lcloc["line"]
    column = lcloc["column"]
    abs_line, m_sp_cfb = _maybe_sp_cfb(line)
    m_sp_ibl = _maybe_sp_ibl(lcloc)
    m_sp_line2 = _maybe_sp_line2(lcloc)
    return [
        "μL (",
        _lc_page_anchor(page),
        f" {page}, col {column}, line {abs_line}{m_sp_line2}{m_sp_cfb}{m_sp_ibl}):",
    ]


def _lc_page_anchor(page):
    # E.g. page == "397B"
    href = f"https://manuscripts.sefaria.org/leningrad-color/BIB_LENCDX_F{page}.jpg"
    return boj_html.anchor_h("page", href)


def _maybe_sp_line2(lcloc):
    if line2 := lcloc.get("line2"):
        return f" and line {line2}"
    return ""


def _maybe_sp_ibl(lcloc):
    if ibl := lcloc.get("including-blank-lines"):
        sq = "s" if ibl != 1 else ""
        return f" (including {ibl} blank line{sq} in the count)"
    return ""


def _maybe_sp_cfb(line):
    if line < 0:
        return line, f" ({-line} counting from bottom of column)"
    return line, ""
