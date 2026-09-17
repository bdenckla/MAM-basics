---
name: github-issues
description: Ben's rules for reading, filing, commenting on, editing, closing, reopening, relabelling, reassigning, or citing GitHub issues. Use for any issue operation, for issue citations whose tracker could be ambiguous, and whenever filing an issue or offering to file one comes up.
---

# GitHub issues

Load the reference for the requested operation before touching GitHub. These rules apply
throughout:

1. Every `gh issue` command names its repository with `--repo bdenckla/<repo>`.
2. `gh` acts through Ben's account. Every issue, comment, body edit, or state-change comment
   written by a session says that it is agent-written and gives the date.
3. Multi-line issue text is written to a uniquely named UTF-8 file in a gitignored scratch
   directory and passed with `--body-file`. Never use stdin, a here-document, a PowerShell
   here-string, `--edit-last`, or `--delete-last`.
4. Do not file an issue for an idea Ben did not ask to pursue, and do not offer to file one.
   Say the idea in the conversation and stop.

## Route by operation

- **Read, file, comment, or correct an open issue body:** read
  `references/reading-and-writing.md`. A full read uses
  `gh issue view <number> --repo bdenckla/<repo> --json title,state,labels,body,comments`.
  Additions and corrections to closed issues are comments. Only a stale fact in an open
  issue's body is corrected in place, through MAM-basics'
  `py/main_github_issue_edit.py` procedure.
- **Close, reopen, relabel, or reassign:** read `references/state-changes.md`. Post a comment
  saying why as part of the act; the timeline event records no reason.
- **Write or audit citations:** read `references/citations.md`. A bare `#NN` is meaningful only
  in a repository-defined context. In cross-repository prose, name the repository. In a GitHub
  issue or comment, link another repository's issue with its full URL. Never let a non-issue
  number render as an issue link.
- **Audit, migrate, or interpret MAM-basics citations:** also read
  `references/mam-basics-trackers.md`. That reference carries the collision history, evacuated
  tracker exceptions, and data-rendering traps that do not belong in every issue task.

## Canonical copy

This skill is canonical at `MAM-basics/dot-claude/skills/github-issues/` and is shared with
Codex through `dot-claude/shared-skills.txt`. Change the canonical copy first, then use the
deployment procedure in `dot-claude/README.md`. The common user-wide instruction body keeps only
the conversation-level rules and a pointer here. Codex loads that body from
`~/.codex/AGENTS.md`; Claude Code imports it through `~/.claude/CLAUDE.md`.
