"""
Generate the change-log index.html listing all releases.

Exports:
    write_index — write index.html from a list of release info dicts

Like its sibling mpplus_html.py, this builds HTML by string assembly and deliberately
bypasses the repo's `mb_misc.mb_html` tree-builder — a considered choice keeping the
whole mb_diff_mpu report subsystem string-based and self-contained, not an oversight.
See mpplus_html.py's module docstring for the full rationale.
"""

from mb_cmn.new_york_time import labelled


def write_index(release_info, change_log_dir):
    """Write index.html listing all releases (newest first).

    Each entry in release_info is a dict with "name", "count", and "old_date" keys.
    """
    lines = [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        "<title>MAM Change Logs</title>",
        '<link rel="stylesheet" href="../../report.css">',
        '<link rel="stylesheet" href="style.css">',
        "</head>",
        '<body class="change-log-index">',
        "<h1>MAM Change Logs</h1>",
        "<ul>",
    ]
    for info in reversed(release_info):
        name = info["name"]
        old_date = info["old_date"]
        count = info["count"]
        suffix = "change" if count == 1 else "changes"
        release_text = (
            f"Release spanning {labelled(old_date)}, to" if old_date else "Release to"
        )
        lines.append(
            f"  <li>{release_text}"
            f' <a href="{name}.html">{name}</a>'
            f" &mdash; {count} {suffix}</li>"
        )
    lines.extend(["</ul>", "</body>", "</html>"])
    path = f"{change_log_dir}/index.html"
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write("\n".join(lines) + "\n")
    print(f"  Index written to {path}")
