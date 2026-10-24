from pathlib import Path
import json,re,shutil,hashlib
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');A=R/'artifacts/nordic-blue/TASK-016';T=R/'tools/nordic-blue-acceptance'
assert not A.exists() and not T.exists();A.mkdir();T.mkdir();(A/'before').mkdir()
for p in [R/'AGENTS.md',R/'README.md',R/'docs/plans/nordic-blue/README.md',R/'docs/plans/nordic-blue/tasks/TASK-016.md']:shutil.copy2(p,A/'before'/('plan-index.md' if p.parent.name=='nordic-blue' else p.name))
p=R/'AGENTS.md';p.write_text(p.read_text(encoding='utf-8-sig')+'''
## Commit and push each completed task

The user explicitly requests a separate commit and push after every completed task. Finish the task's required evidence and documentation, mark its card/index accurately, inspect staged files for dependencies/generated SDK output/secrets, then commit and push to origin/main. Do not wait for another permission request. Do not mark unfinished work DONE merely to commit. Preserve exact bytes through .gitattributes; keep SDK/node_modules/compiled outputs excluded. Verify the remote commit and clean working tree after each push.
''',encoding='utf-8')
p=R/'docs/plans/nordic-blue/tasks/TASK-016.md';p.write_text(p.read_text(encoding='utf-8-sig').replace('Статус: TODO','Статус: IN_PROGRESS'),encoding='utf-8')
p=R/'docs/plans/nordic-blue/README.md';p.write_text(p.read_text(encoding='utf-8-sig').replace('| 014, 015 | TODO |','| 014, 015 | IN_PROGRESS |'),encoding='utf-8')
s=(R/'TestApp/app.json').read_text(encoding='utf-8-sig');s=re.sub(r'("(?:\\.|[^"\\])*")|/\*[\s\S]*?\*/|//[^\r\n]*',lambda m:m[1] or '',s);original=json.loads(s)
for theme in ['classic','nordic']:
 d=R/'TestApp/theme-acceptance'/theme;d.mkdir(parents=True)
 a=json.loads(json.dumps(original));a['theme']='ext-theme-classic' if theme=='classic' else 'theme-nordic-blue'
 a['classpath']=['${workspace.dir}/app'];a['overrides']=['${workspace.dir}/overrides'];a['js'][1]['path']='${workspace.dir}/app.js';a['output']['base']='${workspace.dir}/build/theme-acceptance/'+theme+'/${build.environment}'
 for key in ['etc','var','src']:a['sass'][key]=['${workspace.dir}/'+v for v in a['sass'][key]]
 for key in ['var','src']:a['sass']['generated'][key]='${workspace.dir}/'+a['sass']['generated'][key]
 for e in a.get('resources',[]):
  if 'path' in e and not e['path'].startswith('${'):e['path']='${workspace.dir}/'+e['path']
 (d/'app.json').write_text(json.dumps(a,indent=2),encoding='utf-8');shutil.copy2(R/'TestApp/index.html',d/'index.html');shutil.copy2(R/'TestApp/build.xml',d/'build.xml')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
files=[R/'TestApp/app.json',R/'TestApp/app.js',R/'TestApp/index.html',R/'TestApp/workspace.json']+[p for p in (R/'TestApp/app').rglob('*') if p.is_file()]+[p for p in (R/'TestApp/packages/local/theme-nordic-blue').rglob('*') if p.is_file()]+[R/'TestApp/theme-lab'/f for f in ['app.json','fixture.js','clock.js','loader.js','profiles.json','index.html','lab-shell.css']]
(A/'protected-before.json').write_text(json.dumps({str(p.relative_to(R)).replace('\\','/'):sha(p) for p in files},indent=2),encoding='utf-8')
V=R/'artifacts/nordic-blue/REV-001-folders-v3/validation'
shutil.copy2(V/'build-modes.cjs',A/'build-modes.cjs');shutil.copy2(R/'tools/nordic-blue-regression/extract.js',A/'extract.js')
