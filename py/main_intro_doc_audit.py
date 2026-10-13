"""Build the offline Introduction/doc-note research inventory; no product writes."""

import sys
import ctypes
import os

from intro_doc_audit import (
    audit,
    catalogues,
    proofs,
    review,
    rosters,
    structures,
    poetic_rosters,
)


def main():
    if os.name == "nt":
        kernel = ctypes.windll.kernel32
        kernel.GetCurrentProcess.restype = ctypes.c_void_p
        kernel.SetPriorityClass.argtypes = (ctypes.c_void_p, ctypes.c_uint)
        if not kernel.SetPriorityClass(kernel.GetCurrentProcess(), 0x4000):
            raise ctypes.WinError()
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")
    if sys.argv[1:] == ["review"]:
        review.main()
    elif sys.argv[1:] == ["proofs"]:
        proofs.main()
    elif sys.argv[1:] == ["structures"]:
        structures.main()
    elif sys.argv[1:] == ["catalogues"]:
        catalogues.main()
    elif sys.argv[1:] == ["rosters"]:
        rosters.main()
    elif sys.argv[1:] == ["poetic-rosters"]:
        poetic_rosters.main()
    elif not sys.argv[1:]:
        audit.main()
    else:
        raise SystemExit(
            "Usage: main_intro_doc_audit.py [review|proofs|structures|catalogues|rosters|poetic-rosters]"
        )


if __name__ == "__main__":
    main()
