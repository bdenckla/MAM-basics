"""Differential coverage for closed MAM-simple book-group path dispatch."""

from itertools import count, product
from pathlib import Path

import pytest

from mb_cmn.mam_simple_book_group import resolve_book_group_path

_FORMATS = {"json": ".json", "xml": ".xml"}
_VTRADS = ("mam", "bhs", "sef")
_STEM_ORDERS = (("alpha", "beta"), ("beta", "alpha"))


def _standard_attempts(
    root: Path,
    *,
    fmt: str,
    vtrad: str,
    stems: tuple[str, ...],
    allow_mam_fallback: bool,
) -> list[Path]:
    directories = [root / f"{fmt}-vtrad-{vtrad}"]
    if allow_mam_fallback and vtrad in {"bhs", "sef"}:
        directories.append(root / f"{fmt}-vtrad-mam")
    return [
        directory / f"{stem}{_FORMATS[fmt]}"
        for directory in directories
        for stem in stems
    ]


def _populate(attempts: list[Path], present_mask: int) -> list[Path]:
    present: list[Path] = []
    for index, candidate in enumerate(attempts):
        if present_mask & (1 << index):
            candidate.parent.mkdir(parents=True, exist_ok=True)
            candidate.write_text("independent fixture\n", encoding="utf-8")
            present.append(candidate)
    return present


def test_standard_book_group_resolution_matches_independent_oracle(tmp_path) -> None:
    case_numbers = count()
    for fmt, vtrad, allow_mam_fallback, stems in product(
        _FORMATS, _VTRADS, (False, True), _STEM_ORDERS
    ):
        probe = tmp_path / f"standard-{next(case_numbers)}"
        attempts = _standard_attempts(
            probe,
            fmt=fmt,
            vtrad=vtrad,
            stems=stems,
            allow_mam_fallback=allow_mam_fallback,
        )
        for present_mask in range(1 << len(attempts)):
            root = probe / f"presence-{present_mask}"
            case_attempts = _standard_attempts(
                root,
                fmt=fmt,
                vtrad=vtrad,
                stems=stems,
                allow_mam_fallback=allow_mam_fallback,
            )
            present = _populate(case_attempts, present_mask)
            expected = next(
                (candidate for candidate in case_attempts if candidate in present), None
            )
            if expected is not None:
                assert (
                    resolve_book_group_path(
                        root,
                        fmt=fmt,
                        vtrad=vtrad,
                        stems=stems,
                        allow_mam_fallback=allow_mam_fallback,
                    )
                    == expected
                )
                continue

            tried = ", ".join(str(path) for path in case_attempts)
            expected_message = (
                f"No MAM-simple {fmt} book group for {vtrad}; tried {tried}"
            )
            with pytest.raises(FileNotFoundError) as caught:
                resolve_book_group_path(
                    root,
                    fmt=fmt,
                    vtrad=vtrad,
                    stems=stems,
                    allow_mam_fallback=allow_mam_fallback,
                )
            assert str(caught.value) == expected_message


def test_custom_book_group_resolution_matches_independent_oracle(tmp_path) -> None:
    case_numbers = count()
    for fmt, stems in product(_FORMATS, _STEM_ORDERS):
        for present_mask in range(1 << len(stems)):
            root = tmp_path / f"custom-{next(case_numbers)}"
            requested = root / "caller-selected"
            attempts = [requested / f"{stem}{_FORMATS[fmt]}" for stem in stems]
            present = _populate(attempts, present_mask)
            expected = next(
                (candidate for candidate in attempts if candidate in present), None
            )
            if expected is not None:
                assert (
                    resolve_book_group_path(
                        root,
                        fmt=fmt,
                        stems=stems,
                        requested_dir=requested,
                    )
                    == expected
                )
                continue

            tried = ", ".join(str(path) for path in attempts)
            expected_message = (
                f"No MAM-simple {fmt} book group in requested directory {requested}; "
                f"tried {tried}"
            )
            with pytest.raises(FileNotFoundError) as caught:
                resolve_book_group_path(
                    root,
                    fmt=fmt,
                    stems=stems,
                    requested_dir=requested,
                )
            assert str(caught.value) == expected_message
            assert "for bhs" not in str(caught.value)
