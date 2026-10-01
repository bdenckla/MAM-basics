# Opening Book-of-Job HTML

The rendered Book-of-Job pages are files under `gh-pages/book-of-job/` in the
checkout that generated them. Give Ben an absolute `file:///` link to the page in
that checkout and let Ben open it; do not launch a browser or start a local
server. From a clone in `$HOME/GitRepos`, for example:

[BHQ Job main article](file:///C:/Users/BenDe/GitRepos/MAM-basics/gh-pages/book-of-job/jobn/job2_main_article.html)

The pages use relative resources and work as files. A browser may not honor a
fragment anchor in a `file:///` URL consistently; still give the exact link,
including the fragment, rather than creating a local server as a workaround.
