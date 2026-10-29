from pathlib import Path


def fails_filename(qaoutdir, font_fna, check_type, tcases_fna):
    font_stem = Path(font_fna).stem  # e.g. Taamey_D from font-m-TaD/Taamey_D.ttf
    tcases_stem = tcases_fna.stem
    basename = (
        f"{check_type}_{tcases_stem}" + ".json"
    )  # e.g. regression_bible_words_21.testcases.json
    return qaoutdir / font_stem / basename
    # E.g. qa-out/Taamey_D/regression_bible_words_21.testcases.json
