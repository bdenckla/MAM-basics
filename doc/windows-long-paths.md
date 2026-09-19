# Windows long paths

This guide records the present operating recommendation for Windows paths in
MAM-basics and related local workflows. This is documentation only: no registry,
Git configuration, public API, or runtime behavior change is in scope.

## Operating recommendation

Continue budgeting for short paths even if Windows long paths are enabled. Do
not make paths beyond the legacy limit a workflow requirement until every
external executable involved has passed disposable read/write tests with real
inputs and outputs both below and above that limit.

## Official documentation

Windows historically limits many paths to `MAX_PATH`, 260 characters including
the terminating null character. Microsoft documents two distinct mechanisms for
getting past that limit with absolute paths:

1. An application can pass an extended-length path in the `\\?\...` form to
   Unicode Windows API functions. Windows passes such a path with minimal
   modification and permits an approximate maximum of 32,767 characters. This
   mechanism requires neither `LongPathsEnabled` nor a `longPathAware`
   application manifest, and `LongPathsEnabled` adds no path-length capacity to
   it.
2. On Windows 10 version 1607 and later, many common Win32 functions can accept
   long paths without the `\\?\` prefix when `LongPathsEnabled` is `1` and the
   application manifest declares `longPathAware`. The registry setting alone
   does not make every application long-path aware.

See [Microsoft's long-path
requirements](https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation).

Python 3.6 and later can use extended paths when the Windows setting is enabled.
The Python documentation specifically names `open()`, `os`, and most other path
functionality. See [Python's Windows
guidance](https://docs.python.org/3.13/using/windows.html#removing-the-max-path-limitation).

Git for Windows `core.longpaths` uses the first mechanism: its C-based Git
commands convert long paths to the `\\?\...` form. That prefix-based handling
does not require `LongPathsEnabled` and does not benefit from enabling it. Git
for Windows warns that scripted Git commands can still fail even when
`core.longpaths` is enabled. See [Git for Windows on long
paths](https://gitforwindows.org/git-cannot-create-a-file-or-directory-with-a-long-path.html).

Codex-managed worktrees live under `$CODEX_HOME/worktrees` by default, although
the root can be changed in Codex settings. See the [official OpenAI worktree
documentation](https://developers.openai.com/es-419/docs/environments/git-worktrees).

## Local observations from 2026-09-19

The following are local measurements and observations, not general claims about
all Windows installations or tool versions.

### Machine settings

On 2026-09-19, both the original investigation and execution of this guide
measured:

- `LongPathsEnabled`: `0`.
- Effective Git `core.longpaths`: unset. `git config --show-origin --get-all
  core.longpaths` produced no output and exited with status 1.

Re-measure these values when this guide is used. If either value changes, retain
the 2026-09-19 observation above and record the newer dated measurement rather
than rewriting history.

```powershell
Get-ItemPropertyValue -Path 'HKLM:/SYSTEM/CurrentControlSet/Control/FileSystem' -Name LongPathsEnabled
```

```powershell
git config --show-origin --get-all core.longpaths
```

### Root lengths and observed failures

These root lengths were measured as written:

- `C:/Users/BenDe/.codex/visualizations/2026/09/02/01a063d6-69b4-7f70-a501-16056364e546`:
  84 characters.
- `C:/Users/BenDe/GitRepos/MAM-private/.claude/worktrees/dual-agent-review-2026-09-17`:
  82 characters.
- `C:/Users/BenDe/.codex/worktrees/XXXX/MAM-private`: 48 characters.

None of these roots alone caused the observed failures.

Synthetic retirement tests constructed 251-257-character destinations by
reproducing the source path beneath the retention root. The implementation
anchor is `_shadow_parts` in
[`py/repo_util/worktree_retirement.py`](../py/repo_util/worktree_retirement.py),
which turns the source's drive and absolute path components into the destination
shadow.

Two shorter test roots reduce recurrence in that test surface only:

- `_add_windows_basetemp` in
  [`py/main_test.py`](../py/main_test.py) supplies a short pytest base under
  `.novc/t` on Windows.
- `TemporaryDirectory(prefix="mam-retirement-")` in
  [`py/repo_util/worktree_retirement_simulation_test.py`](../py/repo_util/worktree_retirement_simulation_test.py)
  gives the retirement simulations a short temporary root.

Neither change establishes that the production workflow or its external tools
support paths beyond the legacy limit.

A separate Claude scratchpad Git clone used a 154-character base. The clone
failed when a pack `.keep` path reached 267 characters and succeeded after the
resulting path was shortened to 244 characters. The successful retry resulted
from shortening the path; `core.longpaths` was not used.

## Untested compatibility concerns

**Ben's concern, 2026-09-19:** enabling long paths may allow Python to create
paths that external executables cannot consume.

The local call sites establish that these external executables participate in
the workflows:

- MAM-basics invokes Graphviz `dot.exe` through `subprocess.run` in
  [`py/mb_cmn/graphviz_pin.py`](../py/mb_cmn/graphviz_pin.py).
- hbofonts invokes FontForge through
  `C:/Users/BenDe/GitRepos/hbofonts/ps1_ffscript_generate_sfd_n_ttf_solo.ps1`.
- hbofonts invokes Tidy's `tidy.exe` through
  `C:/Users/BenDe/GitRepos/hbofonts/ps1_html_tidy.ps1`.
- hbofonts invokes HarfBuzz's `hb-view.exe` and `hb-shape.exe` through
  `C:/Users/BenDe/GitRepos/hbofonts/ps1_run_hb_view_on_examples_using_my_font.ps1`
  and
  `C:/Users/BenDe/GitRepos/hbofonts/ps1_run_hb_view_on_examples_using_not_my_font.ps1`.

Graphviz, FontForge, Tidy, and HarfBuzz compatibility above the legacy limit is
unverified: none of these tools is known here either to work or to fail there.
Git's one observed failure and success establish only the tested paths and
configuration, not a general boundary for every Git operation.

## Future disposable probes

Do not perform these probes in a live checkout. A future investigation should
use disposable directories and construct paired full paths clearly below and
above the legacy limit, such as the already observed 244- and 267-character
paths. For each pair, record the complete path, its measured character count,
tool version, command, exit status, and whether input and output bytes were
usable afterward.

1. Use Python to create and verify the same real input files at both lengths.
2. Exercise `git.exe` with a disposable clone or fetch that writes checkout and
   pack paths at both lengths, then read the resulting repository with Git.
3. Exercise Graphviz `dot.exe` with a real DOT input path and SVG output path at
   both lengths, then parse or compare the SVG.
4. Exercise FontForge through the hbofonts wrapper with disposable SFD and
   feature inputs and disposable SFD, TTF, WOFF, and WOFF2 outputs at both
   lengths, then reopen the generated fonts.
5. Exercise Tidy `tidy.exe` with real HTML input and output paths at both
   lengths, then read and validate the output.
6. Exercise HarfBuzz `hb-view.exe` and `hb-shape.exe` with real font and text
   inputs and SVG and trace outputs at both lengths, then read the outputs.

Only results from those executable-specific read/write probes can retire the
corresponding compatibility concern.
