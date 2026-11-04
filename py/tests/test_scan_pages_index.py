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
from copy import deepcopy
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
            assert all(
                n["type"] in {"text", "letter-small", "letter-large", "letter-hung"}
                for n in node["contents"]
            )
            return "".join(map(flatten, node["contents"]))
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
            {"type": "spi-pe2"},
            {"type": "spi-pe3"},
            {"type": "spi-samekh2"},
            {"type": "spi-samekh3"},
        )
        return " "

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
        if contents and contents[0].get("type") == "spi-invnun":
            assert contents[0] == {
                "type": "spi-invnun",
                "class": "including-trailing-space",
            }
            contents = contents[1:]
            assert contents
        source_text = (
            verse["text"] if "text" in verse else "".join(map(flatten, contents))
        )
        expected[int(c), int(v)] = tuple(
            letters
            for token in re.split(r"[\s־]+", source_text)
            if (letters := "".join(ch for ch in token if "א" <= ch <= "ת"))
        )
    return expected


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


def test_every_record_edge_resolves_to_its_observed_page():
    """Each handwritten source cue is an independent oracle for public lookup."""
    count = 0
    for edition in editions.ALL_EDITION_IDS:
        index = index_io.read_index(edition)
        for rec in index["recs"]:
            if rec["stopc"] is None:
                continue
            for end in ("start", "stop"):
                first, _ = text.locate_phrase_span(
                    text.book_atoms(rec["bkid"]),
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
