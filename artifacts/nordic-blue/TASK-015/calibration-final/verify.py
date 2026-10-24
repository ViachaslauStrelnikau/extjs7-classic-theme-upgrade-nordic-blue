from pathlib import Path
import json,sys,hashlib,importlib.util
import numpy as np
from PIL import Image,ImageSequence
from compare import rgb,changed,save_diff
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');O=Path(__file__).parent;G=R/'artifacts/nordic-blue/TASK-015/golden-v1'
sys.path.insert(0,str(R/'tools/nordic-blue-regression'));from metrics import compare
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 cfg=read(R/'config/nordic-blue-visual.json');assert sha(G/'manifest.json')==cfg['goldenManifestSha256']
 manifest=read(G/'manifest.json');icons=read(R/'config/nordic-blue-icons.json');assert manifest['activeIcons']['manifestSha256']==icons['manifestSha256'] and manifest['activeIcons']['approvalSha256']==icons['approvalSha256']
 rows=[];frames=[];controls=[]
 for e in manifest['entries']:
  assert sha(G/e['path'])==e['sha256'],'Golden modified '+e['path']
  d,s=e['dpr'],e['case']+'--'+e['state'];gold=rgb(G/e['path'])
  if e['scope']=='native':
   file=O/'captures'/f'dpr-{d}'/'nordic'/(s+'--'+e['kind']+'.png')
   target=O/'golden-diffs'/f'dpr-{d}'/(s+'--'+e['kind']+'.png');target.parent.mkdir(parents=True,exist_ok=True)
   count=save_diff(gold,rgb(file),target)
  else:
   actual=O/'diffs'/f'dpr-{d}'/(s+'--icon-support.png');count=int(changed(gold,rgb(actual)).sum())
  rows.append({'path':e['path'],'pixels':count,'status':'FAIL' if count else 'PASS'})
 decoded={}
 for e in manifest['frames']:
  assert sha(G/e['path'])==e['sha256']
  key=e['resource']
  if key not in decoded:
   source=R/'TestApp/build/theme-lab/nordic/testing/resources'/key;assert sha(source)==e['sourceSha256']
   decoded[key]=[np.asarray(f.convert('RGBA')) for f in ImageSequence.Iterator(Image.open(source))]
  actual=decoded[key][e['frame']];gold=np.asarray(Image.open(G/e['path']).convert('RGBA'));count=int(np.any(actual!=gold,axis=2).sum());frames.append({'resource':key,'frame':e['frame'],'pixels':count,'status':'FAIL' if count else 'PASS'})
 for d in [1,2]:
  base=G/'native'/f'dpr-{d}';support=np.asarray(Image.open(base/'tree--normal--icon-support.png').convert('L'))>0
  for kind in ['icon-shift-1px','adjacent-text-shift-1px','icon-artwork-filter']:
   f=O/'negative-controls'/f'dpr-{d}'/kind;metrics=read(f/'metrics.json');assert not metrics['errors'] and not metrics['bad']
   raw=rgb(base/'tree--normal--raw.png');norm=rgb(base/'tree--normal--normalized.png')
   assert not changed(raw,rgb(f/'before.png')).any()
   rawPixels=save_diff(raw,rgb(f/'mutated-raw.png'),f/'raw-diff.png')
   structure=changed(norm,rgb(f/'mutated-normalized.png'))&~support
   im=np.full_like(norm,255);im[structure]=[210,25,70];Image.fromarray(im).save(f/'structure-diff.png')
   deltas=compare(metrics['before'],metrics['mutated']);restored=compare(metrics['before'],metrics['restored'])
   restoredPixels=int(changed(raw,rgb(f/'restored.png')).sum());assert rawPixels>0 and restoredPixels==0 and not restored
   if kind=='adjacent-text-shift-1px':assert structure.any() and deltas
   if kind=='icon-shift-1px':assert deltas
   if kind=='icon-artwork-filter':assert not deltas,'Artwork control must prove pixel gate catches a defect without a metric delta'
   controls.append({'dpr':d,'kind':kind,'rawGoldenDiffPixels':rawPixels,'structureOutsideFrozenSupportPixels':int(structure.sum()),'geometryIssues':deltas,'restoredPixels':restoredPixels,'status':'PASS','expectedGateResult':'FAIL','actualGateResult':'FAIL'})
 result={'status':'PASS' if all(r['status']=='PASS' for r in rows+frames) else 'FAIL','nativeGoldenImages':sum(e['scope']=='native' for e in manifest['entries']),'frozenMasks':sum(e['scope']!='native' for e in manifest['entries']),'artworkResources':len(decoded),'artworkFrames':len(frames),'negativeControls':controls,'images':rows,'frames':frames}
 (O/'golden-results.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in result.items() if k not in ['images','frames']}));assert result['status']=='PASS'
if __name__=='__main__':main()
