from pathlib import Path
import json,hashlib
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');P=R/'TestApp/packages/local/theme-nordic-blue-soft';A=R/'artifacts/nordic-blue/TASK-021'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
icons=read(R/'config/nordic-soft-icons.json');reviewed=[P/'package.json',P/'build.xml',P/'sass/src/Component.scss',P/'resources/soft-motion.js']
images={k:v['sha256'] for k,v in icons['runtimeImages'].items() if v['source'].startswith('artifacts/nordic-blue/TASK-021/candidate/')}
policy={'version':'nordic-soft-policy-v1','parent':'theme-nordic-blue','sdk':'7.7.0.31','reviewedFiles':{p.relative_to(R).as_posix():sha(p) for p in reviewed},'childImages':images,'parentIconConfigSha256':sha(R/'config/nordic-blue-icons.json'),'softIconConfigSha256':sha(R/'config/nordic-soft-icons.json'),'approvalPath':icons['approvalPath'],'approvalSha256':icons['approvalSha256'],'paintExceptions':{'radii':{'selectors':['.x-btn','.x-form-text','.x-boundlist','.x-menu'],'value':'3px','windowValue':'4px'},'optInFloatingShadow':'0 5px 16px rgba(37,55,77,.16)','transitions':'Only background-color/border-color/color;120ms ease-out; no dimensions/transform/font transition','appearance':'Optional public-component listeners;150ms opacity .35→1; immediate hide; no Ext override; system/manual reduction'},'runtimeJsAutoIncluded':False}
(R/'config/nordic-soft-policy.json').write_text(json.dumps(policy,indent=2),encoding='utf-8')
print('Prepared exact child source/asset policy; parent policy remains unchanged')
