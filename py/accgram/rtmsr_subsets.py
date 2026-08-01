from __future__ import annotations

from pathlib import Path

_OVERVIEW_HTML_NAME = "goerwitz.html"


def overview_html_out_path(main_html_out_path: Path) -> Path:
    return main_html_out_path.parent / _OVERVIEW_HTML_NAME
