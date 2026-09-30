"""Read the explicit automated-review protocol without adopting manual rounds."""

from __future__ import annotations

from datetime import date, datetime
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import subprocess

from mb_cmn.git_process import git_command
from mb_cmn.new_york_time import NEW_YORK, labelled
from repo_util.worktree_owners import runtime_facts

AGENTS = ("claude", "codex")
TURN_PATH = re.compile(
    r"doc/dual-agent-review-(\d{4}-\d{2}-\d{2})-turn-(\d{2})-(claude|codex)\.md"
)
ROUND_PATH = re.compile(r"doc/dual-agent-review-(\d{4}-\d{2}-\d{2})-round\.md")
NEXT = re.compile(
    r"Next: (?:(?:turn (\d{2}), (claude|codex)(?:; (acknowledgment|objection))?)"
    r"|(?:none; round closed)|(?:Ben; (\S.*)))"
)


class ReviewError(RuntimeError):
    """Protocol or operational preconditions refused the action."""


def git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    environment = os.environ.copy()
    environment.update(GIT_TERMINAL_PROMPT="0", GCM_INTERACTIVE="Never")
    result = subprocess.run(
        git_command(repo, *args), capture_output=True, env=environment, timeout=60
    )
    if check and result.returncode:
        raise ReviewError(result.stderr.decode("utf-8", errors="replace").strip())
    return result


def git_text(repo: Path, *args: str) -> str:
    return git(repo, *args).stdout.decode("utf-8").strip()


def validate_date(value: str) -> str:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ReviewError("round must be a YYYY-MM-DD date")
    date.fromisoformat(value)
    return value


def round_path(round_date: str) -> str:
    return f"doc/dual-agent-review-{validate_date(round_date)}-round.md"


def turn_path(round_date: str, number: int, agent: str) -> str:
    if agent not in AGENTS or not 1 <= number <= 99:
        raise ReviewError("invalid turn owner or number")
    return (
        f"doc/dual-agent-review-{validate_date(round_date)}-turn-{number:02}-{agent}.md"
    )


def census(filenames) -> list[tuple[str, int, str, str]]:
    return sorted(
        (match[1], int(match[2]), match[3], filename)
        for filename in filenames
        if (match := TURN_PATH.fullmatch(filename))
    )


def tree_files(repo: Path, ref: str) -> list[str]:
    return [
        name.decode("utf-8")
        for name in git(repo, "ls-tree", "-r", "--name-only", "-z", ref).stdout.split(
            b"\0"
        )
        if name
    ]


def header(text: str) -> list[str]:
    lines = text.splitlines()
    boundary = next(
        (i for i, line in enumerate(lines) if line.startswith("## ")), len(lines)
    )
    return lines[:boundary]


def field(lines: list[str], name: str) -> str:
    found = [line[len(name) + 2 :] for line in lines if line.startswith(name + ": ")]
    if len(found) != 1:
        raise ReviewError(f"expected exactly one {name}: header line")
    return found[0]


def parse_next(text: str) -> dict:
    lines = text.splitlines()
    markers = [line for line in lines if line.startswith("Next:")]
    if len(markers) != 1 or markers[0] not in header(text):
        raise ReviewError("expected exactly one Next: line in the header")
    if header(text).index(markers[0]) <= 2:
        raise ReviewError("Next: must follow the line-3 State:")
    match = NEXT.fullmatch(markers[0])
    if not match:
        raise ReviewError("invalid Next: line")
    if match[1]:
        return {
            "kind": "turn",
            "turn": int(match[1]),
            "agent": match[2],
            "flag": match[3],
        }
    if match[4]:
        return {"kind": "Ben", "reason": match[4]}
    return {"kind": "closed"}


def parse_round(
    text: str, repo: Path, round_date: str, *, bind_checkout: bool = True
) -> dict:
    lines = header(text)
    if field(lines, "Protocol") != "1" or field(lines, "State") != "live":
        raise ReviewError("unsupported round protocol or State")
    agent1 = field(lines, "Agent 1")
    if agent1 not in AGENTS:
        raise ReviewError("invalid Agent 1")
    values = {"agent1": agent1}
    for label, key in (("Start", "start"), ("End", "end")):
        value = field(lines, label)
        if not re.fullmatch(r"[a-f0-9]{40}", value):
            raise ReviewError(f"invalid {label} commit")
        values[key] = value
    for label, key, minimum in (
        ("Turn cap", "turn_cap", 3),
        ("Reopening cap", "reopening_cap", 0),
    ):
        value = field(lines, label)
        if not re.fullmatch(r"\d+", value) or not minimum <= int(value) <= 99:
            raise ReviewError(f"invalid {label}")
        values[key] = int(value)
    values["instruction"] = json.loads(field(lines, "Kickoff instruction"))
    if not isinstance(values["instruction"], str) or not values["instruction"].strip():
        raise ReviewError("kickoff instruction is empty")
    values["models"] = {}
    values["checkouts"] = {}
    for agent in AGENTS:
        model = field(lines, agent.capitalize() + " model")
        if not re.fullmatch(r"[A-Za-z0-9._-]+", model):
            raise ReviewError("invalid pinned model")
        values["models"][agent] = model
        expected = (repo / ".claude/worktrees" / f"dar-{round_date}-{agent}").resolve()
        path_text = json.loads(field(lines, agent.capitalize() + " checkout"))
        recorded = (
            PureWindowsPath(path_text)
            if PureWindowsPath(path_text).is_absolute()
            else PurePosixPath(path_text)
        )
        if not recorded.is_absolute() or recorded.parts[-3:] != (
            ".claude",
            "worktrees",
            f"dar-{round_date}-{agent}",
        ):
            raise ReviewError("invalid absolute round checkout pattern")
        configured = Path(path_text).resolve()
        if bind_checkout and configured != expected:
            raise ReviewError(
                "round checkout differs from the task-owned checkout pattern"
            )
        values["checkouts"][agent] = (
            configured.as_posix() if bind_checkout else recorded.as_posix()
        )
    if (
        field(lines, "Claude effort") != "max"
        or field(lines, "Codex effort") != "xhigh"
    ):
        raise ReviewError("round efforts must be max and xhigh")
    values["facts_only"] = field(lines, "Facts only from turn 03") == "yes"
    values["rehearsal"] = field(lines, "Rehearsal") == "yes"
    if field(lines, "Rehearsal") not in ("yes", "no"):
        raise ReviewError("invalid rehearsal flag")
    if field(lines, "Facts only from turn 03") not in ("yes", "no"):
        raise ReviewError("invalid facts-only rule")
    overrides = [line for line in lines if line.startswith("Override:")]
    values["override"] = None
    if overrides:
        if len(overrides) != 1:
            raise ReviewError("duplicate Override:")
        match = re.fullmatch(
            r"Override: next turn (\d{2}), (claude|codex)", overrides[0]
        )
        if not match:
            raise ReviewError("invalid Override:")
        values["override"] = {
            "kind": "turn",
            "turn": int(match[1]),
            "agent": match[2],
            "flag": None,
        }
    return values


def validate_turn(
    text: str, number: int, agent: str, agent1: str, previous: dict | None
) -> dict:
    expected_agent = agent1 if number % 2 else other(agent1)
    if agent != expected_agent:
        raise ReviewError("turn filename disagrees with Agent 1 parity")
    lines = text.splitlines()
    if len(lines) < 4 or not lines[0].startswith("# ") or lines[1] != "":
        raise ReviewError("turn needs an H1, blank line, and line-3 State:")
    state = lines[2]
    if number > 1:
        if not re.fullmatch(r"State: completed \d{4}-\d{2}-\d{2}; review only", state):
            raise ReviewError("later turn has invalid D10 State:")
    elif not state.startswith("State: not yet acted on"):
        raise ReviewError("turn 01 must record not yet acted on")
    next_step = parse_next(text)
    acknowledged = previous is not None and previous.get("flag") == "acknowledgment"
    if next_step["kind"] == "closed" and not acknowledged:
        raise ReviewError("only an owed acknowledgment may close the round")
    if next_step["kind"] == "turn":
        if next_step["turn"] != number + 1 or next_step["agent"] != other(agent):
            raise ReviewError("Next: must name the next number and the other agent")
        if next_step["flag"] == "objection" and not acknowledged:
            raise ReviewError("objection must answer an owed acknowledgment")
        if acknowledged and next_step["flag"] != "objection":
            raise ReviewError("acknowledgment must close, object, or ask Ben")
    return next_step


def other(agent: str) -> str:
    if agent not in AGENTS:
        raise ReviewError("unknown agent")
    return "codex" if agent == "claude" else "claude"


def status(repo: Path, round_date: str, *, occupancy: bool = True) -> dict:
    repo = repo.resolve()
    validate_date(round_date)
    ref = f"refs/remotes/origin/dar-{round_date}"
    result = {
        "repo": repo.as_posix(),
        "round": round_date,
        "tip": None,
        "turns": [],
        "last_turn": 0,
        "last_agent": None,
        "agent1": None,
        "next": None,
        "reopenings": 0,
        "dispatchable": False,
        "stop_reason": None,
        "inflight": None,
        "checkouts": {},
        "problems": [],
        "observed_at": datetime.now(NEW_YORK).isoformat(),
        "observed_at_labelled": labelled(datetime.now(NEW_YORK).isoformat()),
    }
    try:
        probe = git(repo, "rev-parse", "--verify", ref, check=False)
        if probe.returncode:
            result["stop_reason"] = "no remote round"
            return result
        tip = probe.stdout.decode("ascii").strip()
        result["tip"] = tip
        files = tree_files(repo, tip)
        metadata = round_path(round_date)
        if metadata not in files:
            result["stop_reason"] = "manual round; no automated protocol"
            return result
        specification = parse_round(
            git(repo, "show", f"{tip}:{metadata}").stdout.decode("utf-8"),
            repo,
            round_date,
        )
        result.update(specification)
        turns = [item for item in census(files) if item[0] == round_date]
        previous = None
        for expected, (_, number, agent, filename) in enumerate(turns, 1):
            if number != expected:
                raise ReviewError("turn sequence is not contiguous from 01")
            if previous and previous["kind"] != "turn":
                creation = git_text(
                    repo,
                    "log",
                    "-1",
                    "--diff-filter=A",
                    "--format=%H",
                    tip,
                    "--",
                    filename,
                )
                historical = parse_round(
                    git(repo, "show", f"{creation}:{metadata}").stdout.decode("utf-8"),
                    repo,
                    round_date,
                )
                override = historical["override"]
                if (
                    not override
                    or override["turn"] != number
                    or override["agent"] != agent
                ):
                    raise ReviewError(
                        "turn follows a stop without an explicit Override:"
                    )
            text = git(repo, "show", f"{tip}:{filename}").stdout.decode("utf-8")
            previous = validate_turn(
                text, number, agent, specification["agent1"], previous
            )
            result["reopenings"] += previous.get("flag") == "objection"
            result["turns"].append(
                {"turn": number, "agent": agent, "path": filename, "next": previous}
            )
        result["last_turn"] = len(turns)
        result["last_agent"] = turns[-1][2] if turns else None
        next_step = previous or {
            "kind": "turn",
            "turn": 1,
            "agent": specification["agent1"],
            "flag": None,
        }
        override = specification["override"]
        if override and override["turn"] > len(turns):
            if override["turn"] != len(turns) + 1 or override["agent"] != (
                specification["agent1"]
                if override["turn"] % 2
                else other(specification["agent1"])
            ):
                raise ReviewError("Override: must name the next alternating turn")
            next_step = override
        result["next"] = next_step
        if next_step["kind"] != "turn":
            result["stop_reason"] = (
                "round closed"
                if next_step["kind"] == "closed"
                else "Ben's decision required"
            )
        elif next_step["turn"] > specification["turn_cap"]:
            result["stop_reason"] = "turn cap reached"
        elif result["reopenings"] > specification["reopening_cap"]:
            result["stop_reason"] = "reopening cap exceeded"
        else:
            result["dispatchable"] = True
        if occupancy:
            result["occupancy"] = {
                agent: runtime_facts(Path(path))
                for agent, path in specification["checkouts"].items()
            }
    except (ReviewError, OSError, ValueError, KeyError, TypeError) as exc:
        result["problems"].append(str(exc))
        result["dispatchable"] = False
        result["stop_reason"] = "invalid protocol"
    return result
