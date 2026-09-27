"""Add the public plain-product notice to transient parser-stage data."""

from mb_cmn import public_data_consumer_notice as consumer_notice
from py_misc import mam_parser_stage


def add_header(light_books, source):
    """Build parser-stage data and add the requested public-product notice."""
    return add_consumer_notice(mam_parser_stage.add_header(light_books), source)


def add_consumer_notice(section, source):
    """Return a shallow copy with the public plain-product notice."""
    out_section = dict(section)
    header = dict(section["header"])
    if source == "wikisource":
        header["consumer_notice"] = consumer_notice.mam_parsed_notice("plain")
    elif source != "google":
        raise ValueError(f"unknown MAM-parsed source: {source!r}")
    out_section["header"] = header
    return out_section
