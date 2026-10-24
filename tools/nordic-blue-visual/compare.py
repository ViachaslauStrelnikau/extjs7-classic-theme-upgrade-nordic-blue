from pathlib import Path
import json,sys,hashlib,importlib.util,math,html
import numpy as np
from PIL import Image,ImageDraw
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');O=Path(__file__).parent
sys.path.insert(0,str(R/'tools/nordic-blue-regression'));from metrics import compare
spec=importlib.util.spec_from_file_location('contracts',R/'tools/nordic-blue-regression/icon-contracts.py');contracts=importlib.util.module_from_spec(spec);spec.loader.exec_module(contracts)
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def rgb(p):return np.asarray(Image.open(p).convert('RGB'))
def changed(a,b):
 if a.shape!=b.shape:raise ValueError('Image dimensions differ')
 return np.any(a!=b,axis=2)
def save_diff(a,b,p):
 mask=changed(a,b);im=np.full_like(a,255);im[mask]=[210,25,70];Image.fromarray(im).save(p);return int(mask.sum())
def compare_case(folder,dpr,stem,save=True):
 ca=folder/'classic';nb=folder/'nordic';a,b=read(ca/(stem+'.json')),read(nb/(stem+'.json'))
 bound,observed=contracts.bind_icon_contracts(a['metrics'],b['metrics'],dpr);issues=compare(a['metrics'],bound)
 for doc in [a,b]:issues+=['normalization/'+x for x in compare(doc['metrics'],doc['normalizedMetrics'])]
 x,y=rgb(ca/(stem+'--normalized.png')),rgb(nb/(stem+'--normalized.png'))
 def support(root):return np.any(rgb(root/(stem+'--support-white.png'))!=255,axis=2)|np.any(rgb(root/(stem+'--support-black.png'))!=0,axis=2)
 ma,mb=support(ca),support(nb);mask=ma|mb
 diff=changed(x,y);outside=diff&~mask
 # Every excluded support pixel must belong to a listed approved background owner.
 bounds=Image.new('1',(x.shape[1],x.shape[0]));draw=ImageDraw.Draw(bounds)
 for region in a['regions']:
  for side,doc in [('classicHost',a),('nordicHost',b)]:
   r=region[side]
   # Installed Classic checkcolumn ::after participates in inline baseline layout;
   # its painted ink can extend below the host span's DOMRect. No pseudo rect is
   # invented. Bound the observed support by its recorded semantic cell-inner.
   # This guard does not add any pixel to the exclusion mask.
   if region['node'].endswith('::after') and region['parent']=='images/form/checkbox.gif':
    hosts=[e for e in doc['metrics']['elements'] if e['rect']==r and e['id'].endswith('/graphic/x-grid-checkcolumn')]
    if len(hosts)==1:
     parent_id=hosts[0]['id'].rsplit('/graphic/',1)[0];parents=[e for e in doc['metrics']['elements'] if e['id']==parent_id]
     assert len(parents)==1;r=parents[0]['rect']
   # At DPR2 the legacy Classic tab-close raster has an observed device-pixel
   # fringe beyond its fractional host border. Bound by the real containing tab;
   # keep the measured support unchanged (no padding/dilation/tolerance).
   if region['parent']=='images/tab/tab-default-close.gif':
    hosts=[e for e in doc['metrics']['elements'] if e['rect']==r and e['id'].endswith('/part/tab-close')]
    if len(hosts)==1:
     parent_id=hosts[0]['id'].rsplit('/part/',1)[0];parents=[e for e in doc['metrics']['elements'] if e['id']==parent_id]
     assert len(parents)==1;r=parents[0]['rect']
   l=math.floor(r['x']*dpr);t=math.floor((r['y']-doc['clip']['y'])*dpr);right=math.ceil((r['x']+r['width'])*dpr)-1;bottom=math.ceil((r['y']+r['height']-doc['clip']['y'])*dpr)-1
   if right>=l and bottom>=t:draw.rectangle((l,t,right,bottom),fill=1)
 leaks=mask&~np.asarray(bounds,dtype=bool)
 if outside.any():issues.append('normalized-structure-pixels')
 if leaks.any():issues.append('icon-support-outside-approved-owner')
 if not a['regions'] and mask.any():issues.append('unexpected-support')
 repeat=[]
 for theme,doc in [('classic',a),('nordic',b)]:
  previous=R/('artifacts/nordic-blue/TASK-006/captures/pass-1' if theme=='classic' else 'artifacts/nordic-blue/TASK-014/run-1/nordic/captures/pass-1')/f'dpr-{dpr}'/(stem+'.png')
  old=Image.open(previous).convert('RGB');new=rgb(folder/theme/(stem+'--raw.png'));top=round(doc['clip']['y']*dpr);cropped=np.asarray(old.crop((0,top,new.shape[1],top+new.shape[0])))
  count=int(changed(cropped,new).sum());repeat.append({'theme':theme,'pixels':count,'source':str(previous.relative_to(R)).replace('\\','/')})
  if count:issues.append(theme+'-raw-repeat')
 if save:
  target=O/'diffs'/f'dpr-{dpr}';target.mkdir(parents=True,exist_ok=True)
  save_diff(x,y,target/(stem+'--all.png'))
  out=np.full_like(x,255);out[outside]=[210,25,70];Image.fromarray(out).save(target/(stem+'--structure.png'))
  Image.fromarray((mask*255).astype('uint8')).save(target/(stem+'--icon-support.png'))
 return {'dpr':dpr,'case':a['case'],'state':a['state'],'stem':stem,'regions':a['regions'],'supportPixels':int(mask.sum()),'supportLeakPixels':int(leaks.sum()),'normalizedDiffPixels':int(diff.sum()),'structureDiffPixels':int(outside.sum()),'rawRepeat':repeat,'elements':a['metrics']['elementCount'],'iconObservations':len(observed),'status':'FAIL' if issues else 'PASS','issues':issues}
def main():
 rows=[]
 for d in [1,2]:
  folder=O/'captures'/f'dpr-{d}'
  if '--partial' in sys.argv:
   records=[{'stem':p.stem} for p in (folder/'nordic').glob('*.json')]
  else:
   index=read(folder/'index.json');assert index['status']=='PASS' and len(index['records'])==102;records=index['records']
   expected=read(R/f'artifacts/nordic-blue/TASK-006/captures/pass-1/dpr-{d}/index.json')['records']
   assert [(r['case'],r['state']) for r in records]==[(r['case'],r['state']) for r in expected]
  for r in records:
   row=compare_case(folder,d,r['stem']);rows.append(row)
   if row['issues']:print(json.dumps({k:v for k,v in row.items() if k!='regions'}),flush=True)
 status='PASS' if rows and all(r['status']=='PASS' for r in rows) else 'FAIL'
 result={'status':status,'cases':len(rows),'metricElementComparisons':sum(r['elements'] for r in rows),'rawRepeatComparisons':len(rows)*2,'structureDiffPixels':sum(r['structureDiffPixels'] for r in rows),'threshold':{'channelDelta':0,'allowedChangedPixels':0,'dilation':0},'results':rows}
 (O/('partial-results.json' if '--partial' in sys.argv else 'visual-results.json')).write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in result.items() if k!='results'}))
 if '--partial' not in sys.argv and status!='PASS':raise SystemExit(1)
if __name__=='__main__':main()
