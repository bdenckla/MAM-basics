"""
Generate the change-log index.html listing all releases.

Exports:
    write_index — write index.html from a list of release info dicts
"""


def write_index(release_info, change_log_dir):
    """Write index.html listing all releases (newest first).

    Each entry in release_info is a dict with "name" and "count" keys.
    """
    lines = [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        "<title>MAM Change Log</title>",
        "<style>",
        "body {",
        '  font: 15px/1.6 "Segoe UI", system-ui, sans-serif;',
        "  max-width: 700px; margin: 2rem auto; padding: 0 1.5rem;",
        "  color: #333;",
        "}",
        "h1 { font-size: 1.4rem; margin-bottom: 1rem; }",
        "ul { margin: 0; padding-left: 1.5rem; }",
        "li { margin: .3rem 0; }",
        "a { color: #4a90d9; }",
        "</style>",
        "</head>",
        "<body>",
        "<h1>MAM Change Log</h1>",
        "<ul>",
    ]
    for info in reversed(release_info):
        name = info["name"]
        count = info["count"]
        suffix = "change" if count == 1 else "changes"
        lines.append(
            f'  <li><a href="{name}.html">{name}</a>'
            f" &mdash; {count} body text {suffix}</li>"
        )
    lines.extend(["</ul>", "</body>", "</html>"])
    path = f"{change_log_dir}/index.html"
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"  Index written to {path}")
