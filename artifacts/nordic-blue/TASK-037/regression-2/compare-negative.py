from pathlib import Path
import json
from metrics import compare
O=Path(__file__).parent;rows=[]
for d in [1,2]:
 p=O/'negative-controls'/('dpr-'+str(d));read=lambda n:json.loads((p/(n+'.json')).read_text())
 before=read('before')
 for name in ['shift-1px','font-size']:
  issues=compare(before,read(name));assert issues,(d,name,'not rejected')
  restored=compare(before,read(name+'-restored'));assert not restored,(d,name,'restore',restored)
  rows.append({'dpr':d,'control':name,'rejected':True,'restore':'PASS','issues':issues})
(O/'negative-results.json').write_text(json.dumps({'status':'PASS','actualBrowserMutations':rows},indent=2));print('4actual1px/font controls rejected; exact restores PASS')
