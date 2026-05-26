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
