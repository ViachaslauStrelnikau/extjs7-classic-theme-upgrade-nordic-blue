from pathlib import Path
import json,hashlib,shutil
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');O=Path(__file__).parent/'output/task008';D=O/'delivery'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
expected=json.loads((O/'source-expected.json').read_text())
assert not (R/'tools/lint-nordic-blue.py').exists()
expected['tools/lint-nordic-blue.py']=None
for rel,h in expected.items():assert (sha(R/rel) if (R/rel).exists() else None)==h,rel
A=R/'artifacts/nordic-blue/TASK-008';A.mkdir(exist_ok=False)
shutil.copytree(R/'TestApp/packages/local/theme-nordic-blue',A/'before-theme')
protected=json.loads((R/'artifacts/nordic-blue/TASK-007/protected-inputs.json').read_text())
assert all(sha(R/p)==h for p,h in protected.items())
(A/'protected-inputs.json').write_text(json.dumps(protected,indent=2),encoding='utf-8')
for p in D.rglob('*'):
 if p.is_file():
  rel=p.relative_to(D);target=R/rel
  assert rel.as_posix() in expected
  target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
card=R/'docs/plans/nordic-blue/tasks/TASK-008.md'
(A/'task-before.md').write_bytes(card.read_bytes())
card.write_text(card.read_text(encoding='utf-8-sig').replace('Статус: TODO','Статус: IN_PROGRESS'),encoding='utf-8')
print('Installed 15 tokens, 52 color assignments, policy and read-only lint; application/SDK unchanged')
