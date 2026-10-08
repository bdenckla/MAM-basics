"""Build the near-Aleppo dataset from local MAM-parsed-plus and stored pointings.

The pipeline resolves E-column templates, applies representation policies and
readings quoted in MAM's notes, then adds frozen, individual and reviewed
pointings in that priority order. Each stored pointing records the ketiv and qere
it was made for, and the build stops, naming the record, where the template no
longer has them. Original MAM targets are copied into changed notes before flags and
reviewed note-content baking. C and D columns are preserved. Changed notes carry
reviewed near-Aleppo clauses and the remaining original clauses in MAM context.

Every book is built and checked in memory before any output is written. The
counts that the local census also reports must agree with it
(build_expectations.py). The build then writes its counts, with the verses where
it recorded them, to in/near-aleppo/build-populations.json beside the dataset, so
that their diff shows what a change moved; no count or site there is pinned.

Use py/main_near_aleppo.py --build, or add --check to compare the 24 book files
under out/near-aleppo/plus and the population file without writing.
"""

import argparse
import copy
import json
import sys

from mb_cmn import bib_locales as tbn
from near_aleppo import build_paths
from near_aleppo import build_expectations
from near_aleppo import consumer_notice
from near_aleppo import ketiv_checks
from near_aleppo.phase2_templates import Resolver
from near_aleppo.phase2_templates import assert_templates_absent
from near_aleppo.phase3_policies import Policies
from near_aleppo.phase5_readings import Readings
from near_aleppo.phase6_flags import Flags
from near_aleppo.phase6_mam_targets import MAM_TARGET_PARAMETER
from near_aleppo.phase6_mam_targets import MamTargets
from near_aleppo.phase6_rename import Renames
from near_aleppo.frozen_ketiv import FrozenPointing
from near_aleppo.editorial_ketiv import EditorialPointing
from near_aleppo.reviewed_ketiv import ReviewedPointing

# The stem of each of MAM-parsed-plus's 24 book files.
_BOOK_STEMS = frozenset(tbn.ordered_short_dash_full_24(b) for b in tbn.ALL_BK24_IDS)


def build(bake_notes=True):
    """Return the serialized dataset and the population-recording build state."""
    if bake_notes:
        from near_aleppo import doc_note_review
        from near_aleppo.note_content import NoteContent

        notes = NoteContent(doc_note_review.check())
    in_dir = build_paths.mam_parsed_plus_dir()
    paths = sorted(in_dir.glob("*.json"))
    stems = {path.stem for path in paths}
    if stems != _BOOK_STEMS:
        raise AssertionError(
            f"{in_dir}: books missing {sorted(_BOOK_STEMS - stems)}, unknown files "
            f"{sorted(stems - _BOOK_STEMS)}"
        )
    resolver = Resolver()
    policies = Policies()
    readings = Readings()
    mam_targets = MamTargets()
    flags = Flags()
    renames = Renames(source_replay=not bake_notes)
    frozen = FrozenPointing()
    editorial = EditorialPointing()
    reviewed = ReviewedPointing()
    out = {}
    for path in paths:
        book = json.loads(path.read_text(encoding="utf-8"))
        # Each verse's cells with its name, for the rename below.
        book_verses = []
        for book39 in book["book39s"]:
            # A verse is named (book, chapter, verse), the book being the file's
            # stem, followed in a file of several books by the sub-book's name:
            # ('BA-Samuel שמ"א', "15", "1") is 1 Samuel 15:1.
            book_name = path.stem
            if book39["sub_book_name"] is not None:
                book_name += " " + book39["sub_book_name"]
            for chapter, chapter_verses in book39["chapters"].items():
                for verse, cells in chapter_verses.items():
                    if len(cells) != 3:
                        raise AssertionError(
                            f"{path.name} {chapter}:{verse} has {len(cells)} cells, not 3"
                        )
                    ref = (book_name, chapter, verse)
                    mam_cell = copy.deepcopy(cells[2])
                    resolved = resolver.resolve_e_cell(cells[2], ref)
                    cells[2] = policies.apply_e_cell(resolved, ref)
                    cells[2] = readings.apply_e_cell(cells[2], ref)
                    flag_evidence = (
                        copy.deepcopy(cells[2])
                        if frozen.by_verse.get(ref)
                        or editorial.by_verse.get(ref)
                        or reviewed.by_verse.get(ref)
                        else None
                    )
                    cells[2] = frozen.apply(cells[2], ref)
                    cells[2] = editorial.apply(cells[2], ref)
                    cells[2] = reviewed.apply(cells[2], ref)
                    ketiv_checks.check_e_cell(cells[2], ref)
                    # MAM-target copying follows the last Scripture-reading change. The
                    # flags step after it adds parameters only, none inside a
                    # note's target, and the rename after the verse loop changes
                    # only the names of notes.
                    mam_targets.add_to_e_cell(mam_cell, cells[2], ref)
                    flags.add_to_e_cell(cells[2], ref, evidence_cell=flag_evidence)
                    book_verses.append((cells, ref))
        assert_templates_absent(book, path.name, MAM_TARGET_PARAMETER)
        # Rename after assert_templates_absent, which knows MAM's note names,
        # then bake reviewed content. Both preserve Scripture readings.
        for cells, ref in book_verses:
            renames.rename_e_cell(cells[2], ref)
            if bake_notes:
                notes.apply(cells[2], ref)
        consumer_notice.set_in_header(book["header"], path.name)
        text = json.dumps(book, indent=2, ensure_ascii=False) + "\n"
        out[path.name] = text.encode("utf-8")
    frozen.finish()
    editorial.finish()
    reviewed.finish()
    if bake_notes:
        notes.finish()
    return out, resolver, policies, readings, mam_targets, flags, renames


def write(dataset, populations):
    """Write the dataset's book files, then ``populations``, the population file."""
    out_dir = build_paths.dataset_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    extra = sorted(p.name for p in out_dir.iterdir() if p.name not in dataset)
    if extra:
        raise AssertionError(f"Unexpected files in {out_dir}: {extra}")
    for name, data in dataset.items():
        (out_dir / name).write_bytes(data)
    print(f"Wrote {len(dataset)} files to {out_dir}")
    build_expectations.write(populations)


def check(dataset, populations):
    """Compare the dataset and ``populations`` with the tracked files."""
    out_dir = build_paths.dataset_dir()
    problems = []
    for name, data in dataset.items():
        path = out_dir / name
        if not path.exists():
            problems.append(f"missing {name}")
        elif path.read_bytes() != data:
            problems.append(f"differs {name}")
    if out_dir.is_dir():
        problems += [
            f"unexpected {p.name}"
            for p in sorted(out_dir.iterdir())
            if p.name not in dataset
        ]
    populations_path = build_expectations.POPULATIONS_PATH
    if not populations_path.exists():
        problems.append(f"missing {populations_path}")
    elif populations_path.read_bytes() != populations.encode("utf-8"):
        problems.append(f"differs {populations_path}")
    if problems:
        print(f"The dataset in {out_dir} or its population file is not current:")
        for problem in problems:
            print(f"  {problem}")
        return 1
    print(
        f"The dataset in {out_dir} is current ({len(dataset)} files), "
        f"and so is {populations_path.name}"
    )
    return 0


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help=(
            "Rebuild in memory and compare with the tracked dataset and population "
            "file; write nothing."
        ),
    )
    args = parser.parse_args(argv)

    dataset, resolver, policies, readings, mam_targets, flags, renames = build()
    build_expectations.assert_census_agrees(resolver, policies, readings, mam_targets)
    renames.assert_expected_counts(mam_targets.counts)
    populations = build_expectations.render(
        resolver, policies, readings, mam_targets, flags
    )
    if args.check:
        return check(dataset, populations)
    write(dataset, populations)
