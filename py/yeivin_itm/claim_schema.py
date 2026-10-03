"""Closed claim contract and pins for the statements Ben approved.

The fraction pins are review gates for the existing prose, not survey inputs.
Changing a fraction or a record of the claim population requires inspecting both
the data and prose.
"""

import re

SCHEMA = "yeivin-meteg-claims-v1"
INPUT_IDENTITY = "out/accgram/meteg-before-stress.json"

# The claim population: every ordinary-qamats record of the analysis whose pattern is one
# of these, the records the claims and their footnotes are drawn from.  Its SHA-256, which
# claims.population_sha256 computes, is pinned; the claim file's input SHA-256 identifies
# the whole analysis file as provenance and is not a pin.
CLAIM_PATTERNS = ("FR1", "FR2", "FR3", "AFR1", "AFR4", "XAFR1")
APPROVED_POPULATION_SHA256 = (
    "452c78e4aab25cefc932bd3f6eb0aafa1e36e5f272fcb7240ce63dd008322653"
)

# Exact reviewed fractions, including the primary-accent qualifications in §320.
APPROVED_FRACTIONS = {
    "fully-regular.all": (3583, 3583),
    "fully-regular.disjunctive-without-target-meteg": (134, 3583),
    "fully-regular.conjunctive-with-target-meteg": (210, 3583),
    "fully-regular.exceptions": (344, 3583),
    "fully-regular.disjunctive-without-target-meteg.other-meteg": (33, 134),
    "fully-regular.disjunctive-without-target-meteg.qadma-or-metigah": (6, 134),
    "fully-regular.disjunctive-without-target-meteg.merkha": (3, 134),
    "fully-regular.disjunctive-without-target-meteg.metigah": (6, 134),
    "fully-regular.disjunctive-without-target-meteg.merkha-with-azla-legarmeh": (
        2,
        134,
    ),
    "FR1.conjunctive-with-target-meteg": (80, 283),
    "FR2.conjunctive-with-target-meteg": (99, 493),
    "FR3.conjunctive-with-target-meteg": (31, 610),
    "fully-regular.disjunctive-exception-rate": (134, 2197),
    "fully-regular.target-meteg-rate": (2273, 3583),
    "AFR1.disjunctive-exception-rate": (20, 107),
    "AFR1.target-meteg-rate": (89, 137),
    "AFR4.disjunctive-exception-rate": (72, 129),
    "AFR4.target-meteg-rate": (60, 173),
    "XAFR1.disjunctive-with-target-meteg": (2, 18),
    "XAFR1.disjunctive-without-target-meteg": (16, 18),
}


def _keys(value, expected, where):
    if not isinstance(value, dict) or set(value) != set(expected):
        raise ValueError(f"Invalid claim keys at {where}")


def validate(claims):
    """Reject unknown fields, malformed fractions, and prose-disagreeing data."""
    validate_shape(claims)
    pin_claims(claims)


def validate_shape(claims):
    """Reject unknown fields and malformed fractions, whatever their values."""
    _keys(claims, ("schema", "input", "populations", "measurements"), "root")
    if claims["schema"] != SCHEMA:
        raise ValueError("Unknown Yeivin meteg claim schema")
    _keys(claims["input"], ("identity", "sha256"), "input")
    source = claims["input"]
    if source["identity"] != INPUT_IDENTITY or not isinstance(source["sha256"], str):
        raise ValueError("Invalid independent meteg analysis identity")
    if not re.fullmatch(r"[0-9a-f]{64}", source["sha256"]):
        raise ValueError("Invalid independent meteg analysis hash")
    _keys(claims["populations"], APPROVED_FRACTIONS, "populations")
    _keys(claims["measurements"], APPROVED_FRACTIONS, "measurements")
    for name, fraction in claims["measurements"].items():
        _keys(fraction, ("numerator", "denominator", "percentage"), name)
        numerator, denominator = fraction["numerator"], fraction["denominator"]
        if (
            type(numerator) is not int
            or type(denominator) is not int
            or not 0 <= numerator <= denominator
            or denominator == 0
        ):
            raise ValueError(f"Invalid integer fraction: {name}")
        if (
            type(fraction["percentage"]) not in (float, int)
            or fraction["percentage"] != 100 * numerator / denominator
        ):
            raise ValueError(f"Percentage does not match the exact fraction: {name}")
        population = claims["populations"][name]
        _keys(population, ("definition", "exclusions"), f"population {name}")
        if (
            not isinstance(population["definition"], str)
            or not population["definition"]
        ):
            raise ValueError(f"Missing population definition: {name}")
        exclusions = population["exclusions"]
        if (
            not isinstance(exclusions, list)
            or not exclusions
            or any(not isinstance(item, str) or not item for item in exclusions)
        ):
            raise ValueError(f"Missing population exclusions: {name}")


def pin_claims(claims):
    """Fail if a new fraction would silently alter the approved argument."""
    for name, expected in APPROVED_FRACTIONS.items():
        value = claims["measurements"][name]
        if (value["numerator"], value["denominator"]) != expected:
            raise ValueError(f"Ben's prose pin changed: {name}; review the footnotes")


def pin_population(population_sha256):
    """Fail if a claim-population record changed, was added or was removed."""
    if population_sha256 != APPROVED_POPULATION_SHA256:
        raise ValueError("The claim population has changed; review Ben's claims")
