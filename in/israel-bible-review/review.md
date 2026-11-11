# The Israel Bible: this ain't no Koren edition

The Israel Bible (2018) comes from Menorah Books, which its copyright page calls an imprint of Koren
Publishers Jerusalem. Its acknowledgments praise Koren as Israel's foremost Bible publisher and
thank Koren's staff by name. One might assume from all this that the Hebrew text of the Israel Bible
is the same as that in other Koren editions of the Tanakh, but it is not. Not even close.

The Hebrew text of the Israel Bible is the Westminster Leningrad Codex (WLC), version 4.18, as
tanach.us distributed it in November 2014 and as Sefaria imported it in early 2015, when Sefaria's
import script stripped off its accents along with other content such as its
bracket-notes.[^provenance] The Israel Bible's [website](https://theisraelbible.com/) shows, by
default, the same Hebrew text as the printed book. The Israel Bible's copyright page credits the JPS
Tanakh for the English; it credits nothing for the Hebrew. The website's "About" page does name a
source, MAM, but MAM is only the text of a "Cantillation" layer that the website hides by default.[^site-translit]

So the Israel Bible, sold under the name of a prominent Israeli Bible publisher, reproduces, without
any editing,[^ib-editing] an outdated diplomatic edition of a single manuscript, the Leningrad Codex. A
diplomatic edition tries to show one manuscript as it stands, quirks and all. That is the right
thing for a student of that manuscript and the wrong thing for almost everyone else. A
general-purpose Bible should give its readers the Masoretic consensus, with the reading aids that
Jewish editions have long provided. Notably for an explicitly Zionist edition, the Israel Bible
ignores the work of the great Israeli Bible scholars like Breuer, Dotan, and Yeivin.

I refer to WLC as "outdated" above, but WLC's quality as a diplomatic edition is beside the point
here.[^wlc-quality] The point is the Israel Bible's many departures from the Masoretic consensus,
whether they come from a good transcription of the word in question or a bad one. A departure that
comes from a bad transcription is slightly more frustrating, but that doesn't matter much.

The Israel Bible leaves out the accents, a reasonable choice for readers who do not chant, though
this forfeits the help with stress that most accents provide. Some prayer books provide stress
help by marking nonfinal stress with meteg/silluq. The Israel Bible provides no such help,
despite the interest in pronunciation that it demonstrates through its many transliterations,
which put the stressed syllable in capitals.

And beyond stress, the Israel Bible gives no help with the following distinctions:

- the distinction between silent shewa and vocal shewa
- the distinction between qamats (gadol) and qamats qatan

Such distinctions are made in Koren editions, so here the misleading association with Koren hits
particularly hard.

## A sampling of quirks

In each of the 48 rows below, the Israel Bible's form is shown above a consensus form of the same
word.
(I take the consensus form to be MAM's form.) MAM's form is shown without accents or meteg, to
provide an "apples-to-apples" comparison with the Israel Bible's form.

<!-- weird-pointing -->

| Verse | Page | Israel Bible | MAM | Note |
|---|---|---|---|---|
| Deut 3:22 | 457 | תְִּירָאוּם | תִּירָאוּם | IB partners the consensus ḥiriq with a sheva that is nonsensical, non-robustly encoded, and typographically mishandled.<details><summary>Details</summary>The Israel Bible fails to use a CGJ (as at Exod 20:4, below), and thus leaves itself open to variable presentation depending on whether the environment does Unicode normalization or not. Normalization puts the sheva first, which in some fonts gives a false "ḥataf ḥiriq" look.[^hataf-hiriq]<br><br>As it turns out, the order of the two marks is immaterial due to IB's font's mishandling of this (admittedly outlandish) combination of marks. In IB's PDF (I have not inspected the paper edition), the font draws the ḥiriq and the sheva superimposed: the ḥiriq's dot lands almost on the sheva's upper dot, so the page shows something like a sheva with a misshapen top dot.<br><br>![The word as page 457 of the Israel Bible's PDF draws it](img/deut-3-22-word.png)</details> |
| Isa 49:23 | 1054 | קוָֹי׃ | קֹוָי׃ | IB has a nonsensical ḥolam male dot on vav rather than a ḥolam ḥaser dot on qof. |
| Lam 3:25 | 1813 | לְקוָֹו | לְקֹוָו | |
| Lam 4:4 | 1816 | אֶל־חכּוֹ | אֶל־חִכּוֹ | IB has no vowel under the ḥet. |
| Eccl 2:23 | 1827 | לִבּו | לִבּוֹ | IB has a bare vav instead of a ḥolam male. |

## The Decalogues

The Decalogues are among the most challenging passages of the Bible to present. So, it is no
surprise that the Israel Bible did not rise to the challenge. Each Decalogue has two cantillations,
the טעם תחתון and the טעם עליון, which differ in a few of their non-accent marks as well as in their
accents. (It is a little-known fact that the accent system interacts with the non-accent marks, i.e.
the accent system is not, as an edition like IB pretends, fully separable from the system of vowel
marks and dagesh.) In each of the 8 rows below, the Israel Bible's form is shown above MAM's עליון
form. (We choose the עליון because it is the closer of the two cantillations to IB's text.)

| Verse | Page | Israel Bible | MAM's עליון | Note |
|---|---|---|---|---|
| Exod 20:3 | 198 | עַל־פָּנָיַ | עַל־פָּנַי | IB has the תחתון's qamats under the nun, and the עליון's pataḥ under the yod rather than the nun. |
| Deut 5:7 | 463 | עַל־פָּנָיַ | עַל־פָּנַי | |
| Exod 20:4 | 198 | מִתַָּחַת | מִתַּחַת | IB has both the תחתון's qamats and the עליון's pataḥ under the tav. At Deut 5:8, below, it has the qamats alone.<details><summary>Details</summary>IB does not use a CGJ between the two vowels (as at Deut 3:22, above), so its encoding is not robust to normalization, though that doesn't matter since for display purposes, IB got kind of lucky and its PDF (I have not checked the printed page) draws them at the same point: in its Hebrew typeface a qamats is a pataḥ with a stem added, so the pataḥ lands exactly on the qamats's bar and vanishes. Anyone who copies or searches the PDF's text, or the website's, still gets the pataḥ.</details> |
| Exod 20:9 | 198 | כָּל־מְלַאכְתֶּךָ | כׇל־מְלַאכְתֶּךָ | IB has the תחתון's dagesh in the kaf. Correctly reflecting an error in the LC, WLC 4.18 has no rafeh here. Contrast with Deut 5:13, below. |
| Exod 20:10 | 198 | לֹא־תַעֲשֶׂה | לֹא תַעֲשֶׂה | IB has the תחתון's maqaf. |
| Deut 5:8 | 463 | לֹא־תַעֲשֶׂה־לְךָ | לֹא תַעֲשֶׂה־לְךָ | |
| Deut 5:8 | 463 | מִתָּחַת | מִתַּחַת | IB has the תחתון's qamats under the tav instead of the עליון's pataḥ. At Exod 20:4, above, it has both. See also my [note on the LC at Deut 5:8](https://bdenckla.github.io/MAM-basics/clc/Deuter-5-long-notes.html#long-Deuter-5-8-elyon-patah). |
| Deut 5:13 | 463 | כָּל־מְלַאכְתֶּךָ | כׇל־מְלַאכְתֶּךָ | IB has the תחתון's dagesh in the kaf. Correctly reflecting the LC, WLC 4.18 has an important rafeh here, but Sefaria stripped it.[^wlc422-rafeh] |

## In a long line

The Israel Bible is the latest in a long line of Hebrew Bibles slapped together from a Unicode
conversion of WLC. One expects that of free websites. One expects better of printed books, which
cost real money to make and to buy, but the line includes those too:

1. Zondervan's _A Reader's Hebrew Bible_ (2008) names its source, WLC version 4.4, and marks the
   places where WLC differs from BHS. Various follow-ons to this publication exist, including a
   second edition of this Reader (2026), as well as _A Reader's Hebrew and Greek Bible_, whose third
   edition came out in April 2026. But I assume that these follow-ons continue to use WLC, probably
   not even a more recent version of WLC.
2. Hendrickson's _A Hebrew Reader for the Pentateuch_ (2024) says in its preface that its Hebrew is
   WLC. This is the book I reviewed in
   ["WLC Considered Harmful"](https://bdenckla.github.io/MAM-basics/MAM-with-doc/misc/review_of_hebrew_reader_for_the_pentateuch.html).
   The same publisher's _A Hebrew Reader for the Psalms_ (2021), mostly a fresh transcription from
   the Aleppo Codex, shows what it could have done instead.
3. Crossway's _The Hebrew Old Testament, Reader's Edition_ (2021) cites its use of WLC: in its
   publisher's words, it "combines the text of the Westminster Leningrad Codex (WLC)" with glosses.
   With no qualifier such as "based on", that implies WLC's text verbatim.
4. Timothy A. Lee's Hebrew Bible Readers say on their copyright page that their base text is based
   on WLC, and I can attest that "based on" means quite closely based on, i.e. with little or no
   editing.
5. GlossaHouse's illustrated series does not say where its Hebrew comes from, but a review of its
   Genesis volume says that it is WLC with vowels and without accents, which is just what the Israel
   Bible gives its readers.

## Use of ḥataf vowels under non-gutturals

One expects to find an occasional "ḥataf-NG": a ḥataf vowel under a non-guttural, i.e. under a
letter other than the אהח״ע letters (alef, he, ḥet, and ayin). The Masoretes held a ḥataf
necessary to mark a vocal shewa under a guttural but optional under other letters, and the
manuscripts differ widely in how often they have one there (Yeivin,
[ITM §391](https://bdenckla.github.io/MAM-basics/yeivin-itm/yeivin_itm-376_393.html#ns391)). Cases of
ḥataf-NG appear more frequently in IB than in a consensus edition such as MAM. These "excess"
appearances, beyond the consensus, are not wrong, but they may surprise an intermediate student
of Biblical Hebrew.

The counts below include resh but leave out the divine-name-related cases that might be included
if their implied qere is ignored.[^divine-name] IB has 431 cases of ḥataf-NG, 225 of which are in
agreement with MAM.[^mam-hataf-ng] None of the cases in agreement with MAM is a ḥataf pataḥ:
under a non-guttural, MAM has only a ḥataf qamats or a ḥataf segol. That leaves 206 cases of
excess ḥataf-NG in IB, 97 of them under resh alone. (MAM has only one ḥataf under resh, in רֳאִי
at Gen 16:13, and IB has this one too.)

Unlike IB, MAM has a special notation for a ḥataf under a non-guttural in authoritative
manuscripts. That notation is the varika mark, which MAM has 674 times, as on the lamed of
MAM's וּלְﬞהַבְדִּיל at Gen 1:18, where IB has a ḥataf pataḥ. So, though MAM has only a simple
sheva rather than a ḥataf vowel on these letters, the varika mark records the ḥataf vowel that
might surprise the intermediate student. MAM marks 194 of IB's 206 cases of excess ḥataf-NG with
the varika, which makes something close to agreement between the editions for those cases.

## Conclusion

Through a series of examples, we have demonstrated the perils of just slapping together a Hebrew
Bible using WLC. The result is nothing like a Koren Bible, which is a consensus edition biased
towards the printed tradition and providing pronunciation aids that have become common. Nor is the
result like MAM, a consensus edition biased towards the manuscript tradition but not slavishly
diplomatic to any one exemplar of that tradition.[^mam-aleppo]

## Related work

I have written about WLC before, in my series
["Undoing and redoing the work of the Masoretes"](https://bdenckla.github.io/MAM-basics/MAM-with-doc/misc/urwotm_1_tale_of_the_qadma.html)
and in
["WLC Considered Harmful"](https://bdenckla.github.io/MAM-basics/MAM-with-doc/misc/review_of_hebrew_reader_for_the_pentateuch.html),
my review of _A Hebrew Reader for the Pentateuch_. That review lists the quirks the Reader inherited
from WLC, and every one of them that survives the stripping of the accents is in the Israel Bible
too.

Other works by me about the Masoretic Text can be found in this
[index of my documents](https://bdenckla.github.io/MAM-basics/).

[^provenance]: Sefaria's import script, `parseLeningradCodex.py`, read tanach.us's XML (build 24.2),
    leaving out WLC's bracket-notes, and, for its "Tanach with Nikkud", applied a regular expression
    that deletes all accents, meteg, rafeh, the paseq code point, the extraordinary upper and lower
    dots, and every parenthesized one-letter marker: the setumah and petuḥah markers and the
    inverted nuns.

[^site-translit]: We suspect that MAM, rather than IB, is the source of the website's
    transliterations! Our unpublished research of 2026-11-10 on the Israel Bible's
    transliterations found that the website began to transliterate every verse in August 2023,
    when it began to show MAM's text, and that where MAM's text and WLC's differ, its
    transliterations mostly follow MAM.

[^ib-editing]: The Israel Bible added a ḥolam to YHVH-Adonai, wrote the ḥolam ḥaser of a consonantal
    vav (as in מִצְוֺת) as a sin dot (!), and, in Jerusalem-related words, inconsistently separated
    the orphan ḥiriq from the lamed's own vowel with a hair space. Of the 633 words with the orphan
    ḥiriq, 144 have no hair space, almost all of them in Joshua through 2 Kings, and of the
    four ירושלמה words, whose lamed has an orphan sheva instead, only 1 Kgs 10:2 has a hair space.

[^wlc-quality]: WLC is not even a particularly good diplomatic edition. It began as a digital copy
    of the body text of _Biblia Hebraica Stuttgartensia_ (BHS), a diplomatic edition of the LC first
    published over the decade 1967–1977. WLC has not evolved much beyond BHS. BHS, though a great
    achievement when it was first published, is, by today's standards, no longer a particularly good
    diplomatic edition. (BHS was revised in 1984, 1990, and 1997. What changed in those revisions is
    unknown, and this lack of transparency is one of the many criticisms that can be levelled
    against BHS.)

    Worse, the Israel Bible presents this diplomatic text without ever expressing any surprise or
    doubt, and a diplomatic presentation that never does so is somewhere between nonsensical and
    irresponsible. Of the 48 words sampled in "A sampling of quirks", 45 are marked with surprise or
    doubt in at least one of three sources:

    - WLC 4.20's bracket-notes call 28 of them anomalous or of questionable validity
    - MAM notes surprise or doubt in 14 of the 21 that are in sections where MAM relies on the LC
    - Dotan's BHL marks its reading of 3 as doubtful, and effectively marks 43 of them with surprise
      by banishing them to Appendix A.

[^hataf-hiriq]: A ḥataf ḥiriq appears five times in the Aleppo Codex: see
    [near-Aleppo](https://bdenckla.github.io/MAM-basics/near-aleppo/editorial-policies.html#hataf).

[^vav-dot]: This is a known mark of the LC and of the Aleppo Codex, though they write it only
    sometimes: a dot in a consonantal vav before a shuruq. Yeivin, as MAM's introduction
    (chapter 2) quotes him, takes it to show that the vav is pronounced almost as a vowel. Dotan
    calls it "the mappiq point in the letter waw followed by the vowel u", counts twenty-one words
    with it in the LC, and leaves it out of BHL's text (Foreword, p. xiv); MAM leaves it out too,
    as Breuer did. The Israel Bible keeps it and explains nothing, so its readers can only take it
    for a dagesh or a shuruq.

[^wlc422-rafeh]: WLC itself has since dropped this rafeh too. WLC 4.22, released in August 2020,
    removed all twelve rafeh marks that WLC 4.20 had, the seven in the Decalogues among them. See
    my [notes on this change in WLC 4.22](https://bdenckla.github.io/MAM-basics/wlc/420422/full-record/420422-33.html).

[^divine-name]: The cases left out are the ḥataf segol under the yod of YHVH-Elohim, and, at
    Ps 144:15, IB's ḥataf pataḥ under the yod of YHVH-Adonai and MAM's ḥataf segol under the shin
    prefixed to it.

[^mam-hataf-ng]: MAM has 6 cases of ḥataf-NG where IB has none. At 3 of them IB has a simple
    sheva (Ezek 44:13, Ezra 4:9, and 2 Chr 5:7), and at the other 3 a full vowel: a qamats
    (Num 35:20 and 1 Sam 26:10) or a segol (2 Sam 6:5).

[^mam-aleppo]: MAM even occasionally diverges from the Aleppo Codex, the greatest exemplar of the
    manuscript tradition.
