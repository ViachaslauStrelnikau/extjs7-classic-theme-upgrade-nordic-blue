from pathlib import Path
import json,hashlib,re
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue')
O=Path(__file__).parent/'output/task008';O.mkdir(exist_ok=True)
D=O/'delivery';D.mkdir(exist_ok=True)
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(rel,data):
 p=D/rel;p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(data if isinstance(data,str) else json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
palette_text=(R/'docs/plans/nordic-blue/palette.md').read_text(encoding='utf-8-sig')
tokens=dict(re.findall(r'\| (nb-[a-z-]+) \| (#[0-9A-Fa-f]{6}) \|',palette_text));assert len(tokens)==15
audit=read(R/'artifacts/nordic-blue/TASK-002/source-index.json')
old=read(R/'artifacts/nordic-blue/TASK-002/variable-policy.json')
mapping=dict(old['allowColorOverrides'])
mapping.update({'button-default-border-color-over':{'group':'Button','target':'nb-accent-hover'},'form-field-empty-color':{'group':'Form','target':'nb-muted'}})
pkg='TestApp/packages/local/theme-nordic-blue'
grouped={};allow={}
for i,(name,entry) in enumerate(mapping.items()):
 defs=audit['definitions'][name];last=defs[-1];namespace=last['path'].split('/sass/var/')[1]
 path='sass/var/'+namespace
 rhs='$'+entry['target'] if entry['target'].startswith('nb-') else entry['target']
 uses=[v for v in audit['references'][name] if not re.match(r'\s*\$'+re.escape(name)+r'\s*:',v.get('text',''))]
 assert uses,(name,'No SDK consumer')
 allow[name]={**entry,'path':path,'rhs':rhs,'declarations':defs,'consumers':uses,'sentinel':'#%06X'%(0x135701+i*211)}
 grouped.setdefault(path,[]).append('$'+name+': dynamic('+rhs+');')
write(pkg+'/sass/var/all.scss','// Nordic Blue public color tokens. Canonical PDF example names; no short aliases.\n'+'\n'.join('$'+name+': dynamic('+value+');' for name,value in tokens.items())+'\n')
for path,lines in grouped.items():write(pkg+'/'+path,'// Color assignments only. Geometry and typography are inherited from Classic.\n'+'\n'.join(lines)+'\n')
manifest_path=R/'artifacts/nordic-blue/TASK-004/icon-manifest.json'
approval=read(R/'artifacts/nordic-blue/TASK-004/approval.json')
assert approval['status']=='APPROVED' and sha(manifest_path)==approval['manifestSha256']
icons=read(manifest_path);images={}
for entry in icons['entries']:
 for density,v in entry['outputs'].items():
  for format,source_key,hash_key in [('fallback','fallback','fallbackSha256'),('preferred','preferred','sha256')]:
   source=v[source_key];rel=source.split('candidate/'+density+'x/')[1]
   if density!='1':rel=rel.replace('images/','images/@'+density+'x/',1)
   item={'id':entry['id'],'source':'artifacts/nordic-blue/TASK-004/'+source,'sha256':v[hash_key],
         'density':int(density),'bitmapDimensions':v['bitmapDimensions'],'cssBackgroundSize':v['cssBackgroundSize'],
         'classicDimensions':entry['classicDimensions'],'frameCount':v.get('frameCount',entry['frames'])}
   if rel in images:assert images[rel]['sha256']==item['sha256'],rel
   images[rel]=item
icon_policy={'approvalPath':'artifacts/nordic-blue/TASK-004/approval.json','approvalSha256':sha(R/'artifacts/nordic-blue/TASK-004/approval.json'),
 'manifestPath':'artifacts/nordic-blue/TASK-004/icon-manifest.json','manifestSha256':sha(manifest_path),
 'integrationEnabled':False,'integrationTask':'TASK-013','runtimeImages':images,
 'spriteContracts':icons['spriteContracts'],'geometryPolicy':'Byte-identical approved bitmap, exact density dimensions, unchanged CSS size/cell offsets. CSS adapters must be separately bound to approved hashes before integration; arbitrary CSS is denied.',
 'approvedGeometryAdapters':{}}
policy={'sdk':'7.7.0.31','package':pkg,'defaultAction':'DENY_UNLISTED','tokens':tokens,'allowColorOverrides':allow,
 'protectedPackageFiles':{p:sha(R/pkg/p) for p in ['package.json','build.xml','sass/config.rb']},
 'sdkSources':{v['path']:v['sha256'] for v in audit['files']},
 'denyMetricVariables':old['denyMetricOverrides'],'denyGlobalFlags':old['inheritFlagsAndGlobalVariables'],
 'denyImageVariables':old['imageAndGlyphVariablesRequireTask003MappingAndTask004Approval'],
 'reviewRequiredGradients':old['gradientsRequireComponentGeometryAndFrameReview'],
 'iconPolicy':'config/nordic-blue-icons.json','allowedReviewedScss':{},
 'notes':['Only dynamic(token/literal) assignments at exact Ext namespace paths. No selectors, imports, functions or UI mixins in theme SCSS yet.',
 'The 50 TASK-002 color hooks plus button hover border and field placeholder color consume all 15 tokens.',
 'Gradients, state completeness, frames and component visual acceptance remain TASK-009..012; images remain TASK-013.']}
write('config/nordic-blue-policy.json',policy);write('config/nordic-blue-icons.json',icon_policy)
expected={str(p.relative_to(D)).replace('\\','/'):sha(R/p.relative_to(D)) if (R/p.relative_to(D)).exists() else None for p in D.rglob('*') if p.is_file()}
(O/'source-expected.json').write_text(json.dumps(expected,indent=2),encoding='utf-8')
print(json.dumps({'tokens':len(tokens),'variables':len(allow),'namespaceFiles':len(grouped),'imageContracts':len(images),'sdkFiles':len(policy['sdkSources'])}))
