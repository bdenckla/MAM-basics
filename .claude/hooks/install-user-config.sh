#!/usr/bin/env bash
#
# SessionStart hook: put Ben's user-level Claude configuration into ~/.claude/ when
# the session is running in an ephemeral cloud container, which does not get it any
# other way.
#
# WHAT IS MISSING WITHOUT THIS, AND WHY IT MATTERS
#
# A cloud session starts from a fresh clone of MAM-basics, so everything tracked in
# the repository travels: CLAUDE.md, .claude/settings.json, .claude/skills/. Nothing
# under ~/.claude/ travels -- Anthropic's cloud-environments documentation says so
# outright, in its "What carries over from your setup" table, for both
# ~/.claude/CLAUDE.md and ~/.claude/skills/. Verified in a remote session on
# 2026-09-09: `find / -name CLAUDE.md` found nothing outside the checkout, and
# ~/.claude/skills/ held no hebrew-prose.
#
# MAM-basics' own CLAUDE.md depends on both by name. Its section "Invoke the
# hebrew-prose skill before writing or editing prose about accentuation" calls that
# skill "the canonical, single home" for the accentuation-prose rules, and two later
# sections defer to ~/.claude/CLAUDE.md by name -- the doc/boj-*.md section ("the
# global conventions win") and the testing section (its "No sys.path surgery" rule).
# So a cloud session reads a CLAUDE.md that cites two documents it cannot open, and
# nothing says so.
#
# WHY THIS COPIES AND DOES NOT CLONE
#
# It cloned bdenckla/github-misc until 2026-09-09, and that could never have worked.
# A cloud session's git credential is scoped to the repositories attached to the
# session; github-misc is private and unattached, so the clone returned "Invalid
# username or token" no matter how the token was supplied. Measured that day. The
# files therefore moved into MAM-basics, at dot-claude/ and dot-Codex/, where they
# arrive with the clone -- so this hook now copies from the checkout and touches the
# network not at all. doc/user-level-config-in-cloud-sessions.md records the
# measurement and the reasoning; dot-claude/README.md records the deployment
# procedure for Ben's own machines, which is unchanged.
#
# WHAT IS INSTALLED, AND WHAT IS DELIBERATELY NOT
#
#   dot-claude/user-wide-CLAUDE.md  -> ~/.claude/CLAUDE.md
#   dot-claude/skills/hebrew-prose/ -> ~/.claude/skills/hebrew-prose/
#
# Those are the two MAM-basics' CLAUDE.md names. Three further trees are tracked
# beside them and none is installed here:
#
#   dot-claude/skills/prune-claude-state/
#                          operates on ~/.claude/plans/ and on the per-repo
#                          auto-memory directory, neither of which reaches a cloud
#                          container, so it would have nothing to read. It is also
#                          declared disable-model-invocation: true, so it runs only
#                          when Ben asks for it by name.
#   dot-claude/README.md, dot-Codex/
#                          the deployment procedure and the Codex-side
#                          configuration. Nothing in a Claude cloud session loads
#                          either, and both are readable in the checkout if wanted.
#
# WHICH GATE, AND WHY BOTH OF THEM
#
# Gate 1, CLAUDE_CODE_REMOTE=true, is the documented discriminator: the cloud VM
# sets it and it is never true locally. It is what keeps this script from touching
# ~/.claude/ on Ben's own machines, where that directory is the live configuration
# and overwriting it would be destructive. On a local machine the script exits
# before reading anything.
#
# Gate 2, write only what is absent, is not redundant with gate 1. A self-hosted
# runner also reports CLAUDE_CODE_REMOTE=true, and Anthropic's documentation says
# such a runner can seed a session from the runner host's own ~/.claude/. So
# "remote" does not by itself imply "~/.claude/ is empty", and gate 2 is what makes
# the script safe in that case. It also makes a resumed session a no-op.
#
# WHY IT NEVER EXITS NON-ZERO
#
# A SessionStart hook that exits 2 blocks the session from starting. Missing prose
# rules must not stop the session; they must be announced. So every path here exits
# 0, and a failure is reported by printing a banner. SessionStart is one of the few
# events whose plain-text stdout Claude Code adds to the session as context, so the
# banner reaches both Ben's transcript and the model.

set -u

DOC_NOTE="doc/user-level-config-in-cloud-sessions.md"
DEST="$HOME/.claude"

# $CLAUDE_PROJECT_DIR is set for a hook, but derive a fallback from this script's own
# location so the hook still works when run by hand from another directory.
REPO="${CLAUDE_PROJECT_DIR:-}"
if [ -z "$REPO" ]; then
    REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
fi
SRC="$REPO/dot-claude"

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
    # Nothing to install, but still say where the two documents are: this branch is
    # what a resumed or compacted session hits, and after a compaction the notice
    # printed at startup may no longer be in context.
    echo "MAM-basics SessionStart hook: Ben's user-level Claude configuration is already in place."
    echo "  $HOME/.claude/CLAUDE.md            -- global cross-repo conventions."
    echo "  $HOME/.claude/skills/hebrew-prose/ -- the canonical accentuation-prose rules;"
    echo "    if it is not in your available-skills list, read its SKILL.md directly."
    exit 0
fi

if [ ! -f "$SRC/user-wide-CLAUDE.md" ] || [ ! -f "$SRC/skills/hebrew-prose/SKILL.md" ]; then
    echo "================================================================================"
    echo "  MAM-basics SessionStart hook: USER-LEVEL CLAUDE CONFIGURATION IS MISSING"
    echo "================================================================================"
    echo "Expected these in the checkout, and at least one is not there:"
    echo "    dot-claude/user-wide-CLAUDE.md"
    echo "    dot-claude/skills/hebrew-prose/SKILL.md"
    echo "Looked under: $SRC"
    echo "Found:"
    ls -1 "$SRC" 2>&1 | sed 's/^/    /'
    echo
    echo "WHAT THIS MEANS FOR THIS SESSION"
    echo "  - The hebrew-prose skill is NOT available. Do not write or edit prose about"
    echo "    Hebrew accentuation as though you had read it, and do not report having"
    echo "    followed it."
    echo "  - MAM-basics' CLAUDE.md cites both of those documents by name, so parts of it"
    echo "    now point at files this session cannot open."
    echo "  - Say so in your first reply to Ben, before doing the task."
    echo "  - Nothing here needs the network: these files are tracked in this repository,"
    echo "    so their absence means the checkout is wrong or they have been moved."
    echo "    See $DOC_NOTE."
    echo "================================================================================"
    exit 0
fi

if [ "$want_conventions" = yes ]; then
    mkdir -p "$DEST"
    cp "$SRC/user-wide-CLAUDE.md" "$DEST/CLAUDE.md"
fi
if [ "$want_skill" = yes ]; then
    mkdir -p "$DEST/skills"
    cp -R "$SRC/skills/hebrew-prose" "$DEST/skills/hebrew-prose"
fi

# Report against the filesystem rather than against what the copies returned, so a
# half-completed install is announced as one.
ok_conventions=no
ok_skill=no
[ -f "$DEST/CLAUDE.md" ] && ok_conventions=yes
[ -f "$DEST/skills/hebrew-prose/SKILL.md" ] && ok_skill=yes

if [ "$ok_conventions" = yes ] && [ "$ok_skill" = yes ]; then
    echo "MAM-basics SessionStart hook: installed Ben's user-level Claude configuration from this checkout."
    echo "  ~/.claude/CLAUDE.md            -- global cross-repo conventions, cited by name in MAM-basics' CLAUDE.md."
    echo "  ~/.claude/skills/hebrew-prose/ -- the canonical accentuation-prose rules."
    echo "Claude Code watches ~/.claude/skills/ and picks up a skill added to it without a"
    echo "restart, and that directory already exists in a cloud container, so hebrew-prose"
    echo "should appear in the available-skills list. If it does not, read"
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
