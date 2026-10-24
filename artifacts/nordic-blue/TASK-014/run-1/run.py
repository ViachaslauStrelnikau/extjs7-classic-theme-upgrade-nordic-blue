"""Run the entire Classic/Nordic acceptance gate into a fresh output directory."""
from pathlib import Path
import argparse,subprocess,shutil,os,json,hashlib,sys,datetime
P=argparse.ArgumentParser();P.add_argument('--output',required=True);P.add_argument('--url',default='http://127.0.0.1:51752/theme-lab/');P.add_argument('--node',default='C:/Users/Damned/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe');args=P.parse_args()
S=Path(__file__).resolve().parent;R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');O=Path(args.output).resolve()
if O.exists():raise SystemExit('Output already exists. Use a fresh directory; accepted evidence is never overwritten.')
O.mkdir(parents=True)
for p in S.iterdir():
 if p.is_dir() and p.name in ['frozen-gif-frame0','nordic-gif-frame0']:shutil.copytree(p,O/p.name)
 elif p.is_file() and p.suffix in ['.py','.cjs','.js','.json']:shutil.copy2(p,O/p.name)
env=dict(os.environ,NORDIC_CPU_RASTER='1',NORDIC_LAB_URL=args.url.rstrip('/')+'/')
env.pop('NORDIC_BASELINE_RECAPTURE',None);env.pop('NORDIC_CAPTURE_THEME',None)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
protected=[R/'TestApp/theme-lab'/x for x in ['fixture.js','clock.js','index.html','app.json','profiles.json']]
protected+=list((R/'TestApp/packages/local/theme-nordic-blue').rglob('*.scss'))
protected+=list((R/'TestApp/packages/local/theme-nordic-blue/resources/images').rglob('*'))
protected=[p for p in protected if p.is_file()]
before={str(p.relative_to(R)):sha(p) for p in protected}
history=[]
def run(label,cmd):
 print(label,flush=True)
 with (O/(label+'.log')).open('w',encoding='utf-8') as log:r=subprocess.run(cmd,cwd=R,env=env,stdout=log,stderr=subprocess.STDOUT)
 history.append({'step':label,'command':list(map(str,cmd)),'exitCode':r.returncode})
 (O/'execution.json').write_text(json.dumps(history,indent=2),encoding='utf-8')
 if r.returncode:raise RuntimeError(label+' failed; see '+str(O/(label+'.log')))
try:
 run('lint',[sys.executable,str(R/'tools/lint-nordic-blue.py'),'--check-icon-candidates','--report',str(O/'lint-report.json')])
 for theme in ['classic','nordic']:
  frozen=json.loads((O/(theme+'-frozen-resources.json')).read_text(encoding='utf-8-sig'))
  for item in frozen.values():
   assert sha(R/item['source'])==item['sourceSha256']
   assert sha(O/item['derivedPng'])==item['derivedPngSha256']
 for dpr in [1,2]:
  for driver in ['capture','form-review','grid-review','secondary-review','core-review','window-review']:
   run(driver+'-dpr-'+str(dpr),[args.node,str(O/(driver+'.cjs')),str(dpr)])
 for driver in ['adapters','negative-controls']:run(driver,[args.node,str(O/(driver+'.cjs'))])
 run('compare',[sys.executable,str(O/'report.py')])
 assert all(sha(R/k)==v for k,v in before.items()),'Protected source/resource changed'
 (O/'source-guard.json').write_text(json.dumps({'status':'PASS','files':before},indent=2),encoding='utf-8')
 (O/'run-status.json').write_text(json.dumps({'status':'PASS','finished':datetime.datetime.now().isoformat(),'url':args.url,'sourceFilesChecked':len(before),'baseline':'TASK-006/pass-1','project':str(R)},indent=2),encoding='utf-8')
except Exception as e:
 (O/'run-status.json').write_text(json.dumps({'status':'FAIL','error':str(e)}),encoding='utf-8');raise
