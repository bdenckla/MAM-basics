import mb_cmn.bib_locales as tbn
import mb_cmn.cantsys as cantsys
import phonetic_mam.core.summary_of_accents as accsum


def mk_dtx_with_bcvt(dtx, bcvt):
    return {**dtx, "dtx-bcvt": bcvt}


def mk_dtx_with_qamats(dtx, bcvt):
    return {**dtx, "dtx-qamats": bcvt}


def suppress_edition_census(dtx):
    """Return a context whose alternative must not enter the edition census.

    Both qamats variants and both cantillation strands remain in the phonetic
    products.  The accent census instead describes one implied edition: it uses
    the ``ד`` qamats variant and the ``א`` (taḥton) cantillation strand.  The
    caller applies this flag to the unused alternative while still producing
    that alternative's phonetic data.
    """
    return {**dtx, "dtx-include-in-edition-census": False}


def include_in_edition_census(dtx):
    return dtx.get("dtx-include-in-edition-census", True)


def get_bcvt(dtx):
    return dtx.get("dtx-bcvt")


def get_qamats(dtx):
    return dtx.get("dtx-qamats")


def get_bcv_str(dtx):
    return tbn.short_bcv_of_bcvt(get_bcvt(dtx))


def get_cantsys(dtx):
    bcvt = get_bcvt(dtx)
    is_poetcant = tbn.is_poetcant(bcvt)
    the_cantsys = cantsys.get_cantsys_from_is_poetcant(is_poetcant)
    return the_cantsys


def make_context(cooked_uts, *, lookup_keys=None):
    use_counts = {word: 0 for word in cooked_uts.keys()}
    dtx = {
        "dtx-dualcant-untanglers": cooked_uts,
        "dtx-untangler-lookup-keys": lookup_keys or {},
        "dtx-out-dualcant-untanglers-use-counts": use_counts,
        "dtx-out-cs-hccvec-seen-counts": accsum.empty_cs_seen_counts(),
        "dtx-out-cs-hccvec-seen-examples": accsum.empty_cs_seen_examps(),
    }
    return dtx
