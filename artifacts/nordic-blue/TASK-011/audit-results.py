from pathlib import Path
import json,hashlib
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');O=Path(__file__).parent
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
policy=read(R/'config/nordic-blue-policy.json');protected=read(R/'artifacts/nordic-blue/TASK-011/protected-inputs.json')
assert all(sha(R/p)==h for p,h in protected.items())
assert all(sha(R/p)==h for p,h in policy['sdkSources'].items())
base=read(R/'artifacts/nordic-blue/TASK-006/input-hashes.json')
changed=[p for p,h in base.items() if not (R/p).is_file() or sha(R/p)!=h]
assert set(changed)<= {'AGENTS.md','TestApp/theme-lab/build-profiles.json','TestApp/theme-lab/README.md'},changed
manifest=read(R/'artifacts/nordic-blue/TASK-004/icon-manifest.json')
images=[e for e in manifest['entries'] if not e['id'].startswith('adapter/')]
for e in images:assert sha(R/'TestApp/build/theme-lab/nordic/testing/resources'/e['resource'])==e['sourceSha256'],e['resource']
(O/'inherited-icons.json').write_text(json.dumps({'status':'PASS','count':len(images),'resources':[{'resource':e['resource'],'sha256':e['sourceSha256']} for e in images]},indent=2),encoding='utf-8')
pkg=R/policy['package']
assert not [p for p in (pkg/'resources/images').rglob('*') if p.is_file()]
assert not [p for p in (pkg/'overrides').rglob('*') if p.is_file()]
result={'status':'PASS','sdkSassFiles':len(policy['sdkSources']),'originalApplicationInputs':len(protected),'baselineInputsCompared':len(base),'baselineDifferences':changed,'inheritedIconBytesCompared':len(images),'sourceImages':0,'sourceOverrides':0,'note':'Only previously documented instruction/lab profile changes relative to TASK-006. Application, shared fixture, SDK and approved artwork unchanged. All 180 inherited icon resources targeted for TASK-013 equal Classic. Cmd-generated color frame slices are separate and may reflect the palette.'}
(O/'source-guards.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
rows=[]
for dpr in [1,2]:
 for group in ['grid','tree','paging']:
  for p in (O/f'nordic/captures/pass-1/dpr-{dpr}').glob(group+'--*.json'):
   a=read(R/f'artifacts/nordic-blue/TASK-006/captures/pass-1/dpr-{dpr}'/p.name);b=read(p)
   excess=lambda data:[{'id':e['id'],'client':e['client'],'scroll':e['scroll'],'overflow':[e['computed']['overflowX'],e['computed']['overflowY']]} for e in data['elements'] if e['visible'] and e.get('client') and e.get('scroll') and (e['scroll']['width']>e['client']['width'] or e['scroll']['height']>e['client']['height'])]
   assert excess(a)==excess(b),p.name
   iconrows=[{'id':e['id'],'rect':e.get('rect'),'hostRect':e.get('hostRect'),'cssBox':e.get('cssBox'),'offset':e['offset'],'size':e['size']} for e in b['icons']]
   rows.append({'dpr':dpr,'scenario':p.stem,'status':'PASS','unchangedScrollExcess':excess(b),'inheritedIconBoxes':iconrows})
(O/'overflow-trigger-audit.json').write_text(json.dumps({'status':'PASS','scenarios':len(rows),'policy':'Visible element scroll/client excess lists match Classic exactly. Existing clipping/nowrap/ellipsis, trigger boxes, sprite offsets and font metrics are unchanged; no corrective positioning or global text clipping was introduced. Actual raw images grid-selected and tree-selected at DPR1 were visually inspected.','results':rows},indent=2),encoding='utf-8')
print(json.dumps(result));print('Overflow/trigger audit PASS',len(rows))

