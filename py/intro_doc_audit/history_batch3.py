"""The third manually adjudicated history batch; no semantic inference from matches."""

from intro_doc_audit import audit, history_batch_compile
from intro_doc_audit.revision_history import diff_url


def main():
    records = []

    def add(
        cid, classification, result, limits, chapters, intro, links, pairs=(), **extra
    ):
        records.append(
            dict(
                case=cid,
                classification=classification,
                result=result,
                limits=limits,
                chapters=[dict(key=k, verses=v, selected=r) for k, v, r in chapters],
                intro=intro,
                links=[
                    dict(label=label, url=diff_url(old, new))
                    for label, old, new in links
                ],
                adjacent_pairs=list(pairs),
                **extra
            )
        )

    add(
        "TORAH-SPELLING-DEUT32-SHEVA",
        "established-staleness-after-doc-note-correction",
        "On 28 January 2024 the canonical note adds the missing yod sheva to its Leningrad quotation and description. The Introduction's quotation is unchanged in the immediately surrounding chapter-3 snapshots. The older form was already in the 2015 canonical note; this dates staleness relative to the note correction, without independently verifying the manuscript.",
        [
            "The correction's physical manuscript basis is not rechecked.",
            "The older draft's first quotation is not dated.",
        ],
        [("deuter-32", [6], [655705, 2821665, 2835957])],
        dict(revisions=[1290610, 2835211, 2835961], refs=[["Deuter", 32, 6]]),
        [("Note corrects yod sheva", 2821665, 2835957)],
        [(2821665, 2835957)],
    )
    add(
        "L-CANDIDATE-PS-18-7",
        "attribution-tension-present-when-Introduction-alternative-added",
        "The Introduction first presents definite Leningrad meteg with a ḥataf at 20:44 on 6 March 2023. At 21:02:18 the canonical note instead explicitly assigns Leningrad merkha with a ḥataf; seventeen seconds later the Introduction adds its current doubtful merkha-or-meteg alternatives. This tension coexists with that addition, rather than arising from a later note change.",
        [
            "The question mark may preserve a legitimate unresolved manuscript interpretation.",
            "The history does not settle the supporting manuscript reading or choose between alternatives.",
        ],
        [("psalms-18", [7], [1434520, 2707404])],
        dict(revisions=[2707401, 2707405], refs=[["Psalms", 18, 7]]),
        [
            ("Explicit Leningrad note", 1434520, 2707404),
            ("Introduction alternatives", 2707401, 2707405),
        ],
        [(1434520, 2707404), (2707401, 2707405)],
    )
    add(
        "HATAF-PROVERBS-ADDITION",
        "later-note-expansion-unreflected-in-existing-list",
        "On 9 August 2024 the note first explicitly documents Leningrad's ḥataf at Proverbs 30:17. The twelve-item Proverbs list remains literally unchanged in Introduction snapshots before and after the edit and omits that form. This establishes an unreflected note expansion, but does not date the reading's discovery or prove that the list was complete when assembled.",
        [
            "The public pre-MAM 2011 chapter already has a ḥataf form.",
            "The list's entire formation history is unexamined; the proposed addition remains unapproved.",
        ],
        [("chapter", [17], [2860044, 2871735])],
        dict(revisions=[2865999, 2879657], list_claim="ch5:L712", scope_caption=True),
        [("Leningrad note expansion", 2860044, 2871735)],
        [(2860044, 2871735)],
    )
    add(
        "NUM-10-8-B17-METEG",
        "internal-note-conflict-introduced-by-source-code-replacement",
        "The 2018 note assigns Firkovich B17 no meteg. In 2021 the opening agreement list instead names L1 with meteg, while the lower no-meteg list names L2. On 24 December 2023 only that lower L2 becomes L1, leaving L1 in both conflicting lists. This dates the internal conflict; the earlier assessments differ and history cannot decide which reading to retain.",
        [
            "L1 is Firkovich B17 in the current sigil inventory; historical L2's intended identity remains unadjudicated.",
            "Prior claims of image inspection are source statements, not this audit's scan verification.",
        ],
        [("numbers-10", [8], [803014, 812251, 1170471, 1290402, 2809587, 2826766])],
        dict(revisions=[], refs=[]),
        [
            ("2018 assessment", 803014, 812251),
            ("2021 source lists", 1170471, 1290402),
            ("Conflicting replacement", 2809587, 2826766),
        ],
        [(803014, 812251), (1170471, 1290402), (2809587, 2826766)],
    )
    add(
        "ALL-HATAF-SAM-8-10",
        "omission-present-when-Samuel-list-expanded",
        "The explicit Aleppo ḥataf quotation at 2 Samuel 8:10 is present in the first canonical MAM note of October 2015 and remains in all seventeen note-bearing revisions. The February 2023 Samuel list expansion already omits it. The omission predates later note-format changes and is not caused by a newly reported manuscript form.",
        [
            "The February 2023 list has thirty semantic entries; its malformed 'not included' annotation also exposes a thirty-first ordinary link to 7:10. That explicitly excluded annotation is not a list member.",
            "No independent manuscript reading is asserted; Ben's approved addition remains unapplied.",
        ],
        [("2samuel-8", [10], [653478, 1379350, 2700554])],
        dict(
            revisions=[2700411, 2700495, 2700515, 2700730],
            list_claim="ch5:L698",
            scope_caption=True,
            allow_absent=True,
        ),
        [
            ("Canonical quotation", 407513, 653478),
            ("Samuel list expansion", 2700515, 2700730),
        ],
        [(1379350, 2700554)],
    )
    add(
        "SPECIAL-LETTER-2SAM-21-19",
        "wrong-description-present-when-added",
        "On 9 February 2023 revision 2700701 adds prose describing a large resh while retaining the existing small-resh template. The Introduction specifies a small resh immediately before and after that edit. A later letter-size change does not explain the mismatch.",
        [
            "The historical prose is erroneous relative to the unchanged template and Introduction; no fresh manuscript inspection was made."
        ],
        [("2samuel-21", [19], [1418073, 2700701])],
        dict(revisions=[2700515, 2700730], refs=[["2Samuel", 21, 19]]),
        [("Large-resh prose added", 1418073, 2700701)],
        [(1418073, 2700701)],
    )
    add(
        "SAM-21-12",
        "dated-note-expansion-with-partial-appendix-update",
        "The Introduction's two-word example was added on 9 February 2023, agreeing with the contemporary note. On 5 March 2024 the appendix adds a three-word catalogue entry but retains the entire old nine-item two-word line, including this verse. Five minutes later the canonical note expands to three words; on 13 March its template name is corrected. Chapter 5 retains its older two-word description. The history establishes a partial update, while the intended counting scope remains open.",
        [
            "The new three-word catalogue does not by itself decide whether the overlapping two-word classification was intentional.",
            "No Ben adjudication or source-text edit is added.",
        ],
        [("2samuel-21", [12], [2824160, 2842695, 2842697, 2844021])],
        dict(
            revisions=[2700733, 2700734, 2841570, 2865999, 2841701, 2842694],
            refs=[["2Samuel", 21, 12]],
            allow_absent=True,
        ),
        [
            ("Introduction example", 2700733, 2700734),
            ("Appendix partial update", 2841701, 2842694),
            ("Three-word note", 2824160, 2842695),
            ("Template name corrected", 2842697, 2844021),
        ],
        [
            (2700733, 2700734),
            (2841701, 2842694),
            (2824160, 2842695),
            (2842697, 2844021),
        ],
    )
    for cid, verse, explanation in [
        ("ALL-HATAF-SAM-24-16", 16, "the resh ḥataf in the Aleppo ketiv"),
        ("ALL-HATAF-SAM-24-18", 18, "the nun ḥataf qamats in the Aleppo ketiv"),
    ]:
        add(
            cid,
            "insufficient-semantic-evidence-for-list-category",
            "The exact Aleppo ketiv quotation is already in the October 2015 canonical MAM import and remains unchanged in all twenty-four note-bearing revisions. It predates the February 2023 Samuel list expansion, which omits it. History therefore excludes a later note addition as the cause, but does not establish the phonetic function of "
            + explanation
            + " or its eligibility for this list.",
            [
                "A literal ḥataf mark is not proof of the non-guttural vowel category intended by the list.",
                "This is an unresolved category question, not a confirmed missing entry.",
            ],
            [("2samuel-24", [verse], [653491])],
            dict(
                revisions=[2700515, 2700730], list_claim="ch5:L698", scope_caption=True
            ),
            [
                ("Canonical ketiv quotation", 407553, 653491),
                ("Samuel list expansion", 2700515, 2700730),
            ],
        )
    add(
        "ALL-HATAF-GEN-30-27",
        "omission-present-when-Genesis-numeric-count-assigned",
        "The Leningrad note's ḥataf form is unchanged from the October 2015 canonical import. On 31 August 2023 the Genesis list moves from thirty-one entries with an unknown count to thirty-two entries with a count of thirty-two, adding only 49:23; 30:27 is absent on both sides and at every observed assembly stage. The omission was present during list assembly, rather than caused by a later note change.",
        [
            "The Torah section still carries a work-in-progress marker, so assigning the Genesis count is not proof that the whole section was completed.",
            "Ben's approved addition and revised current total remain unapplied.",
        ],
        [("genesis-30", [27], [655648, 2797075, 2797080])],
        dict(
            revisions=[2778793, 2778794, 2778988, 2799568, 2800792, 2835961],
            list_claim="ch3:L1126",
            allow_absent=True,
        ),
        [("Genesis count assigned", 2799568, 2800792)],
        [(2799568, 2800792)],
    )
    add(
        "ALL-HATAF-NUM-10-9",
        "omission-present-when-Numbers-numeric-count-assigned",
        "The linked December 2013 MAM draft already explicitly documents Leningrad's ḥataf; the canonical note retains it from its 2015 import. On 2 October 2023 the Numbers list is created with seven entries and an unknown count at 15:26, then assigned eighteen entries at 15:41. Numbers 10:9 is absent at both stages and throughout the twelve inspected October-2 snapshots. The omission was present during assembly, rather than caused by a later canonical-note addition.",
        [
            "The section remains marked under construction into January 2024; Ben's phonetic question is separately unresolved.",
            "Ben's approved addition remains unapplied.",
        ],
        [("numbers-10", [9], [655593])],
        dict(
            revisions=[2806427, 2806435, 2806441, 2806442, 2806467, 2812137, 2834443],
            list_claim="ch3:L1132",
            allow_absent=True,
        ),
        [
            ("Numbers list created", 2806427, 2806435),
            ("Count assigned eighteen", 2806441, 2806442),
        ],
        [(2806427, 2806435), (2806441, 2806442)],
        extra_notes=[dict(revision=519486, note="Numbers 10:9/2/0")],
    )
    add(
        "TORAH-SPELLING-NAMES",
        "mixed-chronology-later-certainty-and-original-qualification",
        "For Numbers 1:10 the canonical note resolves the formerly doubtful one-atom Leningrad name on 17 December 2023; the Introduction retains its older question marks. For 10:19 the linked December 2013 draft is already explicit about two atoms before the Introduction adds its question marks later that day. The first mismatch follows a later clarification; the second was present when the qualification appeared.",
        [
            "The exact 2013 qualification insertion is bounded by revisions 519598 and 519608 here.",
            "Different confidence does not prove which source's manuscript judgment is justified; no scan or interpretation change is made.",
        ],
        [
            ("numbers-1", [10], [655582, 2815664, 2825395]),
            ("numbers-10", [19], [655593]),
        ],
        dict(
            revisions=[519598, 519608, 519609, 519610, 519611, 2812137, 2835961],
            refs=[["Numbers", 1, 10], ["Numbers", 10, 19]],
            allow_absent=True,
        ),
        [
            ("Numbers 1:10 clarification", 2815664, 2825395),
            ("Numbers 10:19 observed qualification interval", 519598, 519608),
        ],
        [(2815664, 2825395)],
        extra_notes=[dict(revision=519486, note="Numbers 10:19/2/0")],
    )
    add(
        "PS-17-14-MAQAF",
        "not-explained-by-later-canonical-note-change-origin-undated",
        "Both explicit Leningrad alternatives have maqaf in every one of the thirty canonical MAM-note revisions from January 2016 onward. Chapter 2's contrary wording is present by the observed 26 November 2025 revision and remains in the pinned cache. A later canonical-note maqaf change cannot explain the discrepancy; the exact Introduction insertion remains undated.",
        [
            "The 2011 pre-MAM public text is not assumed to be the draft consulted by the Introduction.",
            "No physical manuscript reading is independently verified.",
        ],
        [("psalms-17", [14], [671397, 1401358, 2707399])],
        dict(revisions=[2965114, 2965129], refs=[["Psalms", 17, 14]]),
        [("Observed Introduction wording", 2965114, 2965129)],
    )
    add(
        "L-CANDIDATE-PS-17-14",
        "attribution-tension-present-when-Introduction-candidate-added",
        "At 20:43:14 on 6 March 2023 the note explicitly assigns the selected pattern to Sassoon/general Aleppo practice and retains two different Leningrad alternatives. Fourteen seconds later the Introduction adds that first pattern as a third possible Leningrad reading. The attribution question is present at the candidate's addition, rather than caused by a later note expansion.",
        [
            "The question mark may preserve a legitimate manuscript uncertainty; the note's two alternatives do not disprove a third physical reading.",
            "The supporting source for the extra Leningrad candidate remains unidentified.",
        ],
        [("psalms-17", [14], [1401358, 2707399])],
        dict(revisions=[2707149, 2707400], refs=[["Psalms", 17, 14]]),
        [
            ("Contemporary note", 1401358, 2707399),
            ("Introduction candidate added", 2707149, 2707400),
        ],
        [(1401358, 2707399), (2707149, 2707400)],
    )
    add(
        "ALL-HATAF-PS-17-14-SOURCE",
        "later-scope-caption-retains-earlier-Sassoon-entry-origin-bounded",
        "The Sassoon 1053 entry is present by 7 March 2023 under a generic ḥataf heading with a cross-reference paragraph. The narrower Aleppo-or-Leningrad caption is already present by 30 June 2024 and retains the same Sassoon entry. The chapter note's source attribution is not a later conflicting reading. The observed sequence points to a scope-caption issue; its exact insertion remains undated.",
        [
            "The first observed entry is not claimed to be its insertion.",
            "The missing Aleppo section does not acquire a direct quotation merely from this caption.",
            "A broader scope description or explicit exception remains an editorial decision.",
        ],
        [("psalms-17", [14], [671397, 2707399])],
        dict(
            revisions=[2707462, 2865999, 2879657, 2891769, 2892878, 2892889],
            list_claim="ch5:L710",
            scope_caption=True,
        ),
        [("Observed scope-caption interval", 2707462, 2865999)],
    )
    plan = dict(
        method="Independent cached-source readers supplied semantic findings; the single report writer selected literal before/after sources. Complete canonical chapter histories are distinguished from selected Introduction snapshots. Exact note states retain codepoints; source sigils and historical confidence are interpreted manually. A successful compile verifies provenance and coverage only, not consistency.",
        cases=records,
    )
    audit.dump("history-batch3-plan.json", plan)
    history_batch_compile.main("history-batch3")
