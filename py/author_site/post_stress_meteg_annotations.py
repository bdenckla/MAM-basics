"""Validate MAS annotations against source forms without changing displayed text.

Phonetic MAM uses MASORA CIRCLE and UPPER DOT as annotations. Those codepoints
can also belong to a source text: accept an exact independently sourced form,
including its Hebrew context. LOWER DOT and VARIKA are not these annotations.
Complete-page validation covers cells, prose, literals, compositions, fallbacks
and attributes. Survey strings and literals locate defects but do not authorize
themselves as reference forms.
"""

from __future__ import annotations

import ast
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
import re
import unicodedata

from accgram import post_stress_meteg as psm
from accgram import mam_simple_verse
from mb_cmn import paths

_FORM = re.compile(r"[\u034f\u0590-\u05ff\ufb1e~]+")
_BCV = re.compile(r"(.+?)(\d+):(\d+)$")
_ANNOTATION_MARKS = frozenset((psm.hpu.MCIRC, psm.hpu.UPDOT))
_BLOCKS = frozenset(
    (
        "html",
        "head",
        "body",
        "title",
        "p",
        "div",
        "table",
        "thead",
        "tbody",
        "tr",
        "td",
        "th",
        "li",
        "ul",
        "ol",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "br",
        "hr",
        "section",
        "figure",
        "figcaption",
        "pre",
    )
)


def _survey_strings(node: object, pointer: str = ""):
    if isinstance(node, str):
        yield pointer, node
    elif isinstance(node, dict):
        for key, value in node.items():
            escaped = str(key).replace("~", "~0").replace("/", "~1")
            yield from _survey_strings(value, f"{pointer}/{escaped}")
    elif isinstance(node, (list, tuple)):
        for index, value in enumerate(node):
            yield from _survey_strings(value, f"{pointer}/{index}")


def _add_source_location(locations, text: str, source: str) -> None:
    for match in _FORM.finditer(text):
        form = match[0]
        locations[form].add(source)
        # Index the permitted display spelling too; never change the source text.
        locations[form.replace(psm.hpu.NU_GMAQ, psm.MAQAF)].add(source)


def source_locations(survey: dict, author_path: Path) -> dict[str, set[str]]:
    """Locate possible inputs of a displayed form without accepting those inputs."""
    locations = defaultdict(set)
    for pointer, text in _survey_strings(survey):
        _add_source_location(
            locations, text, f"{psm.default_json_out_path()}#{pointer}"
        )
    tree = ast.parse(author_path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            _add_source_location(locations, node.value, f"{author_path}:{node.lineno}")
    return locations


def reference_forms(extra_sources: dict[str, str]) -> dict[str, set[str]]:
    """Independent current-MAM forms and explicitly supplied comparison sources.

    All cantillation projections participate, preserving native extraordinary dots.
    An authored literal or a raw survey form is never its own reference.
    """
    references = defaultdict(set)
    directory = paths.require_mam_simple_dir()
    source_files = {}
    for bb in psm.wlc_bb_codes():
        path = mam_simple_verse._mam_simple_json_path(
            directory, psm.wlc_bb_to_bk39id(bb)
        )
        if path is None:
            raise FileNotFoundError(f"{directory}: missing MAM source for {bb}")
        source_files[bb] = path
    for cantillation in (None, psm.CANT_ALEF, psm.CANT_BET):
        for bcv, words in psm._mam_words_by_bcv(cantillation).items():
            for word in words:
                for match in _FORM.finditer(word):
                    if _ANNOTATION_MARKS.intersection(match[0]):
                        references[match[0]].add(
                            f"{source_files[_BCV.fullmatch(bcv)[1]]} {bcv} "
                            f"{cantillation or 'cant-combined'}"
                        )
    for source, text in extra_sources.items():
        for match in _FORM.finditer(text):
            references[match[0]].add(source)
    return references


class _PageAnnotations(HTMLParser):
    """Join Hebrew across inline spans so typography cannot evade validation."""

    def __init__(self, path, locations, references):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.locations = locations
        self.references = references
        self.problems = []
        self.forms_checked = 0
        self.source_marks_checked = 0
        self.pending = ""
        self.pending_position = None
        self.ignored = None

    def _check(self, form, position, context):
        self.forms_checked += 1
        marks = _ANNOTATION_MARKS.intersection(form)
        if not marks:
            return
        if form in self.references:
            self.source_marks_checked += 1
            return
        locations = self.locations.get(form, set())
        if not locations:
            locations = {
                location
                for fragment, origins in self.locations.items()
                if fragment in form and marks.intersection(fragment)
                for location in origins
            }
        self.problems.append(
            {
                "output": f"{self.path}:{position[0]}:{position[1] + 1} ({context})",
                "form": form,
                "marks": [
                    f"U+{ord(mark):04X} {unicodedata.name(mark)}"
                    for mark in sorted(marks)
                ],
                "sources": sorted(locations)
                or ["unresolved composed input; inspect output location"],
            }
        )

    def _flush(self):
        if self.pending:
            self._check(self.pending, self.pending_position, "text")
            self.pending = ""
            self.pending_position = None

    def handle_starttag(self, tag, attrs):
        if tag in _BLOCKS or tag in {"script", "style"}:
            self._flush()
        for name, value in attrs:
            for match in _FORM.finditer(value or ""):
                self._check(match[0], self.getpos(), f"{tag} @{name}")
        if tag in {"script", "style"}:
            self.ignored = tag

    def handle_endtag(self, tag):
        if tag in _BLOCKS or tag == self.ignored:
            self._flush()
        if tag == self.ignored:
            self.ignored = None

    def handle_data(self, data):
        if self.ignored:
            return
        line, column = self.getpos()
        end = 0
        for match in _FORM.finditer(data):
            if match.start() != end:
                self._flush()
            if not self.pending:
                prefix = data[: match.start()]
                offset = prefix.count("\n")
                self.pending_position = (
                    line + offset,
                    len(prefix.rsplit("\n", 1)[-1]) if offset else column + len(prefix),
                )
            self.pending += match[0]
            end = match.end()
        if end != len(data):
            self._flush()

    def close(self):
        super().close()
        self._flush()


def validate_pages(page_paths, survey, author_path, *, extra_sources):
    """Raise with source and output locations for every unverified annotation form."""
    locations = source_locations(survey, author_path)
    references = reference_forms(extra_sources)
    reports = []
    problems = []
    for filename in page_paths:
        path = Path(filename)
        parser = _PageAnnotations(path, locations, references)
        parser.feed(path.read_text(encoding="utf-8"))
        parser.close()
        reports.append(
            {
                "path": str(path),
                "forms_checked": parser.forms_checked,
                "source_marks_checked": parser.source_marks_checked,
            }
        )
        problems.extend(parser.problems)
    if not reports:
        raise ValueError("MAS annotation validation received no output pages")
    if problems:
        raise ValueError(f"Unverified MAS display annotations: {problems}")
    return reports
