from __future__ import annotations

from collections.abc import Iterator

from hkq_cmn.template_name_quotes import canonical_template_name
from mb_cmn import template_names

# Folded once here for the same reason each comparison below folds: a plus file
# written before MAM-parsed 2993dbd spells this name with an ASCII quote rather
# than the gershayim the constant carries.
_INVERTED_NUN_CMP = canonical_template_name(template_names.INVERTED_NUN)


def _numeric_key(kind: str, key: object) -> int:
    """Convert a numeric-string chapter/verse key to int.

    MAM-parsed plus JSON keys chapters and verses by plain numeric strings
    (e.g. "1", "24"); it no longer carries a header.he_to_int map decoding
    Hebrew-numeral keys. The "0" (superscription) and total-row sentinel
    verse keys are a plain-file concern and never appear in plus files, so no
    sentinel skip is needed here -- a non-numeric key is unexpected data and
    is surfaced as an error rather than silently skipped.
    """
    if not isinstance(key, str):
        raise ValueError(f"{kind} key must be string, got {type(key)}")
    if not key.isdigit():
        raise ValueError(f"{kind} key is not a numeric string: {key!r}")
    return int(key)


def _iter_plus_verse_payloads(
    plus_json: object,
) -> Iterator[tuple[int, int, int, object]]:
    if not isinstance(plus_json, dict):
        raise ValueError("plus JSON root must be an object")

    book39s = plus_json.get("book39s")
    if not isinstance(book39s, list):
        raise ValueError("plus JSON missing list key 'book39s'")

    for book39_index, book39 in enumerate(book39s):
        if not isinstance(book39, dict):
            raise ValueError(f"book39 entry must be object, got {type(book39)}")
        chapters = book39.get("chapters")
        if not isinstance(chapters, dict):
            raise ValueError("book39 entry missing object key 'chapters'")

        for chapter_key, verse_map in chapters.items():
            chapter_num = _numeric_key("chapter", chapter_key)
            if not isinstance(verse_map, dict):
                raise ValueError(f"chapter value must be object, got {type(verse_map)}")

            for verse_key, verse_payload in verse_map.items():
                verse_num = _numeric_key("verse", verse_key)

                yield (book39_index, chapter_num, verse_num, verse_payload)


# ---------------------------------------------------------------------------
# VARIANT-SELECTION (POSSIBLE MISSED HITS) WARNING
#
# This function renders a single flat verse string by picking ONE canonical
# param from each variant-storing template and ignoring the others:
#
#   מ:דחי / מ:צינור — uses param "1" (canonical accent); ignores param "2"
#                      (stress-helper duplicate).  A token that appears ONLY
#                      in param "2" would be silently missed.
#   מ:קמץ            — uses param "ד" (Ashkenazic qamats distinction); ignores
#                      param "ס" (Sephardic).  A vowel difference in the
#                      Sephardic param would not be seen.
#   מ:כפול           — uses param "כפול" (combined form); ignores params "א"
#                      and "ב" (individual alef/bet cantillation readings for
#                      dual-cantillation verses: Decalogue, Saga of Reuben).
#                      A token that differs between the two readings (e.g.
#                      accent-based vowel variants) might not appear in כפול.
#
# Each row above opens on Hebrew and so lays out right to left: Ben Denckla chose
# the column alignment over giving each row a Latin runway, 2026-09-02.
#
# Callers that scan the resulting text for specific features should be aware
# that hits present only in the ignored params will not be found.
# ---------------------------------------------------------------------------
# Per-template extraction rules below mirror those in:
#   MAM-parsed/gh-pages/plus/html/mpplus.html and its siblings, the rendered
#     structure reference, whose source is this repo's py/author_misc/ --
#     mpplus_aot.py for the special-letter schema, mp_cmn_groups_misc.py for
#     the navigation and book-title rows
#   MAM-private/mgketer/documentation/mpu-parsing.md (Template dispatch section)
#   qere_projection.py (project_qere_atoms)
# When changing a rule here, check all four locations.
#
# THE FIRST ENTRY NAMED A FILE THAT DOES NOT EXIST, until 2026-09-02: it read
# MAM-parsed/doc-under-readme/reading-mam-parsed-plus.md (extract_text example),
# and that whole directory is gone.  The rendered structure reference above is
# the live document, and MAM-parsed/README.md links it.
def _collect_text_fragments(node: object, out_parts: list[str]) -> None:
    """Append the verse text of one plus-JSON node to out_parts.

    WHAT A TEMPLATE MEANS DECIDES WHAT IT CONTRIBUTES, AND WHETHER IT CARRIES
    PARAMETERS DOES NOT.  Every rule below dispatches on the template NAME, and
    a name with no rule RAISES rather than contributing a guess.

    Reading a parameter as a proxy for a meaning is the defect this dispatch
    replaced, on 2026-09-02.  "A template with no parameters carries no text"
    is sound,
    and the fallback below still rests on it.  But this function also read the
    CONVERSE -- a template with parameters carries verse text -- in a loop that
    collected every parameter of anything it did not recognise.  The converse is
    false, and it put documentation into the string callers count atoms in.

    THE CORPUS SETTLES IT, RATHER THAN ARGUMENT.  Four templates appear in
    MAM-parsed both with and without a parameter: the setuma and petucha
    markers סס (1519 parameter-free against 35 parameter-bearing), ססס (404
    against 26), פפ (1545 against 8) and פפפ (3 against 15).  In all 84 of the
    parameter-bearing cases the parameter is one identical string: it is the
    note פסקא באמצע פסוק, which names what the marker is.  So one marker with
    one meaning was getting opposite treatment according to whether a note had
    been written into it.  Exodus 20:13 holds one of each.  Its parameter-free
    marker סס contributed a space, correctly, while its parameter-bearing ססס
    put three atoms of Hebrew documentation into the verse and fused them onto
    both neighbours.  Where that verse has רֵעֶ֑ךָ and לֹֽא, it rendered the
    three atoms רֵעֶ֑ךָפסקא, then באמצע, then פסוקלֹֽא.

    SEVEN THINGS LEAKED THIS WAY, measured 2026-09-02 over MAM-parsed 54ba7e0.
    Re-measure rather than trusting the figures, and treat a mismatch as a
    finding.  Together they changed the atom count of 507 verses:

      1. the navigation template מ:פסוק, in 895 payloads, leaking book name,
         chapter, verse, seder and aliyah
      2. the aliyah template מ:עלייה, 532, reached only inside the navigation
         template
      3. the book-title template מ:ספר חדש, 24
      4. the four setuma and petucha markers named above, 84
      5. the minor-prophets first-verse spacing template, 12, whose parameter
         is a prophet name: מ:רווח בתרי עשר בפסוק הראשון
      6. the Psalms-division first-verse spacing template, 5, whose parameter
         is a division name: מ:רווח לספר בתהלים בפסוק הראשון
      7. the special-letter template מ:אות-מיוחדת-במילה, 51, which is not
         metadata but collected all five of its parameters, so that the word
         went in twice and three parameters of documentation followed it

    Genesis 1:1 is the worked example.  It rendered 9 atoms for a seven-word
    verse, its first atom running the book title, the whole navigation
    reference and two copies of בְּרֵאשִׁית together, and two atoms of
    documentation after that.
    """
    if isinstance(node, str):
        out_parts.append(node)
        return
    if isinstance(node, list):
        for item in node:
            _collect_text_fragments(item, out_parts)
        return
    if isinstance(node, dict):
        tmpl_name = node.get("tmpl_name")
        # Folded to ASCII quotes for matching the quote-bearing literals below;
        # tmpl_name itself (gershayim) is never stored from this function.
        cmp_name = canonical_template_name(tmpl_name)
        tmpl_params = node.get("tmpl_params")
        if tmpl_name in template_names.NO_VERSE_TEXT_TMPL_NAMES:
            # A TEMPLATE THAT CARRIES NO VERSE TEXT SEPARATES THE TEXT AROUND
            # IT, so it contributes a space, whether or not it has parameters.
            # The set is declared in mb_cmn/template_names.py; the docstring
            # above says why the meaning has to be named there rather than read
            # off the presence of a parameter.
            #
            # A SEPARATOR IS THE WHOLE OF WHAT ATOM COUNTING NEEDS, and a space
            # is one.  None of these templates is an atom, and none joins the
            # text around it into one atom.  So nothing here decides how such a
            # template RENDERS: whether the paseq template מ:פסק emits U+05C0,
            # or the gray-maqaf template מ:מקף אפור a maqaf, is a separate
            # question this rule neither asks nor answers.  Ben Denckla settled
            # that separation on 2026-09-02, noting that a gray maqaf raises a
            # real question only for CHANTED WORD counting, which this function
            # does not do.
            #
            # The set covers the shirah spaces of the Song of Deborah, which
            # fused בֶּן־עֲנָת֙ and בִּימֵ֣י in Judges 5:6 so that the verse counted
            # 11 atoms where it has 13.  See foi/kq_trivial_types.py, which
            # groups the same names the same way for a different purpose.
            out_parts.append(" ")
            return
        if not isinstance(tmpl_params, dict):
            # A TEMPLATE WITH NO PARAMETERS CARRIES NO TEXT, and separates the
            # text around it, so it contributes a space.  This is the FALLBACK
            # for a name the set above does not list, and it is sound in that
            # one direction only -- the docstring says what converse it does not
            # license.  Before this rule such a template fell through the whole
            # function and contributed NOTHING, which silently FUSED the atoms
            # on either side of it and put every atom index after it out by one.
            #
            # THE TWO RULES ARE INDEPENDENT, NEITHER ONE A SUPERSET.  This one
            # replaced a WHITESPACE_TMPL_NAMES branch on 2026-09-02, and 757aa68
            # said it subsumed that branch, which was wrong in both directions.
            # The poetic-space marker ר4 occurs 4269 times, always without a
            # parameter, and has never been in that set, so only this rule
            # reaches it; while the 84 parameter-bearing setuma and petucha
            # markers of the docstring were handled by that branch, and are
            # handled by the set above now.
            #
            # Measured 2026-09-02 over MAM-parsed/plus: this rule separates 626
            # fused atoms across 559 verses -- the paseq template מ:פסק 508
            # times, the gray-maqaf template מ:מקף אפור 116 times, and the
            # legarmeh template מ:לגרמיה-2 twice.  Every other parameter-free
            # template already stands beside a space and gains nothing.  The
            # case that produced the rule is Judges 1:7, whose one paseq
            # template sits between שִׁבְעִ֣ים and מְלָכִ֡ים: fused, the verse counts
            # 22 atoms and Jerusalem lands at 20; separated, 23 and 21, and 21
            # is the number Daniel Holman sent.
            out_parts.append(" ")
            return
        if tmpl_name == "נוסח" or tmpl_name == "מ:הערה-2":
            # Param 1 is the in-verse target; param 2 is documentation.
            _collect_text_fragments(tmpl_params.get("1"), out_parts)
            return
        if tmpl_name == "מ:הערה":
            # Suppressed note — no verse text.
            return
        if tmpl_name in ("מ:דחי", "מ:צינור"):
            # Two-param stress-variant template.  Param "1" is the canonical
            # (clean) form; param "2" adds a stress-helper duplicate accent.
            _collect_text_fragments(tmpl_params.get("1"), out_parts)
            return
        if tmpl_name == "מ:קמץ":
            # Two-param qamats template.  Param "ד" (dikduk) is the canonical
            # qamats-gadol/qamats-qatan distinction; param "ס" is Sephardic.
            _collect_text_fragments(tmpl_params.get("ד"), out_parts)
            return
        if tmpl_name == "מ:כפול":
            # "Double-cantillation" template.  Param "כפול" is the combined form.
            _collect_text_fragments(tmpl_params.get("כפול"), out_parts)
            return
        if tmpl_name == "כתיב ולא קרי":
            # Written-but-not-read: contributes nothing to the reading text.
            return
        if tmpl_name == "קרי ולא כתיב":
            # Read-but-not-written: param 2 is the qere text.
            _collect_text_fragments(tmpl_params.get("2"), out_parts)
            return
        if cmp_name == 'מ:קו"כ-אם-2':
            # Trivial qere: param 1 is the word; param 2 is a documentation
            # string (e.g. "א-קרי=..."), not verse text.
            _collect_text_fragments(tmpl_params.get("1"), out_parts)
            return
        if 'כו"ק' in (cmp_name or "") or 'קו"כ' in (cmp_name or ""):
            # Ketiv-qere: param 1 is ketiv (written), param 2 is qere (read).
            _collect_text_fragments(tmpl_params.get("2"), out_parts)
            return
        if tmpl_name in template_names.IN_WORD_TMPL_NAMES:
            # Param 1 is the word, or the part of one, that the template marks:
            # the large letter מ:אות-ג, the small letter מ:אות-ק, the hung
            # letter מ:אות תלויה, and the whole-word template for a special
            # letter, מ:אות-מיוחדת-במילה.  The three letter templates carry
            # param 1 and nothing else; only the whole-word one has a choice
            # to make.
            #
            # THAT WORD HAS TWO COMPLETE REPRESENTATIONS, NEITHER OF THEM THE
            # ONE.  Param 1 spells it as an array decomposed around the special
            # letter, carrying the three letter templates above; params 2-4
            # spell it again as a plain string, a dot-mask and a type code,
            # from which the same conclusion about the word's contents can be
            # reached.  Param 5 is a letter/type summary derivable from params 3
            # and 4.  py/author_misc/mpplus_aot.py states that schema and
            # MAM-parsed/gh-pages/plus/html/mpplus_aot.html is what it renders.
            #
            # PARAM 1 IS TAKEN BECAUSE THE OTHER THREE FLATTENERS TAKE IT, not
            # because it is easier to flatten -- param 2 is already a plain
            # string and param 1 is a tree, so param 2 is the flatter of the
            # two.  qere_projection.py recurses into param 1 for all four of
            # these names, foi/kq_trivial_types.py falls through to element 1,
            # and MAM-private's mpu-parsing.md says outright that param 2 is
            # discarded.  Taking param 1 also lets one rule cover all four
            # names, param 1 being where the other three sit.
            #
            # Atom counts do not decide it: measured 2026-09-02, param 1 and
            # param 2 give the same count in all 51 cases, and differ in text at
            # only 4, where a מ:לגרמיה-2 at the end of param 1 becomes a space
            # while param 2 has the paseq/legarmeh character appended instead.
            _collect_text_fragments(tmpl_params.get("1"), out_parts)
            return
        if cmp_name == _INVERTED_NUN_CMP:
            # The inverted nun, whose param 1 is the character itself (U+05C6).
            # Keeping it changes no atom count, U+05C6 being outside
            # find_hebrew_tokens' character class, so this rule preserves what
            # the collect-everything loop did rather than altering it.
            # qere_projection.py and MAM-private's mpu-parsing.md both drop the
            # template instead, which no atom count can distinguish.
            _collect_text_fragments(tmpl_params.get("1"), out_parts)
            return
        raise ValueError(
            f"no verse-text rule for template {tmpl_name!r}"
            f" carrying parameters {sorted(str(key) for key in tmpl_params)}."
            " A template either carries no verse text, and belongs in"
            " template_names.NO_VERSE_TEXT_TMPL_NAMES, or it carries some, and"
            " needs a rule here naming which parameters. Check the four mirror"
            " locations listed above this function when adding one."
        )


def _render_template_like_text(node: object) -> str:
    if isinstance(node, str):
        return node

    if isinstance(node, list):
        return "".join(_render_template_like_text(item) for item in node)

    if isinstance(node, dict):
        tmpl_name = node.get("tmpl_name")
        tmpl_params = node.get("tmpl_params")
        if isinstance(tmpl_name, str) and isinstance(tmpl_params, dict):
            return _render_template_call(tmpl_name, tmpl_params)

        # Fallback for non-template container nodes.
        return "".join(_render_template_like_text(value) for value in node.values())

    return ""


def _render_template_call(tmpl_name: str, tmpl_params: dict[object, object]) -> str:
    rendered_args: list[str] = []
    for key, value in tmpl_params.items():
        rendered_value = _render_template_like_text(value)
        if isinstance(key, str) and key.isdigit():
            rendered_args.append(rendered_value)
        else:
            rendered_args.append(f"{key}={rendered_value}")

    if not rendered_args:
        return f"{{{{{tmpl_name}}}}}"

    return f"{{{{{tmpl_name}|{'|'.join(rendered_args)}}}}}"


def _collect_nusach_targets(node: object, out_targets: list[str]) -> None:
    if isinstance(node, list):
        for item in node:
            _collect_nusach_targets(item, out_targets)
        return

    if isinstance(node, dict):
        tmpl_name = node.get("tmpl_name")
        tmpl_params = node.get("tmpl_params")
        if isinstance(tmpl_params, dict):
            if tmpl_name == "נוסח":
                target_text = _render_template_like_text(tmpl_params.get("1")).strip()
                if target_text:
                    out_targets.append(target_text)

                # Skip param 2 because it is documentation, not verse text.
                for key, value in tmpl_params.items():
                    if key in {"1", "2"}:
                        continue
                    _collect_nusach_targets(value, out_targets)
                return

            for value in tmpl_params.values():
                _collect_nusach_targets(value, out_targets)


def verse_nusach_targets_by_location(
    plus_json: object,
) -> dict[tuple[int, int, int], list[str]]:
    out: dict[tuple[int, int, int], list[str]] = {}
    for (
        book39_index,
        chapter_num,
        verse_num,
        verse_payload,
    ) in _iter_plus_verse_payloads(plus_json):
        targets: list[str] = []
        _collect_nusach_targets(verse_payload, targets)
        out[(book39_index, chapter_num, verse_num)] = targets
    return out


def _collect_template_argument_records(
    node: object,
    out_records: list[dict[str, str]],
) -> None:
    if isinstance(node, list):
        for item in node:
            _collect_template_argument_records(item, out_records)
        return

    if isinstance(node, dict):
        tmpl_name = node.get("tmpl_name")
        tmpl_params = node.get("tmpl_params")
        if isinstance(tmpl_name, str) and isinstance(tmpl_params, dict):
            for key, value in tmpl_params.items():
                argument_key = str(key)
                # In plus JSON, נוסח param 2 is documentation, not verse text.
                if tmpl_name == "נוסח" and argument_key == "2":
                    continue

                argument_text = _render_template_like_text(value).strip()
                if argument_text:
                    out_records.append(
                        {
                            "template_name": tmpl_name,
                            "argument_key": argument_key,
                            "argument_text": argument_text,
                        }
                    )

                _collect_template_argument_records(value, out_records)
            return

        for value in node.values():
            _collect_template_argument_records(value, out_records)


def verse_template_argument_records_by_location(
    plus_json: object,
) -> dict[tuple[int, int, int], list[dict[str, str]]]:
    out: dict[tuple[int, int, int], list[dict[str, str]]] = {}
    for (
        book39_index,
        chapter_num,
        verse_num,
        verse_payload,
    ) in _iter_plus_verse_payloads(plus_json):
        records: list[dict[str, str]] = []
        _collect_template_argument_records(verse_payload, records)
        out[(book39_index, chapter_num, verse_num)] = records
    return out


def verse_texts_by_location(
    plus_json: object,
) -> dict[tuple[int, int, int], str]:
    out: dict[tuple[int, int, int], str] = {}
    for (
        book39_index,
        chapter_num,
        verse_num,
        verse_payload,
    ) in _iter_plus_verse_payloads(plus_json):
        text_parts: list[str] = []
        try:
            _collect_text_fragments(verse_payload, text_parts)
        except ValueError as exc:
            # A rule is missing, and where it is missing is the expensive half
            # to find again: name the verse rather than leaving a grep of the
            # corpus as the way to locate it.
            raise ValueError(
                f"book39 index {book39_index}, {chapter_num}:{verse_num}: {exc}"
            ) from exc
        out[(book39_index, chapter_num, verse_num)] = "".join(text_parts)
    return out
