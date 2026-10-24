from pathlib import Path
import json,shutil
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');O=Path(__file__).parent/'output/task009';A=R/'artifacts/nordic-blue/TASK-009'
p=R/'config/nordic-blue-policy.json';policy=json.loads(p.read_text());source=R/policy['package']/'sass/var/button/Button.scss';text=source.read_text()
changes=[]
for family in ['default','toolbar']:
 name='button-'+family+'-background-color-focus-pressed';item=policy['allowColorOverrides'][name];old=item['rhs'];new='#C7DCF6'
 assert old=='$nb-control-pressed' and text.count('$'+name+': dynamic('+old+');')==1
 text=text.replace('$'+name+': dynamic('+old+');','$'+name+': dynamic('+new+');');item['target']=new;item['rhs']=new
 changes.append({'variable':name,'old':old,'new':new})
source.write_text(text,encoding='utf-8');policy['notes'].append('TASK-009 focus-pressed #C7DCF6 is a fixed component state color: 90% RGB control-pressed + 10% accent, rounded channels. It differs from pressed so SDK emits its focus-pressed rule above focus-over. Fifteen public tokens unchanged.')
p.write_text(json.dumps(policy,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(O/'focus-pressed-decision.json').write_text(json.dumps({'changes':changes,'formula':'round(0.9 * RGB(#D8E7FA) + 0.1 * RGB(#3275D6)) = RGB(199,220,246) = #C7DCF6','sdkReason':'Combined focus-pressed background is emitted only if distinct from pressed. This specific color removes the inherited focus-over cascade ambiguity. No geometry, glyph or metric change.','status':'IMPLEMENTED_PENDING_REVIEW'},indent=2),encoding='utf-8')
shutil.copy2(O/'core-state-comparison.json',O/'core-state-comparison-before-pressed-fix.json')
print('Set two exact component state colors; public palette and all geometry remain inherited')
