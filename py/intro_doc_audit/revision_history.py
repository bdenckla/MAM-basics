"""Read-only, bounded Wikisource history research outside the scripture caches."""

import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import mwparserfromhell


class HistoryClient:
    """Retain faithful API responses; request metadata before selected content."""

    def __init__(self, cache_dir):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def fetch(self, key, **params):
        if params.get("action") not in {"query", "compare"}:
            raise ValueError("History research supports read-only query/compare")
        path = self.cache_dir / (key + ".json")
        if path.exists():
            return json.loads(path.read_bytes())
        url = "https://he.wikisource.org/w/api.php?" + urlencode(
            {"format": "json", "formatversion": 2, **params}
        )
        request = Request(
            url,
            headers={
                "User-Agent": "MAM-basics read-only revision-history research (github.com/bdenckla/MAM-basics)"
            },
        )
        with urlopen(request, timeout=25) as response:
            raw = response.read()
        result = json.loads(raw)
        if "error" in result:
            raise ValueError(result["error"])
        path.write_bytes(raw)
        return result

    def metadata(self, key, title, max_pages=10):
        continuation = {}
        revisions = []
        for index in range(max_pages):
            result = self.fetch(
                f"{key}-metadata-{index:03}",
                action="query",
                prop="revisions",
                titles=title,
                rvprop="ids|timestamp|comment",
                rvlimit=500,
                rvdir="newer",
                **continuation,
            )
            page = result["query"]["pages"][0]
            revisions.extend(page.get("revisions", []))
            if "continue" not in result:
                return dict(page, revisions=revisions)
            continuation = result["continue"]
        raise ValueError("History metadata exceeds the bounded page allowance")

    def revision(self, revision_id):
        result = self.fetch(
            f"revision-{revision_id}",
            action="query",
            prop="revisions",
            revids=revision_id,
            rvprop="ids|timestamp|comment|content",
            rvslots="main",
        )
        return result["query"]["pages"][0]["revisions"][0]

    def contents(self, key, revision_ids, batch_size=8):
        records = {}
        for index in range(0, len(revision_ids), batch_size):
            batch = revision_ids[index : index + batch_size]
            result = self.fetch(
                f"{key}-content-{index // batch_size:03}",
                action="query",
                prop="revisions",
                revids="|".join(map(str, batch)),
                rvprop="ids|timestamp|comment|content",
                rvslots="main",
            )
            for page in result["query"]["pages"]:
                for revision in page.get("revisions", []):
                    records[revision["revid"]] = revision
            if not set(batch) <= set(records):
                raise ValueError("Requested historical content was not returned")
        return records


def pair_excerpts(text, forms):
    """Decode the note template's main argument, preserving every source string."""
    excerpts = []
    for line_number, line in enumerate(text.splitlines(), 1):
        if not any(form in line for form in forms):
            continue
        selected = []
        for template in mwparserfromhell.parse(line).filter_templates():
            if str(template.name).strip() == "נוסח" and template.has("1"):
                primary = str(template.get("1").value).strip()
                if primary in forms:
                    selected.append(
                        {"main": primary, "literal_template": str(template)}
                    )
        excerpts.append({"line": line_number, "text": line, "selected_pairs": selected})
    return excerpts


def revision_url(revision_id):
    return f"https://he.wikisource.org/w/index.php?oldid={revision_id}"


def diff_url(parent_id, revision_id):
    return f"https://he.wikisource.org/w/index.php?diff={revision_id}&oldid={parent_id}"
