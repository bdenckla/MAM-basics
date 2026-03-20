"""Exports various ren_el constructors & getters"""


def mk_ren_el_t(tag: str):
    """
    Return a render element with only a tag (no contents).
    """
    return {"_ren_tag": tag}


def mk_ren_el_tc(tag, flex_contents):
    """
    Return a render element with contents.
    """
    if isinstance(flex_contents, str):
        contents_tup = (flex_contents,)
    elif isinstance(flex_contents, list):
        contents_tup = tuple(flex_contents)
    else:
        contents_tup = flex_contents
        assert isinstance(flex_contents, tuple)
    return {**mk_ren_el_t(tag), "contents": contents_tup}


def mk_ren_el_tc_and_attr(tag, contents, attr):
    """
    Return a render element with contents and attributes.
    """
    return {**mk_ren_el_tc(tag, contents), "ren_el_attr": attr}


def mk_ren_el_tc_and_doc(doc_target_stripped, doc_lemma, doc_parts):
    """
    Return a render element with contents, a doc lemma, and doc parts.
    """
    return {
        **mk_ren_el_tc("mam-doc", doc_target_stripped),
        "doc_lemma": doc_lemma,
        "doc_parts": doc_parts,
    }


def get_ren_el_tag(ren_el):
    """Return the tag of ren_el."""
    return ren_el["_ren_tag"]


def get_ren_el_tc(ren_el):
    """Return the tag and contents of ren_el."""
    return get_ren_el_tag(ren_el), ren_el["contents"]


def get_ren_el_contents(ren_el):
    """Return contents if they exist."""
    return ren_el.get("contents")


def get_ren_el_attr(ren_el):
    """Return attributes if they exist."""
    return ren_el.get("ren_el_attr")


def ren_el_is_tag_only(ren_el):
    """Return whether the ren_el has only a tag."""
    return tuple(ren_el.keys()) == ("_ren_tag",)


def obj_is_ren_el(obj):
    """Return whether obj is a ren_el."""
    return isinstance(obj, dict) and "_ren_tag" in tuple(obj.keys())
