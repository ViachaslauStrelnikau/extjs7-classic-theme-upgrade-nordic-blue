from pathlib import Path
import subprocess,os,json,hashlib
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');A=R/'artifacts/nordic-blue/TASK-041';cmd=R/'node_modules/@sencha/cmd-windows/dist/sencha.exe';env=dict(os.environ);env['JAVA_HOME']='C:/Program Files/Java/jdk1.8.0_501';env['PATH']=env['JAVA_HOME']+'/bin;'+str(cmd.parent/'bin/windows/node')+';'+env['PATH'];rows=[]
inputs=[R/'TestApp/packages/local/theme-nordic-blue-soft-contrast/sass/src/Component.scss',R/'TestApp/packages/local/theme-nordic-blue-soft-contrast/sass/var/grid/header/Container.scss',R/'TestApp/packages/local/theme-nordic-blue/sass/src/Component.scss',R/'TestApp/packages/local/theme-nordic-blue/package.json',R/'TestApp/packages/local/theme-nordic-blue-soft-contrast/package.json'];inputs+=list((R/'TestApp/packages/local/theme-nordic-blue/resources/images').rglob('elbow-line*'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before={str(p):sha(p) for p in inputs}
for scope,folder in [('lab','TestApp/contrast-lab'),('real','TestApp/theme-acceptance/contrast')]:
 for mode in ['testing','development','production']:
  print('Release build',scope,mode,flush=True)
  with (A/('final-build-'+scope+'-'+mode+'.log')).open('w',encoding='utf-8') as f:p=subprocess.run([str(cmd),'app','build',mode],cwd=R/folder,env=env,stdout=f,stderr=subprocess.STDOUT)
  rows.append({'scope':scope,'mode':mode,'cwd':folder,'command':[str(cmd),'app','build',mode],'exitCode':p.returncode});(A/'final-build-commands.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
  if p.returncode:raise RuntimeError('Build failed')
assert before=={str(p):sha(p) for p in inputs};(A/'final-build-inputs.json').write_text(json.dumps(before,indent=2),encoding='utf-8');print('All release builds complete',flush=True)
