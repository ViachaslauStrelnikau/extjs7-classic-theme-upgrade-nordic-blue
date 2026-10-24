from pathlib import Path
import json, hashlib, shutil
root=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue')
out=root/'artifacts/nordic-blue/TASK-007'
out.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
protected=[root/'TestApp'/x for x in ['app.json','app.js','build.xml','workspace.json','index.html']]
protected+=list((root/'TestApp/app').rglob('*'))
protected+=[root/'TestApp/theme-lab/fixture.js',root/'artifacts/nordic-blue/TASK-004/approval.json',root/'artifacts/nordic-blue/TASK-006/baseline-manifest.json']
(out/'protected-inputs.json').write_text(json.dumps({str(p.relative_to(root)):sha(p) for p in protected if p.is_file()},indent=2),encoding='utf-8')
pkg=root/'TestApp/packages/local/theme-nordic-blue'
shutil.copytree(pkg,out/'generated-scaffold')
# Cmd-generated theme identity bootstrap is not a component override; archive it to
# keep the stricter project contract of an entirely empty overrides directory.
for p in (pkg/'overrides').iterdir():
    assert p.name in ['Readme.md','init.js']
    p.unlink()
(pkg/'resources/images').mkdir()
lab=root/'TestApp/theme-lab'
assert not (lab/'app.json').exists()
profiles=json.loads((lab/'build-profiles.json').read_text(encoding='utf-8-sig'))['builds']
config={
 'name':'NordicThemeLab','namespace':'NordicThemeLab','version':'1.0.0',
 'framework':'ext','toolkit':'classic','theme':'theme-classic',
 'id':'nordic-theme-lab-77','classpath':[],'overrides':[], 'requires':[],
 'indexHtmlPath':'build-entry.html',
 'js':[{'path':'build-requires.js','bundle':True}],
 'css':[{'path':'${build.out.css.path}','bundle':True,'exclude':['fashion']}],
 'sass':{'namespace':'','etc':[],'var':[],'src':[]},
 'fashion':{'missingParameters':'error','inliner':{'enable':False}},
 'output':{'base':'${workspace.dir}/build/theme-lab/${build.id}/${build.environment}',
           'manifest':{'embed':False,'enable':True}},
 'bootstrap':{'base':'${app.dir}/generated','manifest':'${build.id}.json',
              'microloader':'${build.id}.js','css':'${build.id}.css'},
 'cache':{'enable':False},'resources':[],
 'builds':profiles
}
(lab/'app.json').write_text(json.dumps(config,indent=2)+'\n',encoding='utf-8')
(lab/'build.xml').write_bytes((root/'TestApp/build.xml').read_bytes().replace(b'name="TestApp"',b'name="NordicThemeLab"'))
(lab/'build-entry.html').write_text('<!DOCTYPE html>\n<html><head><meta charset="utf-8"><title>Theme Lab build dependency entry</title>\n<script id="microloader" data-app="nordic-theme-lab-77" src="generated/bootstrap.js"></script></head><body></body></html>\n',encoding='utf-8')
card=root/'docs/plans/nordic-blue/tasks/TASK-007.md'
(out/'task-before.md').write_bytes(card.read_bytes())
card.write_text(card.read_text(encoding='utf-8-sig').replace('Статус: TODO','Статус: IN_PROGRESS'),encoding='utf-8')
print('Prepared isolated laboratory build descriptor; TestApp source/config unchanged')
