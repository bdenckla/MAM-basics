# Agent Planning Principles

These principles capture planning preferences for AI coding agents working in this repository.

## Generated Outputs Are the Tests

For workflows whose important behavior is expressed through generated, git-tracked artifacts, do not add test files or test cases unless explicitly requested.

Instead, use the generated outputs as the verification surface:

- Regenerate the relevant JSON and HTML artifacts with the real CLI command.
- Inspect the generated output files for expected changes.
- Confirm that files expected to remain unchanged do remain unchanged, aside from normal generated metadata if applicable.
- Treat unexpected diffs in generated JSON or HTML as test failures until explained.

In these workflows, examining the generated HTML and JSON is the test.

### The two shapes of test that have earned their place

An audit of git history, code comments, and issues across all of Ben's repos (2026-07-25) found four occasions where a test demonstrably found something, and **zero** recorded cases of a pre-existing example-based unit test failing later and thereby catching a regression. All four have one of two shapes. If a proposed test is neither shape, do not write it.

**1. A differential check against an independent oracle.** Regenerate the whole corpus and compare it against a frozen reference, or against a second derivation of the same fact.

- The PLY parity comparator against the frozen Goerwitz C checker (Phases A–F, `51e2748`..`cda21f9`). It did not merely confirm the port; the parity number *was* the completion criterion, climbing 0/18666 → 14/20 Obadiah → 37 books → 18,666/18,666 byte-identical.
- The Decalogue transcription checks against the vendored strands: `ee21ebb` found a real qadma-for-pashta divergence in the Simanim Tanakh, `80ca0df` found the first Koren page to diverge from its strand.
- In a MAM-private project, `efa95ccf`: a self-test reconstructing each verse's visible text from that project's emitted JSON and comparing it against the project's own input caught that paseq was being silently dropped in 8 verses across 5 chapters (private annex §5).

**2. A mechanical lint over the tree.** A decidable property of the *source text*, not of behavior. `py/tests/test_transliterations.py` (issue #26) is the working example; `9c95cf9` fixed a `tarkha`→`tarxa` and a kh-for-ḥet gap that it exposed.

### What not to write

Do not write an example-based unit test that pins one hand-picked case, a string, or a name. Two reasons, both from the record:

- No such test in this repo is recorded as ever having caught anything.
- They are pure carrying cost. 253 of 807 commits touch `py/tests`, and much of that is the suite being dragged through terminology sweeps it does not police: `simanim_*`→`simtiq_*`, the `ws/` strand prefix, "oddball"→ungrammatical, the meteg standardization.

Bear in mind that no CI runs pytest here — `pages.yml` is a Pages deploy that never invokes it. A suite that runs only when someone chooses to run it earns its keep by finding something *when it is written*, not by standing guard afterward.

### A missing input must fail, never skip

`25a7800` deleted twenty-one guards that skipped when an input was absent, each reporting green having verified nothing. Skips are a **semantic** channel in this suite — the one remaining site reports that a page diverges from its strand — so environment skips mixed in make that list unreadable. An empty `@parametrize` list is itself reported as a skip, which is why the `or ["(none committed)"]` fallbacks exist and must stay.

### Do not enforce this rule mechanically

Resist turning this into a gate (a `check_repo_standards.py` rule, a meta-test). "Is this test example-based?" is not decidable, and issue #27 → #49 is the cautionary tale: a guard test faithfully enforced decomposed ḥ across 21 files until the policy reversed to NFC, at which point the enforcement made the reversal more expensive rather than cheaper. This is advice a reviewer can override.

## Prefer New Files For New Features

Implement new features in new focused modules/files as much as practical.

Prefer small, purpose-named modules for new feature areas rather than swelling existing large files. Existing files should usually receive only the wiring, reuse hooks, and documentation needed to connect the new behavior to the established workflow.

This keeps review simpler and makes it easier to abandon, revise, or phase in new behavior without disturbing mature code paths.

## Size Phases to Natural Boundaries

Size phases to coherent goals and natural verification points, not to any model's context limit. A capable agent can take on a large phase in one session, so do not pre-fragment work to fit a smaller executor; combine steps that share a goal and a verification point.

A good phase should have:

- A coherent implementation goal.
- A natural verification point.
- A clear handoff boundary to the next phase.

Limited blast radius and fresh-session executability are virtues, but they follow from a coherent goal rather than from an imposed size budget. Do not make every mechanical step its own phase. For example, styling and docs are often too small to be standalone phases; they usually belong with the functional work they support. Conversely, a risky refactor that preserves existing behavior may deserve its own phase before new behavior is added.

## Write State Back Before Continuing

At the end of each phase, write the current state back into the plan before proceeding.

The phase-end update should include:

- What changed.
- What verification was run.
- What generated outputs changed or intentionally did not change.
- Any unexpected findings or unresolved risks.
- The exact next phase to execute.

After writing the phase state back, compact the conversation context before continuing. This acts as a poor man's fresh session: the next phase starts with a short, current plan rather than stale conversational residue.

## Keep Verification Close To The Workflow

Prefer real workflow commands over narrow synthetic checks. For generated-output workflows, the primary verification should be the same CLI command a maintainer would run to refresh the artifacts.

If a smaller local invocation is useful inside an intermediate phase, use it only as provisional verification. The final phase should still run the real regeneration command and inspect the resulting tracked artifacts.
