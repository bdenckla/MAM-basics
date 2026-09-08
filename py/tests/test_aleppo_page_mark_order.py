"""Mechanical MAM-mark-order lint over the owned Aleppo HTML page family."""

import re
import subprocess

from mb_cmn import paths, uni_denorm

_HEBREW_RUN_RE = re.compile(r"[\u0590-\u05FF\u034F\uFB1E]+")
_HEBREW_LETTER_RE = re.compile(r"[\u05D0-\u05EA]")


def _tracked_aleppo_pages() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "--", "gh-pages/aleppo/*.html"],
        cwd=paths.repo_root(),
        capture_output=True,
        encoding="utf-8",
        check=True,
    )
    return [name for name in result.stdout.splitlines() if name]


def test_owned_aleppo_page_family_uses_mam_mark_order():
    pages = _tracked_aleppo_pages()
    assert len(pages) > 2, f"Aleppo page coverage disappeared: {pages}"

    run_count = 0
    offenders = []
    for rel in pages:
        text = (paths.repo_root() / rel).read_text(encoding="utf-8")
        for line_no, line in enumerate(text.splitlines(), 1):
            for match in _HEBREW_RUN_RE.finditer(line):
                run = match.group()
                if not _HEBREW_LETTER_RE.search(run):
                    continue
                run_count += 1
                if not uni_denorm.has_std_mark_order(run):
                    offenders.append(f"{rel}:{line_no}")

    assert run_count > 400, f"Only {run_count} Aleppo-page Hebrew runs were checked"
    assert not offenders, f"Aleppo pages contain non-MAM mark order: {offenders}"
