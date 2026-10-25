from pathlib import Path
import shutil,json
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');S=R/'tools/nordic-blue-regression';O=R/'artifacts/nordic-blue/TASK-021/regression';assert not O.exists();O.mkdir()
for p in S.iterdir():
 if p.is_file() and p.name not in ['run.py','report.py']:shutil.copy2(p,O/p.name)
 elif p.name in ['frozen-gif-frame0','nordic-gif-frame0']:shutil.copytree(p,O/p.name)
p=O/'icon-contracts.py';p.write_text(p.read_text(encoding='utf-8-sig').replace("config/nordic-blue-icons.json","config/nordic-soft-icons.json"),encoding='utf-8')
p=O/'metrics.py';s=p.read_text(encoding='utf-8-sig').replace("build/theme-lab/nordic/(?:testing|development|production)","build/(?:theme-lab/nordic|theme-soft)/(?:testing|development|production)");p.write_text(s,encoding='utf-8')
p=O/'capture.cjs';s=p.read_text(encoding='utf-8-sig').replace("build\\/theme-lab\\/(?:classic|nordic)\\/testing","build\\/(?:theme-lab\\/(?:classic|nordic)|theme-soft)\\/testing");p.write_text(s,encoding='utf-8')
p=O/'extract.js';s=p.read_text(encoding='utf-8-sig').replace("if('value'in el)","entry.softRadius=el.matches('.x-window')?4:el.matches('.x-btn,.x-form-text,.x-boundlist,.x-menu')?3:0;\n        if('value'in el)");p.write_text(s,encoding='utf-8')
s=(R/'tools/nordic-blue-acceptance/compare-browser.py').read_text(encoding='utf-8-sig');s=s.replace("b,seen=c.bind_icon_contracts(a,b,d);issues=compare(a,b)","""b,seen=c.bind_icon_contracts(a,b,d)
 old={x['id']:x for x in a['elements']}
 for x in b['elements']:
  radius=x.get('softRadius')
  if radius and x['id'] in old:
   for prop in ['borderTopLeftRadius','borderTopRightRadius','borderBottomLeftRadius','borderBottomRightRadius']:
    assert x['computed'][prop]==str(radius)+'px',(x['id'],prop,x['computed'][prop],radius)
    x['computed'][prop]=old[x['id']]['computed'][prop]
 issues=compare(a,b)""");s=s.replace("'baselinePolicy':","'paintException':'Only declared3px control/menu and4px window corners, checked against actual selector ownership and exact compiled values. All other metric/state/offset/font checks unchanged.', 'baselinePolicy':")
(O/'compare-browser.py').write_text(s,encoding='utf-8')
print('Prepared fresh Classic/Soft geometry/action gate with explicit radius paint exception')
