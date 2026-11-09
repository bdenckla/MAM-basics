"""Sparse endpoint checks, not repository tests or generator replay."""
import ast,json,re,html,types,copy
from pathlib import Path
from collections import Counter
from dataclasses import dataclass
from typing import NamedTuple
from collections.abc import Iterator
R=Path(__file__).parent;H=R/'head';B=R/'base'
report={'base':'ea19ea15dafde6843a9880931558ccdb9c1b7907','head':'be9870504fdfeea07f7358e886200e5215d96a79','scope':'Sparse independent endpoint and extracted-function probes, not repository suite or regeneration','outputs':{}}
changed=json.loads((R/'compare.json').read_text())['files']
for f in changed:
 if f['filename'].endswith('.py'):ast.parse((H/f['filename']).read_text())
report['changed_python_parses']=6
for stem in ('foi-unicode','foi-alef-dual-ml-alef-second','foi-kq-simple','foi-qamats-variants'):
 p=Path('gh-pages/MAM-with-doc/foi')/stem
 old=json.loads((B/p.with_suffix('.json')).read_text());new=json.loads((H/p.with_suffix('.json')).read_text())
 assert len(old)==len(new)
 counts=Counter()
 for a,b in zip(old,new):
  aa={k:v for k,v in a.items() if k!='gsp'};bb={k:v for k,v in b.items() if k!='gsp'}
  if aa!=bb:
   assert stem=='foi-kq-simple' and a['bcv_short']=='Ps10:5'
   assert b['pqere']==a['pqere']+'\u05c0'
   assert {k:v for k,v in aa.items() if k!='pqere'}=={k:v for k,v in bb.items() if k!='pqere'}
   counts['legarmeh_added_pqere']+=1
  if a.get('gsp')!=b.get('gsp'):counts['gsp_added' if b.get('gsp') else 'gsp_removed']+=1
  assert not any('\ue000'<=c<='\uf8ff' for c in json.dumps(b,ensure_ascii=False))
 text=(H/p.with_suffix('.html')).read_text();assert '\ue000' not in text and '\ue001' not in text
 html_rows=0;gray_rows=Counter();gray_tables=0
 strip=lambda x:' '.join(html.unescape(re.sub('<[^>]*>','',x)).split())
 ungray=lambda x:re.sub(r'<span class="foi-gray-sof-pasuq">.*?</span>','',x,flags=re.S)
 for table in re.findall(r'<table\b[^>]*>(.*?)</table>',text,re.S):
  sizes=[];labels_in_table=set(re.findall(r'<abbr[^>]*>(GSP|GM)</abbr>',table));gray_tables+=bool(labels_in_table)
  for row in re.findall(r'<tr\b[^>]*>(.*?)</tr>',table,re.S):
   cells=re.findall(r'<td\b[^>]*>(.*?)</td>',row,re.S)
   if not cells:continue
   sizes.append(len(cells));html_rows+=1
   labels=set(re.findall(r'<abbr[^>]*>(GSP|GM)</abbr>',row))
   assert ('GSP' in labels)==('class="foi-gray-sof-pasuq"' in row)
   assert ('GM' in labels)==('class="mam-implicit-maqaf"' in row)
   target=strip(ungray(cells[0]));loc=strip(cells[1])
   candidates=[r for r in new if ' '.join(r['r'].split())==target and r['bcv_short']==loc]
   assert candidates,(stem,target,loc)
   assert any(bool(r.get('gsp'))==('GSP' in labels) and bool(r.get('gm'))==('GM' in labels) for r in candidates)
   if stem=='foi-kq-simple' and 'GSP' in labels: assert any(r.get('pqere')==strip(ungray(cells[2])) for r in candidates)
   gray_rows.update(labels)
  assert len(set(sizes))<=1
 report['outputs'][stem]={'rows':len(new),'delta':dict(counts),'html_rows':html_rows,'html_gray_rows':dict(gray_rows),'gray_tables':gray_tables}
# Exact AST definitions run with explicit lightweight dependencies. No sys.path modification.
def defs(path,env=None,names=None):
 env=env or {};t=ast.parse((H/path).read_text())
 t.body=[n for n in t.body if not isinstance(n,(ast.Import,ast.ImportFrom)) and (names is None or isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in names)]
 exec(compile(t,path,'exec'),env);return types.SimpleNamespace(**env)
def el(tag,c,a=None):return {'_htel_tag':tag,'contents':(c,) if isinstance(c,str) else c or (), 'attr':a or {}}
mb=types.SimpleNamespace(span=lambda c,a:el('span',c,a),abbr=lambda c,a:el('abbr',c,a),table_datum=lambda c:el('td',c),is_htel=lambda x:isinstance(x,dict) and '_htel_tag' in x)
hpu=types.SimpleNamespace(SOPA='\u05c3',MAQ='\u05be',PASOLEG='\u05c0',GERSHAYIM='\u05f4')
gray=defs('py/foi/foi_gray_marks.py',{'NamedTuple':NamedTuple,'hpu':hpu,'mb_html':mb})
finals=defs('py/foi/foi_finals.py',{'gray_marks':gray},['_rm_html','_rm_html_single','_json_value','_row_dic_for_json','_slash_str_from_path_parts'])
gsp=gray.gray_sof_pasuq();gm=gray.target('אב\ue001גד');target=('אב',gsp)
assert gray.labels(target,gm)==('GSP','GM')
assert gray.json_flags(target,gm)=={'gsp':True,'gm':True}
assert finals._rm_html(target)=='אב' and finals._rm_html(gm)=='אב־גד'
assert finals._row_dic_for_json(('kq-simple','x'),'Ps1:1',{'pqere':target},('אב',))=={'bcv_short':'Ps1:1','pqere':'אב','fp':'x','r':'אב','gsp':True}
assert gray.labels_of_table([])==() and gray.labels_of_table([('GM',),('GSP',)])==('GSP','GM')
assert len(gray.cells((),('GSP','GM')))==2
# Actual template accessors and constant/validation declarations.
tmpln=defs('py/mb_cmn/template_names.py')
wtnp=defs('py/mb_cmn/ws_tmpl_named_params.py',{},['simplify_singleton'])
wtp=defs('py/mb_cmn/ws_tmpl2.py',{'hpu':hpu,'wtnp':wtnp,'dv_map':lambda f,d:{k:f(v) for k,v in d.items()}})
fwh=defs('py/foi/foi_wikitext_helpers.py',{'re':re,'hpu':hpu,'wtp':wtp,'wtnp':wtnp,'tmpln':tmpln,'gray_marks':gray})
def tmpl(name,**params):return {'tmpl_name':name,'tmpl_params':params} if params else {'tmpl_name':name}
q=tmpl(tmpln.QAMATS_VARIANT,**{'ד':'אב','ס':'אב'});note=tmpl('נוסח',**{'1':q,'2':'note'})
source=[note,'׃'];snapshot=copy.deepcopy(source)
assert fwh.templates_before_sof_pasuq(source)=={id(note),id(q)}
assert fwh.templates_before_sof_pasuq([q,'־אב'])==set()
assert fwh.templates_before_sof_pasuq([q,' ׃'])==set()
assert fwh.templates_before_sof_pasuq([q,'׃'])=={id(q)}
for mark in ['׃','־']:
 result=fwh.with_attached_marks([q,mark]);assert result[0]['tmpl_params']=={'ד':'אב'+mark,'ס':'אב'+mark}
assert source==snapshot
assert fwh.templates_before_sof_pasuq([tmpl(tmpln.SILLUQ_BEFORE_METEG,**{'1':'אב','2':'1'}),'׃'])==set()
try:fwh.templates_before_sof_pasuq([tmpl('unknown'),'׃']);raise AssertionError('unknown did not raise')
except ValueError:pass
# Changed qamats display gate, preserving JSON of both variants.
qv=defs('py/foi/foiz_wt_qamats_var.py',{'gray_marks':gray},['_dalsam_htseq','_disputed_part_ends_both'])
empty={'dsa-undisputed-suffix':[],'dsa-dal-endpunc':[],'dsa-sam-endpunc':[]}
assert qv._disputed_part_ends_both(empty)
for key in empty:assert not qv._disputed_part_ends_both({**empty,key:['x']})
assert finals._rm_html(qv._dalsam_htseq(('אב','גד'),True))==finals._rm_html(qv._dalsam_htseq(('אב','גד'),False))=='ד=אב ס=גד'
fct=defs('py/foi/foi_struct.py')
kq=defs('py/foi/foiz_wt_kq_1.py',{'fct':fct,'gray_marks':gray},['_with_gray_sof_pasuq'])
qt=fct.make_qtarget(('unchanged',),{'pqere':'אב'});got=kq._with_gray_sof_pasuq(qt)
assert qt==fct.make_qtarget(('unchanged',),{'pqere':'אב'}) and fct.qtar_proper(got)==('unchanged',)
assert finals._json_value(fct.qtar_qual(got)['pqere'])=='אב'
qp=defs('py/hkq_cmn/qere_projection.py',{'dataclass':dataclass,'re':re,'Iterator':Iterator,'MAQ':'־','PASOLEG':'׀','template_names':tmpln,'canonical_template_name':lambda s:s.replace('"','״')})
for policy in [qp.HOLAM_HE_MAIN_COMPATIBLE_POLICY,qp.XATAF_QAMATS_POLICY,qp.FOI_KQ_SIMPLE_MAIN_COMPATIBLE_POLICY]:
 p=qp.project_qere_atoms([tmpl('מ:פסק'),tmpl('מ:לגרמיה-2'),tmpl('מ:מקף אפור')],source=None,policy=policy)
 assert [x['text'] for x in p]==([' ','׀','־'] if policy==qp.FOI_KQ_SIMPLE_MAIN_COMPATIBLE_POLICY else ['׀','׀','־'])
report['function_probes']='passed: gray labels and JSON omission, qualifiers, template identity and nesting, literal punctuation attachment, unchanged input, closed unknown-template failure, silluq-before-meteg None, qamats eligibility, kq pqere, three projection policies; explicit HTML constructor substitutes'
(R/'result.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
