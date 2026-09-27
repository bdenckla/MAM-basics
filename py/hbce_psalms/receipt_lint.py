"""Check every Hebrew form in the receipt against the data it reports on.

An editor that rewrites a file can silently reorder a form's combining marks, which renders
identically and compares differently. So each Hebrew form in
``doc/hbce-psalms-vs-mam-2026-09-26.md`` must be in MAM-normal mark order, as every tracked
``.md`` must be (``py/tests/test_prose_mark_order.py``), and must occur in the generated
outputs or in HBCE's transcriptions once both are put in MAM-normal order. A form with no
marks may instead equal the letters of a form that occurs there. A form that fails either
test was reordered some other way, or retyped.
"""

import re

from hbce_psalms import hbce_paths
from mb_cmn import hebrew_letters as hle
from mb_cmn import hebrew_points as hpo
from mb_cmn.uni_denorm import give_std_mark_order, has_std_mark_order

HEB = re.compile(f"[{hpo.RECC_HEBR}]+")


def _corpus() -> str:
    """The outputs and the transcriptions, in MAM-normal mark order."""
    paths = sorted(hbce_paths.out_dir().iterdir())
    paths += sorted(hbce_paths.transcriptions_dir().glob("*.xml"))
    texts = [p.read_text(encoding="utf-8") for p in paths]
    return give_std_mark_order("\n".join(texts))


def problems() -> tuple[int, list[str]]:
    """The number of distinct forms in the receipt, and a line for each one that fails."""
    corpus = _corpus()
    letters_only = {hle.letters(run) for run in HEB.findall(corpus)}
    receipt = hbce_paths.receipt_path().read_text(encoding="utf-8")
    forms = sorted(set(HEB.findall(receipt)))
    found = []
    for form in forms:
        codes = " ".join(f"{ord(c):04X}" for c in form)
        if not has_std_mark_order(form):
            found.append(f"not in MAM-normal mark order: {form} {codes}")
        elif form not in corpus and form not in letters_only:
            found.append(f"not in the data: {form} {codes}")
    return len(forms), found
