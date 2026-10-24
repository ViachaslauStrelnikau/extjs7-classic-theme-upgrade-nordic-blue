from pathlib import Path
import json,importlib.util
O=Path(__file__).parent;read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
scope={'__file__':str(O/'compare-geometry.py')};exec((O/'compare-geometry.py').read_text().split('from importlib.util')[0],scope);normalize=scope['normalize']
spec=importlib.util.spec_from_file_location('contracts',O/'icon-contracts.py');contracts=importlib.util.module_from_spec(spec);spec.loader.exec_module(contracts)
rows=[];observations=[]
for folder,expected in [('form-actions',48),('grid-actions',46),('secondary-actions',58)]:
 for dpr in [1,2]:
  index=read(O/f'{folder}/dpr-{dpr}/index.json');assert index['status']=='PASS' and len(index['records'])==expected
  for rec in index['records']:
   if rec['theme']!='classic':continue
   a=read(O/rec['path']);b=read(O/rec['path'].replace('classic','nordic'));metrics,seen=contracts.bind_icon_contracts(a['metrics'],b['metrics'],dpr);issues=[]
   for key in ['elements','icons','activeElement','scroll','data','stores','duplicates','errors','unownedGraphics','elementCount','visibleElementCount']:
    if normalize(a['metrics'][key])!=normalize(metrics[key]):issues.append(key)
   if a['flags']!=b['flags']:issues.append('actual-state/value')
   observations+=seen;rows.append({'folder':folder,'dpr':dpr,'action':rec['action'],'elements':a['metrics']['elementCount'],'status':'FAIL' if issues else 'PASS','issues':issues})
result={'status':'PASS' if all(r['status']=='PASS' for r in rows) else 'FAIL','pairs':len(rows),'actionExecutions':len(rows)*2,'elementComparisons':sum(r['elements'] for r in rows),'mappedImageObservations':len(observations),'policy':'Reused TASK-010–012 genuine interaction drivers on identical fixture with approved runtime icons; only exact approved image/density/adapter contracts are mapped before strict non-paint geometry/state/data comparison.','results':rows}
(O/'native-action-comparison.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in result.items() if k!='results'}));assert result['status']=='PASS'
