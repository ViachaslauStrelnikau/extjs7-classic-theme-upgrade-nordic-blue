from pathlib import Path
import json,sys,importlib.util,re,copy
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');A=R/'artifacts/nordic-blue/TASK-021';O=A/'regression';sys.path.insert(0,str(O));from metrics import compare
spec=importlib.util.spec_from_file_location('contracts',O/'icon-contracts.py');c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def roots(v):
 if isinstance(v,str):return re.sub(r'(?:http://127\.0\.0\.1:\d+)?/build/(?:theme-acceptance/(?:classic|nordic|soft)|theme-lab/(?:classic|nordic)|theme-soft)/(?:testing|development|production)/resources/','/CLASSIC-RESOURCES/',v)
 if isinstance(v,list):return [roots(x) for x in v]
 if isinstance(v,dict):return {k:roots(x) for k,x in v.items()}
 return v
def paint(a,b):
 old={e['id']:e for e in a['elements']}
 for x in b['elements']:
  radius=x.get('softRadius')
  if radius and x['id'] in old:
   for prop in ['borderTopLeftRadius','borderTopRightRadius','borderBottomLeftRadius','borderBottomRightRadius']:
    assert x['computed'][prop]==str(radius)+'px',(x['id'],prop,x['computed'][prop],radius)
    x['computed'][prop]=old[x['id']]['computed'][prop]
 return b
idx=read(A/'native-pages-edge.json');assert idx['status']=='PASS' and len(idx['records'])==96
classic=[r for r in idx['records'] if r['theme']=='classic'];soft=[r for r in idx['records'] if r['theme']=='nordic'];identity=lambda r:(r['scope'],r['mode'],r['dpr'],r['state']);rows=[]
for a in classic:
 b=next(r for r in soft if identity(a)==identity(r));x,y=read(A/a['path']),read(A/b['path']);y,seen=c.bind_icon_contracts(x,y,a['dpr']);issues=compare(roots(x),roots(paint(x,y)));rows.append({'scope':a['scope'],'mode':a['mode'],'dpr':a['dpr'],'state':a['state'],'elements':x['elementCount'],'status':'FAIL' if issues else 'PASS','issues':issues,'iconObservations':len(seen)})
result={'status':'PASS' if rows and all(r['status']=='PASS' for r in rows) else 'FAIL','pairs':len(rows),'elementComparisons':sum(r['elements'] for r in rows),'paintException':'Only exact3px control/menu and4px window corner paint; URL mapping follows approved icon contracts. No layout/font/offset tolerances.','results':rows}
(A/'native-page-comparison.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in result.items() if k!='results'}));print(json.dumps([r for r in rows if r['status']=='FAIL'][:8]));assert result['status']=='PASS'
