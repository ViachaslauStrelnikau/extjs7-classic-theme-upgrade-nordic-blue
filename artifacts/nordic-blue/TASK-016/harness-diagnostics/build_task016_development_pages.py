from pathlib import Path
import subprocess,os,json
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');A=R/'artifacts/nordic-blue/TASK-016';cmd=R/'node_modules/@sencha/cmd-windows/dist/sencha.exe'
env=dict(os.environ);env['JAVA_HOME']='C:/Program Files/Java/jdk1.8.0_501';env['PATH']=env['JAVA_HOME']+'/bin;'+str(cmd.parent/'bin/windows/node')+';'+env['PATH'];rows=[]
for scope in ['lab','real']:
 for theme in ['classic','nordic']:
  cwd=R/'TestApp/theme-lab' if scope=='lab' else R/'TestApp/theme-acceptance'/theme
  args=[str(cmd),'-cwd='+str(cwd),'app','build']+(['lab-'+theme] if scope=='lab' else [])+['development'];label=scope+'-'+theme+'-development-output'
  print(label,flush=True)
  with (A/(label+'.log')).open('w',encoding='utf-8') as f:p=subprocess.run(args,cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT)
  rows.append({'label':label,'command':args,'exitCode':p.returncode});(A/'development-output-commands.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
  if p.returncode:raise RuntimeError(label+' failed')
