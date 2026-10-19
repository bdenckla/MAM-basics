"""Differential citation-output checks, with no retirement preparation or execution."""

import hashlib
import ntpath
import posixpath
import subprocess
from types import SimpleNamespace

import pytest

from repo_util import worktree_retirement_inspection as inspection


@pytest.mark.parametrize("normcase", [posixpath.normcase, ntpath.normcase])
@pytest.mark.parametrize("reference_set", ["empty", "novc", "mixed", "plain", "upper"])
def test_citation_output_matches_explicit_line_oracle(
    tmp_path, monkeypatch, normcase, reference_set
):
    def normalize(text):
        return normcase(text).replace(chr(92), "/")

    # Spellings reproduce POSIX, Windows and file-URL references. Case folding is
    # selected explicitly, so Windows matching is exercised on POSIX runners too.
    spellings = [
        (".novc/artifact.txt", "relative", False),
        (".novc/folder", "relative", True),
        ("C:/cache/.novc/artifact.txt", "absolute", False),
        ("/tmp/cache/.novc/artifact.txt", "absolute", False),
        ("file:///C:/cache/.novc/artifact.txt", "file-url", False),
        ("retained/plain.txt", "checkout-relative", False),
        (".NOVC/upper.txt", "relative", False),
    ]
    indexes = {
        "empty": [],
        "novc": [0, 1, 2, 3, 4],
        "mixed": [0, 1, 2, 3, 4, 5],
        "plain": [5],
        "upper": [6],
    }[reference_set]
    references = [
        {
            "source": f"source-{index}",
            "reference": normalize(spellings[index][0]),
            "kind": spellings[index][1],
            "directory": spellings[index][2],
        }
        for index in indexes
    ]
    # Duplicate spellings for one source must not duplicate a citation or change
    # which reference is recorded. Two distinct sources on one line remain two hits.
    if 0 in indexes:
        references.append({**references[0], "kind": "duplicate"})

    lines = []
    expected_hits = []

    def add(text, *matches):
        lines.append(text)
        expected_hits.extend(
            (len(lines), index) for index in matches if index in indexes
        )

    add("")
    add("ordinary source line")
    add("generic .novc policy; .novc/absent.txt")
    for index, (spelling, _, directory) in enumerate(spellings):
        add(f"`{spelling}`", index)
        add(f"[{spelling.replace('/', chr(92))}]", index)
        if normcase is ntpath.normcase or spelling.upper() == spelling:
            add(f"<{spelling.upper()}>", index)
        else:
            add(f"<{spelling.upper()}>")
        add(f"({spelling}).!?:", index)
        if directory:
            add(f"`{spelling}/`", index)
            add(f"`{spelling}/child.txt`")
        else:
            for locator in (":3", ":3-5", ":3\N{EN DASH}5", "#L3", "#l3", ":3:"):
                add(f"`{spelling}{locator}`", index)
            add(f"`{spelling}:3bad`")
            add(f"`{spelling}#L3bad`")
        add(f"prefix{spelling}")
        add(f"other/{spelling}")
        add(f"{spelling}.bak")
        add(f"{spelling}-other")
    add(".novc/artifact.txt retained/plain.txt", 0, 5)
    add("x" * 510 + " `.novc/artifact.txt`", 0)
    add("`.novc/artifact.txt` then `.novc/artifact.txt`", 0)

    content = ("\n".join(lines) + "\n").encode("utf-8")
    filenames = ["z citation.md", "a\ttab.md"]
    for filename in filenames:
        (tmp_path / filename).write_bytes(content)

    def fake_git(*args, **kwargs):
        assert references, "empty reference sets must not invoke Git"
        assert args[1:] == ("grep", "-l", "-z", "-I", "-i", "-e", ".novc", "--")
        assert kwargs == {"text": False}
        return subprocess.CompletedProcess(
            args, 0, b"\0".join(name.encode() for name in filenames) + b"\0", b""
        )

    monkeypatch.setattr(inspection, "_git", fake_git)
    monkeypatch.setattr(inspection, "_citation_references", lambda *_: references)
    monkeypatch.setattr(
        inspection, "os", SimpleNamespace(path=SimpleNamespace(normcase=normcase))
    )
    actual = inspection._tracked_relocation_citations(tmp_path, tmp_path, tmp_path, [])
    expected = [
        {
            "path": filename,
            "line": line_number,
            "text": lines[line_number - 1][:500],
            "matched_source": f"source-{index}",
            "matched_reference": normalize(spellings[index][0]),
            "reference_kind": spellings[index][1],
            "tracked_file_bytes": len(content),
            "tracked_file_sha256": hashlib.sha256(content).hexdigest(),
        }
        for filename in sorted(filenames)
        for line_number, index in sorted(expected_hits)
    ]
    assert actual == expected


@pytest.mark.parametrize("normcase", [posixpath.normcase, ntpath.normcase])
def test_prefilter_keeps_unreadable_citation_failure(tmp_path, monkeypatch, normcase):
    """A filtered-out line cannot suppress an unreadable tracked-file blocker."""
    (tmp_path / "bad.md").write_bytes(b".novc/artifact.txt\n\xff")
    monkeypatch.setattr(
        inspection,
        "_citation_references",
        lambda *_: [{"reference": ".novc/artifact.txt"}],
    )
    monkeypatch.setattr(
        inspection,
        "_git",
        lambda *args, **_: subprocess.CompletedProcess(args, 0, b"bad.md\0", b""),
    )
    monkeypatch.setattr(
        inspection, "os", SimpleNamespace(path=SimpleNamespace(normcase=normcase))
    )
    with pytest.raises(
        inspection.RetirementError, match="cannot review tracked citation"
    ):
        inspection._tracked_relocation_citations(tmp_path, tmp_path, tmp_path, [])
