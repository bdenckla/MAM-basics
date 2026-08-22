"""
Spell check English text in HTML output files under gh-pages/

Usage:
    python ./check_spelling_in_quirkrecs.py
"""

import json
import re
from html.parser import HTMLParser
from pathlib import Path
from spellchecker import SpellChecker

import boj_paths


def load_custom_dictionary(
    dict_path: Path,
) -> tuple[set[str], set[str], list[str], set[str]]:
    """Load custom words and phrases from JSON dictionary file.

    Returns (words_ci, words_exact, phrases, phrases_hebrew,
    words_hebrew, names_of_hebrew_letters) where:
    - words_ci: case-insensitive words (stored lowercased)
    - words_exact: case-sensitive words (stored in original case,
      with curly apostrophes normalized to straight)
    - phrases: multi-word English entries
    - phrases_hebrew: multi-word Hebrew entries
    - words_hebrew: Hebrew words (exact match)
    - names_of_hebrew_letters: single-letter Hebrew words (letter names)
    """
    words_ci = set()
    words_exact = set()
    phrases = []
    phrases_hebrew = []
    words_hebrew = set()
    names_of_hebrew_letters = set()
    if dict_path.exists():
        data = json.loads(dict_path.read_text(encoding="utf-8"))
        for word in data.get("words", []):
            # Normalize curly apostrophes to straight for lookup
            words_ci.add(word.replace("’", "'").lower())
        for word in data.get("words_exact", []):
            # Normalize curly apostrophes but preserve case
            words_exact.add(word.replace("’", "'"))
        phrases = data.get("phrases", [])
        phrases_hebrew = data.get("phrases_hebrew", [])
        for word in data.get("words_hebrew", []):
            words_hebrew.add(word)
        for word in data.get("names_of_hebrew_letters", []):
            names_of_hebrew_letters.add(word)
    return (
        words_ci,
        words_exact,
        phrases,
        phrases_hebrew,
        words_hebrew,
        names_of_hebrew_letters,
    )


def extract_english_words(text: str) -> list[str]:
    """Extract English words from text, ignoring Hebrew and sigla."""
    # Remove Hebrew characters (includes base letters, vowel points, accents, marks)
    text = re.sub(r"[\u0590-\u05FF]+", " ", text)
    # Remove $-prefixed sigla ($BHQ, $yod, $BHL_A, etc.)
    text = re.sub(r"\$[A-Za-z_]+", " ", text)
    # Extract words (letters including scholarly transliteration chars like š, ṣ, x)
    # Include curly apostrophe (’) as part of contractions (e.g. doesn’t)
    # Include μ for sigla like μL, μA
    words = re.findall(r"[a-zA-ZšṣḥŠṢḤμ]+(?:\u2019[a-zA-Z]+)*", text)
    return words


def extract_hebrew_words(text: str) -> list[str]:
    """Extract Hebrew words from text (letters and maqaf only)."""
    # Match sequences of Hebrew base letters (U+05D0-U+05EA) and maqaf (U+05BE)
    return re.findall(r"[\u05D0-\u05EA][\u05D0-\u05EA\u05BE]*", text)


class _TextExtractor(HTMLParser):
    """Extract visible text from HTML, skipping <style>, <script>, and lang="hbo" elements.

    Text inside <span class="unpointed-tanakh"> is collected separately
    rather than included in the main text.
    """

    _SKIP_TAGS = {"style", "script"}

    def __init__(self):
        super().__init__()
        self._pieces: list[str] = []
        self._skip_depth = 0
        self._tag_stack: list[tuple[str, bool, bool]] = []
        self._hbo_depth = 0
        self._unpointed_tanakh_depth = 0
        self._unpointed_tanakh_pieces: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in self._SKIP_TAGS:
            self._skip_depth += 1
        attrs_dict = dict(attrs)
        is_hbo = attrs_dict.get("lang") == "hbo"
        is_upt = tag == "span" and attrs_dict.get("class") == "unpointed-tanakh"
        self._tag_stack.append((tag, is_hbo, is_upt))
        if is_hbo:
            self._hbo_depth += 1
        if is_upt:
            self._unpointed_tanakh_depth += 1

    def handle_endtag(self, tag):
        if tag in self._SKIP_TAGS and self._skip_depth > 0:
            self._skip_depth -= 1
        while self._tag_stack:
            popped_tag, was_hbo, was_upt = self._tag_stack.pop()
            if was_hbo and self._hbo_depth > 0:
                self._hbo_depth -= 1
            if was_upt and self._unpointed_tanakh_depth > 0:
                self._unpointed_tanakh_depth -= 1
            if popped_tag == tag:
                break

    def handle_data(self, data):
        if self._skip_depth > 0 or self._hbo_depth > 0:
            return
        if self._unpointed_tanakh_depth > 0:
            self._unpointed_tanakh_pieces.append(data)
        else:
            self._pieces.append(data)

    def get_text(self) -> str:
        return " ".join(self._pieces)

    def get_unpointed_tanakh_text(self) -> str:
        return " ".join(self._unpointed_tanakh_pieces)


def check_straight_apostrophes(html_files: list[Path]):
    """Check for straight apostrophes (U+0027) in HTML text; curly (’) should be used."""
    issues = []
    for html_path in html_files:
        text, _ = _extract_text_from_html(html_path)
        rel = html_path.as_posix()
        for match in re.finditer(r"'", text):
            context = text[max(0, match.start() - 10) : match.end() + 10]
            issues.append({"file": rel, "context": context})
    return issues


def check_period_uppercase(html_files: list[Path]):
    """Check for period immediately followed by an uppercase letter (missing space)."""
    issues = []
    for html_path in html_files:
        text, _ = _extract_text_from_html(html_path)
        rel = html_path.as_posix()
        for match in re.finditer(r"\.[A-Z]", text):
            context = text[max(0, match.start() - 10) : match.end() + 10]
            issues.append({"file": rel, "context": context})
    return issues


def check_spelling(html_files: list[Path], custom_dict_path: Path):
    """Check spelling of English words in HTML files.

    Returns (issues, word_ci_freq, word_exact_freq, phrase_freq,
    phrase_heb_freq, word_heb_freq, upt_freq) where the freq dicts map each
    custom-dictionary entry to the number of times it was matched,
    and upt_freq maps unpointed-tanakh words to their frequencies.
    """
    spell = SpellChecker()
    (
        words_ci,
        words_exact,
        custom_phrases,
        custom_phrases_heb,
        words_hebrew,
        names_of_heb_letters,
    ) = load_custom_dictionary(custom_dict_path)

    # Track how many times each custom entry is matched
    word_ci_freq: dict[str, int] = {w: 0 for w in words_ci}
    word_exact_freq: dict[str, int] = {w: 0 for w in words_exact}
    phrase_freq: dict[str, int] = {p: 0 for p in custom_phrases}
    phrase_heb_freq: dict[str, int] = {p: 0 for p in custom_phrases_heb}
    word_heb_freq: dict[str, int] = {w: 0 for w in words_hebrew}
    letter_name_freq: dict[str, int] = {w: 0 for w in names_of_heb_letters}
    upt_freq: dict[str, int] = {}

    issues = []

    for html_path in html_files:
        text, upt_text = _extract_text_from_html(html_path)

        # Count unpointed-tanakh Hebrew words
        for heb_word in extract_hebrew_words(upt_text):
            upt_freq[heb_word] = upt_freq.get(heb_word, 0) + 1

        # Normalize whitespace so phrase matching works
        # (the HTML text extractor can produce runs of whitespace)
        cleaned = re.sub(r"\s+", " ", text)

        # Remove accepted phrases before word extraction, counting hits
        for phrase in custom_phrases:
            pattern = re.compile(re.escape(phrase), flags=re.IGNORECASE)
            matches = pattern.findall(cleaned)
            phrase_freq[phrase] += len(matches)
            cleaned = pattern.sub(" ", cleaned)
        for phrase in custom_phrases_heb:
            pattern = re.compile(re.escape(phrase))
            matches = pattern.findall(cleaned)
            phrase_heb_freq[phrase] += len(matches)
            cleaned = pattern.sub(" ", cleaned)

        # Check English words
        words = extract_english_words(cleaned)
        for word in words:
            # Normalize curly apostrophe to straight for lookups
            normalized = word.replace("’", "'")
            lookup_lower = normalized.lower()
            if normalized in words_exact:
                word_exact_freq[normalized] += 1
            elif lookup_lower in words_ci:
                word_ci_freq[lookup_lower] += 1
            elif lookup_lower not in spell:
                rel = html_path.as_posix()
                issues.append(
                    {
                        "file": rel,
                        "word": word,
                        "suggestions": list(spell.candidates(word.lower()) or [])[:5],
                    }
                )

        # Check Hebrew words
        heb_words = extract_hebrew_words(cleaned)
        for heb_word in heb_words:
            if heb_word in names_of_heb_letters:
                letter_name_freq[heb_word] += 1
            elif heb_word in words_hebrew:
                word_heb_freq[heb_word] += 1
            else:
                rel = html_path.as_posix()
                issues.append(
                    {
                        "file": rel,
                        "word": heb_word,
                        "suggestions": [],
                    }
                )

    return (
        issues,
        word_ci_freq,
        word_exact_freq,
        phrase_freq,
        phrase_heb_freq,
        word_heb_freq,
        letter_name_freq,
        upt_freq,
    )


def main(*, verbose=False):
    # Two roots, spelled apart on purpose: the pages checked are DATA and stay in
    # book-of-job, the custom dictionary is CODE and travels beside this module.
    # One Path(__file__).parent stood for both until Phase 1 of the evacuation plan.
    docs_dir = boj_paths.gh_pages_dir()
    custom_dict_path = Path(__file__).parent / "check_spelling_in_html.custom-dict.json"

    if not docs_dir.exists():
        print(f"Error: {docs_dir} not found")
        print("Run: python main_gen_misc_authored_english_documents.py")
        return

    html_files = _collect_html_files(docs_dir)
    if not html_files:
        print(f"Error: no HTML files found under {docs_dir}")
        return

    if verbose:
        print(
            f"Checking spelling in {len(html_files)} HTML file(s) under {docs_dir}..."
        )
        print(f"Using custom dictionary: {custom_dict_path}")

    apos_issues = check_straight_apostrophes(html_files)
    if apos_issues:
        print(f"\nFound {len(apos_issues)} straight-apostrophe issues (use ’ not '):\n")
        for issue in apos_issues:
            print(f"  [{issue['file']}]: ...{issue['context']}...")

    period_issues = check_period_uppercase(html_files)
    if period_issues:
        print(
            f"\nFound {len(period_issues)} period-uppercase issues (missing space?):\n"
        )
        for issue in period_issues:
            print(f"  [{issue['file']}]: ...{issue['context']}...")

    (
        issues,
        word_ci_freq,
        word_exact_freq,
        phrase_freq,
        phrase_heb_freq,
        word_heb_freq,
        letter_name_freq,
        upt_freq,
    ) = check_spelling(html_files, custom_dict_path)

    # Write custom dictionary frequency reports
    out_dir = boj_paths.out_dir()
    out_dir.mkdir(exist_ok=True)

    def _make_freq_report(sorter):
        return {
            "words": {k: v for k, v in sorter(word_ci_freq.items())},
            "words_exact": {k: v for k, v in sorter(word_exact_freq.items())},
            "phrases": {k: v for k, v in sorter(phrase_freq.items())},
            "phrases_hebrew": {k: v for k, v in sorter(phrase_heb_freq.items())},
            "words_hebrew": {k: v for k, v in sorter(word_heb_freq.items())},
            "names_of_hebrew_letters": {
                k: v for k, v in sorter(letter_name_freq.items())
            },
            "words_unpointed_tanakh": {k: v for k, v in sorter(upt_freq.items())},
        }

    # Alphabetical order
    alpha_path = out_dir / "custom-dict-freqs-ordered-by-entry.json"
    alpha_path.write_text(
        json.dumps(_make_freq_report(sorted), indent=4, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="",
    )

    # By count (descending), then alphabetical within same count
    def by_count(items):
        return sorted(items, key=lambda x: (-x[1], x[0]))

    count_path = out_dir / "custom-dict-freqs-ordered-by-count.json"
    count_path.write_text(
        json.dumps(_make_freq_report(by_count), indent=4, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="",
    )

    # Suggest removals for zero-count entries
    unused_words = sorted(w for w, c in word_ci_freq.items() if c == 0)
    unused_words += sorted(w for w, c in word_exact_freq.items() if c == 0)
    unused_words += sorted(w for w, c in word_heb_freq.items() if c == 0)
    unused_words += sorted(w for w, c in letter_name_freq.items() if c == 0)
    unused_phrases = sorted(p for p, c in phrase_freq.items() if c == 0)
    unused_phrases += sorted(p for p, c in phrase_heb_freq.items() if c == 0)
    if unused_words or unused_phrases:
        print("\nSuggested removals from custom dictionary (zero occurrences):")
        for w in unused_words:
            print(f"  word: {w}")
        for p in unused_phrases:
            print(f"  phrase: {p}")
    else:
        if verbose:
            print("\nAll custom dictionary entries are in use.")

    if issues:
        print(f"\nFound {len(issues)} potential spelling issues:\n")
        for issue in issues:
            print(f"  [{issue['file']}]: '{issue['word']}'")
            if issue["suggestions"]:
                print(f"    Suggestions: {', '.join(issue['suggestions'])}")

        # Group by word
        word_counts = {}
        for issue in issues:
            word = issue["word"].lower()
            word_counts[word] = word_counts.get(word, 0) + 1

        print("\n--- Summary by word ---")
        for word, count in sorted(word_counts.items(), key=lambda x: -x[1]):
            print(f"  {word}: {count} occurrence(s)")
    else:
        if verbose:
            print("\nNo spelling issues found!")

    if apos_issues or period_issues or issues:
        exit(1)


def _extract_text_from_html(html_path: Path) -> tuple[str, str]:
    """Parse an HTML file and return (visible_text, unpointed_tanakh_text)."""
    html = html_path.read_text(encoding="utf-8")
    extractor = _TextExtractor()
    extractor.feed(html)
    return extractor.get_text(), extractor.get_unpointed_tanakh_text()


def _collect_html_files(docs_dir: Path) -> list[Path]:
    """Collect all .html files under gh-pages/, recursively."""
    return sorted(docs_dir.rglob("*.html"))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    main(verbose=args.verbose)
