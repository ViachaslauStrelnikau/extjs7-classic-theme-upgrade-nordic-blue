from pathlib import Path
import json
from compare import rgb,changed
O=Path(__file__).parent;C=O.parent/'calibration-final';read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
rows=[]
for d in [1,2]:
 index=read(C/f'captures/dpr-{d}/index.json');assert index['status']=='PASS' and len(index['records'])==29
 for r in index['records']:
  for theme in ['classic','nordic']:
   for kind in ['raw','normalized','support-white','support-black']:
    name=r['stem']+'--'+kind+'.png';a=rgb(O/f'captures/dpr-{d}'/theme/name);b=rgb(C/f'captures/dpr-{d}'/theme/name);count=int(changed(a,b).sum())
    rows.append({'dpr':d,'case':r['case'],'state':r['state'],'theme':theme,'kind':kind,'pixels':count,'status':'FAIL' if count else 'PASS'})
result={'status':'PASS' if all(r['status']=='PASS' for r in rows) else 'FAIL','scenariosPerDpr':29,'imageComparisons':len(rows),'changedPixels':sum(r['pixels'] for r in rows),'threshold':{'maxChannelDelta':0,'maxChangedPixels':0,'maskDilation':0},'results':rows}
(O.parent/'calibration-report.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in result.items() if k!='results'}));assert result['status']=='PASS'
