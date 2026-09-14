"""Correct a stale fact in an open GitHub issue's body: fetch, replace, push, in one process.

Run with MAM-basics' interpreter, from any directory -- every path here is
resolved from this file, never from the cwd:

    C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_github_issue_edit.py --repo <repo> --issue <number> --edits <file> [--dry-run]

--repo is a repository name, standing for bdenckla/<name>, or an owner/name
slug.  It is required because gh otherwise resolves a bare issue number from
the checkout it runs in, and the trackers' numbers collide.

THE EDITS FILE is UTF-8 JSON with two keys:

    {
      "replacements": [{"old": "<text now in the body>", "new": "<its replacement>"}],
      "note": "<one line saying who edited the body, when and why>"
    }

The replacements are applied in order to the body as just fetched, and each
"old" must occur exactly once in the body as it stands when that replacement is
reached.  A stale or ambiguous "old" refuses the whole edit before anything is
pushed.  The note becomes the body's last paragraph.  Copy each "old" from the
body as `gh issue view --json body` returns it, and write the file with a
script when it holds Hebrew, since the Write tool can reorder Hebrew marks.

WHAT IT WRITES.  The new body goes to one fixed path per issue under this
repository's .novc/, issue-<owner>-<repo>-<number>-outgoing.md, overwritten on
every run.  With --dry-run nothing is pushed, and that file is the edit to read
before running again without the flag.  After a push the body is read back from
GitHub, and the run exits 1 if it differs from that file.

WHEN TO USE IT.  Only to correct a stale fact in an open issue.  An addition to
an issue, and any correction to a closed one, is a new comment instead; the
github-issues skill, canonical at dot-claude/skills/github-issues/SKILL.md, sets
out which is which.  The mega never runs this program, since a run would edit
an issue on GitHub, and py/tests/test_mega_coverage.py declares it.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import github_issue_edit


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    args = _build_parser().parse_args()
    replacements, note = _read_edits(Path(args.edits))
    body = github_issue_edit.fetch_body(args.issue, repo=args.repo)
    for old, new in replacements:
        body = github_issue_edit.replace_once(body, old, new)
    body = f"{body.rstrip()}\n\n{note}\n"
    path = github_issue_edit.write_and_edit(
        args.issue, body, repo=args.repo, dry_run=args.dry_run
    )
    if args.dry_run:
        print(f"Dry run, nothing pushed.  The new body is in {path}")
        return
    if github_issue_edit.fetch_body(args.issue, repo=args.repo) != body:
        print(
            f"Pushed, but the body now on GitHub differs from {path}; compare the two.",
            file=sys.stderr,
        )
        sys.exit(1)
    print(f"Edited the body of issue {args.issue} of {args.repo}, as sent in {path}")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--repo",
        required=True,
        help="a repository name, e.g. MAM-basics, or owner/name",
    )
    parser.add_argument("--issue", required=True, type=int, help="the issue's number")
    parser.add_argument(
        "--edits", required=True, help="the edits file, as THE EDITS FILE describes"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="write the new body and push nothing"
    )
    return parser


def _read_edits(path: Path) -> tuple[list[tuple[str, str]], str]:
    """The replacements and the note, refusing a file that lacks either."""
    edits = json.loads(path.read_text(encoding="utf-8"))
    replacements = [(each["old"], each["new"]) for each in edits["replacements"]]
    note = edits["note"].strip()
    if not replacements:
        raise github_issue_edit.IssueEditError(
            "the edits file has no replacements; an addition is a comment, not a body edit"
        )
    if not note or "\n" in note:
        raise github_issue_edit.IssueEditError(
            "the edits file's note must be one line saying who edited the body, when and why"
        )
    return replacements, note


if __name__ == "__main__":
    main()
