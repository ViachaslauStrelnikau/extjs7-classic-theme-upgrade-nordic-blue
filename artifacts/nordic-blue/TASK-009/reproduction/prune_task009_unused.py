from pathlib import Path
import json,hashlib
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');O=Path(__file__).parent/'output/task009';A=R/'artifacts/nordic-blue/TASK-009'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
policy_path=R/'config/nordic-blue-policy.json';policy=json.loads(policy_path.read_text())
css=(O/'consumption-probe.css').read_text().lower()
missing=[k for k,v in policy['allowColorOverrides'].items() if v['sentinel'].lower() not in css]
assert len(missing)==14 and all('inner-border-color' in name for name in missing)
before={str(p.relative_to(R/'TestApp/build/theme-lab/nordic/testing')).replace('\\','/'):sha(p) for p in (R/'TestApp/build/theme-lab/nordic/testing/resources').rglob('*') if p.is_file()}
(O/'before-prune-built-hashes.json').write_text(json.dumps(before,indent=2),encoding='utf-8')
files={policy['allowColorOverrides'][n]['path'] for n in missing}
for rel in files:
 p=R/policy['package']/rel;lines=p.read_text().splitlines();lines=[s for s in lines if not any(s.startswith('$'+name+':') for name in missing)]
 p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
for name in missing:del policy['allowColorOverrides'][name]
policy['notes'].append('TASK-009 compiler probe rejected 14 button inner-border color hooks not consumed by this Classic default UI. They were removed; inherited inner border colors/widths remain intact.')
policy_path.write_text(json.dumps(policy,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(O/'removed-unused-hooks.json').write_text(json.dumps({'variables':missing,'reason':'No sentinel occurrence in compiled Classic default UI. Remove overrides instead of enabling inner borders or changing their widths.'},indent=2),encoding='utf-8')
print(json.dumps({'removed':len(missing),'activeColors':len(policy['allowColorOverrides'])}))
