# Obad Output Difference Handoff (2026-05-26)

## Problem Statement
When running `accents -p` on the Obadiah input produced by MAM-basics split/filter flow, Obadiah parse output differs from reference output derived from `Obad.new`.

Observed mismatch in generated `.data`-style output:
- Generated output is missing `Obadiah 1:1`.
- Generated output is missing `Obadiah 1:3`.
- Output starts with `Obadiah 1:2`, then continues with `Obadiah 1:4+` in normal order.
- Stderr contains repeated parser warnings referencing `Obadiah 1:2`.

## Scope / Working Assumption
Treat question-mark differences as a red herring for this investigation.

Working assumption for next session:
- `?` markers are line-end markers in the source encoding and are likely ignored by `accents` parsing behavior.
- Therefore, Obad behavior difference between the two inputs is likely caused by other token/content differences, not by `?` differences.

## Inputs and Outputs Involved
Reference input/output:
- `accents-1.1.4/Obad.new`
- `accents-1.1.4/Obad.new.data`

MAM-basics split/filter input and run-orig outputs:
- `../wlc-utils-io/out/goerwitz/wlc_422_psf/wlc_422_ps_ob.txt`
- `out/accgram/orig/wlc_422_ps_ob_ag.txt`
- `out/accgram/orig-stderr/wlc_422_ps_ob_ag.stderr.txt`

Useful temporary comparison artifact:
- `.novc/Obad.new.unwrapped.txt` (one-line-per-verse version of `Obad.new`)

## Reproduction Commands (PowerShell from MAM-basics repo root)
Regenerate split/filter corpus:

```powershell
.venv/Scripts/python.exe py/main_accgram.py filter-split-wlc
```

Regenerate original accents outputs:

```powershell
.venv/Scripts/python.exe py/main_accgram.py run-orig
```

Directly run accents on Obad split file:

```powershell
wsl bash -lc '/mnt/c/Users/BenDe/GitRepos/MAM-basics/accents-1.1.4/accents -p < /mnt/c/Users/BenDe/GitRepos/wlc-utils-io/out/goerwitz/wlc_422_psf/wlc_422_ps_ob.txt' \
  1> .novc/wlc_422_ps_ob_ag.rerun.txt \
  2> .novc/wlc_422_ps_ob_ag.rerun.stderr.txt
```

## Key Observations Already Established
1. Running `accents -p` on `../wlc-utils-io/out/goerwitz/wlc_422_psf/wlc_422_ps_ob.txt` reproduces the same Obad output shape and same warning pattern seen in `out/accgram/orig/*`.
2. `out/accgram/orig-stderr/wlc_422_ps_ob_ag.stderr.txt` contains warnings such as:
   - `verse is missing sof pasuq, Obadiah 1:2`
   - repeated `general parsing error Obadiah 1:2`
3. Generated headings vs reference headings:
   - Generated: `1:2, 1:4, 1:5, ...`
   - Reference: `1:1, 1:2, 1:3, 1:4, ...`
   - Missing in generated: `1:1`, `1:3`
4. From `1:4` onward, heading order appears aligned.
5. Current investigation direction: ignore `?` as causal and focus on non-`?` token differences around Obadiah 1:2.

## What Was Tried and Should Not Be Re-litigated First
- Adjusting split normalization around terminal `?` did not resolve the Obad output mismatch.
- The mismatch persisted after regenerating split/filter artifacts and rerunning `run-orig`.

## Recommended Next Investigation Steps
1. Do a token-by-token diff for Obadiah `1:2` between:
   - `.novc/Obad.new.unwrapped.txt`
   - `../wlc-utils-io/out/goerwitz/wlc_422_psf/wlc_422_ps_ob.txt`
2. Identify first parser-sensitive divergence (non-`?`), including punctuation/sign characters and bracket/note artifacts.
3. Minimize to a smallest failing input snippet for `accents -p` that reproduces the 1:2 warnings.
4. Compare with smallest passing snippet from `Obad.new` for the same verse.
5. Only after identifying concrete offending token(s), decide whether fix belongs in:
   - WLC preprocessing/normalization in MAM-basics, or
   - parser behavior/expectations in `accents`.

## Handoff Goal for Fresh Session
Find the exact non-`?` content difference in Obadiah 1:2 that triggers the `yyparse` warnings and causes missing `1:1`/`1:3` in generated parse output.

## Follow-up Findings (same date, later session)

### 1) Square-bracket note hypothesis was tested directly
- `Obad.new` does contain square-bracket notes (for example `]1`, `]3`).
- The WLC split Obad file contains alpha-style bracket tails (for example `]Q]c]n`, `]U`, `]C]c`).
- Controlled WLC mutations were run with `accents -p`:
   - Replace all `]alpha` groups with `]1`.
   - Remove all `]alpha` groups.
   - Remove all `]` characters.
- Result: all three mutated WLC variants still failed with the same signature:
   - first heading `Obadiah 1:2`
   - `Obadiah 1:3` missing
   - repeated `yyparse` warnings at `Obadiah 1:2`

Conclusion: square-bracket note fragments are not the root cause.

### 2) A single token mutation in Obadiah 1:1 reproduces the failure
Using clean `Obad.new` as baseline (`O0`), one first-occurrence token mutation at Obadiah 1:1 was tested:

- Baseline token fragment: `(FLE73Y/HF`
- Failing mutation (`O1`): `(FLEY/HF]Q]c]n`

`O1` reproduces the WLC failure signature exactly:
- output starts at `Obadiah 1:2`
- `Obadiah 1:3` missing
- warnings: `verse is missing sof pasuq, Obadiah 1:2` and repeated `general parsing error Obadiah 1:2`

### 3) Isolated causality: missing `73` is the parser-sensitive change
Additional controlled variants from `Obad.new`:

- `O2` (drop `73` only): `(FLEY/HF`
- `O3` (keep `73`, add note tails only): `(FLE73Y/HF]Q]c]n`
- `O4` (drop `73`, add `]1`): `(FLEY/HF]1`
- `O5` (drop `73`, add `]Qcn`): `(FLEY/HF]Qcn`

Results:
- `O2`, `O4`, `O5` all fail with the same `1:2` warning signature.
- `O3` passes (same as baseline `O0`).

Conclusion: removing the numeric marker `73` from that Obadiah 1:1 token is sufficient to trigger the downstream parse break; bracket-note suffixes are not sufficient when `73` is preserved.

### 4) Practical implication for preprocessing
The key normalization target is not `?` and not bracket notes; it is preserving parser-significant numeric markup within transliteration tokens (specifically this observed `73` case in Obadiah 1:1).

### 5) Important experiment hygiene note
`accents` behavior is newline-sensitive in these tests. Mutation files must preserve LF line endings (`\n`) to avoid false negative runs.
