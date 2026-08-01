"""Force UTF-8 stdout/stderr.

Several entry points print non-ASCII diagnostics (Hebrew text, "→", etc.). On a
non-UTF-8 console -- notably Windows cp1252 -- such a ``print`` crashes with
``UnicodeEncodeError``. Call :func:`force_utf8_io` at startup to reconfigure the
streams to UTF-8 so these prints succeed regardless of the console code page.
"""

from __future__ import annotations

import sys


def force_utf8_io() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8")
