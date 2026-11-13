"""Write an HTML forwarding page for an address that has moved within the site."""

import html
import json
from pathlib import Path

_TEMPLATE = """<!doctype html>
<!-- {comment} -->
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<link rel="canonical" href="{href}">
<meta http-equiv="refresh" content="0; url={href}">
<script>
location.replace({href_js} + location.search + location.hash);
</script>
</head>
<body>
<p>This page has moved to <a href="{href}">a different location</a>.</p>
</body>
</html>
"""


def write(path: Path, href: str, title: str, *, generated_comment: str) -> str:
    """Write a stub pointing to a relative URL and return the path written."""
    path.write_text(
        _TEMPLATE.format(
            comment=html.escape(generated_comment),
            title=html.escape(f"Redirect for {title}"),
            href=html.escape(href, quote=True),
            href_js=json.dumps(href),
        ),
        encoding="utf-8",
        newline="\n",
    )
    return str(path)
