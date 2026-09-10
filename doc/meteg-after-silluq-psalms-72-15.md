# Meteg after silluq at Psalms 72:15 in UXLC and WLC: what the repositories hold

Written 2026-09-10 by a Claude session in the MAM-basics worktree `C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/eloquent-ritchie-0e4c6c`, on the branch `claude/interesting-taussig-6aa52b`. Ben's instruction, 2026-09-10: "Psalms 72:15, UXLC 3.9 seems to point to a possible additional case of meteg after silluq in Leningrad ... For right now we'll just investigate that Psalms 72:15 word individually". The complete run over every verse-final chanted word that he asked for in the same message is recorded as `doc/PLAN-meteg-after-silluq-in-uxlc-and-wlc.md`. Everything below is this session's account of the data, and the terms are those of `doc/meteg-after-silluq-job-4-12.md`.

The verse-final chanted word of Psalms 72:15 is a lone atom, and the verse, as MAM-simple has it, is וִיחִ֗י וְיִתֶּן־לוֹ֮ מִזְּהַ֢ב שְׁ֫בָ֥א וְיִתְפַּלֵּ֣ל בַּעֲד֣וֹ תָמִ֑יד כׇּל־הַ֝יּ֗וֹם יְבָרְכֶֽנְהוּ׃

## 1. Summary: MAM, and the Aleppo Codex as MAM quotes it, have one U+05BD; UXLC and WLC record a second, after the silluq

1. **MAM has one U+05BD, on the kaf, and MAM's documentation twice quotes the Aleppo Codex with that one: established.** MAM's source (`in/mam-ws/D1-Psalms.json` line 2148) has יְבָרְﬞכֶֽנְהוּ in a `נוסח` template whose note gives the Aleppo Codex's form as יְבָרֲכֶֽנְהוּ, with a hataf under the resh where MAM has a sheva with a varika. MAM's introduction quotes the Aleppo Codex with the same form in its list of hatafs under non-guttural letters (`in/mam-ws-intro/ch5.mediawiki` line 737, under the heading at line 716). Both quotations are about the hataf, so neither was made to record the meteg, and both agree with MAM's text. MAM copies the meteg as the Aleppo Codex has it wherever that manuscript survives (`in/mam-ws-intro/ch3.mediawiki` line 1328), and this verse is on the Aleppo Codex's leaf 253v, which has Psalms 71:18–73:10 (MAM's index of the Aleppo Codex, `in/mam-ws-intro/index-aleppo.mediawiki` line 613).
2. **UXLC 3.9, WLC 4.22 and WLC 4.20 record two U+05BD, on the kaf and on the he: established for the transcriptions.** UXLC 3.9 records יְבָרֲכֶֽנְהֽוּ׃ with no note on the word (`in/UXLC-39/Psalms.xml` line 13314), and the two WLC conversions have the same codepoints (line 33165 of `out/wlc422-u/1verses_08_2cps.json`, line 33140 of `out/wlc420-u/1verses_08_2cps.json`). The Leningrad Codex itself was not consulted: the verse is on its folio 380A (`uxlc/data/lci_augrecs.json`, the record at line 15070), and no image of that folio is on disk.
3. **mgketer's transcription of Mikra'ot Gedolot ha-Keter records one U+05BD, on the kaf: established.** Its form is יְבָרֲכֶֽנְהוּ (`C:/Users/BenDe/GitRepos/MAM-private/mgketer/out/D1-Psalms/mgketer-json-massaged/D1-Psalms_72.json` line 646).
4. **In MAM the stress is penultimate, so the U+05BD on the he that UXLC and WLC record is after the silluq.** MAM's one U+05BD, on the kaf, is its silluq, and Phonetic MAM's `jta` is `y^.va.r^.!khen.hu`. The parallels in section 4 of `doc/meteg-after-silluq-job-4-12.md` have the same suffix, stressed on the syllable before it. The syllables are those of MAM's 1 Kings 7:37, לְכֻלָּֽהְנָֽה׃: a stressed closed syllable, then an open last syllable with a long vowel, which has the second U+05BD.
5. **Koren has not yet been looked up at this verse.** The lookup is Ben's, asked for on 2026-09-10.
6. **The earlier screen listed this verse, and the post-stress-meteg survey does not treat it.** `doc/meteg-after-silluq-screen-against-uxlc-and-wlc.md` puts Psalms 72:15 in its class (v) against both UXLC 3.9 and WLC 4.22 (its section 4), with 1 Samuel 17:5, 1 Kings 14:14 (against UXLC 3.9 only) and Psalms 70:2. The survey's post-silluq page, `gh-pages/post-stress-meteg-post-silluq.html`, treats 1 Samuel 17:5 alone.
7. **Yeivin and Breuer say nothing about this word.** Of the two books only CoS cites Psalms 72:15, once, as an unpointed verse-division example (chapter 10 §4, `C10-S001.md` line 365 under `C:/Users/BenDe/GitRepos/MAM-private/masorah-books/books/cos/md-export-of-docx/`). The ga'aya the U+05BD on the he would be, Breuer's type j after a mafsik, is named for 1 Kings 7:37 alone (CoS chapter 8 §46 note [^81]).

## 2. The forms

| Text | Form | Its U+05BD | Where |
| --- | --- | --- | --- |
| MAM | יְבָרְﬞכֶֽנְהוּ | on the kaf | `in/mam-ws/D1-Psalms.json` line 2148; MAM-simple's form lacks the varika on the resh |
| The Aleppo Codex, as MAM's note and introduction quote it | יְבָרֲכֶֽנְהוּ | on the kaf | `in/mam-ws/D1-Psalms.json` line 2148; `in/mam-ws-intro/ch5.mediawiki` line 737 |
| UXLC 3.9 | יְבָרֲכֶֽנְהֽוּ׃ | on the kaf and on the he | `in/UXLC-39/Psalms.xml` line 13314 |
| WLC 4.22 and WLC 4.20 | the same codepoints as UXLC 3.9's form | on the kaf and on the he | line 33165 of `out/wlc422-u/1verses_08_2cps.json`; line 33140 of `out/wlc420-u/1verses_08_2cps.json` |
| mgketer (Mikra'ot Gedolot ha-Keter) | יְבָרֲכֶֽנְהוּ | on the kaf | `D1-Psalms_72.json` line 646, as in section 1 |
| Koren | not yet looked up | | |

## 3. Not consulted, and what would bear on it

1. **Koren**, Ben's lookup: does Koren have a U+05BD on the he?
2. **The Leningrad Codex, folio 380A**, at `https://manuscripts.sefaria.org/leningrad-color/BIB_LENCDX_F380A.jpg`, the URL pattern of `doc/boj-leningrad-word-crops.md`: whether the manuscript has the stroke on the he that UXLC and WLC record. A download, which needs Ben's approval.
3. **The Aleppo Codex, leaf 253v**, whose image MAM's index links at `https://barhama.com/aleppocodex/?image=ALEPPO_CODEX_253v`: whether it has the one stroke that MAM's text and quotations imply. Also a download.
4. **The complete run** over every verse-final chanted word, in `doc/PLAN-meteg-after-silluq-in-uxlc-and-wlc.md`.

## 4. Scripts and commands that re-establish every figure

All are throwaway scripts, gitignored under `.novc/` in the worktree named at the top, run from its root on `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`.

1. `.novc/job412_spell2.py` spells out this atom codepoint by codepoint in every source above and in Phonetic MAM, and writes `.novc/job412_spell2_report.txt`.
2. `.novc/ps7215_write_doc.py` writes this file from `.novc/ps7215_doc_template.md`. It lifts every pointed form and the `jta` from the data; asserts that the note's and the introduction's quotations of the Aleppo Codex agree, that UXLC 3.9 and both WLC conversions have the same codepoints, and how many U+05BD each form has; and checks the result with `has_std_mark_order`.
