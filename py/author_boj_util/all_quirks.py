"""Data class for all quirks and related data."""

from dataclasses import dataclass, field

__all__ = ["AllQuirks"]


@dataclass
class AllQuirks:
    tdm_ch: tuple
    ov_and_de: dict
    qr_groups: dict
    # The group keys that pages have listed through para_and_table, which adds each
    # one, for get_qr_groups.check_every_quirkrec_presented.
    listed_groups: set = field(default_factory=set)
