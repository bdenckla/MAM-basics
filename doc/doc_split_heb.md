# "Split Hebrew" representation
* sh: split Hebrew, i.e. split into 4 layers: L, V, A, & S.
     * L stands for letters (a somewhat vague concept).
         * In this case "letters" indicates a set we'll call the "pointed consonants".
         * I define the "pointed consonants" as the set of letters which:
             * has *dagesh* or *mapiq* versions of all chars that can have them
             * has both *shin* and *sin*, but lacks "unpointed" (ambiguous) *shin*
             * has both of the *vav*-based vowels (*holam male* & *shuruq*)
     * V for vowel points (a somewhat vague concept).
       * I define the vowel points as:
           * excluding the points in the *vav*-based vowels
               * Thus the only *holam* in layer V is *holam haser*.
           * including *sheva nach*, even though it indicates the absence of any vowel
     * A for accents including *meteg* & trope marks
     * S for "specials" (everything not captured in LVA)


* caps for *dagesh* except for `f` and `v`, which map to `P` & `B` respectively
    * I.e. since they are a better fit for usual pronunciation & romanization:
       * `P` & `f` represent *pei* & *fei* respectively (neither `p` or `F` are used)
       * `B` & `v` represent *bet* & *vet* respectively (neither `b` or `V` are used)
* final form indicated by a trailing period, e.g. `n.` for *nun sofit*
* `w` for *vav*:
    * using `w` distinguishes it from the `v` used for *vet*
    * using `w` harkens back to an older style of romanization
        * This older style reflects speculation about historical pronunciation.
* `o` & `u` for the *vav*-based vowels (*holam male* & *shuruq*)
* We use `x` for *chet* because in the IPA, \[x\] & \[χ\] represent velar and uvular voiceless fricatives, sounds that are in the *ballpark* of how *chet* is usually pronounced.
   * According to some, the ideal pronunciation of *chet* may be \[ħ\] (a voiceless *pharyngeal* fricative). I.e. the connection of `x` to \[x\] & \[χ\] is just as a mnemonic, not a technical claim of phonetic judgment.

* P f B v w o u
    * Pei, fei, Bet, vet, vav, holam male, shuruq
* K k q x h
    * kaf, khaf, qof, chet, hei
* te ta ts
    * tet, tav, tsadi
* sh si sa
    * shin, sin, samech
* al ay
    * alef, ayin

* :e :0
    * shva na (vocal), shva nach (silent) (stop)
* .. 3
    * tsere, segol
* Tg Tk
    * qamats gadol, qamats katon
* mer tip
    * merekha, tippecha

In the table below:
* The "d" in "df" stands for "*dagesh* or *mapiq*".
* The "f" stands for "final".

|--|d-|-f|df|notes|
|--|--|--|--|-----|
|`al`&#x5d0;|`AL`&#x5d0;&#x5bc;|||mid-dot is rare
|`v`&#x5d1;|`B`&#x5d1;&#x5bc;|||
|`g`&#x5d2;|`G`&#x5d2;&#x5bc;|||
|`d`&#x5d3;|`D`&#x5d3;&#x5bc;|||
|`h`&#x5d4;|`H`&#x5d4;&#x5bc;|||
|`w`&#x5d5;|`W`&#x5d5;&#x5bc;|||
|`o`&#x5d5;&#x5b9;||||holam male
|`u`&#x5d5;&#x5bc;||||shuruq
|`z`&#x5d6;|`Z`&#x5d6;&#x5bc;|||
|`x`&#x5d7;||||
|`te`&#x5d8;|`TE`&#x5d8;&#x5bc;|||
|`y`&#x5d9;|`Y`&#x5d9;&#x5bc;|||
|`k`&#x5db;|`K`&#x5db;&#x5bc;|`k.`&#x5da;|`K.`&#x5da;&#x5bc;|
|`l`&#x5dc;|`L`&#x5dc;&#x5bc;|||
|`m`&#x5de;|`M`&#x5de;&#x5bc;|`m.`&#x5dd;|`M.`&#x5dd;&#x5bc;|
|`n`&#x5e0;|`N`&#x5e0;&#x5bc;|`n.`&#x5df;|`N.`&#x5df;&#x5bc;|
|`sa`&#x5e1;|`SA`&#x5e1;&#x5bc;|||
|`ay`&#x5e2;||||
|`f`&#x5e4;|`P`&#x5e4;&#x5bc;|`f.`&#x5e3;|`P.`&#x5e3;&#x5bc;|
|`ts`&#x5e6;|`TS`&#x5e6;&#x5bc;|`ts.`&#x5e5;|`TS.`&#x5e5;&#x5bc;|
|`q`&#x5e7;|`Q`&#x5e7;&#x5bc;|||
|`r`&#x5e8;|`R`&#x5e8;&#x5bc;|||*dagesh* is rare
|`sh`&#x5e9;&#x5c1;|`SH`&#x5e9;&#x5c1;&#x5bc;|||
|`si`&#x5e9;&#x5c2;|`SI`&#x5e9;&#x5c2;&#x5bc;|||
|`ta`&#x5ea;|`TA`&#x5ea;&#x5bc;|||

* *resh* with *dagesh* is rare.
    * 13 times in the *tanakh*.
    * See Jacobson page 245.
* mid-dot on *aleph* is rare.
    * 4 times in the *tanakh*.
    * Its meaning is not clear.
        * Probably not a *dagesh*.
        * Maybe a *mapiq*.
        * Maybe something else entirely.
    * See Jacobson page 251.

* ??? which final forms can take a dagesh ???
    * Wikipedia says pe hazak sofit ףּ is found once in the Tanakh
    * maybe nun sofit & mem sofit never have dagesh (hazak) forms?

* There is no separate encoding of the following points, since their
  encoding is always combined with the consonant to which they belong:
    * shin dot and sin dot
    * the \[high\] point used with vav to form holam male
    * the \[mid\] point used with vav to form shuruq
    * all dagesh and mapiq points
* Another way of summarizing the "alphabet" of layer L:
    * Everything "in the middle" (consonants plus mid dots) plus:
        * shin dots & sin dots
        * the point used with vav to form holam male

* tcs: target character system, e.g.:
   * 0: Jacobson's technical romanization
       * here "technical" means *phonetically* technical/precise, not, for example, *orthographically* technical/precise!
   * 1: pointed Hebrew

* Ambiguous *shin* (*shin* without a *shin* dot or *sin* dot) is not representable.
   * I.e. this is a system for representing fully pointed Hebrew.

* *Vav haluma* is represented as a *vav* (`w`) in layer L and a *holam haser* (`o`) in layer V.
    * This is usually pronounced, roughly, "vo".
    * Recall that *holam male* is represented entirely in layer L.
    * In Unicode, *vav haluma* and *holam male* can be either:
        * not distinguished (represented identically)
        * "half-distinguished" (see below).
    * In contrast, in split Hebrew, the only option is to fully distinguish *vav haluma* and *holam male*.

* Full ambiguities in Unicode
   * In Unicode, *shuruq* (indicating a vowel sound) cannot be distinguished from *vav* with a *dagesh* (indicating a consonant sound). Perhaps you could make this distinction by using presentation form U+FB35 (HEBREW LETTER VAV WITH DAGESH) as *shuruq* but that seems like a bad idea. For one thing your distinction would not survive a normalization that gets rid of presentation forms.
* "Half distinctions" in Unicode
   * Unicode Hebrew has several cases in which:
      * a sequence of code points *s* can represent character *c* or *d*.
      * a sequence of code points *t* can only represent character *d*.
      * no sequence exists that can only represent character *c*.
   * Important cases of "half distinction" in Unicode include:
       * *s* = U-*qamats*-U (we enclose descriptions of code points in U--U)
          * *t* = U-*qamats katan*-U
          * *c* = *qamats gadol*
          * I.e. there is no way to represent only *qamats gadol*.
       * *s* = *vav* followed by *holam*
          * *t* = U-*vav*-U followed by U-*holam haser* for *vav*-U
          * *c* = *holam male*
          * *d* = *vav haluma*
          * I.e. there is no way to represent only *holam male*.
          * E.g. there is no code point "*holam* to make *holam male*".
   * So, even when we try to distinguish *c* from *d*, some ambiguity persists.
      * Some ambiguity persists because without some context, when we encounter *s* we don't know whether *c* or *d* was intended.
      * The needed context could simply be documentation, e.g.:
         * This text distinguishes *c* from *d*.
         * I.e. this text uses *s* to mean *c* and only *c*.
         * I.e. this text never uses *s* to mean *d*.
         * I.e. this text uses *t* and only *t* to mean *d*.
      * Or perhaps the context could be implicit:
          * if *t* (which can only mean *d*) is found to be present, then perhaps it can be assumed that *s* means only *c* in this context
    * It is too bad that one or more new code points were not added to make a sequence *u* that would represent *c* and only *c*.
        * Not every text needs to be unambiguous.
        * Indeed some texts *need* to be ambiguous (for example when representing an ambiguous source)
        * But it would be nice to have the *option* to be unambiguous.
