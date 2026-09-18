"""Operational retirement simulation against Git and filesystem oracles.

This module lives outside ``py/tests`` and is excluded from default
``py/main_test.py`` collection. Actual worktree retirement invokes it first.
Every destructive operation remains confined to pytest's temporary repositories,
and equivalent owner fixtures must leave the same Git and retained-data outcome.
"""

import gc
import hashlib
import json
import os
import sqlite3
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

import pytest

from repo_util import worktree_retirement as retirement
from repo_util import worktree_owners
from repo_util import git_worktree_cleanup
from repo_util import codex_worktree_retirement
from main_repo_util import build_parser, _validate_action_specific_args


@pytest.fixture
def tmp_path():
    # Sparse absolute-path shadows repeat the source prefix; keep fixture paths
    # short enough for Windows hosts where extended-length paths are disabled.
    with tempfile.TemporaryDirectory(prefix="mam-retirement-") as directory:
        try:
            yield Path(directory)
        finally:
            # sqlite3's read-only connection can participate in a reference
            # cycle after runtime inspection; collect it before Windows removes
            # the isolated database.
            gc.collect()


def git(repo, *args, check=True):
    """Independent oracle, with no dependency on retirement's Git wrappers."""
    return subprocess.run(
        ["git", "-c", f"safe.directory={repo.as_posix()}", "-C", str(repo), *args],
        check=check,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def tree_bytes(path):
    return {
        file.relative_to(path).as_posix(): file.read_bytes()
        for file in path.rglob("*")
        if file.is_file()
    }


def registration_paths(repo):
    return {
        field.removeprefix("worktree ")
        for field in git(repo, "worktree", "list", "--porcelain", "-z").stdout.split(
            "\0"
        )
        if field.startswith("worktree ")
    }


def branch_exists(repo, branch):
    return (
        git(
            repo, "show-ref", "--verify", "--quiet", f"refs/heads/{branch}", check=False
        ).returncode
        == 0
    )


@pytest.fixture
def isolated_runtime(tmp_path, monkeypatch):
    home = tmp_path / "h"
    home.mkdir()
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: home))
    monkeypatch.setenv("CODEX_HOME", str(home / ".codex"))
    monkeypatch.setenv("APPDATA", str(home / "appdata"))
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", os.devnull)
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")
    return home


def fixture_repo(tmp_path, home, owner, name="task", branch=None):
    primary = tmp_path / f"p-{owner[:2]}-{name}"
    primary.mkdir()
    git(primary, "init", "-b", "main")
    git(primary, "config", "user.name", "Retirement fixture")
    git(primary, "config", "user.email", "retirement@example.invalid")
    git(primary, "config", "core.autocrlf", "false")
    (primary / ".gitignore").write_text(
        ".novc/\n.ignored/\n.claude/\n__pycache__/\n", encoding="utf-8"
    )
    (primary / "tracked.txt").write_text("independent fixture\n", encoding="utf-8")
    git(primary, "add", ".")
    git(primary, "commit", "-m", "Create fixture")
    target = (
        primary / ".claude" / "worktrees" / name
        if owner == "claude"
        else home / ".codex" / "worktrees" / name / primary.name
    )
    branch = branch or f"{owner}/{name}"
    git(primary, "worktree", "add", "-b", branch, str(target), "main")
    return primary, target, branch


def prepare(tmp_path, target, name="preflight", **kwargs):
    path = tmp_path / f"{name}.json"
    plan = retirement.prepare_retirement(
        target,
        retirement_root=tmp_path / "retained",
        preflight_file=path,
        task_ended=True,
        citations_reviewed=True,
        citation_note="Reviewed fixture references; retained paths are in this preflight.",
        **kwargs,
    )
    return path, plan


def add_novc(target):
    source = target / ".novc"
    (source / "empty").mkdir(parents=True)
    (source / "nested").mkdir()
    (source / "evidence.bin").write_bytes(bytes(range(256)))
    (source / "nested" / "notes.txt").write_bytes(b"review evidence\n")
    return source


def assert_retained(plan, original):
    item = plan["destinations"][0]
    destination = Path(item["destination"])
    assert tree_bytes(destination) == original
    assert (destination / "empty").is_dir()
    metadata = json.loads(Path(item["sidecar"]).read_text(encoding="utf-8"))
    assert metadata["original_worktree_path"] == plan["snapshot"]["worktree_path"]
    assert metadata["owners"] == plan["snapshot"]["owners"]
    assert metadata["head"] == plan["snapshot"]["head"]
    assert metadata["branch"] == plan["snapshot"]["branch"]
    assert metadata["disposition"] == "retained"
    assert datetime.fromisoformat(metadata["retired_at"]).utcoffset() is not None
    assert metadata["file_count"] == len(original)
    assert metadata["total_bytes"] == sum(map(len, original.values()))
    oracle = {
        name: (len(data), hashlib.sha256(data).hexdigest())
        for name, data in original.items()
    }
    recorded = {
        entry["path"]: (entry["bytes"], entry["sha256"])
        for entry in metadata["verification"]["files"]
    }
    assert recorded == oracle
    return metadata


@pytest.mark.parametrize("cross_volume", [False, True])
def test_equivalent_owner_retirement_matches_oracles(
    tmp_path, isolated_runtime, monkeypatch, cross_volume
):
    monkeypatch.setattr(retirement, "_same_volume", lambda *_: not cross_volume)
    outcomes = []
    for owner in ("claude", "codex"):
        primary, target, branch = fixture_repo(tmp_path, isolated_runtime, owner)
        source = add_novc(target)
        original = tree_bytes(source)
        preflight, plan = prepare(tmp_path, target, owner)
        assert source.exists()  # Preparation does not relocate anything.
        result = retirement.execute_retirement(preflight, confirm_task_ended=True)
        assert target.as_posix() not in registration_paths(primary)
        assert not target.exists()
        assert not branch_exists(primary, branch)
        assert branch_exists(primary, "main")
        metadata = assert_retained(plan, original)
        assert metadata["branch_deleted"] and metadata["worktree_removed"]
        outcomes.append(
            (
                result["worktree_removed"],
                len(result["retained_novc"]),
                metadata["verification"],
            )
        )
    assert outcomes[0] == outcomes[1]


def claude_record(home, target, lease=False):
    if lease:
        register = home / "appdata" / "Claude" / "git-worktrees.json"
        register.parent.mkdir(parents=True, exist_ok=True)
        register.write_text(
            json.dumps(
                {
                    "worktrees": {
                        "fixture": {"path": str(target), "leasedBy": "fixture-session"}
                    }
                }
            ),
            encoding="utf-8",
        )
    else:
        sessions = home / ".claude" / "sessions"
        sessions.mkdir(parents=True, exist_ok=True)
        (sessions / "fixture.json").write_text(
            json.dumps({"cwd": str(target), "pid": 123}), encoding="utf-8"
        )


def codex_record(home, target, leased=True):
    root = home / ".codex"
    root.mkdir(exist_ok=True)
    with sqlite3.connect(root / "state_5.sqlite") as db:
        db.execute("CREATE TABLE IF NOT EXISTS threads (id TEXT PRIMARY KEY, cwd TEXT)")
        db.execute(
            "INSERT OR REPLACE INTO threads VALUES (?, ?)",
            ("fixture-task", str(target)),
        )
    if leased:
        locks = root / "thread-writer-locks"
        locks.mkdir(exist_ok=True)
        (locks / "fixture-task.lock").write_bytes(b"")


@pytest.mark.parametrize(
    "scenario",
    [
        "active",
        "claude_lease",
        "codex_lease",
        "locked",
        "current",
        "dirty",
        "untracked",
        "unmerged",
        "nonintegrated",
        "ignored",
        "reflog",
        "rewritten",
        "objects",
    ],
)
def test_equivalent_refusals_preserve_git_and_bytes(
    tmp_path, isolated_runtime, monkeypatch, scenario
):
    for owner in ("claude", "codex"):
        primary, target, branch = fixture_repo(tmp_path, isolated_runtime, owner)
        admin = Path(git(target, "rev-parse", "--absolute-git-dir").stdout.strip())
        if scenario == "active":
            claude_record(isolated_runtime, target)
        elif scenario == "claude_lease":
            claude_record(isolated_runtime, target, lease=True)
        elif scenario == "codex_lease":
            codex_record(isolated_runtime, target)
        elif scenario == "locked":
            git(primary, "worktree", "lock", str(target))
        elif scenario == "dirty":
            (target / "tracked.txt").write_text("changed\n", encoding="utf-8")
        elif scenario == "untracked":
            (target / "new.txt").write_text("untracked\n", encoding="utf-8")
        elif scenario == "unmerged":
            (admin / "rebase-merge").mkdir()
        elif scenario == "ignored":
            (target / ".ignored").mkdir()
            (target / ".ignored" / "unique").write_bytes(b"unique data")
        elif scenario == "objects":
            (admin / "objects").mkdir()
            (admin / "objects" / "recovery").write_bytes(b"recoverable")
        elif scenario in ("nonintegrated", "reflog", "rewritten"):
            (target / "tracked.txt").write_text("unmerged work\n", encoding="utf-8")
            git(target, "commit", "-am", "Unmerged fixture work")
            tip = git(target, "rev-parse", "HEAD").stdout.strip()
            if scenario != "nonintegrated":
                git(target, "reset", "--hard", "main")
            if scenario == "rewritten":
                git(target, "update-ref", "refs/rewritten/fixture", tip)
        before = tree_bytes(target)
        with monkeypatch.context() as context:
            if scenario == "current":
                context.chdir(target)
            with pytest.raises(retirement.RetirementError):
                prepare(tmp_path, target, owner)
        assert tree_bytes(target) == before
        assert target.as_posix() in registration_paths(primary)
        assert branch_exists(primary, branch)


def test_selection_and_branch_deletion_stay_in_scope(tmp_path, isolated_runtime):
    primary, claude, claude_branch = fixture_repo(tmp_path, isolated_runtime, "claude")
    codex = isolated_runtime / ".codex" / "worktrees" / "mixed" / "repo"
    unknown = tmp_path / "topic"
    for target, branch in ((codex, "codex/mixed"), (unknown, "topic")):
        git(primary, "worktree", "add", "-b", branch, str(target), "main")
    git(primary, "branch", "claude/orphan")
    git(primary, "branch", "codex/orphan")
    expected = {"claude": {claude}, "codex": {codex}, "both": {claude, codex}}
    for owner, paths in expected.items():
        assert {
            r.path for r in retirement.select_worktrees(primary, owner=owner)
        } == paths
    assert {r.path for r in retirement.select_worktrees(primary, exact=unknown)} == {
        unknown
    }
    with pytest.raises(retirement.RetirementError):
        prepare(tmp_path, claude, "wrong", owner_selector="codex")
    before = registration_paths(primary)
    git_worktree_cleanup.clean_worktrees(primary)
    assert registration_paths(primary) == before
    for target in (claude, unknown, codex):
        path, _ = prepare(tmp_path, target, target.name)
        retirement.execute_retirement(path, confirm_task_ended=True)
        if target == claude:
            assert branch_exists(primary, "codex/mixed")
            assert codex.as_posix() in registration_paths(primary)
    assert not branch_exists(primary, claude_branch)
    assert not branch_exists(primary, "codex/mixed")
    for branch in ("main", "topic", "claude/orphan", "codex/orphan"):
        assert branch_exists(primary, branch)
    with pytest.raises(retirement.RetirementError):
        prepare(tmp_path, primary, "primary")


def test_generic_policy_does_not_gate_and_task_provenance(tmp_path, isolated_runtime):
    for owner in ("claude", "codex"):
        primary, target, _ = fixture_repo(tmp_path, isolated_runtime, owner)
        codex_record(isolated_runtime, target, leased=False)
        path = tmp_path / f"unreviewed-{owner}.json"
        plan = retirement.prepare_retirement(
            target,
            retirement_root=tmp_path / "retained",
            preflight_file=path,
            task_ended=True,
        )
        assert plan["snapshot"]["tracked_novc_citations"] == []
        assert plan["ready_for_execution"]
        assert plan["codex_task_ids"] == ["fixture-task"]
        assert target.as_posix() in registration_paths(primary)


@pytest.mark.parametrize(
    "drift", ["dirty", "novc", "ignored", "branch", "lease", "plan", "collision"]
)
def test_execution_refuses_drift_before_mutation(tmp_path, isolated_runtime, drift):
    for owner in ("claude", "codex"):
        primary, target, branch = fixture_repo(tmp_path, isolated_runtime, owner)
        source = add_novc(target)
        path, plan = prepare(tmp_path, target, owner)
        if drift == "dirty":
            (target / "tracked.txt").write_bytes(b"changed")
        elif drift == "novc":
            (source / "added").write_bytes(b"late evidence")
        elif drift == "ignored":
            (target / ".ignored").mkdir()
            (target / ".ignored" / "added").write_bytes(b"late evidence")
        elif drift == "branch":
            git(target, "switch", "-c", f"{owner}/new")
        elif drift == "lease":
            claude_record(isolated_runtime, target, lease=True)
        elif drift == "plan":
            plan["citation_note"] = "changed after preparation"
            path.write_text(json.dumps(plan), encoding="utf-8")
        elif drift == "collision":
            destination = Path(plan["destinations"][0]["destination"])
            destination.mkdir(parents=True)
            (destination / "existing").write_bytes(b"never overwrite")
        before = tree_bytes(target)
        with pytest.raises(retirement.RetirementError):
            retirement.execute_retirement(path, confirm_task_ended=True)
        assert tree_bytes(target) == before
        assert target.as_posix() in registration_paths(primary)
        assert branch_exists(primary, branch)


@pytest.mark.parametrize("with_novc", [False, True])
@pytest.mark.parametrize("unregistered", [False, True])
def test_partial_removal_resumes_conservatively(
    tmp_path, isolated_runtime, monkeypatch, with_novc, unregistered
):
    for owner in ("claude", "codex"):
        primary, target, branch = fixture_repo(tmp_path, isolated_runtime, owner)
        original = tree_bytes(add_novc(target)) if with_novc else None
        path, plan = prepare(tmp_path, target, owner)
        original_git = retirement._git
        removal_calls = []

        def partial(repo, *args, **kwargs):
            if args[:2] == ("worktree", "remove"):
                removal_calls.append(args)
                if unregistered:
                    original_git(repo, *args, **kwargs)
                    target.mkdir()
                    (target / "acl-residue").write_bytes(b"left by Windows")
                return subprocess.CompletedProcess(
                    args, 1, "", "simulated Windows removal failure"
                )
            return original_git(repo, *args, **kwargs)

        with monkeypatch.context() as context:
            context.setattr(retirement, "_git", partial)
            if unregistered:
                result = retirement.execute_retirement(path, confirm_task_ended=True)
                assert result["residue"]["total_bytes_readable"] == len(
                    b"left by Windows"
                )
                assert not result["worktree_removed"]
            else:
                with pytest.raises(retirement.RetirementError):
                    retirement.execute_retirement(path, confirm_task_ended=True)
        assert len(removal_calls) == 1
        if unregistered:
            claude_record(isolated_runtime, target)
            with pytest.raises(retirement.RetirementError):
                retirement.execute_retirement(path, confirm_task_ended=True)
            (isolated_runtime / ".claude" / "sessions" / "fixture.json").unlink()
        result = retirement.execute_retirement(path, confirm_task_ended=True)
        assert target.as_posix() not in registration_paths(primary)
        assert not branch_exists(primary, branch)
        assert result["worktree_removed"] == (not unregistered)
        if original is not None:
            assert_retained(plan, original)


def test_destination_allocator_and_aliases(tmp_path, isolated_runtime, monkeypatch):
    primary, target, _ = fixture_repo(tmp_path, isolated_runtime, "codex")
    source = add_novc(target)
    root = tmp_path / "retained"
    identifiers = iter(("collision", "unique"))
    parent = root.joinpath(*retirement._shadow_parts(source.parent))
    parent.mkdir(parents=True)
    sentinel = parent / ".novc--collision.json"
    sentinel.write_bytes(b"already retained")
    monkeypatch.setattr(retirement, "_retirement_id", lambda: next(identifiers))
    path = tmp_path / "alias.json"
    plan = codex_worktree_retirement.prepare_retirement(
        target,
        retirement_root=root,
        preflight_file=path,
        task_ended=True,
        citations_reviewed=True,
        citation_note="Fixture review",
    )
    assert plan["retirement_id"] == "unique"
    assert sentinel.read_bytes() == b"already retained"
    codex_worktree_retirement.execute_retirement(path, confirm_task_ended=True)
    parser = build_parser()
    for owner in worktree_owners.SELECTORS:
        args = parser.parse_args(["--inspect-worktrees", "--worktree-owner", owner])
        _validate_action_specific_args(parser, args)
    args = parser.parse_args(["--inspect-worktrees", "--worktree", str(target)])
    _validate_action_specific_args(parser, args)
    assert target.as_posix() not in registration_paths(primary)


def test_branch_reflog_history_preceding_checkout_is_protected(
    tmp_path, isolated_runtime
):
    for owner in ("claude", "codex"):
        primary, target, _ = fixture_repo(tmp_path, isolated_runtime, owner)
        # A second branch predates the checkout that eventually uses it.
        branch = f"{owner}/older"
        git(primary, "switch", "-c", branch)
        (primary / "history.txt").write_bytes(b"recoverable branch-only history")
        git(primary, "add", ".")
        git(primary, "commit", "-m", "Recoverable fixture history")
        recovery_tip = git(primary, "rev-parse", "HEAD").stdout.strip()
        git(primary, "reset", "--hard", "main")
        git(primary, "switch", "main")
        older = target.parent / "older"
        git(primary, "worktree", "add", str(older), branch)
        with pytest.raises(retirement.RetirementError):
            prepare(tmp_path, older, f"blocked-{owner}")
        git(primary, "tag", "recovery", recovery_tip)
        path, _ = prepare(tmp_path, older, owner)
        retirement.execute_retirement(path, confirm_task_ended=True)
        assert git(primary, "rev-parse", "recovery").stdout.strip() == recovery_tip
        assert not branch_exists(primary, branch)


def test_exact_relocation_citations_gate_and_survive_retirement(
    tmp_path, isolated_runtime
):
    for owner in ("claude", "codex"):
        primary, target, _ = fixture_repo(tmp_path, isolated_runtime, owner)
        source = add_novc(target)
        original = tree_bytes(source)
        absolute_citation = str(source / "evidence.bin")
        relative_citation = ".novc/evidence.bin"
        noncitation = str(target / ".novc-old" / "evidence.bin")
        (primary / "policy.md").write_text(
            "A generic `.novc` policy is not an artifact reference.\n"
            f"This similarly named path is not the target: {noncitation}\n",
            encoding="utf-8",
        )
        git(primary, "add", "policy.md")
        git(primary, "commit", "-m", "Add generic fixture policy")
        observer = tmp_path / f"observer-{owner}"
        git(
            primary,
            "worktree",
            "add",
            "-b",
            f"observer/{owner}",
            str(observer),
            "main",
        )

        generic_plan = retirement.prepare_retirement(
            target,
            retirement_root=tmp_path / "retained",
            preflight_file=tmp_path / f"generic-{owner}.json",
            task_ended=True,
        )
        assert generic_plan["ready_for_execution"]
        assert generic_plan["snapshot"]["tracked_novc_citations"] == []

        (primary / "receipt.md").write_text(
            f"absolute twice: {absolute_citation} and {absolute_citation}\n"
            f"relative: {relative_citation}\n",
            encoding="utf-8",
        )
        git(primary, "add", "receipt.md")
        git(primary, "commit", "-m", "Record exact fixture citations")
        git(observer, "merge", "main")

        unreviewed_path = tmp_path / f"unreviewed-exact-{owner}.json"
        unreviewed = retirement.prepare_retirement(
            target,
            retirement_root=tmp_path / "retained",
            preflight_file=unreviewed_path,
            task_ended=True,
        )
        citations = unreviewed["snapshot"]["tracked_novc_citations"]
        assert not unreviewed["ready_for_execution"]
        assert {item["checkout"] for item in citations} == {
            str(primary),
            str(observer),
        }
        assert {item["reference_kind"] for item in citations} == {
            "absolute",
            "relative",
        }
        assert len(citations) == 4
        assert all(item["path"] == "receipt.md" for item in citations)
        assert all(item["matched_source"] == str(source) for item in citations)
        assert all(item["tracked_file_sha256"] for item in citations)
        assert all(".novc-old" not in item["text"] for item in citations)
        assert unreviewed["citation_review"]["citations"] == citations
        assert unreviewed["citation_review"]["note"] is None
        with pytest.raises(retirement.RetirementError):
            retirement.execute_retirement(unreviewed_path, confirm_task_ended=True)

        reviewed_path, reviewed = prepare(tmp_path, target, f"reviewed-{owner}")
        review_payload = {
            key: value
            for key, value in reviewed["citation_review"].items()
            if key != "fingerprint"
        }
        assert reviewed["citation_review"]["citations"] == citations
        assert reviewed["citation_review"]["reviewed"]
        assert reviewed["citation_review"]["note"] == (
            "Reviewed fixture references; retained paths are in this preflight."
        )
        assert reviewed["citation_review"]["fingerprint"] == retirement._fingerprint(
            review_payload
        )
        retirement.execute_retirement(reviewed_path, confirm_task_ended=True)
        metadata = assert_retained(reviewed, original)
        assert metadata["citation_review"] == reviewed["citation_review"]
        assert observer.as_posix() in registration_paths(primary)


def test_cached_remote_reporting_matches_selected_ref_oracle(
    tmp_path, isolated_runtime
):
    primary, _, _ = fixture_repo(tmp_path, isolated_runtime, "claude")
    head = git(primary, "rev-parse", "HEAD").stdout.strip()
    tree = git(primary, "rev-parse", "HEAD^{tree}").stdout.strip()
    tip = git(
        primary, "commit-tree", tree, "-p", head, "-m", "Remote fixture work"
    ).stdout.strip()
    refs = {
        f"{prefix}remote"
        for prefixes in worktree_owners.BRANCH_PREFIXES.values()
        for prefix in prefixes
    }
    for branch in refs:
        git(primary, "update-ref", f"refs/remotes/origin/{branch}", tip)
    before = registration_paths(primary)
    for owner in worktree_owners.SELECTORS:
        report = git_worktree_cleanup.clean_worktrees(primary, owner=owner)
        prefixes = tuple(
            prefix
            for key, values in worktree_owners.BRANCH_PREFIXES.items()
            if owner == "both" or key == owner
            for prefix in values
        )
        assert set(report.stranded_branches) == {
            ref for ref in refs if ref.startswith(prefixes)
        }
    assert registration_paths(primary) == before


def test_resume_preserves_new_branch_reflog_history(
    tmp_path, isolated_runtime, monkeypatch
):
    for owner in ("claude", "codex"):
        primary, target, branch = fixture_repo(tmp_path, isolated_runtime, owner)
        path, plan = prepare(tmp_path, target, owner)
        original_git = retirement._git

        def fail_branch_delete(repo, *args, **kwargs):
            if args[:2] == ("branch", "-d"):
                return subprocess.CompletedProcess(
                    args, 1, "", "simulated branch failure"
                )
            return original_git(repo, *args, **kwargs)

        with monkeypatch.context() as context:
            context.setattr(retirement, "_git", fail_branch_delete)
            with pytest.raises(retirement.RetirementError):
                retirement.execute_retirement(path, confirm_task_ended=True)
        assert target.as_posix() not in registration_paths(primary)
        tree = git(primary, "rev-parse", "HEAD^{tree}").stdout.strip()
        tip = git(
            primary, "commit-tree", tree, "-p", "HEAD", "-m", "Later recovery work"
        ).stdout.strip()
        git(primary, "update-ref", f"refs/heads/{branch}", tip)
        git(primary, "update-ref", f"refs/heads/{branch}", plan["snapshot"]["head"])
        with pytest.raises(retirement.RetirementError):
            retirement.execute_retirement(path, confirm_task_ended=True)
        assert branch_exists(primary, branch)
        git(primary, "tag", "later-recovery", tip)
        retirement.execute_retirement(path, confirm_task_ended=True)
        assert not branch_exists(primary, branch)
        assert git(primary, "rev-parse", "later-recovery").stdout.strip() == tip


def test_cross_volume_source_drift_preserves_late_bytes(
    tmp_path, isolated_runtime, monkeypatch
):
    for owner in ("claude", "codex"):
        primary, target, branch = fixture_repo(tmp_path, isolated_runtime, owner)
        source = add_novc(target)
        path, plan = prepare(tmp_path, target, owner)
        copytree = retirement.shutil.copytree

        def copy_then_change(*args, **kwargs):
            result = copytree(*args, **kwargs)
            (source / "late").write_bytes(b"must survive")
            return result

        with monkeypatch.context() as context:
            context.setattr(retirement, "_same_volume", lambda *_: False)
            context.setattr(retirement.shutil, "copytree", copy_then_change)
            with pytest.raises(retirement.RetirementError):
                retirement.execute_retirement(path, confirm_task_ended=True)
        assert (source / "late").read_bytes() == b"must survive"
        assert target.as_posix() in registration_paths(primary)
        assert branch_exists(primary, branch)
        sidecar = Path(plan["destinations"][0]["sidecar"])
        assert (
            json.loads(sidecar.read_text(encoding="utf-8"))["disposition"]
            == "relocation_failed"
        )
