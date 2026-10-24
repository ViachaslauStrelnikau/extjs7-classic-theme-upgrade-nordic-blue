from pathlib import Path
import json,re,hashlib
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');O=Path(__file__).parent/'output/task009';D=O/'flat';D.mkdir(exist_ok=True)
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
geometry=read(O/'phase-a-geometry.json');assert geometry['status']=='PASS'
policy=read(R/'config/nordic-blue-policy.json');audit=read(R/'artifacts/nordic-blue/TASK-002/source-index.json')
names=['panel-header-background-gradient','toolbar-background-gradient']
names+=['button-default-background-gradient'+s for s in ['','-over','-focus','-pressed','-focus-over','-focus-pressed','-disabled']]
names+=['button-toolbar-background-gradient'+s for s in ['-over','-focus','-pressed','-focus-over','-focus-pressed']]
review={'status':'PASS','decision':'Remove only these SDK gradient layers; keep inherited frame radius, widths, padding, slicing dimensions and every metric. No new shadow.',
 'variables':names,'geometryReport':'artifacts/nordic-blue/TASK-009/phase-a-geometry.json','geometrySha256':sha(O/'phase-a-geometry.json'),
 'comparison':'22 scenarios including overview at each DPR; 2738 element comparisons, zero geometry/typography/overflow differences before flattening.',
 'finalAcceptance':'TASK-009 may be DONE only after the flattened build, exact geometry comparison and visual state checks also pass.'}
(O/'gradient-review.json').write_text(json.dumps(review,indent=2),encoding='utf-8')
for name in names:
 defs=audit['definitions'][name];path='sass/var/'+defs[-1]['path'].split('/sass/var/')[1]
 if name not in policy['reviewRequiredGradients']:policy['reviewRequiredGradients'].append(name)
 policy['allowGradientOverrides'][name]={'path':path,'rhs':"'none'",'declarations':defs,
  'consumers':[v for v in audit['references'][name] if not re.match(r'\s*\$'+re.escape(name)+r'\s*:',v.get('text',''))],
  'reviewEvidence':'artifacts/nordic-blue/TASK-009/gradient-review.json','reviewSha256':sha(O/'gradient-review.json')}
grouped={}
for name,item in policy['allowColorOverrides'].items():grouped.setdefault(item['path'],[]).append('$'+name+': dynamic('+item['rhs']+');')
for name,item in policy['allowGradientOverrides'].items():grouped.setdefault(item['path'],[]).append('$'+name+': dynamic('+item['rhs']+');')
for rel,lines in grouped.items():
 p=D/policy['package']/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('// SDK color hooks and specifically reviewed flat gradients; metrics inherited.\n'+'\n'.join(lines)+'\n',encoding='utf-8')
policy['notes'].append('TASK-009: 14 explicit none gradient assignments admitted only after phase-A geometry review; no other gradient or arbitrary SCSS permission.')
p=D/'config/nordic-blue-policy.json';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(policy,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
s=(R/'artifacts/nordic-blue/TASK-009/before/tools/lint-nordic-blue.py').read_text(encoding='utf-8-sig')
s=s.replace("|transparent)\\s*\\)","|transparent|\\x27none\\x27)\\s*\\)")
assert 'transparent|\\x27none\\x27' in s
needle="        elif name in policy['denyMetricVariables']"
addition="""        elif name in policy.get('allowGradientOverrides',{}):
            item=policy['allowGradientOverrides'][name]
            if rel!=item['path'] or value!=item['rhs'] or value!="'none'": fail('GRADIENT_CONTRACT','Only exact reviewed dynamic(\\'none\\') at its Ext namespace path is permitted: $'+name)
"""
assert needle in s;s=s.replace(needle,addition+needle,1)
s=s.replace("'colorOverrides':0,'images'","'colorOverrides':0,'gradientOverrides':0,'images'")
needle="    for name,item in policy['allowColorOverrides'].items():"
addition="""    for name,item in policy.get('allowGradientOverrides',{}).items():
        try:
            evidence=project/item['reviewEvidence'];review=read_json(evidence)
            geo=project/review['geometryReport']
            if name not in policy['reviewRequiredGradients'] or item['rhs']!="'none'" or digest(evidence.read_bytes())!=item['reviewSha256'] or review['status']!='PASS' or name not in review['variables'] or digest(geo.read_bytes())!=review['geometrySha256'] or read_json(geo)['status']!='PASS':
                fail('GRADIENT_REVIEW',name,'Missing or altered geometry review for the exact gradient hook')
            for decl in item['declarations']:
                line=(project/decl['path']).read_text(encoding='utf-8-sig').splitlines()[decl['line']-1]
                if not re.search(r'^\\s*\\$'+re.escape(name)+r'\\s*:',line): fail('SDK_DECLARATION',name,'Gradient not declared at audited SDK line')
        except (OSError,ValueError,KeyError) as e: fail('GRADIENT_REVIEW',name,str(e))
"""
assert needle in s;s=s.replace(needle,addition+needle,1)
s=s.replace("list(policy['allowColorOverrides']):","list(policy['allowColorOverrides'])+list(policy.get('allowGradientOverrides',{})):")
s=s.replace("    return {'status':'FAIL' if errors else 'PASS'","    counts['gradientOverrides']=sum(name in policy.get('allowGradientOverrides',{}) for name,_,_ in assignments)\n    return {'status':'FAIL' if errors else 'PASS'")
p=D/'tools/lint-nordic-blue.py';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
expected={str(p.relative_to(D)).replace('\\','/'):sha(R/p.relative_to(D)) for p in D.rglob('*') if p.is_file()}
(O/'flat-expected.json').write_text(json.dumps(expected,indent=2),encoding='utf-8')
print(json.dumps({'colors':len(policy['allowColorOverrides']),'reviewedFlatGradients':len(names)}))
