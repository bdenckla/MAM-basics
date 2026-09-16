#!/usr/bin/env bash
#
# SessionStart hook: put Ben's user-level Claude configuration and its Codex import
# target into an ephemeral cloud container, which does not get them any other way.
#
# WHAT IS MISSING WITHOUT THIS, AND WHY IT MATTERS
#
# A cloud session starts from a fresh clone of MAM-basics, so everything tracked in
# the repository travels: CLAUDE.md, .claude/settings.json, .claude/skills/. Nothing
# under ~/.claude/ travels -- Anthropic's cloud-environments documentation says so
# outright, in its "What carries over from your setup" table, for both
# ~/.claude/CLAUDE.md and ~/.claude/skills/. Verified in a remote session on
# 2026-09-09: `find / -name CLAUDE.md` found nothing outside the checkout, and
# ~/.claude/skills/ held no hebrew-prose. The common user-level arrangement adopted
# for implementation in MAM-basics issue 274 also needs ~/.codex/AGENTS.md: the
# minimal Claude wrapper will import that file, and the tracked copy alone does not
# create the import target.
#
# The target symmetric setup depends on all three resources by name. Its repository
# instructions require the hebrew-prose skill, while its minimal user-level Claude
# wrapper will import ~/.codex/AGENTS.md. Without this hook, a cloud session can read
# wrappers or repository instructions that point at files the session cannot open,
# and nothing says so.
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
# measurement and the reasoning; dot-claude/README.md records the origin/main-sourced
# deployment procedure for Ben's own machines. Ben's decision, 2026-09-13: this hook
# is the exception. It uses the user-level files from the cloud session's checked-out
# branch, which is main only when main is that branch; it never substitutes main for a
# different checked-out branch.
#
# WHAT IS INSTALLED, AND WHAT IS DELIBERATELY NOT
#
#   dot-Codex/user-wide-AGENTS.md    -> ~/.codex/AGENTS.md
#   dot-claude/user-wide-CLAUDE.md  -> ~/.claude/CLAUDE.md
#   dot-claude/skills/hebrew-prose/ -> ~/.claude/skills/hebrew-prose/
#
# Those are the three resources the target symmetric Claude setup needs. Four further
# entries are tracked beside them and none is installed here:
#
#   1. dot-claude/skills/prune-claude-state/
#                          operates on ~/.claude/plans/ and on the per-repo
#                          auto-memory directory, neither of which reaches a cloud
#                          container, so it would have nothing to read. It is also
#                          declared disable-model-invocation: true, so it runs only
#                          when Ben asks for it by name.
#   2. dot-claude/skills/verse-links/
#                          names its interpreter and py/main_verse_links.py by the
#                          absolute Windows paths of Ben's own machines, which a
#                          cloud container does not have. The command itself needs
#                          only the checkout, and its --help says how to run it.
#   3. dot-claude/skills/github-issues/
#                          names the same interpreter and
#                          py/main_github_issue_edit.py by those absolute Windows
#                          paths, and whether a cloud session's repository-scoped
#                          token may write to a GitHub issue has not been
#                          measured. Ben's decision, 2026-09-14: not installed here.
#   4. dot-claude/README.md and the rest of dot-Codex/
#                          are the deployment procedure and Codex-only resources.
#                          Nothing in a Claude cloud session loads them, and they
#                          are readable in the checkout if wanted.
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

DOC_NOTE="doc/user-level-config-in-cloud-sessions-update.md"
CLAUDE_DEST="$HOME/.claude"
CODEX_DEST="$HOME/.codex"

# $CLAUDE_PROJECT_DIR is set for a hook, but derive a fallback from this script's own
# location so the hook still works when run by hand from another directory.
REPO="${CLAUDE_PROJECT_DIR:-}"
if [ -z "$REPO" ]; then
    REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
fi
CLAUDE_SRC="$REPO/dot-claude"
CODEX_SRC="$REPO/dot-Codex"

# Gate 1: do nothing at all outside an ephemeral cloud container.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
    exit 0
fi

# Gate 2: decide what is actually absent. Anything already present is left alone.
want_common=no
want_wrapper=no
want_skill=no
[ -f "$CODEX_DEST/AGENTS.md" ] || want_common=yes
[ -f "$CLAUDE_DEST/CLAUDE.md" ] || want_wrapper=yes
# A directory alone is not the skill: an interrupted cp -R leaves one behind, and
# the report below already reads presence off SKILL.md rather than off the directory.
[ -f "$CLAUDE_DEST/skills/hebrew-prose/SKILL.md" ] || want_skill=yes

if [ "$want_common" = no ] && [ "$want_wrapper" = no ] && [ "$want_skill" = no ]; then
    # Nothing to install, but still say where the three resources are: this branch is
    # what a resumed or compacted session hits, and after a compaction the notice
    # printed at startup may no longer be in context.
    echo "MAM-basics SessionStart hook: Ben's user-level Claude configuration is already in place."
    echo "  $HOME/.codex/AGENTS.md"
    echo "      -- the user-level instruction file at Codex's native path."
    echo "  $HOME/.claude/CLAUDE.md"
    echo "      -- the user-level instruction file at Claude Code's native path."
    echo "  $HOME/.claude/skills/hebrew-prose/"
    echo "      -- the canonical accentuation-prose rules; if hebrew-prose is not in your"
    echo "         available-skills list, read its SKILL.md directly."
    exit 0
fi

have_common_source=no
have_wrapper_source=no
have_skill_source=no
[ -f "$CODEX_SRC/user-wide-AGENTS.md" ] && have_common_source=yes
[ -f "$CLAUDE_SRC/user-wide-CLAUDE.md" ] && have_wrapper_source=yes
[ -f "$CLAUDE_SRC/skills/hebrew-prose/SKILL.md" ] && have_skill_source=yes

missing_source=no
if [ "$want_common" = yes ] && [ "$have_common_source" = no ]; then
    missing_source=yes
fi
if [ "$want_wrapper" = yes ] && [ "$have_wrapper_source" = no ]; then
    missing_source=yes
fi
if [ "$want_skill" = yes ] && [ "$have_skill_source" = no ]; then
    missing_source=yes
fi

if [ "$missing_source" = yes ]; then
    echo "================================================================================"
    echo "  MAM-basics SessionStart hook: USER-LEVEL CLAUDE CONFIGURATION IS MISSING"
    echo "================================================================================"
    echo "SOURCE STATUS (a source is needed only when its destination is missing)"
    echo "  dot-Codex/user-wide-AGENTS.md present:             $have_common_source"
    echo "  dot-claude/user-wide-CLAUDE.md present:            $have_wrapper_source"
    echo "  dot-claude/skills/hebrew-prose/SKILL.md present:   $have_skill_source"
    echo "Looked under:"
    echo "    $CODEX_SRC"
    echo "    $CLAUDE_SRC"
    echo "Found under dot-Codex/:"
    ls -1 "$CODEX_SRC" 2>&1 | sed 's/^/    /'
    echo "Found under dot-claude/:"
    ls -1 "$CLAUDE_SRC" 2>&1 | sed 's/^/    /'
    echo
    echo "DESTINATION STATUS"
    if [ "$want_common" = yes ]; then
        echo "  $HOME/.codex/AGENTS.md present: no"
    else
        echo "  $HOME/.codex/AGENTS.md present: yes"
    fi
    if [ "$want_wrapper" = yes ]; then
        echo "  $HOME/.claude/CLAUDE.md present: no"
    else
        echo "  $HOME/.claude/CLAUDE.md present: yes"
    fi
    if [ "$want_skill" = yes ]; then
        echo "  $HOME/.claude/skills/hebrew-prose/SKILL.md present: no"
    else
        echo "  $HOME/.claude/skills/hebrew-prose/SKILL.md present: yes"
    fi
    echo
    echo "WHAT THIS MEANS FOR THIS SESSION"
    if [ "$want_common" = yes ]; then
        echo "  - The user-level instructions at $HOME/.codex/AGENTS.md are unavailable."
    fi
    if [ "$want_wrapper" = yes ]; then
        echo "  - The user-level Claude file at $HOME/.claude/CLAUDE.md is unavailable."
    fi
    if [ "$want_skill" = yes ]; then
        echo "  - The hebrew-prose skill is NOT available. Do not write or edit prose about"
        echo "    Hebrew accentuation as though you had read it, and do not report having"
        echo "    followed it."
    fi
    echo "  - Say so in your first reply to Ben, before doing the task."
    echo "  - Nothing here needs the network: all three sources are tracked in this repository,"
    echo "    so their absence means the checkout is wrong or they have been moved."
    echo "    See $DOC_NOTE."
    echo "================================================================================"
    exit 0
fi

if [ "$want_common" = yes ]; then
    mkdir -p "$CODEX_DEST"
    cp "$CODEX_SRC/user-wide-AGENTS.md" "$CODEX_DEST/AGENTS.md"
fi
if [ "$want_wrapper" = yes ]; then
    mkdir -p "$CLAUDE_DEST"
    cp "$CLAUDE_SRC/user-wide-CLAUDE.md" "$CLAUDE_DEST/CLAUDE.md"
fi
if [ "$want_skill" = yes ]; then
    # The trailing /. copies the contents, so a directory left by an interrupted
    # run is filled rather than nested inside itself.
    mkdir -p "$CLAUDE_DEST/skills/hebrew-prose"
    cp -R "$CLAUDE_SRC/skills/hebrew-prose/." "$CLAUDE_DEST/skills/hebrew-prose/"
fi

# Report against the filesystem rather than against what the copies returned, so a
# half-completed install is announced as one.
ok_common=no
ok_wrapper=no
ok_skill=no
[ -f "$CODEX_DEST/AGENTS.md" ] && ok_common=yes
[ -f "$CLAUDE_DEST/CLAUDE.md" ] && ok_wrapper=yes
[ -f "$CLAUDE_DEST/skills/hebrew-prose/SKILL.md" ] && ok_skill=yes

if [ "$ok_common" = yes ] && [ "$ok_wrapper" = yes ] && [ "$ok_skill" = yes ]; then
    # Both banners spell these paths the same way, expanded. They did not until
    # 2026-09-09, when the cloud verification reported that this branch wrote a
    # literal ~ while the already-in-place branch above wrote the expanded form; an
    # agent that has to open the file is better served by the expanded one.
    echo "MAM-basics SessionStart hook: installed Ben's user-level Claude configuration from this checkout."
    echo "  $HOME/.codex/AGENTS.md"
    echo "      -- the user-level instruction file at Codex's native path."
    echo "  $HOME/.claude/CLAUDE.md"
    echo "      -- the user-level instruction file at Claude Code's native path."
    echo "  $HOME/.claude/skills/hebrew-prose/"
    echo "      -- the canonical accentuation-prose rules."
    echo "Claude Code watches ~/.claude/skills/ and picks a skill added to it up without a"
    echo "restart. Measured 2026-09-09 in a cloud container: hebrew-prose was in the"
    echo "available-skills list, and these instructions were in context, on the turn after"
    echo "this hook ran. If hebrew-prose is nonetheless absent from your list, read"
    echo "$HOME/.claude/skills/hebrew-prose/SKILL.md directly before writing or editing any"
    echo "prose about accentuation, and read both $HOME/.claude/CLAUDE.md and"
    echo "$HOME/.codex/AGENTS.md before your first edit."
else
    echo "================================================================================"
    echo "  MAM-basics SessionStart hook: INSTALL ONLY PARTLY SUCCEEDED"
    echo "================================================================================"
    echo "  ~/.codex/AGENTS.md present:                      $ok_common"
    echo "  ~/.claude/CLAUDE.md present:                     $ok_wrapper"
    echo "  ~/.claude/skills/hebrew-prose/SKILL.md present:  $ok_skill"
    echo "Tell Ben which resource is missing; do not treat its rules as available."
    echo "See $DOC_NOTE."
    echo "================================================================================"
fi

exit 0
