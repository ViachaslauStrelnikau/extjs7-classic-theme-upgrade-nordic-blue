from pathlib import Path
import json,hashlib,sys,itertools
O=Path(__file__).parent
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
# Reuse only the pure normalization declarations, not the comparison runner.
scope={'__file__':str(O/'compare-geometry.py')};exec((O/'compare-geometry.py').read_text().split('reports=[]')[0],scope)
normalize=scope['normalize']
rows=[];state_checks=[];actions=[]
for dpr in [1,2]:
 index=read(O/f'core-states-v3/dpr-{dpr}/index.json');assert index['status']=='PASS' and len(index['records'])==56
 actions+=index['actions']
 for rec in [r for r in index['records'] if r['theme']=='classic']:
  stem=rec['target']+'--'+rec['state'];a=read(O/f'core-states-v3/dpr-{dpr}/classic/{stem}.json');b=read(O/f'core-states-v3/dpr-{dpr}/nordic/{stem}.json')
  issues=[]
  for key in ['elements','icons','activeElement','scroll','data','stores','duplicates','errors','unownedGraphics','elementCount','visibleElementCount']:
   if normalize(a['metrics'][key])!=normalize(b['metrics'][key]):issues.append(key)
  if a['flags']!=b['flags']:issues.append('actual-state-flags')
  rows.append({'dpr':dpr,'target':rec['target'],'state':rec['state'],'elements':a['metrics']['elementCount'],'status':'PASS' if not issues else 'FAIL','issues':issues})
 for target in ['button.normal','button.menu','button.split','toolbar.first']:
  paints={}
  for state in ['normal','hover','focus','pressed','focus-over','focus-pressed','disabled']:
   row=read(O/f'core-states-v3/dpr-{dpr}/nordic/{target}--{state}.json');els=[x for x in row['metrics']['elements'] if x['id']==target or x['id'].startswith(target+'/')]
   assert els
   root=next(x for x in els if x['id']==target)
   assert root['computed']['backgroundImage']=='none',(target,state,root['computed']['backgroundImage'])
   props=['color','backgroundColor','borderTopColor','outlineStyle','outlineWidth','outlineColor','boxShadow','opacity']
   paints[state]=[{p:e['computed'][p] for p in props} for e in els]
  pairs=list(itertools.combinations(paints,2))
  for left,right in pairs:
   passed=paints[left]!=paints[right]
   state_checks.append({'dpr':dpr,'target':target,'states':[left,right],'paintDistinct':passed})
result={'status':'PASS' if all(r['status']=='PASS' for r in rows) and all(r['paintDistinct'] for r in state_checks) and all(a['passed'] for a in actions) else 'FAIL',
 'pairComparisons':len(rows),'elementComparisons':sum(r['elements'] for r in rows),'paintChecks':state_checks,'actions':actions,'results':rows,
 'policy':'Same existing components/configs. Focus via component focus API, hover and pressed via genuine pointer input, disabled via component API. A pointer-pressed button uses its real x-btn-pressed class (pressed property alone only represents enableToggle buttons). Only color/gradient paint differs; metrics/typography/image offsets/data/focus/state match. Esc tested with focus on a real menu item after opening with mouse.'}
(O/'core-state-comparison.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'status':result['status'],'pairs':len(rows),'elements':result['elementComparisons'],'paintChecks':len(state_checks),'actions':len(actions),'stateFailures':[x for x in state_checks if not x['paintDistinct']],'geometryFailures':[x for x in rows if x['status']!='PASS']}))
if result['status']!='PASS':raise SystemExit(1)
