"""Describe retained features, omissions, limitations and pending editorial work.

doc_page.py assembles these sections. The manual-task section links published
sources for readers to inspect by eye; those links are navigation, not inputs.
"""

from near_aleppo import consumer_notice
from near_aleppo.doc_html import code
from near_aleppo.doc_html import he_name
from near_aleppo.doc_html import itm
from near_aleppo.doc_html import link
from near_aleppo.doc_html import table
from near_aleppo.doc_html import verse_refs
from mb_misc import mb_html
from near_aleppo.phase2_templates import _RULES
from near_aleppo.phase2_templates import _VERBATIM
from near_aleppo.phase6_flags import _MAQAF_SILENCE
from near_aleppo.phase6_flags import _QERE_SILENCE

KEPT = ("kept-as-mam-has-it", "What near-Aleppo keeps as MAM has it")
NOT_REPRESENTED = ("not-represented", "What near-Aleppo does not represent")
LIMITATIONS = ("limitations", "Limitations")
PENDING = ("pending", "What is still pending")
MANUAL_TASK = ("manual-task", "A manual task left undone")

MGKETER = "https://www.mgketer.org/"

_P2 = "phase2_counts"
_P3 = "phase3_counts"
_P5 = "phase5_counts"
_P5S = "phase5_sites"
_READ = "codex readings: "


def _heading(section):
    return mb_html.heading_level_2(section[1], {"id": section[0]})


def sections(numbers):
    return (
        _kept(numbers)
        + _not_represented()
        + _limitations(numbers)
        + _pending(numbers)
        + _manual_task(numbers)
    )


def _kept(numbers):
    verbatim = [name for name, rule in _RULES.items() if rule.action == _VERBATIM]
    items = [
        "Both U+05A2 HEBREW ACCENT ATNAH HAFUKH and U+05AA HEBREW ACCENT YERAH BEN "
        "YOMO, the galgal: the codex tells the two apart.",
        [
            "Every rafe of MAM's, U+05BF HEBREW POINT RAFE, all ",
            numbers.fig("rafe_mam"),
            " of them; near-Aleppo has ",
            numbers.fig("rafe"),
            " in all, the others coming with readings of the codex that MAM's notes "
            "give.",
        ],
        [
            "The extraordinary dots, on ",
            numbers.fig("dots_atoms"),
            " words in ",
            numbers.fig("dots_verses"),
            " verses, as MAM has them from the codex (Yeivin, ",
            itm(),
            " §79).",
        ],
        "The two words of Deuteronomy 32:6 with the space between them, which is the "
        "codex's form, and its large he.",
        [
            "U+05BA HEBREW POINT HOLAM HASER FOR VAV wherever MAM has it, all ",
            numbers.fig("holam_haser_for_vav_mam"),
            " of them; near-Aleppo has ",
            numbers.fig("holam_haser_for_vav"),
            " in all, the others coming with readings of the codex.",
        ],
        "MAM's order of the marks on a letter, and its COMBINING GRAPHEME JOINERs: no "
        "normalization is run over MAM's strings.",
        [
            "MAM's verse numbering, and the templates near-Aleppo keeps whole, as "
            "MAM has them: ",
            *_listed([he_name(name) for name in verbatim]),
            ", among them the inverted nun, at ",
            numbers.fig("inverted_nuns"),
            " places.",
        ],
        "No ketiv/qere encoding that MAM lacks: MAM's apparatus names no site where "
        "the codex has a qere note and MAM has no ketiv/qere template.",
    ]
    return [
        _heading(KEPT),
        mb_html.para(
            "Near-Aleppo keeps the following as MAM has them. Most are features of "
            "the codex that MAM already has, and a change to any of them would move "
            "near-Aleppo away from the codex:"
        ),
        mb_html.unordered_list(items),
    ]


def _not_represented():
    return [
        _heading(NOT_REPRESENTED),
        mb_html.para(
            "Near-Aleppo represents the codex's body text and its ketiv/qere "
            "apparatus, and nothing else of the manuscript. It does not represent:"
        ),
        mb_html.unordered_list(
            [
                "The rest of the masorah: the masorah circles, the masora parva, and "
                "the masora magna. Only the qere notes are there, as MAM's ketiv/qere "
                "templates.",
                "The codex's rafe marks, beyond the few that MAM has. The codex has "
                "many more, and how many is not known.",
            ]
        ),
    ]


def _limitations(numbers):
    rows = [
        [
            "Rafe",
            [
                "The codex marks the rafe in many places where MAM does not, and how "
                "many is not known. The manuscripts use the rafe inconsistently "
                "(Yeivin, ",
                itm(),
                " §397), so near-Aleppo does not derive the missing ones by rule, "
                "which would give them a regularity the manuscripts lack. Near-Aleppo "
                "has fewer rafe marks than the codex.",
            ],
        ],
        [
            "The holam in the divine name",
            [
                "MAM's notes record the codex's holam in the divine name at ",
                numbers.snap(
                    _P3, "Adonai reading: holam kept where a note records the codex's"
                ),
                " words, and MAM does not say that they are every such place. So "
                "near-Aleppo is right in general, and wrong wherever the codex has a "
                "holam that no note records. For the divine title MAM speaks only of "
                "isolated places, but its ",
                numbers.record(
                    numbers.snap_value(_P3, "divine title: holam on the dalet stripped")
                    + numbers.snap_value(
                        _P3, "divine title: holam kept where a note records the codex's"
                    ),
                    "phase3_counts: the divine title's atoms, stripped and kept",
                ),
                " words are few enough for a person to look through.",
            ],
        ],
        [
            "The maqaf",
            [
                "MAM's introduction says, citing Yeivin's study of the codex, that "
                "about 50 places in the codex lack a maqaf after a word that should "
                "have one, and gives no list. MAM's notes name ",
                numbers.snap(
                    _P3, "maqaf: clause form has a space where the target had a maqaf"
                ),
                " such places that near-Aleppo follows; it flags 1 Kings 20:29 without "
                "following it, and leaves 1 Chronicles 9:4, 2 Samuel 8:3, and 2 Kings "
                "5:18 to later work on the ketiv/qere. The rest cannot be recovered "
                "from MAM.",
            ],
        ],
        [
            "The pointed ketiv",
            "Near-Aleppo imports an approved frozen subset of inferred pointings "
            "where MAM's notes give none. These categorical selections are not "
            "certified correct; source-ownership and transfer warnings remain in "
            "the separate source archive. Inference faces the codex's convention of which letter a "
            "mark goes on, which MAM describes as usual rather than invariable, and "
            "which MAM says it records only in part, so that an inferred pointing "
            "can differ at an unknown number of sites.",
        ],
        [
            "The sparseness of the ketiv/qere",
            "MAM declines to encode a ketiv/qere, as a policy, wherever the qere lacks "
            "only one mater lectionis, and near-Aleppo adds no encoding. So its "
            "ketiv/qere apparatus is sparser than the codex's, by an amount MAM's "
            "apparatus does not record.",
        ],
        [
            "The zarqa's stress helper",
            [
                "Near-Aleppo has no zarqa stress helper at ",
                numbers.snap(_P3, "stress helpers: zarqa's stress helper stripped"),
                " of the words where MAM has one, on Ben Denckla's assumption, not "
                "on an inspection, that the codex most likely has none of them; it keeps "
                "the one whose note records it in the codex. Where the codex is lost, "
                "the only evidence is that UXLC records none, and a stress helper is "
                "just the fine mark a transcription normalizes away. No manuscript "
                "has been read at any of those sites.",
            ],
        ],
        [
            "Special letters",
            [
                "At Job 16:14 and Job 7:5 the codex survives and MAM's notes say "
                "nothing about the special letter, so near-Aleppo has each word "
                "without it, as it does wherever it evaluates away a special-letter template: ",
                numbers.snap(_P2, "special letter word flattened"),
                " in its text, and ",
                numbers.snap(
                    _P2, "special letter word flattened (unselected parameter)"
                ),
                ", Job 7:5's, in a ketiv. At Isaiah 44:14 MAM's small letter follows "
                "the codex's margin rather than its text.",
            ],
        ],
    ]
    numbers.require_sites(
        "flag_sites", ("qualification 2: clauses flagged",), ('BC-Kings מל"א|20|29',)
    )
    numbers.require_sites(
        _P5S,
        (
            _READ + "ketiv/qere plane reading pending by name",
            _READ
            + "ketiv/qere plane reading at a one-sided template, left for later work",
        ),
        (('FC-Chronicles דה"א', "9", "4"), ('BC-Kings מל"ב', "5", "18")),
    )
    if numbers.fig_value("deferred_qere_maqaf_sites") != [('BA-Samuel שמ"ב', "8", "3")]:
        raise AssertionError("the page names 2 Samuel 8:3's deferred qere maqaf")
    return [
        _heading(LIMITATIONS),
        mb_html.para(
            "Near-Aleppo is an editorial approximation. MAM's notes do not record "
            "every manuscript departure from a general policy. Editorial guesses "
            "where Aleppo is lost remain uncertain."
        ),
        mb_html.para(
            "What near-Aleppo cannot know, or does not yet do, where it therefore "
            "differs from the codex:"
        ),
        table(["Limitation", "What it means"], rows, [None, None]),
    ]


def _pending(numbers):
    by_name = _READ + "ketiv/qere plane reading pending by name"
    one_sided = (
        _READ + "ketiv/qere plane reading at a one-sided template, left for later work"
    )
    space = (
        _READ
        + "pending, the form stopping at the codex's space for a qere without ketiv"
    )
    return [
        _heading(PENDING),
        mb_html.para(
            "The near-Aleppo dataset documented here is a first version. Still to do:"
        ),
        mb_html.unordered_list(
            [
                [
                    "The one-sided ketiv/qere templates. Where MAM has a ketiv that is "
                    "not read, the template ",
                    he_name("כתיב ולא קרי"),
                    ", at ",
                    numbers.snap(_P2, "כתיב ולא קרי"),
                    " sites, near-Aleppo's text is MAM's unpointed ketiv in round "
                    "brackets, where the codex has the unpointed letters alone. Where "
                    "MAM has a qere that is not written, the template ",
                    he_name("קרי ולא כתיב"),
                    ", at ",
                    numbers.snap(_P2, "קרי ולא כתיב"),
                    " sites, near-Aleppo still displays MAM's pointed qere. "
                    "The planned body text is empty where no letters or marks are "
                    "written. At 2 Samuel 18:20, MAM's note records tsere and merkha "
                    "without letters or space, at the join inside a maqaf compound. "
                    "A planned template specific to near-Aleppo, ",
                    he_name(consumer_notice.MARKS_WITHOUT_LETTER_OR_SPACE),
                    ", would represent those marks. The build and example renderer "
                    "do not yet implement it.",
                ],
                [
                    "The readings of the codex that wait for that work: ",
                    numbers.snap(_P5, by_name),
                    " at ketiv/qere templates (",
                    verse_refs(numbers.snap_sites(_P5S, by_name)),
                    "), ",
                    numbers.snap(_P5, one_sided),
                    " at one-sided templates (",
                    verse_refs(numbers.snap_sites(_P5S, one_sided)),
                    "), and the one at ",
                    verse_refs(numbers.snap_sites(_P5S, space)),
                    ", about the codex's unpointed space for a qere without ketiv.",
                ],
                [
                    "The clauses citing the codex that near-Aleppo has not yet read: ",
                    numbers.snap(
                        _P5, _READ + "policy-pending (candidate-form-punctuation)"
                    ),
                    " whose form has exceptional punctuation, ",
                    numbers.snap(
                        _P5, _READ + "policy-pending (candidate-form-count-0)"
                    ),
                    " that quotes no form, and ",
                    numbers.snap(
                        _P5,
                        _READ
                        + "prose-led heads ending in a codex siglum, held pending",
                    ),
                    " whose head is prose ending in a siglum of the codex.",
                ],
            ]
        ),
    ]


def _manual_task(numbers):
    sites = numbers.fig_value("silence_sites")
    am2 = [site["verse"] for site in sites if site["family"] == "מ:קו״כ-אם-2"]
    others = [site for site in sites if site["family"] != "מ:קו״כ-אם-2"]
    qere_others = [site["verse"] for site in others if site["value"] == _QERE_SILENCE]
    maqaf_others = [site["verse"] for site in others if site["value"] == _MAQAF_SILENCE]
    if len(qere_others) != 1 or len(maqaf_others) != 1 or len(others) != 2:
        raise AssertionError("the page describes the two other silence sites singly")
    return [
        _heading(MANUAL_TASK),
        mb_html.para(
            [
                "At ",
                numbers.record(len(am2), "doc_figures: silence_sites of מ:קו״כ-אם-2"),
                " sites in ",
                numbers.record(
                    len(set(map(tuple, am2))),
                    "doc_figures: the verses of the silence sites of מ:קו״כ-אם-2",
                ),
                " verses where a leaf of the codex survives, MAM has a ",
                he_name("מ:קו״כ-אם-2"),
                " whose note names another manuscript and says nothing of the codex: ",
                verse_refs(am2),
                ". MAM's apparatus being silent, near-Aleppo keeps each template and "
                "flags it, ",
                code("flagged-not-applied"),
                " with the value “",
                _QERE_SILENCE,
                "”. The same flag stands at ",
                verse_refs(qere_others),
                ", where MAM implies without saying so that the codex has no qere "
                "note, and the flag with the value “",
                _MAQAF_SILENCE,
                "” stands at ",
                verse_refs(maqaf_others),
                ", at a maqaf after a ketiv that is not read.",
            ]
        ),
        mb_html.para(
            [
                "Settling these sites by eye, in ",
                link("mgketer.org", MGKETER),
                " and in the Jerusalem Crown edition, is a tractable job, just not one "
                "done for this first version.",
            ]
        ),
    ]


def _listed(items):
    out = []
    for index, item in enumerate(items):
        if index:
            if index == len(items) - 1:
                out.append(", and " if len(items) > 2 else " and ")
            else:
                out.append(", ")
        out.append(item)
    return out
