from pathlib import Path
import subprocess,os,sys,json
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');O=R/'artifacts/nordic-blue/TASK-037/regression-2';node='C:/Users/Damned/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe';env=dict(os.environ,NORDIC_CPU_RASTER='1',NORDIC_LAB_URL='http://127.0.0.1:51754/contrast-lab/');steps=[]
def run(label,args):
 print(label,flush=True)
 with (O/(label+'.log')).open('w',encoding='utf-8') as f:p=subprocess.run(args,cwd=R,env=env,stdout=f,stderr=subprocess.STDOUT)
 steps.append({'step':label,'command':args,'exitCode':p.returncode});(O/'execution.json').write_text(json.dumps(steps,indent=2),encoding='utf-8')
 if p.returncode:raise RuntimeError(label+' failed')
try:
 for d in [1,2]:
  for theme in ['classic','nordic']:
   env['NORDIC_CAPTURE_THEME']=theme;run('capture-'+theme+'-dpr-'+str(d),[node,str(O/'capture.cjs'),str(d)])
  env.pop('NORDIC_CAPTURE_THEME',None)
  for driver in ['form-review','grid-review','secondary-review','core-review','window-review']:run(driver+'-dpr-'+str(d),[node,str(O/(driver+'.cjs')),str(d)])
 run('negative-controls',[node,str(O/'negative-controls.cjs')])
 run('negative-compare',[sys.executable,str(O/'compare-negative.py')])
 run('compare',[sys.executable,str(O/'compare-browser.py')]);(O/'run-status.json').write_text(json.dumps({'status':'PASS'}),encoding='utf-8')
except Exception as e:
 (O/'run-status.json').write_text(json.dumps({'status':'FAIL','error':str(e)}),encoding='utf-8');raise
