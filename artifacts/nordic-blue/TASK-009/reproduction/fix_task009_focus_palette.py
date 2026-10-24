from pathlib import Path
import json,shutil
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');O=Path(__file__).parent/'output/task009';A=R/'artifacts/nordic-blue/TASK-009'
p=R/'config/nordic-blue-policy.json';policy=json.loads(p.read_text());source=R/policy['package']/'sass/var/button/Button.scss';text=source.read_text()
changes=[]
for family in ['default','toolbar']:
 for suffix,target in [('-focus','nb-control-bg'),('-focus-over','nb-accent-soft')]:
  name='button-'+family+'-background-color'+suffix;item=policy['allowColorOverrides'][name];old=item['rhs'];new='$'+target
  assert text.count('$'+name+': dynamic('+old+');')==1
  text=text.replace('$'+name+': dynamic('+old+');','$'+name+': dynamic('+new+');')
  changes.append({'variable':name,'old':old,'new':new});item['target']=target;item['rhs']=new
source.write_text(text,encoding='utf-8');policy['notes'].append('TASK-009 focus palette: focus uses control-bg plus inherited dotted focus outline/accent border; focus-over uses accent-soft, distinct from hover so SDK emits its combined rule. No metric/selector override.')
p.write_text(json.dumps(policy,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(O/'focus-palette-decision.json').write_text(json.dumps({'changes':changes,'sdkReason':'theme-neutral/sass/var/button/Button.scss emits focus-over background only when it differs from over. Keyboard-mode focus has higher specificity. Fix through existing color hooks only.','status':'IMPLEMENTED_PENDING_REVIEW'},indent=2),encoding='utf-8')
shutil.copy2(O/'core-state-comparison.json',O/'core-state-comparison-before-focus-fix.json')
print('Updated four verified state colors to ensure the SDK emits distinct keyboard hover paint')
