from pyauthor_rocc import rocc_util as ru


_CPARA = "Now let’s look at במתג ורסן in Psalm 32:9:"
_TABLE_DATA = {
    "$CTR, $JP": ("בְּמֶ֣תֶג וָ֭רֶסֶן", "$munax, $dexi"),
    "$MAM": ("בְּמֶתֶג־וָרֶ֣סֶן", "$maqaf, $munax"),
    "$KCT, $WMG, $SBB": ("בְּמֶֽתֶג־וָרֶ֣סֶן", ru.aeq("$MAM")),
}
_CPARA_2 = [
    ["Most of the accent differences presented so far"],
    [" involve two conjunctive accents or"],
    [" involve a conjunctive accent and $maqaf"],
    [" (the lack of an accent)"],
    [" (the formation of a compound word)."],
    [" But here the difference involves"],
    [" a disjunctive accent ($dexi$hairsp) and"],
    [" a conjunctive accent ($munax)."],
    [" A difference like this is generally considered"],
    [" to be a more significant difference"],
    [" than a conjunctive vs. conjunctive difference or"],
    [" a conjunctive vs. $maqaf difference."],
]
ARGS = _CPARA, _TABLE_DATA, [_CPARA_2]
