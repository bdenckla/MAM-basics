import ast, json, re, html, types
from pathlib import Path
from collections import Counter
from typing import NamedTuple
R=Path(__file__).parent
H=R/'head'; B=R/'base'
report={'scope':'Independent sparse scratch checks; not repository tests or generator execution','base':'653b84198a6ea646c83b7b249370722e6fe2cf38','head':'ea19ea15dafde6843a9880931558ccdb9c1b7907'}
report['syntax_files']=[]
for p in (H/'py').rglob('*.py'):
 ast.parse(p.read_text());report['syntax_files'].append(str(p.relative_to(H)))
report['outputs']={}
for stem in ('foi-unicode','foi-alef-dual-ml-alef-second'):
 path=Path('gh-pages/MAM-with-doc/foi')/stem
 old=json.loads((B/path.with_suffix('.json')).read_text());new=json.loads((H/path.with_suffix('.json')).read_text())
 assert len(old)==len(new)
 counts=Counter()
 for a,b in zip(old,new):
  assert {k:v for k,v in a.items() if k!='r'}=={k:v for k,v in b.items() if k not in ('r','gsp','gm')}
  assert not any('\ue000'<=c<='\uf8ff' for c in b['r'])
  if b.get('gsp'): assert b['r'].endswith('\u05c3');counts['gsp']+=1
  if b.get('gm'): assert '\u05be' in b['r'];counts['gm']+=1
  if a['r']!=b['r']:
   counts['changed_form']+=1
   if b.get('gm'): counts['gray_maqaf_form']+=1
   else:
    assert b['r'] in (a['r']+'\u05c0',a['r']+'\u05c3'),(a,b)
    counts['appended_'+hex(ord(b['r'][-1]))]+=1
 text=(H/path.with_suffix('.html')).read_text()
 assert '\ue000' not in text and '\ue001' not in text
 html_rows=0;gray_rows=Counter();tables_with_gray=0
 for table in re.findall(r'<table\b[^>]*>(.*?)</table>',text,re.S):
  rows=re.findall(r'<tr\b[^>]*>(.*?)</tr>',table,re.S)
  table_labels=set(re.findall(r'<abbr[^>]*>(GSP|GM)</abbr>',table))
  if table_labels: tables_with_gray+=1
  sizes=[]
  for row in rows:
   cells=re.findall(r'<td\b[^>]*>(.*?)</td>',row,re.S)
   if not cells: continue
   sizes.append(len(cells));html_rows+=1
   strip=lambda x:html.unescape(re.sub('<[^>]*>','',x)).strip()
   target=strip(cells[0]);loc=strip(cells[1])
   labels=set(re.findall(r'<abbr[^>]*>(GSP|GM)</abbr>',row))
   spans=set(re.findall(r'<span class="(foi-gray-sof-pasuq|mam-implicit-maqaf)"',cells[0]))
   assert ('GSP' in labels)==('foi-gray-sof-pasuq' in spans)
   assert ('GM' in labels)==('mam-implicit-maqaf' in spans)
   candidates=[r for r in new if r['r']==target and r['bcv_short']==loc]
   assert candidates,(target,loc)
   assert any(bool(r.get('gsp'))==('GSP' in labels) and bool(r.get('gm'))==('GM' in labels) for r in candidates)
   gray_rows.update(labels)
  assert len(set(sizes))<=1,sizes
 report['outputs'][stem]={'rows':len(new),'delta':dict(counts),'html_rows_checked':html_rows,'html_gray_rows':dict(gray_rows),'tables_with_gray_columns':tables_with_gray}
for path in ('py/mb_misc/styles_mam_with_doc.css','gh-pages/MAM-with-doc/two_col_style.css'):
 text=(H/path).read_text();assert 'span.foi-gray-sof-pasuq { color: gray; }' in text
 assert text.replace('/* A sof pasuq that a FOI page adds for context: py/foi/foi_gray_marks.py. */\nspan.foi-gray-sof-pasuq { color: gray; }\n','')==(B/path).read_text()
report['css_only_expected_addition']=True
# Execute exact gray helper definitions with an explicit small HTML-constructor stand-in.
# This is a scratch contract probe, NOT the real rendering pipeline.
def el(tag,contents,attrs=None):return {'tag':tag,'contents':(contents,) if isinstance(contents,str) else (contents or ()), 'attr':attrs or {}}
mb=types.SimpleNamespace(span=lambda c,a:el('span',c,a),abbr=lambda c,a:el('abbr',c,a),table_datum=lambda c:el('td',c),is_htel=lambda x:isinstance(x,dict))
env={'NamedTuple':NamedTuple,'hpu':types.SimpleNamespace(SOPA='\u05c3',MAQ='\u05be'),'mb_html':mb}
tree=ast.parse((H/'py/foi/foi_gray_marks.py').read_text());tree.body=[n for n in tree.body if not isinstance(n,(ast.Import,ast.ImportFrom))];exec(compile(tree,'gray-scratch','exec'),env)
for raw,labs in [('אב',()),('אב\ue000',('GSP',)),('אב\ue001גד',('GM',)),('אב\ue001גד\ue000',('GSP','GM'))]:
 target=env['target'](raw);assert env['labels'](target)==labs
 assert env['json_flags'](target)=={l.lower():True for l in labs}
 assert '\ue000' not in env['text'](raw) and '\ue001' not in env['text'](raw)
assert env['labels_of_table']([('GM',),('GSP',)])==('GSP','GM')
assert env['labels_of_table']([])==()
assert len(env['cells']((),('GSP','GM')))==2
report['gray_helper_scratch_probes']='passed with explicit HTML constructor stand-in; 4 forms plus column ordering/empty-cell checks'
(R/'result.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
