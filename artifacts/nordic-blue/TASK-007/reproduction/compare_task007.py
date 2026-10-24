from pathlib import Path
import json,hashlib,re,sys
from PIL import Image,ImageChops
ROOT=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue')
OUT=Path(__file__).parent/'output/task007'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def normalize(value):
 if isinstance(value,str):
  # Map only the two known build resource roots to the same logical path.
  # No changes to image names, offsets, CSS metrics, paint, state or coordinates.
  return re.sub(r'(?:http://127\.0\.0\.1:\d+)?/(?:theme-lab/sdk/build/classic/theme-classic|build/theme-lab/nordic/testing)/resources/', '/CLASSIC-RESOURCES/',value)
 if isinstance(value,list):return [normalize(x) for x in value]
 if isinstance(value,dict):return {k:normalize(v) for k,v in value.items()}
 return value
probe='--probe' in sys.argv
reports=[]
chrome=read(OUT/'lab-chrome.json')
for dpr in ([1] if probe else [1,2]):
 a=ROOT/f'artifacts/nordic-blue/TASK-006/captures/pass-1/dpr-{dpr}'
 b=OUT/'nordic'/Path(f'probe/dpr-{dpr}/pass-1' if probe else f'captures/pass-1/dpr-{dpr}')
 records=[{'case':'all','state':'normal','metrics':'all--normal.json','screenshot':'all--normal.png'}] if probe else read(b/'index.json')['records']
 results=[]
 for rec in records:
  x,y=read(a/rec['metrics']),read(b/rec['metrics']);issues=[]
  for key in ['case','state','fixtureSemanticCount','elementCount','visibleElementCount','duplicates','unownedGraphics','elements','icons','activeElement','scroll','data','stores','errors']:
   xx,yy=normalize(x[key]),normalize(y[key])
   if xx!=yy:
    if key in ['elements','icons']:
     left={v['id']:v for v in xx};right={v['id']:v for v in yy}
     for id in sorted(set(left)|set(right)):
      if left.get(id)!=right.get(id):issues.append({'kind':key,'id':id,'classic':left.get(id),'child':right.get(id)})
    else:issues.append({'kind':key,'classic':xx,'child':yy})
  ex,ey=dict(x['environment']),dict(y['environment']);ex.pop('profile');ey.pop('profile')
  if ex!=ey:issues.append({'kind':'environment','classic':ex,'child':ey})
  left=Image.open(a/rec['screenshot']).convert('RGB');right=Image.open(b/rec['screenshot']).convert('RGB')
  assert left.size==right.size
  raw=ImageChops.difference(left,right);rawbox=raw.getbbox()
  # The native HTML theme selector and profile-name status are outside the Ext
  # fixture. Exclude only their measured boxes, retain every raw raster/diff.
  diff=raw.copy()
  for box in chrome['rectsByScenario'][rec['case']+'/'+rec['state']]:
   pix=tuple(round(v*dpr) for v in box)
   diff.paste((0,0,0),pix)
  bounds=diff.getbbox();count=sum(p!=(0,0,0) for p in diff.getdata()) if bounds else 0
  if rawbox:
   dest=OUT/f'diffs/dpr-{dpr}'/rec['screenshot'];dest.parent.mkdir(parents=True,exist_ok=True);raw.save(dest)
  results.append({'case':rec['case'],'state':rec['state'],'elements':x['elementCount'],'icons':len(x['icons']),
   'metricsIdentical':not issues,'fixturePixelsIdentical':bounds is None,'differentFixturePixels':count,
   'rawDiffBounds':rawbox,'fixtureDiffBounds':bounds,'issues':issues,
   'classicPngSha256':sha(a/rec['screenshot']),'childPngSha256':sha(b/rec['screenshot'])})
 report={'dpr':dpr,'scenarios':len(results),'elementComparisons':sum(v['elements'] for v in results),
  'iconComparisons':sum(v['icons'] for v in results),'results':results,
  'status':'PASS' if all(v['metricsIdentical'] and v['fixturePixelsIdentical'] for v in results) else 'FAIL'}
 reports.append(report)
result={'status':'PASS' if all(r['status']=='PASS' for r in reports) else 'FAIL',
 'policy':'Exact computed metrics including paint after explicit resource-root mapping. Exact raster outside two measured native lab metadata controls (theme selector/profile status); no Ext component regions excluded, no pixel tolerance. Raw rasters and raw diffs preserved.',
 'metadataRects':chrome,'reports':reports}
(OUT/('probe-comparison.json' if probe else 'inheritance-comparison.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'status':result['status'],'reports':[{'dpr':r['dpr'],'scenarios':r['scenarios'],'elements':r['elementComparisons'],'icons':r['iconComparisons'],'failures':[{'case':v['case'],'state':v['state'],'pixels':v['differentFixturePixels'],'issues':[(i['kind'],i.get('id')) for i in v['issues']][:4]} for v in r['results'] if not v['metricsIdentical'] or not v['fixturePixelsIdentical']]}for r in reports]},ensure_ascii=False))
if result['status']!='PASS':raise SystemExit(1)
