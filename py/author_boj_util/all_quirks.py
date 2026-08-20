"""Data class for all quirks and related data."""

from dataclasses import dataclass

__all__ = ["AllQuirks"]


@dataclass
class AllQuirks:
    tdm_ch: tuple
    ov_and_de: dict
    qr_groups: dict
