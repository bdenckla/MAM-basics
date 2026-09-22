# GitHub issue state, labels, and assignments

Read this reference before closing, reopening, relabelling, or reassigning an issue.

## 5. Closing, reopening, relabelling and reassigning

Closing, reopening, reassigning or relabelling a GitHub issue writes one line into its timeline:
the event, the account, the timestamp. **It records no reason, and it will not record one later.**
So the reason goes in a comment, posted with the change. Ben asks this of himself as much as of
agents, having been on the wrong end of it.

**Never close, or suggest closing, a GitHub issue until its work is both committed and pushed to
the remote.** Closing before pushing leaves the issue marked resolved while the fix is still only
local.

1. **Close** with `gh issue close <number> --repo bdenckla/<repo> --comment "<one line>"`, adding
   `--reason "not planned"` when the work will not be done. **Reopen** with `gh issue reopen` and
   the same `--comment`. Both take the comment only as an argument, so a reason longer than one
   line is posted first with `gh issue comment --body-file` (`references/reading-and-writing.md`,
   section 3), and the close or reopen
   follows it at once.
2. **Relabel or reassign** with `gh issue edit <number> --repo bdenckla/<repo>` and
   `--add-label`, `--remove-label`, `--add-assignee` or `--remove-assignee`, with a comment
   saying why.
3. **The account is not the actor, so the timeline cannot tell Ben and a session apart.** A
   session's `gh issue close` authenticates with Ben's personal token, so its event reads
   `actor: bdenckla`, `actor_type: User`, `performed_via_github_app: null` — byte for byte what
   his own click in the web UI produces. Do not infer from a timeline entry that a human did
   something, or that a session did; the only honest reading is "this account did it."
4. **The worked case, 2026-08-27: MAM-basics #260.** It was closed at 11:19 local with no comment.
   An hour later the work it tracked completed. Nothing on the issue said whether it had been
   closed because the *question* was answered — `skadish1` had answered it at 00:05 — or because
   the *work* was done, and those are different definitions of done for that issue: its title
   says "Investigate and document sigil ב2" and its "Done when" is entirely about evidence and
   confidence, while the replacement of ב2 by ת451 was the consequence rather than the scope.
   Establishing merely that no session had closed it took a scan of **483 transcripts** across
   every project directory. A one-sentence closing comment would have cost nothing and answered
   it.
5. **Say when a comment is agent-written.** A commit carries a `Co-Authored-By` trailer, so
   commits are already attributed; issue comments and state changes have no such convention and
   are indistinguishable from Ben's. Put it in the text.
6. **This is the cheap half of a bigger question Ben decided against.** A separate GitHub machine
   account for agent use would make every action self-identifying, and he already runs exactly
   that pattern on Wikisource as `BDencklaBot`. On GitHub it is not worth it for attribution
   alone: ~20 repos to add a collaborator to, a second persona in front of `skadish1`, `gh auth`
   juggling whose failure mode is worse than the problem, and a possible paid seat for
   MAM-private. If he ever wants it, the reason will be **permission scoping** — an agent token
   that cannot force-push or delete — not attribution, which the comment fixes for free. A
   fine-grained PAT or a GitHub App would be the form, since an App's actions set
   `performed_via_github_app` and so are distinguishable without adding a second voice.
7. **Each of these is an outward-facing act**, item 1 of "Risk has two independent axes" in the
   common `~/.codex/AGENTS.md` body, so a report names it as one. Claude Code receives that body
   through `~/.claude/CLAUDE.md`.

This section stood in both full instruction bodies until 2026-09-14, under the heading "Never
change an issue's state without a comment saying why". The common body now keeps the pointer to
this skill.
