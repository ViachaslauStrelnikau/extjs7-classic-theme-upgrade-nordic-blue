from pathlib import Path
import json,shutil,subprocess,os
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');A=R/'artifacts/nordic-blue/TASK-021';D=R/'TestApp/theme-acceptance/soft';assert not D.exists();D.mkdir()
for name in ['index.html','build.xml','local.properties']:shutil.copy2(R/'TestApp/theme-acceptance/nordic'/name,D/name)
app=json.loads((R/'TestApp/theme-acceptance/nordic/app.json').read_text(encoding='utf-8-sig'));app['theme']='theme-nordic-blue-soft';app['output']['base']='${workspace.dir}/build/theme-acceptance/soft/${build.environment}';(D/'app.json').write_text(json.dumps(app,indent=2),encoding='utf-8')
cmd=R/'node_modules/@sencha/cmd-windows/dist/sencha.exe';env=dict(os.environ);env['JAVA_HOME']='C:/Program Files/Java/jdk1.8.0_501';env['PATH']=env['JAVA_HOME']+'/bin;'+str(cmd.parent/'bin/windows/node')+';'+env['PATH'];rows=[]
for mode in ['testing','development','production']:
 print('real-soft-'+mode,flush=True);args=[str(cmd),'app','build',mode]
 with (A/('real-soft-'+mode+'.log')).open('w',encoding='utf-8') as f:p=subprocess.run(args,cwd=D,env=env,stdout=f,stderr=subprocess.STDOUT)
 rows.append({'mode':mode,'command':args,'cwd':'TestApp/theme-acceptance/soft','exitCode':p.returncode});(A/'real-build-commands.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
 if p.returncode:raise RuntimeError(mode+' failed')
