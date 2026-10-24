from pathlib import Path
import json,sys,importlib.util,re
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');A=R/'artifacts/nordic-blue/TASK-016';sys.path.insert(0,str(R/'tools/nordic-blue-regression'));from metrics import compare
spec=importlib.util.spec_from_file_location('contracts',R/'tools/nordic-blue-regression/icon-contracts.py');c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def roots(v):
 if isinstance(v,str):return re.sub(r'(?:http://127\.0\.0\.1:\d+)?/build/(?:theme-acceptance|theme-lab)/(?:classic|nordic)/(?:testing|development|production)/resources/','/CLASSIC-RESOURCES/',v)
 if isinstance(v,list):return [roots(x) for x in v]
 if isinstance(v,dict):return {k:roots(x) for k,x in v.items()}
 return v
rows=[]
for browser in read(A/'browser-availability.json'):
 if browser['status']!='AVAILABLE':continue
 idx=read(A/('native-pages-'+browser['name']+'.json'));assert idx['status']=='PASS' and len(idx['records'])==96
 classic=[r for r in idx['records'] if r['theme']=='classic'];nordic=[r for r in idx['records'] if r['theme']=='nordic']
 identity=lambda r:(r['scope'],r['mode'],r['dpr'],r['state'])
 assert len(classic)==len(nordic)==48 and len({identity(r) for r in classic})==48
 for a in classic:
  b=next(r for r in nordic if identity(a)==identity(r));x,y=read(A/a['path']),read(A/b['path']);y,seen=c.bind_icon_contracts(x,y,a['dpr']);issues=compare(roots(x),roots(y))
  rows.append({'browser':browser['name'],'scope':a['scope'],'mode':a['mode'],'dpr':a['dpr'],'state':a['state'],'elements':x['elementCount'],'mappedObservations':len(seen),'status':'FAIL' if issues else 'PASS','issues':issues})
result={'status':'PASS' if rows and all(x['status']=='PASS' for x in rows) else 'FAIL','pairs':len(rows),'elementComparisons':sum(x['elements'] for x in rows),'policy':'Actual built index.html and microloader/manifest/JS/CSS with a real reload; same-browser/DPR Classic/Nordic comparisons. Lab injects the unchanged fixture only after the compiled entry is ready. Real app uses unchanged application classes/configs and real pointer actions.','results':rows}
(A/'native-page-comparison.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in result.items() if k!='results'}));print(json.dumps([x for x in rows if x['status']=='FAIL'][:15]));assert result['status']=='PASS'
