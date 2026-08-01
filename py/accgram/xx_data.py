from py_html import wlc_utils_html


def github_issue_comment_item(href):
    """A comment item pointing to a word’s GitHub issue, linked as “GitHub issue”
    just as the same issue is linked above the comment."""
    link = wlc_utils_html.anchor("GitHub issue", {"href": href})
    return wlc_utils_html.para(
        ("See the ", link, " regarding this word."),
        {"class": "goerwitz-tms-comment"},
    )
