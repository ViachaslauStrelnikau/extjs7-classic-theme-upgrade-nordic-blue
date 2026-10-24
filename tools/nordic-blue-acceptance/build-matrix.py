from pathlib import Path
import subprocess,os,json,sys
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');A=R/'artifacts/nordic-blue/TASK-016';cmd=R/'node_modules/@sencha/cmd-windows/dist/sencha.exe'
env=dict(os.environ);env['JAVA_HOME']='C:/Program Files/Java/jdk1.8.0_501';env['PATH']=env['JAVA_HOME']+'/bin;'+str(cmd.parent/'bin/windows/node')+';'+env['PATH']
history=[]
def run(label,cwd,args):
 print(label,flush=True)
 command=[str(cmd),'-cwd='+str(cwd),*args]
 with (A/(label+'.log')).open('w',encoding='utf-8') as f:p=subprocess.run(command,cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT)
 history.append({'label':label,'command':command,'exitCode':p.returncode});(A/'build-commands.json').write_text(json.dumps(history,indent=2),encoding='utf-8')
 if p.returncode:raise RuntimeError(label+' failed')
for mode in ['testing','development','production']:
 for theme in ['classic','nordic']:run('lab-'+theme+'-'+mode,R/'TestApp/theme-lab',['app','build','lab-'+theme,mode])
 for theme in ['classic','nordic']:run('real-'+theme+'-'+mode,R/'TestApp/theme-acceptance'/theme,['app','build',mode])
run('original-app-testing',R/'TestApp',['app','build','testing'])
