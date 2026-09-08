"""Mechanical lint over the HTML and CSS files directly at the Pages deploy root."""

import subprocess
import sys

from mb_cmn import paths


def test_deploy_root_html_passes_the_local_checker():
    result = subprocess.run(
        [sys.executable, "py/check_html_syntax_and_sanity.py", "--deploy-root"],
        cwd=paths.repo_root(),
        capture_output=True,
        encoding="utf-8",
    )
    assert result.returncode == 0, result.stdout + result.stderr
