"""
Generate the change logs' contributors page, contributors.html.

Exports:
    write_contributors — write contributors.html from each record's match

The page lists each contributor whom ``in/mam-change-log-credits.json`` credits, that is,
each contributor other than Ben Denckla and Avi Kadish whom the change logs credit, sorted by
name ignoring case. Under each it lists every change credited to them, in the order the
reports list the changes: the releases in releases.json's order, then unpinned-latest, and
each report's entries in its order. A change shows its release, linked to that release's
report; its verse, linked to its card there by the card's id, ``mpplus_credits.card_id``;
its old and new forms; and its evidence, under the labels its card gives the evidence.

The forms are the card's own, read back from the report as written: the card's
change-display line, which ``mpplus_html._render_card`` draws with ``char_diff_spans``. A
record holds its forms as the report's JSON does, as text, while the card draws that text as
the verse's templates have it. On 2026-11-19 the record crediting 2 Samuel 15:12 holds the
paseq code point, which its card marks as a legarmeh with a ruby, so that the record's own
forms drawn with ``char_diff_spans`` would have shown the bare code point. Reading the card
back also checks the page's links: generation stops unless the report has a card with the id
that the page links, and that card carries the record's credit line. A change credited by its
templates has no forms on its card, and the page shows the templates added and removed.

Like its siblings mpplus_html.py and mpplus_index.py, this builds HTML by string assembly;
mpplus_html.py's module docstring gives the reason.
"""

from collections import Counter
from pathlib import Path

from mb_diff_mpu import mpplus_credits, mpplus_html

_TITLE = "Contributors Credited in the MAM Change Logs"
# The lines of a card that mpplus_html._render_card writes, up to its credit lines.
_CARD_OPENING = '<div class="diff-card" id="'
_VERSE_REF = '<div class="verse-ref">'
_CHANGE_DISPLAY = '<div class="change-display">'
_CREDIT_LINE = '<p class="credit">'


def _read_card(lines, report, credit):
    """Find, in a report's lines, the card that the page links for a record.

    Return the card's line number and its change-display line, or None for a card that
    has none. The card's lines are its opening tag, which holds its id; its verse-ref line;
    its change-display line, when its text changed; and then a credit line for each of its
    credits, which must include this record's.
    """
    card_id = mpplus_credits.card_id(credit)
    opening = f'{_CARD_OPENING}{card_id}" '
    found = [number for number, line in enumerate(lines) if line.startswith(opening)]
    if len(found) != 1:
        raise mpplus_credits.CreditError(
            f"contributors.html: {report}.html has {len(found)} cards, not 1, with the id"
            f" {card_id} of {credit.describe()}"
        )
    number = found[0] + 1
    if not lines[number].startswith(_VERSE_REF):
        raise mpplus_credits.CreditError(
            f"contributors.html: the card {card_id} of {report}.html has no verse-ref line"
            " after its opening tag"
        )
    number += 1
    forms = None
    if lines[number].startswith(_CHANGE_DISPLAY):
        forms = lines[number]
        number += 1
    credit_lines = []
    while lines[number].startswith(_CREDIT_LINE):
        credit_lines.append(lines[number])
        number += 1
    if mpplus_html.credit_line_html(credit) not in credit_lines:
        raise mpplus_credits.CreditError(
            f"contributors.html: the card {card_id} of {report}.html does not carry the"
            f" credit line of {credit.describe()}"
        )
    return found[0], forms


def _template_names(names):
    """Template names as a card's description lists them, each isolated with a ``<bdi>``."""
    counts = Counter(names)
    return ", ".join(
        f"<bdi>{mpplus_html._esc(name)}</bdi>"
        + ("" if counts[name] == 1 else f" x{counts[name]}")
        for name in sorted(counts)
    )


def _shown(credit, forms, report):
    """What the page shows of a credited change: its card's forms, or its templates."""
    if credit.change is not None:
        if forms is None:
            raise mpplus_credits.CreditError(
                f"contributors.html: the card of {credit.describe()} in {report}.html"
                " shows no forms"
            )
        return forms
    if credit.templates is not None:
        added, removed = credit.templates
        parts = []
        if added:
            parts.append(f"added: {_template_names(added)}")
        if removed:
            parts.append(f"removed: {_template_names(removed)}")
        return f'<p class="change-desc">Template change ({"; ".join(parts)})</p>'
    raise AssertionError(f"record {credit.number} has neither change nor templates")


def _change_lines(match, forms):
    """The page's lines for one credited change."""
    credit = match.credit
    report = mpplus_html._esc(match.report)
    card_id = mpplus_html._esc(mpplus_credits.card_id(credit))
    ref = mpplus_html._esc(f"{credit.book} {credit.chapter}:{credit.verse}")
    return [
        '<div class="diff-card">',
        '<div class="verse-ref"><span class="ref-text">'
        f'Release <a href="{report}.html">{report}</a>,'
        f' <a href="{report}.html#{card_id}">{ref}</a></span></div>',
        _shown(credit, forms, match.report),
        f'<p class="credit">Evidence: {mpplus_html.credit_evidence_html(credit)}.</p>',
        "</div>",
    ]


def write_contributors(matches, report_names, change_log_dir):
    """Write contributors.html into ``change_log_dir`` from each record's ``Match``.

    ``matches`` are those that ``mpplus_credits.require_each_record_matched_once`` returns,
    and ``report_names`` the reports it read, in releases.json's order and then
    unpinned-latest. Every report must already be written in ``change_log_dir``.
    """
    order = {name: index for index, name in enumerate(report_names)}
    report_lines = {}
    # Each contributor's id, mapped to one of their credits, which gives their name.
    credit_of = {}
    # Each contributor's id, mapped to their changes: each one's place in the reports,
    # its match, and its card's forms.
    changes_of = {}
    for match in matches:
        if match.report not in report_lines:
            path = Path(change_log_dir) / f"{match.report}.html"
            report_lines[match.report] = path.read_text(encoding="utf-8").split("\n")
        number, forms = _read_card(
            report_lines[match.report], match.report, match.credit
        )
        place = (order[match.report], match.entry, number)
        ident = match.credit.contributor
        credit_of.setdefault(ident, match.credit)
        changes_of.setdefault(ident, []).append((place, match, forms))
    lines = [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        f"<title>{_TITLE}</title>",
        '<link rel="stylesheet" href="../../report.css">',
        '<link rel="stylesheet" href="style.css">',
        "</head>",
        "<body>",
        f"<h1>{_TITLE}</h1>",
        '<p class="subtitle"><a href="index.html">Up to MAM Change Logs</a></p>',
        '<p class="subtitle">This page lists the contributors other than Ben Denckla and'
        " Avi Kadish whom the MAM change logs credit, each credit recorded on Ben's"
        " word.</p>",
    ]
    by_name = sorted(
        changes_of, key=lambda ident: (credit_of[ident].name.casefold(), ident)
    )
    for ident in by_name:
        changes = sorted(changes_of[ident], key=lambda change: change[0])
        count = len(changes)
        noun = "credited change" if count == 1 else "credited changes"
        name_html = mpplus_html.credit_name_html(credit_of[ident])
        lines.append(f"<h2>{name_html} ({count} {noun})</h2>")
        for _, match, forms in changes:
            lines.extend(_change_lines(match, forms))
    lines.extend(["</body>", "</html>"])
    path = f"{change_log_dir}/contributors.html"
    with open(path, "w", encoding="utf-8", newline="") as out_fp:
        out_fp.write("\n".join(lines) + "\n")
    print(f"  Contributors page written to {path}")
