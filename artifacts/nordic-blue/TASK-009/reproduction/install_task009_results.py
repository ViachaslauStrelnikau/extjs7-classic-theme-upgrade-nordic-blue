from pathlib import Path
import json,hashlib,shutil
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');O=Path(__file__).parent/'output/task009';A=R/'artifacts/nordic-blue/TASK-009';D=O/'documents'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
expected=read(O/'document-expected.json')
for rel,h in expected.items():assert (sha(R/rel) if (R/rel).exists() else None)==h,rel
for name in ['flat-geometry.json','core-state-comparison.json','lint-report.json','compiler-consumption.json','policy-controls.json']:assert read(O/name)['status']=='PASS'
for rel,h in expected.items():
 if h is not None:
  target=A/'before-final-documents'/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,target)
for p in O.rglob('*'):
 if not p.is_file():continue
 rel=p.relative_to(O)
 if rel.parts[0] in ['phase-a','flat','documents','control-package','__pycache__','nordic','core-states','core-states-v2','core-states-v3','frozen-gif-frame0']:continue
 if p.name in ['diagnostics.zip','consumption-probe.css','consumption-probe.scss']:continue
 target=A/rel
 if target.exists():
  assert sha(target)==sha(p),str(target)
  continue
 target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
for name in ['prepare_task009.py','install_task009_phase_a.py','adapt_task009_tools.py','prepare_task009_flat.py','install_task009_flat.py','prune_task009_unused.py','fix_task009_focus_palette.py','fix_task009_focus_pressed.py','adapt_task009_controls.py','finish_task009.py','install_task009_results.py']:
 target=A/'reproduction'/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(Path(__file__).parent/name,target)
for rel in ['config/nordic-blue-policy.json','config/nordic-blue-icons.json','tools/lint-nordic-blue.py','TestApp/packages/local/theme-nordic-blue/package.json']:
 target=A/'source-snapshot'/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,target)
# Full Sass/config and compiled CSS snapshots are already packed in evidence.zip.
for p in D.rglob('*'):
 if p.is_file():
  target=R/p.relative_to(D);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
protected=read(A/'protected-inputs.json');assert all(sha(R/p)==h for p,h in protected.items())
assert not list((R/'TestApp/packages/local/theme-nordic-blue/overrides').iterdir())
assert not list((R/'TestApp/packages/local/theme-nordic-blue/resources/images').iterdir())
proof={'status':'PASS','protectedApplicationFiles':len(protected),'sourceImagesEmpty':True,'sourceOverridesEmpty':True,
 'sourcePolicySha256':sha(R/'config/nordic-blue-policy.json'),'lintSha256':sha(R/'tools/lint-nordic-blue.py'),
 'compiledCssSha256':sha(R/'TestApp/build/theme-lab/nordic/testing/resources/NordicThemeLab-all.css'),
 'finalFullCapturePass':3,'finalCoreStates':'core-states-v3'}
(A/'post-install-guards.json').write_text(json.dumps(proof,indent=2),encoding='utf-8')
inventory={str(p.relative_to(A)).replace('\\','/'):sha(p) for p in A.rglob('*') if p.is_file() and p.name!='artifact-manifest.json'}
(A/'artifact-manifest.json').write_text(json.dumps({'files':inventory},indent=2),encoding='utf-8')
print(json.dumps({'status':'INSTALLED','artifactFiles':len(inventory),'documents':len(expected),'protectedApplicationFiles':len(protected)}))
