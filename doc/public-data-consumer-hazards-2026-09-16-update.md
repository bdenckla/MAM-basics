# Public-data consumer hazards audit, 2026-09-16 — update

State: finished audit update. This receipt supplements
`public-data-consumer-hazards-2026-09-16.md` and remains the family's single update
file while the base receipt is tracked.

## Correction to “Ten accepted hazards”

The base receipt's “Ten accepted hazards” section omitted an eleventh hazard. Item 5,
“Structural boundaries are not segmentation boundaries,” records the related failure
in which a separate MAM-simple node representing either narrow-sense paseq or legarmeh
was treated as a chanted word. Item 5 does not record what MAM's lack of whitespace
around narpas means, and the embedded notice produced from the base receipt did not
state that meaning.

## Eleventh accepted hazard

11. **Absent whitespace around narpas is neither a grouping instruction nor a spacing
    policy.** Narpas is narrow-sense paseq (׀). MAM encodes its paseq template with no
    text whitespace before or after it. Narpas forms no compound of any kind; in
    particular, it forms neither a maqaf compound nor a separate category of “paseq
    compound.” Only maqaf joins atoms into a chanted word. MAM omits the whitespace to
    avoid choosing how an edition spaces the mark, not to group the surrounding text.
    An edition decides whether to display spacing before and/or after narpas; an
    analytical consumer need not make a display-spacing decision.

    Commit `753b9b2d8483325f4e08b509d687ea2ccae2017c`, “near-aleppo step 27 of
    41: INVERT-STEP the legarmeh split, ending tier 1,” measured the then-current
    representation: none of its 508 narrow-sense-paseq template sites had whitespace
    in either adjacent literal string. Commit
    `757aa68af33e8f71d96e3407db7d78111f8ba55f`, “Give a
    param-less template a separator, and correct Joshua 10:12's form,” documented the
    consumer consequence: treating the template as empty fused the atoms on its two
    sides, while an atom-counting consumer had to supply a separator without deciding
    how an edition should render the template. Commit
    `9fa80e1162c8dc9a0c3f9a93dd1507ca755d92f3`, “Add the diff-ctr-vs-mam step,
    and a handler for the narrow-sense paseq template,” supplied a space in one flat
    comparison projection because the source representation deliberately supplied
    none.

    Failure mode: invented grouping, including an invented “paseq compound,” or an
    accidental display-spacing policy. Audience: generic external consumers and
    MAM-internal reproducers. Destination: embedded MAM-parsed and MAM-simple notices
    and adjacent documentation.

## Resulting notice-policy correction

The base receipt's “Resulting notice policy” remains in force, with this addition:
both Scripture-data notices must say that narpas forms no compound of any kind, that
only maqaf joins atoms into a chanted word, and that MAM's lack of whitespace around
narpas prescribes neither grouping nor display spacing. The adjacent documentation
must distinguish an edition's display-spacing choice from an analytical consumer that
needs no display-spacing choice.

## Further correction to the accepted-hazard list

The base receipt's “Ten accepted hazards” section and this update's eleventh hazard do
not separately record a demonstrated failure involving MAM-parsed whitespace
templates. The base receipt's first hazard records the opposite failure: generic
parameter walking inserted parashah-marker documentation into Scripture. The eleventh
hazard records that narpas is not a whitespace template and forms no compound of any
kind. Neither statement says what a consumer must do when a template itself represents
whitespace or layout but the adjacent strings contain no literal whitespace.

## Twelfth accepted hazard

12. **A whitespace template can be the only separator between adjacent Scripture
    strings.** In MAM-parsed, templates such as `מ:ששש` and `ססס` can sit between
    strings whose boundary has no literal whitespace. Dropping such a template as
    “empty” fuses separate atoms. A plain-text projection that does not preserve
    layout must supply at least one separator; a layout-preserving renderer must
    implement the template's documented space or break. A consumer must not instead
    collect a descriptive parameter such as `פסקא באמצע פסוק` as Scripture.

    Commit `fce03759a263a5380beba66750548cc474370b4e`, “Ingest Holman's suggested
    corrections to MAM,” found the omission direction in
    `py/hkq_cmn/mam_plus_verse_data.py`: a whitespace template contributed nothing,
    so the shirah spaces in Judges 5:6 fused the atoms on either side. The verse
    counted 11 atoms instead of 13, making two correct external atom indexes appear
    wrong. Commit `757aa68af33e8f71d96e3407db7d78111f8ba55f`, “Give a param-less
    template a separator, and correct Joshua 10:12's form,” generalized the separator
    rule. Commit `147e9e4fb52655203b042aa909521c6d755ec04e`, “Dispatch on what a
    template MEANS, not on whether it carries parameters,” then closed the other
    direction: a parameter-bearing `ססס` had contributed the three documentation
    atoms `פסקא באמצע פסוק`, fused to the Scripture strings on both sides. Commit
    `d8442efda42212ad7cb1b8432f71efdfdacb7e5a`, “Remove the fallback too: a
    template is named, or it raises,” made the current prevention explicit and
    fail-fast in `py/mb_cmn/template_names.py:NO_ATOM_TMPL_NAMES`.

    This rule differs from the eleventh hazard. A whitespace template semantically
    supplies separation or layout even when no literal whitespace surrounds its
    object. Narpas semantically supplies a mark, not whitespace; MAM's lack of
    whitespace around narpas prescribes neither grouping nor display spacing.

    Failure mode: fused atoms when the template is dropped, or contaminated Scripture
    when its documentation is collected. Audience: generic external consumers and
    MAM-internal reproducers. Destination: the embedded MAM-parsed notice and adjacent
    MAM-parsed documentation.

## Further resulting notice-policy correction

The prior notice policy remains in force, with this addition: the MAM-parsed notice
must say that a documented whitespace or layout template can be the only separator
between adjacent Scripture strings. It must require a plain-text projection to supply
a separator and a layout-preserving renderer to implement the documented space or
break. It must distinguish that positive whitespace meaning from narpas, whose absent
literal whitespace expresses no display-spacing policy.
