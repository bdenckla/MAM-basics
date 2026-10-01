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
            for acknowledgment in ((False, True) if number >= 3 else (False,)):
                previous = (
                    {
                        "kind": "turn",
                        "flag": "acknowledgment" if acknowledgment else None,
                    }
                    if number > 1
                    else None
                )
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
                    expected = expected and not (
                        number == 1 and kind == "acknowledgment"
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


def git_observe(repo, *arguments):
    return subprocess.run(
        git_command(repo, *arguments), capture_output=True, check=True
    ).stdout


def oracle_round(
    repo, round_date, agent1, turn_cap, reopening_cap, terminal=False, override=None
):
    """Author inputs from the approved grammar, independently of production rendering."""
    state = f"executed {round_date}; close-out completed" if terminal else "live"
    head = git_observe(repo, "rev-parse", "HEAD").decode("ascii").strip()
    lines = [
        f"# Independent round {round_date}",
        "",
        f"State: {state}",
        "Protocol: 1",
        f"Agent 1: {agent1}",
        f"Start: {head}",
        f"End: {head}",
        f"Turn cap: {turn_cap}",
        f"Reopening cap: {reopening_cap}",
        'Kickoff instruction: "Assess the independent protocol history."',
        "Claude model: claude-opus-5-5",
        "Claude effort: max",
        "Codex model: gpt-6.1-sol",
        "Codex effort: xhigh",
        "Facts only from turn 03: no",
        "Rehearsal: yes",
    ]
    for agent in ("claude", "codex"):
        checkout = (repo / ".claude/worktrees" / f"dar-{round_date}-{agent}").resolve()
        import json

        lines.append(
            agent.capitalize() + " checkout: " + json.dumps(checkout.as_posix())
        )
    if override:
        lines.append(f"Override: next turn {override[0]:02}, {override[1]}")
    return "\n".join(lines) + "\n\n## Evidence\n\nIndependent history.\n"


def test_protocol_status_against_reachable_git_histories_and_caps(tmp_path):
    repo = tmp_path / "r"
    repo.mkdir()
    git_observe(repo, "init", "-b", "main")
    git_observe(repo, "config", "user.name", "Protocol oracle")
    git_observe(repo, "config", "user.email", "oracle@example.invalid")
    (repo / "baseline.txt").write_text(
        "Independent baseline.\n", encoding="utf-8", newline="\n"
    )
    git_observe(repo, "add", "--", "baseline.txt")
    git_observe(repo, "commit", "-m", "Independent protocol baseline")
    scenarios = (
        [(["continue"] * cap, cap, 2, "turn cap reached", False) for cap in (3, 4, 5)]
        + [
            (
                [
                    "continue",
                    "acknowledgment",
                    "objection",
                    "acknowledgment",
                    "objection",
                ],
                9,
                cap,
                "reopening cap exceeded" if cap < 2 else None,
                False,
            )
            for cap in (0, 1, 2)
        ]
        + [
            (["continue", "acknowledgment", "close"], 9, 2, "round closed", False),
            (["continue", "Ben"], 9, 2, "Ben's decision required", False),
            (["continue"], 9, 2, "close-out completed", True),
        ]
    )
    for assignment, agent1 in enumerate(("claude", "codex")):
        for case, (
            actions,
            turn_cap,
            reopening_cap,
            expected_stop,
            terminal,
        ) in enumerate(scenarios):
            round_date = f"2026-{assignment + 1:02}-{case + 1:02}"
            round_name = f"doc/dual-agent-review-{round_date}-round.md"
            (repo / "doc").mkdir(exist_ok=True)
            metadata = repo / round_name
            metadata.write_text(
                oracle_round(repo, round_date, agent1, turn_cap, reopening_cap),
                encoding="utf-8",
                newline="\n",
            )
            git_observe(repo, "add", "--", round_name)
            git_observe(repo, "commit", "-m", "Independent round input")
            independently_owned = []
            for number, action in enumerate(actions, 1):
                agent = (
                    agent1
                    if number % 2
                    else ("claude" if agent1 == "codex" else "codex")
                )
                successor = "claude" if agent == "codex" else "codex"
                if action == "close":
                    next_line = "Next: none; round closed"
                elif action == "Ben":
                    next_line = "Next: Ben; Independently assessed decision"
                else:
                    suffix = "" if action == "continue" else "; " + action
                    next_line = f"Next: turn {number + 1:02}, {successor}{suffix}"
                state = (
                    "State: not yet acted on"
                    if number == 1
                    else f"State: completed {round_date}; review only"
                )
                name = f"doc/dual-agent-review-{round_date}-turn-{number:02}-{agent}.md"
                (repo / name).write_text(
                    f"# Independent turn\n\n{state}\n{next_line}\n\n## Findings\n\nIndependent evidence.\n",
                    encoding="utf-8",
                    newline="\n",
                )
                git_observe(repo, "add", "--", name)
                git_observe(repo, "commit", "-m", "Independent reachable transition")
                independently_owned.append((number, agent, name))
            if terminal:
                successor = "claude" if agent1 == "codex" else "codex"
                metadata.write_text(
                    oracle_round(
                        repo,
                        round_date,
                        agent1,
                        turn_cap,
                        reopening_cap,
                        terminal=True,
                        override=(2, successor),
                    ),
                    encoding="utf-8",
                    newline="\n",
                )
                git_observe(repo, "add", "--", round_name)
                git_observe(repo, "commit", "-m", "Independent completed close-out")
            head = git_observe(repo, "rev-parse", "HEAD").decode("ascii").strip()
            git_observe(
                repo, "update-ref", f"refs/remotes/origin/dar-{round_date}", head
            )
            result = protocol.status(repo, round_date, occupancy=False)
            assert not result["problems"], result
            assert result["stop_reason"] == expected_stop
            assert result["dispatchable"] == (expected_stop is None)
            assert result["reopenings"] == actions.count("objection")
            assert [
                (turn["turn"], turn["agent"], turn["path"]) for turn in result["turns"]
            ] == independently_owned
            assert result["tip"] == head
            assert result["terminal"] == terminal
