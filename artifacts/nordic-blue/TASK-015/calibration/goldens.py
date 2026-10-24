from pathlib import Path
from PIL import Image,ImageSequence
import hashlib,json,shutil
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');O=Path(__file__).parent;A=O.parent
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def create():
 result=read(O/'visual-results.json');assert result['status']=='PASS' and result['cases']==204
 G=A/'golden-v1';assert not G.exists();G.mkdir();entries=[]
 for r in result['results']:
  d,s=r['dpr'],r['stem'];F=O/'captures'/f'dpr-{d}'/'nordic';dest=G/'native'/f'dpr-{d}';dest.mkdir(parents=True,exist_ok=True)
  for kind in ['raw','normalized']:
   source=F/(s+'--'+kind+'.png');target=dest/source.name;shutil.copy2(source,target);entries.append({'scope':'native','case':r['case'],'state':r['state'],'dpr':d,'kind':kind,'path':str(target.relative_to(G)).replace('\\','/'),'sha256':sha(target)})
  source=O/'diffs'/f'dpr-{d}'/(s+'--icon-support.png');target=dest/source.name;shutil.copy2(source,target);entries.append({'scope':'frozen-icon-support','case':r['case'],'state':r['state'],'dpr':d,'path':str(target.relative_to(G)).replace('\\','/'),'sha256':sha(target)})
 policy=read(R/'config/nordic-blue-icons.json');frames=[]
 for resource,item in policy['runtimeImages'].items():
  source=R/'TestApp/build/theme-lab/nordic/testing/resources'/resource
  assert sha(source)==item['sha256'],resource
  im=Image.open(source)
  for i,frame in enumerate(ImageSequence.Iterator(im)):
   rgba=frame.convert('RGBA');target=G/'artwork'/resource/f'frame-{i:03d}.png';target.parent.mkdir(parents=True,exist_ok=True);rgba.save(target)
   frames.append({'resource':resource,'density':item['density'],'frame':i,'size':list(rgba.size),'path':str(target.relative_to(G)).replace('\\','/'),'sha256':sha(target),'rgbaSha256':hashlib.sha256(rgba.tobytes()).hexdigest(),'sourceSha256':item['sha256']})
 manifest={'version':'nordic-blue-visual-v1','status':'INITIAL_TECHNICAL_BASELINE','policy':'No automatic replacement. Active icon artwork is user-approved v3; this initial full-theme snapshot records tested implementation, not final user/release acceptance. Require review for any future golden update.','activeIcons':{k:policy[k] for k in ['manifestPath','manifestSha256','approvalPath','approvalSha256']},'nativeCases':204,'nativeSnapshots':408,'artworkResources':len(policy['runtimeImages']),'artworkFrames':len(frames),'threshold':{'maxChannelDelta':0,'maxChangedPixels':0,'maskDilation':0},'entries':entries,'frames':frames}
 (G/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in manifest.items() if k not in ['entries','frames','activeIcons']}))
if __name__=='__main__':create()
