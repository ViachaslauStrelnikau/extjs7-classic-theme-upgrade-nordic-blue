from pathlib import Path
import json,hashlib,shutil
ROOT=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue')
OUT=Path(__file__).parent/'output/task007';DEST=ROOT/'artifacts/nordic-blue/TASK-007'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
expected=read(OUT/'delivery-expected.json')
assert read(OUT/'inheritance-comparison.json')['status']=='PASS'
for rel,h in expected.items():
 p=ROOT/rel
 assert (sha(p) if p.exists() else None)==h,rel
# Preserve all modified existing documentation/config before guarded replacement.
for rel,h in expected.items():
 if h is not None:
  target=DEST/'before-documentation'/rel
  target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/rel,target)
for p in OUT.rglob('*'):
 if not p.is_file() or 'delivery' in p.relative_to(OUT).parts or p.name=='delivery-expected.json':continue
 target=DEST/p.relative_to(OUT);assert not target.exists(),str(target)
 target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
for name in ['prepare_task007.py','stage_task007_capture.py','compare_task007.py','finish_task007.py','install_task007.py']:
 target=DEST/'reproduction'/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(Path(__file__).parent/name,target)
for rel in ['TestApp/theme-lab/app.json','TestApp/theme-lab/build.xml','TestApp/theme-lab/build-entry.html','TestApp/packages/local/theme-nordic-blue/package.json']:
 target=DEST/'built-config'/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/rel,target)
for p in (OUT/'delivery').rglob('*'):
 if p.is_file():
  target=ROOT/p.relative_to(OUT/'delivery');target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
before=read(DEST/'protected-inputs.json')
assert all(sha(ROOT/p)==h for p,h in before.items())
baseline=read(ROOT/'artifacts/nordic-blue/TASK-006/input-hashes.json')
changes=[p for p,h in baseline.items() if sha(ROOT/p)!=h]
assert set(changes)<=set(expected),changes
post={'status':'PASS','unchangedApplicationFiles':len(before),'baselineSourceChanges':changes,
 'expectedDocumentChanges':list(expected),'note':'Source changes are limited to documented build-profile mirror/readme/plan instructions; common fixture and original TestApp application/config and SDK remain unchanged.'}
(DEST/'post-install-guards.json').write_text(json.dumps(post,indent=2),encoding='utf-8')
inventory={str(p.relative_to(DEST)).replace('\\','/'):sha(p) for p in DEST.rglob('*') if p.is_file() and p.name!='artifact-manifest.json'}
(DEST/'artifact-manifest.json').write_text(json.dumps({'files':inventory},indent=2),encoding='utf-8')
print(json.dumps({'status':'INSTALLED','files':len(inventory),'protectedApplicationFiles':len(before),'documentedBaselineSourceChanges':changes},ensure_ascii=False))
