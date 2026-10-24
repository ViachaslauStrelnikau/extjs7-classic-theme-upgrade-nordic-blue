from pathlib import Path
import json,subprocess,sys,os,shutil
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');O=R/'artifacts/nordic-blue/TASK-016/browsers/firefox'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
partial=(O/'nordic/captures/pass-1/dpr-2').resolve();archive=(O/'nordic-dpr-2-readiness-diagnostic').resolve();assert partial.is_relative_to(O.resolve()) and archive.is_relative_to(O.resolve()) and not archive.exists();shutil.move(str(partial),str(archive));shutil.copy2(O/'execution.json',O/'execution-before-readiness-retry.json');shutil.copy2(O/'run-status.json',O/'run-status-before-readiness-retry.json');shutil.move(str(O/'capture-nordic-dpr-2.log'),str(O/'capture-nordic-dpr-2-initial.log'))
steps=[s for s in read(O/'execution.json') if s['exitCode']==0];env=dict(os.environ,NORDIC_CPU_RASTER='1');node='C:/Users/Damned/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe'
def run(label,command):
 print(label,flush=True)
 with (O/(label+'.log')).open('w',encoding='utf-8') as f:p=subprocess.run(command,cwd=R,env=env,stdout=f,stderr=subprocess.STDOUT)
 steps.append({'step':label,'command':command,'exitCode':p.returncode});(O/'execution.json').write_text(json.dumps(steps,indent=2),encoding='utf-8');assert p.returncode==0,label
env['NORDIC_CAPTURE_THEME']='nordic';run('capture-nordic-dpr-2',[node,str(O/'capture.cjs'),'2']);env.pop('NORDIC_CAPTURE_THEME')
for driver in ['form-review','grid-review','secondary-review','core-review','window-review']:run(driver+'-dpr-2',[node,str(O/(driver+'.cjs')),'2'])
run('compare',[sys.executable,str(O/'compare-browser.py')]);(O/'run-status.json').write_text(json.dumps({'status':'PASS','browser':read(O/'browser-config.json'),'retry':'Nordic DPR2 capture repeated from a fresh page/process after recorded readiness timeout under concurrent browser runs; no fixture/readiness/metric policy changed.'},indent=2),encoding='utf-8')
