"""Run visual acceptance against the reviewed immutable Nordic snapshot set."""
from pathlib import Path
import argparse,subprocess,shutil,os,json,sys,hashlib
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');S=Path(__file__).resolve().parent
P=argparse.ArgumentParser();P.add_argument('--output',required=True);P.add_argument('--url',default='http://127.0.0.1:51752/theme-lab/');P.add_argument('--node',default='C:/Users/Damned/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe');args=P.parse_args();O=Path(args.output).resolve()
if O.exists():raise SystemExit('Use a fresh output directory. Existing evidence and goldens are never overwritten.')
O.mkdir(parents=True)
for p in S.iterdir():
 if p.is_file():shutil.copy2(p,O/p.name)
 elif p.name in ['frozen-gif-frame0','nordic-gif-frame0']:shutil.copytree(p,O/p.name)
env=dict(os.environ,NORDIC_LAB_URL=args.url.rstrip('/')+'/');history=[]
def run(label,command):
 print(label,flush=True)
 with (O/(label+'.log')).open('w',encoding='utf-8') as f:r=subprocess.run(command,cwd=R,env=env,stdout=f,stderr=subprocess.STDOUT)
 history.append({'step':label,'command':list(map(str,command)),'exitCode':r.returncode});(O/'execution.json').write_text(json.dumps(history,indent=2),encoding='utf-8')
 if r.returncode:raise RuntimeError(label+' failed; see log')
try:
 run('lint',[sys.executable,str(R/'tools/lint-nordic-blue.py'),'--check-icon-candidates'])
 for theme in ['classic','nordic']:
  for asset in json.loads((O/(theme+'-frozen-resources.json')).read_text(encoding='utf-8-sig')).values():
   sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
   assert sha(R/asset['source'])==asset['sourceSha256'] and sha(O/asset['derivedPng'])==asset['derivedPngSha256']
 for d in [1,2]:run('capture-dpr-'+str(d),[args.node,str(O/'capture.cjs'),str(d)])
 run('structure',[sys.executable,str(O/'compare.py')]);run('controls',[args.node,str(O/'controls.cjs')]);run('golden',[sys.executable,str(O/'verify.py')])
 (O/'run-status.json').write_text(json.dumps({'status':'PASS','golden':'nordic-blue-visual-v1','url':args.url}),encoding='utf-8')
except Exception as e:
 (O/'run-status.json').write_text(json.dumps({'status':'FAIL','error':str(e)}),encoding='utf-8');raise
