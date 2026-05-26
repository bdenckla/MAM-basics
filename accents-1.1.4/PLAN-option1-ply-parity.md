# Stage 1 Specific Plan: PLY Parity Port

This document describes Stage 1 only. It is intentionally detailed because it is the first part of a larger overall plan in which Stage 2 performs a later architectural refactor.

## Goal
Implement a Python port of Accents using PLY (lex + yacc style) with behavior parity as the primary requirement.

## Scope
- Input scope: the new format (such as Obad.new).
- Functional target: match current parsing outcomes, error signaling, and tree structure behavior for the agreed corpus.
- Non-goal for Stage 1: architectural cleanup beyond what is needed for parity.

## Work Breakdown
1. Baseline and fixtures
- Capture representative input fixtures from the new format corpus.
- Define expected outputs and error cases from the current implementation.
- Freeze a parity corpus to avoid moving-target comparisons.

2. Token model definition
- Define Python token names matching current parser expectations.
- Preserve token semantics needed by grammar actions.
- Document token categories and special-case tokens.

3. Lexer port in PLY
- Port lexer state-machine behavior for new format processing.
- Port key right-context and lookahead-sensitive rules.
- Preserve special-case logic (including location-aware exceptions such as legarmeh handling).

4. Grammar port in PLY
- Translate yacc productions to PLY grammar rules.
- Preserve precedence, recovery paths, and error productions.
- Keep node labels and composition logic compatible with current tree output.

5. Tree and utility layer
- Recreate minimal node utilities needed by grammar actions.
- Preserve display-oriented structure needed for parity checks.
- Keep API simple and internal to Stage 1.

6. CLI wrapper
- Provide a Python entry point with Stage 1-compatible behavior for target use.
- Include options needed for parity verification (including tree display mode).

7. Verification
- Run corpus comparisons against current implementation.
- Compare pass/fail status per verse and tree-shape expectations for selected fixtures.
- Record mismatches and resolve until acceptance threshold is met.

8. Hardening
- Add regression tests for each resolved mismatch class.
- Add basic documentation for running parity checks.
- Mark known limitations explicitly.

## Progress Tracking
Use this file as the canonical progress record for Stage 1.

Status labels:
- Not started
- In progress
- Blocked
- Done

Cadence:
- Update this section each time a meaningful task lands.
- Keep entries factual and short: date, change, evidence, next step.

### Stage 1 Status Board
- 1. Baseline and fixtures: In progress
- 2. Token model definition: Not started
- 3. Lexer port in PLY: Not started
- 4. Grammar port in PLY: Not started
- 5. Tree and utility layer: Not started
- 6. CLI wrapper: In progress
- 7. Verification: In progress
- 8. Hardening: In progress

### Progress Log
- 2026-05-26: Added Python CLI entry point py/main_accgram.py with subcommand split-wlc to split wlc422_ps.txt into per-book fixtures under .novc/wlc_422_ps using wlc_422_ps_bb.txt naming. Evidence: command run succeeded with 39 books and 23213 verse lines written. Next: define baseline output generation flow per split book to allow incremental parity captures.
- 2026-05-26: Added py/main_accgram.py subcommand filter-split-wlc to write filtered fixtures under .novc/wlc_422_psf. Evidence: command run succeeded with 37 output files and 18723 verse lines; Psalms and Proverbs files are absent; gn35:22, ex20:2-13, and dt5:6-17 are excluded; for Job, prose ranges jb1:1-3:1 and jb42:7-42:17 remain while the poetic block jb3:2-42:6 is excluded. Next: use filtered fixtures as Stage 1 default corpus for parity-focused parser bring-up.
- 2026-05-26: Addendum to prior filter-split-wlc entry: dual-cantillation exclusion intent for Exodus 20 and Deuteronomy 5 is reckoned in WLC/BHS versification; implementation was corrected to map WLC refs to MAM locales before dual-cantillation checks. Evidence: command run succeeded with 37 output files; BHS-numbered exclusions now include gn35:22, ex20:2-17, and dt5:6-21; verses excluded now report 4498. Next: use filtered fixtures as Stage 1 default corpus for parity-focused parser bring-up.
- 2026-05-26: Added and wired run-orig flow in py/main_accgram.py (subcommand run-orig) with accgram.run_orig defaults for filtered inputs and out/accgram/orig + out/accgram/orig-stderr outputs. Evidence: artifact counts are aligned (37 filtered inputs, 37 *_ag outputs, 37 stderr sidecars). Next: use these outputs as the Stage 1 baseline oracle while PLY port work is still pending.
- 2026-05-26: Added Stage 1 hardening tests for current harness behavior in py/tests/test_accgram_filter_split_wlc.py and py/tests/test_accgram_run_orig.py. Evidence: .venv/Scripts/python.exe py/main_test.py --accgram-filter-split-wlc --accgram-run-orig reports "Ran 5 tests" and "OK" (exit code 0). Next: extend tests to cover known mismatch classes discovered during corpus comparison.
- 2026-05-26: Ran verification snapshot for Obadiah in run-orig outputs. Evidence: out/accgram/orig/wlc_422_ps_ob_ag.txt exists (414 lines) and out/accgram/orig-stderr/wlc_422_ps_ob_ag.stderr.txt reports repeated Obadiah 1:2 errors including "verse is missing sof pasuq"; generated tree starts at Obadiah 1:2 while accents-1.1.4/Obad.new.data starts at Obadiah 1:1. Next: normalize/validate sof-pasuq handling in split input generation and re-run Obadiah parity comparison.

## Acceptance Criteria
- The Stage 1 parity corpus produces equivalent parse success/error outcomes.
- Selected tree outputs match expected structure for representative verses.
- Special-case behaviors are covered by explicit regression tests.
- Remaining differences, if any, are documented and accepted.

## Risks and Mitigations
- Risk: subtle lexer context differences.
  Mitigation: fixture-driven tests around boundary patterns and right-context rules.

- Risk: error recovery divergence.
  Mitigation: explicit tests for malformed verses and missing-marker cases.

- Risk: hidden dependency on C implementation quirks.
  Mitigation: treat current behavior as the oracle and add focused golden tests.

## Exit Criteria for Stage 1
Stage 1 is complete when parity acceptance criteria are met and documented, enabling transition to Stage 2 refactor work under the overall plan.
