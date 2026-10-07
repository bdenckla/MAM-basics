"""Exports various funs related to survey"""

from mb_cmn import file_io
from mb_cmn import paths


def make():
    """Construct a survey structure."""
    return _make(set())


def add(survey1, survey2):
    """Add two survey structures."""
    return _make(_union(survey1, survey2, get_ren_tags_seen))


def record_ren_tag_seen(survey, one_ren_tag_seen):
    """Record the use of a render tag."""
    survey["_ren_tags_seen"].add(one_ren_tag_seen)


def get_ren_tags_seen(survey):
    """Return the render tags seen."""
    return survey["_ren_tags_seen"]


def unused_ren_tags(handled, seen):
    """The handled render tags not seen, sorted.

    The handled set stays closed: a tag seen that it does not hold raises, as the renderer's
    own lookup already does.  A handled tag that nothing uses any more is not an error but a
    change in the text, which ``write_unused_report`` records where a diff shows it.
    """
    unhandled = set(seen) - set(handled)
    if unhandled:
        raise AssertionError(f"render tags seen but not handled: {sorted(unhandled)}")
    return sorted(set(handled) - set(seen))


def unused_report_path(name):
    """The unused-render-tag report of the generator ``name``."""
    return paths.out_dir() / "render-tags-unused" / f"{name}.json"


def write_unused_report(name, handled, seen):
    """Write the handled render tags not seen to the report of the generator ``name``."""
    file_io.json_dump_to_file_path(
        unused_ren_tags(handled, seen), str(unused_report_path(name))
    )


def _union(survey1, survey2, getter):
    return getter(survey1) | getter(survey2)


def _make(ren_tags_seen):
    """Construct a survey structure."""
    return {"_ren_tags_seen": ren_tags_seen}
