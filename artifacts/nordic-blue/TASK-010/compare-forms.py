from pathlib import Path
import json
O=Path(__file__).parent
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
scope={'__file__':str(O/'compare-geometry.py')};exec((O/'compare-geometry.py').read_text().split('reports=[]')[0],scope)
normalize=scope['normalize'];rows=[]
for dpr in [1,2]:
 index=read(O/f'form-actions/dpr-{dpr}/index.json');assert index['status']=='PASS'
 for r in index['records']:
  if r['theme']!='classic':continue
  a=read(O/r['path']);b=read(O/r['path'].replace('classic','nordic'));issues=[]
  for key in ['elements','icons','activeElement','scroll','data','stores','duplicates','errors','unownedGraphics','elementCount','visibleElementCount']:
   if normalize(a['metrics'][key])!=normalize(b['metrics'][key]):issues.append(key)
  if a['flags']!=b['flags']:issues.append('state/value/validity')
  rows.append({'dpr':dpr,'action':r['action'],'elements':a['metrics']['elementCount'],'status':'FAIL' if issues else 'PASS','issues':issues})
result={'status':'PASS' if all(r['status']=='PASS' for r in rows) else 'FAIL','pairs':len(rows),'actions':2*len(rows),'elementComparisons':sum(r['elements'] for r in rows),'results':rows,'policy':'Same unchanged fixture, genuine keyboard/mouse input, identical component state/value/validity and exact normalized metrics, fonts, image sizes/offsets, client/scroll. Only reviewed paint colors/gradient layers excluded as in full geometry comparison.'}
(O/'form-action-comparison.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result))
assert result['status']=='PASS'
