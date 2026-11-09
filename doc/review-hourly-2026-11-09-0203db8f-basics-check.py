"""Independent sparse differential checks and extracted-function probes; no repo test run."""
import ast, copy, html, json, re, types
from pathlib import Path
from collections import Counter
from typing import NamedTuple
R=Path(__file__).parent; H=R/'head'; B=R/'base'
OLD=R.parent/'basics-endpoint-be987/head'
report={'base':'be9870504fdfeea07f7358e886200e5215d96a79','head':'0203db8fe6fb816eddc5880bd588c2d6f010a213','outputs':{},'limits':'Sparse output comparison and extracted-function probes with explicit substitutes. Not repository suite, renderer execution, source-corpus survey, browser QA or regeneration.'}
for item in json.loads((R/'compare-full.json').read_text())['files']:
 if item['filename'].endswith('.py'):ast.parse((H/item['filename']).read_text())
report['changed_python_parses']=6
strip=lambda x:' '.join(html.unescape(re.sub('<[^>]*>','',x)).split())
ungray=lambda x:re.sub(r'<span class="foi-gray-sof-pasuq"[^>]*>.*?</span>','',x,flags=re.S)
for stem in ('kq-simple','kq-complex','rare-tmpls','slh-word'):
 p=Path('gh-pages/MAM-with-doc/foi')/('foi-'+stem)
 old=json.loads((B/p.with_suffix('.json')).read_text());new=json.loads((H/p.with_suffix('.json')).read_text())
 assert len(old)==len(new)
 changed=[]
 for a,b in zip(old,new):
  aa={k:v for k,v in a.items() if k!='gsp'};bb={k:v for k,v in b.items() if k!='gsp'}
  if aa!=bb:
   assert stem=='kq-complex' and b['bcv_short']=='2K17:31' and a['r']==b['r']+'\u05c3'
   assert {k:v for k,v in aa.items() if k!='r'}=={k:v for k,v in bb.items() if k!='r'}
  if a!=b:
   assert not a.get('gsp') and b.get('gsp')
   changed.append((b['bcv_short'],b['fp']))
  assert not any('\ue000'<=c<='\uf8ff' for c in json.dumps(b,ensure_ascii=False))
 text=(H/p.with_suffix('.html')).read_text()
 assert not any('\ue000'<=c<='\uf8ff' for c in text)
 html_rows=0;gray_rows=0;gray_spans=0
 for table in re.findall(r'<table\b[^>]*>(.*?)</table>',text,re.S):
  sizes=[]
  for row in re.findall(r'<tr\b[^>]*>(.*?)</tr>',table,re.S):
   cells=re.findall(r'<td\b[^>]*>(.*?)</td>',row,re.S)
   if not cells:continue
   html_rows+=1;sizes.append(len(cells))
   labels=set(re.findall(r'<abbr[^>]*>(GSP|GM)</abbr>',row))
   assert ('GSP' in labels)==('class="foi-gray-sof-pasuq"' in row)
   assert ('GM' in labels)==('class="mam-implicit-maqaf"' in row)
   target=strip(ungray(cells[0]));loc=strip(cells[1])
   if stem=='slh-word':
    target+=' ('+strip(cells[1])+')';loc=strip(cells[2])
   candidates=[r for r in new if ' '.join(r['r'].split())==target and r['bcv_short']==loc]
   assert candidates,(stem,target,loc)
   assert any(bool(r.get('gsp'))==('GSP' in labels) and bool(r.get('gm'))==('GM' in labels) for r in candidates)
   gray_rows+=('GSP' in labels);gray_spans+=row.count('class="foi-gray-sof-pasuq"')
   if stem=='slh-word' and 'GSP' in labels:
    assert '<span class="foi-gray-sof-pasuq" lang="hbo">' in cells[3]
   if stem=='kq-simple' and 'GSP' in labels and any('pqere' in r for r in candidates):
    assert any(r.get('pqere')==strip(ungray(cells[2])) for r in candidates)
  assert len(set(sizes))<=1
 report['outputs'][stem]={'rows':len(new),'new_gsp':len(changed),'gsp_rows':sum(bool(r.get('gsp')) for r in new),'html_rows':html_rows,'html_gsp_rows':gray_rows,'html_gsp_spans':gray_spans,'new_gsp_by_feature':dict(Counter(fp for _,fp in changed)),'changed_rows':changed}
 if stem=='kq-complex':
  before=[x for x in old if x['fp']=='k1q1-qk-sp'];after=[x for x in new if x['fp']=='k1q1-qk-sp']
  assert len(before)==7 and before==after and all(x['r'].endswith('\u05c3') for x in after)
assert [report['outputs'][s]['new_gsp'] for s in ('kq-simple','kq-complex','rare-tmpls','slh-word')]==[82,1,4,9]
def defs(path,env=None,names=None,root=H):
 env={} if env is None else env
 t=ast.parse((root/path).read_text())
 t.body=[n for n in t.body if not isinstance(n,(ast.Import,ast.ImportFrom)) and (names is None or isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in names)]
 exec(compile(t,path,'exec'),env);return types.SimpleNamespace(**env)
def el(tag,c,a=None):return {'_htel_tag':tag,'contents':(c,) if isinstance(c,str) else c or (), 'attr':a or {}}
mb=types.SimpleNamespace(span=lambda c,a:el('span',c,a),abbr=lambda c,a:el('abbr',c,a),table_datum=lambda c:el('td',c),is_htel=lambda x:isinstance(x,dict) and '_htel_tag' in x)
hpu=types.SimpleNamespace(SOPA='\u05c3',MAQ='\u05be',PASOLEG='\u05c0',GERSHAYIM='\u05f4')
gray=defs('py/foi/foi_gray_marks.py',{'NamedTuple':NamedTuple,'hpu':hpu,'mb_html':mb})
finals=defs('py/foi/foi_finals.py',{'gray_marks':gray},['_rm_html','_rm_html_single','_json_value','_row_dic_for_json','_slash_str_from_path_parts'])
fct=defs('py/foi/foi_struct.py')
kq=defs('py/foi/foiz_wt_kq_1.py',{'fct':fct,'gray_marks':gray},['_with_gray_sof_pasuq','_with_gray_sof_pasuq_after'])
gsp=gray.gray_sof_pasuq();gm=gray.target('a\ue001b')
assert gray.gray_sof_pasuq('hbo')['attr']['lang']=='hbo' and 'lang' not in gsp['attr']
assert finals._json_value(('abc',gsp))=='abc' and finals._json_value(gm)== 'a\u05beb'
markup=(el('span','abc',{'class':'special'}),)
assert finals._json_value((*markup,gsp))==markup
assert finals._json_value(markup)==markup
assert finals._json_value((*markup,gm[1],gsp))==(*markup,gm[1])
for qual in ({},{'kind':'x'},{'pqere':'abc','kind':'x'}):
 qt=fct.make_qtarget(('rendered',),qual);snapshot=copy.deepcopy(qt)
 got=kq._with_gray_sof_pasuq(qt)
 assert qt==snapshot and gray.labels(fct.qtar_proper(got))==('GSP',)
 jr=finals._row_dic_for_json(('kq-simple','x'),'X1:1',fct.qtar_qual(got),fct.qtar_proper(got))
 assert jr=={'bcv_short':'X1:1',**qual,'fp':'x','r':'rendered','gsp':True}
assert finals._rm_html(kq._with_gray_sof_pasuq(('abc',)))=='abc'
slh=defs('py/foi/foiz_wt_slh_word.py',{'gray_marks':gray,'_html_for_wtseq':lambda x:markup},['_html_in_context'])
tmpl={};assert slh._html_in_context(set(),tmpl)==markup
with_gsp=slh._html_in_context({id(tmpl)},tmpl)
assert with_gsp[-1]['attr']['lang']=='hbo' and finals._json_value(with_gsp)==markup
# Execute the exact complex feature function with its real declarative dispatch table.
t=ast.parse((H/'py/foi/foiz_wt_kq_2.py').read_text());env={'hpu':hpu,'gray_marks':gray,'sd':types.SimpleNamespace(NBSP='\u00a0',DOUB_VERT_LINE='\u2016')}
t.body=[n for n in t.body if isinstance(n,ast.FunctionDef) and n.name=='_feature' or isinstance(n,ast.Assign) and any(isinstance(a,ast.Name) and a.id in ('_KQ0','_FEATURES','_RUNS_ENDING_IN_A_GRAY_SOF_PASUQ') for a in n.targets)]
exec(compile(t,'complex-feature','exec'),env)
for run,feature in env['_FEATURES'].items():
 verse=['a' if x not in (' ',hpu.SOPA,'paseq') else '\u00a0\u2016 ' if x=='paseq' else x for x in run]
 got=env['_feature'](verse,(0,run))
 if feature is None:assert got==[]
 elif run in env['_RUNS_ENDING_IN_A_GRAY_SOF_PASUQ']:
  assert gray.labels(got[0][1])==('GSP',) and finals._rm_html(got[0][1])==''.join(verse[:-1])
 else:assert got==[(feature,''.join(verse).lstrip('\u00a0'))]
wtnp=defs('py/mb_cmn/ws_tmpl_named_params.py',{},['simplify_singleton'])
wtp=defs('py/mb_cmn/ws_tmpl2.py',{'hpu':hpu,'wtnp':wtnp,'dv_map':lambda f,d:{k:f(v) for k,v in d.items()}})
def intersperse(sep,seq):
 out=[]
 for x in seq:
  if out:out.append(sep)
  out.append(x)
 return out
rare=defs('py/foi/foiz_wt_rare_tmpls.py',{'wtp':wtp,'gray_marks':gray,'_html_for_wtseq':lambda x,column:tuple(x),'_FP_RT_NA_NOTE':('rare-tmpls','na-note'),'intersperse':intersperse,'sum_of_tuples':lambda x:sum(x,()),'fwh':types.SimpleNamespace(label_args_of_scrdfftar=lambda *a:[])},['_record_scrdff_in_col_x'])
note={'tmpl_name':'note','tmpl_params':{'1':'target','2':'body','3':'star'}}
snapshot=copy.deepcopy(note)
for column in ('C','E'):
 plain=rare._record_scrdff_in_col_x(column,set(),{},(),note)[0][1]
 marked=rare._record_scrdff_in_col_x(column,{id(note)},{},(),note)[0][1]
 assert plain==('target',' / ','body',' / ','star')
 assert marked[0]=='target' and gray.is_gray_mark(marked[1]) and marked[2:]==plain[1:]
 assert finals._rm_html(plain)==finals._rm_html(marked)
assert note==snapshot
report['extracted_function_probes']='passed: qualifier preservation and GSP omission, GM retention, simple/qualified/trivial kq and nonmutation, slh context/lang, all 14 complex dispatch signatures, rare-template target-only mark in columns C and E without input mutation'
report['complex_dispatch_signatures']=len(env['_FEATURES'])
(R/'result.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({**report,'outputs':{k:{a:b for a,b in v.items() if a!='changed_rows'} for k,v in report['outputs'].items()}},indent=2))
