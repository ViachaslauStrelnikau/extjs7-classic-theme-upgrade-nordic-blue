from pathlib import Path
import importlib.util,json,copy
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');O=Path(__file__).parent;read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
spec=importlib.util.spec_from_file_location('contracts',O/'icon-contracts.py');c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
scope={'__file__':str(O/'compare-geometry.py')};exec((O/'compare-geometry.py').read_text().split('from importlib.util')[0],scope);norm=scope['normalize']
a=read(R/'artifacts/nordic-blue/TASK-006/captures/pass-1/dpr-1/tool--normal.json');b=read(O/'nordic/captures/pass-1/dpr-1/tool--normal.json');rows=[]
def control(name,fn):
 bad=copy.deepcopy(b);fn(bad)
 try:
  bound,_=c.bind_icon_contracts(a,bad,1);rejected=norm(a['elements'])!=norm(bound['elements']) or norm(a['icons'])!=norm(bound['icons'])
 except (AssertionError,KeyError):rejected=True
 rows.append({'name':name,'expected':'REJECT','passed':rejected})
def graphic(x):return next(e for e in x['elements'] if e['id']=='tool.resize/part/tool-image')
control('icon-rect-one-pixel',lambda x:graphic(x)['rect'].__setitem__('width',16))
control('wrong-sheet-size',lambda x:graphic(x)['computed'].__setitem__('backgroundSize','60px 30px'))
control('wrong-sprite-x',lambda x:graphic(x)['computed'].__setitem__('backgroundPositionX','-14px'))
control('wrong-approved-adapter-y',lambda x:graphic(x)['computed'].__setitem__('backgroundPositionY','-15px'))
control('unapproved-image-url',lambda x:graphic(x)['computed'].__setitem__('backgroundImage','url("/unapproved/other.png")'))
control('wrong-density-sheet',lambda x:graphic(x)['computed'].__setitem__('backgroundImage',graphic(x)['computed']['backgroundImage'].replace('/images/','/images/@2x/')))
bound,_=c.bind_icon_contracts(a,b,1);rows.append({'name':'approved-contract-and-exact-metrics','expected':'ACCEPT','passed':norm(a['elements'])==norm(bound['elements']) and norm(a['icons'])==norm(bound['icons'])})
report={'status':'PASS' if all(r['passed'] for r in rows) else 'FAIL','controls':rows,'note':'Only disposable in-memory observations changed; SDK/source/assets untouched. Geometry and resource checks reject wrong sizes, offsets, URL and density.'};(O/'contract-controls.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps({'status':report['status'],'controls':len(rows)}));assert report['status']=='PASS'
