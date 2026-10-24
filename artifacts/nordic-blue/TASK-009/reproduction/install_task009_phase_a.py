from pathlib import Path
import json,hashlib,shutil
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');O=Path(__file__).parent/'output/task009';D=O/'phase-a';A=R/'artifacts/nordic-blue/TASK-009'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
expected=json.loads((O/'phase-a-expected.json').read_text())
for rel,h in expected.items():assert (sha(R/rel) if (R/rel).exists() else None)==h,rel
A.mkdir(exist_ok=False)
shutil.copytree(R/'TestApp/packages/local/theme-nordic-blue',A/'before-theme')
for rel in ['config/nordic-blue-policy.json','tools/lint-nordic-blue.py','AGENTS.md','docs/plans/nordic-blue/README.md','docs/plans/nordic-blue/tasks/TASK-009.md']:
 dest=A/'before'/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,dest)
protected=json.loads((R/'artifacts/nordic-blue/TASK-008/protected-inputs.json').read_text());assert all(sha(R/p)==h for p,h in protected.items())
(A/'protected-inputs.json').write_text(json.dumps(protected,indent=2),encoding='utf-8')
for p in D.rglob('*'):
 if p.is_file():
  dest=R/p.relative_to(D);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
card=R/'docs/plans/nordic-blue/tasks/TASK-009.md'
card.write_text(card.read_text(encoding='utf-8-sig').replace('Статус: TODO','Статус: IN_PROGRESS'),encoding='utf-8')
print('Installed phase A core colors; SDK/application unchanged')
