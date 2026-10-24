from pathlib import Path
import json,re,hashlib,shutil
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');O=Path(__file__).parent/'output/task009';O.mkdir(exist_ok=True);D=O/'phase-a';D.mkdir(exist_ok=True)
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
policy=read(R/'config/nordic-blue-policy.json');audit=read(R/'artifacts/nordic-blue/TASK-002/source-index.json')
extra={
 'panel-body-color':'nb-text','panel-frame-background-color':'nb-toolbar-bg','panel-header-inner-border-color':'nb-surface',
 'panel-header-focus-outline-color':'nb-accent','panel-tool-focus-outline-color':'nb-accent',
 'window-background-color':'nb-toolbar-bg','window-inner-border-color':'nb-surface','window-body-background-color':'nb-surface',
 'window-body-border-color':'nb-border','window-body-color':'nb-text',
 'toolbar-text-color':'nb-text','toolbar-footer-background-color':'nb-toolbar-bg','toolbar-separator-color':'nb-border','toolbar-separator-highlight-color':'nb-surface'
}
states=['','-over','-focus','-pressed','-focus-over','-focus-pressed','-disabled']
bg=['nb-control-bg','nb-control-hover','nb-accent-soft','nb-control-pressed','nb-control-hover','nb-control-pressed','nb-control-bg']
border=['nb-border','nb-accent-hover','nb-accent','nb-accent','nb-accent','nb-accent','nb-border']
for family in ['default','toolbar']:
 for i,state in enumerate(states):
  extra['button-'+family+'-background-color'+state]=bg[i] if family=='default' or state not in ['', '-disabled'] else 'transparent'
  extra['button-'+family+'-border-color'+state]=border[i] if family=='default' or state not in ['', '-disabled'] else 'transparent'
  extra['button-'+family+'-color'+state]='nb-text'
  extra['button-'+family+'-inner-border-color'+state]='nb-surface' if family=='default' or state not in ['', '-disabled'] else 'transparent'
 extra['button-'+family+'-body-outline-color-focus']='nb-accent'
new=[]
for name,target in extra.items():
 assert name in audit['definitions'],name
 defs=audit['definitions'][name];decl=defs[-1];path='sass/var/'+decl['path'].split('/sass/var/')[1]
 uses=[v for v in audit['references'][name] if not re.match(r'\s*\$'+re.escape(name)+r'\s*:',v.get('text',''))]
 assert uses,name
 old=policy['allowColorOverrides'].get(name,{})
 if not old:new.append(name)
 policy['allowColorOverrides'][name]={'group':'Core components TASK-009','target':target,'path':path,'rhs':'$'+target if target.startswith('nb-') else target,'declarations':defs,'consumers':uses,'sentinel':'#%06X'%(0x245701+len(policy['allowColorOverrides'])*211)}
# Reassign all sentinels uniquely for the expanded compiler proof.
for i,item in enumerate(policy['allowColorOverrides'].values()):item['sentinel']='#%06X'%(0x245701+i*211)
policy['allowGradientOverrides']={}
policy['notes'].append('TASK-009 phase A: complete default/toolbar button color states and panel/window/toolbar surfaces. Inherited gradients remain until geometry comparison passes.')
grouped={}
for name,item in policy['allowColorOverrides'].items():grouped.setdefault(item['path'],[]).append('$'+name+': dynamic('+item['rhs']+');')
for path,lines in grouped.items():
 target=D/policy['package']/path;target.parent.mkdir(parents=True,exist_ok=True)
 target.write_text('// Color-only SDK hooks; all metrics inherited from Classic.\n'+'\n'.join(lines)+'\n',encoding='utf-8')
target=D/'config/nordic-blue-policy.json';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(policy,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
expected={str(p.relative_to(D)).replace('\\','/'):sha(R/p.relative_to(D)) if (R/p.relative_to(D)).exists() else None for p in D.rglob('*') if p.is_file()}
(O/'phase-a-expected.json').write_text(json.dumps(expected,indent=2),encoding='utf-8')
(O/'new-color-hooks.json').write_text(json.dumps(new,indent=2),encoding='utf-8')
for name in ['capture.cjs','extract.js','frozen-resources.json']:
 shutil.copy2(R/'artifacts/nordic-blue/TASK-008'/name,O/name)
shutil.copytree(R/'artifacts/nordic-blue/TASK-008/frozen-gif-frame0',O/'frozen-gif-frame0',dirs_exist_ok=True)
print(json.dumps({'colorOverrides':len(policy['allowColorOverrides']),'newHooks':len(new),'files':len(grouped),'phase':'inherited gradients'}))
