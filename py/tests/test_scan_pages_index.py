"""Lint the tracked scan-pages indexes. See doc/scan-pages.md.

This is the mechanical-lint shape the repo's test rules allow: a decidable property of
tracked data, checked against an independent derivation of the same fact, with no
hand-picked example pinned anywhere.  It needs no scans folder -- the indexes are
self-contained -- but it does need MAM-parsed, and it FAILS rather than skips without
it, per the repo's missing-input rule.
"""

from scan_pages import check
from scan_pages import census
from scan_pages import editions
from scan_pages import index_io
from scan_pages import lookup
from scan_pages import text
from mb_cmn import paths
from mb_cmn import mam_simple_json
from accgram import mam_simple_verse
from mb_misc import osis_book_abbrevs
from mb_cmn import bib_locales as tbn, read_books_from_mam_parsed_plus as plus
from mb_cmn import template_names
from mb_cmn import kq_special_templates
from mb_cmn.silluq_before_meteg import validate_silluq_before_meteg
from copy import deepcopy
from functools import cache
import pytest
import re


def test_tracked_indexes_pass_every_lint():
    """Every check in scan_pages.check, over all five tracked indexes."""
    counts = check.check_all()
    # Guard against a green run that verified nothing: the five indexes exist and hold
    # thousands of pages, so a run reporting a handful means the data went missing.
    assert counts["editions"] == len(editions.ALL_EDITION_IDS)
    assert counts["pages"] > 5000, counts


def test_every_edition_has_a_tracked_index():
    """A new edition must arrive with its index, not merely with its folder name."""
    for edition_id in editions.ALL_EDITION_IDS:
        index = index_io.read_index(edition_id)
        assert index["edition"] == edition_id
        assert index["pages"], edition_id


def _independent_simple_atoms(book):
    """Decode the separate simple export under the maintained written-slot policy."""

    def flatten(node):
        kind = node["type"]
        if kind == "cant-all-three":
            assert set(node) == {"type", "contents"}
            branches = node["contents"]
            assert isinstance(branches, list) and len(branches) == 3
            assert all(isinstance(branch, dict) for branch in branches)
            assert [branch.get("type") for branch in branches] == [
                "cant-combined",
                "cant-alef",
                "cant-bet",
            ]
            forms = []
            for branch in branches:
                if set(branch) == {"type", "text"}:
                    assert isinstance(branch["text"], str) and branch["text"].strip()
                    forms.append(branch["text"])
                else:
                    assert set(branch) == {"type", "contents"}
                    children = branch["contents"]
                    assert isinstance(children, list) and children
                    assert all(
                        isinstance(child, dict)
                        and child.get("type") in {"text", "lp-paseq", "lp-legarmeih"}
                        for child in children
                    )
                    forms.append("".join(map(flatten, children)))
            populations = [
                tuple(
                    letters
                    for token in re.split(r"[\s־]+", form)
                    if (letters := "".join(ch for ch in token if "א" <= ch <= "ת"))
                )
                for form in forms
            ]
            assert populations[0] == populations[1] == populations[2]
            return forms[0]
        if kind == "silluq-before-meteg":
            assert set(node) == {"type", "text", "letters-with-silluq"}
            validate_silluq_before_meteg(
                node["text"], node["letters-with-silluq"], verse["osisID"]
            )
            return node["text"]
        if kind == "spi-invnun":
            assert node == {"type": "spi-invnun"}
            assert verse["osisID"] in {"Num.10.35", "Num.10.36"}
            return "\N{HEBREW PUNCTUATION NUN HAFUKHA}"
        if kind == "spi-samekh3" and "class" in node:
            assert node == {"type": "spi-samekh3", "class": "nu10-invnun-neighbor"}
            assert verse["osisID"] in {"Num.10.35", "Num.10.36"}
            return " "
        if kind == "scrdfftar":
            assert set(node) == {"type", "sdt-starpos", "contents"}
            assert node["sdt-starpos"] in {"before-word", "after-word"}
            assert isinstance(node["contents"], list) and len(node["contents"]) == 2
            target, note = node["contents"]
            assert isinstance(target, dict) and target["type"] == "sdt-target"
            assert isinstance(note, dict) and note["type"] == "sdt-note"
            assert set(note) in ({"type", "text"}, {"type", "contents"})
            if "text" in note:
                assert isinstance(note["text"], str)
            else:
                assert isinstance(note["contents"], list)
            # Only the declared target supplies Scripture. The note is documentation.
            if set(target) == {"type", "text"}:
                assert isinstance(target["text"], str)
                return target["text"]
            assert set(target) == {"type", "contents"}
            assert isinstance(target["contents"], list)
            return "".join(map(flatten, target["contents"]))
        if kind == "kq-trivial" and "contents" in node:
            assert set(node) == {"type", "contents"}
            assert isinstance(node["contents"], list) and len(node["contents"]) == 2
            word, separator = node["contents"]
            assert word["type"] == "text" and separator == {"type": "lp-legarmeih"}
            return flatten(word) + " "
        if kind in {
            "text",
            "kq-trivial",
            "kq-k-velo-q",
            "letter-small",
            "letter-large",
            "letter-hung",
        }:
            assert set(node) == {"type", "text"}
            assert isinstance(node["text"], str)
            return node["text"]
        if kind in {"kq-q-velo-k", "good-ending"}:
            assert set(node) == {"type", "text"}
            assert isinstance(node["text"], str)
            # The maintained written-atom reader omits a qere-only word and
            # the repeated good ending. A written-only word above remains.
            return " "
        if kind == "slh-word":
            assert set(node) == {
                "type",
                "contents",
                "slhw-desc-0",
                "slhw-desc-1",
                "slhw-desc-2",
                "slhw-desc-3",
            }
            assert isinstance(node["contents"], list) and node["contents"]
            assert all(isinstance(node[f"slhw-desc-{i}"], str) for i in range(4))
            pieces, terminal = [], False
            for index, child in enumerate(node["contents"]):
                if child["type"] in {
                    "text",
                    "letter-small",
                    "letter-large",
                    "letter-hung",
                }:
                    piece = flatten(child)
                    if child["type"] != "text":
                        assert sum("א" <= ch <= "ת" for ch in piece) == 1
                        assert not any(ch.isspace() or ch == "־" for ch in piece)
                    pieces.append(piece)
                else:
                    assert child == {"type": "lp-legarmeih"}
                    assert index == len(node["contents"]) - 1
                    terminal = True
            body = "".join(pieces)
            assert any("א" <= ch <= "ת" for ch in body)
            assert (
                body + ("\N{HEBREW PUNCTUATION PASEQ}" if terminal else "")
                == node["slhw-desc-0"]
            )
            return body + (" " if terminal else "")
        if kind == "kq":
            assert sorted(n["type"] for n in node["contents"]) == ["kq-k", "kq-q"]
            qere = next(n for n in node["contents"] if n["type"] == "kq-q")
            if set(qere) == {"type", "text"}:
                assert isinstance(qere["text"], str)
                return qere["text"]
            assert set(qere) == {"type", "contents"}
            assert all(
                n["type"] in {"text", "lp-paseq", "lp-legarmeih"}
                for n in qere["contents"]
            )
            return "".join(map(flatten, qere["contents"]))
        assert node in (
            {"type": "lp-legarmeih"},
            {"type": "lp-paseq"},
            {"type": "implicit-maqaf"},
            {"type": "shirah-space"},
            {"type": "spi-pe2"},
            {"type": "spi-pe3"},
            {"type": "spi-samekh2"},
            {"type": "spi-samekh3"},
        )
        return " "

    def flatten_sequence(nodes):
        assert isinstance(nodes, list)
        parts = []
        for index, node in enumerate(nodes):
            if node.get("type") == "kq-k-velo-q-maq":
                assert node == {"type": "kq-k-velo-q-maq"} and index > 0
                previous = nodes[index - 1]
                assert set(previous) == {"type", "text"}
                assert previous["type"] == "kq-k-velo-q"
                assert isinstance(previous["text"], str)
                written = tuple(
                    letters
                    for token in re.split(r"[\s־]+", previous["text"])
                    if (letters := "".join(ch for ch in token if "א" <= ch <= "ת"))
                )
                assert len(written) == 1
                # This bare following mark adds no atom; keep the neighboring
                # written forms apart when concatenating the Scripture text.
                parts.append(" ")
            else:
                parts.append(flatten(node))
        return "".join(parts)

    simple_path = mam_simple_verse.mam_simple_json_path(
        paths.repo_root() / "MAM-simple" / "json-vtrad-mam", book
    )
    expected = {}
    prefix = osis_book_abbrevs.BOOK_ABBREVS[book] + "."
    for verse in mam_simple_json.verses(mam_simple_json.read_book_group(simple_path)):
        if not verse["osisID"].startswith(prefix):
            continue
        _, c, v = verse["osisID"].split(".")
        contents = verse.get("contents", [])
        if (
            contents
            and contents[0].get("type") == "spi-invnun"
            and verse["osisID"] not in {"Num.10.35", "Num.10.36"}
        ):
            assert contents[0] == {
                "type": "spi-invnun",
                "class": "including-trailing-space",
            }
            contents = contents[1:]
            assert contents
        source_text = verse["text"] if "text" in verse else flatten_sequence(contents)
        expected[int(c), int(v)] = tuple(
            letters
            for token in re.split(r"[\s־]+", source_text)
            if (letters := "".join(ch for ch in token if "א" <= ch <= "ת"))
        )
    return expected


def test_dual_representations_agree_with_independent_simple_export():
    """Check every current dual context and its closed branch contracts."""
    checked_nodes, checked_verses = 0, 0
    for book in tbn.ALL_BK39_IDS:
        data = plus.read_parsed_plus_bk39s(
            [book], mam_parsed_path=paths.mam_parsed_path()
        )[book]
        assert data["verses_plus"]
        expected = None
        for bcvt, row in data["verses_plus"].items():
            duals = [
                node
                for node in _templates(row.EP)
                if node["tmpl_name"] == template_names.DUAL_CANTILLATION
            ]
            if not duals:
                continue
            if expected is None:
                expected = _independent_simple_atoms(book)
                assert expected
            cv = tbn.bcvt_get_chnu(bcvt), tbn.bcvt_get_vrnu(bcvt)
            pointed = text._verse_text(row.EP, bcv=(book, *cv))
            assert text.letters_atoms(pointed) == expected[cv]
            checked_verses += 1
            for node in duals:
                params = template_names.validate_current_plus_template(node)
                forms, traces = [], []
                for key in ("כפול", "א", "ב"):
                    trace = []
                    forms.append(text._target_text(params[key], protected=trace))
                    traces.append(trace)
                    for mutation in ("missing", "unknown", "unequal"):
                        bad = deepcopy(node)
                        if mutation == "missing":
                            del bad["tmpl_params"][key]
                        elif mutation == "unknown":
                            bad["tmpl_params"][key] = {
                                "tmpl_name": "unknown-dual-child"
                            }
                        else:
                            previous = bad["tmpl_params"][key]
                            bad["tmpl_params"][key] = (
                                ["א", *previous]
                                if isinstance(previous, (list, tuple))
                                else ["א", previous]
                            )
                        with pytest.raises((ValueError, TypeError)):
                            text._body_text([bad])
                assert (
                    text.letters_atoms(forms[0])
                    == text.letters_atoms(forms[1])
                    == text.letters_atoms(forms[2])
                )
                assert traces[0] == traces[1] == traces[2]
                selected_trace = []
                assert text._body_text([node], protected=selected_trace) == forms[0]
                assert selected_trace == traces[0]
                checked_nodes += 1
    assert checked_nodes and checked_verses, "No current dual population was checked"


def test_censused_books_agree_with_independent_simple_export():
    """Compare every adopted book's atom stream with the separate simple product."""
    checked = set()
    for edition in editions.ALL_EDITION_IDS:
        index = index_io.read_index(edition)
        for segment in index["segments"]:
            for book in segment["bkids"]:
                if book in checked:
                    continue
                assert _independent_simple_atoms(book) == text.book_atoms(book), (
                    edition,
                    book,
                )
                checked.add(book)
    assert checked, "No adopted book was cross-checked"


def test_frontier_jeremiah_atoms_agree_and_malformed_forms_refuse():
    """Check all frontier text independently without declaring page coverage."""
    assert _independent_simple_atoms("Jeremiah") == text.book_atoms("Jeremiah")
    book = plus.read_parsed_plus_bk39s(
        ["Jeremiah"], mam_parsed_path=paths.mam_parsed_path()
    )["Jeremiah"]

    def templates(node):
        if isinstance(node, dict):
            if "tmpl_name" in node:
                yield node
            for child in node.values():
                yield from templates(child)
        elif isinstance(node, (list, tuple)):
            for child in node:
                yield from templates(child)

    checked = 0
    for row in book["verses_plus"].values():
        for wrapper in templates(row.EP):
            name, params = wrapper["tmpl_name"], wrapper.get("tmpl_params", {})
            corruptions = []
            if name == "קרי ולא כתיב":
                for key in ("1", "2"):
                    bad = deepcopy(wrapper)
                    bad["tmpl_params"][key] += "א"
                    corruptions.append(bad)
                    bad = deepcopy(wrapper)
                    bad["tmpl_params"][key] = [params[key]]
                    corruptions.append(bad)
                    bad = deepcopy(wrapper)
                    bad["tmpl_params"][key] += " " + params[key]
                    corruptions.append(bad)
            elif name == "מ:כו״ק מיוחד" and isinstance(params["2"], list):
                bad = deepcopy(wrapper)
                bad["tmpl_params"]["2"][1]["tmpl_name"] = "unsupported"
                corruptions.append(bad)
                bad = deepcopy(wrapper)
                bad["tmpl_params"]["2"][1]["tmpl_params"] = {"1": "annotation"}
                corruptions.append(bad)
                bad = deepcopy(wrapper)
                del bad["tmpl_params"]["2"][1]
                corruptions.append(bad)
                bad = deepcopy(wrapper)
                bad["tmpl_params"]["2"][0] += " " + params["2"][0]
                corruptions.append(bad)
            for bad in corruptions:
                with pytest.raises((ValueError, TypeError)):
                    text._body_text([bad])
                checked += 1
    assert checked, "No new frontier form was fault-checked"


def _psalms_source():
    return plus.read_parsed_plus_bk39s(
        ["Psalms"], mam_parsed_path=paths.mam_parsed_path()
    )["Psalms"]


def _templates(node):
    if isinstance(node, dict):
        if "tmpl_name" in node:
            yield node
        for child in node.values():
            yield from _templates(child)
    elif isinstance(node, (list, tuple)):
        for child in node:
            yield from _templates(child)


def test_frontier_psalms_atoms_agree_with_independent_simple_export():
    """Compare the whole candidate text without declaring native page coverage."""
    assert _independent_simple_atoms("Psalms") == text.book_atoms("Psalms")


def test_frontier_psalms_malformed_forms_refuse():
    """Fault-check the new closed shapes throughout the actual source corpus."""
    checked = set()
    separators = {"ר0", "ר1", "ר2", "ר3", "ר4", "מ:מקף אפור"}
    letters = {"מ:אות-ק", "מ:אות-ג", "מ:אות תלויה"}
    variants = {template_names.QAMATS_VARIANT, *template_names.STRESS_HELPER_TMPL_NAMES}
    for row in _psalms_source()["verses_plus"].values():
        for wrapper in _templates(row.EP):
            name, params = wrapper["tmpl_name"], wrapper.get("tmpl_params", {})
            corruptions = []
            if name in separators | variants | letters | {template_names.SLH_WORD}:
                bad = deepcopy(wrapper)
                bad.setdefault("tmpl_params", {})["extra"] = "metadata"
                corruptions.append(bad)
            if name in separators:
                bad = deepcopy(wrapper)
                bad["tmpl_params"] = {"1": "א"}
                corruptions.append(bad)
            elif name in variants:
                key = "ס" if name == template_names.QAMATS_VARIANT else "2"
                bad = deepcopy(wrapper)
                bad["tmpl_params"][key] = "א"
                corruptions.append(bad)
                bad = deepcopy(wrapper)
                bad["tmpl_params"][key] = [params[key]]
                corruptions.append(bad)
                if isinstance(params[key], str):
                    bad = deepcopy(wrapper)
                    value = params[key]
                    # Toggle a real outer boundary, preserving all letters.
                    if value[-1].isspace() or value[-1] == "\u05be":
                        value = value.rstrip().rstrip("\u05be").rstrip()
                    else:
                        value += " "
                    bad["tmpl_params"][key] = value
                    corruptions.append(bad)
            elif name in letters:
                for value in (params["1"] + "א", params["1"] + " ", [params["1"]]):
                    bad = deepcopy(wrapper)
                    bad["tmpl_params"]["1"] = value
                    corruptions.append(bad)
            elif name == template_names.SLH_WORD:
                bad = deepcopy(wrapper)
                bad["tmpl_params"]["2"] += "א"
                corruptions.append(bad)
                for key in ("3", "4", "5"):
                    bad = deepcopy(wrapper)
                    bad["tmpl_params"][key] = []
                    corruptions.append(bad)
            elif name == "מ:כו״ק מיוחד":
                bad = deepcopy(wrapper)
                bad["tmpl_params"]["1"] += "א"
                corruptions.append(bad)
                bad = deepcopy(wrapper)
                bad["tmpl_params"]["סוג"] = "unsupported"
                corruptions.append(bad)
            elif name in {"כו״ק", "קו״כ", template_names.TRIVIAL_QERE}:
                for key, form in params.items():
                    if isinstance(form, list):
                        bad = deepcopy(wrapper)
                        bad["tmpl_params"][key][-1] = {"tmpl_name": "unsupported"}
                        corruptions.append(bad)
                    elif isinstance(form, dict):
                        bad = deepcopy(wrapper)
                        bad["tmpl_params"][key]["tmpl_name"] = "unsupported"
                        corruptions.append(bad)
            for bad in corruptions:
                with pytest.raises((ValueError, TypeError, KeyError)):
                    text._body_text([bad])
                checked.add(name)
    assert separators - {"ר4"} <= checked
    assert (
        variants
        | letters
        | {template_names.SLH_WORD, "מ:כו״ק מיוחד", template_names.TRIVIAL_QERE, "כו״ק"}
        <= checked
    )


def test_frontier_psalms_inverted_nuns_remain_leading_and_exact():
    """A source sign cannot contribute letters, hide an interior node or join atoms."""
    checked = 0
    for row in _psalms_source()["verses_plus"].values():
        nodes = row.EP
        if not (
            isinstance(nodes[0], dict)
            and nodes[0].get("tmpl_name") == template_names.INVERTED_NUN
        ):
            continue
        assert text._verse_text(nodes) == text._body_text(nodes[1:])
        for value in ("\u05c6", "\u05c6  ", "\u05c6 א", " ", ["\u05c6 "]):
            bad = deepcopy(nodes[0])
            bad["tmpl_params"]["1"] = value
            with pytest.raises((ValueError, TypeError)):
                text._verse_text([bad, *nodes[1:]])
        for bad in (
            [nodes[0]],
            [nodes[0], *nodes],
            [*nodes[1:], nodes[0]],
            [{"tmpl_name": "נוסח", "tmpl_params": {"1": nodes[0]}}],
        ):
            with pytest.raises((ValueError, TypeError)):
                text._verse_text(bad)
        checked += 1
    assert checked, "No leading sign was checked"


def test_frontier_psalms_unequal_mappings_preserve_spans_and_refuse_ambiguity():
    """Derive mapped pairs from source and independently decoded verse atoms."""
    from types import SimpleNamespace

    expected = _independent_simple_atoms("Psalms")
    book = _psalms_source()
    actual = text.book_alignment_spans("Psalms", {"Psalms": book})
    derived = []
    for bcvt, row in book["verses_plus"].items():
        phrases = []
        text._verse_text(row.EP, protected=phrases)
        cv = tbn.bcvt_get_chnu(bcvt), tbn.bcvt_get_vrnu(bcvt)
        for phrase in phrases:
            pair = tuple(phrase.split(" "))
            matches = [
                i
                for i in range(len(expected[cv]) - 1)
                if expected[cv][i : i + 2] == pair
            ]
            assert len(pair) == 2 and len(matches) == 1
            first = matches[0] + 1
            derived.append(((*cv, first), (*cv, first + 1)))
            bad = [*row.EP, " " + phrase]
            mutated = {"Psalms": {"verses_plus": {bcvt: SimpleNamespace(EP=bad)}}}
            with pytest.raises(ValueError, match="supply a longer unique cue"):
                text.book_alignment_spans("Psalms", mutated)
    assert derived and tuple(derived) == actual


def test_every_record_edge_resolves_to_its_observed_page(monkeypatch):
    """Each handwritten source cue is an independent oracle for public lookup."""
    # Reuse each immutable book projection and each edition's checked partition.
    # The resolver still locates every cue and selects its page for every query.
    book_atoms = cache(text.book_atoms)
    validate_book = census.validate_book
    checked = {}

    def checked_book(index, book, verses):
        key = index["edition"], book
        if key not in checked:
            checked[key] = validate_book(index, book, verses)
        return checked[key]

    monkeypatch.setattr(text, "book_atoms", book_atoms)
    monkeypatch.setattr(census, "validate_book", checked_book)
    count = 0
    for edition in editions.ALL_EDITION_IDS:
        index = index_io.read_index(edition)
        for rec in index["recs"]:
            if rec["stopc"] is None:
                continue
            for end in ("start", "stop"):
                first, _ = text.locate_phrase_span(
                    book_atoms(rec["bkid"]),
                    rec[f"{end}c"],
                    rec[f"{end}v"],
                    rec[f"{end}_phrase"],
                    anchor=end,
                )
                hits = lookup.resolve(
                    index,
                    rec["bkid"],
                    first[0],
                    first[1],
                    rec[f"{end}_phrase"],
                )
                assert [hit["page"] for hit in hits] == [rec["page"]]
                count += 1
    assert count, "No observed page edges were queried"


def test_adopted_partitions_refuse_boundaries_inside_mapped_written_words():
    """An otherwise contiguous canonical partition cannot split one written word."""
    checked = 0
    for edition in editions.ALL_EDITION_IDS:
        index = index_io.read_index(edition)
        for segment in index["segments"]:
            for book in segment["bkids"]:
                verses = text.book_atoms(book)
                for first, last in text.book_alignment_spans(book):
                    records = census.validate_book(index, book, verses)
                    i = next(
                        i
                        for i, rec in enumerate(records)
                        if tuple(rec["start" + s] for s in "cvp") <= first
                        and last <= tuple(rec["stop" + s] for s in "cvp")
                    )
                    assert first[:2] == last[:2] and last[2] == first[2] + 1
                    c, v = first[:2]
                    pair = " ".join(verses[c, v][first[2] - 1 : last[2]])
                    assert [
                        hit["page"] for hit in lookup.resolve(index, book, c, v, pair)
                    ] == [records[i]["page"]]
                    assert i + 1 < len(records)
                    bad = deepcopy(index)
                    left = next(r for r in bad["recs"] if r == records[i])
                    right = next(r for r in bad["recs"] if r == records[i + 1])
                    # Move a real page boundary into the mapped pair. Both cues
                    # are unique, and every canonical atom still occurs once.
                    for side, rec, pos in (
                        ("stop", left, first),
                        ("start", right, last),
                    ):
                        rec.update({side + key: n for key, n in zip("cvp", pos)})
                    left["stop_phrase"] = " ".join(verses[c, v][: first[2]])
                    right["start_phrase"] = " ".join(verses[c, v][last[2] - 1 :])
                    assert (
                        text.locate_phrase_span(
                            verses, c, v, left["stop_phrase"], anchor="stop"
                        )[1]
                        == first
                    )
                    assert (
                        text.locate_phrase_span(verses, c, v, right["start_phrase"])[0]
                        == last
                    )
                    with pytest.raises(
                        ValueError, match="inside a mapped written-word span"
                    ):
                        census.validate_book(bad, book, verses)
                    checked += 1
    assert checked, "No adopted unequal mapping was boundary-checked"


def test_nested_vowel_ketiv_qere_agrees_with_independent_simple_export():
    """Cross-check each newly supported nested form in the Ezekiel source corpus."""
    book = plus.read_parsed_plus_bk39s(
        ["Ezekiel"], mam_parsed_path=paths.mam_parsed_path()
    )["Ezekiel"]
    simple_path = mam_simple_verse.mam_simple_json_path(
        paths.repo_root() / "MAM-simple" / "json-vtrad-mam", "Ezekiel"
    )
    exported = {
        tuple(map(int, verse["osisID"].split(".")[1:])): verse
        for verse in mam_simple_json.verses(
            mam_simple_json.read_book_group(simple_path)
        )
    }
    checked = 0
    for bcvt, row in book["verses_plus"].items():
        nested = [
            element
            for element in row.EP
            if isinstance(element, dict)
            and element["tmpl_name"] in {"כו״ק", "קו״כ"}
            and any(
                isinstance(form, dict)
                and form.get("tmpl_name") == template_names.QAMATS_VARIANT
                for form in element["tmpl_params"].values()
            )
        ]
        if not nested:
            continue
        cv = tbn.bcvt_get_chnu(bcvt), tbn.bcvt_get_vrnu(bcvt)
        parts = []
        for node in exported[cv]["contents"]:
            if node["type"] == "text":
                parts.append(node["text"])
            else:
                assert node["type"] == "kq"
                assert sorted(child["type"] for child in node["contents"]) == [
                    "kq-k",
                    "kq-q",
                ]
                parts.append(
                    next(
                        child["text"]
                        for child in node["contents"]
                        if child["type"] == "kq-q"
                    )
                )
        expected = tuple(
            letters
            for token in re.split(r"[\s־]+", "".join(parts))
            if (letters := "".join(ch for ch in token if "א" <= ch <= "ת"))
        )
        assert text.letters_atoms(text._body_text(row.EP)) == expected, cv
        for wrapper in nested:
            # Mutate the independently captured form: accepting an unknown
            # wrapper, unequal alternatives or extra slots would invalidate
            # this one-to-one physical alignment even if the verse still parsed.
            key = next(
                key
                for key, form in wrapper["tmpl_params"].items()
                if isinstance(form, dict)
            )
            form = wrapper["tmpl_params"][key]
            corrupt_forms = []
            bad = deepcopy(form)
            bad["tmpl_name"] = "unsupported"
            corrupt_forms.append(bad)
            bad = deepcopy(form)
            bad["tmpl_params"]["ד"] += "א"
            corrupt_forms.append(bad)
            bad = deepcopy(form)
            for alternative in ("ד", "ס"):
                bad["tmpl_params"][alternative] += " " + bad["tmpl_params"][alternative]
            corrupt_forms.append(bad)
            bad = deepcopy(form)
            del bad["tmpl_params"]["ס"]
            corrupt_forms.append(bad)
            corrupt_forms.append([deepcopy(form)])
            for bad_form in corrupt_forms:
                bad_wrapper = deepcopy(wrapper)
                bad_wrapper["tmpl_params"][key] = bad_form
                with pytest.raises((ValueError, TypeError)):
                    text._body_text([bad_wrapper])
        checked += 1
    assert checked, "No nested vowel ketiv/qere was cross-checked"


def test_written_only_following_maqaf_verses_agree_with_simple():
    """Compare every actual following-maqaf verse with the independent export."""
    books = plus.read_parsed_plus_bk39s(mam_parsed_path=paths.mam_parsed_path())
    expected, checked = {}, 0
    for book, data in books.items():
        for bcvt, row in data["verses_plus"].items():
            markers = [
                node
                for node in _templates(row.EP)
                if node["tmpl_name"] == "כתיב ולא קרי" and "3" in node["tmpl_params"]
            ]
            if not markers:
                continue
            if book not in expected:
                expected[book] = _independent_simple_atoms(book)
            cv = tbn.bcvt_get_chnu(bcvt), tbn.bcvt_get_vrnu(bcvt)
            assert (
                text.letters_atoms(text._verse_text(row.EP, bcv=(book, *cv)))
                == expected[book][cv]
            )
            checked += len(markers)
    assert checked, "No written-only following-maqaf forms were compared"


def test_all_one_written_two_qere_special_verses_agree_with_simple():
    """Compare every declared pair and its protected span with the stored export."""
    pair_types = {
        "k1q2-sr-kqq",
        "k1q2-sr-qqk",
        "k1q2-sr-bcom",
        "k1q2-wr-kqq",
        "k1q2-ur-qqk",
    }
    books = plus.read_parsed_plus_bk39s(mam_parsed_path=paths.mam_parsed_path())
    expected, simple_verses, checked = {}, {}, 0

    def simple_kq_inventory(node):
        # Whole-structure inventory only; qere selection below uses typed roles.
        if isinstance(node, dict):
            if node.get("type") == "kq":
                yield node
            for child in node.get("contents", []):
                yield from simple_kq_inventory(child)

    for book, data in books.items():
        for bcvt, row in data["verses_plus"].items():
            pairs = [
                node
                for node in _templates(row.EP)
                if node["tmpl_name"] == "מ:כו״ק מיוחד"
                and kq_special_templates.canonical_special_kq_type_from_name_and_sug(
                    node["tmpl_name"], node["tmpl_params"]["סוג"]
                )
                in pair_types
            ]
            if not pairs:
                continue
            if book not in expected:
                expected[book] = _independent_simple_atoms(book)
                simple_path = mam_simple_verse.mam_simple_json_path(
                    paths.repo_root() / "MAM-simple/json-vtrad-mam", book
                )
                simple_verses[book] = {
                    tuple(map(int, verse["osisID"].split(".")[1:])): verse
                    for verse in mam_simple_json.verses(
                        mam_simple_json.read_book_group(simple_path)
                    )
                    if verse["osisID"].startswith(
                        osis_book_abbrevs.BOOK_ABBREVS[book] + "."
                    )
                }
            cv = tbn.bcvt_get_chnu(bcvt), tbn.bcvt_get_vrnu(bcvt)
            bounded = {book: {"verses_plus": {bcvt: row}}}
            assert text.book_atoms(book, bounded) == {cv: expected[book][cv]}
            spans = text.book_alignment_spans(book, bounded)
            assert len(spans) == len(pairs)
            expected_spans = []
            for pair in pairs:
                matching = [
                    node
                    for node in simple_kq_inventory(simple_verses[book][cv])
                    if any(
                        child.get("type") == "kq-k"
                        and child.get("text") == pair["tmpl_params"]["1"]
                        for child in node["contents"]
                    )
                ]
                assert len(matching) == 1
                qere = next(
                    child
                    for child in matching[0]["contents"]
                    if child["type"] == "kq-q"
                )
                if set(qere) == {"type", "text"}:
                    pointed = qere["text"]
                else:
                    assert set(qere) == {"type", "contents"}
                    assert all(
                        set(child) == {"type", "text"}
                        and child["type"] == "text"
                        or child in ({"type": "lp-paseq"}, {"type": "lp-legarmeih"})
                        for child in qere["contents"]
                    )
                    pointed = "".join(
                        child["text"] if child["type"] == "text" else " "
                        for child in qere["contents"]
                    )
                reading = tuple(
                    letters
                    for atom in re.split(r"[\s־]+", pointed)
                    if (letters := "".join(c for c in atom if "א" <= c <= "ת"))
                )
                assert len(reading) == 2
                matches = [
                    i
                    for i in range(len(expected[book][cv]) - 1)
                    if expected[book][cv][i : i + 2] == reading
                ]
                assert len(matches) == 1
                expected_spans.append(((*cv, matches[0] + 1), (*cv, matches[0] + 2)))
            assert spans == tuple(expected_spans)
            for first, last in spans:
                assert first[:2] == last[:2] == cv and last[2] == first[2] + 1
                phrase = expected[book][cv][first[2] - 1 : last[2]]
                matches = [
                    i
                    for i in range(len(expected[book][cv]) - 1)
                    if expected[book][cv][i : i + 2] == phrase
                ]
                assert matches == [first[2] - 1]
            checked += len(pairs)
    assert checked, "No declared one-written/two-qere cases were compared"


def test_all_two_written_one_qere_special_verses_agree_with_simple():
    """Compare every named two/one form with independent tagged qere roles."""
    books = plus.read_parsed_plus_bk39s(mam_parsed_path=paths.mam_parsed_path())
    assert len(books) == 39
    expected, simple_verses, checked = {}, {}, 0

    def simple_kq_inventory(node):
        # Stored-node inventory only; selection uses the named roles below.
        if isinstance(node, dict):
            if node.get("type") == "kq":
                yield node
            for child in node.get("contents", []):
                yield from simple_kq_inventory(child)

    for book, data in books.items():
        for bcvt, row in data["verses_plus"].items():
            cases = [
                node
                for node in _templates(row.EP)
                if node["tmpl_name"] == "מ:כו״ק מיוחד"
                and kq_special_templates.canonical_special_kq_type_from_name_and_sug(
                    node["tmpl_name"], node["tmpl_params"]["סוג"]
                )
                == "k2q1"
            ]
            if not cases:
                continue
            if book not in expected:
                expected[book] = _independent_simple_atoms(book)
                simple_path = mam_simple_verse.mam_simple_json_path(
                    paths.repo_root() / "MAM-simple/json-vtrad-mam", book
                )
                simple_verses[book] = {
                    tuple(map(int, verse["osisID"].split(".")[1:])): verse
                    for verse in mam_simple_json.verses(
                        mam_simple_json.read_book_group(simple_path)
                    )
                    if verse["osisID"].startswith(
                        osis_book_abbrevs.BOOK_ABBREVS[book] + "."
                    )
                }
            cv = tbn.bcvt_get_chnu(bcvt), tbn.bcvt_get_vrnu(bcvt)
            bounded = {book: {"verses_plus": {bcvt: row}}}
            assert text.book_atoms(book, bounded) == {cv: expected[book][cv]}
            assert text.book_alignment_spans(book, bounded) == ()
            for case in cases:
                matches = [
                    node
                    for node in simple_kq_inventory(simple_verses[book][cv])
                    if any(
                        child.get("type") == "kq-k"
                        and child.get("text") == case["tmpl_params"]["1"]
                        for child in node["contents"]
                    )
                ]
                assert len(matches) == 1
                roles = matches[0]["contents"]
                assert len(roles) == 2 and {child["type"] for child in roles} == {
                    "kq-k",
                    "kq-q",
                }
                assert all(
                    set(child) == {"type", "text"} and isinstance(child["text"], str)
                    for child in roles
                )
                written = next(
                    child["text"] for child in roles if child["type"] == "kq-k"
                )
                reading = next(
                    child["text"] for child in roles if child["type"] == "kq-q"
                )
                assert (
                    len(text.letters_atoms(written)) == 2
                    and len(text.letters_atoms(reading)) == 1
                )
                trace = []
                assert (
                    text._body_text(
                        [case], protected=trace, context=((book, *cv), row.EP)
                    )
                    == reading
                )
                assert trace == []
                checked += 1
    assert checked, "No named two-written/one-qere cases were compared"


def test_mid_compound_special_verses_agree_with_tagged_simple():
    """Inventory the declared subtype and compare its complete verse and roles."""
    books = plus.read_parsed_plus_bk39s(mam_parsed_path=paths.mam_parsed_path())
    expected, stored, checked = {}, {}, 0

    def kq_inventory(node):
        if isinstance(node, dict):
            if node.get("type") == "kq":
                yield node
            for child in node.get("contents", []):
                yield from kq_inventory(child)

    for book, data in books.items():
        for bcvt, row in data["verses_plus"].items():
            selected = [
                node
                for node in _templates(row.EP)
                if node["tmpl_name"] == "מ:כו״ק מיוחד"
                and kq_special_templates.canonical_special_kq_type_from_name_and_sug(
                    node["tmpl_name"], node["tmpl_params"]["סוג"]
                )
                == "k1q1-mcom"
            ]
            if not selected:
                continue
            if book not in expected:
                expected[book] = _independent_simple_atoms(book)
                simple_path = mam_simple_verse.mam_simple_json_path(
                    paths.repo_root() / "MAM-simple/json-vtrad-mam", book
                )
                stored[book] = {
                    tuple(map(int, verse["osisID"].split(".")[1:])): verse
                    for verse in mam_simple_json.verses(
                        mam_simple_json.read_book_group(simple_path)
                    )
                    if verse["osisID"].startswith(
                        osis_book_abbrevs.BOOK_ABBREVS[book] + "."
                    )
                }
            cv = tbn.bcvt_get_chnu(bcvt), tbn.bcvt_get_vrnu(bcvt)
            bounded = {book: {"verses_plus": {bcvt: row}}}
            assert text.book_atoms(book, bounded) == {cv: expected[book][cv]}
            assert text.book_alignment_spans(book, bounded) == ()
            for node in selected:
                params = node["tmpl_params"]
                matching = [
                    kq
                    for kq in kq_inventory(stored[book][cv])
                    if any(
                        child.get("type") == "kq-k" and child.get("text") == params["1"]
                        for child in kq["contents"]
                    )
                ]
                assert len(matching) == 1
                simple = matching[0]
                assert (
                    set(simple) == {"type", "class", "contents"}
                    and simple["class"] == "sep-maqaf"
                )
                assert sorted(child["type"] for child in simple["contents"]) == [
                    "kq-k",
                    "kq-q",
                ]
                for child in simple["contents"]:
                    assert set(child) == {"type", "text"} and isinstance(
                        child["text"], str
                    )
                    assert (
                        child["text"] == params["1" if child["type"] == "kq-k" else "2"]
                    )
                    atoms = tuple(
                        letters
                        for atom in re.split(r"[\s־]+", child["text"])
                        if (letters := "".join(c for c in atom if "א" <= c <= "ת"))
                    )
                    assert len(atoms) == 1
                checked += 1
    assert checked, "No declared mid-compound special forms were compared"


def test_preceding_maqaf_special_contexts_refuse_trailing_whitespace():
    """Fault-check literal adjacency in every declared preceding-maqaf context."""
    types = {"k1q1-mcom", "k1q2-sr-qqk", "k1q2-sr-bcom", "k1q2-ur-qqk"}
    books = plus.read_parsed_plus_bk39s(mam_parsed_path=paths.mam_parsed_path())
    checked = 0
    for book, data in books.items():
        for bcvt, row in data["verses_plus"].items():
            for node in _templates(row.EP):
                if node["tmpl_name"] != "מ:כו״ק מיוחד":
                    continue
                subtype = (
                    kq_special_templates.canonical_special_kq_type_from_name_and_sug(
                        node["tmpl_name"], node["tmpl_params"]["סוג"]
                    )
                )
                if subtype not in types:
                    continue
                cv = tbn.bcvt_get_chnu(bcvt), tbn.bcvt_get_vrnu(bcvt)
                text._verse_text(row.EP, bcv=(book, *cv))
                owners = [
                    i
                    for i, element in enumerate(row.EP)
                    if element is node
                    or isinstance(element, dict)
                    and element.get("tmpl_name") == "נוסח"
                    and element["tmpl_params"]["1"] is node
                ]
                assert len(owners) == 1 and owners[0] > 0
                previous = owners[0] - 1
                assert isinstance(row.EP[previous], str) and row.EP[previous].endswith(
                    "\N{HEBREW PUNCTUATION MAQAF}"
                )
                for whitespace in (" ", "\t", "\n", "\N{NO-BREAK SPACE}"):
                    altered = deepcopy(list(row.EP))
                    altered[previous] += whitespace
                    with pytest.raises(ValueError):
                        text._verse_text(altered, bcv=(book, *cv))
                    checked += 1
    assert checked, "No preceding-maqaf contexts were fault-checked"


def test_between_maqaf_pairs_keep_complete_following_simple_partner():
    """Derive the following compound boundary from independently tagged storage."""
    books = plus.read_parsed_plus_bk39s(mam_parsed_path=paths.mam_parsed_path())
    stored, expected, checked = {}, {}, 0

    def contexts(node):
        if isinstance(node, dict):
            children = node.get("contents", [])
            for index, child in enumerate(children):
                if child.get("type") == "kq":
                    yield child, children[index + 1 :]
                yield from contexts(child)

    for book, data in books.items():
        for bcvt, row in data["verses_plus"].items():
            selected = [
                node
                for node in _templates(row.EP)
                if node["tmpl_name"] == "מ:כו״ק מיוחד"
                and kq_special_templates.canonical_special_kq_type_from_name_and_sug(
                    node["tmpl_name"], node["tmpl_params"]["סוג"]
                )
                == "k1q2-sr-bcom"
            ]
            if not selected:
                continue
            if book not in stored:
                simple_path = mam_simple_verse.mam_simple_json_path(
                    paths.repo_root() / "MAM-simple/json-vtrad-mam", book
                )
                stored[book] = {
                    tuple(map(int, verse["osisID"].split(".")[1:])): verse
                    for verse in mam_simple_json.verses(
                        mam_simple_json.read_book_group(simple_path)
                    )
                    if verse["osisID"].startswith(
                        osis_book_abbrevs.BOOK_ABBREVS[book] + "."
                    )
                }
                expected[book] = _independent_simple_atoms(book)
            cv = tbn.bcvt_get_chnu(bcvt), tbn.bcvt_get_vrnu(bcvt)
            bounded = {book: {"verses_plus": {bcvt: row}}}
            assert text.book_atoms(book, bounded) == {cv: expected[book][cv]}
            for node in selected:
                params = node["tmpl_params"]
                matches = [
                    (simple, following)
                    for simple, following in contexts(stored[book][cv])
                    if any(
                        child.get("type") == "kq-k" and child.get("text") == params["1"]
                        for child in simple["contents"]
                    )
                ]
                assert len(matches) == 1
                simple, following = matches[0]
                assert simple == {
                    "type": "kq",
                    "class": "sep-maqaf",
                    "contents": [
                        {"type": "kq-k", "text": params["1"]},
                        {"type": "kq-q", "text": params["2"]},
                    ],
                }
                assert following and set(following[0]) == {"type", "text"}
                assert following[0]["type"] == "text"
                tail = following[0]["text"]
                partner, separator, remainder = tail.partition(" ")
                assert partner and not partner[0].isspace() and separator == " "
                owners = [
                    i
                    for i, element in enumerate(row.EP)
                    if element is node
                    or isinstance(element, dict)
                    and element.get("tmpl_name") == "נוסח"
                    and element["tmpl_params"]["1"] is node
                ]
                assert len(owners) == 1 and owners[0] + 1 < len(row.EP)
                assert row.EP[owners[0] + 1] == tail
                for letter in ("א", "ת"):
                    altered = deepcopy(list(row.EP))
                    altered[owners[0] + 1] = partner + letter + separator + remainder
                    with pytest.raises(ValueError):
                        text._verse_text(altered, bcv=(book, *cv))
                    checked += 1
    assert checked, "No declared between-maqaf pair contexts were checked"
