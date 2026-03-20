"""Exports various funs related to survey"""


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


def _union(survey1, survey2, getter):
    return getter(survey1) | getter(survey2)


def _make(ren_tags_seen):
    """Construct a survey structure."""
    return {"_ren_tags_seen": ren_tags_seen}
