"""The hand-encoded oracle of the CLC dual-cantillation strand splitter (§7.7).

``clc_dual_cant`` splits UXLC's combined form of each dual-cantillation verse into
its alef and bet strands. ``_ORACLE`` is the one place it learns which of two
combined marks belongs to which strand, where a supplied break falls, and which
accent a strand wants where UXLC has only the other's: MAM consulted as the
oracle, encoded once, by hand, with nothing of MAM's text imported. The comments
inside ``_ORACLE`` record how each verse's entries were derived and cross-checked.
``_validate_oracle`` runs when this module is imported, so a malformed entry stops
the build before any strand is split.

Terminology note: below, "pasoleg" (echoing the PASOLEG constant, hpu.PASOLEG -- a
paseq+legarmeh portmanteau) names the raw U+05C0 character itself, independent of whether
it functions as narrow-sense paseq or legarmeh -- exactly the ambiguity §7.16 is about.
Comments here use it whenever code is manipulating that character positionally (counting,
subtracting, tokenizing) without asserting anything about its grammatical identity; bare
"paseq" is reserved for the narrow sense, and "legarmeh" always means legarmeh.
"""

import mb_cmn.hebrew_accents as acc
import mb_cmn.hebrew_letters as hl
import mb_cmn.hebrew_points as hpo
import mb_cmn.hebrew_punctuation as hpu
from mb_cmn import str_defs as sd
import mb_diff_mpu.describe_diff as describe_diff

# Combining grapheme joiner: a control char (no textual meaning) used in the
# combined form only to sequence two combined accents. Once a single accent
# remains it has nothing to sequence, so a strand drops it (cf. §7.14). It lives
# inside a divergence cluster (atom 14) and simply isn't in either resolution.
_CGJ = sd.CGJ

_STRAND_ALEF = "alef"
_STRAND_BET = "bet"

# The closed set of marks a strand may have SUPPLIED (the additive charity) — only
# accent-coupled *punctuation*. An accent UXLC omitted is NEVER supplied;
# it is recorded as an omitted-accent note (see _OMITTABLE / _omitted_note). Legarmeh is
# suppliable in principle (the third punctuation mark, §7.7) but never arises in the
# Decalogues — there it is only ever suppressed — so it is not in this set yet.
_SUPPLIABLE = {hpu.MAQ, hpu.SOPA}
# Display names for a supplied mark, used in the synthesized doc-column note.
_ADDED_NAME = {hpu.MAQ: "maqaf", hpu.SOPA: "sof pasuq"}


def _is_accent(ch):
    """An accent (U+0591–U+05AF) or the meteg/silluq mark (U+05BD)."""
    return 0x0591 <= ord(ch) <= 0x05AF or ch == hpo.MTGOSLQ


# The hardcoded oracle. For each dual-cant verse, map a 1-based atom index (only
# the *divergence* words, where the two strands each mark a letter) to a resolution:
#
#   atom_index -> {
#       "cluster": exact combined substring that diverges (incl. CGJ if present),
#       "alef":    the cluster's alef resolution (a subsequence of "cluster"),
#       "bet":     the cluster's bet  resolution (a subsequence of "cluster"),
#       "add":     optional {strand: [char, ...]} of maqaf/sof-pasuq SUPPLIED to
#                  that strand (rendered bracketed/green + a synthesized note),
#       "omit":    optional {strand: [accent, ...]} an accent that strand's chanting
#                  wants but UXLC omitted — NOTED, never supplied (so it is NOT in
#                  the strand's text; just a synthesized note). Accents only.
#   }
#
# Building a strand replaces "cluster" with that strand's resolution at its exact
# site (position-safe — a recurrence of any constituent mark elsewhere is left
# alone) and appends any supplied marks. Clusters/resolutions are spelled from
# named mark constants so the (invisible, combining) bytes are legible and match
# UXLC byte-for-byte — guarded by _validate_oracle() at import and by the
# `cluster in combined_text` assert in split_word. Every atom not listed carries
# a single shared mark and is left byte-for-byte.
#
# Genesis 35:22 (clusters derived by diffing UXLC's combined words against the
# alef/bet strands; cross-checked to reproduce the prior accent-only split):
#
#   atom  combined word   alef keeps              bet keeps
#   ----  --------------  ---------------------   ---------------------
#    7    רְאוּבֵ֔֗ן        zaqef qatan  U+0594     revia        U+0597
#    8    וַיִּשְׁכַּ֕ב֙      zaqef gadol  U+0595     pashta       U+0599
#   10    בִּלְהָ֖ה֙         tipexa       U+0596     pashta       U+0599
#   12    אָבִ֑֔יו          etnaxta      U+0591     zaqef qatan  U+0594
#   14    יִשְׂרָאֵ֑͏ֽל       meteg/silluq U+05BD     etnaxta      U+0591  (CGJ dropped)
#         + alef ALSO gains a supplied sof-pasuq — pashut chants this as a verse end.
_ORACLE = {
    "Genesis": {
        (35, 22): {
            7: {"cluster": acc.ZAQ_Q + acc.REV, "alef": acc.ZAQ_Q, "bet": acc.REV},
            8: {
                "cluster": acc.ZAQ_G + hl.BET + acc.PASH,
                "alef": acc.ZAQ_G + hl.BET,
                "bet": hl.BET + acc.PASH,
            },
            10: {
                "cluster": acc.TIP + hl.HE + acc.PASH,
                "alef": acc.TIP + hl.HE,
                "bet": hl.HE + acc.PASH,
            },
            12: {"cluster": acc.ATN + acc.ZAQ_Q, "alef": acc.ATN, "bet": acc.ZAQ_Q},
            14: {
                "cluster": acc.ATN + _CGJ + hpo.MTGOSLQ,
                "alef": hpo.MTGOSLQ,
                "bet": acc.ATN,
                "add": {_STRAND_ALEF: [hpu.SOPA]},
            },
        },
    },
    # The Decalogues (Exodus 20, Deuteronomy 5), taxton (alef) / elyon (bet). Derived from
    # MAM-simple's cant-alef / cant-bet strands (the oracle) diffed against UXLC's combined
    # atoms by a throwaway generator (since retired), then self-verified by simulating split_word.
    # Punctuation
    # tracks accents: where a strand keeps a NON-silluq final accent (e.g. etnaxta) while
    # the other keeps silluq, the sof-pasuq is SUPPRESSED in the non-silluq strand — it
    # appears only on a silluq word (e.g. ex 20:2 atom 9: elyon keeps silluq + sof-pasuq,
    # taxton keeps etnaxta with the sof-pasuq removed; ex 20:5 atom 21 is the mirror).
    # Encoded so far: the pure-accent (+ sof-pasuq-suppression) verses; ex 20:8 / ex 20:9
    # whose taxton verse-end SUPPLIES a sof-pasuq UXLC omitted (the additive charity); the
    # rafe/dagesh verses (ex 20:9,13–15; dt 5:13,17,18,19) where the two strands harden/soften a
    # בגדכפת letter — the hard strand keeps UXLC's dagesh, the soft keeps UXLC's rafe (faithful,
    # Policy 1; bare where UXLC has no rafe, as in ex 20:9 כל); the OMITTED-accent verses
    # (dt 5:6,13,17) where UXLC has only one strand's accent and the other's is NOTED, never
    # supplied (Ben's policy — see the "omit" field and _omitted_note); the QUPO vowel-split
    # verses (ex 20:3, dt 5:7) where the two strands have DIFFERENT vowels (patax vs. qamats) on
    # one letter — the same position-safe subtraction bucket as rafe/dagesh (see ex 20:3's own
    # comment below); and the pasoleg-tokenization verses (ex 20:4,10; dt 5:8,12,14,15, UXLC-utils#29) —
    # MAM-simple tokenizes a standalone pasoleg (see the module docstring's terminology note)
    # as its own word where UXLC embeds it directly in the preceding word's atom, which looked
    # like a real word-count divergence until a throwaway harvest script (since retired) folded it
    # UXLC does; once folded, the pasoleg is an ordinary divergent mark (present in one strand's
    # atom text, absent from the other) and flows through the same position-safe subtraction
    # path as every other mark class — no new runtime mechanism. (UXLC-utils#29 also closed UXLC-utils#28's open
    # מתחת question: the count mismatch in ex 20:4 / dt 5:8 comes from a pasoleg elsewhere in
    # the verse — atoms 4, 8, 14 — not from מתחת; ex 20:4's first מתחת occurrence, atom 12, IS a
    # third QUPO vowel-split case, same shape as פני; its second occurrence, atom 15, is a plain
    # two-accent divergence; dt 5:8's twin atom 12 is NOT QUPO there — an ordinary cross-book
    # textual difference between the two verses.) dt 5:16 was also a pasoleg-tokenization count
    # mismatch, but resolves to NO
    # divergence at all: once folded, its taxton/elyon strands are byte-identical for every word
    # (both keep the same lone pasoleg), so it correctly carries no oracle entry — is_dual_cant()
    # is False for it, unlike its 6 siblings above.
    #
    # MAM cross-check (issues UXLC-utils#43/UXLC-utils#44) — VALIDATION ONLY: MAM was consulted as an independent
    # signal (harvested by hand via a throwaway script, since retired, from
    # MAM-parsed/plus), the oracle needed no change, and NOTHING of MAM is rendered inline or
    # embedded at runtime. MAM's per-witness sof-pasuq collation confirms L is among the
    # witnesses LACKING the taxton sof-pasuq at all five Exodus sites this oracle SUPPLIES one
    # (ex 20:3/4/8/9/10 = MAM 20:2/3/7/8/9), grounding the charitable "L's taxton strand ends no
    # verse here" claim; the apparent red-flag verses where MAM has L among those WITH the taxton
    # sof-pasuq (dt 5:8/5:9) are consistent — CLC keeps UXLC's own sof-pasuq there and supplies
    # none. MAM's two-marks-on-one-letter doc-notes corroborate the QUPO vowel assignment
    # (dt 5:7 פני = קמץ+silluq taxton / patax elyon; ex 20:4 מתחת = קמץ+atnax taxton / patax+azla
    # elyon) and, at dt 5:8 מתחת, MAM's own text follows the witness WITHOUT the extra patax —
    # corroborating this oracle's NON-QUPO treatment there. (dt 5:7/5:12's supplied sof-pasuqs
    # carry no per-witness MAM note in the harvest, so they stay uncorroborated.) See §7.7.
    #
    # MAM cross-check (issue UXLC-utils#42) — VALIDATION ONLY, legarmeh-vs-paseq (§7.16) + pisqah (§7.7):
    # the raw pasoleg (U+05C0) bars this oracle subtracts positionally (the "Unicode-PASEQ
    # tokenization" atoms — ex 20:4 atoms 4/8/14, ex 20:10 atoms 3/10; dt 5:8 atoms 4/8/14,
    # dt 5:12 atom 7, dt 5:14 atom 3, dt 5:15 atom 4) each carry a legarmeh-vs-paseq grammatical
    # identity this oracle never needed: subtraction is identity-agnostic (same bytes either way,
    # §7.16). MAM adjudicates it explicitly — מ:לגרמיה-2 = legarmeh, מ:פסק = narrow paseq — and its
    # 15 Decalogue tags (11 legarmeh, 4 paseq) map 1:1 onto these sites: legarmeh on במים / שבת /
    # אתה / צוך / היית; paseq on פסל and בשמים (both Decalogues). ex 20:4's בשמים carries its מ:פסק
    # tag NESTED as the target (param 1) of a נוסח note recording L's disputed stroke — tagged, just
    # one level deeper (the throwaway harvest first mis-filed it as a ‖ נוסח note until its scan was
    # taught to recurse into נוסח targets; there is no Exodus/Deuteronomy tagging asymmetry). accgram
    # (wlc-utils/py/accgram prose scanner) is an INDEPENDENT classifier of the same distinction
    # (munax+paseq before revia = legarmeh, else narrow paseq; no Decalogue verse sits in its
    # has_legarmeh 17-passage list, so the rule reduces to before-revia here) — but only truly
    # independent on the ORDINARY prose run; in the dual-cant loci its detangler takes strand
    # punctuation FROM MAM, so there it concurs rather than witnesses. Three more legarmeh
    # (dt 5:4 פנים, 5:25 יספים, 5:27 ואת) sit on ordinary single-cant rows, not strands — the
    # natural surface for a future rendered §7.16 note (deferred to UXLC-utils#37, legarmeh visual
    # representation); a fourth, dt 5:16 למען, sits on the folded byte-identical verse (both strands
    # keep the bar — the reason it correctly carries no _ORACLE entry). MAM's pisqah-be'emtsa-pasuq
    # markings (×8, strand-tagged) corroborate the taxton verse-internal breaks this oracle already
    # handles inside elyon's merged coveting verse (ex 20:13/14/15, dt 5:17/18/19). No bytes change
    # and nothing of MAM is rendered or embedded. See §7.16.
    "Exodus": {
        (20, 2): {
            1: {
                "cluster": acc.TIP + hl.YOD + acc.PASH,
                "alef": hl.YOD + acc.PASH,
                "bet": acc.TIP + hl.YOD,
            },
            3: {"cluster": acc.ATN + acc.ZAQ_Q, "alef": acc.ZAQ_Q, "bet": acc.ATN},
            8: {"cluster": acc.MUN + acc.MER, "alef": acc.MUN, "bet": acc.MER},
            9: {
                "cluster": acc.ATN + _CGJ + hpo.MTGOSLQ + hl.YOD + hl.FMEM + hpu.SOPA,
                "alef": acc.ATN + hl.YOD + hl.FMEM,
                "bet": hpo.MTGOSLQ + hl.YOD + hl.FMEM + hpu.SOPA,
            },
        },
        # ex 20:3 — the QUPO vowel split, the last of the Decalogue's divergence mechanisms.
        # Atom 7 פָּנָ֗י ("before me"): the נ carries both QAMATS and PATAX, sequenced by a
        # CGJ (same shape as Gen 35:22 atom 14) — taxton (alef) keeps qamats + meteg, elyon (bet)
        # keeps patax + revia; pure position-safe subtraction, exactly like rafe/dagesh. Atom 7
        # also SUPPLIES a sof-pasuq (taxton ends the verse here; UXLC has none). Atom 1 לא
        # SUPPLIES the first-ever maqaf in the Decalogues: taxton joins it to the next word
        # (לא־יהיה) where UXLC does not. Atom 2 יהיה: taxton's merkha is OMITTED (UXLC left it
        # untangled, noted not supplied). Atoms 3–5 are pure-accent.
        (20, 3): {
            1: {
                "cluster": hpo.MTGOSLQ + acc.MUN,
                "alef": hpo.MTGOSLQ,
                "bet": acc.MUN,
                "add": {_STRAND_ALEF: [hpu.MAQ]},
            },
            2: {
                "cluster": hpo.MTGOSLQ + hl.HE + hpu.MAQ,
                "alef": hl.HE,
                "bet": hpo.MTGOSLQ + hl.HE + hpu.MAQ,
                "omit": {_STRAND_ALEF: [acc.MER]},
            },
            3: {"cluster": acc.TEV + acc.TEL_Q, "alef": acc.TEV, "bet": acc.TEL_Q},
            4: {"cluster": acc.MER + acc.QOM, "alef": acc.MER, "bet": acc.QOM},
            5: {"cluster": acc.TIP + acc.GER, "alef": acc.TIP, "bet": acc.GER},
            7: {
                "cluster": hpo.QAMATS + hpo.MTGOSLQ + _CGJ + hpo.PATAX + acc.REV,
                "alef": hpo.QAMATS + hpo.MTGOSLQ,
                "bet": hpo.PATAX + acc.REV,
                "add": {_STRAND_ALEF: [hpu.SOPA]},
            },
        },
        # ex 20:4 — the first pasoleg-tokenization verse (UXLC-utils#29). Atoms 4/8/14 (פסל/בשמים/במים)
        # each end in a pasoleg that ONE strand keeps and the other drops (elyon keeps all
        # three here; taxton drops all three) — the cluster spans from the nearest divergent
        # accent through the trailing space to the pasoleg itself, so the space is shared
        # (kept by both resolutions) and only the pasoleg mark itself is subtracted. Atom 1
        # SUPPLIES a maqaf (taxton joins לא to the next word, like ex 20:3's atom 1); atom 16
        # SUPPLIES the verse-end sof-pasuq (taxton ends the verse here; elyon reads on, like
        # ex 20:8's atom 5). Atom 12 (מתחת, occurrence 1) IS a third QUPO vowel-split case —
        # same patax/qamats-on-one-letter shape as ex 20:3's פני; atom 15 (מתחת, occurrence 2)
        # is a plain two-accent divergence (UXLC-utils#28's open מתחת question, resolved — see the
        # module comment above).
        (20, 4): {
            1: {
                "cluster": hpo.MTGOSLQ + acc.MUN,
                "alef": hpo.MTGOSLQ,
                "bet": acc.MUN,
                "add": {_STRAND_ALEF: [hpu.MAQ]},
            },
            2: {
                "cluster": hpo.MTGOSLQ
                + _CGJ
                + hpo.PATAX
                + hl.AYIN
                + hpo.XPATAX
                + hl.SHIN
                + hpo.SIND
                + hpo.SEGOL_V
                + acc.QOM
                + hl.HE
                + hpu.MAQ,
                "alef": hpo.PATAX
                + hl.AYIN
                + hpo.XPATAX
                + hl.SHIN
                + hpo.SIND
                + hpo.SEGOL_V
                + acc.QOM
                + hl.HE,
                "bet": hpo.MTGOSLQ
                + hpo.PATAX
                + hl.AYIN
                + hpo.XPATAX
                + hl.SHIN
                + hpo.SIND
                + hpo.SEGOL_V
                + hl.HE
                + hpu.MAQ,
            },
            3: {"cluster": acc.MER + acc.MUN, "alef": acc.MER, "bet": acc.MUN},
            4: {
                "cluster": acc.MUN
                + acc.PASH
                + hl.SAMEKH
                + hpo.SEGOL_V
                + hl.LAMED
                + acc.PASH
                + chr(0x0020)
                + hpu.PASOLEG,
                "alef": acc.PASH
                + hl.SAMEKH
                + hpo.SEGOL_V
                + hl.LAMED
                + acc.PASH
                + chr(0x0020),
                "bet": acc.MUN
                + hl.SAMEKH
                + hpo.SEGOL_V
                + hl.LAMED
                + chr(0x0020)
                + hpu.PASOLEG,
            },
            6: {"cluster": acc.PAZ + acc.ZAQ_Q, "alef": acc.ZAQ_Q, "bet": acc.PAZ},
            7: {"cluster": acc.MAH + acc.MUN, "alef": acc.MAH, "bet": acc.MUN},
            8: {
                "cluster": acc.MUN
                + acc.PASH
                + hl.YOD
                + hpo.XIRIQ
                + hl.FMEM
                + acc.PASH
                + chr(0x0020)
                + hpu.PASOLEG,
                "alef": acc.PASH
                + hl.YOD
                + hpo.XIRIQ
                + hl.FMEM
                + acc.PASH
                + chr(0x0020),
                "bet": acc.MUN
                + hl.YOD
                + hpo.XIRIQ
                + hl.FMEM
                + chr(0x0020)
                + hpu.PASOLEG,
            },
            9: {"cluster": acc.PAZ + acc.ZAQ_Q, "alef": acc.ZAQ_Q, "bet": acc.PAZ},
            10: {
                "cluster": acc.MER + hl.RESH + acc.TEL_Q,
                "alef": acc.MER + hl.RESH,
                "bet": hl.RESH + acc.TEL_Q,
            },
            11: {"cluster": acc.TIP + acc.QOM, "alef": acc.TIP, "bet": acc.QOM},
            12: {
                "cluster": hpo.QAMATS + acc.ATN + _CGJ + hpo.PATAX + acc.GER,
                "alef": hpo.QAMATS + acc.ATN,
                "bet": hpo.PATAX + acc.GER,
            },
            14: {
                "cluster": acc.TIP
                + acc.MUN
                + hl.YOD
                + hpo.XIRIQ
                + hl.FMEM
                + chr(0x0020)
                + hpu.PASOLEG,
                "alef": acc.TIP + hl.YOD + hpo.XIRIQ + hl.FMEM + chr(0x0020),
                "bet": acc.MUN
                + hl.YOD
                + hpo.XIRIQ
                + hl.FMEM
                + chr(0x0020)
                + hpu.PASOLEG,
            },
            15: {"cluster": acc.MER + acc.MUN, "alef": acc.MER, "bet": acc.MUN},
            16: {
                "cluster": hpo.MTGOSLQ + acc.REV,
                "alef": hpo.MTGOSLQ,
                "bet": acc.REV,
                "add": {_STRAND_ALEF: [hpu.SOPA]},
            },
        },
        (20, 5): {
            2: {"cluster": acc.MER + acc.MUN, "alef": acc.MER, "bet": acc.MUN},
            3: {
                "cluster": acc.TIP + hl.FMEM + acc.Z_OR_TSOR,
                "alef": acc.TIP + hl.FMEM,
                "bet": hl.FMEM + acc.Z_OR_TSOR,
            },
            5: {
                "cluster": acc.ATN + hl.FMEM + acc.SEG_A,
                "alef": acc.ATN + hl.FMEM,
                "bet": hl.FMEM + acc.SEG_A,
            },
            21: {
                "cluster": hpo.MTGOSLQ + acc.ATN + hl.YOD + hpu.SOPA,
                "alef": hpo.MTGOSLQ + hl.YOD + hpu.SOPA,
                "bet": acc.ATN + hl.YOD,
            },
        },
        (20, 6): {
            1: {"cluster": acc.MER + acc.MAH, "alef": acc.MER, "bet": acc.MAH},
            2: {
                "cluster": acc.TIP
                + acc.PASH
                + hl.SAMEKH
                + hpo.SEGOL_V
                + hl.DALET
                + acc.PASH,
                "alef": acc.TIP + hl.SAMEKH + hpo.SEGOL_V + hl.DALET,
                "bet": acc.PASH + hl.SAMEKH + hpo.SEGOL_V + hl.DALET + acc.PASH,
            },
            3: {"cluster": acc.ATN + acc.ZAQ_Q, "alef": acc.ATN, "bet": acc.ZAQ_Q},
        },
        # ex 20:8 — the first SUPPLIED sof-pasuq in the Decalogues (the additive charity,
        # like Gen 35:22). Atom 5 לְקַדְּשֽׁ֗וֹ ends the Sabbath-commandment's *first* prose
        # verse: taxton (alef) chants a verse-end there — silluq, already in UXLC — while
        # elyon (bet) keeps revia and reads on (its Sabbath verse runs vv.8–11). UXLC has
        # no sof-pasuq here (cf. ex 20:5 atom 21, the same shape, where it DID); MAM's
        # cant-alef confirms one belongs, so taxton SUPPLIES it (bracketed/green). Atoms
        # 1/3/4 are pure-accent. ex 20:9 / dt 5:12 also want a supplied sof-pasuq but are
        # entangled with a rafe/dagesh (כָּל) and a maqaf count-mismatch respectively — TBD.
        (20, 8): {
            1: {
                "cluster": acc.TEV + hl.VAV + hpo.XOLAM + hl.RESH + acc.TEL_Q,
                "alef": acc.TEV + hl.VAV + hpo.XOLAM + hl.RESH,
                "bet": hl.VAV + hpo.XOLAM + hl.RESH + acc.TEL_Q,
            },
            3: {"cluster": acc.MER + acc.QOM, "alef": acc.MER, "bet": acc.QOM},
            4: {"cluster": acc.TIP + acc.GER, "alef": acc.TIP, "bet": acc.GER},
            5: {
                "cluster": hpo.MTGOSLQ + acc.REV,
                "alef": hpo.MTGOSLQ,
                "bet": acc.REV,
                "add": {_STRAND_ALEF: [hpu.SOPA]},
            },
        },
        # ex 20:9 (ששת ימים תעבד): the first rafe/dagesh split. Atom 5 כָּל־ ("all") — taxton
        # keeps the dagesh (hard: ועשית took a disjunctive tipxa, so כל opens after a pause),
        # elyon drops it (soft: ועשית took a conjunctive munax). UXLC has no rafe here, so
        # the soft kaf stays bare (faithful — Policy 1). Atom 6 מלאכתך supplies a sof-pasuq
        # (taxton ends v.9; elyon keeps segolta and reads on).
        (20, 9): {
            1: {"cluster": acc.MAH + acc.MUN, "alef": acc.MAH, "bet": acc.MUN},
            2: {
                "cluster": acc.MUN + hl.YOD + hl.FMEM + acc.PASH,
                "alef": hl.YOD + hl.FMEM + acc.PASH,
                "bet": acc.MUN + hl.YOD + hl.FMEM,
            },
            3: {
                "cluster": acc.ZAQ_Q + hl.DALET + acc.Z_OR_TSOR,
                "alef": acc.ZAQ_Q + hl.DALET,
                "bet": hl.DALET + acc.Z_OR_TSOR,
            },
            4: {"cluster": acc.TIP + acc.MUN, "alef": acc.TIP, "bet": acc.MUN},
            5: {
                "cluster": hl.KAF + hpo.DAGOMOSD,
                "alef": hl.KAF + hpo.DAGOMOSD,
                "bet": hl.KAF,
            },
            6: {
                "cluster": hpo.MTGOSLQ + hl.FKAF + hpo.QAMATS + acc.SEG_A,
                "alef": hpo.MTGOSLQ + hl.FKAF + hpo.QAMATS,
                "bet": hl.FKAF + hpo.QAMATS + acc.SEG_A,
                "add": {_STRAND_ALEF: [hpu.SOPA]},
            },
        },
        # ex 20:10 (the Sabbath verse's back half, ...לא תעשה כל מלאכה): the second
        # pasoleg-tokenization verse (UXLC-utils#29). Atom 3 שבת ends in a pasoleg that elyon (bet) keeps
        # and taxton (alef) drops — the mirror of ex 20:4's atoms 4/8/14, where taxton kept
        # the pasoleg and elyon dropped it. Atom 10 אתה ׀ is the sharpest pasoleg case: this word
        # carries no accent of its own at all, so the divergence cluster is the
        # bare pasoleg character alone (not swept together with anything else) — taxton keeps
        # it (a standalone word in MAM's alef list), elyon drops it entirely (its bet
        # resolution is the empty string, like an omitted accent but for punctuation, since
        # a lone pasoleg is never SUPPLIED, only ever suppressed like any other divergent mark
        # already present in UXLC). Atom 18 SUPPLIES the verse-end sof-pasuq, same shape as
        # ex 20:4's atom 16 / ex 20:8's atom 5.
        (20, 10): {
            1: {
                "cluster": acc.QOM + hl.VAV + hpo.XOLAM + hl.FMEM + acc.PASH,
                "alef": hl.VAV + hpo.XOLAM + hl.FMEM + acc.PASH,
                "bet": acc.QOM + hl.VAV + hpo.XOLAM + hl.FMEM,
            },
            2: {"cluster": acc.ZAQ_Q + acc.GER, "alef": acc.ZAQ_Q, "bet": acc.GER},
            3: {
                "cluster": acc.TIP + acc.MUN + hl.TAV + chr(0x0020) + hpu.PASOLEG,
                "alef": acc.TIP + hl.TAV + chr(0x0020),
                "bet": acc.MUN + hl.TAV + chr(0x0020) + hpu.PASOLEG,
            },
            5: {"cluster": acc.ATN + acc.REV, "alef": acc.ATN, "bet": acc.REV},
            6: {
                "cluster": hpo.MTGOSLQ + acc.MUN + hl.ALEF + hpu.MAQ,
                "alef": hpo.MTGOSLQ + hl.ALEF + hpu.MAQ,
                "bet": acc.MUN + hl.ALEF,
            },
            7: {"cluster": acc.MUN + acc.QOM, "alef": acc.QOM, "bet": acc.MUN},
            9: {"cluster": acc.PAZ + acc.GER, "alef": acc.GER, "bet": acc.PAZ},
            10: {"cluster": hpu.PASOLEG, "alef": hpu.PASOLEG, "bet": ""},
            11: {
                "cluster": hpo.MTGOSLQ + acc.MUN + hpu.MAQ,
                "alef": acc.MUN,
                "bet": hpo.MTGOSLQ + hpu.MAQ,
            },
            12: {
                "cluster": acc.TEL_G
                + hl.BET
                + hpo.XIRIQ
                + hl.TAV
                + hpo.DAGOMOSD
                + hpo.SEGOL_V
                + acc.REV,
                "alef": hl.BET
                + hpo.XIRIQ
                + hl.TAV
                + hpo.DAGOMOSD
                + hpo.SEGOL_V
                + acc.REV,
                "bet": acc.TEL_G
                + hl.BET
                + hpo.XIRIQ
                + hl.TAV
                + hpo.DAGOMOSD
                + hpo.SEGOL_V,
            },
            13: {"cluster": acc.MAH + acc.QOM, "alef": acc.MAH, "bet": acc.QOM},
            14: {"cluster": acc.GER + acc.PASH, "alef": acc.PASH, "bet": acc.GER},
            15: {"cluster": acc.ZAQ_Q + acc.REV, "alef": acc.ZAQ_Q, "bet": acc.REV},
            16: {"cluster": acc.TIP + acc.PASH, "alef": acc.TIP, "bet": acc.PASH},
            17: {"cluster": acc.MER + acc.MUN, "alef": acc.MER, "bet": acc.MUN},
            18: {
                "cluster": hpo.MTGOSLQ + acc.ZAQ_Q,
                "alef": hpo.MTGOSLQ,
                "bet": acc.ZAQ_Q,
                "add": {_STRAND_ALEF: [hpu.SOPA]},
            },
        },
        # ex 20:13–15 (לא תרצח / תנאף / תגנב): here taxton joins each short commandment to the
        # next (לא takes a conjunctive merkha/munax, so the verb opens SOFT) while elyon chants
        # each as its own verse (לא takes a disjunctive tipxa → verb HARD + silluq + sof-pasuq).
        # UXLC has dagesh+rafe together on the verb's first letter, so the split is pure subtraction:
        # taxton keeps the rafe (soft) + its mid-unit accent, elyon keeps the dagesh (hard) +
        # silluq + sof-pasuq. (Faithful — Policy 1: the soft letter shows UXLC's own rafe.)
        (20, 13): {
            1: {"cluster": acc.MER + acc.TIP, "alef": acc.MER, "bet": acc.TIP},
            2: {
                "cluster": hl.TAV
                + hpo.DAGOMOSD
                + hpo.RAFE
                + hpo.XIRIQ
                + hl.RESH
                + hpo.SHEVA
                + hl.TSADI
                + hpo.QAMATS
                + acc.TIP
                + _CGJ
                + hpo.MTGOSLQ
                + hl.XET
                + hpu.SOPA,
                "alef": hl.TAV
                + hpo.RAFE
                + hpo.XIRIQ
                + hl.RESH
                + hpo.SHEVA
                + hl.TSADI
                + hpo.QAMATS
                + acc.TIP
                + hl.XET,
                "bet": hl.TAV
                + hpo.DAGOMOSD
                + hpo.XIRIQ
                + hl.RESH
                + hpo.SHEVA
                + hl.TSADI
                + hpo.QAMATS
                + hpo.MTGOSLQ
                + hl.XET
                + hpu.SOPA,
            },
        },
        (20, 14): {
            1: {"cluster": acc.MUN + acc.TIP, "alef": acc.MUN, "bet": acc.TIP},
            2: {
                "cluster": hl.TAV
                + hpo.DAGOMOSD
                + hpo.RAFE
                + hpo.XIRIQ
                + hl.NUN
                + hpo.SHEVA
                + hl.ALEF
                + hpo.QAMATS
                + acc.ATN
                + _CGJ
                + hpo.MTGOSLQ
                + hl.FPE
                + hpu.SOPA,
                "alef": hl.TAV
                + hpo.RAFE
                + hpo.XIRIQ
                + hl.NUN
                + hpo.SHEVA
                + hl.ALEF
                + hpo.QAMATS
                + acc.ATN
                + hl.FPE,
                "bet": hl.TAV
                + hpo.DAGOMOSD
                + hpo.XIRIQ
                + hl.NUN
                + hpo.SHEVA
                + hl.ALEF
                + hpo.QAMATS
                + hpo.MTGOSLQ
                + hl.FPE
                + hpu.SOPA,
            },
        },
        (20, 15): {
            1: {"cluster": acc.MUN + acc.TIP, "alef": acc.MUN, "bet": acc.TIP},
            2: {
                "cluster": hl.TAV
                + hpo.DAGOMOSD
                + hpo.RAFE
                + hpo.XIRIQ
                + hl.GIMEL
                + hpo.SHEVA
                + hl.NUN
                + hpo.XOLAM
                + hpo.MTGOSLQ
                + acc.ZAQ_Q
                + hl.BET
                + hpu.SOPA,
                "alef": hl.TAV
                + hpo.RAFE
                + hpo.XIRIQ
                + hl.GIMEL
                + hpo.SHEVA
                + hl.NUN
                + hpo.XOLAM
                + acc.ZAQ_Q
                + hl.BET,
                "bet": hl.TAV
                + hpo.DAGOMOSD
                + hpo.XIRIQ
                + hl.GIMEL
                + hpo.SHEVA
                + hl.NUN
                + hpo.XOLAM
                + hpo.MTGOSLQ
                + hl.BET
                + hpu.SOPA,
            },
        },
    },
    "Deuter": {
        # dt 5:6 (אנכי...): the Deuteronomy twin of ex 20:2, but where UXLC there combined BOTH
        # strands' accents, here it has only the taxton's — so elyon's are OMITTED, not present.
        # Atom 1 אנכי: taxton keeps its pashta; elyon wants a tipxa UXLC left untangled (noted, not
        # supplied) → elyon shows אנכי accent-less. Atom 3 אלהיך likewise: taxton zaqef kept, elyon's
        # etnaxta omitted. Atoms 8/9 are the pure-subtraction shape of ex 20:2 (munax/merkha; then
        # etnaxta vs. silluq+sof-pasuq at the verse end).
        (5, 6): {
            1: {
                "cluster": acc.PASH,
                "alef": acc.PASH,
                "bet": "",
                "omit": {_STRAND_BET: [acc.TIP]},
            },
            3: {
                "cluster": acc.ZAQ_Q,
                "alef": acc.ZAQ_Q,
                "bet": "",
                "omit": {_STRAND_BET: [acc.ATN]},
            },
            8: {"cluster": acc.MUN + acc.MER, "alef": acc.MUN, "bet": acc.MER},
            9: {
                "cluster": acc.ATN + _CGJ + hpo.MTGOSLQ + hl.YOD + hl.FMEM + hpu.SOPA,
                "alef": acc.ATN + hl.YOD + hl.FMEM,
                "bet": hpo.MTGOSLQ + hl.YOD + hl.FMEM + hpu.SOPA,
            },
        },
        # dt 5:7 — the Deuteronomy twin of ex 20:3, same QUPO vowel split at atom 7 פָּנָ֗י (see
        # its comment there). Atom 1 לא here carries NO meteg at all (UXLC has only munax) — and
        # taxton wants neither: it drops the munax entirely and instead SUPPLIES a maqaf, joining
        # לא to the next word. Atom 2 יהיה is the mirror of ex 20:3's: here taxton keeps its own
        # merkha (present in UXLC) while elyon's meteg is OMITTED — an ordinary meteg, NOT silluq,
        # since UXLC's maqaf-joined יהיה־ is mid-verse, not verse-final (silluq is defined by
        # verse-final position, not by the U+05BD codepoint alone — see _accent_name). Atoms 3–5
        # are pure-accent, same shape as ex 20:3.
        (5, 7): {
            1: {
                "cluster": acc.MUN,
                "alef": "",
                "bet": acc.MUN,
                "add": {_STRAND_ALEF: [hpu.MAQ]},
            },
            2: {
                "cluster": acc.MER + hl.HE + hpu.MAQ,
                "alef": acc.MER + hl.HE,
                "bet": hl.HE + hpu.MAQ,
                "omit": {_STRAND_BET: [hpo.MTGOSLQ]},
            },
            3: {"cluster": acc.TEV + acc.TEL_Q, "alef": acc.TEV, "bet": acc.TEL_Q},
            4: {"cluster": acc.MER + acc.QOM, "alef": acc.MER, "bet": acc.QOM},
            5: {"cluster": acc.TIP + acc.GER, "alef": acc.TIP, "bet": acc.GER},
            7: {
                "cluster": hpo.QAMATS + hpo.MTGOSLQ + _CGJ + hpo.PATAX + acc.REV,
                "alef": hpo.QAMATS + hpo.MTGOSLQ,
                "bet": hpo.PATAX + acc.REV,
                "add": {_STRAND_ALEF: [hpu.SOPA]},
            },
        },
        # dt 5:8 — the Deuteronomy twin of ex 20:4 (UXLC-utils#29's other pasoleg-tokenization verse),
        # same three pasoleg atoms (4/8/14, פסל/בשמים/במים — elyon keeps, taxton drops) and the
        # same מתחת pair at atoms 12/15 — but here NEITHER מתחת occurrence is QUPO: atom 12's
        # cluster has no patax/CGJ (only qamats + two accents), an ordinary cross-book
        # difference from ex 20:4's atom 12 (see the module comment above). Because that patax
        # is genuinely absent from the LC, atom 12 does not resolve silently either: it carries
        # an omitted-*vowel* note (the "omit_vowel" field below, the asymmetric sibling of a
        # QUPO split) — the elyon strand wants the patax ex 20:4 has, but the LC has only
        # the taxton's qamats there, leaving the elyon tav bare. Like an omitted accent, that
        # patax is NOTED, never supplied (_omitted_vowel_note). Atom 2's mid-word
        # pashta (grammatically impossible there — pashta must fall on a word's final letter)
        # is corrected to a qadma upstream in clc_collect (_UXLC_PENDING_CHANGES_APPLIED,
        # applying UXLC's own pending change #10, design doc §7.4) — before this oracle ever
        # runs. That qadma belongs to taxton alone: MAM's own cant-alef/cant-bet for this word
        # (MAM-simple xml-vtrad-mam/Deut.xml, verse osisID "Deut.5.7") give alef a qadma and
        # bet a plain meteg, never both on the same strand. So the cluster below tracks the
        # qadma/meteg slot itself (not just the meteg-or-silluq + maqaf tail after it) — an
        # ordinary position-safe subtraction, same as every other atom here, not an omission.
        (5, 8): {
            1: {
                "cluster": hpo.MTGOSLQ + acc.MUN + hl.ALEF + hpu.MAQ,
                "alef": hpo.MTGOSLQ + hl.ALEF + hpu.MAQ,
                "bet": acc.MUN + hl.ALEF,
            },
            2: {
                "cluster": acc.QOM + hpo.MTGOSLQ + hl.HE + hpu.MAQ,
                "alef": acc.QOM + hl.HE,
                "bet": hpo.MTGOSLQ + hl.HE + hpu.MAQ,
            },
            3: {"cluster": acc.MER + acc.MUN, "alef": acc.MER, "bet": acc.MUN},
            4: {
                "cluster": acc.MUN
                + acc.PASH
                + hl.SAMEKH
                + hpo.SEGOL_V
                + hl.LAMED
                + acc.PASH
                + chr(0x0020)
                + hpu.PASOLEG,
                "alef": acc.PASH
                + hl.SAMEKH
                + hpo.SEGOL_V
                + hl.LAMED
                + acc.PASH
                + chr(0x0020),
                "bet": acc.MUN
                + hl.SAMEKH
                + hpo.SEGOL_V
                + hl.LAMED
                + chr(0x0020)
                + hpu.PASOLEG,
            },
            6: {"cluster": acc.ZAQ_Q + acc.PAZ, "alef": acc.ZAQ_Q, "bet": acc.PAZ},
            7: {"cluster": acc.MAH + acc.MUN, "alef": acc.MAH, "bet": acc.MUN},
            8: {
                "cluster": acc.MUN
                + acc.PASH
                + hl.YOD
                + hpo.XIRIQ
                + hl.FMEM
                + acc.PASH
                + chr(0x0020)
                + hpu.PASOLEG,
                "alef": acc.PASH
                + hl.YOD
                + hpo.XIRIQ
                + hl.FMEM
                + acc.PASH
                + chr(0x0020),
                "bet": acc.MUN
                + hl.YOD
                + hpo.XIRIQ
                + hl.FMEM
                + chr(0x0020)
                + hpu.PASOLEG,
            },
            9: {"cluster": acc.ZAQ_Q + acc.PAZ, "alef": acc.ZAQ_Q, "bet": acc.PAZ},
            10: {
                "cluster": acc.MER + hl.RESH + acc.TEL_Q,
                "alef": acc.MER + hl.RESH,
                "bet": hl.RESH + acc.TEL_Q,
            },
            11: {"cluster": acc.TIP + acc.QOM, "alef": acc.TIP, "bet": acc.QOM},
            12: {
                "cluster": hpo.QAMATS + acc.ATN + acc.GER,
                "alef": hpo.QAMATS + acc.ATN,
                "bet": acc.GER,
                "omit_vowel": {_STRAND_BET: [hpo.PATAX]},
            },
            14: {
                "cluster": acc.TIP
                + acc.MUN
                + hl.YOD
                + hpo.XIRIQ
                + hl.FMEM
                + chr(0x0020)
                + hpu.PASOLEG,
                "alef": acc.TIP + hl.YOD + hpo.XIRIQ + hl.FMEM + chr(0x0020),
                "bet": acc.MUN
                + hl.YOD
                + hpo.XIRIQ
                + hl.FMEM
                + chr(0x0020)
                + hpu.PASOLEG,
            },
            15: {"cluster": acc.MER + acc.MUN, "alef": acc.MER, "bet": acc.MUN},
            16: {
                "cluster": hpo.MTGOSLQ
                + acc.REV
                + hl.RESH
                + hpo.SEGOL_V
                + hl.FTSADI
                + hpu.SOPA,
                "alef": hpo.MTGOSLQ + hl.RESH + hpo.SEGOL_V + hl.FTSADI + hpu.SOPA,
                "bet": acc.REV + hl.RESH + hpo.SEGOL_V + hl.FTSADI,
            },
        },
        (5, 9): {
            2: {"cluster": acc.MER + acc.MUN, "alef": acc.MER, "bet": acc.MUN},
            3: {
                "cluster": acc.TIP + hl.FMEM + acc.Z_OR_TSOR,
                "alef": acc.TIP + hl.FMEM,
                "bet": hl.FMEM + acc.Z_OR_TSOR,
            },
            5: {
                "cluster": acc.ATN + hl.FMEM + acc.SEG_A,
                "alef": acc.ATN + hl.FMEM,
                "bet": hl.FMEM + acc.SEG_A,
            },
            21: {
                "cluster": hpo.MTGOSLQ + acc.ATN + hl.YOD + hpu.SOPA,
                "alef": hpo.MTGOSLQ + hl.YOD + hpu.SOPA,
                "bet": acc.ATN + hl.YOD,
            },
        },
        (5, 10): {
            1: {"cluster": acc.MER + acc.MAH, "alef": acc.MER, "bet": acc.MAH},
            2: {
                "cluster": acc.TIP
                + acc.PASH
                + hl.SAMEKH
                + hpo.SEGOL_V
                + hl.DALET
                + acc.PASH,
                "alef": acc.TIP + hl.SAMEKH + hpo.SEGOL_V + hl.DALET,
                "bet": acc.PASH + hl.SAMEKH + hpo.SEGOL_V + hl.DALET + acc.PASH,
            },
            3: {"cluster": acc.ATN + acc.ZAQ_Q, "alef": acc.ATN, "bet": acc.ZAQ_Q},
        },
        # dt 5:12 (שמור...): the Deuteronomy twin of ex 20:8 — same shape (taxton's verse-end
        # SUPPLIES a sof-pasuq UXLC omits, atom 9) plus a third pasoleg-tokenization atom (UXLC-utils#29):
        # atom 7 צוך ׀ ends in a pasoleg that elyon keeps and taxton drops, the same direction as
        # ex 20:4/dt 5:8's atoms.
        (5, 12): {
            1: {"cluster": acc.TEV + acc.MUN, "alef": acc.TEV, "bet": acc.MUN},
            3: {
                "cluster": acc.MER + hl.VAV + hpo.XOLAM + hl.FMEM + acc.TEL_Q,
                "alef": acc.MER + hl.VAV + hpo.XOLAM + hl.FMEM,
                "bet": hl.VAV + hpo.XOLAM + hl.FMEM + acc.TEL_Q,
            },
            4: {"cluster": acc.TIP + acc.QOM, "alef": acc.TIP, "bet": acc.QOM},
            5: {"cluster": acc.ATN + acc.GER, "alef": acc.ATN, "bet": acc.GER},
            7: {
                "cluster": acc.TIP + acc.MUN + chr(0x0020) + hpu.PASOLEG,
                "alef": acc.TIP + chr(0x0020),
                "bet": acc.MUN + chr(0x0020) + hpu.PASOLEG,
            },
            8: {"cluster": acc.MER + acc.MUN, "alef": acc.MER, "bet": acc.MUN},
            9: {
                "cluster": hpo.MTGOSLQ + acc.REV,
                "alef": hpo.MTGOSLQ,
                "bet": acc.REV,
                "add": {_STRAND_ALEF: [hpu.SOPA]},
            },
        },
        # dt 5:13 (ששת ימים...): the Deuteronomy twin of ex 20:9, but UXLC has only the elyon
        # munax on ימים (atom 2), so the taxton's PASHTA is OMITTED — noted, not supplied; taxton
        # shows ימים accent-less. Atom 5 כל is the mirror of ex 20:9's: here taxton is HARD (dagesh)
        # and UXLC DOES have a rafe, so elyon is soft (rafe kept) — faithful Policy 1. Atom 6 ends
        # the taxton verse (silluq + sof-pasuq, both in UXLC — no supply, unlike ex 20:9).
        (5, 13): {
            1: {"cluster": acc.MUN + acc.MAH, "alef": acc.MAH, "bet": acc.MUN},
            2: {
                "cluster": acc.MUN,
                "alef": "",
                "bet": acc.MUN,
                "omit": {_STRAND_ALEF: [acc.PASH]},
            },
            3: {
                "cluster": acc.ZAQ_Q + hl.DALET + acc.Z_OR_TSOR,
                "alef": acc.ZAQ_Q + hl.DALET,
                "bet": hl.DALET + acc.Z_OR_TSOR,
            },
            4: {"cluster": acc.TIP + acc.MUN, "alef": acc.TIP, "bet": acc.MUN},
            5: {
                "cluster": hl.KAF + hpo.DAGOMOSD + hpo.RAFE,
                "alef": hl.KAF + hpo.DAGOMOSD,
                "bet": hl.KAF + hpo.RAFE,
            },
            6: {
                "cluster": hpo.MTGOSLQ + hl.FKAF + hpo.QAMATS + acc.SEG_A + hpu.SOPA,
                "alef": hpo.MTGOSLQ + hl.FKAF + hpo.QAMATS + hpu.SOPA,
                "bet": hl.FKAF + hpo.QAMATS + acc.SEG_A,
            },
        },
        # dt 5:14 — the Deuteronomy twin of ex 20:10's front half (both share the same
        # ...יום השביעי שבת... opening), so atoms 1/2/3/5 repeat that pattern verbatim
        # (atom 3's pasoleg: elyon keeps, taxton drops). dt 5:14 runs on to v.14's own ending
        # (atom 26) instead of ex 20:10's continuation — pure accent divergence there, no
        # pasoleg/QUPO/rafe. (Its own count mismatch (UXLC-utils#29) was the same atom-3 pasoleg.)
        (5, 14): {
            1: {
                "cluster": acc.QOM + hl.VAV + hpo.XOLAM + hl.FMEM + acc.PASH,
                "alef": hl.VAV + hpo.XOLAM + hl.FMEM + acc.PASH,
                "bet": acc.QOM + hl.VAV + hpo.XOLAM + hl.FMEM,
            },
            2: {"cluster": acc.ZAQ_Q + acc.GER, "alef": acc.ZAQ_Q, "bet": acc.GER},
            3: {
                "cluster": acc.TIP + acc.MUN + hl.TAV + chr(0x0020) + hpu.PASOLEG,
                "alef": acc.TIP + hl.TAV + chr(0x0020),
                "bet": acc.MUN + hl.TAV + chr(0x0020) + hpu.PASOLEG,
            },
            5: {"cluster": acc.ATN + acc.REV, "alef": acc.ATN, "bet": acc.REV},
            26: {
                "cluster": hpo.MTGOSLQ
                + acc.ATN
                + hl.VAV
                + hpo.XOLAM
                + hl.FKAF
                + hpo.QAMATS
                + hpu.SOPA,
                "alef": hpo.MTGOSLQ
                + hl.VAV
                + hpo.XOLAM
                + hl.FKAF
                + hpo.QAMATS
                + hpu.SOPA,
                "bet": acc.ATN + hl.VAV + hpo.XOLAM + hl.FKAF + hpo.QAMATS,
            },
        },
        # dt 5:15 (וזכרת...): the "remember you were a slave" clause unique to Deuteronomy's
        # Decalogue (no Exodus twin) — its own pasoleg-tokenization mismatch (UXLC-utils#29) is atom 4
        # היית ׀ (elyon keeps the pasoleg, taxton drops — same direction as every other pasoleg
        # atom above). Otherwise pure-accent divergence throughout.
        (5, 15): {
            1: {"cluster": acc.REV + acc.GER_2, "alef": acc.REV, "bet": acc.GER_2},
            2: {
                "cluster": acc.MUN + hl.YOD + hpu.MAQ,
                "alef": acc.MUN + hl.YOD,
                "bet": hl.YOD + hpu.MAQ,
            },
            3: {"cluster": acc.MAH + acc.MER, "alef": acc.MAH, "bet": acc.MER},
            4: {
                "cluster": acc.MUN
                + acc.PASH
                + hl.YOD
                + hl.TAV
                + hpo.QAMATS
                + acc.PASH
                + chr(0x0020)
                + hpu.PASOLEG,
                "alef": acc.PASH
                + hl.YOD
                + hl.TAV
                + hpo.QAMATS
                + acc.PASH
                + chr(0x0020),
                "bet": acc.MUN
                + hl.YOD
                + hl.TAV
                + hpo.QAMATS
                + chr(0x0020)
                + hpu.PASOLEG,
            },
            6: {"cluster": acc.ZAQ_Q + acc.REV, "alef": acc.ZAQ_Q, "bet": acc.REV},
            7: {
                "cluster": acc.QOM
                + hl.ALEF
                + hpo.XPATAX
                + hl.FKAF
                + hpo.QAMATS
                + acc.GER
                + acc.TEL_Q,
                "alef": acc.QOM + hl.ALEF + hpo.XPATAX + hl.FKAF + hpo.QAMATS + acc.GER,
                "bet": hl.ALEF + hpo.XPATAX + hl.FKAF + hpo.QAMATS + acc.TEL_Q,
            },
            8: {"cluster": acc.MAH + acc.QOM, "alef": acc.MAH, "bet": acc.QOM},
            9: {
                "cluster": acc.MAH
                + acc.PASH
                + hl.YOD
                + hl.FKAF
                + hpo.QAMATS
                + acc.PASH,
                "alef": acc.PASH + hl.YOD + hl.FKAF + hpo.QAMATS + acc.PASH,
                "bet": acc.MAH + hl.YOD + hl.FKAF + hpo.QAMATS,
            },
            10: {
                "cluster": acc.ZAQ_Q + hl.FMEM + acc.PASH,
                "alef": acc.ZAQ_Q + hl.FMEM,
                "bet": hl.FMEM + acc.PASH,
            },
            11: {"cluster": acc.MER + acc.MAH, "alef": acc.MER, "bet": acc.MAH},
            12: {
                "cluster": acc.TIP + hl.HE + acc.PASH,
                "alef": acc.TIP + hl.HE,
                "bet": hl.HE + acc.PASH,
            },
            14: {"cluster": acc.ATN + acc.ZAQ_Q, "alef": acc.ATN, "bet": acc.ZAQ_Q},
        },
        # dt 5:16 (כבד את אביך...): the seventh pasoleg-tokenization verse (UXLC-utils#29) — and the one
        # that turns out to carry NO divergence at all. Its atom 10 (למען ׀) has a lone pasoleg,
        # but MAM's taxton AND elyon both keep it (fold to the same word), so once the fold
        # fixes the count mismatch, every one of its 22 words is byte-identical between the
        # two strands. Deliberately NOT an _ORACLE entry: is_dual_cant("Deuter", 5, 16) is
        # False, and the verse renders as an ordinary single-cantillation row — the two
        # traditions simply don't diverge here (see the module comment above).
        # dt 5:17 (לא תרצח): the Deuteronomy twin of ex 20:13, but UXLC has the elyon verse-end's
        # sof-pasuq WITHOUT its silluq — so elyon's SILLUQ is OMITTED (noted, not supplied): elyon's
        # תרצח keeps the dagesh (hard) + the lone sof-pasuq, with no accent shown. taxton keeps the
        # rafe (soft) + its mid-unit tipxa and reads on (sof-pasuq suppressed).
        (5, 17): {
            1: {"cluster": acc.MER + acc.TIP, "alef": acc.MER, "bet": acc.TIP},
            2: {
                "cluster": hl.TAV
                + hpo.DAGOMOSD
                + hpo.RAFE
                + hpo.XIRIQ
                + hl.RESH
                + hpo.SHEVA
                + hl.TSADI
                + hpo.QAMATS
                + acc.TIP
                + hl.XET
                + hpu.SOPA,
                "alef": hl.TAV
                + hpo.RAFE
                + hpo.XIRIQ
                + hl.RESH
                + hpo.SHEVA
                + hl.TSADI
                + hpo.QAMATS
                + acc.TIP
                + hl.XET,
                "bet": hl.TAV
                + hpo.DAGOMOSD
                + hpo.XIRIQ
                + hl.RESH
                + hpo.SHEVA
                + hl.TSADI
                + hpo.QAMATS
                + hl.XET
                + hpu.SOPA,
                "omit": {_STRAND_BET: [hpo.MTGOSLQ]},
            },
        },
        # dt 5:18–19 (לא תנאף / תגנב): the Deuteronomy twins of ex 20:14–15 — same rafe/dagesh
        # split (taxton soft via the rafe, elyon hard via the dagesh + silluq + sof-pasuq), all
        # combined in UXLC so it is pure subtraction. (Unlike dt 5:17, UXLC here DOES have the
        # elyon silluq, so nothing is omitted.)
        (5, 18): {
            1: {"cluster": acc.MUN + acc.TIP, "alef": acc.MUN, "bet": acc.TIP},
            2: {
                "cluster": hl.TAV
                + hpo.DAGOMOSD
                + hpo.RAFE
                + hpo.XIRIQ
                + hl.NUN
                + hpo.SHEVA
                + hl.ALEF
                + hpo.QAMATS
                + hpo.MTGOSLQ
                + acc.ATN
                + hl.FPE
                + hpu.SOPA,
                "alef": hl.TAV
                + hpo.RAFE
                + hpo.XIRIQ
                + hl.NUN
                + hpo.SHEVA
                + hl.ALEF
                + hpo.QAMATS
                + acc.ATN
                + hl.FPE,
                "bet": hl.TAV
                + hpo.DAGOMOSD
                + hpo.XIRIQ
                + hl.NUN
                + hpo.SHEVA
                + hl.ALEF
                + hpo.QAMATS
                + hpo.MTGOSLQ
                + hl.FPE
                + hpu.SOPA,
            },
        },
        (5, 19): {
            1: {"cluster": acc.MUN + acc.TIP, "alef": acc.MUN, "bet": acc.TIP},
            2: {
                "cluster": hl.TAV
                + hpo.DAGOMOSD
                + hpo.RAFE
                + hpo.XIRIQ
                + hl.GIMEL
                + hpo.SHEVA
                + hl.NUN
                + hpo.XOLAM
                + hpo.MTGOSLQ
                + acc.ZAQ_Q
                + hl.BET
                + hpu.SOPA,
                "alef": hl.TAV
                + hpo.RAFE
                + hpo.XIRIQ
                + hl.GIMEL
                + hpo.SHEVA
                + hl.NUN
                + hpo.XOLAM
                + acc.ZAQ_Q
                + hl.BET,
                "bet": hl.TAV
                + hpo.DAGOMOSD
                + hpo.XIRIQ
                + hl.GIMEL
                + hpo.SHEVA
                + hl.NUN
                + hpo.XOLAM
                + hpo.MTGOSLQ
                + hl.BET
                + hpu.SOPA,
            },
        },
    },
}


# The niqqud vowel points: describe_diff.POINT_NAMES minus its non-vowel points (dagesh,
# meteg, rafe, shin-dot, sin-dot, varika). Used to spot the vowel one strand keeps and the
# other lacks at an omitted-vowel atom, without mistaking a shared dagesh/meteg for it.
_VOWEL_POINTS = frozenset(describe_diff.POINT_NAMES) - {
    hpo.DAGOMOSD,
    hpo.MTGOSLQ,
    hpo.RAFE,
    hpo.SHIND,
    hpo.SIND,
    hpo.VARIKA,
}


def _is_subsequence(sub, whole):
    it = iter(whole)
    return all(ch in it for ch in sub)


def _validate_oracle():
    """Fail loudly at import on an oracle typo (cheap; catches bad bytes early)."""
    for book in _ORACLE.values():
        for entry in (e for verse in book.values() for e in verse.values()):
            cluster = entry["cluster"]
            for strand in (_STRAND_ALEF, _STRAND_BET):
                assert _is_subsequence(entry[strand], cluster), (entry, strand)
            for added in entry.get("add", {}).values():
                for ch in added:
                    assert ch in _SUPPLIABLE, ch  # only punctuation is ever supplied
            for omitted in entry.get("omit", {}).values():
                for ch in omitted:
                    # only ACCENTS are noted-as-omitted; punctuation would be supplied instead.
                    # Require a canonical display name so the note reads cleanly — either a
                    # curated mb_diff_mpu name or CLC's silluq/meteg override for U+05BD (the name
                    # picked at render time by verse-finality, not fixed here — see _accent_name)
                    # — never a raw "HEBREW …" Unicode fallback.
                    assert _is_accent(ch), ch
                    assert ch == hpo.MTGOSLQ or ch in describe_diff.ACCENT_NAMES, ch
                    assert ch not in _SUPPLIABLE, ch
            for omitted_v in entry.get("omit_vowel", {}).values():
                for ch in omitted_v:
                    # Only VOWELS are noted-as-omitted here (accents go in "omit" above):
                    # a genuine niqqud vowel with a canonical describe_diff name, never a
                    # suppliable punctuation mark (punctuation would be supplied, not noted).
                    assert ch in _VOWEL_POINTS, ch
                    assert ch not in _SUPPLIABLE, ch


_validate_oracle()
