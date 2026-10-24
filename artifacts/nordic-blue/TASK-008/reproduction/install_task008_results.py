from pathlib import Path
import json,hashlib,shutil
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');O=Path(__file__).parent/'output/task008';A=R/'artifacts/nordic-blue/TASK-008';D=O/'documents'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
expected=read(O/'document-expected.json')
for rel,h in expected.items():assert (sha(R/rel) if (R/rel).exists() else None)==h,rel
for name in ['geometry-comparison.json','lint-report.json','compiler-consumption.json','policy-controls.json']:assert read(O/name)['status']=='PASS'
for rel,h in expected.items():
 if h is not None:
  backup=A/'before-documents'/rel;backup.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,backup)
# Publish the evidence without disposable package copies or staged delivery files.
for p in O.rglob('*'):
 if not p.is_file():continue
 rel=p.relative_to(O)
 if rel.parts[0] in ['delivery','documents','control-package','preflight-package','__pycache__']:continue
 target=A/rel;assert not target.exists(),str(target)
 target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
for name in ['prepare_task008.py','install_task008_sources.py','fix_task008_token_import.py','prepare_task008_evidence.py','finish_task008.py','install_task008_results.py']:
 target=A/'reproduction'/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(Path(__file__).parent/name,target)
for rel in ['config/nordic-blue-policy.json','config/nordic-blue-icons.json','tools/lint-nordic-blue.py','TestApp/packages/local/theme-nordic-blue/package.json']:
 target=A/'source-snapshot'/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,target)
shutil.copytree(R/'TestApp/packages/local/theme-nordic-blue/sass',A/'source-snapshot/theme-sass')
for rel in ['app.json','resources/NordicThemeLab-all.css']:
 target=A/'compiled'/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/'TestApp/build/theme-lab/nordic/testing'/rel,target)
for p in D.rglob('*'):
 if p.is_file():
  target=R/p.relative_to(D);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
protected=read(A/'protected-inputs.json');assert all(sha(R/p)==h for p,h in protected.items())
assert not list((R/'TestApp/packages/local/theme-nordic-blue/overrides').iterdir())
assert not list((R/'TestApp/packages/local/theme-nordic-blue/resources/images').iterdir())
guard={'status':'PASS','protectedApplicationFiles':len(protected),'sourceImagesEmpty':True,'sourceOverridesEmpty':True,
       'sourcePolicySha256':sha(R/'config/nordic-blue-policy.json'),'iconPolicySha256':sha(R/'config/nordic-blue-icons.json'),'lintSha256':sha(R/'tools/lint-nordic-blue.py'),
       'compiledCssSha256':sha(R/'TestApp/build/theme-lab/nordic/testing/resources/NordicThemeLab-all.css')}
(A/'post-install-guards.json').write_text(json.dumps(guard,indent=2),encoding='utf-8')
inventory={str(p.relative_to(A)).replace('\\','/'):sha(p) for p in A.rglob('*') if p.is_file() and p.name!='artifact-manifest.json'}
(A/'artifact-manifest.json').write_text(json.dumps({'files':inventory},indent=2),encoding='utf-8')
print(json.dumps({'status':'INSTALLED','artifactFiles':len(inventory),'documents':len(expected),'protectedApplicationFiles':len(protected)}))
