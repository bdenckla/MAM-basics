# Overall Plan: Port Accents to Python in Two Stages

## Objective
Create a Python implementation that first matches current Accents behavior, then evolves to a cleaner long-term architecture.

## Stage 1: Parity Baseline
Build a parity-focused Python port as the first milestone.

Outcome:
- A trustworthy baseline that reproduces current behavior for the target input scope.
- A stable reference point for later refactoring.

## Stage 2: Architectural Refactor
After parity is achieved and validated, refactor toward a hybrid architecture (custom tokenizer + Lark parser).

Outcome:
- Improved maintainability and readability.
- Better separation of concerns and easier future enhancements.

## Governance and Transition Rule
Proceed to Stage 2 only after Stage 1 is accepted as functionally equivalent for the agreed corpus and checks.

## Deliverables
- Stage 1 plan and implementation artifacts.
- Stage 2 refactor plan and implementation artifacts.
- Migration notes that explain equivalence assumptions and behavior boundaries.
