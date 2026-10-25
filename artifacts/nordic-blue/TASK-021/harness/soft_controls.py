from pathlib import Path
import json,copy,subprocess,sys
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');A=R/'artifacts/nordic-blue/TASK-021';O=A/'regression';sys.path.insert(0,str(O));read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
# Reuse the exact tested pair function, including its approved icon/radius contracts.
code=(O/'compare-browser.py').read_text(encoding='utf-8-sig').split('for d in [1,2]:')[0];ns={'__file__':str(O/'compare-browser.py')};exec(compile(code,str(O/'compare-browser.py'),'exec'),ns)
x,y=[read(O/f'{theme}/captures/pass-1/dpr-1/all--normal.json') for theme in ['classic','nordic']];checks=[]
ns['pair'](x,copy.deepcopy(y),1,'restore','reference');assert ns['rows'][-1]['status']=='PASS'
for name in ['rect+1px','font+1px','radius5px']:
 bad=copy.deepcopy(y)
 if name=='rect+1px':bad['elements'][0]['rect']['width']+=1
 elif name=='font+1px':bad['elements'][0]['computed']['fontSize']=format(float(bad['elements'][0]['computed']['fontSize'][:-2])+1,'g')+'px'
 else:next(e for e in bad['elements'] if e.get('softRadius')==3)['computed']['borderTopLeftRadius']='5px'
 rejected=False
 try:ns['pair'](x,bad,1,'negative',name);rejected=ns['rows'][-1]['status']=='FAIL'
 except AssertionError:rejected=True
 assert rejected,name;checks.append({'control':name,'rejected':True})
P=R/'TestApp/packages/local/theme-nordic-blue-soft'
for name,path,change in [('unapproved-image',P/'resources/images/tree/folder.png',lambda b:b+b'\0'),('extra-transform',P/'sass/src/Component.scss',lambda b:b+b'\n.x-btn { transform: translateX(1px); }\n')]:
 original=path.read_bytes()
 try:
  path.write_bytes(change(original));p=subprocess.run([sys.executable,str(R/'tools/lint-nordic-soft.py')],cwd=R,capture_output=True,text=True,encoding='utf-8');assert p.returncode!=0,name;checks.append({'control':name,'rejected':True,'log':p.stdout})
 finally:path.write_bytes(original)
p=subprocess.run([sys.executable,str(R/'tools/lint-nordic-soft.py')],cwd=R,capture_output=True,text=True,encoding='utf-8');assert p.returncode==0
ns['pair'](x,copy.deepcopy(y),1,'restore','final');assert ns['rows'][-1]['status']=='PASS'
(A/'negative-controls.json').write_text(json.dumps({'status':'PASS','controls':checks,'restore':'Exact source bytes and unmodified metrics restored; final lint/pair PASS. Geometry/font mutations are captured-JSON controls; asset/Sass controls modify and restore actual child sources, not built output or parent.'},indent=2),encoding='utf-8');print('5negative controls rejected; exact restore PASS')
