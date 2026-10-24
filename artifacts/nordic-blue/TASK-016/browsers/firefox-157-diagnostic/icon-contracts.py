from pathlib import Path
import json,re,copy
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');O=Path(__file__).parent
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
icons=read(R/'config/nordic-blue-icons.json');manifest=read(R/icons['manifestPath']);runtime=icons['runtimeImages']
origins={}
for e in manifest['entries']:
 for density,value in e['outputs'].items():
  for prop in ['fallback','preferred']:
   key=value[prop].split(f'candidate/{density}x/')[1]
   if density!='1':key=key.replace('images/','images/@'+density+'x/',1)
   origins.setdefault(key,set()).add(e['resource'])
key=lambda s:(re.search(r'(?:^|/)(images/[^?#"\s)]+)',s).group(1) if re.search(r'(?:^|/)(images/[^?#"\s)]+)',s) else None)
def adapter(identity):
 m=re.match(r'^tool\.(resize|move)(?:/|$)',identity)
 return m.group(1) if m else None
def bind_icon_contracts(a,b,dpr):
 b=copy.deepcopy(b);observations=[]
 def image_pair(old,new,identity,image_prop,size_prop,pos_prop=None):
  if image_prop not in new or image_prop not in old:return
  av,bv=old[image_prop],new[image_prop]
  aurls=av if isinstance(av,list) else re.findall(r'url\(["\x27]?([^"\x27)]+)',av)
  burls=bv if isinstance(bv,list) else re.findall(r'url\(["\x27]?([^"\x27)]+)',bv)
  if not aurls or not burls:return
  if not any(key(u) in runtime for u in burls):return
  assert len(aurls)==len(burls)==1,('unexpected image layer count',identity)
  ak,bk=key(aurls[0]),key(burls[0]);item=runtime[bk];special=adapter(identity)
  assert ak in origins[bk] or (special and ak=='images/tools/tool-sprites.gif' and item['id']=='adapter/tool-'+special),(identity,ak,bk)
  assert item['density']==dpr,(identity,'wrong density',bk,dpr)
  expected=' '.join(str(v)+'px' for v in item['cssBackgroundSize']);assert new[size_prop]==expected,(identity,'wrong CSS sheet size',new[size_prop],expected)
  # Map only an explicitly approved resource/density sheet to its verified parent.
  # Rects, hit boxes, all other dimensions and offsets remain exact comparisons.
  new[size_prop]=old[size_prop];new[image_prop]=copy.deepcopy(av)
  if special and item['id']=='adapter/tool-'+special:
   original='-360px' if special=='resize' else '-375px'
   if pos_prop:
    assert old[pos_prop]==original and new[pos_prop]=='0px',(identity,'adapter y',old[pos_prop],new[pos_prop]);new[pos_prop]=old[pos_prop]
   elif 'offset' in new:
    assert old['offset'][1]==original and new['offset'][1]=='0px',(identity,'adapter y');new['offset'][1]=old['offset'][1]
  observations.append({'id':identity,'parentResource':ak,'runtimeResource':bk,'density':item['density'],'cssSheetSize':item['cssBackgroundSize'],'adapter':special if item['id'].startswith('adapter/') else None})
 for group in ['elements','icons']:
  aa={e['id']:e for e in a[group]}
  for e in b[group]:
   if e['id'] not in aa:continue
   old=aa[e['id']]
   if group=='elements':
    image_pair(old['computed'],e['computed'],e['id'],'backgroundImage','backgroundSize','backgroundPositionY')
    original_pseudos={p['pseudo']:p for p in old.get('pseudos',[])}
    for p in e.get('pseudos',[]):
     if p['pseudo'] in original_pseudos:image_pair(original_pseudos[p['pseudo']]['computed'],p['computed'],e['id']+p['pseudo'],'backgroundImage','backgroundSize','backgroundPositionY')
   else:image_pair(old,e,e['id'],'resources','size')
 return b,observations
