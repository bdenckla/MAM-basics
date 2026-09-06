"""
Stats reporter and consistency checker for line-break JSON files.

Checks each file in line-breaks/*.json for structural
consistency and reports summary statistics.

Usage:
    .venv/Scripts/python.exe py/main_ac_check_line_breaks.py          # check all files
    .venv/Scripts/python.exe py/main_ac_check_line_breaks.py 270v      # check one file
"""

import json
import sys
import webbrowser
from collections import Counter

import ac_paths
from py_ac_loc.gen_flat_stream import (
    build_flat_stream,
    get_page_verses,
)
from py_cam1753_word_image.hebrew_metrics import no_marks_comparison_key

LB_DIR = ac_paths.line_breaks_dir()

EXPECTED_LINES_PER_COL = 28

# The directory holds two distinct, internally contiguous capture runs.  They
# must not be joined into one MAM-simple comparison: the MAM verses between
# Deut 34 and Ps 149 do not occur in either JSON run.
WORD_SEQUENCE_RUNS = (
    (
        "Deuteronomy pages 001r-006r",
        (
            "001r",
            "001v",
            "002r",
            "002v",
            "003r",
            "003v",
            "004r",
            "004v",
            "005r",
            "005v",
            "006r",
        ),
    ),
    (
        "Aleppo leaf run 270r-281v",
        (
            "270r",
            "270v",
            "271r",
            "271v",
            "272r",
            "272v",
            "273r",
            "273v",
            "274r",
            "274v",
            "275r",
            "275v",
            "276r",
            "276v",
            "277r",
            "277v",
            "278r",
            "278v",
            "279r",
            "279v",
            "280r",
            "280v",
            "281r",
            "281v",
        ),
    ),
)


def load_stream(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _parse_verse_label(label):
    """Parse 'Job 38:31' into ['Job', 38, 31]."""
    parts = label.split(" ", 1)
    book = parts[0]
    cv = parts[1].split(":")
    return [book, int(cv[0]), int(cv[1])]


def _first_verse_ref(path):
    """Extract the first verse reference from a line-break file.

    Returns [book, ch, vs] or None.
    """
    stream = load_stream(path)
    for item in stream:
        if isinstance(item, dict):
            for key in ("verse-start", "verse-fragment-start"):
                if key in item:
                    return _parse_verse_label(item[key])
    return None


def _last_verse_ref(path):
    """Extract the last verse reference from a line-break file.

    Returns [book, ch, vs] or None.
    """
    stream = load_stream(path)
    for item in reversed(stream):
        if isinstance(item, dict):
            for key in ("verse-end", "verse-fragment-end"):
                if key in item:
                    return _parse_verse_label(item[key])
    return None


def word_sequence_runs(paths):
    """Return selected paths partitioned into their declared text runs.

    The expected MAM-simple stream is contiguous only within each run.  New
    line-break JSON requires an explicit entry in ``WORD_SEQUENCE_RUNS`` rather
    than silently extending the preceding run.
    """
    by_page = {path.stem: path for path in paths}
    declared = {page_id for _, page_ids in WORD_SEQUENCE_RUNS for page_id in page_ids}
    undeclared = sorted(set(by_page) - declared)
    runs = []
    for label, page_ids in WORD_SEQUENCE_RUNS:
        selected = [by_page[page_id] for page_id in page_ids if page_id in by_page]
        if selected:
            runs.append((label, selected))
    return runs, undeclared


def check_word_sequence_run(label, paths, stats):
    """Return the cross-file word-sequence issue for one contiguous run, if any."""
    first_ref = _first_verse_ref(paths[0])
    last_ref = _last_verse_ref(paths[-1])
    if not first_ref or not last_ref:
        return None, None

    mega_verses = get_page_verses(
        first_ref[0],
        (first_ref[1], first_ref[2]),
        last_ref[0],
        (last_ref[1], last_ref[2]),
    )
    mega_stream = build_flat_stream("_mega_", mega_verses)
    mam_words = [x for x in mega_stream if isinstance(x, str)]
    json_words = []
    for path in paths:
        json_words.extend(x for x in load_stream(path) if isinstance(x, str))
    if not json_words:
        return None, None

    # MAM may have extra tokens at the first and last extracted verses. Match
    # the shared no-marks key only: pointed JSON strings remain the page's
    # display and transcription data, while punctuation stays significant.
    match_start = next(
        (
            i
            for i in range(len(mam_words) - len(json_words) + 1)
            if no_marks_comparison_key(mam_words[i])
            == no_marks_comparison_key(json_words[0])
        ),
        None,
    )
    if match_start is None:
        return (
            f"Cross-file word check ({label}): first JSON word "
            f"{json_words[0]!r} not found in MAM-simple XML stream",
            stats[0],
        )

    mam_slice = mam_words[match_start : match_start + len(json_words)]
    if len(mam_slice) < len(json_words):
        return (
            f"Cross-file word check ({label}): JSON has {len(json_words)} words "
            f"but only {len(mam_words) - match_start} remain in MAM-simple XML "
            "from match position",
            stats[-1],
        )

    mismatches = []
    for index, (json_word, mam_word) in enumerate(zip(json_words, mam_slice)):
        if no_marks_comparison_key(json_word) != no_marks_comparison_key(mam_word):
            mismatches.append((index, json_word, mam_word))
            if len(mismatches) >= 5:
                break
    if not mismatches:
        return None, None

    words_so_far = 0
    mismatch_index = mismatches[0][0]
    blame_stat = stats[0]
    for stat in stats:
        if words_so_far + stat["words"] > mismatch_index:
            blame_stat = stat
            break
        words_so_far += stat["words"]
    detail = "; ".join(
        f"word {index}: JSON={json_word!r} MAM={mam_word!r}"
        for index, json_word, mam_word in mismatches
    )
    return (
        f"Cross-file word check ({label}): {len(mismatches)} mismatch(es) "
        f"shown vs MAM-simple XML: {detail}",
        blame_stat,
    )


def classify_item(item):
    """Return a classification string for a stream item."""
    if isinstance(item, str):
        return "word"
    if isinstance(item, dict):
        for key in (
            "page-start",
            "page-end",
            "verse-start",
            "verse-end",
            "verse-fragment-start",
            "verse-fragment-end",
            "line-start",
            "line-end",
            "parashah",
        ):
            if key in item:
                return key
        return f"unknown-dict({sorted(item.keys())})"
    return f"unknown-type({type(item).__name__})"


def check_file(path, verbose=True):
    """Check a single line-break JSON file.

    Args:
        path: Path object pointing to a line-break JSON file.
        verbose: if True, print progress and issue details to stdout.

    Returns:
        List of issue description strings (empty if no problems found).
    """
    name = path.stem
    stream = load_stream(path)
    issues = []

    # Classify all items
    classes = Counter()
    for item in stream:
        classes[classify_item(item)] += 1

    # --- Structural checks ---

    # page-start / page-end
    if classes["page-start"] != 1:
        issues.append(f"Expected 1 page-start, found {classes['page-start']}")
    if classes["page-end"] != 1:
        issues.append(f"Expected 1 page-end, found {classes['page-end']}")

    # Unknown types
    for key, count in classes.items():
        if key.startswith("unknown"):
            issues.append(f"Unknown item type: {key} (×{count})")

    # --- Line marker checks ---

    # Every line-start has exactly one matching line-end and vice versa
    line_start_counts = Counter()  # (col, line-num) -> count
    line_end_counts = Counter()
    line_starts = {}  # (col, line-num) -> last stream index (for ordering check)
    line_ends = {}  # (col, line-num) -> last stream index
    col_lines = {}  # col -> list of line-nums (from line-end markers)

    for idx, item in enumerate(stream):
        cls = classify_item(item)
        if cls == "line-start":
            info = item["line-start"]
            key = (info["col"], info["line-num"])
            line_start_counts[key] += 1
            line_starts[key] = idx
        elif cls == "line-end":
            info = item["line-end"]
            col = info["col"]
            lnum = info["line-num"]
            key = (col, lnum)
            line_end_counts[key] += 1
            line_ends[key] = idx
            if col not in col_lines:
                col_lines[col] = []
            col_lines[col].append(lnum)

    all_keys = sorted(set(line_start_counts) | set(line_end_counts))
    for key in all_keys:
        sc = line_start_counts[key]
        ec = line_end_counts[key]
        if sc == 0:
            issues.append(
                f"line-end(col={key[0]}, num={key[1]}) with no matching line-start"
            )
        elif sc > 1:
            issues.append(
                f"line-start(col={key[0]}, num={key[1]}) appears {sc} times (expected 1)"
            )
        if ec == 0:
            issues.append(
                f"line-start(col={key[0]}, num={key[1]}) with no matching line-end"
            )
        elif ec > 1:
            issues.append(
                f"line-end(col={key[0]}, num={key[1]}) appears {ec} times (expected 1)"
            )

    # Reversed-order pairs (line-end before line-start) must be truly
    # empty (no words between them)
    empty_lines = []
    matched_keys = sorted(set(line_starts) & set(line_ends))
    for key in matched_keys:
        s_idx = line_starts[key]
        e_idx = line_ends[key]
        if e_idx < s_idx:
            words_between = [
                stream[i]
                for i in range(e_idx + 1, s_idx)
                if classify_item(stream[i]) == "word"
            ]
            if words_between:
                issues.append(
                    f"line-end(col={key[0]}, num={key[1]}) comes before "
                    f"line-start but {len(words_between)} word(s) between them"
                )
            else:
                empty_lines.append(key)

    # N lines per column, numbered sequentially 1..N
    for col in sorted(col_lines.keys()):
        nums = col_lines[col]
        n = len(nums)
        if n != EXPECTED_LINES_PER_COL:
            issues.append(f"Col {col}: {n} lines (expected {EXPECTED_LINES_PER_COL})")
        expected_nums = list(range(1, n + 1))
        if nums != expected_nums:
            issues.append(
                f"Col {col}: line numbers are {nums}, " f"expected {expected_nums}"
            )

    # No words before first line-start or after last line-end
    first_ls = next(
        (i for i, x in enumerate(stream) if classify_item(x) == "line-start"),
        None,
    )
    if first_ls is not None:
        pre_words = [i for i in range(first_ls) if classify_item(stream[i]) == "word"]
        if pre_words:
            issues.append(f"{len(pre_words)} word(s) before first line-start")

    last_le = None
    for i, x in enumerate(stream):
        if classify_item(x) == "line-end":
            last_le = i
    if last_le is not None:
        post_words = [
            i
            for i in range(last_le + 1, len(stream))
            if classify_item(stream[i]) == "word"
        ]
        if post_words:
            issues.append(f"{len(post_words)} word(s) after last line-end")

    # Both columns present (structural, but depends on col_lines built above)
    if 1 not in col_lines:
        issues.append("No col 1 line markers")
    if 2 not in col_lines:
        issues.append("No col 2 line markers")

    # --- Verse marker checks ---

    # All verse identifiers are well-formed (Book C:V)
    for item in stream:
        if isinstance(item, dict):
            for key in (
                "verse-start",
                "verse-fragment-start",
                "verse-end",
                "verse-fragment-end",
            ):
                if key in item:
                    vs = item[key]
                    parts = vs.rsplit(" ", 1)
                    if len(parts) != 2 or ":" not in parts[1]:
                        issues.append(f"Malformed {key}: {vs!r}")

    # Every verse-start has exactly one matching verse-end or verse-fragment-end
    start_counts = Counter()  # counts of verse-end/verse-fragment-end per verse ID
    end_counts = Counter()  # counts of verse-start/verse-fragment-start per verse ID
    file_verse_starts = set()
    file_verse_ends = set()
    for item in stream:
        if isinstance(item, dict):
            if "verse-start" in item:
                file_verse_starts.add(item["verse-start"])
                end_counts[item["verse-start"]] += 1
            if "verse-fragment-start" in item:
                end_counts[item["verse-fragment-start"]] += 1
            if "verse-end" in item:
                file_verse_ends.add(item["verse-end"])
                start_counts[item["verse-end"]] += 1
            if "verse-fragment-end" in item:
                start_counts[item["verse-fragment-end"]] += 1

    for v in sorted(file_verse_starts):
        n = start_counts[v]
        if n == 0:
            issues.append(
                f"verse-start {v} has no matching verse-end or verse-fragment-end"
            )
        elif n > 1:
            issues.append(
                f"verse-start {v} has {n} matching verse-end/verse-fragment-end markers (expected 1)"
            )

    # Every verse-end has exactly one matching verse-start or verse-fragment-start
    for v in sorted(file_verse_ends):
        n = end_counts[v]
        if n == 0:
            issues.append(
                f"verse-end {v} has no matching verse-start or verse-fragment-start"
            )
        elif n > 1:
            issues.append(
                f"verse-end {v} has {n} matching verse-start/verse-fragment-start markers (expected 1)"
            )

    # --- Word count ---
    word_count = classes.get("word", 0)

    # --- Build stats dict ---
    stats = {
        "name": name,
        "words": word_count,
        "col_lines": {col: len(nums) for col, nums in sorted(col_lines.items())},
        "verse_starts": classes.get("verse-start", 0),
        "verse_ends": classes.get("verse-end", 0),
        "frag_starts": classes.get("verse-fragment-start", 0),
        "frag_ends": classes.get("verse-fragment-end", 0),
        "parashahs": classes.get("parashah", 0),
        "empty_lines": empty_lines,
        "file_verse_starts": file_verse_starts,
        "file_verse_ends": file_verse_ends,
        "issues": issues,
    }

    return stats


def main():
    # --no-open: suppress opening the HTML report in a browser
    no_open = "--no-open" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--no-open"]

    # Determine which files to check
    if args:
        pages = args
        paths = []
        for p in pages:
            path = LB_DIR / f"{p}.json"
            if not path.exists():
                print(f"ERROR: {path} not found")
                sys.exit(1)
            paths.append(path)
    else:
        paths = sorted(LB_DIR.glob("*.json"))

    if not paths:
        print("No JSON files found in", LB_DIR)
        sys.exit(1)

    all_stats = []
    total_issues = 0

    for path in paths:
        stats = check_file(path)
        all_stats.append(stats)
        total_issues += len(stats["issues"])

    # --- Cross-file duplicate verse check ---
    # Each full verse-start and each full verse-end should
    # appear in exactly one file.
    vs_to_files = {}  # verse -> list of filenames (from verse-start)
    ve_to_files = {}  # verse -> list of filenames (from verse-end)
    for s in all_stats:
        for v in s["file_verse_starts"]:
            vs_to_files.setdefault(v, []).append(s["name"])
        for v in s["file_verse_ends"]:
            ve_to_files.setdefault(v, []).append(s["name"])
    for v in sorted(set(vs_to_files) | set(ve_to_files)):
        vs_files = vs_to_files.get(v, [])
        ve_files = ve_to_files.get(v, [])
        if len(vs_files) > 1:
            msg = f"verse-start {v} in multiple files: {vs_files}"
            total_issues += 1
            for s in all_stats:
                if s["name"] == vs_files[0]:
                    s["issues"].append(msg)
                    break
        if len(ve_files) > 1:
            msg = f"verse-end {v} in multiple files: {ve_files}"
            total_issues += 1
            for s in all_stats:
                if s["name"] == ve_files[0]:
                    s["issues"].append(msg)
                    break

    # --- Cross-file word sequence check (MAM-simple XML ground truth) ---
    # Each declared run is contiguous in MAM-simple.  The directory as a whole
    # is not: its Deuteronomy pages and Aleppo leaf run are separated by text
    # that no JSON file represents.
    if len(paths) > 1:
        runs, undeclared_pages = word_sequence_runs(paths)
        if undeclared_pages:
            total_issues += 1
            all_stats[0]["issues"].append(
                "Cross-file word check: undeclared page run(s): "
                + ", ".join(undeclared_pages)
            )
        stats_by_name = {stat["name"]: stat for stat in all_stats}
        for label, run_paths in runs:
            run_stats = [stats_by_name[path.stem] for path in run_paths]
            msg, blame_stat = check_word_sequence_run(label, run_paths, run_stats)
            if msg:
                total_issues += 1
                blame_stat["issues"].append(msg)

    # --- Collect unique verse-start values ---
    all_verses = set()
    for path in paths:
        stream = load_stream(path)
        for item in stream:
            if isinstance(item, dict) and "verse-start" in item:
                all_verses.add(item["verse-start"])

    # --- Collect empty lines ---
    all_empty = []
    for s in all_stats:
        for col, lnum in s["empty_lines"]:
            all_empty.append((s["name"], col, lnum))

    # --- Totals ---
    tw = sum(s["words"] for s in all_stats)
    tc1 = sum(s["col_lines"].get(1, 0) for s in all_stats)
    tc2 = sum(s["col_lines"].get(2, 0) for s in all_stats)
    tvs = sum(s["verse_starts"] for s in all_stats)
    tve = sum(s["verse_ends"] for s in all_stats)
    tfs = sum(s["frag_starts"] for s in all_stats)
    tfe = sum(s["frag_ends"] for s in all_stats)
    tp = sum(s["parashahs"] for s in all_stats)
    tem = sum(len(s["empty_lines"]) for s in all_stats)

    # --- Build HTML ---
    passed = total_issues == 0
    verdict_class = "pass" if passed else "fail"
    verdict_text = "All checks passed" if passed else f"{total_issues} issue(s) found"

    rows_html = []
    for s in all_stats:
        c1 = s["col_lines"].get(1, 0)
        c2 = s["col_lines"].get(2, 0)
        em = len(s["empty_lines"])
        has_issues = bool(s["issues"])
        row_class = ' class="issue-row"' if has_issues else ""
        issue_cell = "; ".join(s["issues"]) if has_issues else "✔"
        issue_class = ' class="fail"' if has_issues else ' class="pass"'
        rows_html.append(
            f"<tr{row_class}>"
            f"<td>{s['name']}</td>"
            f"<td class='num'>{s['words']}</td>"
            f"<td class='num'>{c1}</td>"
            f"<td class='num'>{c2}</td>"
            f"<td class='num'>{s['verse_starts']}</td>"
            f"<td class='num'>{s['verse_ends']}</td>"
            f"<td class='num'>{s['frag_starts']}</td>"
            f"<td class='num'>{s['frag_ends']}</td>"
            f"<td class='num'>{s['parashahs']}</td>"
            f"<td class='num'>{em}</td>"
            f"<td{issue_class}>{issue_cell}</td>"
            f"</tr>"
        )

    empty_rows_html = ""
    if all_empty:
        elines = "".join(
            f"<tr><td>{p}</td><td class='num'>{c}</td><td class='num'>{ln}</td></tr>"
            for p, c, ln in all_empty
        )
        empty_rows_html = f"""
    <h2>Empty Lines ({len(all_empty)})</h2>
    <table>
      <tr><th>Page</th><th>Col</th><th>Line</th></tr>
      {elines}
    </table>"""

    COL_HEADERS = """
      <th title="Codex page ID (e.g. 270r = leaf 270 recto)">Page</th>
      <th title="Hebrew word count">Words</th>
      <th title="Column 1 (right) line count">C1</th>
      <th title="Column 2 (left) line count">C2</th>
      <th title="Full verse-start markers">V-st</th>
      <th title="Full verse-end markers">V-en</th>
      <th title="Verse-fragment-start (verse continues from previous page)">Fg-st</th>
      <th title="Verse-fragment-end (verse continues to next page)">Fg-en</th>
      <th title="Parashah marker count">Par</th>
      <th title="Empty lines (blank lines in the codex)">EmLn</th>
      <th title="Consistency check issues">Issues</th>"""

    html = f"""\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Line-Break Checker Report</title>
<style>
  body {{ font-family: system-ui, sans-serif; margin: 2em; background: #fafafa; }}
  h1 {{ margin-bottom: 0.3em; }}
  .verdict {{ font-size: 1.3em; font-weight: bold; margin-bottom: 1.5em; }}
  .pass {{ color: #2a7d2a; }}
  .fail {{ color: #c03030; }}
  table {{ border-collapse: collapse; margin-bottom: 1.5em; }}
  th, td {{ border: 1px solid #ccc; padding: 4px 10px; text-align: left; }}
  th {{ background: #e8e8e8; }}
  td.num {{ text-align: right; font-variant-numeric: tabular-nums; }}
  tr.issue-row {{ background: #fff0f0; }}
  tfoot td {{ font-weight: bold; background: #f0f0f0; }}
  .summary {{ margin-bottom: 1.5em; }}
  .summary span {{ margin-right: 2em; }}
</style>
</head>
<body>
<h1>Line-Break Checker Report</h1>
<div class="verdict {verdict_class}">{verdict_text}</div>

<div class="summary">
  <span>Unique verses: {len(all_verses)}</span>
  <span>Empty lines: {len(all_empty)}</span>
  <span>Pages: {len(all_stats)}</span>
</div>

<table>
  <thead>
    <tr>{COL_HEADERS}
    </tr>
  </thead>
  <tbody>
    {"".join(rows_html)}
  </tbody>
  <tfoot>
    <tr>{COL_HEADERS}
    </tr>
    <tr>
      <td>TOTAL</td>
      <td class="num">{tw}</td>
      <td class="num">{tc1}</td>
      <td class="num">{tc2}</td>
      <td class="num">{tvs}</td>
      <td class="num">{tve}</td>
      <td class="num">{tfs}</td>
      <td class="num">{tfe}</td>
      <td class="num">{tp}</td>
      <td class="num">{tem}</td>
      <td>{total_issues} issue(s)</td>
    </tr>
  </tfoot>
</table>
{empty_rows_html}

<h2>Checks Performed</h2>

<h3>Structural</h3>
<ol>
  <li>Exactly 1 <code>page-start</code> and 1 <code>page-end</code> marker per file</li>
  <li>No unknown dict types in the stream</li>
  <li>Both columns (1 and 2) present in every file</li>
</ol>

<h3>Line markers</h3>
<ol start="4">
  <li>Every <code>line-start</code> has exactly one matching <code>line-end</code> (same col &amp; line number), and vice versa</li>
  <li>Reversed-order pairs (line-end before line-start) must be truly empty (no words between them)</li>
  <li>{EXPECTED_LINES_PER_COL} lines per column, numbered sequentially 1–{EXPECTED_LINES_PER_COL}</li>
  <li>No words before first <code>line-start</code> (pre-content) or after last <code>line-end</code> (post-content)</li>
</ol>

<h3>Verse markers (within-file)</h3>
<ol start="8">
  <li>All verse identifiers are well-formed (<code>Book C:V</code>)</li>
  <li>Every <code>verse-start</code> has exactly one matching <code>verse-end</code> or <code>verse-fragment-end</code> in the same file, and vice versa</li>
  <li>Every <code>verse-end</code> has exactly one matching <code>verse-start</code> or <code>verse-fragment-start</code> in the same file, and vice versa</li>
</ol>

<h3>Verse markers (cross-file)</h3>
<ol start="11">
  <li>No full verse (<code>verse-start</code>/<code>verse-end</code>) appears in more than one file</li>
  <li>Concatenated JSON words match the MAM-simple XML word sequence for the full page range</li>
</ol>
</body>
</html>
"""

    out_path = ac_paths.check_line_breaks_html_path()
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(html, encoding="utf-8", newline="")
    print(f"Report written to {out_path}")
    if not no_open:
        webbrowser.open(out_path.as_uri())

    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
