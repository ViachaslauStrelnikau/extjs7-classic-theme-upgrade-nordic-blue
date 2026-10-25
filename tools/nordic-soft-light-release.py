"""Reproducible source-only handoff of all three required theme packages."""
from pathlib import Path
import argparse,json,hashlib,zipfile
R=Path(__file__).resolve().parents[1];p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args();O=Path(args.output).resolve()
if O.exists():raise SystemExit('Use a new output directory; existing evidence is immutable')
sha=lambda b:hashlib.sha256(b).hexdigest();read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));files=set()
for name in ['theme-nordic-blue','theme-nordic-blue-soft','theme-nordic-blue-soft-contrast']:
 root=R/'TestApp/packages/local'/name
 for f in root.rglob('*'):
  if f.is_file():
   assert '.sencha' not in f.parts
   if f.suffix=='.js':assert f.relative_to(R).as_posix()=='TestApp/packages/local/theme-nordic-blue-soft/resources/soft-motion.js'
   files.add(f)
for cfg in ['config/nordic-blue-icons.json','config/nordic-soft-icons.json']:
 conf=read(R/cfg);manifest=R/conf['manifestPath'];assert sha(manifest.read_bytes())==conf['manifestSha256'];assert sha((R/conf['approvalPath']).read_bytes())==conf['approvalSha256'];files.update([R/cfg,manifest,R/conf['approvalPath']]);m=read(manifest)
 for e in m['entries']:
  f=(manifest.parent/e['master']).resolve();assert f.is_relative_to(R.resolve()) and f.suffix=='.svg' and sha(f.read_bytes())==e['masterSha256'];files.add(f)
for f in ['artifacts/nordic-blue/TASK-030/report.md','config/nordic-soft-contrast-policy.json','artifacts/nordic-blue/TASK-030/design-approval.json','docs/nordic-soft-light-installation.md','config/nordic-blue-policy.json','config/nordic-soft-policy.json','docs/nordic-soft-installation.md','docs/plans/nordic-blue/palette.md','artifacts/nordic-blue/TASK-004/sources-and-license.md','artifacts/nordic-blue/TASK-021/integration-report.md','artifacts/nordic-blue/TASK-021/acceptance-matrix.json','artifacts/nordic-blue/REV-002-tree-warm-v2/candidate-manifest.json','tools/nordic-soft-light-release.py']:files.add(R/f)
payload={f.relative_to(R).as_posix():f.read_bytes() for f in sorted(files)}
assert not any(f.endswith(('.png','.gif')) and not f.startswith('TestApp/packages/local/') for f in payload),'Reference bitmaps must not ship'
manifest={'version':'nordic-soft-light-source-handoff-v1.1','sdk':'7.7.0.31','packages':['theme-nordic-blue','theme-nordic-blue-soft','theme-nordic-blue-soft-contrast'],'policy':'Source-only, optional public-listener motion module. No SDK/Classic reference assets/compiled app/dependencies/debug patches. No new license grant. Full source/evidence remains in repository.','files':[{'path':n,'bytes':len(b),'sha256':sha(b)} for n,b in payload.items()]};payload['SOURCE-MANIFEST.json']=(json.dumps(manifest,indent=2)+'\n').encode('utf-8')
O.mkdir(parents=True);archive=O/'nordic-soft-light-extjs-classic-7.7-source.zip'
with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for n,b in sorted(payload.items()):
  info=zipfile.ZipInfo(n,(2026,10,25,0,0,0));info.create_system=3;info.external_attr=0o100644<<16;info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,b,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
with zipfile.ZipFile(archive) as z:assert z.testzip() is None and all(z.read(n)==b for n,b in payload.items())
receipt={'status':'PASS','archive':archive.name,'bytes':archive.stat().st_size,'sha256':sha(archive.read_bytes()),'payloadFiles':len(manifest['files']),'source':manifest}
(O/'release-manifest.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in receipt.items() if k!='source'},indent=2))
