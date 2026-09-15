# Citing GitHub issues

Read this reference when writing or auditing issue citations.

## 6. Citing issues

1. **What a bare `#NN` means depends on where it is written.**
   1. In MAM-basics' files, and in MAM-basics' issues and comments, a bare `#NN` is a MAM-basics
      issue, and any other tracker's issue is written `repo#NN`, such as `wlc-utils#88`.
      MAM-basics' `CLAUDE.md`, "Five issue trackers", lists the collisions that make the prefix
      necessary.
   2. In MAM-private, a bare `#NN` inside an evacuated tree such as `mgketer/` means that tree's
      own tracker, and MAM-private's own issues are always written `MAM-private#NN`. MAM-private's
      `CLAUDE.md`, "Issue citations", is the statement.
   3. In this skill, and anywhere a reader could be in either repository, write the repository
      out: "MAM-basics #263".
2. **In an issue or a comment, give another tracker's issue as its full URL**,
   `https://github.com/bdenckla/<repo>/issues/<number>`. GitHub turns a bare `#NN` there into a
   link to the same repository's issue, whatever was meant.
3. **Never write a bare `#NN` for a number that is not an issue**, whether in a file, an issue or
   chat. The Claude desktop app turns a bare `#NN` in chat into an issue link, and does it
   inconsistently: of `(#83, #109, #115) plus #161`, written identically, only the middle two
   became links (2026-09-04). Ben, that day: *"at a minimum, prevent a wrong link (a link to an
   unrelated (or even worse, related!) github issue) from being generated at render-time!"* Give
   such a number a form no renderer reads as an issue: a UXLC change as its change id,
   `2026.02.05-109`; a Yeivin section as "ITM section 194"; a design-document item as "design doc
   §9 item 6".
