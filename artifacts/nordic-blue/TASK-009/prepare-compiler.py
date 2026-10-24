from pathlib import Path
import json,re,shutil,hashlib,os
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');O=Path(__file__).parent
old=R/'artifacts/nordic-blue/TASK-007'
for name in ['capture.cjs','extract.js','frozen-resources.json']:
 shutil.copy2(old/name,O/name)
shutil.copytree(old/'frozen-gif-frame0',O/'frozen-gif-frame0',dirs_exist_ok=True)
# The actual generated GIF bytes must still be the original Classic sources.
for key,item in json.loads((O/'frozen-resources.json').read_text()).items():
 p=R/'TestApp/build/theme-lab/nordic/testing/resources'/key
 assert hashlib.sha256(p.read_bytes()).hexdigest()==item['sourceSha256']
gen=R/'TestApp/build/temp/testing/NordicThemeLab/sass/NordicThemeLab-all.scss'
text=gen.read_text(encoding='utf-8-sig')
assert 'theme-nordic-blue/sass/var/all' in text
def absolute(m):
 value=m[2]
 if value.startswith('.'):
  target=(gen.parent/value).resolve()
  value=os.path.relpath(target,R/'artifacts/nordic-blue/TASK-009/compiler-probe').replace('\\','/')
 return '@import '+m[1]+value+m[1]+';'
text=re.sub(r'''@import\s+(['"])(.*?)\1;''',absolute,text)
policy=json.loads((R/'config/nordic-blue-policy.json').read_text(encoding='utf-8-sig'))
sentinels='\n// Isolated compiler consumption probe; never installed in the theme.\n'+'\n'.join('$'+name+': dynamic('+v['sentinel']+');' for name,v in policy['allowColorOverrides'].items())+'\n'
marker='/* ======================== RULE ======================== */'
assert marker in text
text=text.replace(marker,sentinels+'\n'+marker,1)
(O/'consumption-probe.scss').write_text(text,encoding='utf-8')
shutil.copy2(gen,O/'generated-theme.scss')
print('Prepared isolated 52-variable consumption probe and DPR capture tools')
