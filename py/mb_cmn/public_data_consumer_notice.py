"""Canonical warning labels embedded in public structured-data products."""

MAM_PARSED_PLUS_DOCUMENTATION = (
    "https://bdenckla.github.io/MAM-basics/MAM-parsed/plus/html/"
    "mpplus.html#consumer-notice"
)
MAM_SIMPLE_DOCUMENTATION = (
    "https://bdenckla.github.io/MAM-basics/MAM-simple/"
    "reading-mam-simple.html#consumer-notice"
)
LENINGRAD_INDEX_DOCUMENTATION = (
    "https://github.com/bdenckla/MAM-basics/blob/main/"
    "doc/scan-pages.md#codex-entry-indexes"
)
ALEPPO_INDEX_DOCUMENTATION = (
    "https://github.com/bdenckla/MAM-basics/blob/main/"
    "aleppo/README.md#consumer-guide"
)
CAMBRIDGE_INDEX_DOCUMENTATION = (
    "https://github.com/bdenckla/MAM-basics/blob/main/"
    "cam1753/README.md#consumer-guide"
)
EVR_INDEX_DOCUMENTATION = (
    "https://github.com/bdenckla/MAM-basics/blob/main/"
    "evr-ii-b-55/README.md#consumer-guide"
)


def _narpas_grouping_rule(label: str) -> str:
    """The narpas rule, naming narrow-sense paseq as the product itself has it."""
    return (
        f"Narpas (narrow-sense paseq, {label}) forms no compound of any kind: only "
        "maqaf joins atoms into a chanted word. Within the Scripture stream, MAM "
        "encodes no whitespace before or after narpas; that absence expresses "
        "neither grouping nor a display-spacing preference. An edition chooses "
        "whether to display spacing before and/or after narpas, while an analytical "
        "consumer need not make a display-spacing decision."
    )


# MAM-parsed has the template מ:פסק; MAM-simple has the element lp-paseq instead.
MAM_PARSED_NARPAS_GROUPING_RULE = _narpas_grouping_rule("מ:פסק")
MAM_SIMPLE_NARPAS_GROUPING_RULE = _narpas_grouping_rule("lp-paseq")


def _ketiv_qere_rule(structure: str) -> str:
    """The ketiv/qere rule, naming the structure as the product itself has it.

    Ben's decision, 2026-10-16: an edition may show both ketiv and qere, as every
    edition MAM-basics makes except Phonetic MAM does, and one that shows an unpointed
    ketiv beside its pointed qere makes a legitimate editorial decision. So ketiv/qere
    is not among the choices the notice says to resolve.
    """
    return (
        f"{structure} is not a choice that must be resolved: an edition may show its "
        "ketiv and its qere together, separated by a space and kept distinguishable, "
        "as an unpointed ketiv beside its pointed qere is, or only one of them."
    )


# MAM-parsed has ketiv/qere templates; MAM-simple has the element kq instead.
MAM_PARSED_KETIV_QERE_RULE = _ketiv_qere_rule("A ketiv/qere template")
MAM_SIMPLE_KETIV_QERE_RULE = _ketiv_qere_rule("A kq element")

MAM_PARSED_WHITESPACE_TEMPLATE_RULE = (
    "A whitespace template can be the only separator between adjacent Scripture "
    "strings: for example, מ:ששש and ססס can have no literal whitespace at that "
    "boundary. Do not drop the template or collect a descriptive parameter as "
    "Scripture. A plain-text projection that does not preserve layout must supply "
    "a separator; a layout-preserving renderer must implement the documented space "
    "or break. This rule does not apply to narpas, whose missing literal whitespace "
    "prescribes no display spacing."
)


def _gray_maqaf_rule(label: str, what: str) -> str:
    """The gray-maqaf sentences, naming the gray maqaf as the product itself has it.

    Ben's position, 2026-10-20, as relayed to this change: a consumer is free to read MAM's
    gray maqaf as a space, as an ordinary maqaf or as some other kind of maqaf, such as a
    visibly gray one, and is free to drop it and join the atoms on either side of it only at
    its peril, since that is very unlikely to be what anyone wants.  So the sentences permit
    the readings and warn about the drop without forbidding it.
    """
    return (
        f"MAM's gray maqaf ({label}) {what}, and no whitespace stands on either side of "
        "it. A consumer may read it as a maqaf, as a space or as a distinct kind of maqaf, "
        "such as a gray one; a consumer that drops it runs the atoms on either side of it "
        "together into one atom, which is very unlikely to be what it wants."
    )


# MAM-parsed has the template מ:מקף אפור; MAM-simple has the element implicit-maqaf instead.
MAM_PARSED_GRAY_MAQAF_RULE = _gray_maqaf_rule(
    "מ:מקף אפור", "is a template with no parameters"
)
MAM_SIMPLE_GRAY_MAQAF_SENTENCES = _gray_maqaf_rule("implicit-maqaf", "also has no text")


def mam_parsed_notice() -> dict[str, object]:
    """Return the notice for a MAM-parsed-plus payload."""
    return {
        "summary": (
            "This is a structured dataset, not ready-to-display Scripture; interpret "
            "each structure by its documented role and choose a projection wherever "
            "the payload presents alternatives."
        ),
        "critical_rules": [
            (
                "Use a closed, role-aware template dispatch: recurse only through "
                "documented Scripture-bearing fields, and fail on an unknown template "
                "instead of guessing from its parameters or skipping it."
            ),
            (
                "Choose one documented branch of each choice-bearing structure, "
                "including dual cantillation, qamats, and poetic stress-helper "
                "alternatives where present; do not concatenate the branches."
            ),
            MAM_PARSED_KETIV_QERE_RULE,
            (
                "A special-letter template's interrupted spelling and uninterrupted "
                "atom-form are two representations of one atom-form; select one text "
                "representation rather than collecting both."
            ),
            (
                "Reassemble text fragments before identifying atoms or chanted words; "
                "array, template, and element boundaries are not segmentation "
                "boundaries."
            ),
            MAM_PARSED_NARPAS_GROUPING_RULE,
            MAM_PARSED_WHITESPACE_TEMPLATE_RULE,
            MAM_PARSED_GRAY_MAQAF_RULE,
            (
                "For literal search, byte comparison, or MAM-compatible output, "
                "preserve MAM mark order or transform both sides deliberately; "
                "Unicode-normalized text can look identical while comparing "
                "differently."
            ),
        ],
        "documentation": MAM_PARSED_PLUS_DOCUMENTATION,
    }


def mam_simple_notice() -> dict[str, object]:
    """Return the notice shared by every MAM-simple JSON file."""
    return {
        "summary": (
            "This is an extract of MAM, not a complete representation of the "
            "source; consume its documented roles and retained alternatives "
            "explicitly."
        ),
        "critical_rules": [
            (
                "If a requested BHS or Sefaria book-group file is absent, read the MAM "
                "file for that book group and confirm that its "
                "versification-tradition value names the requested tradition."
            ),
            (
                "Use a closed, role-aware element dispatch and fail on an unknown "
                "element; choose one branch where alternatives remain, including "
                "cant-all-three, and do not concatenate note branches or repeated "
                "endings. MAM-simple has already resolved or removed some MAM-parsed "
                "choices, so absence here does not establish absence there."
            ),
            MAM_SIMPLE_KETIV_QERE_RULE,
            (
                "The children of slh-word spell one atom-form and slhw-desc-0 repeats "
                "that atom-form without letter formatting; do not collect both as "
                "running text."
            ),
            (
                "Reassemble fragments before identifying atoms or chanted words; "
                "structural boundaries do not define units of cantillation. An "
                "lp-legarmeih node represents a mark that belongs with the preceding "
                "atom. Narrow-sense paseq (lp-paseq) is not part of the preceding atom."
            ),
            MAM_SIMPLE_NARPAS_GROUPING_RULE,
            (
                "An element with no text can still matter. spi-invnun stands for the "
                "inverted nun, followed by a space when its class is "
                "including-trailing-space. Within a verse, shirah-space and the "
                "parashah markers spi-samekh2, spi-samekh3, spi-pe2 and spi-pe3 can be "
                "the only separator between adjacent Scripture strings, with no literal "
                "whitespace at that boundary. Do not drop such an element. A plain-text "
                "projection that does not preserve layout must supply the inverted nun "
                "and each such separator; a layout-preserving renderer must implement "
                "the documented space or break. " + MAM_SIMPLE_GRAY_MAQAF_SENTENCES
            ),
            (
                "For a break between verses, the parashah marker and the adjacent "
                "starts-with-sampe and ends-with-sampe fields describe one break, "
                "not three."
            ),
            (
                "For literal search, byte comparison, or MAM-compatible output, "
                "preserve MAM mark order or transform both sides deliberately; "
                "Unicode-normalized text can look identical while comparing "
                "differently."
            ),
        ],
        "documentation": MAM_SIMPLE_DOCUMENTATION,
    }


def codex_index_notice(documentation: str) -> dict[str, object]:
    """Return the notice for one of the four public manuscript entry indexes."""
    if documentation not in {
        LENINGRAD_INDEX_DOCUMENTATION,
        ALEPPO_INDEX_DOCUMENTATION,
        CAMBRIDGE_INDEX_DOCUMENTATION,
        EVR_INDEX_DOCUMENTATION,
    }:
        raise ValueError(f"unknown codex-index documentation URL: {documentation!r}")
    return {
        "summary": (
            "This file is a locator index, not a manuscript transcription or a Bible "
            "edition."
        ),
        "critical_rules": [
            (
                "Text ranges and text cues locate content on photographed pages; they "
                "must not be cited as a diplomatic transcription of the manuscript."
            ),
            (
                "Gaps and mid-verse boundaries are meaningful locator evidence; do not "
                "round them to whole verses or fill them from another edition."
            ),
            (
                "Line-break and page-geometry annotations are separate supporting data; "
                "do not infer either from this entry index."
            ),
        ],
        "documentation": documentation,
    }
