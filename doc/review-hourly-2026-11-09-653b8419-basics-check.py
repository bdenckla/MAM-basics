"""Bounded offline artifact/function checks. Materialize selected endpoint files
into base/ and head/ beside this script, preserving repository-relative paths.
The accompanying receipt records exact commits, paths and SHA-256 identities.
This is not a project CLI regeneration or a full-environment test pass.
"""
import ast
import collections
import json
import re
import types
import unicodedata
import html as html_lib
from pathlib import Path

ROOT = Path(__file__).parent
H = ROOT / 'head'
B = ROOT / 'base'
report = {}

def selected(path, names, env):
    tree = ast.parse(path.read_text())
    nodes = [n for n in tree.body if (isinstance(n, ast.FunctionDef) and n.name in names) or (isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id in names for t in n.targets))]
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), 'exec'), env)

env = {'re': re}
selected(H/'py/foi/foi_wikitext_helpers.py', {'LETTERS_MARKS_JOINERS','DOUBLE_GUILLEMETS','_FORM','forms'}, env)
forms = env['forms']
old = json.loads((B/'gh-pages/MAM-with-doc/foi/foi-unicode.json').read_text())
new = json.loads((H/'gh-pages/MAM-with-doc/foi/foi-unicode.json').read_text())
added = [r for r in new if 'alef-with-mapiq' in r['fp']]
remaining = [r for r in new if 'alef-with-mapiq' not in r['fp']]
assert len(old) == len(remaining)
changed = []
for a,b in zip(old,remaining):
    assert (a['fp'],a['bcv_short']) == (b['fp'],b['bcv_short'])
    if a != b:
        assert 'doc-part-n' in a['fp']
        assert b['r'] in forms(a['r']), (a,b)
        changed.append(b)
report['foi_rows'] = {'base':len(old),'head':len(new),'punctuation_only_note_rows':len(changed),'new_categories':dict(collections.Counter(r['fp'] for r in added))}
assert len(added)==12
env.update(unicodedata=unicodedata,hpo=types.SimpleNamespace(DAGOMOSD=chr(0x5bc)),hl=types.SimpleNamespace(ALEF=chr(0x5d0)))
selected(H/'py/foi/foiz_wt_unicode.py', {'_has_alef_with_mapiq'},env)
assert all(env['_has_alef_with_mapiq'](r['r']) for r in added)
assert all(re.search(chr(0x5d0)+r'[^\u05d0-\u05ea]*'+chr(0x5bc),r['r']) for r in added)
report['new_category_locations'] = dict(collections.Counter(r['bcv_short'] for r in added))
for name in ['custom-dict-freqs-ordered-by-count.json','custom-dict-freqs-ordered-by-entry.json']:
    a=json.loads((B/'book-of-job/out'/name).read_text()); b=json.loads((H/'book-of-job/out'/name).read_text())
    delta={k:v-a['words_exact'][k] for k,v in b['words_exact'].items() if v!=a['words_exact'][k]}
    assert delta=={'BHQ':2,'BHS':1,'WLC':1,'μL':1}
    a['words_exact']=b['words_exact']; assert a==b
report['dictionary_deltas']={'BHQ':2,'BHS':1,'WLC':1,'μL':1}
env2={}
selected(H/'py/author_boj_util/short_id_etc.py',{'short_id'},env2)
selected(H/'py/author_boj_util/noted_by.py',{'_STARTSWITH_N','_STARTSWITH_X','startswith_n','startswith_x'},env2)
tree=ast.parse((H/'py/author_boj_util/get_qr_groups.py').read_text())
names={n.name for n in tree.body if isinstance(n,ast.FunctionDef)}|{'_T30','_FILTER_FNS'}
selected(H/'py/author_boj_util/get_qr_groups.py',names,env2)
records=json.loads((H/'book-of-job/out/enriched-quirkrecs.json').read_text())
groups=collections.defaultdict(list)
for r in records: groups[env2['get_pgroup'](r)].append(r)
selected(H/'py/author_boj/job2_main_article.py',{'PRESENTED_IN_PROSE'},env2)
prose=env2['PRESENTED_IN_PROSE']
assert {env2['short_id'](r):g for g,rs in groups.items() if g in prose.values() for r in rs}==prose
env2['check_every_quirkrec_presented'](groups,set(groups)-set(prose.values()),prose)
report['job_grouping']={'records':len(records),'groups':{g:len(rs) for g,rs in groups.items()},'prose_declarations':prose}
html=(H/'gh-pages/book-of-job/jobn/job2_main_article.html').read_text()
for sid in prose:
    assert f'../jobn-details/{sid}.html' in html
    assert (H/f'gh-pages/book-of-job/jobn-details/{sid}.html').exists()
report['python_syntax_files']=len(list((H/'py').rglob('*.py')))
for p in (H/'py').rglob('*.py'): ast.parse(p.read_text())
foi_html=(H/'gh-pages/MAM-with-doc/foi/foi-unicode.html').read_text()
html_rows=[]
for row in re.findall(r'<tr>(.*?)</tr>',foi_html,re.S):
    cells=re.findall(r'<td[^>]*>(.*?)</td>',row,re.S)
    if len(cells)==2:
        html_rows.append(tuple(html_lib.unescape(re.sub(r'<[^>]*>','',c)).strip() for c in cells))
json_rows=collections.Counter((r['r'],r['bcv_short']) for r in new)
assert not (collections.Counter(html_rows)-json_rows)
assert not (collections.Counter((r['r'],r['bcv_short']) for r in added)-collections.Counter(html_rows))
report['two_cell_html_rows_match_json']=len(html_rows)
report['all_12_new_rows_rendered']=True
(ROOT/'result.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(report,ensure_ascii=False))
