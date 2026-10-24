from pathlib import Path
import json,copy,importlib.util,html
from metrics import compare
O=Path(__file__).parent;R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue')
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
spec=importlib.util.spec_from_file_location('contracts',O/'icon-contracts.py');contracts=importlib.util.module_from_spec(spec);spec.loader.exec_module(contracts)
rows=[];observations=[];controls=[]
def pair(a,b,dpr,scope,name):
 bound,seen=contracts.bind_icon_contracts(a,b,dpr);issues=compare(a,bound)
 observations.extend([{'scope':scope,'name':name,'dpr':dpr,**s} for s in seen])
 rows.append({'scope':scope,'name':name,'dpr':dpr,'elements':a['elementCount'],'icons':len(a['icons']),'issues':issues,'status':'FAIL' if issues else 'PASS'})
for dpr in [1,2]:
 base=R/f'artifacts/nordic-blue/TASK-006/captures/pass-1/dpr-{dpr}';folder=O/f'nordic/captures/pass-1/dpr-{dpr}'
 index=read(folder/'index.json');expected=read(base/'index.json')
 assert index['scenarioCount']==expected['scenarioCount']==102
 assert [(r['case'],r['state']) for r in index['records']]==[(r['case'],r['state']) for r in expected['records']]
 for row in index['records']:
  a,b=read(base/row['metrics']),read(folder/row['metrics'])
  assert b['environment']['profile']['theme']=='nordic' and not b['network']['errors'] and not b['network']['badResponses']
  pair(a,b,dpr,'coverage',row['case']+'/'+row['state'])
 for scope,count in [('form-actions',48),('grid-actions',46),('secondary-actions',58),('core-states-v3',56),('window-actions',28)]:
  idx=read(O/f'{scope}/dpr-{dpr}/index.json');assert idx['status']=='PASS' and len(idx['records'])==count
  classics=[r for r in idx['records'] if r['theme']=='classic'];nordics=[r for r in idx['records'] if r['theme']=='nordic'];assert len(classics)==len(nordics)==count//2
  identity=lambda r:(r.get('action'),r.get('target'),r.get('state'))
  assert len({identity(r) for r in classics})==count//2
  assert [identity(r) for r in classics]==[identity(r) for r in nordics]
  for rec,nrec in zip(classics,nordics):
   a,b=read(O/rec['path']),read(O/nrec['path']);assert a['flags']==b['flags']
   for doc in [a,b]:assert not doc['errors'] and not doc['bad']
   pair(a['metrics'],b['metrics'],dpr,scope,rec.get('action',rec.get('target','')+'/'+rec.get('state','')))
  if scope=='core-states-v3':assert len(idx['actions'])==10 and all(r['passed'] for r in idx['actions'])
 neg=O/f'negative-controls/dpr-{dpr}';a=read(neg/'before.json')
 for kind in ['shift-1px','font-size']:
  issues=compare(a,read(neg/(kind+'.json')));restored=compare(a,read(neg/(kind+'-restored.json')))
  controls.append({'dpr':dpr,'control':kind,'rejected':bool(issues),'restoredPass':not restored,'issues':issues});assert issues and not restored
 for kind in ['missing-element','wrong-count','wrong-state','duplicate-id','empty-elements']:
  b=copy.deepcopy(a)
  if kind=='missing-element':b['elements'].pop();b['elementCount']-=1
  if kind=='wrong-count':b['elementCount']+=1
  if kind=='wrong-state':b['state']='wrong'
  if kind=='duplicate-id':b['elements'][1]['id']=b['elements'][0]['id']
  if kind=='empty-elements':b['elements']=[];b['elementCount']=0
  issues=compare(a,b);assert issues;controls.append({'dpr':dpr,'control':kind,'rejected':True,'issues':issues})
adapter=read(O/'adapter-validation.json');assert adapter['status']=='PASS' and len(adapter['rows'])==12
assert observations
status='PASS' if all(r['status']=='PASS' for r in rows) else 'FAIL'
result={'status':status,'coveragePairs':sum(r['scope']=='coverage' for r in rows),'actionAndStatePairs':sum(r['scope']!='coverage' for r in rows),'coreAdditionalActions':20,'elementComparisons':sum(r['elements'] for r in rows),'iconComparisons':sum(r['icons'] for r in rows),'imageContractObservations':len(observations),'negativeControls':controls,'adapterChecks':12,'results':rows}
(O/'regression-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
(O/'icon-contract-observations.json').write_text(json.dumps({'status':status,'observations':observations}),encoding='utf-8')
summary={k:v for k,v in result.items() if k not in ['results','negativeControls']};print(json.dumps(summary))
table=''.join('<tr><td>'+str(r['dpr'])+'</td><td>'+html.escape(r['scope'])+'</td><td>'+html.escape(r['name'])+'</td><td>'+r['status']+'</td><td>'+html.escape(', '.join(r['issues']))+'</td></tr>' for r in rows)
(O/'review.html').write_text('<!doctype html><meta charset="utf-8"><title>TASK-014 regression</title><style>body{font:14px Arial;background:#f4f7fd;color:#273d5c;margin:24px}td,th{padding:6px;border:1px solid #afc5df}table{border-collapse:collapse}pre{white-space:pre-wrap}</style><h1>TASK-014: '+status+'</h1><p>Exact metrics within DPR; approved image mapping only. Paint differences are intentional. This is not final visual or release acceptance.</p><pre>'+html.escape(json.dumps(summary,indent=2))+'</pre><p>Negative controls: '+str(len(controls))+' rejected; real shift/font controls restored successfully.</p><table><tr><th>DPR<th>Scope<th>Case/action<th>Status<th>Issues</tr>'+table+'</table>',encoding='utf-8')
assert status=='PASS'
