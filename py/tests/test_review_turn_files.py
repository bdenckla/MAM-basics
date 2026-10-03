"""Lint the numbered turn files of every dual-agent review round since 2026-09-16.

D9 and D10 in doc/dual-agent-review.md give a round's turn files their numbering, their
alternation between the two agents and their line-3 State shapes. This lint checks those
three properties over the tracked tree, manual and automated rounds alike. It took over
test_turn_census_and_sequences from the relay's own test module when the relay was
retired, without that module's comparison against the relay's census.
"""

from collections import defaultdict
import re
import subprocess

from mb_cmn import paths
from mb_cmn.git_process import git_command

_TURN_FILE = re.compile(
    r"^doc/dual-agent-review-([0-9]{4}-[0-9]{2}-[0-9]{2})-turn-([0-9]{2})-(claude|codex)[.]md$"
)
_OTHER_AGENT = {"claude": "codex", "codex": "claude"}


def test_turn_numbering_alternation_and_state_lines():
    root = paths.repo_root()
    raw = subprocess.run(
        git_command(root, "ls-files", "-z"), capture_output=True, check=True
    ).stdout
    filenames = [part.decode("utf-8") for part in raw.split(b"\0") if part]
    turns = []
    for name in filenames:
        match = _TURN_FILE.fullmatch(name)
        if match:
            turns.append((match[1], int(match[2]), match[3], name))
    assert turns, "tracked review-turn inputs are missing"
    rounds = defaultdict(list)
    for entry in turns:
        if entry[0] >= "2026-09-16":
            rounds[entry[0]].append(entry)
    assert rounds, "contiguous-round lint has no input"
    for entries in rounds.values():
        entries.sort()
        assert [entry[1] for entry in entries] == list(range(1, len(entries) + 1))
        agent1 = entries[0][2]
        for _, number, agent, filename in entries:
            assert agent == (agent1 if number % 2 else _OTHER_AGENT[agent1]), filename
            lines = (root / filename).read_text(encoding="utf-8").splitlines()
            assert lines[2].startswith("State: "), filename
            if number > 1:
                assert re.fullmatch(
                    r"State: completed \d{4}-\d{2}-\d{2}; review only", lines[2]
                ), filename
