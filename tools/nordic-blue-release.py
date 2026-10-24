"""Create a deterministic source-only Nordic Blue handoff; never overwrite a release."""
from pathlib import Path
import argparse,hashlib,json,zipfile,sys
R=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args();out=Path(args.output).resolve()
if out.exists():raise SystemExit('Output must be new; accepted releases are immutable')
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda b:hashlib.sha256(b).hexdigest()
policy=read(R/'config/nordic-blue-icons.json');manifestPath=R/policy['manifestPath'];manifest=read(manifestPath)
assert sha(manifestPath.read_bytes())==policy['manifestSha256']
assert sha((R/policy['approvalPath']).read_bytes())==policy['approvalSha256']
files=set(p for p in (R/'TestApp/packages/local/theme-nordic-blue').rglob('*') if p.is_file())
assert not any('.sencha' in p.parts or p.suffix=='.js' for p in files),'No SDK/cache/runtime JS in source package'
for key,item in policy['runtimeImages'].items():assert sha((R/'TestApp/packages/local/theme-nordic-blue/resources'/key).read_bytes())==item['sha256']
for entry in manifest['entries']:
 p=(manifestPath.parent/entry['master']).resolve();assert p.is_relative_to(R.resolve()) and p.suffix=='.svg';assert sha(p.read_bytes())==entry['masterSha256'];files.add(p)
for relative in [policy['manifestPath'],policy['approvalPath'],'artifacts/nordic-blue/TASK-004/approval.json','artifacts/nordic-blue/TASK-004/sources-and-license.md','artifacts/nordic-blue/TASK-004/export_task004.py','config/nordic-blue-icons.json','config/nordic-blue-policy.json','config/nordic-blue-visual.json','docs/nordic-blue-installation.md','docs/nordic-blue-release-notes.md','docs/plans/nordic-blue/palette.md','docs/plans/nordic-blue/coverage.md','docs/plans/nordic-blue/traceability.md','artifacts/nordic-blue/TASK-014/regression-report.md','artifacts/nordic-blue/TASK-015/visual-report.md','artifacts/nordic-blue/TASK-015/visual-policy.md','artifacts/nordic-blue/TASK-016/acceptance-report.md','artifacts/nordic-blue/TASK-016/acceptance-matrix.json','artifacts/nordic-blue/TASK-017/acceptance-report.md','artifacts/nordic-blue/TASK-017/deviations.md','artifacts/nordic-blue/TASK-017/coverage-traceability.json','tools/nordic-blue-release.py']:
 files.add(R/relative)
assert all(p.is_file() for p in files)
assert not any(p.suffix.lower() in ['.png','.gif'] and not p.is_relative_to(R/'TestApp/packages/local/theme-nordic-blue') for p in files),'Exclude Classic reference assets'
payload={p.relative_to(R).as_posix():p.read_bytes() for p in sorted(files)}
records=[{'path':name,'bytes':len(body),'sha256':sha(body)} for name,body in payload.items()]
contract={'format':'nordic-blue-source-handoff-v1','sdk':'7.7.0.31','cmd':'7.7.0.36','activeIcons':{'version':manifest['version'],'manifestSha256':policy['manifestSha256'],'approvalSha256':policy['approvalSha256']},'policy':'Source theme package plus approved SVG masters, notices, config, palette and report summaries; no SDK, Classic reference assets, compiled application, dependencies, runtime overrides or temporary debug patches. No license grant invented. Full evidence remains in repository/local artifacts.','files':records}
payload['SOURCE-MANIFEST.json']=(json.dumps(contract,indent=2)+'\n').encode('utf-8')
out.mkdir(parents=True);archive=out/'nordic-blue-extjs-classic-7.7-source.zip'
with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for name,body in sorted(payload.items()):
  info=zipfile.ZipInfo(name,(2026,10,24,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.create_system=3;info.external_attr=0o100644<<16;z.writestr(info,body,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
with zipfile.ZipFile(archive) as z:
 assert sorted(z.namelist())==sorted(payload) and z.testzip() is None
 assert all(z.read(name)==body for name,body in payload.items())
receipt={'status':'PASS','archive':archive.name,'archiveBytes':archive.stat().st_size,'archiveSha256':sha(archive.read_bytes()),'payloadFiles':len(records),'payloadManifestSha256':sha(payload['SOURCE-MANIFEST.json']),'verification':'Every ZIP entry and SHA exactly equals current source bytes; ZIP CRC checked. Accepted consuming-app builds are TASK-016, not a claimed independent blank-workspace build.','source':contract}
(out/'release-manifest.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in receipt.items() if k!='source'},indent=2))
