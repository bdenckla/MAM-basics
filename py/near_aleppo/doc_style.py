"""Styles for the near-Aleppo documentation under gh-pages/near-aleppo/.

The stylesheet declares color-scheme and defines each color once as a light-dark()
custom property. Pointed Hebrew uses 20pt Taamey D from the page set's font copy.
Unpointed template and parameter names are slightly larger than surrounding
English. The HTML isolates bidirectional runs with bdi elements.
"""


def css(generated_by):
    """The stylesheet's text, opening with the comment ``generated_by``."""
    return _CSS_TEMPLATE.replace("GENERATED_BY", generated_by)


_CSS_TEMPLATE = """\
/* GENERATED_BY */

@font-face {
  font-family: "Taamey D";
  src: url("woff2/Taamey_D.woff2") format("woff2");
}

:root {
  color-scheme: light dark;
  --text: light-dark(#1d1d1f, #e8e8ea);
  --background: light-dark(#ffffff, #141416);
  --link: light-dark(#0b57d0, #8ab4f8);
  --link-visited: light-dark(#6b3fa0, #c9a7f5);
  --rule: light-dark(#c9cad0, #45464d);
  --table-head: light-dark(#f1f2f5, #232429);
  --code-background: light-dark(#f3f3f5, #202126);
  --spelling-mnu: light-dark(#174ea6, #9cc2ff);
  --spelling-mun: light-dark(#8e2455, #ffafd1);
  --example-difference: light-dark(#006b5f, #75dacb);
  --template-syntax: light-dark(#5c3aa4, #cbb7ff);
  --template-name: light-dark(#974600, #ffc18a);
}

body {
  font-size: 13pt;
  line-height: 1.55;
  color: var(--text);
  background-color: var(--background);
  max-width: 52em;
  margin: 0 auto;
  padding: 0 16px 4em;
}

a {
  color: var(--link);
}

a:visited {
  color: var(--link-visited);
}

h1,
h2,
h3 {
  line-height: 1.25;
}

h2 {
  margin-top: 2em;
  padding-top: 0.4em;
  border-top: 1px solid var(--rule);
}

[lang="hbo"] {
  font-family: "Taamey D", "SBL Hebrew", "Ezra SIL", serif;
}

.pointed {
  font-size: 20pt;
  line-height: 1.7;
}

.name {
  font-size: 1.15em;
}

code {
  font-size: 0.92em;
  background-color: var(--code-background);
  padding: 0 0.25em;
  border-radius: 3px;
}

.table-wrap {
  overflow-x: auto;
}

.template-example {
  overflow-wrap: anywhere;
}

.template-syntax {
  color: var(--template-syntax);
}

.template-name {
  color: var(--template-name);
}

.template-ellipsis {
  background-color: var(--code-background);
  border-radius: 0.2em;
  padding: 0 0.2em;
}

.qamats-example {
  font-feature-settings: "ss03";
}

.display-example {
  text-align: center;
}

.display-table table {
  margin: 1em auto;
}

.display-table .display-example {
  margin: 0;
}

.display-example .pointed {
  letter-spacing: 0.2em;
}

.example-difference {
  color: var(--example-difference);
}

.example-space {
  background-color: var(--example-difference);
  white-space: pre;
}

table {
  border-collapse: collapse;
  margin: 1em 0;
}

th,
td {
  border: 1px solid var(--rule);
  padding: 0.35em 0.65em;
  vertical-align: middle;
  text-align: start;
}

th {
  background-color: var(--table-head);
}

td.spelling-mnu,
td.spelling-mun {
  text-align: center;
  font-weight: 600;
}

td.spelling-mnu {
  color: var(--spelling-mnu);
}

td.spelling-mun {
  color: var(--spelling-mun);
}

td.bcv {
  white-space: nowrap;
  padding-left: 0.9em;
}

td.num {
  text-align: end;
  white-space: nowrap;
}

li {
  margin-bottom: 0.35em;
}
"""
