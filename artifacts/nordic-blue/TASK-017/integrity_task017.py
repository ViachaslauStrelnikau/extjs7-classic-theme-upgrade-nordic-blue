from pathlib import Path
import hashlib,json,sys
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');A=R/'artifacts/nordic-blue/TASK-017'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rows=[]
for task in ['TASK-014','TASK-015','TASK-016']:
 base=R/'artifacts/nordic-blue'/task;m=read(base/'artifact-manifest.json');bad=[];missing=[]
 for item in m['files']:
  p=(base/item['path']).resolve();assert p.is_relative_to(base.resolve()),str(p)
  if not p.exists():missing.append(item['path'])
  elif sha(p)!=item['sha256'] or p.stat().st_size!=item['bytes']:bad.append(item['path'])
 rows.append({'task':task,'status':'PASS' if not bad and not missing else 'FAIL','filesChecked':len(m['files']),'manifestSha256':sha(base/'artifact-manifest.json'),'missing':missing,'changed':bad})
protected=read(R/'artifacts/nordic-blue/TASK-016/protected-before.json');changed=[k for k,v in protected.items() if sha(R/k)!=v];assert not changed,changed
result={'status':'PASS' if all(r['status']=='PASS' for r in rows) else 'FAIL','evidence':rows,'protectedSources':len(protected),'changedProtectedFiles':changed,'policy':'Verify actual local retained evidence bytes. No changes to previous baselines, goldens or approvals.'}
(A/'integrity-check.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result,indent=2));assert result['status']=='PASS'
