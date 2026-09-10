"""Validate batched chapter identities and retrieve their exact raw revisions."""

import requests

from ws import ws_revision_metadata as metadata


class ChapterResponseError(RuntimeError):
    """A chapter response cannot establish a complete, unambiguous identity."""


class CountingSession(requests.Session):
    """Count transport attempts, including HTTP retries and connection failures."""

    def __init__(self):
        super().__init__()
        self.metadata_requests = 0
        self.content_requests = 0

    def request(self, method, url, **kwargs):
        if kwargs["params"]["prop"] == "info":
            self.metadata_requests += 1
        else:
            self.content_requests += 1
        return super().request(method, url, **kwargs)


def batches(items, size):
    """Batch materialized chapters without changing their order."""
    return [items[i : i + size] for i in range(0, len(items), size)]


def _require(condition, message):
    if not condition:
        raise ChapterResponseError(message)


def _query(response):
    _require(isinstance(response, dict), "Wikisource response is not an object")
    for key in ("error", "errors", "warnings", "continue"):
        _require(key not in response, f"Wikisource {key}: {response.get(key)!r}")
    query = response.get("query")
    _require(isinstance(query, dict), "Wikisource response has no query object")
    _require(
        not query.get("badrevids"), f"Unavailable revisions: {query.get('badrevids')!r}"
    )
    _require(
        isinstance(query.get("pages"), list), "Wikisource response has no pages array"
    )
    return query


def _resolved_titles(query, titles):
    _require(len(set(titles)) == len(titles), "Duplicate requested titles")
    aliases = {}
    for key in ("normalized", "redirects"):
        entries = query.get(key, [])
        _require(isinstance(entries, list), f"Invalid {key} mappings")
        for entry in entries:
            _require(isinstance(entry, dict), f"Invalid {key} entry")
            source, target = entry.get("from"), entry.get("to")
            _require(
                isinstance(source, str)
                and source
                and isinstance(target, str)
                and target,
                f"Invalid {key} titles",
            )
            _require(source not in aliases, f"Duplicate alias: {source!r}")
            aliases[source] = target
    resolved = {}
    used = set()
    for title in titles:
        current, visited = title, set()
        while current in aliases:
            _require(current not in visited, f"Cyclic title aliases: {title!r}")
            visited.add(current)
            current = aliases[current]
        used.update(visited)
        _require(current not in resolved, f"Requested titles converge on {current!r}")
        resolved[current] = title
    _require(used == set(aliases), "Unexpected title aliases in response")
    return resolved


def _page_identity(page):
    _require(isinstance(page, dict), "Invalid page object")
    for key in ("missing", "invalid", "interwiki"):
        _require(key not in page, f"Inaccessible page: {page!r}")
    _require(isinstance(page.get("title"), str) and page["title"], "Invalid page title")
    _require(metadata.positive_id(page.get("pageid")), f"Invalid page ID: {page!r}")
    return {"resolved_title": page["title"], "page_id": page["pageid"]}


def _revision(page):
    revisions = page.get("revisions")
    _require(
        isinstance(revisions, list) and len(revisions) == 1,
        "Expected exactly one revision per page",
    )
    revision = revisions[0]
    _require(
        isinstance(revision, dict) and metadata.positive_id(revision.get("revid")),
        "Invalid revision ID",
    )
    slots = revision.get("slots")
    _require(
        isinstance(slots, dict) and isinstance(slots.get("main"), dict),
        "Missing main revision slot",
    )
    for part in (revision, slots["main"]):
        _require(
            not any(
                key in part for key in ("texthidden", "contenthidden", "suppressed")
            ),
            "Hidden or suppressed revision content",
        )
    content = slots["main"].get("content")
    _require(isinstance(content, str), "Missing or inaccessible revision content")
    return revision["revid"], content.splitlines()


def title_results(response, titles, *, content):
    """Return requested-title results in request order, resolving alias chains."""
    query = _query(response)
    resolved = _resolved_titles(query, titles)
    found, page_ids, revision_ids = {}, set(), set()
    for page in query["pages"]:
        identity = _page_identity(page)
        title = resolved.get(identity["resolved_title"])
        _require(
            title is not None and title not in found,
            "Unexpected or duplicate page title",
        )
        if content:
            revision_id, lines = _revision(page)
        else:
            revision_id, lines = page.get("lastrevid"), None
            _require(metadata.positive_id(revision_id), "Invalid lastrevid")
        _require(
            identity["page_id"] not in page_ids and revision_id not in revision_ids,
            "Duplicate page/revision identity",
        )
        page_ids.add(identity["page_id"])
        revision_ids.add(revision_id)
        identity.update(requested_title=title, revision_id=revision_id)
        found[title] = (identity, lines)
    _require(set(found) == set(titles), "Incomplete Wikisource title response")
    return {title: found[title] for title in titles}


def revision_results(response, identities):
    """Bind exact content by both revision and page identity, never page order."""
    query = _query(response)
    _require(
        not query.get("normalized") and not query.get("redirects"),
        "Unexpected aliases for exact revisions",
    )
    expected = {identity["revision_id"]: identity for identity in identities}
    _require(len(expected) == len(identities), "Duplicate requested revisions")
    found = {}
    for page in query["pages"]:
        page_identity = _page_identity(page)
        revision_id, lines = _revision(page)
        identity = expected.get(revision_id)
        _require(
            identity is not None and revision_id not in found,
            "Unexpected or duplicate revision",
        )
        _require(
            all(identity[key] == value for key, value in page_identity.items()),
            "Page moved or identity changed after revision check",
        )
        found[revision_id] = (identity, lines)
    _require(set(found) == set(expected), "Incomplete Wikisource revision response")
    return {
        identity["requested_title"]: found[identity["revision_id"]]
        for identity in identities
    }


class ChapterClient:
    """Serial chapter queries with global identity checks across request batches."""

    def __init__(self, downloader, endpoint):
        self.downloader = downloader
        self.endpoint = endpoint
        self.metadata_batches = 0
        self.content_batches = 0
        self._owners = {"page_id": {}, "revision_id": {}, "resolved_title": {}}

    def _get(self, params):
        if params["prop"] == "info":
            self.metadata_batches += 1
        else:
            self.content_batches += 1
        return self.downloader.get_json(
            self.endpoint,
            params={
                "action": "query",
                "format": "json",
                "formatversion": 2,
                "maxlag": 1,
                **params,
            },
            allow_cache=False,
        )

    def by_titles(self, titles, *, content):
        params = {
            "prop": "revisions" if content else "info",
            "redirects": 1,
            "titles": "|".join(titles),
        }
        if content:
            params.update(rvprop="ids|content", rvslots="main")
        results = title_results(self._get(params), titles, content=content)
        for identity, _lines in results.values():
            for key, owners in self._owners.items():
                value, title = identity[key], identity["requested_title"]
                _require(
                    value not in owners or owners[value] == title,
                    f"Duplicate {key} across chapter batches",
                )
                owners[value] = title
        return results

    def by_revisions(self, identities):
        return revision_results(
            self._get(
                {
                    "prop": "revisions",
                    "revids": "|".join(
                        str(identity["revision_id"]) for identity in identities
                    ),
                    "rvprop": "ids|content",
                    "rvslots": "main",
                }
            ),
            identities,
        )
