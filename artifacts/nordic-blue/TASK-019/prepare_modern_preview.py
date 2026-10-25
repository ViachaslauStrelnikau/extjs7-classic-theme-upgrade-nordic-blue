from pathlib import Path
import json,hashlib,shutil
C=Path(__file__).parent;R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');target=R/'TestApp/modern-preview';A=R/'artifacts/nordic-blue/TASK-019';V=R/'artifacts/nordic-blue/REV-002-tree-warm'
assert not target.exists() and not A.exists() and not V.exists()
shutil.copytree(C/'modern-preview-stage',target);(target/'icons').mkdir();A.mkdir();V.mkdir()
closed='<path d="M1.5 4h4.75l1.5 1.5h6.75v7h-13Z" fill="#FFD46A" stroke="#B98423" stroke-linejoin="round"/><path d="M2 6.5h12M2.5 11.5h11" stroke="#FFE8A4" stroke-width=".7"/>'
opened='<path d="M1.5 12.5V4h4.75l1.5 1.5H13V12" fill="#FFE29A" stroke="#B98423" stroke-linejoin="round"/><path d="m1.5 12.5 2-5.5h11l-2 5.5Z" fill="#F7C64E" stroke="#B98423" stroke-linejoin="round"/><path d="M4 8h9" stroke="#FFE8A4" stroke-width=".7"/>'
leaf='<path d="M4 2.5h6l2 2v9H4Z" fill="#F4F8FF" stroke="#547BAC" stroke-linejoin="round"/><path d="M10 2.5v2h2" fill="#D7E6FA" stroke="#547BAC" stroke-linejoin="round"/><path d="M5.5 6.5h5M5.5 8.5h5M5.5 10.5h3.75" stroke="#6D93C3" stroke-width=".8"/>'
for name,body in [('folder',closed),('folder-open',opened),('folder-rtl','<g transform="translate(16 0) scale(-1 1)">'+closed+'</g>'),('folder-open-rtl','<g transform="translate(16 0) scale(-1 1)">'+opened+'</g>'),('leaf',leaf)]:
 (target/'icons'/f'{name}.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">'+body+'</svg>',encoding='utf-8')
source=R/'TestApp/packages/local/theme-nordic-blue'
(A/'protected-before.json').write_text(json.dumps({p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for base in [source,R/'TestApp/theme-lab'] for p in base.rglob('*') if p.is_file() and 'generated' not in p.parts and '.sencha' not in p.parts},indent=2),encoding='utf-8')
server=(R/'tools/nordic-blue-acceptance/serve.cjs').read_text(encoding='utf-8-sig').replace("path.resolve(__dirname,'../../TestApp')","path.resolve(__dirname,'..')").replace('server.listen(51753,','server.listen(51754,')
server=server.replace("'.png':'image/png'","'.svg':'image/svg+xml','.png':'image/png'").replace("'/theme-lab/index.html';","'/modern-preview/index.html';")
server=server.replace("console.log('http://localhost:'+server.address().port+'/theme-lab/index.html?theme=classic&case=all&state=normal')","console.log('http://127.0.0.1:'+server.address().port+'/modern-preview/index.html')")
(target/'serve.cjs').write_text(server,encoding='utf-8')
print('Prepared isolated TASK-019 prototype and REV-002 artwork candidates')
