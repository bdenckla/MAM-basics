# Updates to checkout kinds and portable knowledge

State: open, first entry 2026-09-29.

## 2026-09-29: recommendations for the deferred knowledge and cloud-skill decisions

Recorded by Codex. This entry addresses the base receipt's passages beginning
“Deferred proposal — new lessons” and “Deferred proposal — cloud skills” under
“Decisions for Ben”. The opening continuation prompt was prepared by the preceding Codex
session; its reconstruction is not evidence that Ben approved either proposal.

**Effective base State:** executed 2026-09-29 for Workstreams A and B. Decisions 6 and 7
were deferred when this investigation began. Ben approved Decision 6's narrow rule and
Decision 7's six-skill installation with cloud limits below. The historical “Fresh-session handoff” has been executed;
“Secondary forests created and verified” remains the completion evidence. This investigation
does not repeat forest setup, suite, mega or environment verification.

**Verified checkout:** source, development and final integration are the full clone
`C:/Users/BenDe/GitRepos/MAM-basics`, clean `main` at required commit
`eea4c583f12ee90f75003dd4c75be5d6d52f7c85` before editing. The root, HEAD, branch and
NUL-delimited status were checked; the ancestry check passed because HEAD equals the required
commit. Any later implementation uses this clone's own
`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe` from its repository root.
Codex root owns write-back, verification, integration and deployment. A delegated agent audited
the six shared skills read-only; Codex root inspected the material implementation claims.
Required instructions are the common body and repository `AGENTS.md`. Required skills are
`iterative-document-editing`, `mam-repository-topology` with its routed references,
`github-issues` with the relevant operation references, and `hebrew-prose` with its MAM-basics
reference before editing that skill's prose. Read `doc/clone-forests.md`, both configuration
READMEs and the affected canonical skill references before approved implementation.

### Decision 6: approval for new reusable lessons

**Approved by Ben on 2026-09-29:** require approval for a newly inferred reusable
lesson outside the authorized task's scope. Continue recording approved decisions, verified
task outcomes and necessary documentation corrections as part of the authorized work.

The base's proposed “commit only when Ben says yes” is too broad unless “new lessons” is
defined. `dot-Codex/user-wide-AGENTS.md`, “Git and commits”, currently says “Commit finished
work without asking.” Its “Memory retirement” section routes maintained knowledge to owning
tracked instructions, skills or documents. Neither passage currently grants an inferred lesson
special policy status or imposes a general knowledge-edit approval gate. A gate on every
documentation commit would also interrupt the required same-commit phase records in
`iterative-document-editing`.

The proposed addition to the common instruction body is:

> When a session identifies a new reusable lesson outside the authorized task's scope, propose
> the owning tracked file, the exact text and its supporting evidence, and wait for Ben's
> approval before applying the edit. Record Ben's explicit decisions, verified task outcomes
> and documentation changes needed to complete authorized work within that work's existing
> authorization. Commit finished authorized work without asking again.

This is a narrow scope rule, rather than a second approval for an already authorized
commit. Ben chose “Approve the narrow rule (Recommended)” in reply to the exact proposal on
2026-09-29. The canonical common body now contains the approved paragraph under “New reusable
lessons”. Its ordinary commit, push and canonical deployment belong to that authorized change.

### Decision 7: make all six shared skills available as cloud instructions

**Approved by Ben on 2026-09-29:** install all six declared shared skills after
adding explicit cloud applicability and runtime requirements. Skill availability supplies the
rules for a requested act; it does not establish that the act's dependencies or permissions
are available. In particular, the refresh rules prevent a cloud session from treating partial
regeneration as a completed refresh, and the issue rules remain useful for citations and
agent-written text when a particular issue command cannot run.

`dot-claude/shared-skills.txt` declares six skills. Local deployment in
`py/repo_util/user_config_sync.py`, `_build_mappings`, sends every Claude skill to Claude and
the declared shared skills to Codex. The cloud hook has a different inventory:
`.claude/hooks/install-user-config.sh`, “WHAT IS INSTALLED”, copies only the common body,
Claude wrapper and `hebrew-prose`. Its absence checks, source checks and banners all name
that one skill. `.claude/settings.json` invokes the hook on startup, resume and compaction.

The hook's exclusions for `verse-links` and `github-issues` still describe absolute Windows
command paths. Their skill command recipes now use the selected checkout. Other runtime
obstacles remain, and `mam-wikisource-refresh/SKILL.md` still names the desktop interpreter.
Removing every Windows path is not an appropriate readiness test: historical measurements
and named local source locations can remain useful evidence, while a relative command can
still depend on unavailable private inputs or an unsupported API.

| Shared skill | Cloud applicability and actual requirements | Proposed disposition |
| --- | --- | --- |
| `hebrew-prose` | Its prose rules already apply and are already installed. `references/sources-and-corpora.md` identifies private OCR and account-local source books. `references/verifying.md`, “Commands”, includes Windows interpreter recipes and distinguishes private surveys from rendering with tracked surveys. Missing source material limits research claims. | Keep installed; add a cloud runtime/source-availability clause and correct active interpreter recipes without rewriting dated evidence or copying private material. |
| `iterative-document-editing` | Planning, approval, cumulative revisions, receipt updates and one-writer ownership use tracked text. The skill has no mandatory private input or executable runtime. | Install unchanged. |
| `mam-repository-topology` | The roster and evacuated-repository rules are useful in a shallow cloud checkout. Forest sweeps and retirement require other checkouts, runtime ownership records and local recovery facilities described in its references. | Install with an explicit clause distinguishing a cloud checkout from a full clone forest; preserve unavailable-operation limits. |
| `verse-links` | “Running the command” requires the selected checkout and says the command needs only tracked MAM-basics data, with no network or sibling. `py/main_verse_links.py` and its imports read that data. The skill still shows a Windows `.venv/Scripts/python.exe` command; Python and required packages must be present in the cloud environment. | Install with a Linux interpreter recipe and environment discovery; keep link generation through the existing entry point. |
| `github-issues` | Citation, authorship, issue-routing and state-change rules are portable. The prescribed full read and `py/github_issue_edit.py` use `gh issue view`; the body edit uses `gh issue edit`. Access is limited to attached repositories, and the current cloud proxy has GraphQL restrictions. | Install with a cloud transport/capability clause. Support a complete REST read, including all comment pages. Keep body edits unavailable under the restricted proxy while the required helper has no REST transport; preserve the helper requirement and report the limitation. |
| `mam-wikisource-refresh` | Public downloading needs the checkout's Python dependencies and Wikisource network access. A changed chapter requires the full MAM-basics → MAM-private → phonetic-hbo → MAM-basics loop in `references/dependent-refresh.md`, including owned downstream checkouts and their environments. The ordinary one-repository cloud checkout cannot complete that loop. | Install with a preflight that stops before starting a chapter refresh when the required dependency loop is unavailable. A cloud mega with declared skips does not establish refresh completion. Correct the remaining desktop-only active command recipes. |

`py/subcommands/download_wikisource.py`, `run`, calls `parse_ws.almost_main` after the
downloads. Starting a download can therefore regenerate local products before the later
dependency preflight in the current skill. The proposed cloud preflight must precede the
download, rather than first checking private prerequisites after a public-side commit.

Anthropic's current [cloud-environment documentation](https://code.claude.com/docs/en/cloud-environments#github-proxy)
describes attached-repository API scope, a restricted GraphQL operation set and REST fallback.
Its [GitHub-tools section](https://code.claude.com/docs/en/cloud-environments#work-with-github-issues-and-pull-requests)
documents `gh` and proxy authentication. GitHub CLI's
[issue lookup](https://github.com/cli/cli/blob/trunk/pkg/cmd/issue/shared/lookup.go),
`FindIssueOrPR`, calls GraphQL, and its
[issue update](https://github.com/cli/cli/blob/trunk/pkg/cmd/pr/shared/editable_http.go),
`updateIssue`, does too. These sources were inspected on 2026-09-29. The inference is that the
current prescribed issue transport is not a reliable cloud path; this is not a measurement of
Ben's current cloud session or its installed `gh` version. The local helper has no REST fallback,
including for `--dry-run`. No issue operation was performed during this audit.

The proposed implementation has these boundaries:

1. Have the hook read and validate the shared-skill inventory, and copy each complete canonical
   skill tree into the cloud Claude skill home when absent. Preserve the remote guard,
   checked-out-branch source, existing files, network-free behavior and zero-exit failure
   reporting. Report each resource independently, including missing sources and incomplete
   copies. Continue excluding Claude-only pruning and Codex-only skills. A future inventory
   addition requires the same applicability audit.
2. Update the four skills needing runtime or capability clauses, plus `hebrew-prose`'s active
   command guidance, at their canonical homes. Provide the cloud REST full-read procedure in
   `github-issues`; the existing body-edit helper and its unavailable cloud transport remain
   explicit. Installing the skill does not enable a substitute ad hoc issue-body rewrite.
3. Keep `dot-Codex/user-wide-AGENTS.md`, “Claude Code only: cloud SessionStart installation”,
   both `dot-*/README.md` files and the maintained cloud-setup description consistent with the
   expanded inventory. Later status belongs in the existing cloud-setup update. Retain the
   2026-09-14 exclusion as a dated decision superseded only if Ben approves this proposal.
4. Provision no dependencies, credentials, permission/trust settings or sibling clones in the
   configuration-copy hook. REST support for issue-body edits is separate executable work,
   outside this proposed installation scope. A real cloud startup and supported-command check
   remains necessary before claiming cloud runtime verification.

Ben chose “Install all six with these cloud limits (Recommended)” on 2026-09-29. This changes
instruction availability and runtime guidance; it does not make the private refresh loop or
every GitHub mutation cloud-capable.

### Verification and integration after a choice

Decision 6 changes instruction text only: inspect the exact diff, run `git diff --check`, commit
on this full clone's `main`, fetch origin, merge a moved `origin/main` and run the checks owed by
the merged content, then push normally. Deploy canonical configuration from freshly fetched
`origin/main` and run the deployment's `--check`. Approval of this implementation includes its
ordinary commit, push and required canonical deployment.

Decision 7 changes executable setup code without reaching a declared product or mega generator
in `py/product_scopes.py`. Run Git Bash's `bash -n` and a disposable fake-home differential
harness for the local no-op, empty home, existing destinations, incomplete skill tree, missing
inventory/source, source-not-needed, repository fallback, repeated run and partial-copy paths.
Compare complete installed trees to the canonical sources and verify that existing sentinel
files remain unchanged. Check that the hook invokes no network or workflow operation. Run the
full suite from this repository root with this clone's own interpreter after the final hook
change. Run `git diff --check`, inspect every changed path, commit, fetch/merge/check and push
normally. Deploy the changed canonical instructions and skills, then require a clean deployment
comparison. A Windows-hosted harness cannot verify actual Claude cloud loading or remote API
permissions; report those limits explicitly. No mega is owed by this proposed scope.

Run the hook syntax check from the verified source/development root:

```powershell
& 'C:/Program Files/Git/bin/bash.exe' -n .claude/hooks/install-user-config.sh
```

Run the suite after Decision 7's final executable change from that same root:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py
```

After an approved canonical change has been pushed, deploy from that root:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_repo_util.py --sync-user-config
```

Then check the same complete deployment:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_repo_util.py --sync-user-config --check
```

**Expected unchanged outputs:** all MAM products, generated pages, mirrors, font outputs and
private outputs. No Wikisource download or save, GitHub issue mutation, forest synchronization,
laptop operation, memory-backup disposal or worktree retirement is part of either proposal.

**Risk:** the planning write-back reaches no product; its only base-receipt change is the
prescribed update pointer and joining of the opening State paragraph. Approved implementation
would also involve a normal outward main push, canonical writes outside Git and a cloud code
path whose actual runtime cannot be exercised on this Windows machine. Those acts remain
separate from product reach.

### Cumulative disposition

| Requirement | Disposition |
| --- | --- |
| Workstreams A and B; both secondary forests | Implemented; completion evidence retained without repeating checks. |
| Investigate Decision 6 against current instructions | Implemented; exact proposed common text above. |
| Audit Decision 7 against hook, mapping, skills and runtime requirements | Implemented; static and primary-source evidence above. |
| Decision 6 policy choice | Implemented; Ben approved the exact narrow paragraph on 2026-09-29. |
| Decision 6 canonical implementation, push and deployment | Implemented; verification and deployment evidence below. |
| Decision 7 policy choice | Implemented; Ben approved the six-skill proposal with its stated cloud limits. |
| Decision 7 implementation and verification | Active under that approval. |
| Source-forest synchronization and other excluded work | Deferred outside this task's scope. |

**Planning write-back verification:** a scratch comparison against the required commit verified
that the base receipt differs only by the prescribed pointer and joining of its opening State
paragraph. NUL-delimited status contains only the base receipt and this update. `git diff --check`
passed. The investigation and Decision 6's instruction change owe neither suite nor mega.
Skills, executable hooks and products remain unchanged at this stage. Decision 6 was
presented to Ben first, following the one-independent-decision-at-a-time procedure; Decision 7
was presented after Ben approved Decision 6.

## 2026-09-29: Decision 6 implemented and deployed

Recorded by Codex. **Implemented:** Ben's exact narrow lesson rule is under “New reusable
lessons” in `dot-Codex/user-wide-AGENTS.md`. Commit
`7549ebf706ca6a098478fe0ea5e6a8cfd90866c0` contains that instruction change, this update and
the prescribed base-receipt pointer. It was pushed normally to `origin/main` after a successful
fetch showed no moved remote commit to merge.

**Passed:** the base-receipt comparison against the required commit, NUL-delimited ownership
check, unstaged and staged `git diff --check`, and exact paragraph inspection. No suite or mega
was owed by the instruction and documentation content. All products and executable hooks
remained unchanged.

**Deployed and verified:** the full canonical deployment fetched and sourced
`refs/remotes/origin/main@7549ebf706ca6a098478fe0ea5e6a8cfd90866c0`, changed two mappings
(the common instruction body and its generated fingerprint), and its subsequent `--check`
reported all 21 mappings clean with zero problems. Live files were changed only through that
repository deployment, never edited directly.

**Effective base State:** executed 2026-09-29 for Workstreams A and B and the approved
Decision 6 continuation. Decision 7 was still deferred at this deployment; its later approval
is recorded below. The cloud hook at that commit installs only `hebrew-prose`.
No excluded task or cloud workflow was performed.

## 2026-09-29: Decision 7 approved for implementation

Recorded by Codex. Ben replied “Install all six with these cloud limits (Recommended)” to the
concrete proposal above. This supersedes his 2026-09-14 cloud exclusion of `github-issues` for
instruction installation, with the approved capability limits preserved.

**Approval snapshot:** implement the hook inventory and copying behavior, canonical skill
runtime clauses and cloud REST full-read guidance described above. Expected changed paths are
`.claude/hooks/install-user-config.sh`, `dot-Codex/user-wide-AGENTS.md`, both configuration
READMEs, the canonical `github-issues`, `hebrew-prose`, `mam-repository-topology`,
`mam-wikisource-refresh` and `verse-links` skill trees, the maintained cloud-setup description,
its existing update and this update. The six-name shared inventory and
`iterative-document-editing` need no content change. Keep `py/github_issue_edit.py` and all
workflow executables unchanged. The verification and integration scope above is approved.
Source, development, integration and sole-writer ownership remain as recorded above; the
implementation baseline is the approved Decision 6 commit
`7549ebf706ca6a098478fe0ea5e6a8cfd90866c0` or its documentation-only descendant.

**Effective base State:** Decision 6 is implemented and deployed; Decision 7 is active under
Ben's explicit approval. Workstreams A and B stay complete. No excluded task is reopened.
