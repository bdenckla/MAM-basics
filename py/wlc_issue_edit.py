"""Edit a GitHub issue body without letting a file become the source of truth.

Editing an issue by hand goes: fetch the body to a scratch file, edit the file, push it back
with ``gh issue edit --body-file``.  The trap is the gap between fetch and push.  Anything that
touched the issue in between is silently reverted, and nothing in the mechanism notices --
``gh`` will happily write a body captured an hour and three edits ago.  Scratch snapshots also
accumulate under near-identical names (``issue69_body.md`` beside ``issue_69_body.md``), so a
later session cannot tell which one is current and picks wrong.

The cure is not tidier filenames.  It is to stop the file being the source: fetch, mutate in
memory, and push, all in ONE process, so the body written back is derived from the body just
read.  The file this module writes is a byproduct -- one fixed path per issue, overwritten
every time, valuable only for reading back what was sent::

    from wlc_issue_edit import fetch_body, replace_once, write_and_edit

    body = fetch_body(69, repo="wlc-utils")
    body = replace_once(body, anchor, anchor + addition)
    write_and_edit(69, body, repo="wlc-utils")

WHICH TRACKER IS AN ARGUMENT, NOT AN INHERITED CWD.  ``gh`` resolves which repo
"issue <number>" names from the git checkout it runs in, so this module used to pass
``cwd=<the wlc-utils root>`` to pin it.  That worked while there was one tracker to
pin to.  There are now two: wlc-utils keeps issues 1-88 where they are, and everything
new is filed in MAM-basics, so NEITHER root is a safe default and a plausible-looking
``#69`` names a different issue in each.  ``repo`` is therefore required and travels to
``gh`` as ``--repo bdenckla/<name>``.  An explicit argument cannot silently edit the
wrong tracker; an inherited cwd can.

The byproduct path carries the repo for the same reason -- one ``issue-69-outgoing.md``
for two trackers would reintroduce, in the scratch directory, exactly the ambiguity the
argument removes.  It is written under this repo's ``.novc/``, the code root, because
what it is a byproduct OF is an issue edit, not the wlc-utils corpus.

:func:`replace_once` is what actually makes this safe.  A plain ``str.replace`` that matches
nothing returns the string unchanged, so a stale anchor -- the exact symptom of someone else
having edited the issue -- sails through and the edit silently does nothing.  Matching twice is
just as bad in the other direction.  So the anchor must match exactly once or it raises.

Bodies are fetched through ``gh --json`` and decoded as UTF-8 from captured output.  Never pipe
issue text through a subprocess's stdin: Python decodes stdin with ``surrogateescape``, and a
lone surrogate from Hebrew text then raises on re-encode -- which has silently pushed an empty
body to a GitHub issue before.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from mb_cmn import paths

_OWNER = "bdenckla"
_OUT_DIR = paths.novc_dir()


class IssueEditError(RuntimeError):
    """An issue edit was refused because it could not be shown to be safe."""


def _repo_slug(repo: str) -> str:
    """``gh``'s ``--repo`` value for a bare repo name, or a slug passed through."""
    return repo if "/" in repo else f"{_OWNER}/{repo}"


def outgoing_path(number: int, repo: str) -> Path:
    """The one fixed path this issue's outgoing body is written to, and overwritten at.

    One path per (repo, issue), never a fresh name per attempt: a pile of near-identical
    snapshots is the failure this module exists to prevent, so the byproduct must not
    accumulate either.  The repo is in the name because two trackers both have an issue
    69.
    """
    return _OUT_DIR / f"issue-{_repo_slug(repo).replace('/', '-')}-{number}-outgoing.md"


def fetch_body(number: int, *, repo: str) -> str:
    """Return the issue's current body, fresh from GitHub."""
    return _fetch_field(number, "body", repo=repo)


def fetch_title(number: int, *, repo: str) -> str:
    """Return the issue's current title, fresh from GitHub."""
    return _fetch_field(number, "title", repo=repo)


def _fetch_field(number: int, field: str, *, repo: str) -> str:
    result = subprocess.run(
        [
            "gh",
            "issue",
            "view",
            str(number),
            "--repo",
            _repo_slug(repo),
            "--json",
            field,
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    return json.loads(result.stdout)[field]


def replace_once(body: str, old: str, new: str) -> str:
    """Replace `old` with `new`, requiring exactly one occurrence.

    Raises :class:`IssueEditError` on zero matches (a stale anchor -- most likely the issue
    moved under you) or on several (an ambiguous anchor, where which one gets rewritten is
    accidental).  Both are the cases a bare ``str.replace`` would wave through.
    """
    count = body.count(old)
    if count != 1:
        what = "no match" if count == 0 else f"{count} matches"
        raise IssueEditError(
            f"anchor has {what}, expected exactly 1; refusing to edit.\nAnchor: {old!r}"
        )
    return body.replace(old, new)


def write_and_edit(number: int, body: str, *, repo: str, dry_run: bool = False) -> Path:
    """Write `body` to this issue's fixed outgoing path and push it with ``gh``.

    Returns the path written, so a caller can read back exactly what was sent.  With
    `dry_run`, the file is written and nothing is pushed.
    """
    path = outgoing_path(number, repo)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8", newline="\n")
    if not dry_run:
        subprocess.run(
            [
                "gh",
                "issue",
                "edit",
                str(number),
                "--repo",
                _repo_slug(repo),
                "--body-file",
                str(path),
            ],
            check=True,
            text=True,
            encoding="utf-8",
        )
    return path
