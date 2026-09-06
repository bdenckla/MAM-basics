"""Ingest Holman's suggested corrections TO MAM into the tracked extract.

Run from the MAM-basics repo root, with the mailbox in its default untracked
location (``.novc/eml-mam/``):

    .venv/Scripts/python.exe py/main_ingest_mam_suggestions.py

Writes ``holman/docs-not-served/mam_suggestions.json`` and the page crops under
``gh-pages/holman/mam_img/``.

WHAT DOES NOT GET WRITTEN, and why this differs from the UXLC ingest beside it.
No message body reaches a tracked file.  ``main_ingest_uxlc_emails.py`` tracks
each body verbatim with addresses replaced; this one tracks the suggestions
themselves and the message's subject, date and sender display name, and nothing
else.  The threads around these messages carry Ben Denckla's and Seth (Avi)
Kadish's discussion of the suggestions, and none of it is harvested from here:
``hkq_cmn/mam_suggestion_extract.py`` reads only messages Holman himself sent.
What that protects is the personal side of the correspondence; a substantive
judgment that settles a suggestion is written down deliberately, with its author
cited, in ``hkq_cmn/mam_suggestion_dispositions.py``.  Both modules' docstrings
state the boundary.

Verification against the landed ``MAM-parsed/plus/*.json`` is part of the
ingest rather than a command of its own.  It never fails the run: a case whose
form is not at its stated atom is a fact about Holman's numbering to be read off
the extract, not a reason to refuse the whole message.  That is the opposite of
the fixed 77-row review's fail-fast verification, and deliberately so -- there
the corpus is the oracle for a fixed scope, here it is a second opinion on
correspondence that Holman and Ben are still working out.
"""

from __future__ import annotations

import argparse
import email
import email.message
import email.policy
from functools import lru_cache
import io
import json
import os
from pathlib import Path
import sys
import zipfile

import hkq_paths
from hkq_cmn.mam_suggestion_corrections import (
    CASE_FIELD_CORRECTIONS,
    apply_corrections,
    corrected_form,
    require_every_correction_applied,
)
from hkq_cmn.mam_suggestion_dispositions import (
    apply_disposition,
    is_suppressed,
    require_every_disposition_applied,
)
from hkq_cmn.mam_suggestion_extract import ImageTarget, read_suggestion_messages
from hkq_cmn.verify_mam_suggestions import check_case, summarize


def _ref_with_atom(ref_as_sent: str, atom: int) -> str:
    """The same reference with a different atom index: "1Ki 7:24.17" -> "1Ki 7:24.16"."""
    head, _, _ = ref_as_sent.rpartition(".")
    return f"{head}.{atom}"


@lru_cache(maxsize=16)
def _message(eml_path: Path) -> email.message.EmailMessage:
    return email.message_from_bytes(eml_path.read_bytes(), policy=email.policy.default)


def _attachment_bytes(eml_path: Path, filename: str) -> bytes:
    for part in _message(eml_path).walk():
        if part.get_filename() == filename:
            payload = part.get_payload(decode=True)
            if payload is None:
                raise ValueError(
                    f"{eml_path.name}: attachment {filename!r} has no payload"
                )
            return payload
    raise ValueError(f"{eml_path.name}: no attachment named {filename!r}")


def _workbook_member_bytes(eml_path: Path, member: str) -> bytes:
    for part in _message(eml_path).walk():
        name = part.get_filename()
        if name and name.lower().endswith(".xlsx"):
            payload = part.get_payload(decode=True)
            if payload is None:
                raise ValueError(f"{eml_path.name}: workbook {name!r} has no payload")
            with zipfile.ZipFile(io.BytesIO(payload)) as archive:
                return archive.read(member)
    raise ValueError(f"{eml_path.name}: no workbook attachment to read {member!r} from")


def _export_images(
    case_index: int,
    targets: list[ImageTarget],
    eml_dir: Path,
    image_dir: Path,
    data_root: Path,
) -> list[str]:
    """Write a case's crops, and return their paths relative to the data root.

    Write-once: a crop already on disk with different bytes raises rather than
    being overwritten, so a re-ingest cannot silently replace an image a reader
    has already looked at.
    """
    exported: list[str] = []
    image_dir.mkdir(parents=True, exist_ok=True)
    for image_index, target in enumerate(targets, start=1):
        eml_path = eml_dir / target.eml_name
        if target.kind == "attachment":
            image_bytes = _attachment_bytes(eml_path, target.locator)
        elif target.kind == "workbook-member":
            image_bytes = _workbook_member_bytes(eml_path, target.locator)
        else:
            raise ValueError(f"unknown image target kind {target.kind!r}")

        suffix = Path(target.locator).suffix or ".png"
        output_path = image_dir / f"mam{case_index:03d}_{image_index:02d}{suffix}"
        if output_path.exists():
            if output_path.read_bytes() != image_bytes:
                raise ValueError(
                    "refusing to overwrite an extracted crop with different bytes: "
                    f"{output_path}"
                )
        else:
            output_path.write_bytes(image_bytes)
        exported.append(
            Path(os.path.relpath(output_path.resolve(), data_root.resolve())).as_posix()
        )
    return exported


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--eml-dir", type=Path, default=hkq_paths.mam_eml_dir())
    parser.add_argument(
        "--suggestions-json",
        type=Path,
        default=hkq_paths.mam_suggestions_json_path(),
    )
    parser.add_argument(
        "--image-dir", type=Path, default=hkq_paths.mam_suggestion_img_dir()
    )
    args = parser.parse_args()

    data_root = hkq_paths.hkq_data_root()
    sources, cases, skipped = read_suggestion_messages(args.eml_dir)
    cases.sort(
        key=lambda one: (
            one.ref.std_book_name,
            one.ref.chapter,
            one.ref.verse,
            one.ref.atom,
        )
    )

    checks = []
    payload_cases = []
    applied_correction_keys: set[tuple[str, str]] = set()
    applied_disposition_refs: set[str] = set()
    for case_index, case in enumerate(cases, start=1):
        ref_as_sent = str(case.ref)
        # The quoted forms reach check_case CORRECTED, so that it can anchor its
        # atom derivation on the form MAM actually has.  The payload below still
        # gets Holman's wording and apply_corrections still rewrites it, so this
        # changes what is verified and not what is published.
        check = check_case(
            std_book_name=case.ref.std_book_name,
            chapter=case.ref.chapter,
            verse=case.ref.verse,
            atom=case.ref.atom,
            mam_form=corrected_form(ref_as_sent, "mam_form", case.mam_form),
            comparison_form=corrected_form(
                ref_as_sent, "comparison_form", case.comparison_form
            ),
        )
        checks.append(check)
        payload = case.payload()
        payload["case_number"] = case_index

        # The derived atom index is the one everything downstream uses; Holman's
        # is kept beside it only where the two differ.  verify_mam_suggestions'
        # docstring says why the derivation is unambiguous.
        if not check.stated_atom_agrees:
            payload["atom"] = check.derived_atom
            payload["atom_as_sent"] = check.stated_atom
            payload["ref"] = _ref_with_atom(ref_as_sent, check.derived_atom)
            payload["ref_as_sent"] = ref_as_sent

        for key in CASE_FIELD_CORRECTIONS:
            if key[0] == ref_as_sent:
                applied_correction_keys.add(key)
        apply_corrections(payload, ref_as_sent)
        if apply_disposition(payload, ref_as_sent):
            applied_disposition_refs.add(ref_as_sent)

        payload["image_files"] = _export_images(
            case_index, case.image_targets, args.eml_dir, args.image_dir, data_root
        )
        payload["mam_plus_check"] = check.payload()
        payload_cases.append(payload)

    require_every_correction_applied(applied_correction_keys)
    require_every_disposition_applied(applied_disposition_refs)

    document = {
        "source_messages": [one.payload() for one in sources],
        "case_count": len(payload_cases),
        "suppressed_case_count": sum(
            1 for payload in payload_cases if is_suppressed(payload)
        ),
        "mam_plus_verify": summarize(checks),
        "cases": payload_cases,
    }
    args.suggestions_json.parent.mkdir(parents=True, exist_ok=True)
    args.suggestions_json.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="",
    )

    print(
        json.dumps(
            {
                "suggestions_json": args.suggestions_json.as_posix(),
                "image_dir": args.image_dir.as_posix(),
                "source_message_count": len(sources),
                "case_count": len(payload_cases),
                "mam_plus_verify": document["mam_plus_verify"],
                "skipped_messages": skipped,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
