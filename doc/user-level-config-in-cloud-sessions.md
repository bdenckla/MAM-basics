# Getting `~/.claude/` into a cloud session

A cloud session — Claude Code on the web, `claude --cloud`, a routine, a Claude Tag session —
starts from a fresh clone of `bdenckla/MAM-basics` on an Anthropic-managed Ubuntu VM. Everything
tracked in this repository travels with that clone. **Nothing under `~/.claude/` does**, and until
2026-09-09 nothing said so.

Since 2026-09-09 the fix has two halves. `dot-claude/` and `dot-Codex/` hold the
version-controlled originals of Ben's user-level Claude and Codex configuration, so they arrive
with the clone; and `.claude/hooks/install-user-config.sh`, wired in by `.claude/settings.json` as
a `SessionStart` hook, copies two of them into `~/.claude/` when that directory lacks them.

This file records the gap and how it was measured, why the configuration is stored here rather
than in `github-misc`, the one sentence that was redacted on the way in, and how the hook is
gated.

## The gap, and how it was measured

Verified in a remote session on 2026-09-09, before the hook existed:

1. `find / -name CLAUDE.md` returned nothing outside the checkout. The user-level
   `~/.claude/CLAUDE.md` was simply absent.
2. `~/.claude/skills/` held only `session-start-hook/` and the synced Anthropic document skills.
   `hebrew-prose` was not among them.

This is documented behaviour rather than a defect. Anthropic's cloud-environments page carries a
table headed "What carries over from your setup" whose rows for `~/.claude/CLAUDE.md` and for
`~/.claude/skills/` both read **No**, with the reason that they live on the machine and not in the
repository, and with the advice to commit the configuration to the repository — which is what
`dot-claude/` now is.

**The gap was silent, and that is the part worth fixing.** The 2026-09-09 session had been told to
read the `hebrew-prose` skill before editing, and nothing signalled that the skill was missing —
it was found only by going to look. So the hook's failure path is loud by design.

## Why the configuration is stored here and not in `github-misc`

It was tracked in `bdenckla/github-misc`, at `dot-claude/` and `dot-Codex/`, from 2026-07-25 until
2026-09-09. Two findings moved it.

### A session's git credential is scoped to its attached repositories, and that covers `git clone`

Measured 2026-09-09 in a cloud session on `bdenckla/MAM-basics`, container `cc 2.1.266`:

| repo | public? | attached to the session? | result |
| --- | --- | --- | --- |
| `bdenckla/MAM-basics` | yes | yes | exit 0, returns `refs/heads/main` |
| `bdenckla/github-misc` | no | **no** | exit 128, `Invalid username or token` |

`GH_TOKEN` and `GITHUB_TOKEN` are both set in the container and git has no `credential.helper`, so
a plain clone offers neither and dies with `could not read Username for 'https://github.com'`.
Supplying the token explicitly through an inline `x-access-token` helper does not help: the token
is a per-repository installation token, and `github-misc` is not in its set. **No credential
wiring inside a hook can reach an unattached repository** — a credential helper, a token in the
URL, and `gh auth` all reach the same refusal.

**This corrects what this file said between `6d19c34a` and `d8a0fdae`**, which was that the
proxy's repository scoping restricts the GitHub API rather than `git clone`. That was a
misreading, twice over, and both halves are worth naming so the next reader does not repeat them:

1. The cloud-environments page's **push-protection** bullet reads "`git push` works only against
   the session's current working branch; cloning, fetching, and PR operations work normally." Its
   subject is the *branch* restriction on push. "Work normally" means "are not subject to that
   branch restriction", not "cloning is unscoped." The adjacent **Git credentials** bullet says
   the client uses "a scoped credential" and never says scoped to what; that was the question to
   ask, and it went unasked.
2. The Claude Code on the web page's line that a session can access any repository the connecting
   account can see sits in the section contrasting the GitHub App with `/web-setup`. It is about
   which repositories a session may be **started on**, not what a running session's token reaches.

The framing to avoid is "cloud sessions cannot use private repositories". They can: a session
started **on** a private repository clones it. What fails is a *second* repository that is not
attached, and one cell is still unmeasured — whether an unattached **public** repository is
reachable, which `git ls-remote https://github.com/github/gitignore.git` from a cloud session
would settle. Nothing here depends on the answer any more.

### `github-misc` was chosen for precedent, not for privacy

Ben's hypothesis, 2026-09-09, and it holds. The commit that created the directory, `f1078d5` of
2026-07-25, gives its reasons outright: "Follows the existing dot-emacs / dot-gitconfig
convention, but as a directory, so `~/.claude`'s other authored config can join it later", and it
notes that `CLAUDE.md` "until now … was the one such file under no version control at all."
Precedent and the absence of version control. Privacy appears nowhere in that message, and
`github-misc` is private because of its other contents rather than because of these trees.

A scan of all twelve files on 2026-09-09 agreed: no email addresses, no tokens, no keys, no
passwords — the one `PAT` match is Ben weighing whether to use one. Of twenty phrases that could
plausibly have needed to stay private, nineteen were already public in this repository, most of
them heavily: `MAM-private` in 66 tracked files, `mgketer.org` in 56, `mgketer` in 89, and
"mgketer comparison" in 5, two of which are module names.

### The one sentence that was redacted on the way in

Filtering for a private project named *together with* its mechanics left one sentence that
mattered, in three files — `dot-claude/user-wide-CLAUDE.md`, `dot-Codex/user-wide-AGENTS.md`, and
the skill's `references/verifying.md`. It described a MAM-private project's self-test as diffing
against "the source HTML", which says what that project's input is.

**No new policy was invented for it.** `doc/agent-planning-principles.md` already carries the
public form of the same sentence, and the three copies were rewritten to match it: "a MAM-private
project", "the project's own input", and a `private annex §5` citation. `doc/sigil-decoding.md`
states the convention — public text cites `private annex §N`, and
`MAM-private/doc/mam-basics-annex.md` "is the annex for the whole repo". The live `~/.claude/`,
`~/.codex/` and `~/.agents/` copies carry the redacted wording too.

## Storage is not load scope, and the layout says so

`dot-claude/` and `dot-Codex/` are **storage**. This repository loads neither, exactly as
`github-misc` loaded neither. The live copies under `~/.claude/`, `~/.codex/` and `~/.agents/` are
what the two agents read, and `dot-claude/README.md` §"Shared-skill deployment to Claude and
Codex" is the deployment procedure of record. Edit the live copy, copy outwards, run both
comparisons.

Two naming decisions follow from that, and both are mechanical rather than cosmetic:

1. **The instruction files are tracked as `user-wide-CLAUDE.md` and `user-wide-AGENTS.md`.**
   Claude Code auto-loads a nested `CLAUDE.md` from a directory being worked in, so a file of that
   name inside `dot-claude/` would begin loading itself beside this repository's own `CLAUDE.md`
   the moment anyone edited a file beside it. The live copies keep the names their loaders
   require; only the tracked copies are renamed.
2. **`hebrew-prose` is kept out of `.claude/skills/`.** Putting it there would make it a project
   skill, auto-loaded with no hook at all — but the skills precedence is enterprise, then
   **personal**, then project, so `~/.claude/skills/hebrew-prose/`, which has to exist anyway for
   MAM-private and for Codex, would shadow it on every one of Ben's machines. The tracked copy
   would then be inert locally and exercised only in the cloud: the copy nobody sees being the
   one that runs. Keeping the skill user-wide also keeps it loaded in MAM-private, which with
   this repository is one of only two repositories in the roster where the accentuation work
   still happens.

## How the hook is gated

It runs everywhere, local sessions included, so it has two independent guards. Both are in the
script's comments at greater length.

1. **`CLAUDE_CODE_REMOTE = true`** is the documented discriminator: the cloud VM sets it and it is
   never true locally. This is what keeps the script from touching `~/.claude/` on Ben's own
   machines, where that directory is the live configuration and a copy over it would be
   destructive. On a local machine the script exits before reading anything.
2. **Write only what is absent.** Not redundant with the first guard: a self-hosted runner also
   reports `CLAUDE_CODE_REMOTE=true`, and Anthropic's documentation says such a runner can seed a
   session from the runner host's own `~/.claude/`. "Remote" therefore does not by itself mean
   "`~/.claude/` is empty". It also makes a resumed or compacted session a no-op.

**Every path exits 0.** A `SessionStart` hook that exits 2 blocks the session from starting and
resumes the previous one, which is far too severe a response to a missing prose reference. Failure
is reported by printing a banner instead: `SessionStart` is one of the few hook events whose
plain-text stdout Claude Code adds to the session as context, so the banner reaches Ben's
transcript **and** the model. Two failures get their own banner — the files being absent from the
checkout, and only one of the two landing — and each tells the session to say so to Ben before
starting work, rather than to proceed as though the rules had been read.

**The hook installs two of the tracked trees and not the rest.**
`dot-claude/skills/prune-claude-state/` reads `~/.claude/plans/` and the per-repo auto-memory
directory, neither of which reaches a cloud container, and it declares
`disable-model-invocation: true`. `dot-claude/README.md` and all of `dot-Codex/` are not loaded by
a Claude cloud session at all, and are readable in the checkout when wanted.

## Is a skill written after Claude Code launches picked up? Yes, measured

**Confirmed in a cloud container on 2026-09-09**, on this repository's `main` at `74d883d2`,
`CLAUDE_CODE_REMOTE=true` and `HOME=/root`. The hook fired on its own at session start and printed
its install banner, which the harness delivered as `SessionStart:startup hook success:`. On the
very next turn:

1. **`hebrew-prose` was in the available-skills list**, first of 25. The fallback path in the
   hook's success message — read `SKILL.md` directly — was not needed.
2. **`~/.claude/CLAUDE.md` was in context**, presented as the user's global instructions, before
   the verifying session had run a single command. So the instruction file is picked up late as
   well as the skill.
3. Both installed copies were byte-identical to the tracked originals: `diff -q` on the two
   `CLAUDE.md` files and `diff -r -q` on the two `hebrew-prose` trees each exited 0 with no output.
4. A second, manual run took the already-in-place branch, printed that banner, exited 0, changed
   the installed file's byte count not at all, and left `git status --porcelain` empty.

The documented mechanism is that Claude Code watches skill directories and picks up an addition
under `~/.claude/skills/` without a restart, the one caveat being that a *top-level skills
directory that did not exist when the session started* needs a restart before it is watched. The
container satisfies that caveat: `~/.claude/skills/` is already present, and in the verified
container held `session-start-hook/` — stamped two and a half hours earlier, so from the image
rather than from this hook — beside a `synced/` directory holding the account-level skills.

The hook still does not depend on the answer. Its success message names both absolute paths and
tells the session to read `SKILL.md` directly if `hebrew-prose` is absent from its list.

## One consequence worth knowing about session sharing

`bdenckla/MAM-basics` is public, and it now holds Ben's user-level configuration, which is
personal without being secret. Sessions are private by default. On a Pro or Max account the
sharing toggle offers **Public**, which makes a session visible to anyone logged in to claude.ai.
The scan above is why that is a note rather than a warning, but a session should still be looked
at before it is shared publicly.

## Re-establishing the facts in this file

The claims about cloud-session behaviour come from Anthropic's documentation as it stood on
2026-09-09, at `https://code.claude.com/docs/en/cloud-environments` (the carry-over table, the
GitHub proxy, network access levels, setup scripts versus `SessionStart` hooks, and
`CLAUDE_CODE_REMOTE`), `https://code.claude.com/docs/en/claude-code-on-the-web` (GitHub
authentication and session isolation) and `https://code.claude.com/docs/en/skills` (precedence and
live reload). The credential-scope table is a measurement rather than a reading, taken in the
session named there.

The hook was exercised on 2026-09-09 against fake `HOME` directories, covering six paths: local
no-op; empty `~/.claude/`; both files already present; one file already present; `dot-claude/`
absent from the checkout; and the hook invoked with no `CLAUDE_PROJECT_DIR`, which must still find
the repository from the script's own location. The harness was a throwaway under `.novc/` and is
not tracked; the six cases are listed here so they can be rebuilt.

**The whole path was then exercised in a real cloud container**, on `main` at `74d883d2`; the
section above records what that run measured. It also settles the one thing the harness cannot:
that the hook makes no network call. The script invokes `cp`, `echo`, `ls`, `mkdir`, and `cd` /
`dirname` / `pwd` in its repository-root fallback, and nothing else — no `git`, no `curl`, no
`gh`.

**The local guard was also exercised against the live `~/.claude/` rather than a fake one**, which
is better evidence than the harness for the one failure that would actually cost something. An
agent ran the hook twice on Ben's own machine, pointed at his real `~/.claude/`. Both runs printed
nothing and exited 0, and that `CLAUDE.md` kept its byte count and its modification time. Gate 1
returned before anything was read.
