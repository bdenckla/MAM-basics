"""Force UTF-8 stdout/stderr.

Several entry points print non-ASCII diagnostics (Hebrew text, "→", etc.). On a
non-UTF-8 console -- notably Windows cp1252 -- such a ``print`` crashes with
``UnicodeEncodeError``. Call :func:`force_utf8_io` at startup to reconfigure the
streams to UTF-8 so these prints succeed regardless of the console code page.

Stderr keeps its ``backslashreplace`` error handler: ``reconfigure`` given an
encoding and no ``errors`` resets the handler to ``strict``, and then a traceback
quoting a lone surrogate fails while it is being reported.
"""

from __future__ import annotations

import sys


def force_utf8_io() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")
