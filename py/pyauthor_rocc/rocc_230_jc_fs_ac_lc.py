from pyauthor_rocc import rocc_util as ru


X01_CPARA_JC_AND_FS_INTRO = [
    ["Two other editions deserve some mention and comparison:"],
    [" the Jerusalem Crown ($JC)"],
    [" and the Feldheim Simanim ($FS) editions."],
    [" They are so close to $MAM that I have not listed them above."],
    [" Yet, they differ from $MAM in some small ways that are worth listing here."],
]
X02_TABLE_DATA_AJRY = {
    "$MAM, $FS": (ru.gray_abg_adm("אשרי־"), "$maqaf"),
    "$JC, $AC, $LC": (ru.gray_abg_adm("אשרי" + " "), "space"),
}
X03_TABLE_DATA_KY = {
    "$MAM, $JC, $AC, $LC": (ru.gray_abg_hxrjty("כֽי־"), "$gaya"),
    "$FS": (ru.gray_abg_hxrjty("כי־"), "no $gaya"),
}
X04_TABLE_DATA_LRJ3 = {
    "$MAM": ("ל֫רשע", "$oleh on $lamed"),
    "$JC, $FS, $AC, $LC": ("לר֫שע", "$oleh on $resh"),
}
_X05A_CPARA = [
    ["Some manuscripts and editions have a $gaya"],
    [" where $MAM has neither a $gaya nor an accent:"],
]
X05B_TABLE_DATA = [
    ("$JC, $FS", "וֽעוני", "(absent in $AC, $LC, & $MAM)"),
    ("$JC, $FS, $LC", "אל־תֽהיו", "(absent in $AC & $MAM)"),
    ("$JC, $FS, $LC", "במֽתג־ורסן", "(absent in $AC & $MAM)"),
    ("$JC, $FS", "לֽרשע", "(absent in $AC, $LC, & $MAM)"),
]
X05C_CPARA_2 = [
    ["Regarding $JC ..."],
    [" In the four cases of $gaya above, $JC uses a small $gaya."],
    [" This small $gaya is an aid to reading"],
    [" that is not supplied by the $AC."],
    [" Thus one could say that in these words, $JC sort of splits the difference"],
    [" between $MAM and the many other editions that have a $gaya (of full size)."],
]
X_05_ARGS_MISC_GAYA = (
    _X05A_CPARA,
    X05B_TABLE_DATA,
    [X05C_CPARA_2],
)
