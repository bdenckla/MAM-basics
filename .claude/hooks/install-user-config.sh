#!/usr/bin/env bash
# Install tracked common instructions, the Claude wrapper and every declared shared
# skill in a Claude cloud home. Ben approved the six-skill inventory on 2026-09-29,
# superseding the 2026-09-14 github-issues exclusion for instruction installation.
# Sources come from the checked-out branch; copying needs no network or Python.
# Skills provide rules, not credentials, dependencies or workflow authorization.
# Existing files are preserved, including in a seeded runner or resumed session.
# A missing resource is reported to session context; every path exits zero.

set -u

# Local sessions return before reading configuration or deriving home destinations.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
    exit 0
fi

DOC_NOTE="doc/user-level-config-in-cloud-sessions-update.md"
if [ -z "${HOME:-}" ] || [ ! -d "$HOME" ] || [ -L "$HOME" ]; then
    echo "MAM-basics SessionStart hook: USER-LEVEL CONFIGURATION IS INCOMPLETE (HOME must name an existing directory, not a link)."
    echo "Tell Ben before the task; no configuration was installed. See $DOC_NOTE."
    exit 0
fi
REPO="${CLAUDE_PROJECT_DIR:-}"
if [ -z "$REPO" ]; then
    if ! REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"; then
        echo "MAM-basics SessionStart hook: cannot locate this checkout. See $DOC_NOTE."
        exit 0
    fi
fi
CLAUDE_SRC="$REPO/dot-claude"
CODEX_SRC="$REPO/dot-Codex"
CLAUDE_DEST="$HOME/.claude"
CODEX_DEST="$HOME/.codex"
problem_count=0
installed_count=0

problem() {
    problem_count=$((problem_count + 1))
    printf '  UNAVAILABLE: %s\n' "$1"
}

destination_parents_ok() {
    local parent
    parent="$(dirname "$1")"
    while [ "$parent" != "$HOME" ] && [ "$parent" != / ] && [ "$parent" != . ]; do
        if [ -L "$parent" ] || { [ -e "$parent" ] && [ ! -d "$parent" ]; }; then
            problem "$parent is an existing non-directory or link; left untouched."
            return 1
        fi
        parent="$(dirname "$parent")"
    done
    return 0
}

publish_missing_file() {
    local source="$1" destination="$2" temporary
    # Stage on the destination filesystem. A failed copy leaves no final file that
    # a resumed session could mistake for a completed install. ln never clobbers.
    if ! temporary="$(mktemp "$(dirname "$destination")/.mam-user-config.XXXXXX")"; then
        return 1
    fi
    if ! cp -- "$source" "$temporary" || ! cmp -s -- "$source" "$temporary"; then
        rm -f -- "$temporary"
        return 1
    fi
    if ! ln -T -- "$temporary" "$destination"; then
        rm -f -- "$temporary"
        return 1
    fi
    rm -f -- "$temporary"
    return 0
}

install_file() {
    local source="$1" destination="$2"
    destination_parents_ok "$destination" || return
    if [ -e "$destination" ] || [ -L "$destination" ]; then
        if [ -f "$destination" ] && [ ! -L "$destination" ]; then
            printf '  PRESERVED: %s\n' "$destination"
        else
            problem "$destination is an existing non-regular file; left untouched."
        fi
        return
    fi
    if [ ! -f "$source" ] || [ -L "$source" ]; then
        problem "$destination needs missing or non-regular source $source."
        return
    fi
    if ! mkdir -p -- "$(dirname "$destination")"; then
        problem "cannot create the parent of $destination."
        return
    fi
    if publish_missing_file "$source" "$destination"; then
        installed_count=$((installed_count + 1))
        printf '  INSTALLED: %s\n' "$destination"
    else
        problem "$destination was not copied completely; existing content was preserved."
    fi
}

install_skill() {
    local name="$1" source="$CLAUDE_SRC/skills/$1" destination="$CLAUDE_DEST/skills/$1"
    local listing entry target relative valid=yes needed=no changed=no
    destination_parents_ok "$destination" || return
    # A seeded skill needs no absent source. When a source is available, check its
    # complete file inventory so a marker alone cannot hide missing references.
    if [ ! -f "$source/SKILL.md" ] || [ -L "$source" ] || [ -L "$source/SKILL.md" ]; then
        if [ -f "$destination/SKILL.md" ] && [ ! -L "$destination" ] && [ ! -L "$destination/SKILL.md" ]; then
            printf '  PRESERVED: %s (source not needed for an existing skill)\n' "$destination"
        else
            problem "$destination needs missing or non-regular source $source/SKILL.md."
        fi
        return
    fi
    if [ -L "$destination" ] || { [ -e "$destination" ] && [ ! -d "$destination" ]; }; then
        problem "$destination is an existing non-directory or link; left untouched."
        return
    fi
    if ! listing="$(mktemp)"; then
        problem "cannot inspect the complete $name source tree."
        return
    fi
    if ! find "$source" -mindepth 1 -print0 > "$listing"; then
        problem "cannot read the complete $name source tree."
        rm -f -- "$listing"
        return
    fi
    # Preflight every required destination before copying through any directory.
    while IFS= read -r -d '' entry; do
        relative="${entry#"$source"/}"
        target="$destination/$relative"
        if [ -L "$entry" ] || { [ ! -f "$entry" ] && [ ! -d "$entry" ]; }; then
            problem "$name source contains an unsupported entry: $entry."
            valid=no
        elif [ -L "$target" ]; then
            problem "$target is an existing link; left untouched."
            valid=no
        elif [ -e "$target" ]; then
            if { [ -d "$entry" ] && [ ! -d "$target" ]; } || { [ -f "$entry" ] && [ ! -f "$target" ]; }; then
                problem "$target has an incompatible existing type; left untouched."
                valid=no
            fi
        else
            needed=yes
        fi
    done < "$listing"
    if [ "$valid" = no ]; then
        rm -f -- "$listing"
        return
    fi
    if [ "$needed" = no ]; then
        printf '  PRESERVED: %s (all required files are present)\n' "$destination"
        rm -f -- "$listing"
        return
    fi
    if ! mkdir -p -- "$destination"; then
        problem "cannot create $destination."
        rm -f -- "$listing"
        return
    fi
    while IFS= read -r -d '' entry; do
        relative="${entry#"$source"/}"
        target="$destination/$relative"
        if [ -d "$entry" ]; then
            if ! mkdir -p -- "$target"; then
                valid=no
                problem "cannot create $target."
                break
            fi
        elif [ ! -e "$target" ] && [ ! -L "$target" ]; then
            if publish_missing_file "$entry" "$target"; then
                changed=yes
            else
                valid=no
                problem "$target was not copied completely."
                break
            fi
        fi
    done < "$listing"
    # Verify every required entry, including references, after the attempted copy.
    while IFS= read -r -d '' entry; do
        relative="${entry#"$source"/}"
        target="$destination/$relative"
        if [ -L "$target" ] || { [ -f "$entry" ] && [ ! -f "$target" ]; } || { [ -d "$entry" ] && [ ! -d "$target" ]; }; then
            valid=no
        fi
    done < "$listing"
    rm -f -- "$listing"
    if [ "$valid" = yes ]; then
        if [ "$changed" = yes ]; then
            installed_count=$((installed_count + 1))
        fi
        printf '  AVAILABLE: %s (complete required tree; existing files preserved)\n' "$destination"
    else
        problem "$destination is incomplete; do not treat this skill as available."
    fi
}

echo "MAM-basics SessionStart hook: checking Ben's tracked user-level Claude configuration."
echo "Sources: $REPO (the checked-out branch)."

# Validate the declaration without treating a malformed name as a path.
skills=()
inventory_ok=yes
inventory="$CLAUDE_SRC/shared-skills.txt"
if [ ! -f "$inventory" ] || [ -L "$inventory" ]; then
    problem "shared-skill inventory is missing or non-regular: $inventory."
    inventory_ok=no
else
    while IFS= read -r name || [ -n "$name" ]; do
        name="${name#"${name%%[![:space:]]*}"}"
        name="${name%"${name##*[![:space:]]}"}"
        if [ -z "$name" ] || [[ "$name" == \#* ]]; then
            continue
        fi
        if [[ ! "$name" =~ ^[a-z0-9][a-z0-9_-]*$ ]]; then
            problem "invalid shared-skill name: $name."
            inventory_ok=no
            continue
        fi
        for previous in "${skills[@]}"; do
            if [ "$previous" = "$name" ]; then
                problem "duplicate shared-skill name: $name."
                inventory_ok=no
            fi
        done
        skills+=("$name")
    done < "$inventory"
    if [ "${#skills[@]}" -eq 0 ]; then
        problem "the shared-skill inventory is empty."
        inventory_ok=no
    fi
fi

install_file "$CODEX_SRC/user-wide-AGENTS.md" "$CODEX_DEST/AGENTS.md"
install_file "$CLAUDE_SRC/user-wide-CLAUDE.md" "$CLAUDE_DEST/CLAUDE.md"
if [ "$inventory_ok" = yes ]; then
    for name in "${skills[@]}"; do
        install_skill "$name"
    done
fi

if [ "$problem_count" -eq 0 ]; then
    echo "MAM-basics SessionStart hook: all declared resources are in place; $installed_count resource(s) installed or completed."
else
    echo "MAM-basics SessionStart hook: USER-LEVEL CONFIGURATION IS INCOMPLETE ($problem_count problem(s))."
    echo "Tell Ben which resource is unavailable before the task; do not treat its rules as read."
    echo "See $DOC_NOTE."
fi
echo "Read $CODEX_DEST/AGENTS.md and $CLAUDE_DEST/CLAUDE.md before the first edit."
echo "If a shared skill is absent from your available-skills list, read its SKILL.md directly under $CLAUDE_DEST/skills/."
echo "Skill installation does not establish workflow dependencies, credentials or permissions; follow each skill's cloud limits."
exit 0
