# Holman data and authored-asset workflow

Read this reference before working with the Holman mailboxes, correspondence derivatives, dispositions, or authored CSS and JavaScript.

## Holman's mailboxes, public derivatives, and authored CSS

The raw mailboxes for Holman's two correspondence projects are untracked under
MAM-basics' `.novc/`: `.novc/eml/` contains suggested UXLC corrections and
`.novc/eml-mam/` contains suggested MAM corrections. This public repository
does not track a `.eml` file or an address from any mail header.

The UXLC ingest writes the address-free derivative in `holman/emails/` and
redacts addresses from message bodies as it reads them, including forwarded
headers quoted in a body. Before adding a field to that derivative, check what
the field would carry from a mail header.

The MAM-suggestions ingest has a stricter boundary. It tracks no message body:
only the suggestion itself, its reference and compared forms, Holman's
description or suggestion where present, and the subject, date, and sender
display name. `py/hkq_cmn/mam_suggestion_extract.py` accepts messages only from
Holman; it does not harvest correspondence among Ben Denckla and Avi Kadish.
A substantive judgment that settles a suggestion belongs in
`py/hkq_cmn/mam_suggestion_dispositions.py`, deliberately and with the person who
reached the judgment cited by name and date. Personal circumstances and
availability do not belong in a disposition.

The four authored Holman CSS and JavaScript assets live under `holman/assets/`.
Edit those files rather than their generated copies under `gh-pages/holman/`.
Every authored CSS theme declares `color-scheme: light dark` on `:root` and
every theme custom property that stores a color uses a
`light-dark(<light>, <dark>)` pair. Fixed badge foregrounds and backgrounds
remain literal colors.
