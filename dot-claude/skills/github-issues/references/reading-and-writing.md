# Reading, filing, commenting, and correcting GitHub issues

Read the sections needed for the requested operation before touching GitHub.

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
      inline one-liners", in the common `~/.codex/AGENTS.md` body imported by Claude Code through
      `~/.claude/CLAUDE.md`, is the general rule.
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

## 5. Correcting references before a tracked document is retired

1. Audit issue bodies and comments before deleting the document. Classify each reference as
   current guidance or historical evidence. Repoint current guidance to a current successor; if
   no successor exists, the reference blocks deletion. Repoint historical evidence to the full
   40-character SHA of the last commit whose tree contains the document.
2. A base receipt and its optional one live `<stem>-update.md` are one retirement family. Verify
   both members at the archival SHA and link both so the correction sequence remains visible.
   Never create a numbered update sibling. A historical numbered sibling found at the archival SHA
   remains part of that historical family and must also be verified and linked; its literal
   preservation does not make numbered siblings current policy. Never use `blob/main`, a branch, a
   tag, a short SHA, or the deletion commit whose tree lacks the files.
3. If the stale reference is in an open issue body, correct that body with
   `py/main_github_issue_edit.py`, first with `--dry-run`, exactly as section 4 requires.
4. If the issue is closed, or if the stale reference is in any comment, add a new dated
   agent-written correction comment with the current-successor or immutable-historical link from
   item 1. Never edit or delete the existing comment. Read the complete issue back after the
   change.
