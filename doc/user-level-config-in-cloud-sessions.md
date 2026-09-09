# Getting `~/.claude/` into a cloud session, and how it reaches private `github-misc`

A cloud session — Claude Code on the web, `claude --cloud`, a routine, a Claude Tag session —
starts from a fresh clone of `bdenckla/MAM-basics` on an Anthropic-managed Ubuntu VM. Everything
tracked in this repository travels with that clone. **Nothing under `~/.claude/` does**, and until
2026-09-09 nothing said so.

`.claude/hooks/install-user-config.sh`, wired in by `.claude/settings.json` as a `SessionStart`
hook, closes the gap by cloning `bdenckla/github-misc` inside the container and copying two things
out of its `dot-claude/` directory. This file records why, what the hook does and does not fetch,
how it reaches a **private** repository the session was not scoped to, and what to do when it
fails.

## The gap, and how it was measured

Verified in a remote session on 2026-09-09, before the hook existed:

1. `find / -name CLAUDE.md` returned nothing outside `/home/user/MAM-basics`. The user-level
   `~/.claude/CLAUDE.md` was simply absent.
2. `~/.claude/skills/` held only `session-start-hook` and the synced Anthropic document skills
   (`docx`, `pdf`, `pptx`, `xlsx` and the rest). `hebrew-prose` was not among them.

This is documented behaviour rather than a defect. Anthropic's cloud-environments page carries a
table headed "What carries over from your setup" whose rows for `~/.claude/CLAUDE.md` and for
`~/.claude/skills/` both read **No**, with the reason that they live on the machine and not in the
repository; its advice is to commit the configuration to the repository, which
[the design constraints](#what-is-fetched-and-what-is-deliberately-not) below rule out for the
skill.

**The gap was silent, and that is the part worth fixing.** The 2026-09-09 session had been told to
read the `hebrew-prose` skill before editing, and nothing signalled that the skill was missing —
it was found only by going to look. So the hook's failure paths are loud by design; see
[When the hook cannot fetch anything](#when-the-hook-cannot-fetch-anything).

## Why these two files and not others

`C:/Users/BenDe/GitRepos/MAM-basics/CLAUDE.md` depends on both by name:

1. Its section **"Invoke the `hebrew-prose` skill before writing or editing prose about
   accentuation"** calls that skill "the canonical, single home" for the accentuation-prose rules,
   and says a rule change goes into the skill first. Search that heading rather than a line number.
2. Its section on `doc/boj-*.md` says that where one of those procedures conflicts with
   `~/.claude/CLAUDE.md` — a `python -c` one-liner, a bare `python`, `PYTHONIOENCODING`, a
   `Start-Process` — "the global conventions win". Search **"the global conventions win"**.
3. Its testing section cites `~/.claude/CLAUDE.md`'s **"No `sys.path` surgery"** section as the
   cross-repo rule this repository is the worked example for.

A cloud session therefore reads a `CLAUDE.md` that defers three times to documents it cannot open.

## What is fetched, and what is deliberately not

`bdenckla/github-misc`'s `dot-claude/` directory holds four things. The hook fetches two:

| Source in `github-misc` | Installed to | Why |
| --- | --- | --- |
| `dot-claude/CLAUDE.md` | `~/.claude/CLAUDE.md` | The global cross-repo conventions, cited three times as above |
| `dot-claude/skills/hebrew-prose/` | `~/.claude/skills/hebrew-prose/` | The canonical accentuation-prose rules |

and leaves two alone:

| Source in `github-misc` | Why it is not fetched |
| --- | --- |
| `dot-claude/README.md` | Documentation about keeping the three copies of this configuration in step, whose procedure is PowerShell against a Windows disk. Nothing loads `~/.claude/README.md`, and a container that is discarded has no second copy to keep in step |
| `dot-claude/skills/prune-claude-state/` | It reads `~/.claude/plans/` and the per-repo auto-memory directory, neither of which reaches a cloud container, so it would have nothing to work on. It also declares `disable-model-invocation: true`, so it runs only when Ben names it |

**The `hebrew-prose` skill is fetched rather than vendored, and that is deliberate.** A tracked
copy under this repository's `.claude/skills/` would travel with the clone and need no hook at all
— and it would be exactly the second home that `CLAUDE.md`'s "canonical, single home" sentence
exists to prevent. `github-misc`'s `dot-claude/README.md` already records that this skill has three
homes and that the third one has silently fallen behind twice; a fourth would be worse. Fetching at
session start into `~/.claude/skills/`, which is untracked and discarded with the container, keeps
the count where it is.

**`~/.claude/CLAUDE.md` is fetched whole, Windows paths and all.** Much of it names
`C:/Users/BenDe/...` paths and PowerShell commands that mean nothing on an Ubuntu VM. That is
noise a session can read past; the alternative — an edited, portable subset — would be a second
home for the conventions with the same drift problem, and the rules that actually bind (no
`python -c`, no heredocs, black, the terminology sections, the prose sections, no `sys.path`
surgery) are platform-independent.

## How the hook reaches a private repository the session was not scoped to

**This is the question that decides whether the hook can work at all**, since `bdenckla/github-misc`
is private and a session started against `bdenckla/MAM-basics` is scoped to that repository.
The answer has three parts.

1. **Session access follows the connected GitHub account, not the repositories the Claude GitHub
   App is installed on.** Anthropic's Claude Code on the web page states this directly: a cloud
   session can reach any repository the connecting GitHub account can see, and installing the App
   on a repository enables PR webhooks for auto-fix rather than acting as a session-level access
   control. So no extra step is needed to make `github-misc` visible: it is Ben's own private
   repository under the same account.
2. **Git traffic is authenticated by a proxy outside the sandbox, over HTTPS.** In an
   Anthropic-hosted environment the real GitHub credentials never enter the VM; the git client
   inside uses a scoped credential that a dedicated GitHub proxy swaps for the real token, and
   that proxy is used whatever the environment's network access level is — even **None**. This is
   why the hook clones `https://github.com/bdenckla/github-misc.git` and **not** the
   `git@github.com:bdenckla/github-misc.git` remote Ben uses locally: SSH keys are among the
   things deliberately kept outside the sandbox.
3. **The proxy's repository scoping restricts the GitHub API, not `git clone`.** Its documented
   restriction is that GitHub API and release-asset requests reach only repositories attached to
   the session, so a setup script downloading a release asset from an unattached repository gets
   a 403. Cloning and fetching are called out separately as working normally; only `git push` is
   restricted, and then only to the session's own working branch. **So the hook clones and does
   not use `gh` or the REST API** — an API-based fetch of the same files would be the one shape
   that scoping blocks.

### If a clone is refused anyway

Point 3 is a reading of the documented restriction rather than a promise, so the hook is built to
announce a refusal rather than to assume one cannot happen. If a `403` or an authentication
failure ever appears in the hook's banner, there are three fallbacks, in order of preference:

1. **Attach `bdenckla/github-misc` to the session** from the web interface, which makes it a
   scoped repository and removes the question. This is per-session.
2. **Set the environment's network access to Custom** and include `github.com`. This only helps if
   the refusal turns out to come from the security proxy rather than the GitHub proxy; GitHub
   traffic is documented as bypassing the network allowlist, so try point 1 first.
3. **Move the fetch into the environment's setup script** at claude.ai/code, which runs as root
   before Claude Code launches. This is also the fix to reach for if the skill turns out not to be
   picked up when written after startup — see the open question below.

## Why the hook is gated twice

The hook runs everywhere, local sessions included, so it has two independent guards. Both are in
the script's comments as well, at greater length.

1. **`CLAUDE_CODE_REMOTE = true`** is the documented discriminator: the cloud VM sets it and it is
   never true locally. This is what keeps the script from touching `~/.claude/` on Ben's own
   machines, where that directory is the live configuration and a copy over it would be
   destructive. On a local machine the script exits before reading anything.
2. **Write only what is absent.** This is not redundant with the first guard. A self-hosted runner
   also reports `CLAUDE_CODE_REMOTE=true`, and Anthropic's documentation says such a runner can
   seed a session from the runner host's own `~/.claude/`. "Remote" therefore does not by itself
   mean "`~/.claude/` is empty". The second guard also makes a resumed or compacted session a
   no-op rather than a re-copy.

The hook clones into a `mktemp -d` directory outside the checkout and deletes it on exit, so no
copy of a private repository is left where a later `git add` could reach it.

## When the hook cannot fetch anything

**Every path through the hook exits 0.** A `SessionStart` hook that exits 2 blocks the session from
starting and resumes the previous one, which is far too severe a response to a missing prose
reference. Failure is reported instead by printing a banner: `SessionStart` is one of the few hook
events whose plain-text stdout Claude Code adds to the session as context, so the banner reaches
Ben's transcript **and** the model.

Three distinct failures each get their own banner, and each tells the session to say so to Ben
before starting work, rather than to proceed as though the rules had been read:

1. **The clone failed** — the banner names both missing documents and quotes `git clone`'s own
   stderr.
2. **The clone succeeded but `dot-claude/` did not hold what was expected** — the banner lists what
   `dot-claude/` actually contains. This fires if `github-misc` is ever reorganized, and means both
   the hook and this file need updating.
3. **Only one of the two landed** — the banner says which.

## Open question: is a skill written after startup picked up?

**This is unresolved and needs a remote session to settle.** A `SessionStart` hook runs *after*
Claude Code launches, so `~/.claude/skills/hebrew-prose/` and `~/.claude/CLAUDE.md` appear on disk
after whatever scan Claude Code does of those locations. Whether the skill then shows up in the
available-skills list, and whether the user-level `CLAUDE.md` is loaded into context, is not
documented either way.

The hook does not depend on the answer: its success message names both absolute paths and tells the
session to read `SKILL.md` directly if `hebrew-prose` is not in its available-skills list. That
delivers the rules regardless. But if the answer turns out to be no, the tidier fix is fallback 3
above — the same fetch in the environment's setup script, which runs before Claude Code launches.

## One consequence worth knowing about session sharing

`bdenckla/MAM-basics` is public and `bdenckla/github-misc` is private, and this hook puts content
from the private repository into every cloud session on the public one. Sessions are private by
default. On a Pro or Max account the sharing toggle offers **Public**, which makes a session
visible to anyone logged in to claude.ai, and Anthropic's own note on that toggle warns that
sessions may contain content from private repositories. So a MAM-basics cloud session should not be
shared publicly without a look at what is in it.

## Re-establishing the facts in this file

Every claim above about cloud-session behaviour comes from Anthropic's documentation as it stood on
2026-09-09, at `https://code.claude.com/docs/en/cloud-environments` (the carry-over table, the
GitHub proxy, network access levels, setup scripts versus `SessionStart` hooks, and
`CLAUDE_CODE_REMOTE`) and `https://code.claude.com/docs/en/claude-code-on-the-web` (GitHub
authentication and session isolation). Re-read those two pages rather than trusting this summary if
something here stops matching what a session observes.

The hook's own behaviour was exercised on 2026-09-09 against fake `HOME` directories and a stubbed
failing `git`, covering all six paths: local no-op, unreachable `github-misc`, empty `~/.claude/`,
both files already present, one file already present, and a reorganized `github-misc`. That harness
was a throwaway under `.novc/` and is not tracked; the six cases are listed here so they can be
rebuilt.
