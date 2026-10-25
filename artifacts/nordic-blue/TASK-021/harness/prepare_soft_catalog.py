from pathlib import Path
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');A=R/'artifacts/nordic-blue/TASK-021'
s=(R/'artifacts/nordic-blue/TASK-016/build-modes.cjs').read_text(encoding='utf-8-sig')
s=s.replace('config/nordic-blue-icons.json','config/nordic-soft-icons.json').replace("'TestApp/build/theme-lab/nordic'","'TestApp/build/theme-soft'")
s=s.replace('**/theme-lab/profiles.json','**/soft-lab/profiles.json').replace('TestApp/theme-lab/profiles.json','TestApp/soft-lab/profiles.json').replace('../build/theme-lab/nordic/${mode}/app.json','../build/theme-soft/${mode}/app.json')
s=s.replace('http://127.0.0.1:51752/theme-lab/index.html','http://127.0.0.1:51754/soft-lab/index.html').replace('http://127.0.0.1:51752/build/theme-lab/nordic/${mode}/resources/','http://127.0.0.1:51754/build/theme-soft/${mode}/resources/')
s=s.replace('Approved v3 folders','Approved Soft folders v2')
(A/'build-modes.cjs').write_text(s,encoding='utf-8');(A/'extract.js').write_text((A/'regression/extract.js').read_text(encoding='utf-8'),encoding='utf-8')
print('Prepared9 mode/density/fallback catalog runs using actual Soft outputs')
