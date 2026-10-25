from pathlib import Path
import json,re,hashlib,sys
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');O=Path(__file__).parent
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
phase='flat'
probe='--probe' in sys.argv
color_properties={'color','backgroundColor','borderTopColor','borderRightColor','borderBottomColor','borderLeftColor','outlineColor'}
color_pattern=re.compile(r'rgba?\([^)]*\)|#[0-9a-fA-F]{3,8}\b')
def normalize(value):
 if isinstance(value,str):return re.sub(r'(?:http://127\.0\.0\.1:\d+)?/(?:theme-lab/sdk/build/classic/theme-classic|build/(?:theme-lab/nordic|theme-contrast)/(?:testing|development|production))/resources/', '/CLASSIC-RESOURCES/',value)
 if isinstance(value,list):return [normalize(x) for x in value]
 if isinstance(value,dict):
  result={}
  for k,v in value.items():
   if k in color_properties:continue
   if k in ['backgroundImage','boxShadow']:
    result[k]=('none' if phase=='flat' and k=='backgroundImage' and 'gradient(' in v and 'url(' not in v else color_pattern.sub('<color>',normalize(v)))
   else:result[k]=normalize(v)
  return result
 return value

KEYS=['case','state','fixtureSemanticCount','elementCount','visibleElementCount','duplicates','unownedGraphics','elements','icons','activeElement','scroll','data','stores','errors']
def compare(a,b):
 issues=[]
 for doc in [a,b]:
  for group in ['elements','icons']:
   ids=[e['id'] for e in doc[group]]
   if len(ids)!=len(set(ids)):issues.append('duplicate-'+group)
  if not doc['elements'] or not doc['elementCount'] or doc['elementCount']!=len(doc['elements']):issues.append('empty/count')
  if doc['duplicates'] or doc['errors']:issues.append('capture-errors')
 for k in KEYS:
  if normalize(a[k])!=normalize(b[k]):issues.append(k)
 ae=dict(a['environment']);be=dict(b['environment']);ae.pop('profile');be.pop('profile')
 if ae!=be:issues.append('environment')
 return issues
