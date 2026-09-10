The original SVG was exported from a Google Drawing:

https://docs.google.com/drawings/d/1NM3wITsGKjGZ7gfe-B5P2iH2lz_C0cAfTmKc1tp1bmM/edit?usp=sharing

That Google Drawing is no longer considered definitive.
Instead, `MAM-process.dot` is now the definitive source.

`MAM-process.dot` is hand-authored — edit it directly. `MAM-process.dot.svg`
beside it is rendered from it by `py/main_pipeline_graph.py`, which also
generates this directory's other graph, `pipeline.dot` and `pipeline.svg`. Run
it from the repo root after editing the `.dot`:

    C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_pipeline_graph.py

Do not render the SVG with a hand `dot` invocation: that bypasses the Graphviz
version pin in `py/mb_cmn/graphviz_pin.py`, which is how this SVG came to sit
two Graphviz majors behind every other tracked SVG here until 2026-09-09.
