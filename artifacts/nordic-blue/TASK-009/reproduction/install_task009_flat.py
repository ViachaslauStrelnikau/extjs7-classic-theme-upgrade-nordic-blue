from pathlib import Path
import json,hashlib,shutil
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');O=Path(__file__).parent/'output/task009';D=O/'flat';A=R/'artifacts/nordic-blue/TASK-009'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
expected=json.loads((O/'flat-expected.json').read_text())
for rel,h in expected.items():assert sha(R/rel)==h,rel
for rel in ['phase-a-geometry.json','gradient-review.json']:shutil.copy2(O/rel,A/rel)
shutil.copy2(R/'TestApp/build/theme-lab/nordic/testing/resources/NordicThemeLab-all.css',A/'phase-a-built.css')
for p in D.rglob('*'):
 if p.is_file():
  dest=R/p.relative_to(D);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
print('Installed only 14 reviewed gradient changes and exact lint support')
