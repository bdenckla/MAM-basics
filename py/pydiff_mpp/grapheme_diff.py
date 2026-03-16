"""Grapheme-cluster diffing utilities.

Split text into grapheme clusters (base char + combining marks) and
produce HTML with ``<mark>`` tags around clusters that differ.

Pure stdlib — depends only on ``unicodedata`` and ``difflib``.
"""

import difflib
import html
import unicodedata


def grapheme_clusters(text):
    """Split *text* into grapheme clusters (base char + combining marks)."""
    clusters = []
    current = []
    for ch in text:
        if unicodedata.category(ch).startswith("M") and current:
            current.append(ch)
        else:
            if current:
                clusters.append("".join(current))
            current = [ch]
    if current:
        clusters.append("".join(current))
    return clusters


def char_diff_spans(text_a, text_b):
    """Return (html_a, html_b) with differing clusters wrapped in <mark>."""
    clusters_a = grapheme_clusters(text_a)
    clusters_b = grapheme_clusters(text_b)
    sm = difflib.SequenceMatcher(None, clusters_a, clusters_b, autojunk=False)
    parts_a, parts_b = [], []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        a_chunk = html.escape("".join(clusters_a[i1:i2]))
        b_chunk = html.escape("".join(clusters_b[j1:j2]))
        if tag == "equal":
            parts_a.append(a_chunk)
            parts_b.append(b_chunk)
        else:
            if a_chunk:
                parts_a.append(f'<mark class="diff-hi">{a_chunk}</mark>')
            if b_chunk:
                parts_b.append(f'<mark class="diff-hi">{b_chunk}</mark>')
    return "".join(parts_a), "".join(parts_b)
