from pathlib import Path
import subprocess,os,json,hashlib
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');A=R/'artifacts/nordic-blue/TASK-021';cmd=R/'node_modules/@sencha/cmd-windows/dist/sencha.exe';env=dict(os.environ);env['JAVA_HOME']='C:/Program Files/Java/jdk1.8.0_501';env['PATH']=env['JAVA_HOME']+'/bin;'+str(cmd.parent/'bin/windows/node')+';'+env['PATH'];rows=[]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
css=[p for p in (R/'TestApp/build').rglob('*.css') if '/theme-soft/' in p.as_posix() or '/theme-acceptance/soft/' in p.as_posix()];before={p.relative_to(R).as_posix():sha(p) for p in css}
for scope,cwd in [('lab',R/'TestApp/soft-lab'),('real',R/'TestApp/theme-acceptance/soft')]:
 for mode in ['testing','development','production']:
  print(scope,mode,flush=True);args=[str(cmd),'app','build',mode]
  with (A/('final-build-'+scope+'-'+mode+'.log')).open('w',encoding='utf-8') as f:p=subprocess.run(args,cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT)
  rows.append({'scope':scope,'mode':mode,'command':args,'cwd':str(cwd),'exitCode':p.returncode});(A/'final-build-commands.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
  if p.returncode:raise RuntimeError('Build failed')
after={k:sha(R/k) for k in before};assert before==after,'Compiled CSS changed; recapture required'
(A/'final-build-css-stability.json').write_text(json.dumps({'status':'PASS','policy':'Final6Cmd builds include corrected optional opacity module. Compiled CSS bytes exactly match the earlier geometry capture inputs. All final module runtime checks occur after these builds.','css':after},indent=2),encoding='utf-8')
