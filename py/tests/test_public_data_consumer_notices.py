"""Mechanical lint for warning labels in current public structured data."""

import json
import re
from pathlib import Path
from urllib.parse import urlparse

from mb_cmn import paths
from mb_cmn import public_data_consumer_notice as notice

ROOT = paths.repo_root()
NOTICE_KEYS = {"summary", "critical_rules", "documentation"}
MAM_SIMPLE_COUNTS = {"mam": 24, "bhs": 6, "sef": 5}
DOCUMENTATION_TARGETS = {
    notice.MAM_PARSED_PLAIN_DOCUMENTATION: (
        ROOT / "gh-pages" / "MAM-parsed" / "plain" / "html" / "mpplain.html",
        'id="consumer-notice"',
    ),
    notice.MAM_PARSED_PLUS_DOCUMENTATION: (
        ROOT / "gh-pages" / "MAM-parsed" / "plus" / "html" / "mpplus.html",
        'id="consumer-notice"',
    ),
    notice.MAM_SIMPLE_DOCUMENTATION: (
        ROOT / "MAM-simple" / "doc" / "reading-mam-simple.md",
        "## Consumer notice",
    ),
    notice.LENINGRAD_INDEX_DOCUMENTATION: (
        ROOT / "doc" / "scan-pages.md",
        "## Codex entry indexes",
    ),
    notice.ALEPPO_INDEX_DOCUMENTATION: (
        ROOT / "aleppo" / "README.md",
        "## Consumer guide",
    ),
    notice.CAMBRIDGE_INDEX_DOCUMENTATION: (
        ROOT / "cam1753" / "README.md",
        "## Consumer guide",
    ),
}
NARPAS_DOCUMENTATION_TARGETS = (
    ROOT / "MAM-parsed" / "README.md",
    ROOT / "gh-pages" / "MAM-parsed" / "plain" / "html" / "mpplain.html",
    ROOT / "gh-pages" / "MAM-parsed" / "plus" / "html" / "mpplus.html",
    ROOT / "MAM-simple" / "README.md",
    ROOT / "MAM-simple" / "doc" / "reading-mam-simple.md",
    ROOT / "MAM-simple" / "doc" / "reading-mam-simple-xml.md",
)
MAM_PARSED_WHITESPACE_DOCUMENTATION_TARGETS = (
    ROOT / "MAM-parsed" / "README.md",
    ROOT / "gh-pages" / "MAM-parsed" / "plain" / "html" / "mpplain.html",
    ROOT / "gh-pages" / "MAM-parsed" / "plus" / "html" / "mpplus.html",
)


def _load_json(path: Path):
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def _assert_notice(actual, expected, source: Path):
    assert isinstance(actual, dict), f"{source}: consumer_notice is not an object"
    assert (
        set(actual) == NOTICE_KEYS
    ), f"{source}: consumer_notice keys {sorted(actual)} != {sorted(NOTICE_KEYS)}"
    assert (
        isinstance(actual["summary"], str) and actual["summary"].strip()
    ), f"{source}: consumer_notice.summary is empty or not a string"
    rules = actual["critical_rules"]
    assert (
        isinstance(rules, list) and rules
    ), f"{source}: consumer_notice.critical_rules is empty or not an array"
    assert all(
        isinstance(rule, str) and rule.strip() for rule in rules
    ), f"{source}: consumer_notice.critical_rules contains an empty or non-string rule"
    documentation = actual["documentation"]
    assert isinstance(
        documentation, str
    ), f"{source}: consumer_notice.documentation is not a string"
    parsed = urlparse(documentation)
    assert (
        parsed.scheme == "https" and parsed.netloc
    ), f"{source}: documentation is not an absolute HTTPS URL: {documentation!r}"
    assert (
        actual == expected
    ), f"{source}: consumer_notice drifted from its canonical value"


def _assert_narpas_rule(actual, source: Path | str):
    assert notice.NARPAS_GROUPING_RULE in actual["critical_rules"], (
        f"{source}: consumer_notice omits the canonical rule that narpas forms "
        "no compound and encodes no grouping or display-spacing preference"
    )


def _assert_mam_parsed_whitespace_rule(actual, source: Path | str):
    assert notice.MAM_PARSED_WHITESPACE_TEMPLATE_RULE in actual["critical_rules"], (
        f"{source}: consumer_notice omits the canonical rule for whitespace "
        "templates without adjacent literal whitespace"
    )


def _assert_documentation_targets():
    assert set(DOCUMENTATION_TARGETS) == {
        notice.MAM_PARSED_PLAIN_DOCUMENTATION,
        notice.MAM_PARSED_PLUS_DOCUMENTATION,
        notice.MAM_SIMPLE_DOCUMENTATION,
        notice.LENINGRAD_INDEX_DOCUMENTATION,
        notice.ALEPPO_INDEX_DOCUMENTATION,
        notice.CAMBRIDGE_INDEX_DOCUMENTATION,
    }
    for url, (path, anchor_text) in DOCUMENTATION_TARGETS.items():
        assert path.is_file(), f"{url}: maintained local target is missing: {path}"
        contents = path.read_text(encoding="utf-8")
        assert (
            anchor_text in contents
        ), f"{url}: maintained local target lacks anchor evidence {anchor_text!r}"


def _assert_narpas_documentation():
    required_text = (
        "narpas",
        "forms no compound of any kind",
        "display-spacing",
    )
    for path in NARPAS_DOCUMENTATION_TARGETS:
        contents = path.read_text(encoding="utf-8").lower()
        for text in required_text:
            assert text in contents, f"{path}: narpas guidance lacks {text!r}"


def _assert_mam_parsed_whitespace_documentation():
    required_text = (
        "a whitespace template can be the only separator",
        "no literal whitespace at that boundary",
        "dropping the template fuses separate atoms",
        "this rule does not apply to narpas",
    )
    for path in MAM_PARSED_WHITESPACE_DOCUMENTATION_TARGETS:
        contents = " ".join(path.read_text(encoding="utf-8").lower().split())
        for text in required_text:
            assert (
                text in contents
            ), f"{path}: whitespace-template guidance lacks {text!r}"


def test_mam_parsed_notices_and_complete_file_sets():
    expected_stems = None
    for variant in ("plain", "plus"):
        directory = ROOT / "MAM-parsed" / variant
        assert directory.is_dir(), f"missing MAM-parsed directory: {directory}"
        files = sorted(directory.glob("*.json"))
        assert files, f"no MAM-parsed {variant} payloads discovered"
        assert (
            len(files) == 24
        ), f"expected 24 MAM-parsed {variant} payloads, discovered {len(files)}"
        stems = {path.stem for path in files}
        if expected_stems is None:
            expected_stems = stems
        else:
            assert stems == expected_stems, "MAM-parsed plain and plus file sets differ"
        expected_notice = notice.mam_parsed_notice(variant)
        _assert_narpas_rule(expected_notice, f"MAM-parsed/{variant}")
        _assert_mam_parsed_whitespace_rule(expected_notice, f"MAM-parsed/{variant}")
        for path in files:
            payload = _load_json(path)
            assert set(payload) == {
                "header",
                "book39s",
            }, f"{path}: unexpected top-level schema"
            assert set(payload["header"]) == {
                "book24_name",
                "sub_book_names",
                "chapter_counts",
                "consumer_notice",
            }, f"{path}: unexpected header schema"
            _assert_notice(payload["header"]["consumer_notice"], expected_notice, path)


def _mam_simple_files(fmt: str, vtrad: str) -> list[Path]:
    directory = ROOT / "MAM-simple" / f"{fmt}-vtrad-{vtrad}"
    assert directory.is_dir(), f"missing MAM-simple directory: {directory}"
    files = sorted(directory.glob(f"*.{fmt}"))
    assert files, f"no MAM-simple {fmt}/{vtrad} payloads discovered"
    expected_count = MAM_SIMPLE_COUNTS[vtrad]
    assert len(files) == expected_count, (
        f"expected {expected_count} MAM-simple {fmt}/{vtrad} payloads, "
        f"discovered {len(files)}"
    )
    return files


def test_mam_simple_json_and_xml_notices_and_complete_file_sets():
    expected_notice = notice.mam_simple_notice()
    _assert_narpas_rule(expected_notice, "MAM-simple")
    for vtrad in MAM_SIMPLE_COUNTS:
        json_files = _mam_simple_files("json", vtrad)
        xml_files = _mam_simple_files("xml", vtrad)
        assert {path.stem for path in json_files} == {
            path.stem for path in xml_files
        }, f"MAM-simple JSON and XML file sets differ for {vtrad}"
        for path in json_files:
            payload = _load_json(path)
            assert list(payload)[:2] == [
                "provenance",
                "consumer_notice",
            ], f"{path}: consumer_notice is not immediately after provenance"
            assert set(payload) == {
                "provenance",
                "consumer_notice",
                "versification-tradition",
                "contents",
            }, f"{path}: unexpected root schema"
            _assert_notice(payload["consumer_notice"], expected_notice, path)
        for path in xml_files:
            contents = path.read_text(encoding="utf-8")
            match = re.search(r"<!-- consumer_notice: (\{.*\}) -->", contents)
            assert (
                match is not None
            ), f"{path}: missing parseable pre-root consumer notice"
            assert match.start() < contents.index(
                "<book24"
            ), f"{path}: consumer notice does not precede the root element"
            _assert_notice(json.loads(match.group(1)), expected_notice, path)


def _assert_codex_index(
    path: Path,
    expected_notice: dict[str, object],
    required_record_keys: set[str],
):
    payload = _load_json(path)
    assert set(payload) == {
        "header",
        "body",
    }, f"{path}: codex index top level must have exactly header and body"
    header = payload["header"]
    assert isinstance(header, dict), f"{path}: header is not an object"
    assert (
        isinstance(header.get("description"), str) and header["description"].strip()
    ), f"{path}: header.description is empty or missing"
    _assert_notice(header.get("consumer_notice"), expected_notice, path)
    body = payload["body"]
    assert isinstance(body, list) and body, f"{path}: body is empty or not an array"
    for index, record in enumerate(body):
        assert isinstance(record, dict), f"{path}: body[{index}] is not an object"
        assert required_record_keys <= set(
            record
        ), f"{path}: body[{index}] lacks record keys {sorted(required_record_keys)}"
        assert not (
            {"comment", "description", "consumer_notice"} & set(record)
        ), f"{path}: body[{index}] contains synthetic documentation"


def test_codex_entry_indexes_use_canonical_schema_and_notices():
    _assert_codex_index(
        ROOT / "in" / "lci_recs.json",
        notice.codex_index_notice(notice.LENINGRAD_INDEX_DOCUMENTATION),
        {"page", "bkid", "startc", "startv", "startp", "stopc", "stopv", "stopp"},
    )
    aleppo_notice = notice.codex_index_notice(notice.ALEPPO_INDEX_DOCUMENTATION)
    for path in (
        ROOT / "aleppo" / "aleppo-wiki" / "index-flat-corrected.json",
        ROOT / "aleppo" / "index-flat-annotated.json",
    ):
        _assert_codex_index(path, aleppo_notice, {"de_leaf", "de_text_range"})
    _assert_codex_index(
        ROOT / "cam1753" / "cam1753-page-index.json",
        notice.codex_index_notice(notice.CAMBRIDGE_INDEX_DOCUMENTATION),
        {"de_leaf", "de_archive_spread", "de_spread_side"},
    )


def test_notice_documentation_targets_and_anchors_exist():
    _assert_documentation_targets()
    _assert_narpas_documentation()
    _assert_mam_parsed_whitespace_documentation()
