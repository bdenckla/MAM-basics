"""Compare dispatched local Git results with independent branch and path observations."""

from contextlib import contextmanager
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from types import SimpleNamespace
import pytest

from mb_cmn.git_process import git_command
from repo_util import dual_agent_review_dispatch as dispatch
from repo_util import dual_agent_review_round as protocol


def observe(repo, *arguments, environment=None, check=True):
    child_environment = os.environ.copy()
    if environment:
        child_environment.update(environment)
    return subprocess.run(
        git_command(repo, *arguments),
        capture_output=True,
        check=check,
        env=child_environment,
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

    def empty_runtime(checkout):
        return {"blockers": []}

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
                        control=control,
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
            monkeypatch.setattr(dispatch, "CONTROL", control)
            monkeypatch.setattr(
                dispatch, "load_config", lambda path=None: configuration
            )
            assert dispatch.run_action(action_args("handoff", home, round_date)) == 0
            recovered = protocol.status(home, round_date)["tip"]
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
                control=control,
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
        home,
        round_date,
        configuration,
        worker=deterministic_worker,
        toast=False,
        control=control,
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
        "remote moved" in reason.message
        for reason in dispatch.gate(home, second_date, checkout, inflight)
    )


def local_relay(directory, monkeypatch):
    """Build disposable inputs; Git observations remain independent of the dispatcher."""
    home, remote, control = directory / "h", directory / "a.git", directory / "c"
    home.mkdir(parents=True)
    remote.mkdir()
    observe(remote, "init", "--bare")
    observe(home, "init", "-b", "main")
    observe(home, "config", "user.name", "Differential oracle")
    observe(home, "config", "user.email", "oracle@example.invalid")
    (home / ".gitignore").write_text(
        ".novc/\n.claude/worktrees/\n", encoding="utf-8", newline="\n"
    )
    (home / ".gitattributes").write_text(
        "*.md text eol=lf\n", encoding="utf-8", newline="\n"
    )
    observe(home, "add", "--", ".gitignore", ".gitattributes")
    observe(home, "commit", "-m", "Disposable oracle baseline")
    observe(home, "remote", "add", "origin", remote.as_posix())
    config = dispatch.load_config()
    config.update(claude_cli=sys.executable, codex_cli=sys.executable, turn_cap=8)
    monkeypatch.setattr(dispatch, "codex_settings", lambda: {"model": "gpt-6.1-sol"})
    monkeypatch.setattr(dispatch, "runtime_facts", lambda checkout: {"blockers": []})
    monkeypatch.setattr(protocol, "runtime_facts", lambda checkout: {"blockers": []})
    baseline = observe(home, "rev-parse", "HEAD").decode("ascii").strip()
    return home, remote, control, config, baseline


def start_local(inputs, round_date="2026-09-30", agent1="claude"):
    home, remote, control, config, baseline = inputs
    return dispatch.start(
        home,
        round_date,
        agent1=agent1,
        start_commit=baseline,
        end_commit=baseline,
        instruction="Exercise the independently observed local mailbox.",
        config=config,
        rehearsal=True,
        control=control,
    )


def turn_name(round_date, number, agent):
    return f"doc/dual-agent-review-{round_date}-turn-{number:02}-{agent}.md"


def turn_bytes(round_date, number, agent, next_line=None):
    successor = "claude" if agent == "codex" else "codex"
    state = (
        "State: not yet acted on"
        if number == 1
        else f"State: completed {round_date}; review only"
    )
    next_line = next_line or f"Next: turn {number + 1:02}, {successor}"
    return (
        f"# Differential turn {number:02}\n\n{state}\n{next_line}\n\n"
        f"## Findings\n\nIndependent body for {number:02} and {agent}.\n"
    ).encode("utf-8")


def draft_from_marker(home, round_date, next_line=None):
    marker = dispatch.state_dir(home, round_date) / "inflight.json"
    inflight = json.loads(marker.read_text(encoding="utf-8"))
    checkout = Path(inflight["checkout"])
    filename = turn_name(round_date, inflight["turn"], inflight["agent"])
    output = checkout / filename
    output.parent.mkdir(exist_ok=True)
    output.write_bytes(
        turn_bytes(round_date, inflight["turn"], inflight["agent"], next_line)
    )
    if inflight["turn"] == 2:
        first = checkout / turn_name(round_date, 1, inflight["agent1"])
        with first.open("ab") as stream:
            stream.write(b"\n## Reconciliation\n\nIndependent append.\n")
    return inflight, output


def marker_for(state, remote):
    number, agent = state["next"]["turn"], state["next"]["agent"]
    return {
        "repo": state["repo"],
        "round": state["round"],
        "checkout": state["checkouts"][agent],
        "tip": state["tip"],
        "turn": number,
        "agent": agent,
        "agent1": state["agent1"],
        "previous": state["turns"][-1]["next"] if state["turns"] else None,
        "repository_identity": {
            "kind": "local",
            "git_dir": Path(
                observe(
                    remote, "rev-parse", "--path-format=absolute", "--git-common-dir"
                )
                .decode("utf-8")
                .strip()
            )
            .resolve()
            .as_posix(),
        },
    }


def refs(repo):
    return observe(repo, "show-ref", check=False)


def index_entries(repo):
    return observe(repo, "ls-files", "--stage", "-z")


def oracle_index(checkout, baseline, owned, directory):
    """Ask Git directly about proposed bytes, without invoking the production helper."""
    directory.mkdir()
    environment = {"GIT_INDEX_FILE": str(directory / "index")}
    observe(checkout, "read-tree", baseline, environment=environment)
    observe(checkout, "add", "--", *owned, environment=environment)
    result = subprocess.run(
        git_command(checkout, "diff", "--cached", "--check"),
        capture_output=True,
        env={**os.environ, **environment},
        check=False,
    )
    tree = observe(checkout, "write-tree", environment=environment).strip()
    return result, tree.decode("ascii")


def successful_worker(home, round_date, controls=None):
    def worker(command, prompt, checkout, log, timeout):
        marker = json.loads(
            (dispatch.state_dir(home, round_date) / "inflight.json").read_text(
                encoding="utf-8"
            )
        )
        next_line = controls.get(marker["turn"]) if controls else None
        draft_from_marker(home, round_date, next_line)
        log.write_text('{"type":"turn.completed"}\n', encoding="utf-8", newline="\n")
        if "-o" in command:
            Path(command[command.index("-o") + 1]).write_text(
                prompt, encoding="utf-8", newline="\n"
            )

    return worker


def action_args(action, home=None, round_date=None):
    return SimpleNamespace(
        dual_agent_review=action,
        repo=home.as_posix() if home else None,
        round=round_date,
        automation_config=None,
        agent=None,
    )


def test_proposed_bytes_against_git_index_oracle(tmp_path, monkeypatch):
    inputs = local_relay(tmp_path, monkeypatch)
    home, remote, control, config, baseline = inputs
    for case, (number, trailing, enabled) in enumerate(
        (number, trailing, enabled)
        for number in (1, 2)
        for trailing in (False, True)
        for enabled in (False, True)
    ):
        round_date = f"2026-09-{case + 1:02}"
        observe(
            home,
            "config",
            "core.whitespace",
            "blank-at-eol" if enabled else "-blank-at-eol",
        )
        state = start_local(inputs, round_date)
        if number == 2:
            state = dispatch.tick_round(
                home,
                round_date,
                config,
                worker=successful_worker(home, round_date),
                toast=False,
                control=control,
            )
        inflight = marker_for(state, remote)
        checkout = Path(inflight["checkout"])
        observe(checkout, "merge", "--ff-only", state["tip"])
        directory = dispatch.state_dir(home, round_date)
        dispatch.write_json(directory / "inflight.json", inflight)
        _, output = draft_from_marker(home, round_date)
        owned = [output.relative_to(checkout).as_posix()]
        target = output
        if number == 2:
            target = checkout / turn_name(round_date, 1, state["agent1"])
            owned.append(target.relative_to(checkout).as_posix())
        if trailing:
            with target.open("ab") as stream:
                stream.write(b"Oracle whitespace. \n")
        expected, tree = oracle_index(
            checkout, state["tip"], owned, home / ".novc" / f"oracle-index-{case}"
        )
        before = (
            index_entries(checkout),
            refs(remote),
            observe(checkout, "rev-parse", "HEAD"),
        )
        bytes_before = {name: (checkout / name).read_bytes() for name in owned}
        failures = dispatch.gate(home, round_date, checkout, inflight)
        assert bool(failures) == bool(expected.returncode)
        if expected.returncode:
            assert {failure.category for failure in failures} == {"whitespace"}
            assert expected.stdout.decode("utf-8").strip() in failures[0].message
            with pytest.raises(protocol.ReviewError):
                dispatch.handoff(home, round_date, directory)
            assert "approved_tree" not in json.loads(
                (directory / "inflight.json").read_text(encoding="utf-8")
            )
        else:
            assert dispatch.proposed_tree(checkout, state["tip"], owned) == tree
        assert before == (
            index_entries(checkout),
            refs(remote),
            observe(checkout, "rev-parse", "HEAD"),
        )
        assert bytes_before == {name: (checkout / name).read_bytes() for name in owned}
        assert observe(home, "rev-parse", "HEAD").decode("ascii").strip() == baseline


def test_legacy_unapproved_index_preserves_git_evidence(tmp_path, monkeypatch):
    inputs = local_relay(tmp_path, monkeypatch)
    home, remote, control, config, baseline = inputs
    state = start_local(inputs)
    inflight = marker_for(state, remote)
    # Old attempts had URL fingerprints, but no approved-tree or subject field.
    inflight.pop("repository_identity")
    inflight["origin_identity"] = dispatch.origin_identity(Path(inflight["checkout"]))
    directory = dispatch.state_dir(home, state["round"])
    marker = directory / "inflight.json"
    dispatch.write_json(marker, inflight)
    _, output = draft_from_marker(home, state["round"])
    with output.open("ab") as stream:
        stream.write(b"Preserved unapproved bytes. \n")
    checkout = Path(inflight["checkout"])
    name = output.relative_to(checkout).as_posix()
    observe(checkout, "add", "--", name)
    before = (
        index_entries(checkout),
        marker.read_bytes(),
        output.read_bytes(),
        refs(remote),
    )
    for _ in range(2):
        with pytest.raises(protocol.ReviewError):
            dispatch.handoff(home, state["round"], directory)
        assert before == (
            index_entries(checkout),
            marker.read_bytes(),
            output.read_bytes(),
            refs(remote),
        )
    # Explicit local recovery corrects bytes and removes only their staging.
    observe(checkout, "restore", "--staged", "--", name)
    output.write_bytes(turn_bytes(state["round"], 1, "claude"))
    committed = dispatch.handoff(home, state["round"], directory)
    assert observe(remote, "show", f"{committed}:{name}", "--") == output.read_bytes()
    assert observe(checkout, "show", "-s", "--format=%P", committed).strip() == state[
        "tip"
    ].encode("ascii")
    assert observe(home, "rev-parse", "HEAD").decode("ascii").strip() == baseline


def test_destination_identity_against_independent_local_and_github_oracles(
    tmp_path, monkeypatch
):
    inputs = local_relay(tmp_path, monkeypatch)
    home, remote, control, config, baseline = inputs
    expected = {"kind": "local", "git_dir": remote.resolve().as_posix()}
    for spelling in (
        remote.as_posix(),
        "../a.git",
        (remote / ".." / remote.name).as_posix(),
        remote.as_uri(),
    ):
        assert dispatch.resolve_destination(home, spelling) == expected
    for owner in ("denckla", "Owner.With-dash"):
        for repository in ("MAM-basics", "r_test"):
            expected_github = {
                "kind": "github",
                "host": "github.com",
                "owner": owner.lower(),
                "repository": repository.lower(),
            }
            for suffix in ("", ".git"):
                for spelling in (
                    f"https://github.com/{owner}/{repository}{suffix}",
                    f"git@github.com:{owner}/{repository}{suffix}",
                    f"ssh://git@github.com/{owner}/{repository}{suffix}",
                ):
                    assert (
                        dispatch.resolve_destination(home, spelling) == expected_github
                    )
    second = tmp_path / "b.git"
    observe(home, "clone", "--bare", remote.as_posix(), second.as_posix())
    before = refs(remote), refs(second), refs(home)
    observe(home, "config", "remote.origin.pushurl", second.as_posix())
    with pytest.raises(protocol.ReviewError):
        start_local(inputs)
    assert before == (refs(remote), refs(second), refs(home))
    assert not (control / "rounds.json").exists()
    assert not (home / ".claude/worktrees").exists()


def test_retained_identity_refuses_between_dispatch_and_worktree_splits(
    tmp_path, monkeypatch
):
    for case, mutation in enumerate(
        ("home-push", "home-both", "worker-push", "worker-fetch", "worker-rewrite")
    ):
        inputs = local_relay(tmp_path / str(case), monkeypatch)
        home, remote, control, config, baseline = inputs
        state = start_local(inputs)
        second = home.parent / "b.git"
        observe(home, "clone", "--bare", remote.as_posix(), second.as_posix())
        before = refs(remote), refs(second)
        checkout = Path(state["checkouts"]["claude"])
        if mutation.startswith("home"):
            observe(home, "config", "remote.origin.pushurl", second.as_posix())
            if mutation == "home-both":
                observe(home, "config", "remote.origin.url", second.as_posix())
        else:
            observe(home, "config", "extensions.worktreeConfig", "true")
            if mutation == "worker-push":
                observe(
                    checkout,
                    "config",
                    "--worktree",
                    "remote.origin.pushurl",
                    second.as_posix(),
                )
            elif mutation == "worker-fetch":
                observe(
                    checkout,
                    "config",
                    "--worktree",
                    "remote.origin.url",
                    second.as_posix(),
                )
            else:
                observe(
                    checkout,
                    "config",
                    "--worktree",
                    f"url.{second.as_posix()}.pushInsteadOf",
                    remote.as_posix(),
                )
        calls = []

        def never_worker(*arguments):
            calls.append(arguments)
            pytest.fail("identity refusal launched a worker")

        with pytest.raises(protocol.ReviewError):
            dispatch.tick_round(
                home,
                state["round"],
                config,
                worker=never_worker,
                toast=False,
                control=control,
            )
        assert not calls
        assert before == (refs(remote), refs(second))
        assert observe(home, "rev-parse", "HEAD").decode("ascii").strip() == baseline


def test_gate_categories_against_faults_and_git_write_oracle(tmp_path, monkeypatch):
    expected_categories = {
        "foreign": "paths",
        "staged": "staging",
        "occupied": "ownership",
        "identity": "identity",
        "whitespace": "whitespace",
        "read-tree": "git",
        "mixed": "paths",
    }
    for case, (fault, expected) in enumerate(expected_categories.items()):
        inputs = local_relay(tmp_path / str(case), monkeypatch)
        home, remote, control, config, baseline = inputs
        state = start_local(inputs)
        directory = dispatch.state_dir(home, state["round"])
        second = home.parent / "b.git"
        observe(home, "clone", "--bare", remote.as_posix(), second.as_posix())
        before = refs(remote), refs(second)
        invocations, owned_bytes = [], {}
        active = {"value": False}
        real_git = protocol.git

        def fault_git(repo, *arguments, **options):
            if fault == "read-tree" and active["value"] and arguments[0] == "read-tree":
                raise protocol.ReviewError(
                    "Next: State: acknowledgment D10 operational failure"
                )
            return real_git(repo, *arguments, **options)

        with monkeypatch.context() as faults:
            faults.setattr(protocol, "git", fault_git)
            if fault == "occupied":
                faults.setattr(
                    dispatch,
                    "runtime_facts",
                    lambda checkout: {
                        "blockers": (
                            ["Next: State: acknowledgment D10"]
                            if active["value"]
                            else []
                        )
                    },
                )

            def worker(command, prompt, checkout, log, timeout):
                invocations.append(log)
                _, output = draft_from_marker(home, state["round"])
                if fault in ("foreign", "mixed"):
                    (checkout / "acknowledgment-D10.txt").write_text(
                        "Next: State:\n", encoding="utf-8", newline="\n"
                    )
                if fault == "mixed":
                    output.write_bytes(
                        output.read_bytes().replace(
                            b"State: not yet acted on", b"State: invalid"
                        )
                    )
                elif fault == "staged":
                    observe(
                        checkout, "add", "--", output.relative_to(checkout).as_posix()
                    )
                elif fault == "identity":
                    observe(home, "config", "extensions.worktreeConfig", "true")
                    observe(
                        checkout,
                        "config",
                        "--worktree",
                        "remote.origin.pushurl",
                        second.as_posix(),
                    )
                elif fault == "whitespace":
                    with output.open("ab") as stream:
                        stream.write(b"Next: State: acknowledgment D10 \n")
                owned_bytes[output] = output.read_bytes()
                log.write_text(
                    '{"type":"turn.completed"}\n', encoding="utf-8", newline="\n"
                )
                active["value"] = True

            with pytest.raises(protocol.ReviewError):
                dispatch.tick_round(
                    home,
                    state["round"],
                    config,
                    worker=worker,
                    toast=False,
                    control=control,
                )
        assert len(invocations) == 1, (fault, invocations)
        attempts = list((directory / "attempts").iterdir())
        assert len(attempts) == 1
        errors = json.loads(
            (attempts[0] / "initial-refusal/gate.json").read_text(encoding="utf-8")
        )
        assert expected in {error["category"] for error in errors}, (fault, errors)
        assert not (attempts[0] / "fixup").exists()
        assert before == (refs(remote), refs(second))
        assert all(path.read_bytes() == value for path, value in owned_bytes.items())
        manifest = json.loads(
            (attempts[0] / "initial-refusal/files.json").read_text(encoding="utf-8")
        )
        for path, value in owned_bytes.items():
            assert (
                attempts[0]
                / "initial-refusal"
                / manifest[path.relative_to(path.parents[1]).as_posix()]
            ).read_bytes() == value
        assert observe(home, "rev-parse", "HEAD").decode("ascii").strip() == baseline


def test_header_fixup_attempts_against_owned_bytes_and_launch_oracles(
    tmp_path, monkeypatch
):
    for case, (number, corruption) in enumerate(
        (number, corruption) for number in (1, 2) for corruption in ("state", "next")
    ):
        inputs = local_relay(tmp_path / str(case), monkeypatch)
        home, remote, control, config, baseline = inputs
        state = start_local(inputs, agent1="codex")
        if number == 2:
            state = dispatch.tick_round(
                home,
                state["round"],
                config,
                worker=successful_worker(home, state["round"]),
                toast=False,
                control=control,
            )
        directory = dispatch.state_dir(home, state["round"])
        invocations, refused, command_outputs = [], {}, []

        def worker(command, prompt, checkout, log, timeout):
            invocations.append((command, prompt, log))
            if len(invocations) == 1:
                marker, output = draft_from_marker(home, state["round"])
                lines = output.read_bytes().splitlines(keepends=True)
                if corruption == "state":
                    lines[2] = b"State: invalid\n"
                else:
                    lines[3] = b"Next: invalid\n"
                output.write_bytes(b"".join(lines))
                refused.update(
                    {
                        path.relative_to(checkout).as_posix(): path.read_bytes()
                        for path in (checkout / "doc").iterdir()
                        if path.name.startswith("dual-agent-review")
                        and "-turn-" in path.name
                    }
                )
            else:
                dirty = observe(
                    checkout, "status", "--porcelain=v1", "-z", "--untracked-files=all"
                )
                actual = [
                    part[3:].decode("utf-8") for part in dirty.split(b"\0") if part
                ]
                match = re.search(r"Expected dirty paths \(JSON\): (.*)", prompt)
                assert match
                assert set(json.loads(match[1])) == set(actual)
                assert (
                    observe(checkout, "rev-parse", "HEAD").decode("ascii").strip()
                    in prompt
                )
                assert not observe(checkout, "diff", "--cached", "--name-only", "-z")
                output = checkout / turn_name(
                    state["round"], number, state["next"]["agent"]
                )
                original_body = output.read_bytes().split(b"## Findings", 1)[1]
                output.write_bytes(
                    turn_bytes(state["round"], number, state["next"]["agent"])
                )
                assert output.read_bytes().split(b"## Findings", 1)[1] == original_body
            log.write_text(
                json.dumps({"type": "turn.completed", "invocation": len(invocations)})
                + "\n",
                encoding="utf-8",
                newline="\n",
            )
            if "-o" in command:
                last = Path(command[command.index("-o") + 1])
                command_outputs.append(last)
                last.write_text(prompt, encoding="utf-8", newline="\n")

        final = dispatch.tick_round(
            home, state["round"], config, worker=worker, toast=False, control=control
        )
        assert len(invocations) == 2
        assert len({item[2] for item in invocations}) == 2
        assert len(set(command_outputs)) == len(command_outputs)
        attempt = invocations[0][2].parents[1]
        for command, prompt, log in invocations:
            assert (log.parent / "prompt.md").read_text(encoding="utf-8") == prompt
            saved = json.loads((log.parent / "launch.json").read_text(encoding="utf-8"))
            assert saved["command"] == command
            assert log.is_file()
        for name, value in refused.items():
            if number == 2 or "-turn-01-" in name:
                refused_directory = attempt / "initial-refusal"
                manifest = json.loads(
                    (refused_directory / "files.json").read_text(encoding="utf-8")
                )
                assert (refused_directory / manifest[name]).read_bytes() == value
        assert {
            item["category"]
            for item in json.loads(
                (attempt / "initial-refusal/gate.json").read_text(encoding="utf-8")
            )
        } == {"header"}
        new_turn = turn_name(state["round"], number, state["next"]["agent"])
        assert observe(
            remote, "show", f"{final['tip']}:{new_turn}", "--"
        ) == turn_bytes(state["round"], number, state["next"]["agent"])
        assert observe(home, "rev-parse", "HEAD").decode("ascii").strip() == baseline


def test_redispatch_preserves_initial_and_failed_fixup_evidence(tmp_path, monkeypatch):
    inputs = local_relay(tmp_path, monkeypatch)
    home, remote, control, config, baseline = inputs
    state = start_local(inputs, agent1="codex")
    directory = dispatch.state_dir(home, state["round"])
    invocations = []

    def refusing_worker(command, prompt, checkout, log, timeout):
        invocations.append(log)
        _, output = draft_from_marker(home, state["round"])
        output.write_bytes(
            output.read_bytes().replace(b"Next: turn 02, claude", b"Next: invalid")
        )
        log.write_text('{"type":"turn.completed"}\n', encoding="utf-8", newline="\n")
        Path(command[command.index("-o") + 1]).write_text(
            prompt, encoding="utf-8", newline="\n"
        )

    with pytest.raises(protocol.ReviewError):
        dispatch.tick_round(
            home,
            state["round"],
            config,
            worker=refusing_worker,
            toast=False,
            control=control,
        )
    assert len(invocations) == 2
    attempt = invocations[0].parents[1]
    assert (attempt / "initial-refusal/gate.json").is_file()
    assert (attempt / "fixup-refusal/gate.json").is_file()
    preserved = {
        path: path.read_bytes() for path in attempt.rglob("*") if path.is_file()
    }
    marker = directory / "inflight.json"
    inflight = json.loads(marker.read_text(encoding="utf-8"))
    output = Path(inflight["checkout"]) / turn_name(state["round"], 1, "codex")
    # The simulated manual resolution retains both marker and abandoned draft.
    output.rename(directory / "manually-retained-draft.md")
    marker.rename(directory / "manually-resolved-inflight.json")
    monkeypatch.setattr(dispatch, "CONTROL", control)
    assert dispatch.run_action(action_args("resume", home, state["round"])) == 0
    final = dispatch.tick_round(
        home,
        state["round"],
        config,
        worker=successful_worker(home, state["round"]),
        toast=False,
        control=control,
    )
    assert len(list((directory / "attempts").iterdir())) == 2
    assert all(path.read_bytes() == value for path, value in preserved.items())
    assert final["last_turn"] == 1
    assert observe(home, "rev-parse", "HEAD").decode("ascii").strip() == baseline


def test_notification_episodes_against_recovery_event_oracle(tmp_path, monkeypatch):
    inputs = local_relay(tmp_path, monkeypatch)
    home, remote, control, config, baseline = inputs
    config = {**config, "enabled_agents": []}
    monkeypatch.setattr(dispatch, "CONTROL", control)
    monkeypatch.setattr(dispatch, "load_config", lambda path=None: config)
    real_notify = dispatch.notify

    def local_notice(repo, round_date, reason, **options):
        real_notify(repo, round_date, reason, **{**options, "toast": False})

    monkeypatch.setattr(dispatch, "notify", local_notice)
    for case, cause in enumerate(("refusal", "marker", "lock"), 1):
        round_date = f"2026-08-{case:02}"
        start_local(inputs, round_date)
        directory = dispatch.state_dir(home, round_date)
        records = {}
        for episode in (1, 2):
            if cause == "refusal":
                dispatch.write_text(directory / "PAUSE", "Preserved failure.\n")
                for _ in range(2):
                    dispatch.notify(home, round_date, "repeated failure", toast=False)
            elif cause == "marker":
                dispatch.write_json(directory / "inflight.json", {"attempt": episode})
                for _ in range(2):
                    state = dispatch.tick_round(
                        home, round_date, config, toast=False, control=control
                    )
                    assert not state["dispatchable"]
            else:
                dispatch.write_json(
                    control / "dispatcher.lock",
                    {
                        "pid": episode,
                        "started_at": f"2026-08-01T00:00:0{episode}-04:00",
                    },
                )
                for _ in range(2):
                    assert (
                        dispatch.run_action(action_args("tick", home, round_date)) == 1
                    )
            notices = list(directory.glob("notice-*.md"))
            assert len(notices) == episode, (cause, episode, notices)
            assert all(path.read_bytes() == value for path, value in records.items())
            records.update({path: path.read_bytes() for path in notices})
            if cause == "refusal":
                assert dispatch.run_action(action_args("resume", home, round_date)) == 0
            elif cause == "marker":
                (directory / "inflight.json").rename(
                    directory / f"resolved-marker-{episode}.json"
                )
                dispatch.tick_round(
                    home, round_date, config, toast=False, control=control
                )
            else:
                (control / "dispatcher.lock").rename(
                    control / f"resolved-lock-{episode}.json"
                )
                assert dispatch.run_action(action_args("tick", home, round_date)) == 0
        assert observe(home, "rev-parse", "HEAD").decode("ascii").strip() == baseline

    real_lock = dispatch.lock
    for timing in ("caught", "notify"):
        lock_path = control / "dispatcher.lock"
        dispatch.write_json(lock_path, {"observed": timing})
        preserved = control / f"finished-lock-{timing}.json"

        @contextmanager
        def disappearing_lock(selected_control):
            try:
                with real_lock(selected_control):
                    yield
            except dispatch.LockExists:
                if timing == "caught":
                    lock_path.rename(preserved)
                raise

        def disappearing_notice(repo, selected_date, reason, **options):
            if timing == "notify" and lock_path.exists():
                lock_path.rename(preserved)
            local_notice(repo, selected_date, reason, **options)

        with monkeypatch.context() as recovery:
            recovery.setattr(dispatch, "lock", disappearing_lock)
            recovery.setattr(dispatch, "notify", disappearing_notice)
            assert dispatch.run_action(action_args("tick")) == 1
        assert preserved.is_file() and not lock_path.exists()
        assert observe(home, "rev-parse", "HEAD").decode("ascii").strip() == baseline


def test_stop_notices_and_inactive_rounds_against_two_round_git_oracle(
    tmp_path, monkeypatch
):
    inputs = local_relay(tmp_path, monkeypatch)
    home, remote, control, config, baseline = inputs
    round_date = "2026-09-30"
    state = start_local(inputs, round_date)
    reason = "Assess the independently observed destinations before continuing"
    worker = successful_worker(home, round_date, {1: "Next: Ben; " + reason})
    state = dispatch.tick_round(
        home, round_date, config, worker=worker, toast=False, control=control
    )
    directory = dispatch.state_dir(home, round_date)
    notices = {path: path.read_bytes() for path in directory.glob("notice-*.md")}
    assert len(notices) == 1
    notice = (directory / "NEEDS-BEN.md").read_text(encoding="utf-8")
    committed = observe(
        remote, "show", f"{state['tip']}:{state['turns'][-1]['path']}", "--"
    ).decode("utf-8")
    assert reason in committed and reason in notice
    for path in (
        state["turns"][-1]["path"],
        turn_name(round_date, 1, "claude").removesuffix(".md") + "-update.md",
        f"doc/dual-agent-review-{round_date}-round.md",
    ):
        assert path in notice
    assert "Override:" in notice
    assert not (directory / "inflight.json").exists()
    dispatch.tick_round(
        home, round_date, config, worker=worker, toast=False, control=control
    )
    assert notices == {
        path: path.read_bytes() for path in directory.glob("notice-*.md")
    }

    # An independently authored override resumes the correct alternating turn.
    checkout = Path(state["checkouts"]["claude"])
    metadata = checkout / f"doc/dual-agent-review-{round_date}-round.md"
    metadata.write_text(
        metadata.read_text(encoding="utf-8").replace(
            "\n## Control", "\nOverride: next turn 02, codex\n\n## Control"
        ),
        encoding="utf-8",
        newline="\n",
    )
    observe(checkout, "add", "--", metadata.relative_to(checkout).as_posix())
    observe(checkout, "commit", "-m", "Disposable authorized override")
    observe(checkout, "push", "origin", f"HEAD:refs/heads/dar-{round_date}")
    closure_worker = successful_worker(
        home,
        round_date,
        {2: "Next: turn 03, claude; acknowledgment", 3: "Next: none; round closed"},
    )
    state = dispatch.tick_round(
        home, round_date, config, worker=closure_worker, toast=False, control=control
    )
    state = dispatch.tick_round(
        home, round_date, config, worker=closure_worker, toast=False, control=control
    )
    assert state["stop_reason"] == "round closed"
    entries = json.loads((control / "rounds.json").read_text(encoding="utf-8"))
    assert entries[0]["state"] == "inactive"
    assert (
        entries[0]["closed_tip"].encode("ascii")
        == observe(remote, "rev-parse", f"refs/heads/dar-{round_date}").strip()
    )
    assert list(directory.glob("deactivation-*.json"))
    assert len(list(directory.glob("notice-*.md"))) == 2

    active_date = "2026-10-01"
    start_local(inputs, active_date)
    calls = []
    original_tick = dispatch.tick_round

    def active_tick(repo, selected_date, configuration, **options):
        calls.append(selected_date)
        assert selected_date == active_date
        return original_tick(
            repo,
            selected_date,
            configuration,
            worker=successful_worker(home, active_date),
            toast=False,
            **options,
        )

    monkeypatch.setattr(dispatch, "CONTROL", control)
    monkeypatch.setattr(dispatch, "load_config", lambda path=None: config)
    monkeypatch.setattr(dispatch, "tick_round", active_tick)
    # A retained inactive registration with an unusable clone must be skipped.
    entries = json.loads((control / "rounds.json").read_text(encoding="utf-8"))
    entries[0]["repo"] = (tmp_path / "missing-home").as_posix()
    dispatch.write_json(control / "rounds.json", entries)
    assert dispatch.run_action(action_args("tick")) == 0
    assert calls == [active_date]
    assert protocol.status(home, active_date)["last_turn"] == 1
    assert observe(home, "rev-parse", "HEAD").decode("ascii").strip() == baseline
    assert (
        original_tick(
            tmp_path / "missing-home", round_date, config, toast=False, control=control
        )["stop_reason"]
        == "inactive"
    )
    entries[0]["state"] = "unknown"
    dispatch.write_json(control / "rounds.json", entries)
    with pytest.raises(protocol.ReviewError):
        dispatch.registry(control)


def test_git_failure_context_against_real_command_results(tmp_path, monkeypatch):
    home, remote, control, config, baseline = local_relay(tmp_path, monkeypatch)
    (home / "second.txt").write_text(
        "Second independent tree.\n", encoding="utf-8", newline="\n"
    )
    observe(home, "add", "--", "second.txt")
    observe(home, "commit", "-m", "Disposable descendant")
    descendant = observe(home, "rev-parse", "HEAD").decode("ascii").strip()
    for arguments in (
        ("merge-base", "--is-ancestor", descendant, baseline),
        ("rev-parse", "--verify", "missing-start^{commit}"),
        ("rev-parse", "--verify", "missing-end^{commit}"),
    ):
        oracle = subprocess.run(
            git_command(home, *arguments), capture_output=True, check=False
        )
        assert oracle.returncode
        with pytest.raises(protocol.ReviewError) as failure:
            protocol.git(home, *arguments)
        message = str(failure.value)
        assert str(oracle.returncode) in message
        assert all(argument in message for argument in arguments)
        for stream in (oracle.stdout, oracle.stderr):
            if stream.strip():
                assert stream.decode("utf-8").strip() in message
    with pytest.raises(protocol.ReviewError) as failure:
        dispatch.require_ancestor(home, descendant, baseline, "Start must precede End")
    assert descendant in str(failure.value) and baseline in str(failure.value)
