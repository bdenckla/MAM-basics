"""Additional styles for near-Aleppo documentation under gh-pages/near-aleppo/.

The pages load MAM-parsed's shared stylesheet first for English typography.
This stylesheet adds the Hebrew examples, template notation and specialized
tables. Pointed Hebrew uses 20pt Taamey D from the page set's font copy.
Unpointed Hebrew inherits the surrounding text's default font and size.
The HTML isolates bidirectional runs with bdi elements.
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
  --rule: light-dark(#c9cad0, #45464d);
  --table-head: light-dark(#f1f2f5, #232429);
  --code-background: light-dark(#f3f3f5, #202126);
  --spelling-mnu: light-dark(#174ea6, #9cc2ff);
  --spelling-mun: light-dark(#8e2455, #ffafd1);
  --example-difference: light-dark(#006b5f, #75dacb);
  --template-syntax: light-dark(#5c3aa4, #cbb7ff);
  --template-name: light-dark(#974600, #ffc18a);
}

.pointed {
  font-family: "Taamey D", "SBL Hebrew", "Ezra SIL", serif;
  font-size: 20pt;
  line-height: 1.7;
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
"""
