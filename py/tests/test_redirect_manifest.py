"""Guard: every frozen redirect URL still has its declared published target.

WHY THIS IS A TEST AND THE REST OF THE LINT IS NOT

``py/main_redirect_stubs.py check`` lints each source repo's stub tree, and it cannot run
here without a clone. One of its four checks needs no stub tree at all, because both sides
are available without a redirect-host clone -- the frozen old-to-target mapping and the
target repository's tracked published pages. That check is the one hoisted here, so it
runs whenever the repository test suite runs, rather than being left in a program
nothing schedules and nothing can currently run.

WHAT BREAKS IT, AND WHY THAT MATTERS

Most stubs send an old URL to a MAM-basics subtree at the same relative path, a pure
prefix rewrite. A row can instead declare an explicit old-path-to-target-path mapping in
another maintained repository. Both contracts keep working only while the declared
target page remains published. Rename or drop that page and the stub keeps redirecting
to a URL that 404s. Nothing in the target tree knows the manifest exists, so the break
is silent, and it is exactly the shape ``py/tests/test_vendoring_policy_paths.py`` was
written for after a manifest went stale unnoticed for a day. That lint was deleted with
the vendoring audit on 2026-09-14.

The repair is a decision rather than a rewrite, which is why this reports rather than
fixes: republish the declared target, deliberately remap the old URL to another maintained
target, or, if the content is genuinely gone, drop the old URL from the manifest and delete
its stub in the source host, accepting that an old citation now lands on ``404.html``.

A MISSING, MALFORMED OR EMPTY MANIFEST FAILS, IT DOES NOT SKIP.
``stubs.redirect_targets`` validates and rejects each case, so none can report green
having verified nothing.

IN A CLOUD CONTAINER, THE HBOFONTS ROW CHECKS ITS MANIFEST AND SKIPS THE REST. Ben's
decision, 2026-09-26. The Taamey_D row's declared target repository is hbofonts, a private
sibling that ``stubs.published_pages`` reads through ``paths.require_sibling``, and a cloud
container cannot clone it: a container run of the suite on 2026-09-25, recorded in the message
of ``ee0d66d5``, failed that row and no other test. So in a container the row still reads and
validates its manifest, which is tracked here, and skips only before reading hbofonts. This
follows ``py/tests/test_final_stress_vs_phonetic_mam.py``, which skips in a container the tests
that read MAM-private. Like that module, it asks ``graphviz_pin.in_cloud_session()``, the
repository's one cloud predicate, so the read is skipped in a container whether or not hbofonts
is attached there. On any machine of Ben's the sibling stays REQUIRED, and a missing hbofonts
fails here as before. The rows whose target is MAM-basics read only this repository and run
everywhere. The skip's reason string is what tells it apart from a semantic skip under ``-rs``.
"""

from __future__ import annotations

import pytest

from mb_cmn import graphviz_pin
from mb_cmn import paths
from redirect_stubs import stubs

_HBOFONTS_CLOUD_SKIP = (
    "cloud container: this row's target, the private hbofonts sibling, cannot be cloned"
    " here -- an environment skip, not this suite's semantic skip"
)


def _cloud_skip_reason(repo: stubs.RedirectRepo) -> str | None:
    """Why ``repo``'s published target cannot be read in this process, or None.

    Dispatches on each target repository that ``stubs.RedirectRepo`` accepts and raises on
    any other, so a new target repository cannot run here without a decision about it.
    """
    if repo.target_repo == "MAM-basics":
        return None
    if repo.target_repo == "hbofonts":
        return _HBOFONTS_CLOUD_SKIP if graphviz_pin.in_cloud_session() else None
    raise ValueError(
        f"{repo.source_repo}: no cloud rule for target repository {repo.target_repo!r}."
    )


@pytest.mark.parametrize(
    "repo", stubs.REDIRECT_REPOS, ids=lambda repo: repo.source_repo
)
def test_every_frozen_url_has_a_published_target(repo: stubs.RedirectRepo) -> None:
    targets = stubs.redirect_targets(paths.repo_root(), repo)
    skip_reason = _cloud_skip_reason(repo)
    if skip_reason is not None:
        pytest.skip(skip_reason)
    published = set(stubs.published_pages(paths.repo_root(), repo))
    declared_targets = set(targets.values())
    if repo.not_found_target is not None:
        declared_targets.add(repo.not_found_target)
    gone = sorted(target for target in declared_targets if target not in published)
    assert not gone, (
        f"{len(gone)} targets declared in {repo.manifest_path} are no longer published"
        f" by {repo.target_repo} under {repo.pages_prefix}, so {repo.source_repo}'s"
        f" corresponding stubs redirect to URLs that 404: {gone}. Republish each target"
        " at that exact path, or make a deliberate manifest and source-host change that"
        " preserves the old citation."
    )
