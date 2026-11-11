# MAM-with-doc images that no page uses

The 36 images in this directory were in `gh-pages/MAM-with-doc/misc/img/` until 2026-11-10, and
so were published, although no page used them. They arrived with the rest of MAM-with-doc in
`5a28bc0e`, "Land MAM-with-doc product and Pages tree" (2026-09-06), and no page referenced them
then either. Ben decided on 2026-11-10 to move them here: "just move them somewhere not in
gh-pages (so we don't have to evaluate whether they actually can be deleted)".

Each image keeps its path below `misc/img/`. To show one again, move it back to the same path
below `gh-pages/MAM-with-doc/misc/img/` and reference it from its page's generator.

By their names, they belong with these pages, which `py/main_authored.py gen-misc` writes:

1. The review of Chabad's CTR, `misc/rocc_0_review_of_ctr.html`, and its parts: the 11 images
   in `ayin/` and the 18 here whose names begin `rocc`.
2. The part on the provenance of CTR, `misc/rocc_1_on_the_provenance_of_ctr.html`: the two
   `CTR CD-ROM box` images and the three `Soncino Classics Collection` images.
3. `misc/tsinnorit_and_the_xxd_in_bhs.html`: the two images in `BHS/`, which
   `py/author_misc/tsinnorit_and_the_xxd_in_bhs.py` names in two commented-out lines.
