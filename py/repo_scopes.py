"""What the source lints scan, now that several evacuated repos' code shares one root.

``check_mark_order``, ``check_escape_sequences`` and their two ``fix_*``
counterparts came here from repos where each walked up to ``.git`` and found a root
holding nothing but the code it was written for.  Here that walk finds a root
holding all of MAM-basics, and none of the checks has a repo-wide meaning: measured
2026-08-19, mark order reports violations in ``py/ws/`` and the escape check reports
them in ``py/wlc_cmn/``, neither of which is any of these repos' business.  So the
scope is a union of hand-maintained per-repo lists rather than a walk.

WHY A UNION AND NOT ONE LIST.  ``py/boj_paths.py``, ``py/hkq_paths.py`` and
``py/uxlc_paths.py`` were three per-repo precedents when Phase 3 of
``doc/PLAN-evacuate-python-from-codex-index-trio.md`` had to decide, and its Phase 0
said per-repo is the default unless a reason against it turns up.  None did: each
repo's list belongs beside that repo's data-root accessor, where the reader who
adds a module is already looking, and this module is the one place that has to know
they exist.

WHICH REPOS ARE IN, AND WHY IT IS NOT ALL OF THEM.  Three of the six repos whose
Python this programme moved into MAM-basics ran these lints over their own trees:
book-of-job, codex-index-aleppo and codex-index-cam1753, whose copies of the four
were two committed blobs -- book-of-job's on one side and the two codex-index repos'
on the other.  Keeping their code linted is a restoration, not an expansion.
UXLC-utils and holman-ketiv-qere never had these lints, and adding their code here
would surface violations that are nobody's current business; they are deliberately
absent. codex-index-leningrad never had them either and IS included, because its
eight small modules pass both checks as they stand, so including them costs nothing
and closes the one gap a reader would otherwise have to be told about.

CORPUS ROOTS ARE A SHORTER LIST THAN CODE PATHS, and the difference is not an
oversight.  ``check_mark_order`` reads ``.json`` as well as ``.py``, and for
book-of-job, codex-index-aleppo and codex-index-cam1753 the hand-made JSON that
stayed behind in each data repo is a large part of what the check was ever for --
24 line-break files in the first, 78 line-break, column-coordinate and flat-stream
files in the second, and 27 line-break plus 28 column-quadrilateral files in the
third. The Leningrad tree now holds only two generated JSON artifacts and no
separate corpus root, so it contributes no mark-order scope.

``check_function_ordering`` is NOT a consumer of this module, and that is
deliberate.  Only book-of-job ever ran it -- it is one of the seven checks in
``check_all.py``, which is book-of-job's register, and codex-index-aleppo's
``check_ac_all.py`` lists four checks that do not include it.  Widening it would
turn a passing check into a failing one over code that has never been held to it,
which is a decision rather than a restoration, so it still reads
``boj_paths.code_paths()`` directly.
"""

from pathlib import Path

import ac_paths
import boj_paths
import cam1753_paths
import lenin_paths
from mb_cmn import paths


def code_paths() -> list[Path]:
    """Every place an in-scope evacuated repo's Python lives under this repo's ``py/``.

    Each contributing list fails loudly on an entry that no longer exists, so a
    renamed or deleted module is caught here rather than going silently unlinted.
    """
    return [
        *boj_paths.code_paths(),
        *ac_paths.code_paths(),
        *lenin_paths.code_paths(),
        *cam1753_paths.code_paths(),
    ]


def corpus_roots() -> list[Path]:
    """The data roots whose ``.json`` the mark-order check reads.

    See the module docstring for why this is shorter than ``code_paths()``.
    """
    return [
        paths.repo_root() / "book-of-job",
        ac_paths.ac_data_root(),
        cam1753_paths.cam1753_data_root(),
    ]


def display_roots() -> list[Path]:
    """The roots a report tries, in order, when showing a path relatively.

    This repo's ``py/`` first, since most in-scope files are under it, then each
    corpus root.  A single ``relative_to`` raises ValueError on every file under
    one of the others, which is why a report needs the list rather than a root.
    """
    return [boj_paths.code_dir(), *corpus_roots()]
