---
name: github-issues
description: Ben's rules for touching a GitHub issue — reading one in full, filing one, commenting on one, correcting a stale fact in an open issue's body with MAM-basics' py/main_github_issue_edit.py, closing, reopening, relabelling or reassigning one with a comment saying why, and citing issues so that no number links to the wrong tracker.
when_to_use: Load before any gh issue command that changes something — gh issue create, comment, edit, close or reopen — before reading an issue in order to work on it or answer about it, and whenever filing an issue comes up at all, since the skill says when not to file one or offer to. Not needed merely to cite an issue in a commit message or a document, which the repository's own CLAUDE.md covers.
---

Ben, 2026-09-14, after a session added a cross-link to MAM-basics #278 by editing the issue's body:
*"why edit an existing comment (the primary comment in this case) for something like this? It
seems way more appropriate (and procedurally easier) to add a comment!"* The rules for touching an
issue were then spread across both user-wide instruction files, MAM-basics' `CLAUDE.md`, a module
docstring and local memory notes, and that session had applied one of them to a case it does not
cover. This skill states them in one place, in six sections; Ben approved its shape the same day.

Two things hold throughout:

1. **Every `gh issue` command names its repository**, `--repo bdenckla/<repo>`. Without it `gh`
   resolves a bare number from the checkout it runs in, and the trackers' numbers collide:
   MAM-basics #69 is a CSS URL, while wlc-utils#69 is the hand transcriptions.
2. **Everything a session does on GitHub is done as Ben.** `gh` runs with his token, so an issue,
   a comment or a state change shows his account, `bdenckla`, exactly as his own would. Only the
   text can say that an agent wrote it, so it always does (sections 2, 3 and 5).

## 1. Reading an issue in full

1. Read an issue you are about to work on, comment on or edit with one command:

   ```
   gh issue view <number> --repo bdenckla/<repo> --json title,state,labels,body,comments
   ```

2. **Each plain form hides half the issue when its output is captured**, as an agent's always is.
   `gh issue view` prints the body and a count such as `comments: 1` but not the comments' text,
   and `gh issue view --comments` prints the comments but not the body. Measured on MAM-basics
   #263: the plain form on 2026-09-13, and both forms on 2026-09-14 with gh 2.86.0. Additions go
   in comments (section 3), so a body read without its comments is not the issue as it now
   stands.
3. **Issue text reaches a script as captured output, never through stdin.** Run `gh` from the
   script with `capture_output=True` and `encoding="utf-8"`. Python decodes stdin with
   `surrogateescape`, and a lone surrogate from Hebrew text then raises on re-encode, which once
   pushed an empty body to a GitHub issue.

## 2. Filing an issue

1. **File no issue for an idea, and do not offer to file one.** Ben, 2026-09-12, declining an idea
   he found interesting: *"let's leave everything 'as is'. Don't even bother to record it as a
   GitHub issue."* His reason that day: *"I've tended to record all interesting ideas as GitHub
   issues and as a result I have so many GitHub issues I am overwhelmed and as a result I'm
   probably ignoring pressing work recorded as GitHub issues because I'm too scared to sort
   through all the non-pressing-but interesting ones to find the pressing ones."* So when an idea
   worth noting is not work he asked for, say it in the conversation and stop; an offer to file
   puts the sorting back on him. He added that labelling might largely solve the problem, but *"I
   just want to keep the total issue volume down, too"*, so a label is no licence to file more.
   An issue about work in flight is unaffected, and so is recording a decision where it belongs:
   a docstring, a `CLAUDE.md` section, a commit message.
2. **A new issue goes in `bdenckla/MAM-basics` or `bdenckla/MAM-private`, and nowhere else.** Ben,
   2026-08-26: *"I'm going to try to add no issues to trackers other than those for MAM-basics and
   MAM-private, just as I am, long-term, aiming to have no unarchived repos other than MAM-basics
   and MAM-private."* Commenting on and closing an existing issue in any other tracker is not
   filing one, and is how those trackers wind down. MAM-private's `CLAUDE.md`, "A new issue is
   filed here, wherever the old citations point", records this, and also which of the two a MAM
   change goes in: MAM-private when the mgketer comparison suggested it, MAM-basics otherwise.
   MAM-basics is public, so check a MAM-basics issue's text for anything about MAM-private's
   content before filing it.
3. **Open the body with an authorship line quoting what Ben asked for**, in the shape MAM-basics
   #272 uses: *"Written by a Claude session on 2026-09-11. Ben's instruction was: "…". Everything
   else below is that session's reconstruction."* A Codex session names itself.
4. **Whether a document gets an issue depends on the kind of document.** Ben approved this split
   on 2026-09-14.
   1. **A `doc/PLAN-*.md` file whose work is still to be done gets a thin pointer issue.** Ben,
      2026-09-12: *"Store this task away with our usual way: a detailed plan in the 'doc' folder
      and thin GitHub issue with a pointer to that plan."* Use MAM-basics #280's shape: the
      authorship line, a link to the plan on GitHub, and a summary of a few sentences. The link
      resolves only once the plan has been pushed to `main`. When the plan's `State:` line comes
      to read `executed`, close the issue with a comment saying so (section 5).
   2. **A `doc/review-findings-*.md` file gets no issue.** Its `State:` line carries open or
      closed. The thin tracking issues the reviews used to file were retired on 2026-09-01, and
      `py/repo_util/check_repo_standards.py`'s docstring records why, under "THE `State:` LINE ON
      doc/review-findings-*.md". A review that finds work somebody must do still files a real
      issue with a real body, as MAM-basics #233 is; the test is whether the issue says anything
      the review file does not.
5. **The title names the work or the question**, as a heading names its subject: "Retire the MAM
   Google Sheet pipeline", "Give the poetic scanner the prose scanner's fast path, about 5 s a
   mega run".
6. **File it with** `gh issue create --repo bdenckla/<repo> --title "<title>" --body-file <file>`,
   the body file written as section 3 says, and give Ben the URL `gh` prints.

## 3. Commenting on an issue

1. **A comment is for anything that adds to an issue, open or closed** — a cross-link, a related
   plan, a later finding, progress — **and for any correction to a closed issue**, which is a
   record. Ben, 2026-09-14, of the cross-link quoted at the top: *"It seems way more appropriate
   (and procedurally easier) to add a comment!"* He asked that that edit not be undone, so
   MAM-basics #278's body keeps its "Related: the mega speedup plan" section. A correction to an
   open issue edits the body instead (section 4).
2. **Open the comment with a line saying an agent wrote it**, such as *"Written by a Claude session
   on 2026-09-14, at Ben's request."* Item 5 of section 5 says why.
3. **Post it from a file**: `gh issue comment <number> --repo bdenckla/<repo> --body-file <file>`.
   1. Never pass a multi-line body as an argument, a shell here-doc or a PowerShell here-string,
      and never `--body-file -`, which reads stdin (item 3 of section 1). "Running scripts — no
      inline one-liners", in `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md`, is the general rule.
   2. Name the file for its one task, such as `.novc/issue272_plan_link_comment.md`, never a
      generic `comment.md` reused across jobs: a stale file from an earlier task gets posted,
      silently, in place of the one meant.
   3. Keep it in the repository's gitignored `.novc/` or in the session's scratchpad.
   4. When it holds pointed Hebrew, write it with a Python script, `encoding="utf-8"` and
      `newline="\n"`, copying the Hebrew from its source. The Write and Edit tools can reorder
      Hebrew combining marks into Unicode-normal order, and MAM-basics keeps MAM-normal order.
4. **Never `gh issue comment --edit-last` or `--delete-last`.** Both act on the last comment of
   the account `gh` runs as, and every session runs as Ben, so that comment can be his.

## 4. Correcting a stale fact in an open issue's body

1. **Edit a body only to correct an open issue**: a dead link, an umbrella issue that has since
   closed, a branch that has since been merged, a count that has since changed. Everything else
   is a comment (section 3). The reason, measured on MAM-basics #263 on 2026-09-13: a correcting
   comment sits exactly where the next session to work on the issue may not look, since captured
   `gh issue view` shows the body and not the comments. Ben accepted that on 2026-09-13 (*"go
   ahead, in that order"*). It is the split MAM-basics makes between a live plan, kept true in
   place, and a finished dated document, corrected in `<stem>-update.md`.
2. **End the corrected body with one line saying who edited it, when and why**, such as *"Edited on
   2026-09-14 by a Claude session, with Ben's approval, to correct …"*.
3. **Make the edit with MAM-basics' command**, from any directory:

   ```
   C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe C:/Users/BenDe/GitRepos/MAM-basics/py/main_github_issue_edit.py --repo <repo> --issue <number> --edits <file> [--dry-run]
   ```

   1. **The edits file** is UTF-8 JSON, `{"replacements": [{"old": "…", "new": "…"}], "note": "…"}`,
      where `note` is the line item 2 describes. Copy each `old` from the body as `--json body`
      returns it, and write the file as item 3.4 of section 3 says when it holds Hebrew.
   2. **The command** fetches the body, applies the replacements in order, requiring each `old` to
      occur exactly once, appends the note as the body's last paragraph, and pushes, all in one
      process, so nothing changed on GitHub in the meantime is lost. A stale or ambiguous `old`
      refuses the whole edit before anything is pushed.
   3. **`--dry-run`** pushes nothing and writes the new body to
      `.novc/issue-bdenckla-<repo>-<number>-outgoing.md` in MAM-basics. Read it, then run again
      without the flag.
   4. **After pushing**, the command reads the body back and exits 1 if it differs from that file.
4. **Never assemble a body edit by hand** from a fetched copy and `gh issue edit --body-file`.
   Anything changed on GitHub between the fetch and the push is silently reverted, and snapshots
   under near-identical names pile up until a later session picks the wrong one.
   `py/github_issue_edit.py`'s docstring is the fuller statement.

## 5. Closing, reopening, relabelling and reassigning

Closing, reopening, reassigning or relabelling a GitHub issue writes one line into its timeline:
the event, the account, the timestamp. **It records no reason, and it will not record one later.**
So the reason goes in a comment, posted with the change. Ben asks this of himself as much as of
agents, having been on the wrong end of it.

1. **Close** with `gh issue close <number> --repo bdenckla/<repo> --comment "<one line>"`, adding
   `--reason "not planned"` when the work will not be done. **Reopen** with `gh issue reopen` and
   the same `--comment`. Both take the comment only as an argument, so a reason longer than one
   line is posted first with `gh issue comment --body-file` (section 3), and the close or reopen
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
7. **Each of these is an outward-facing act**, item 1 of "Two axes of risk" in
   `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md`, so a report names it as one.

This section stood in both of those files until 2026-09-14, under the heading "Never change an
issue's state without a comment saying why", which stays there as a pointer to this skill.

## 6. Citing issues

1. **What a bare `#NN` means depends on where it is written.**
   1. In MAM-basics' files, and in MAM-basics' issues and comments, a bare `#NN` is a MAM-basics
      issue, and any other tracker's issue is written `repo#NN`, such as `wlc-utils#88`.
      MAM-basics' `CLAUDE.md`, "Five issue trackers", lists the collisions that make the prefix
      necessary.
   2. In MAM-private, a bare `#NN` inside an evacuated tree such as `mgketer/` means that tree's
      own tracker, and MAM-private's own issues are always written `MAM-private#NN`. MAM-private's
      `CLAUDE.md`, "Issue citations", is the statement.
   3. In this skill, and anywhere a reader could be in either repository, write the repository
      out: "MAM-basics #263".
2. **In an issue or a comment, give another tracker's issue as its full URL**,
   `https://github.com/bdenckla/<repo>/issues/<number>`. GitHub turns a bare `#NN` there into a
   link to the same repository's issue, whatever was meant.
3. **Never write a bare `#NN` for a number that is not an issue**, whether in a file, an issue or
   chat. The Claude desktop app turns a bare `#NN` in chat into an issue link, and does it
   inconsistently: of `(#83, #109, #115) plus #161`, written identically, only the middle two
   became links (2026-09-04). Ben, that day: *"at a minimum, prevent a wrong link (a link to an
   unrelated (or even worse, related!) github issue) from being generated at render-time!"* Give
   such a number a form no renderer reads as an issue: a UXLC change as its change id,
   `2026.02.05-109`; a Yeivin section as "ITM section 194"; a design-document item as "design doc
   §9 item 6".

## Where these rules came from, and where a change goes

1. **`~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md`**, tracked in MAM-basics as
   `dot-claude/user-wide-CLAUDE.md` and `dot-Codex/user-wide-AGENTS.md`: section 5 moved here from
   them on 2026-09-14. Both keep a pointer under the old heading, and a two-sentence section, "No
   GitHub issue for an idea, and no offer to file one", because that rule has to act in
   conversation before anything loads a skill.
2. **Two local memory notes of Claude's MAM-basics project**, deleted on 2026-09-14 once this
   skill held them: one on correcting an open issue's body, now sections 1, 3 and 4, and one on
   not filing issues for ideas, now item 1 of section 2.
3. **MAM-basics' `CLAUDE.md`**, "Five issue trackers", and **MAM-private's `CLAUDE.md`**, "Issue
   citations" and "A new issue is filed here, wherever the old citations point": item 2 of
   section 2, and section 6. Those files stay the statement of record for their repositories.
4. **`py/repo_util/check_repo_standards.py`'s docstring**: item 4 of section 2.
5. **`py/github_issue_edit.py` and `py/main_github_issue_edit.py`**: section 4. The module was
   `py/wlc_issue_edit.py` until 2026-09-14.

A rule change goes into this skill first. Its canonical copy is
`MAM-basics/dot-claude/skills/github-issues/`, and it is shared with Codex: a change reaches
`~/.claude/skills/github-issues/` and `~/.agents/skills/github-issues/` by the procedure in
`MAM-basics/dot-claude/README.md`. It is not installed in a Claude cloud session, by Ben's decision
of 2026-09-14, and a session there can read it in the checkout.
