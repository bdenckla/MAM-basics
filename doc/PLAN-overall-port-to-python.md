# Overall Plan: Port Accents to Python in Two Stages

## Objective
Create a Python implementation that first matches current Accents behavior, then
evolves to a cleaner long-term architecture. The work covers **both** accent
systems:
- **Prose** — the port of `acc2tre.y` (the 21-book prose accents).
- **Poetic** — the Sifrei Emet (Psalms, Proverbs, Job) checker, built fresh in
  Python with no C predecessor.

Both grammars move through the same two stages, and Stage 2 is done for both at
once.

## Stage 1: Parity Baseline — ACHIEVED
A parity-focused Python port as the first milestone.

Status:
- **Prose: done.** `py/accgram/ply_grammar.py` is a faithful one-to-one PLY port
  of `acc2tre.y`, including yacc-style `error`-token recovery that reproduces the
  ERROR-node ungrammatical trees.
- **Poetic: done, and past bare parity.** The PLY grammar/scanner (Phases 1–4)
  reproduces the expected trees and adds capabilities the C program never had —
  a lexical-validation layer, MAM cross-checks, ungrammatical-verse flagging, and the Breuer
  servant rules.

Outcome:
- A trustworthy baseline that reproduces current behavior for the target input
  scope.
- A stable reference point for later refactoring.

## Stage 2: Architectural Refactor — REMAINING WORK
After parity is achieved and validated, refactor toward a hybrid architecture
(custom tokenizer + Lark parser) for both prose and poetic grammars together.

Scope notes:
- The existing custom scanners (`ply_scanner.py`, the poetic scanner) carry over;
  Lark consumes their token streams.
- Lark's declarative EBNF (with `*`/`+` repetition) collapses the hand-unrolled
  servus sequences and separates grammar from tree-building (done in a
  Transformer), directly serving the maintainability goal.
- The hard, parity-critical part is reproducing yacc's `error`-token recovery —
  which has no direct Lark equivalent — so the ERROR-node trees still match
  byte-for-byte.

Outcome:
- Improved maintainability and readability.
- Better separation of concerns and easier future enhancements.

## Governance and Transition Rule
Proceed to Stage 2 only after Stage 1 is accepted as functionally equivalent for
the agreed corpus and checks. (Stage 1 is now accepted for both grammars.)

## Deliverables
- Stage 1 plan and implementation artifacts. (Complete.)
- Stage 2 refactor plan and implementation artifacts.
- Migration notes that explain equivalence assumptions and behavior boundaries.
