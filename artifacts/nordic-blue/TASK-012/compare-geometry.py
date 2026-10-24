from pathlib import Path
import json,re,hashlib,sys
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');O=Path(__file__).parent
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
phase='flat'
probe='--probe' in sys.argv
color_properties={'color','backgroundColor','borderTopColor','borderRightColor','borderBottomColor','borderLeftColor','outlineColor'}
color_pattern=re.compile(r'rgba?\([^)]*\)|#[0-9a-fA-F]{3,8}\b')
def normalize(value):
 if isinstance(value,str):return re.sub(r'(?:http://127\.0\.0\.1:\d+)?/(?:theme-lab/sdk/build/classic/theme-classic|build/theme-lab/nordic/testing)/resources/', '/CLASSIC-RESOURCES/',value)
 if isinstance(value,list):return [normalize(x) for x in value]
 if isinstance(value,dict):
  result={}
  for k,v in value.items():
   if k in color_properties:continue
   if k in ['backgroundImage','boxShadow']:
    result[k]=('none' if phase=='flat' and k=='backgroundImage' and 'gradient(' in v and 'url(' not in v else color_pattern.sub('<color>',normalize(v)))
   else:result[k]=normalize(v)
  return result
 return value
reports=[]
for dpr in [1,2]:
 base=R/f'artifacts/nordic-blue/TASK-006/captures/pass-1/dpr-{dpr}';folder=O/(f'nordic/probe/dpr-{dpr}/pass-1' if probe else f'nordic/captures/pass-1/dpr-{dpr}')
 index=read(folder/'index.json');assert index['scenarioCount']==(28 if probe else 102)
 results=[]
 for row in index['records']:
  a,b=read(base/row['metrics']),read(folder/row['metrics']);issues=[];paint=0
  for key in ['case','state','fixtureSemanticCount','elementCount','visibleElementCount','duplicates','unownedGraphics','elements','icons','activeElement','scroll','data','stores','errors']:
   x,y=normalize(a[key]),normalize(b[key])
   if x!=y:
    if key in ['elements','icons']:
     xx={z['id']:z for z in x};yy={z['id']:z for z in y}
     for name in sorted(set(xx)|set(yy)):
      if xx.get(name)!=yy.get(name):issues.append({'kind':key,'id':name,'classic':xx.get(name),'nordic':yy.get(name)})
    else:issues.append({'kind':key,'classic':x,'nordic':y})
  ae,be=dict(a['environment']),dict(b['environment']);ae.pop('profile');be.pop('profile')
  if ae!=be:issues.append({'kind':'environment','classic':ae,'nordic':be})
  assert b['environment']['profile']['theme']=='nordic'
  assert not b['network']['errors'] and not b['network']['badResponses']
  for x,y in zip(a['elements'],b['elements']):
   assert x['id']==y['id']
   for prop in color_properties|{'backgroundImage','boxShadow'}:
    if normalize(x['computed'].get(prop))!=normalize(y['computed'].get(prop)):paint+=1
  results.append({'case':row['case'],'state':row['state'],'elements':a['elementCount'],'icons':len(a['icons']),'paintPropertyDifferences':paint,'status':'FAIL' if issues else 'PASS','issues':issues})
 report={'dpr':dpr,'scenarios':len(results),'elementComparisons':sum(x['elements'] for x in results),'iconComparisons':sum(x['icons'] for x in results),'status':'PASS' if all(x['status']=='PASS' for x in results) else 'FAIL','results':results};reports.append(report)
result={'status':'PASS' if all(x['status']=='PASS' for x in reports) else 'FAIL','policy':'Exact geometry, typography, box model, visibility/opacity, state/data/focus/scroll, image names/sizes/offsets and non-color computed values. Only explicit paint-color properties and RGB/hex colors inside background gradients/shadows are omitted; shadow structure is retained; in flat phase the reviewed gradient-only background layers are removed, image URLs remain compared through icon observations. Resource roots mapped explicitly. No pixel equality claim for this palette stage.','excludedColorProperties':sorted(color_properties),'reports':reports}
(O/('phase-a-geometry.json' if probe else 'geometry-comparison.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'status':result['status'],'reports':[{'dpr':x['dpr'],'scenarios':x['scenarios'],'elements':x['elementComparisons'],'icons':x['iconComparisons'],'failures':[(v['case'],v['state'],[(i['kind'],i.get('id')) for i in v['issues']][:5]) for v in x['results'] if v['status']=='FAIL']} for x in reports]}))
if result['status']!='PASS':raise SystemExit(1)
