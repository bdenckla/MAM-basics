"""Lint: the English introduction's section map matches both mirrors.

``in/mam-ws-intro-en-section-map.json`` names each section of the English mirror,
``in/mam-ws-intro-en/``, and the sections of the Hebrew mirror, ``in/mam-ws-intro/``, that
it translates, by their headings, as ``py/ws/ws_intro_en_section_map.py`` reads them.  A
heading renamed or removed on either wiki reaches this repository as a refresh of its
mirror, and this lint then fails until the map follows, as Phase 6, step 1, of
``doc/PLAN-english-intro.md`` asks:

1. The map's entries for each English page with text are its lead and each of its
   headings, in page order: none missing, none extra, none renamed.
2. Each Hebrew counterpart's heading is on its page of the Hebrew mirror exactly once.  The
   map holds Hebrew in MAM's mark order, so it is compared with ``give_std_mark_order`` of
   the heading that the mirror, a capture in Unicode's order, shows.
3. Each evaluation slice that an entry cites is a slice of the evaluation the map names.
4. The whole map is in MAM's mark order, its notes included.

A missing map, mirror page or evaluation fails rather than skips.  The negative control
of 2026-11-22, a scratch script, ran these tests over a scratch copy of both mirrors and
the map: the unchanged copy passed, and a copy with one Hebrew heading renamed, and then
one with one English heading renamed, each failed, naming the heading.  The plan's Phase 6
record gives the details.
"""

import difflib
import re

from mb_cmn import paths
from mb_cmn import uni_denorm
from subcommands import download_wikisource_intro
from subcommands import download_wikisource_intro_en
from ws import ws_intro_en_section_map as section_map


def test_every_english_section_is_mapped_in_page_order():
    the_map = section_map.load()
    text_slugs = download_wikisource_intro_en.text_slugs()
    assert list(the_map.pages) == text_slugs, (
        "The map's English pages must be the English mirror's pages with text, in"
        " their declared order.",
        list(the_map.pages),
        text_slugs,
    )
    mismatches = []
    for slug in text_slugs:
        wikitext = _read(download_wikisource_intro_en.page_path(slug))
        mirrored = [section.heading for section in section_map.sections(wikitext)]
        mapped = [entry.english for entry in the_map.pages[slug]]
        if mapped != mirrored:
            mismatches.append(_mismatch(slug, mapped, mirrored))
    assert not mismatches, (
        "The section map's English entries are not the English mirror's sections (a"
        " leading - is only in the map, a leading + only in the mirror, None the lead)."
        " Update in/mam-ws-intro-en-section-map.json as in/mam-ws-intro-en/README.md,"
        " The section map, says.",
        mismatches,
    )


def test_every_hebrew_counterpart_is_on_its_page_once():
    the_map = section_map.load()
    page_sections = {}
    problems = []
    checked = 0
    for slug, entries in the_map.pages.items():
        for entry in entries:
            for counterpart in entry.hebrew:
                if counterpart.page not in page_sections:
                    page_path = download_wikisource_intro.page_path(counterpart.page)
                    page_sections[counterpart.page] = section_map.sections(
                        _read(page_path)
                    )
                count = sum(
                    section.heading == counterpart.heading
                    for section in page_sections[counterpart.page]
                )
                checked += 1
                if count != 1:
                    problems.append(
                        f"{slug} {entry.english!r} <- {counterpart.page}"
                        f" {counterpart.heading!r}: on its page {count} times"
                    )
    assert checked, "The section map names no Hebrew counterpart at all."
    assert not problems, (
        "A Hebrew heading that the section map names is not on its page of the Hebrew"
        " mirror exactly once. Update in/mam-ws-intro-en-section-map.json as"
        " in/mam-ws-intro-en/README.md, The section map, says.",
        problems,
    )


def test_every_cited_evaluation_slice_is_in_the_evaluation():
    the_map = section_map.load()
    evaluation = _read(paths.repo_root() / the_map.evaluation)
    slices = set(_SLICE_HEADING.findall(evaluation))
    assert slices, f"{the_map.evaluation} has no slice headings"
    cited = {
        slice_name
        for entries in the_map.pages.values()
        for entry in entries
        for slice_name in entry.evaluation_slices
    }
    assert cited <= slices, (
        f"The section map cites slices that {the_map.evaluation} does not have.",
        sorted(cited - slices),
    )


def test_the_map_is_in_mam_mark_order():
    text = _read(section_map.map_path())
    assert uni_denorm.has_std_mark_order(text), (
        "in/mam-ws-intro-en-section-map.json holds Hebrew out of MAM's mark order. Copy"
        " each heading from the mirror through uni_denorm.give_std_mark_order, by"
        " script, as in/mam-ws-intro-en/README.md, The section map, says."
    )


def _read(path):
    with open(path, "r", encoding="utf-8", newline="") as text_fp:
        return text_fp.read()


def _mismatch(slug, mapped, mirrored):
    lines = difflib.ndiff([repr(h) for h in mapped], [repr(h) for h in mirrored])
    return f"{slug}: " + "; ".join(line for line in lines if line[:1] in "-+")


_SLICE_HEADING = re.compile(r"^## ([a-z0-9-]+): ", re.MULTILINE)
