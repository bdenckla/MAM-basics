"""The trial's drafts: each one's data module and the prefix of its work files.

Written for the concrete-transcription trial, 2026-11-03.  Draft 1 is
Claude's first reading; draft 2 is Claude's reading re-seeded from Ben's edits of
draft 1's page; draft 3 is draft 2 changed as Ben asked on 2026-11-04.
"""

import importlib

DRAFTS = {
    "1": ("ct_signs", "draft"),
    "2": ("ct_signs2", "draft2"),
    "3": ("ct_signs3", "draft3"),
}


def draft(name):
    """Draft `name`'s data module and work-file prefix."""
    if name not in DRAFTS:
        raise SystemExit(f"no draft {name!r}; the drafts are {', '.join(DRAFTS)}")
    module, prefix = DRAFTS[name]
    return importlib.import_module(f"concrete_transcription.{module}"), prefix


def draft_of_version(version):
    """The draft whose page carries `version`, as draft() gives it."""
    for name in DRAFTS:
        signs, prefix = draft(name)
        if signs.DRAFT_VERSION == version:
            return signs, prefix
    raise SystemExit(f"no draft is {version!r}")
