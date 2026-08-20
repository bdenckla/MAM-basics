"""Helper for wrapping text in parentheses with thin spaces."""

from mb_cmn.str_defs import THSP


def wrap_with_thin_spaced_paren(text: str) -> str:
    """Wrap text in parentheses with thin spaces for breathing room."""
    return f"({THSP}{text}{THSP})"
