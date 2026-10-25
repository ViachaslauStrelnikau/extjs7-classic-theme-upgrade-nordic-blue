from pathlib import Path
import json,re,shutil,hashlib,os
from PIL import Image
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');A=R/'artifacts/nordic-blue/TASK-021';P=R/'TestApp/packages/local/theme-nordic-blue-soft';V=R/'artifacts/nordic-blue/REV-002-tree-warm-v2'
assert not A.exists();A.mkdir();(A/'generated-scaffold').mkdir()
for p in P.rglob('*'):
 if p.is_file():d=A/'generated-scaffold'/p.relative_to(P);d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d)
for p in (P/'overrides').glob('*'):p.unlink()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
write=lambda p,s:p.write_text(s,encoding='utf-8')
approved=read(V/'candidate-manifest.json')
write(A/'artwork-approval.json',json.dumps({'status':'APPROVED','version':approved['version'],'manifestSha256':sha(V/'candidate-manifest.json'),'selectedVariant':'soft','userStatement':'хорошо. продолжай','context':'Reply to shown squarer folder v2 and explicit request to approve its integration into selected Nordic Soft.','approvedDate':'2026-10-25'},ensure_ascii=False,indent=2))
protected=[p for b in [R/'TestApp/packages/local/theme-nordic-blue',R/'TestApp/theme-lab'] for p in b.rglob('*') if p.is_file() and 'generated' not in p.parts and '.sencha' not in p.parts]
write(A/'protected-before.json',json.dumps({p.relative_to(R).as_posix():sha(p) for p in protected},indent=2))
config=read(R/'config/nordic-blue-icons.json');oldManifest=R/config['manifestPath'];manifest=read(oldManifest)
for e in manifest['entries']:e['master']=os.path.relpath((oldManifest.parent/e['master']).resolve(),A).replace('\\','/')
for name in ['folder','folder-open','folder-rtl','folder-open-rtl','leaf','leaf-rtl']:
 artwork='leaf' if name=='leaf-rtl' else name
 e=next(e for e in manifest['entries'] if e['resource']=='images/tree/'+name+'.gif')
 e['master']=os.path.relpath(R/'TestApp/modern-preview/icons-v2'/f'{artwork}.svg',A).replace('\\','/');e['masterSha256']=sha(R/'TestApp/modern-preview/icons-v2'/f'{artwork}.svg')
 for density in [1,2]:
  dest=A/f'candidate/{density}x/images/tree';dest.mkdir(parents=True,exist_ok=True);png=dest/(name+'.png');gif=dest/(name+'.gif');src=R/f'TestApp/modern-preview/icons-v2/{artwork}@{density}x.png';shutil.copy2(src,png)
  im=Image.open(png).convert('RGBA');alpha=im.getchannel('A');pal=im.convert('RGB').quantize(colors=255);pal.putpalette(pal.getpalette()[:765]+[0,0,0]);pal.paste(255,mask=alpha.point(lambda v:255 if v<128 else 0));pal.save(gif,transparency=255,disposal=2,optimize=False)
  out=e['outputs'][str(density)];out.update({'preferred':png.relative_to(R/'artifacts/nordic-blue').as_posix(),'fallback':gif.relative_to(R/'artifacts/nordic-blue').as_posix(),'sha256':sha(png),'fallbackSha256':sha(gif)})
  for f in [png,gif]:
   key='images/'+('@2x/' if density==2 else '')+'tree/'+f.name;target=P/'resources'/key;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,target);item=config['runtimeImages'][key];item['source']=f.relative_to(R).as_posix();item['sha256']=sha(f)
manifest.update({'version':'nordic-soft-icons-v1','runtimeSourceRoot':'artifacts/nordic-blue','approval':{'status':'APPROVED','sourceApproval':A.relative_to(R).as_posix()+'/artwork-approval.json'},'integration':'Child Soft overrides24 tree resources; other624 runtime resources inherited unchanged from approved Nordic Blue.'})
write(A/'integrated-icon-manifest.json',json.dumps(manifest,ensure_ascii=False,indent=2));config.update({'manifestPath':(A/'integrated-icon-manifest.json').relative_to(R).as_posix(),'manifestSha256':sha(A/'integrated-icon-manifest.json'),'approvalPath':(A/'artwork-approval.json').relative_to(R).as_posix(),'approvalSha256':sha(A/'artwork-approval.json'),'integrationTask':'TASK-021'})
write(R/'config/nordic-soft-icons.json',json.dumps(config,indent=2))
(P/'sass/src').mkdir(parents=True,exist_ok=True)
css='''/* Soft paint only; geometry/typography inherited. No global runtime override. */
.x-btn,.x-form-text,.x-boundlist,.x-menu { border-radius: 3px; }
.x-window { border-radius: 4px; }
body.nb-soft-motion .x-btn,body.nb-soft-motion .x-btn-inner,body.nb-soft-motion .x-form-field,body.nb-soft-motion .x-form-trigger,body.nb-soft-motion .x-grid-cell,body.nb-soft-motion .x-tab,body.nb-soft-motion .x-tab-inner { transition-property: background-color,border-color,color; transition-duration: 120ms; transition-timing-function: ease-out; }
body.nb-soft-motion .x-btn-focus,body.nb-soft-motion .x-form-focus,body.nb-soft-motion .x-tab-focus { transition-duration: 0ms; }
.nb-soft-float { box-shadow: 0 5px 16px rgba(37,55,77,.16); }
@media (prefers-reduced-motion: reduce) { body.nb-soft-motion .x-btn,body.nb-soft-motion .x-btn-inner,body.nb-soft-motion .x-form-field,body.nb-soft-motion .x-form-trigger,body.nb-soft-motion .x-grid-cell,body.nb-soft-motion .x-tab,body.nb-soft-motion .x-tab-inner { transition-duration: 0ms; } }
'''
write(P/'sass/src/Component.scss',css)
# A separate consuming app descriptor avoids touching the accepted lab app.json.
lab=R/'TestApp/soft-lab';lab.mkdir()
for name in ['fixture.js','clock.js','lab-shell.css','loader.js','index.html','build-requires.js','build-entry.html','local.properties','build.xml']:
 if (R/'TestApp/theme-lab'/name).exists():shutil.copy2(R/'TestApp/theme-lab'/name,lab/name)
app=read(R/'TestApp/theme-lab/app.json');app.pop('builds');app['theme']='theme-nordic-blue-soft';app['output']['base']='${workspace.dir}/build/theme-soft/${build.environment}';write(lab/'app.json',json.dumps(app,indent=2))
profiles=read(R/'TestApp/theme-lab/profiles.json');profiles['script']='../theme-lab/sdk/build/ext-all-debug.js';profiles['profiles']['classic']['manifest']='../theme-lab/classic-reference.json';profiles['profiles']['nordic'].update({'manifest':'../build/theme-soft/testing/app.json','allowedThemeNames':['theme-nordic-blue-soft'],'requiredPackage':'theme-nordic-blue-soft'});write(lab/'profiles.json',json.dumps(profiles,indent=2))
# Reference Classic manifest paths are relative to its original URL and remain valid.
write(R/'docs/plans/nordic-blue/tasks/TASK-021.md','''# TASK-021: Интегрировать Nordic Soft

Статус: IN_PROGRESS. Зависимости:019/020; пользователь одобрил папкиv2 и продолжение.

Создать дочерний пакет через Cmd, интегрировать одобренные иконки с1x/2x/GIFfallback, отдельный opt-in motion API, собрать consuming app development/testing/production, проверить размеры/состояния и motion/reduction, документировать ограничения. Старую тему/approval/golden сохранить. DONE только по фактическим доказательствам; затем отдельный commit/push.
''')
print('Prepared child theme, approved artwork exports, isolated soft laboratory')
