"""Compare turn discovery with an independent Git census and lint protocol headers."""

from collections import defaultdict
from pathlib import Path
import re
import subprocess

from mb_cmn import paths
from mb_cmn.git_process import git_command
from repo_util import dual_agent_review_round as protocol


def test_turn_census_and_sequences():
    lint_automated_round_headers()
    root = paths.repo_root()
    raw = subprocess.run(
        git_command(root, "ls-files", "-z"), capture_output=True, check=True
    ).stdout
    filenames = [part.decode("utf-8") for part in raw.split(b"\0") if part]
    oracle = []
    pattern = re.compile(
        r"^doc/dual-agent-review-([0-9]{4}-[0-9]{2}-[0-9]{2})-turn-([0-9]{2})-(claude|codex)[.]md$"
    )
    for name in filenames:
        match = pattern.fullmatch(name)
        if match:
            oracle.append((match[1], int(match[2]), match[3], name))
    assert oracle, "tracked review-turn inputs are missing"
    assert protocol.census(filenames) == sorted(oracle)
    rounds = defaultdict(list)
    for entry in oracle:
        if entry[0] >= "2026-09-16":
            rounds[entry[0]].append(entry)
    assert rounds, "contiguous-round lint has no input"
    for entries in rounds.values():
        entries.sort()
        assert [entry[1] for entry in entries] == list(range(1, len(entries) + 1))
        agent1 = entries[0][2]
        for _, number, agent, filename in entries:
            assert agent == (agent1 if number % 2 else protocol.other(agent1))
            lines = (root / filename).read_text(encoding="utf-8").splitlines()
            assert lines[2].startswith("State: "), filename
            if number > 1:
                assert re.fullmatch(
                    r"State: completed \d{4}-\d{2}-\d{2}; review only", lines[2]
                ), filename


def test_next_transitions_against_independent_state_model():
    for agent1 in ("claude", "codex"):
        for number in range(1, 11):
            agent = (
                agent1 if number % 2 else ("claude" if agent1 == "codex" else "codex")
            )
            successor = "claude" if agent == "codex" else "codex"
            state = (
                "State: not yet acted on"
                if number == 1
                else "State: completed 2026-09-30; review only"
            )
            for acknowledgment in (False, True):
                previous = {
                    "kind": "turn",
                    "flag": "acknowledgment" if acknowledgment else None,
                }
                for kind in ("continue", "acknowledgment", "objection", "close", "Ben"):
                    if kind == "close":
                        marker = "Next: none; round closed"
                    elif kind == "Ben":
                        marker = "Next: Ben; decision needed"
                    else:
                        suffix = "" if kind == "continue" else "; " + kind
                        marker = f"Next: turn {number + 1:02}, {successor}{suffix}"
                    # Independent transition oracle: an acknowledgment has only three
                    # outcomes; ordinary turns cannot object or close.
                    expected = kind in (
                        ("close", "objection", "Ben")
                        if acknowledgment
                        else ("continue", "acknowledgment", "Ben")
                    )
                    for header_markers in (
                        (),
                        (marker,),
                        (marker, marker),
                        (marker, "Next: invalid"),
                    ):
                        for body in (
                            "",
                            marker + "\n",
                            "```text\n" + marker + "\n```\n",
                            "> " + marker + "\n",
                        ):
                            # The protocol's control field belongs only to the
                            # header; body quotations cannot alter a transition.
                            header_text = "\n".join(header_markers)
                            text = (
                                f"# Turn\n\n{state}\n{header_text}\n\n"
                                f"## Findings\n{body}"
                            )
                            accepted = True
                            try:
                                protocol.validate_turn(
                                    text, number, agent, agent1, previous
                                )
                            except protocol.ReviewError:
                                accepted = False
                            assert accepted == (
                                expected and len(header_markers) == 1
                            ), (
                                agent1,
                                number,
                                acknowledgment,
                                kind,
                                header_markers,
                                body,
                            )


def lint_automated_round_headers():
    root = paths.repo_root()
    filenames = protocol.tree_files(root, "HEAD")
    for filename in filenames:
        match = protocol.ROUND_PATH.fullmatch(filename)
        if not match:
            continue
        specification = protocol.parse_round(
            (root / filename).read_text(encoding="utf-8"),
            root,
            match[1],
            bind_checkout=False,
        )
        previous = None
        for round_date, number, agent, turn_file in protocol.census(filenames):
            if round_date == match[1]:
                previous = protocol.validate_turn(
                    (root / turn_file).read_text(encoding="utf-8"),
                    number,
                    agent,
                    specification["agent1"],
                    previous,
                )


def test_agent_deployment_source_and_mapping():
    from repo_util.user_config_sync import _ARCHIVE_PATHS

    root = paths.repo_root()
    source = Path("dot-claude/agents/dual-agent-review-turn.md")
    assert source in _ARCHIVE_PATHS
    assert (root / source).is_file()
    implementation = (root / "py/repo_util/user_config_sync.py").read_text(
        encoding="utf-8"
    )
    assert 'Path(".claude/agents/dual-agent-review-turn.md")' in implementation
