from pathlib import Path
import json
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');A=R/'artifacts/nordic-blue/TASK-021'
version=json.loads((A/'modes-motion-results.json').read_text())['browser']
(A/'browser-availability.json').write_text(json.dumps([{'name':'edge','status':'AVAILABLE','version':version,'launchOptions':{'headless':True,'channel':'msedge','args':['--disable-gpu','--force-color-profile=srgb']}}],indent=2),encoding='utf-8')
s=(R/'tools/nordic-blue-acceptance/native-pages.cjs').read_text(encoding='utf-8-sig').replace('artifacts/nordic-blue/TASK-016','artifacts/nordic-blue/TASK-021').replace("'http://127.0.0.1:51753/'","'http://127.0.0.1:51754/'").replace("path.join(R,'tools/nordic-blue-regression/extract.js')","path.join(A,'regression/extract.js')")
old="'build/'+(scope==='lab'?'theme-lab':'theme-acceptance')+'/'+theme+'/'+mode+'/'"
new="'build/'+(theme==='nordic'?(scope==='lab'?'theme-soft/':'theme-acceptance/soft/'):(scope==='lab'?'theme-lab/classic/':'theme-acceptance/classic/'))+mode+'/'"
assert old in s;s=s.replace(old,new).replace("manifest.packages['theme-nordic-blue']","manifest.packages['theme-nordic-blue-soft']")
s=s.replace("if(ids.has(id))duplicates.push(id);","e.softRadius=el.matches('.x-window')?4:el.matches('.x-btn,.x-form-text,.x-boundlist,.x-menu')?3:0;if(ids.has(id))duplicates.push(id);")
(A/'native-pages.cjs').write_text(s,encoding='utf-8')
print('Prepared actual-output Classic/Soft native page driver')
