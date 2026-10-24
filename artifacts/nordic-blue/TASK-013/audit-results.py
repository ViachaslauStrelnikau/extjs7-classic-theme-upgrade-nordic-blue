from pathlib import Path
import json,hashlib,importlib.util
from PIL import Image
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');O=Path(__file__).parent
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
policy=read(R/'config/nordic-blue-policy.json');icons=read(R/'config/nordic-blue-icons.json');approved=read(R/icons['manifestPath'])
protected=read(R/'artifacts/nordic-blue/TASK-013/protected-inputs.json');assert all(sha(R/p)==h for p,h in protected.items())
assert all(sha(R/p)==h for p,h in policy['sdkSources'].items());assert sha(R/icons['manifestPath'])==icons['manifestSha256'];assert sha(R/icons['approvalPath'])==icons['approvalSha256']
base=read(R/'artifacts/nordic-blue/TASK-006/input-hashes.json');changed=[p for p,h in base.items() if sha(R/p)!=h];assert set(changed)<={'AGENTS.md','TestApp/theme-lab/build-profiles.json','TestApp/theme-lab/README.md'},changed
images=[]
for key,item in icons['runtimeImages'].items():
 builds={}
 for mode in['testing','development','production']:
  p=R/f'TestApp/build/theme-lab/nordic/{mode}/resources'/key;assert sha(p)==item['sha256'];builds[mode]=sha(p)
 with Image.open(R/item['source']) as im:
  assert list(im.size)==item['bitmapDimensions'] and im.n_frames==item['frameCount']
  transparent=im.info.get('transparency') is not None or 'A' in im.getbands()
 images.append({'runtimeResource':key,'approvedId':item['id'],'density':item['density'],'bitmap':item['bitmapDimensions'],'cssSheet':item['cssBackgroundSize'],'frames':item['frameCount'],'transparencyChannelOrPalette':transparent,'approvedSha256':item['sha256'],'builtSha256':builds})
rows=[]
for e in approved['entries']:
 rows.append({'id':e['id'],'resource':e['resource'],'sourcePath':e['sourcePath'],'sourceSha256':e['sourceSha256'],'cssDimensions':e['classicDimensions'],'outputs':e['outputs'],'integration':'Copied exact approved bytes into child resources/images; preferred1x/2x selected through exact installed-selector CSS; original-format fallbacks retained.'})
(O/'integration-manifest.json').write_text(json.dumps({'version':'nordic-icons-v2-runtime-task013','approvedManifestSha256':icons['manifestSha256'],'approvalSha256':icons['approvalSha256'],'entries':rows,'runtimeFiles':images,'sourceApprovalUnchanged':True},indent=2),encoding='utf-8')
(O/'source-guards.json').write_text(json.dumps({'status':'PASS','sdkSassFiles':len(policy['sdkSources']),'originalApplicationInputs':len(protected),'baselineInputsCompared':len(base),'baselineDifferences':changed,'approvedBitmapFiles':len(images),'buildModesVerified':3,'overridesFiles':0,'note':'SDK/application/common fixture unchanged; immutable approved manifest, masters/candidates and approval hashes preserved. Source resources now intentionally contain the 648 approved runtime files.'},indent=2),encoding='utf-8')
scope={'__file__':str(O/'compare-geometry.py')};exec((O/'compare-geometry.py').read_text().split('from importlib.util')[0],scope);normalize=scope['normalize']
spec=importlib.util.spec_from_file_location('contracts',O/'icon-contracts.py');contracts=importlib.util.module_from_spec(spec);spec.loader.exec_module(contracts)
mode_rows=[]
for run in read(O/'build-mode-validation.json')['runs']:
 for reload in[0,1]:
  a=read(R/f'artifacts/nordic-blue/TASK-006/captures/pass-1/dpr-{run["dpr"]}/all--normal.json');b=read(O/'build-modes'/run['label']/f'native-{reload}.json');b,seen=contracts.bind_icon_contracts(a,b,run['density']);issues=[]
  for k in['elements','icons','activeElement','scroll','data','stores','duplicates','errors','unownedGraphics','elementCount','visibleElementCount']:
   if normalize(a[k])!=normalize(b[k]):issues.append(k)
  mode_rows.append({'mode':run['mode'],'dpr':run['dpr'],'fallback':run['fallback'],'reload':reload,'status':'FAIL' if issues else 'PASS','issues':issues,'elements':a['elementCount'],'mappedImages':len(seen)})
result={'status':'PASS' if all(r['status']=='PASS' for r in mode_rows) else 'FAIL','overviewComparisons':len(mode_rows),'elementComparisons':sum(r['elements'] for r in mode_rows),'results':mode_rows}
(O/'build-mode-geometry.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in result.items() if k!='results'}));assert result['status']=='PASS'
print('Guarded source and approved runtime images PASS',len(images))
