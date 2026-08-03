"""Source-hygiene guard for hand-authored source (GitHub issues #22, #26).

Enforces two rules over hand-authored ``py/`` + ``tools/`` + ``doc/``:

1. **No orphan combining mark** (#22): a string literal whose first character is
   a Unicode combining mark. Written raw, such a mark renders as an invisible or
   floating diacritic hanging off the opening quote -- unreadable in an editor,
   un-diffable in review, and easily reintroduced by hand. The fix is a named
   escape ``"\\N{UNICODE NAME}"`` (byte-identical at runtime, self-documenting,
   plain ASCII in the file).

   Why raw source, not the decoded AST value: Python decodes ``\\N{...}`` /
   ``\\uXXXX`` escapes when it builds the AST, so the *approved* escaped form and
   a *raw* orphan mark produce the identical ``ast.Constant.value``. The
   distinction survives only in the source bytes. So we locate string literals
   via the AST (precise: only real literals, never a mark inside a comment) but
   test each literal's **raw source segment** -- a leading escape ``\\`` is a
   base character and is accepted; a leading raw combining mark is flagged.

   The "first character of the literal" test is deliberate: it catches the
   floating diacritic while leaving genuine Hebrew *text* data untouched. The one
   legitimate case in the tree is a word in
   ``py/uxlc_fois/fois_mark_grammar_foi.py`` whose combining accent follows a
   ZERO WIDTH JOINER mid-string -- the literal starts with a base letter, so it
   is not flagged.

2. **No decomposed canonical composite** (#26): a base character immediately
   followed by a combining mark that together have a single-codepoint NFC
   composition (e.g. decomposed ``h`` + U+0323 -> precomposed U+1E25). Hand-
   authored source standardizes on NFC for exactly this class of character (the
   h-with-dot-below transliteration); tooling/paste-from-web defaults to NFC too,
   so pinning it removes an edit/match-failure tax rather than fighting the
   ecosystem default. Read over the *decoded* text (NFC is a property of decoded
   text, unlike rule 1's raw-source distinction). Hebrew text is never flagged:
   every Hebrew letter+point pair is on the NFC composition-exclusion list, so
   nothing Hebrew ever composes -- this holds by construction, not by
   special-casing.

Shared harness: file discovery + a pluggable tuple of ``Check``s, each yielding
``Offense(relpath, line, codepoint, uname, detail)``.

Two entry points, one scanner -- this module is a library and is not itself
runnable:
  * ``py/main_test.py py/tests/source_hygiene_test.py`` -- the guard test.
  * ``python py/main_source_hygiene.py`` -- the CLI, which prints each offender
    and exits non-zero when the tree is dirty.

Escape hatch: a trailing ``# combining-ok`` on the offending line suppresses rule
1, for the rare case where a bare combining mark is genuinely the clearest form.
"""

import ast
import os
import unicodedata
from collections import namedtuple

Offense = namedtuple("Offense", "relpath line codepoint uname detail")

# Directory names pruned from the walk: Python's bytecode cache, and nothing
# else. In UXLC-utils this also pruned ``mb_cmn`` and ``mb_diff_mpu`` as vendored
# copies "not ours to police"; here they are native -- the SOURCE the other repos
# vendor FROM -- so pruning them would exempt the originals from a rule their
# copies are held to. (The same exclusion was deleted from
# ``py/tests/test_transliterations.py`` for the same reason.)
_PRUNED_DIRS = {"__pycache__"}

# Roots of hand-authored source, relative to the repo root: Python (py/) plus
# prose (doc/). Data and generated trees (in/, out/, gh-pages/, .novc/) are never
# under these, so they are excluded by construction. ``tools/`` is UXLC-utils'
# name for a directory this repo does not have; ``os.walk`` of a missing root
# yields nothing, so it costs nothing to keep listed and the scanner stays usable
# against a tree that has one.
_SOURCE_ROOTS = ("py", "tools", "doc")

# Legal string prefixes (r, b, f, u and case/combination variants) that may sit
# between the start of a literal's source segment and its opening quote.
_STRING_PREFIX_CHARS = "rbfuRBFU"

_PRAGMA = "# combining-ok"


def iter_source_files(repo_root):
    """Repo-relative paths of hand-authored ``*.py``/``*.md``/``*.txt`` source."""
    for root_name in _SOURCE_ROOTS:
        root = os.path.join(repo_root, root_name)
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in _PRUNED_DIRS]
            for name in filenames:
                if name.endswith((".py", ".md", ".txt")):
                    full = os.path.join(dirpath, name)
                    yield os.path.relpath(full, repo_root).replace(os.sep, "/")


def _first_string_body_char(seg):
    """The first character *inside* a string literal's raw source ``seg``.

    Skips any string prefix and the opening quote (single or triple). Returns
    ``None`` if ``seg`` is not a plain quoted literal we can read.
    """
    i = 0
    while i < len(seg) and seg[i] in _STRING_PREFIX_CHARS:
        i += 1
    if seg[i : i + 3] in ('"""', "'''"):
        i += 3
    elif i < len(seg) and seg[i] in "\"'":
        i += 1
    else:
        return None
    return seg[i] if i < len(seg) else None


def find_orphan_combining_marks(relpath, text):
    """Yield an ``Offense`` per string literal whose raw source starts with a combining mark.

    Walks the AST so only real string *literals* are inspected, then reads each
    literal's raw source segment so an escaped mark (``\\N{...}`` / ``\\uXXXX``) is
    accepted and only a raw orphan mark is flagged. A trailing ``# combining-ok``
    on the line suppresses the finding.
    """
    lines = text.splitlines()
    tree = ast.parse(text, filename=relpath)
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
            continue
        seg = ast.get_source_segment(text, node)
        if seg is None:
            continue
        ch = _first_string_body_char(seg)
        if ch is None or not unicodedata.combining(ch):
            continue
        line = node.lineno
        if _PRAGMA in lines[line - 1]:
            continue
        yield Offense(
            relpath=relpath,
            line=line,
            codepoint=f"U+{ord(ch):04X}",
            uname=unicodedata.name(ch, f"<unnamed U+{ord(ch):04X}>"),
            detail="orphan combining mark; use a \\N{NAME} escape",
        )


def find_decomposed_composites(relpath, text):
    """Yield an ``Offense`` per decomposed base+combining-mark pair that has a
    single-codepoint NFC composition (GitHub issue #26).

    Reads the *decoded* text (unlike ``find_orphan_combining_marks``, NFC is a
    property of decoded text, not raw source). For each combining mark, checks
    whether it composes with the immediately preceding character; if so, that
    pair is a decomposed canonical composite and should be written precomposed.
    Hebrew is never flagged: no Hebrew letter+point pair has a single-codepoint
    NFC composition (all are on the composition-exclusion list), so this holds
    by construction, not by special-casing.
    """
    line_no = 1
    for i, ch in enumerate(text):
        if ch == "\n":
            line_no += 1
            continue
        if i == 0 or not unicodedata.combining(ch):
            continue
        comp = unicodedata.normalize("NFC", text[i - 1] + ch)
        if len(comp) == 1:
            yield Offense(
                relpath=relpath,
                line=line_no,
                codepoint=f"U+{ord(ch):04X}",
                uname=unicodedata.name(ch, f"<unnamed U+{ord(ch):04X}>"),
                detail=(
                    "decomposed composite; write precomposed "
                    f"U+{ord(comp):04X} {unicodedata.name(comp, '?')}"
                ),
            )


Check = namedtuple("Check", "name applies run")

# The pluggable check tuple.
CHECKS = (
    Check(
        name="orphan-combining-mark",
        applies=lambda relpath: relpath.endswith(".py"),
        run=find_orphan_combining_marks,
    ),
    Check(
        name="decomposed-composite",
        applies=lambda relpath: relpath.endswith((".py", ".md", ".txt")),
        run=find_decomposed_composites,
    ),
)


def scan(repo_root, files=None, checks=CHECKS):
    """Run every applicable check over ``files`` (default: the whole source tree).

    Returns the offenses sorted by ``(relpath, line, codepoint)``.
    """
    if files is None:
        files = iter_source_files(repo_root)
    offenses = []
    for relpath in files:
        with open(os.path.join(repo_root, relpath), encoding="utf-8") as f:
            text = f.read()
        for check in checks:
            if check.applies(relpath):
                offenses.extend(check.run(relpath, text))
    offenses.sort(key=lambda o: (o.relpath, o.line, o.codepoint))
    return offenses


def format_offense(offense):
    """``path:line  U+XXXX NAME -- detail`` -- the actionable one-line report."""
    return (
        f"{offense.relpath}:{offense.line}  {offense.codepoint} {offense.uname}"
        f" -- {offense.detail}"
    )


def run(repo_root):
    """Scan and report; return the process exit code (0 clean, 1 dirty)."""
    offenses = scan(repo_root)
    if offenses:
        print("source hygiene offenses (see GitHub issues #22, #26):")
        for offense in offenses:
            print("  " + format_offense(offense))
        print(f"\n{len(offenses)} offender(s).")
        return 1
    print("source_hygiene: OK")
    return 0
