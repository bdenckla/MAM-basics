from pycmn import ws_tmpl2 as wtp


def unbury_parts(doc_parts_wtseqs):
    return _unbury_parts(doc_parts_wtseqs[0]) + doc_parts_wtseqs[1:]


def _unbury_parts(new_farg):
    parts = [[]]
    for wtel in new_farg:
        if _is_shin_tmpl(wtel):
            parts.append([])
            continue
        parts[-1].append(wtel)
    return parts


def _is_shin_tmpl(wtel):
    return wtp.is_template_with_name(wtel, "ש")
