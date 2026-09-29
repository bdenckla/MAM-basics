# GitHub issue rules and transport in Claude cloud sessions

Read this reference before an issue operation in a Claude cloud session. Installing this skill
supplies Ben's citation, routing, authorship and state-change rules; it supplies no account
credential or authorization for a live act. Discover the available tool and requested tracker's
access within the session. A desktop login, another tracker's visibility or an installed `gh`
does not establish cloud access to the requested tracker. Never print credential values.

## Read the issue and every comment through REST

Anthropic's [cloud GitHub proxy documentation](https://code.claude.com/docs/en/cloud-environments#github-proxy)
describes attached-repository API scope and a restricted GraphQL operation set with REST
fallback. The [GitHub tools section](https://code.claude.com/docs/en/cloud-environments#work-with-github-issues-and-pull-requests)
documents `gh` and proxy authentication. These are runtime requirements to verify, rather than
proof that a particular session has exercised a command. `gh issue view` uses GraphQL, so a
successful REST request does not establish that the local full-read recipe works in cloud.

Create a uniquely named UTF-8 Python script in the session's scratch directory, with the
following body. The script captures the issue and every comments page through `gh api`, writes
both into one UTF-8 artifact and exits on a failed request or unexpected response. Give the
exact `bdenckla/<repo>` slug and issue number from the authorized task; the issue JSON retains
title, state, labels and body, and the separate comments array retains every comment.

```python
import json
from pathlib import Path
import subprocess
import sys

slug, number, output = sys.argv[1:]
number = str(int(number))


def get_json(endpoint, *, paginate=False):
    command = ["gh", "api", "--method", "GET", endpoint]
    if paginate:
        command.extend(["--paginate", "--slurp"])
    result = subprocess.run(
        command, capture_output=True, check=True, encoding="utf-8"
    )
    return json.loads(result.stdout)


issue = get_json(f"repos/{slug}/issues/{number}")
pages = get_json(
    f"repos/{slug}/issues/{number}/comments?per_page=100", paginate=True
)
if not isinstance(issue, dict) or "pull_request" in issue:
    raise ValueError("expected an issue response")
if not {"title", "state", "labels", "body"}.issubset(issue):
    raise ValueError("incomplete issue response")
if not isinstance(pages, list) or not pages:
    raise ValueError("missing comments-page response")
if any(not isinstance(page, list) for page in pages):
    raise ValueError("unexpected comments-page response")
comments = [comment for page in pages for comment in page]
Path(output).write_text(
    json.dumps({"issue": issue, "comments": comments}, ensure_ascii=False, indent=2)
    + "\n",
    encoding="utf-8",
    newline="\n",
)
```

Run that saved script with the checkout's hydrated Linux interpreter and a uniquely named
output path, then read the complete artifact before commenting, editing or changing state.
The session's environment must provide compatible Python and `gh`; use the tracked Linux
requirements/constraints setup when hydration is required. Never substitute stdin or a shell
pipeline for captured UTF-8 output. An inaccessible tracker or failed page request leaves the
full read incomplete; report the limitation instead of proceeding from a partial issue.

## Preserve the required body editor and state-change procedure

`py/main_github_issue_edit.py` delegates reads and writes to `gh issue view` and `gh issue edit`.
It has no REST transport. Under the restricted proxy its body-edit procedure, including
`--dry-run`, is unavailable. Report that limitation and leave the body edit pending; do not
recreate it with a fetched snapshot and a REST PATCH. Compatible support belongs in the
existing helper and needs its own authorized implementation and verification.

Other live writes still require the operation reference, the task's authorization and a
verified compatible transport. When the prescribed command is unsupported, report the act
as pending. A successful issue read is not a write-permission check. Preserve the agent-written
dated text, the reason comment for state changes and the push-before-closing rule. This
installation does not authorize a test mutation, a new credential or a permission change.
