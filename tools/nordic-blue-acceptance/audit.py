from pathlib import Path
import hashlib,json,sys,importlib.util,re
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');A=R/'artifacts/nordic-blue/TASK-016'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
protected=read(A/'protected-before.json'); changed=[k for k,v in protected.items() if sha(R/k)!=v];assert not changed,changed
icons=read(R/'config/nordic-blue-icons.json')['runtimeImages']; assets=[]
for scope in ['theme-lab','theme-acceptance']:
 for mode in ['testing','development','production']:
  base=R/'TestApp/build'/scope/'nordic'/mode/'resources'
  bad=[k for k,v in icons.items() if not (base/k).is_file() or sha(base/k)!=v['sha256']]
  assert not bad,(scope,mode,bad)
  assets.append({'scope':scope,'mode':mode,'assets':len(icons),'status':'PASS'})
sys.path.insert(0,str(R/'tools/nordic-blue-regression'));from metrics import compare
spec=importlib.util.spec_from_file_location('contracts',R/'tools/nordic-blue-regression/icon-contracts.py');c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
rows=[]
for folder in sorted((A/'build-modes').iterdir()):
 idx=read(folder/'index.json');assert idx['status']=='PASS'
 baseline=read(R/f"artifacts/nordic-blue/TASK-006/captures/pass-1/dpr-{idx['dpr']}/all--normal.json")
 for reload in [0,1]:
  snap=read(folder/f'native-{reload}.json');mapped,seen=c.bind_icon_contracts(baseline,snap,idx['density']);issues=compare(baseline,mapped)
  rows.append({'label':folder.name,'reload':reload,'status':'FAIL' if issues else 'PASS','issues':issues,'elements':baseline['elementCount'],'iconObservations':len(seen)})
warnings=[]
original=set(re.findall(r'\[WRN\] (.*)',(A/'original-app-testing.log').read_text(encoding='utf-8-sig')))
for command in read(A/'build-commands.json')+read(A/'development-output-commands.json'):
 text=(A/(command['label']+'.log')).read_text(encoding='utf-8-sig');found=set(re.findall(r'\[WRN\] (.*)',text));assert command['exitCode']==0 and '[ERR]' not in text
 assert found.issubset(original),(command['label'],found-original)
 warnings.append({'label':command['label'],'uniqueWarnings':sorted(found),'newWarningsComparedWithOriginal':[]})
flags=[]
for browser in ['edge','chromium','firefox']:
 for scope in ['lab','real']:
  for mode in ['testing','development','production']:
   for dpr in [1,2]:
    base=A/f'native-pages/{browser}/{scope}/{mode}/dpr-{dpr}'
    classic,nordic=[read(base/theme/'manifest.json') for theme in ['classic','nordic']]
    assert classic['flags']==nordic['flags'] and classic['toolkit']==nordic['toolkit']=='classic'
    assert nordic['packages']['theme-nordic-blue']['extend']=='theme-classic'
    for key,value in classic['packages'].items():assert nordic['packages'][key]==value,(browser,scope,mode,key)
    assert set(nordic['packages'])-set(classic['packages'])=={'theme-nordic-blue'}
    flags.append({'browser':browser,'scope':scope,'mode':mode,'dpr':dpr,'status':'PASS','flags':classic['flags']})
result={'status':'PASS' if all(r['status']=='PASS' for r in rows) else 'FAIL','protectedFiles':len(protected),'changedProtectedFiles':changed,'builtAssets':assets,'modePairs':rows,'buildWarnings':warnings,'manifestPairs':flags}
(A/'source-resource-mode-audit.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result,indent=2));assert result['status']=='PASS'
