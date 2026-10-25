from pathlib import Path
import json,importlib.util,sys
from metrics import compare
O=Path(__file__).parent;read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
spec=importlib.util.spec_from_file_location('contracts',O/'icon-contracts.py');c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
rows=[]
def pair(a,b,d,scope,identity):
 b,seen=c.bind_icon_contracts(a,b,d)
 old={x['id']:x for x in a['elements']}
 for x in b['elements']:
  radius=x.get('softRadius')
  if radius and x['id'] in old:
   for prop in ['borderTopLeftRadius','borderTopRightRadius','borderBottomLeftRadius','borderBottomRightRadius']:
    assert x['computed'][prop]==str(radius)+'px',(x['id'],prop,x['computed'][prop],radius)
    x['computed'][prop]=old[x['id']]['computed'][prop]
 issues=compare(a,b)
 rows.append({'dpr':d,'scope':scope,'identity':identity,'elements':a['elementCount'],'icons':len(a['icons']),'mappedObservations':len(seen),'issues':issues,'status':'FAIL' if issues else 'PASS'})
for d in [1,2]:
 folder=O/f'classic/captures/pass-1/dpr-{d}';other=O/f'nordic/captures/pass-1/dpr-{d}';a,b=read(folder/'index.json'),read(other/'index.json')
 assert len(a['records'])==len(b['records'])==102
 assert [(r['case'],r['state']) for r in a['records']]==[(r['case'],r['state']) for r in b['records']]
 for r in a['records']:
  x,y=read(folder/r['metrics']),read(other/r['metrics']);assert not x['network']['errors'] and not x['network']['badResponses'] and not y['network']['errors'] and not y['network']['badResponses']
  pair(x,y,d,'coverage',r['case']+'/'+r['state'])
 for group,count in [('form-actions',48),('grid-actions',46),('secondary-actions',58),('core-states-v3',56),('window-actions',28)]:
  index=read(O/f'{group}/dpr-{d}/index.json');assert index['status']=='PASS' and len(index['records'])==count
  a=[r for r in index['records'] if r['theme']=='classic'];b=[r for r in index['records'] if r['theme']=='nordic'];assert len(a)==len(b)==count//2
  identity=lambda r:(r.get('action'),r.get('target'),r.get('state'))
  assert len(set(map(identity,a)))==len(a) and list(map(identity,a))==list(map(identity,b))
  for x,y in zip(a,b):
   x,y=read(O/x['path']),read(O/y['path']);assert x['flags']==y['flags'] and not x['errors'] and not x['bad'] and not y['errors'] and not y['bad']
   pair(x['metrics'],y['metrics'],d,group,x.get('action',x.get('target','')+'/'+x.get('state','')))
  if group=='core-states-v3':assert len(index['actions'])==10 and all(x['passed'] for x in index['actions'])
result={'status':'PASS' if all(x['status']=='PASS' for x in rows) else 'FAIL','paintException':'Only declared3px control/menu and4px window corners, checked against actual selector ownership and exact compiled values. All other metric/state/offset/font checks unchanged.', 'baselinePolicy':'Fresh Classic/Nordic within the same actual browser and DPR; no cross-browser coordinate/font equivalence claim. Original Edge TASK-006 is immutable. Missing/count/state/duplicate checks remain exact.','browser':read(O/'browser-config.json'),'coveragePairs':204,'actionStatePairs':236,'additionalCoreFlows':20,'elementComparisons':sum(x['elements'] for x in rows),'results':rows}
(O/'browser-results.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in result.items() if k not in ['results','browser']}))
if result['status']!='PASS':
 print(json.dumps([x for x in rows if x['status']=='FAIL'][:10]));raise SystemExit(1)
