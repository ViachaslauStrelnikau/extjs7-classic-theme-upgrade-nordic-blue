from pathlib import Path
import subprocess,os,json
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');A=R/'artifacts/nordic-blue/TASK-021';cmd=R/'node_modules/@sencha/cmd-windows/dist/sencha.exe'
env=dict(os.environ);env['JAVA_HOME']='C:/Program Files/Java/jdk1.8.0_501';env['PATH']=env['JAVA_HOME']+'/bin;'+str(cmd.parent/'bin/windows/node')+';'+env['PATH'];rows=[]
for mode in ['testing','development','production']:
 args=[str(cmd),'app','build',mode];print(mode,flush=True)
 with (A/('build-'+mode+'.log')).open('w',encoding='utf-8') as f:p=subprocess.run(args,cwd=R/'TestApp/soft-lab',env=env,stdout=f,stderr=subprocess.STDOUT)
 rows.append({'mode':mode,'command':args,'cwd':'TestApp/soft-lab','exitCode':p.returncode});(A/'build-commands.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
 if p.returncode:raise RuntimeError(mode+' failed')
