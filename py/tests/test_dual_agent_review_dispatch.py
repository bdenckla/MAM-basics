"""Compare dispatched local Git results with independent branch and path observations."""

import json
from pathlib import Path
import re
import subprocess
import sys
import pytest

from mb_cmn.git_process import git_command
from repo_util import dual_agent_review_dispatch as dispatch
from repo_util import dual_agent_review_round as protocol


def observe(repo, *arguments):
    return subprocess.run(
        git_command(repo, *arguments), capture_output=True, check=True
    ).stdout


def test_local_dispatch_against_git_oracle(tmp_path, monkeypatch):
    home = tmp_path / "MAM-basics"
    remote = tmp_path / "mailbox.git"
    home.mkdir()
    remote.mkdir()
    observe(remote, "init", "--bare")
    observe(home, "init", "-b", "main")
    observe(home, "config", "user.name", "Rehearsal")
    observe(home, "config", "user.email", "rehearsal@example.invalid")
    (home / ".gitignore").write_text(
        ".novc/\n.claude/worktrees/\n", encoding="utf-8", newline="\n"
    )
    observe(home, "add", ".gitignore")
    observe(home, "commit", "-m", "Local rehearsal baseline")
    observe(home, "remote", "add", "origin", remote.as_posix())
    baseline = observe(home, "rev-parse", "HEAD").decode("ascii").strip()
    configuration = dispatch.load_config()
    configuration.update(
        claude_cli=sys.executable, codex_cli=sys.executable, turn_cap=4
    )
    monkeypatch.setattr(dispatch, "codex_settings", lambda: {"model": "gpt-6.1-sol"})
    empty_runtime = lambda checkout: {"blockers": []}
    monkeypatch.setattr(dispatch, "runtime_facts", empty_runtime)
    monkeypatch.setattr(protocol, "runtime_facts", empty_runtime)
    control = tmp_path / "control"
    round_date = "2026-09-30"
    # Independent Git configuration exposes every destination, including push-only URLs.
    observe(home, "config", "--add", "remote.origin.pushurl", remote.as_posix())
    observe(home, "config", "--add", "remote.origin.pushurl", remote.as_posix())
    assert (
        len(
            observe(home, "remote", "get-url", "--push", "--all", "origin").splitlines()
        )
        == 2
    )
    with pytest.raises(protocol.ReviewError):
        dispatch.start(
            home,
            round_date,
            agent1="claude",
            start_commit=baseline,
            end_commit=baseline,
            instruction="Refuse ambiguous rehearsal destinations.",
            config=configuration,
            rehearsal=True,
            control=control,
        )
    observe(home, "config", "--unset-all", "remote.origin.pushurl")
    observe(
        home, "config", "remote.origin.pushurl", "https://example.invalid/mailbox.git"
    )

    def no_outbound_query(*arguments):
        pytest.fail("refused local rehearsal attempted an outbound remote query")

    with monkeypatch.context() as local_only:
        local_only.setattr(dispatch, "remote_tip", no_outbound_query)
        with pytest.raises(protocol.ReviewError):
            dispatch.start(
                home,
                round_date,
                agent1="claude",
                start_commit=baseline,
                end_commit=baseline,
                instruction="Refuse a network push destination.",
                config=configuration,
                rehearsal=True,
                control=control,
            )
    observe(home, "config", "--unset-all", "remote.origin.pushurl")
    assert not observe(remote, "for-each-ref", "--format=%(refname)", "refs/heads/")
    assert not (control / "rounds.json").exists()
    dispatch.start(
        home,
        round_date,
        agent1="claude",
        start_commit=baseline,
        end_commit=baseline,
        instruction="Rehearse the local mailbox.",
        config=configuration,
        rehearsal=True,
        control=control,
    )

    invocations = []

    def deterministic_worker(command, prompt, checkout, log, timeout):
        marker = json.loads(
            (home / ".novc/dual-agent-review" / round_date / "inflight.json").read_text(
                encoding="utf-8"
            )
        )
        number, agent = marker["turn"], marker["agent"]
        invocations.append(number)
        filename = f"doc/dual-agent-review-{round_date}-turn-{number:02}-{agent}.md"
        if number == 1:
            state = "State: not yet acted on"
            next_line = "Next: turn 02, codex"
        elif number == 2:
            state = "State: completed 2026-09-30; review only"
            next_line = "Next: turn 03, claude; acknowledgment"
            first = checkout / f"doc/dual-agent-review-{round_date}-turn-01-claude.md"
            dispatch.write_text(
                first,
                first.read_text(encoding="utf-8")
                + "\n## Reconciliation\n\nLocal oracle agrees.\n",
            )
        else:
            state = "State: completed 2026-09-30; review only"
            next_line = "Next: none; round closed"
        dispatch.write_text(
            checkout / filename,
            f"# Rehearsal turn {number:02}\n\n{state}\n{next_line}\n\n## Findings\n\nRehearse the local mailbox.\n",
        )
        dispatch.write_text(log, '{"type":"turn.completed"}\n')

    for number in range(1, 4):
        if number == 1:
            real_git = protocol.git

            def rejected_push(repo, *arguments, **options):
                if arguments[0] == "push":
                    raise protocol.ReviewError("forced local push failure")
                return real_git(repo, *arguments, **options)

            with monkeypatch.context() as failure:
                failure.setattr(protocol, "git", rejected_push)
                with pytest.raises(protocol.ReviewError):
                    dispatch.tick_round(
                        home,
                        round_date,
                        configuration,
                        worker=deterministic_worker,
                        toast=False,
                    )
            directory = home / ".novc/dual-agent-review" / round_date
            assert (directory / "NEEDS-BEN.md").is_file()
            approved = json.loads(
                (directory / "inflight.json").read_text(encoding="utf-8")
            )
            assert (
                approved["approved_tree"]
                == observe(Path(approved["checkout"]), "rev-parse", "HEAD^{tree}")
                .decode("ascii")
                .strip()
            )
            recovered = dispatch.handoff(home, round_date, directory)
            assert (
                recovered
                == observe(remote, "rev-parse", "refs/heads/dar-2026-09-30")
                .decode("ascii")
                .strip()
            )
            assert not (directory / "inflight.json").exists()
            (directory / "PAUSE").unlink()
            state = protocol.status(home, round_date)
        else:
            state = dispatch.tick_round(
                home,
                round_date,
                configuration,
                worker=deterministic_worker,
                toast=False,
            )
        remote_head = (
            observe(remote, "rev-parse", "refs/heads/dar-2026-09-30")
            .decode("ascii")
            .strip()
        )
        assert remote_head == state["tip"]
        filenames = (
            observe(remote, "ls-tree", "-r", "--name-only", "-z", remote_head)
            .decode("utf-8")
            .split("\0")
        )
        oracle = [
            name
            for name in filenames
            if re.fullmatch(
                r"doc/dual-agent-review-2026-09-30-turn-[0-9]{2}-(claude|codex)[.]md",
                name,
            )
        ]
        assert len(oracle) == number == state["last_turn"]
        assert observe(home, "rev-parse", "HEAD").decode("ascii").strip() == baseline
    assert state["stop_reason"] == "round closed"
    dispatch.tick_round(
        home, round_date, configuration, worker=deterministic_worker, toast=False
    )
    assert invocations == [1, 2, 3]

    # Exercise every guard against independent Git evidence in a new round.
    second_date = "2026-10-01"
    fresh = dispatch.start(
        home,
        second_date,
        agent1="claude",
        start_commit=baseline,
        end_commit=baseline,
        instruction="Check the gate.",
        config=configuration,
        rehearsal=True,
        control=control,
    )
    checkout = Path(fresh["checkouts"]["claude"])
    inflight = {
        "tip": fresh["tip"],
        "turn": 1,
        "agent": "claude",
        "agent1": "claude",
        "previous": None,
        "origin_identity": dispatch.origin_identity(checkout),
    }
    output = checkout / "doc/dual-agent-review-2026-10-01-turn-01-claude.md"
    dispatch.write_text(
        output,
        "# Gate rehearsal\n\nState: not yet acted on\nNext: turn 02, codex\n\n## Findings\n\nGate check.\n",
    )
    assert not dispatch.gate(home, second_date, checkout, inflight)
    observe(
        home, "config", "remote.origin.pushurl", "https://example.invalid/changed.git"
    )
    assert (
        observe(home, "remote", "get-url", "--push", "origin").strip()
        == b"https://example.invalid/changed.git"
    )
    with monkeypatch.context() as changed_destination:
        changed_destination.setattr(dispatch, "remote_tip", no_outbound_query)
        assert dispatch.gate(home, second_date, checkout, inflight)
    observe(home, "config", "--unset-all", "remote.origin.pushurl")
    foreign = checkout / "unexpected.txt"
    dispatch.write_text(foreign, "Preserve this evidence.\n")
    independently_dirty = observe(
        checkout, "status", "--porcelain=v1", "-z", "--untracked-files=all"
    )
    assert b"unexpected.txt" in independently_dirty
    assert dispatch.gate(home, second_date, checkout, inflight)
    foreign.unlink()
    observe(checkout, "add", "--", output.relative_to(checkout).as_posix())
    assert observe(checkout, "diff", "--cached", "--name-only", "-z")
    assert dispatch.gate(home, second_date, checkout, inflight)
    observe(checkout, "commit", "-m", "Forced worker breach")
    assert (
        observe(checkout, "rev-parse", "HEAD").decode("ascii").strip() != fresh["tip"]
    )
    assert dispatch.gate(home, second_date, checkout, inflight)
    observe(checkout, "push", "origin", "HEAD:refs/heads/dar-2026-10-01")
    actual_tip = (
        observe(remote, "rev-parse", "refs/heads/dar-2026-10-01")
        .decode("ascii")
        .strip()
    )
    assert actual_tip != fresh["tip"]
    assert any(
        "remote moved" in reason
        for reason in dispatch.gate(home, second_date, checkout, inflight)
    )
