#!/usr/bin/env bash
#
# SessionStart hook: put Ben's user-level Claude configuration into ~/.claude/
# when the session is running in an ephemeral cloud container, which does not
# get it any other way.
#
# WHAT IS MISSING WITHOUT THIS, AND WHY IT MATTERS
#
# A cloud session starts from a fresh clone of MAM-basics, so everything tracked
# in the repo travels: CLAUDE.md, .claude/settings.json, .claude/skills/. Nothing
# under ~/.claude/ travels -- Anthropic's cloud-environments documentation says so
# outright, in its "What carries over from your setup" table, for both
# ~/.claude/CLAUDE.md and ~/.claude/skills/. Verified in a remote session on
# 2026-09-09: `find / -name CLAUDE.md` found nothing outside the checkout, and
# ~/.claude/skills/ held no hebrew-prose.
#
# MAM-basics' own CLAUDE.md depends on both by name. Its section "Invoke the
# hebrew-prose skill before writing or editing prose about accentuation" calls
# that skill "the canonical, single home" for the accentuation-prose rules, and
# two later sections defer to ~/.claude/CLAUDE.md by name -- the doc/boj-*.md
# section ("the global conventions win") and the testing section (its "No
# sys.path surgery" rule). So a cloud session reads a CLAUDE.md that cites two
# documents it cannot open, and nothing says so.
#
# WHAT IS INSTALLED, AND WHAT IS DELIBERATELY NOT
#
#   CLAUDE.md               -> ~/.claude/CLAUDE.md
#   skills/hebrew-prose/    -> ~/.claude/skills/hebrew-prose/
#
# Those are the two MAM-basics' CLAUDE.md names. github-misc's dot-claude/ holds
# two more things and neither is fetched:
#
#   README.md              is documentation about keeping the three copies of
#                          this configuration in step, and its procedure is
#                          PowerShell run against a Windows disk. Nothing loads
#                          ~/.claude/README.md, and there is no second copy to
#                          keep in step inside a container that is discarded.
#   skills/prune-claude-state/
#                          operates on ~/.claude/plans/ and on the per-repo
#                          auto-memory directory, neither of which reaches a
#                          cloud container, so it would have nothing to read. It
#                          is also declared disable-model-invocation: true, so it
#                          runs only when Ben asks for it by name.
#
# WHICH GATE, AND WHY BOTH OF THEM
#
# Gate 1, CLAUDE_CODE_REMOTE=true, is the documented discriminator: the cloud VM
# sets it and it is never true locally. It is what keeps this script from
# touching ~/.claude/ on Ben's own machines at all, where that directory is the
# live configuration and overwriting it would be destructive.
#
# Gate 2, write only what is absent, is not redundant with gate 1. A self-hosted
# runner also reports CLAUDE_CODE_REMOTE=true, and Anthropic's documentation
# says such a runner can seed a session from the runner host's own ~/.claude/.
# So "remote" does not by itself imply "~/.claude/ is empty", and gate 2 is what
# makes the script safe in that case. It also makes a resumed session a no-op
# rather than a re-copy.
#
# WHY IT NEVER EXITS NON-ZERO
#
# A SessionStart hook that exits 2 blocks the session from starting. Missing
# prose rules must not stop the session; they must be announced. So every path
# here exits 0, and a failure is reported by printing a banner. SessionStart is
# one of the few events whose plain-text stdout Claude Code adds to the session
# as context, so the banner reaches both Ben's transcript and the model.
#
# WHY HTTPS RATHER THAN THE SSH REMOTE BEN USES LOCALLY
#
# In an Anthropic-hosted environment, git credentials and signing keys stay
# outside the sandbox and all GitHub traffic goes through a proxy that swaps a
# scoped credential for the real token. That proxy handles HTTPS; an SSH key is
# one of the things deliberately left outside. github-misc is private, and a
# cloud session can reach any repository the connected GitHub account can see --
# see doc/user-level-config-in-cloud-sessions.md for that answer in full.

set -u

REPO_URL="https://github.com/bdenckla/github-misc.git"
DOC_NOTE="doc/user-level-config-in-cloud-sessions.md"
DEST="$HOME/.claude"

# Gate 1: do nothing at all outside an ephemeral cloud container.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
    exit 0
fi

# Gate 2: decide what is actually absent. Anything already present is left alone.
want_conventions=no
want_skill=no
[ -f "$DEST/CLAUDE.md" ] || want_conventions=yes
[ -d "$DEST/skills/hebrew-prose" ] || want_skill=yes

if [ "$want_conventions" = no ] && [ "$want_skill" = no ]; then
    # Nothing to fetch, but still say where the two documents are: this branch is
    # what a resumed or compacted session hits, and after a compaction the notice
    # printed at startup may no longer be in context.
    echo "MAM-basics SessionStart hook: Ben's user-level Claude configuration is already in place."
    echo "  $HOME/.claude/CLAUDE.md            -- global cross-repo conventions."
    echo "  $HOME/.claude/skills/hebrew-prose/ -- the canonical accentuation-prose rules;"
    echo "    if it is not in your available-skills list, read its SKILL.md directly."
    exit 0
fi

work="$(mktemp -d 2>/dev/null || mktemp -d -t mam-user-config)" || {
    echo "MAM-basics SessionStart hook: could not create a temporary directory; user-level Claude configuration was NOT installed."
    exit 0
}
trap 'rm -rf "$work"' EXIT

clone_log="$work/clone.log"
if ! git clone --depth 1 --single-branch "$REPO_URL" "$work/github-misc" >"$clone_log" 2>&1; then
    echo "================================================================================"
    echo "  MAM-basics SessionStart hook: USER-LEVEL CLAUDE CONFIGURATION IS MISSING"
    echo "================================================================================"
    echo "Could not clone bdenckla/github-misc, so this session is running WITHOUT:"
    [ "$want_conventions" = yes ] && echo "  * ~/.claude/CLAUDE.md            -- Ben's global cross-repo conventions"
    [ "$want_skill" = yes ]       && echo "  * ~/.claude/skills/hebrew-prose/ -- the accentuation-prose rules"
    echo
    echo "git clone said:"
    sed 's/^/    /' "$clone_log"
    echo
    echo "WHAT THIS MEANS FOR THIS SESSION"
    echo "  - The hebrew-prose skill is NOT available. Do not write or edit prose about"
    echo "    Hebrew accentuation as though you had read it, and do not report having"
    echo "    followed it."
    echo "  - MAM-basics' CLAUDE.md cites both of those documents by name, so parts of it"
    echo "    now point at files this session cannot open."
    echo "  - Say so in your first reply to Ben, before doing the task."
    echo "  - The access question and its fallbacks are written up in $DOC_NOTE."
    echo "================================================================================"
    exit 0
fi

src="$work/github-misc/dot-claude"
if [ ! -f "$src/CLAUDE.md" ] || [ ! -f "$src/skills/hebrew-prose/SKILL.md" ]; then
    echo "================================================================================"
    echo "  MAM-basics SessionStart hook: github-misc CLONED BUT DID NOT HOLD WHAT IS"
    echo "  EXPECTED AT dot-claude/"
    echo "================================================================================"
    echo "Expected dot-claude/CLAUDE.md and dot-claude/skills/hebrew-prose/SKILL.md."
    echo "Found under dot-claude/:"
    ls -1 "$src" 2>&1 | sed 's/^/    /'
    echo
    echo "Nothing was installed. The hebrew-prose skill is NOT available; say so to Ben."
    echo "If github-misc has been reorganized, this hook and $DOC_NOTE need updating."
    echo "================================================================================"
    exit 0
fi

installed=""
if [ "$want_conventions" = yes ]; then
    mkdir -p "$DEST"
    cp "$src/CLAUDE.md" "$DEST/CLAUDE.md" && installed="$installed conventions"
fi
if [ "$want_skill" = yes ]; then
    mkdir -p "$DEST/skills"
    cp -R "$src/skills/hebrew-prose" "$DEST/skills/hebrew-prose" && installed="$installed skill"
fi

# Report against the filesystem rather than against what the copies returned, so
# a half-completed install is announced as one.
ok_conventions=no
ok_skill=no
[ -f "$DEST/CLAUDE.md" ] && ok_conventions=yes
[ -f "$DEST/skills/hebrew-prose/SKILL.md" ] && ok_skill=yes

if [ "$ok_conventions" = yes ] && [ "$ok_skill" = yes ]; then
    echo "MAM-basics SessionStart hook: installed Ben's user-level Claude configuration from bdenckla/github-misc."
    echo "  ~/.claude/CLAUDE.md            -- global cross-repo conventions, cited by name in MAM-basics' CLAUDE.md."
    echo "  ~/.claude/skills/hebrew-prose/ -- the canonical accentuation-prose rules."
    echo "These were written after Claude Code started, so they may not have been picked up"
    echo "by its own loaders. If hebrew-prose is not in your available-skills list, read"
    echo "$HOME/.claude/skills/hebrew-prose/SKILL.md directly before writing or editing any"
    echo "prose about accentuation, and read $HOME/.claude/CLAUDE.md before your first edit."
else
    echo "================================================================================"
    echo "  MAM-basics SessionStart hook: INSTALL ONLY PARTLY SUCCEEDED"
    echo "================================================================================"
    echo "  ~/.claude/CLAUDE.md present:                    $ok_conventions"
    echo "  ~/.claude/skills/hebrew-prose/SKILL.md present: $ok_skill"
    echo "Tell Ben which one is missing; do not treat its rules as available."
    echo "See $DOC_NOTE."
    echo "================================================================================"
fi

exit 0
