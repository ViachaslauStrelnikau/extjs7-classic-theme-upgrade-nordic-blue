from pathlib import Path
import json,hashlib
from PIL import Image,ImageChops
OUT=Path(__file__).parent
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
reports=[]
for dpr in [1,2]:
 a=OUT/f'captures/pass-1/dpr-{dpr}';b=OUT/f'captures/pass-2/dpr-{dpr}'
 ai,bi=read(a/'index.json'),read(b/'index.json');assert ai['scenarioCount']==bi['scenarioCount']==102
 assert ai['viewport']==bi['viewport']==[1280,1600]
 results=[]
 for left,right in zip(ai['records'],bi['records']):
  assert (left['case'],left['state'])==(right['case'],right['state'])
  x,y=read(a/left['metrics']),read(b/right['metrics']);issues=[]
  for key in ['case','state','environment','fixtureSemanticCount','elementCount','visibleElementCount','duplicates','unownedGraphics','elements','icons','activeElement','scroll','data','stores','errors']:
   if x[key]!=y[key]:
    if key in ['elements','icons']:
     xx={i['id']:i for i in x[key]};yy={i['id']:i for i in y[key]}
     for id in sorted(set(xx)|set(yy)):
      if xx.get(id)!=yy.get(id):issues.append({'kind':key,'id':id,'first':xx.get(id),'second':yy.get(id)})
    else:issues.append({'kind':key,'first':x[key],'second':y[key]})
  first=Image.open(a/left['screenshot']).convert('RGBA');second=Image.open(b/right['screenshot']).convert('RGBA')
  pixel_count=None;bbox=None
  if first.size!=second.size:issues.append({'kind':'screenshot-dimensions','first':first.size,'second':second.size})
  else:
   diff=ImageChops.difference(first,second).convert('RGB');bbox=diff.getbbox()
   if bbox:
    pixel_count=sum(v!=(0,0,0) for v in diff.getdata());dest=OUT/f'diffs/dpr-{dpr}'/left['screenshot'];dest.parent.mkdir(parents=True,exist_ok=True);diff.save(dest)
   else:pixel_count=0
  record={'case':left['case'],'state':left['state'],'elements':x['elementCount'],'icons':len(x['icons']),'metricsIdentical':not issues,'screenshotIdentical':bbox is None and first.size==second.size,'differentPixels':pixel_count,'diffBounds':bbox,'pixelDimensions':first.size,'firstSha256':left['screenshotSha256'],'secondSha256':right['screenshotSha256'],'issues':issues}
  results.append(record)
 report={'dpr':dpr,'scenarios':len(results),'status':'PASS' if all(r['metricsIdentical'] and r['screenshotIdentical'] for r in results) else 'FAIL','elementComparisons':sum(r['elements'] for r in results),'iconComparisons':sum(r['icons'] for r in results),'results':results};reports.append(report)
result={'status':'PASS' if all(r['status']=='PASS' for r in reports) else 'FAIL','policy':'Exact equality within the same DPR, all pixels and all recorded metrics. No tolerance and no broad masks. GIF first composited frame served unchanged-size by declared route. Original animated live captures separate.','reports':reports}
(OUT/'repeatability.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'status':result['status'],'reports':[{'dpr':r['dpr'],'status':r['status'],'scenarios':r['scenarios'],'elements':r['elementComparisons'],'icons':r['iconComparisons'],'failures':[{'case':x['case'],'state':x['state'],'pixels':x['differentPixels'],'issues':[(i['kind'],i.get('id')) for i in x['issues']][:8]} for x in r['results'] if not x['metricsIdentical'] or not x['screenshotIdentical']]} for r in reports]},ensure_ascii=False))


if result["status"]!="PASS":raise SystemExit(1)
