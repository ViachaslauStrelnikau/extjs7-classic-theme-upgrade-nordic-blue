from pathlib import Path
import json,shutil,hashlib
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');P=R/'TestApp/modern-preview';A=R/'artifacts/nordic-blue/TASK-020';V=R/'artifacts/nordic-blue/REV-002-tree-warm-v2';I=P/'icons-v2'
assert not A.exists() and not V.exists() and not I.exists();A.mkdir();V.mkdir();I.mkdir()
closed='<path d="M2.5 3.5h4l1.5 1.5h5.5v8h-11Z" fill="#FFD46A" stroke="#B98423" stroke-linejoin="round"/><path d="M3 6h10M3.5 12h9" stroke="#FFE8A4" stroke-width=".7"/>'
opened='<path d="M2.5 13V3.5h4L8 5h4.5v7.5" fill="#FFE29A" stroke="#B98423" stroke-linejoin="round"/><path d="m2.5 13 1.5-6h10l-1.5 6Z" fill="#F7C64E" stroke="#B98423" stroke-linejoin="round"/><path d="M4.5 8h8" stroke="#FFE8A4" stroke-width=".7"/>'
for name,body in [('folder',closed),('folder-open',opened),('folder-rtl','<g transform="translate(16 0) scale(-1 1)">'+closed+'</g>'),('folder-open-rtl','<g transform="translate(16 0) scale(-1 1)">'+opened+'</g>')]:
 (I/f'{name}.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">'+body+'</svg>',encoding='utf-8')
shutil.copy2(P/'icons/leaf.svg',I/'leaf.svg')
for name in ['sample-shell.css','icons.html']:
 p=P/name;(A/('before-'+name)).write_bytes(p.read_bytes());p.write_text(p.read_text(encoding='utf-8').replace("icons/","icons-v2/"),encoding='utf-8')
p=P/'review.js';s=p.read_text(encoding='utf-8');(A/'before-review.js').write_bytes(p.read_bytes());s=s.replace("h.textContent=title;","h.textContent=title+(key==='soft'?' · выбран':'');");p.write_text(s,encoding='utf-8')
p=P/'index.html';s=p.read_text(encoding='utf-8').replace('Три варианта развития темы','Nordic Soft — выбранный вариант');p.write_text(s,encoding='utf-8')
config=json.loads((R/'config/nordic-blue-icons.json').read_text(encoding='utf-8-sig'))
(A/'selection.json').write_text(json.dumps({'selectedVariant':'soft','basis':'User explicitly prefers Nordic Soft, requests squarer folders.','artworkStatus':'WAITING_USER_APPROVAL','runtimeIntegrated':False,'activeProductionManifestSha256':config['manifestSha256'],'physicalSize':[16,16],'proportions':'Closed folder silhouette narrowed from13 to11 units; top raised0.5 and bottom lowered0.5. Canvas and CSS box16×16 unchanged. Open and mirrored folders adjusted consistently. Document bytes unchanged.'},indent=2),encoding='utf-8')
print('Soft selected; new folder candidate v2 prepared')
