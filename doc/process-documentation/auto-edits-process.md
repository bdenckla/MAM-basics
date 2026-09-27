# Google Sheet auto-edits process (retired)

The MAM Google Sheet pipeline was retired on September 12, 2026. Hebrew
Wikisource is the maintained textual source; the Sheet and its change log remain
available as a frozen historical archive.

The retired process downloaded the Sheet, parsed it into `MAM-parsed/google/`,
compared that product with the Wikisource mirror through `diff_wsgo`, and supplied
the resulting auto-edits to two Google Apps Script programs. The downloader,
parser, comparison code, generated comparison results, repository copies of the
Apps Script programs, and this runbook's operational steps were removed together.

Git history is the reconstruction path for the former implementation and its
instructions. This page is only a retirement marker; it is not a live runbook.
