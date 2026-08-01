"""wlc-utils binding of the repo-agnostic ``mb_cmn.provenance`` helpers.

The vendored provenance functions take an optional ``repo_name`` for the
top-level breadcrumb segment.  These thin wrappers supply this repo's logical
name (``wlc_paths.REPO_NAME``) once, so generated-artifact breadcrumbs read
``wlc-utils/...`` even when the checkout dir is a git worktree rather than
literally ``wlc-utils``.

Import this in place of ``mb_cmn.provenance`` -- ``import wlc_provenance as
provenance`` -- and call as before; the call sites stay unchanged.
"""

from __future__ import annotations

import wlc_paths
from mb_cmn import provenance as _provenance


def generated_by_text(generator_file: str) -> str:
    return _provenance.generated_by_text(generator_file, wlc_paths.REPO_NAME)


def generated_html_comment(generator_file: str) -> str:
    return _provenance.generated_html_comment(generator_file, wlc_paths.REPO_NAME)


def with_json_provenance(root, generator_file: str):
    return _provenance.with_json_provenance(root, generator_file, wlc_paths.REPO_NAME)
