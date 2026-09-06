"""Generate gh-pages/MAM-simple/index.html, the product's root pointer to its README.

MAM-simple's former gh-pages/ tree held one page (versification-and-cantillation.html) and no
index.html until 2026-09-01, so its former Pages URL answered with GitHub's 404 rather than
with anything of ours. This emits the stub MAM-parsed's site carries at the same spot: a heading
and one sentence pointing at the README on github.com, which in turn links back to the page
served from gh-pages/MAM-simple/.

author_misc/mp_index.py is that MAM-parsed counterpart, and is deliberately not reused
here: it builds its body through mb_html and hands it to MAM-parsed's ClaimCollection
traversal, which MAM-simple has no equivalent of.  The two generators that already write
into MAM-simple -- versification_and_cantillation/generate_doc.py and
versification_differences/generate_doc.py -- are the shape followed instead, down to the
output_path / check_output_matches / write_output_if_changed trio that main_mam_simple.py's
doc step drives.

Regenerate from the repo root::

    .venv/Scripts/python.exe py/main_mam_simple.py doc-only
"""

from pathlib import Path

from mb_cmn import paths
from mb_cmn import provenance

_GENERATOR_FILE = Path(__file__)

# Served at https://bdenckla.github.io/MAM-basics/MAM-simple/ : MAM-basics' Pages workflow
# publishes gh-pages/ as the site root, so this file is the MAM-simple subtree's root document.
_OUTPUT_PATH = paths.repo_root() / "gh-pages" / "MAM-simple" / "index.html"

_README_URL = "https://github.com/bdenckla/MAM-basics/blob/main/MAM-simple/README.md"

# No stylesheet link, which is the one way this departs from MAM-parsed's index.html.
# That one links a site-wide style.css; gh-pages/MAM-simple/ has no site-wide
# stylesheet, versification-and-cantillation.css being that one page's own, deployed
# beside it by versification_and_cantillation/generate_doc.py.  A heading and one
# sentence do not earn a second stylesheet.
_TEMPLATE = """\
<!doctype html>
<!-- {comment} -->
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MAM-simple</title>
</head>
<body>
<h1>MAM-simple</h1>
<p>For the full project overview, see the
<a href="{readme_url}">README</a>.</p>
</body>
</html>
"""


def render_full_html() -> str:
    comment = provenance.generated_html_comment(_GENERATOR_FILE)
    return _TEMPLATE.format(comment=comment, readme_url=_README_URL)


def output_path():
    return _OUTPUT_PATH


def check_output_matches() -> bool:
    # Guarded on exists(), unlike the two neighbouring generators, whose outputs have
    # always been there: this one's output is absent until its first run.
    if not _OUTPUT_PATH.exists():
        return False
    return _OUTPUT_PATH.read_text(encoding="utf-8") == render_full_html()


def write_output_if_changed() -> bool:
    actual = render_full_html()
    if check_output_matches():
        return False
    # MAM-simple's line-ending policy is LF (.gitattributes eol=lf); write LF
    # directly so the Windows working tree matches and doesn't churn.
    _OUTPUT_PATH.write_text(actual, encoding="utf-8", newline="")
    return True
