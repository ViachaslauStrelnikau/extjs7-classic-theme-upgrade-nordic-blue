"""Validate only the separately reviewed Soft child; never relax the parent policy."""
from pathlib import Path
import json,hashlib,re,sys
R=Path(__file__).resolve().parents[1];P=R/'TestApp/packages/local/theme-nordic-blue-soft'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
policy=read(R/'config/nordic-soft-policy.json');icons=read(R/'config/nordic-soft-icons.json');errors=[]
for key,value in policy['reviewedFiles'].items():
 if not (R/key).is_file() or sha(R/key)!=value:errors.append('Unreviewed child source: '+key)
for name,expected in [('config/nordic-blue-icons.json',policy['parentIconConfigSha256']),('config/nordic-soft-icons.json',policy['softIconConfigSha256']),(policy['approvalPath'],policy['approvalSha256']),(icons['manifestPath'],icons['manifestSha256'])]:
 if sha(R/name)!=expected:errors.append('Stale config/approval: '+name)
expected={str((P/'resources'/key).resolve()):value for key,value in policy['childImages'].items()}
actual=[p for p in (P/'resources/images').rglob('*') if p.is_file()]
if set(map(str,[p.resolve() for p in actual]))!=set(expected):errors.append('Unexpected child image set')
for p in actual:
 if sha(p)!=expected.get(str(p.resolve())):errors.append('Unapproved image bytes: '+str(p))
if any(p.is_file() for p in (P/'overrides').rglob('*')):errors.append('Runtime class overrides not allowed')
if any(p.relative_to(R).as_posix() not in policy['reviewedFiles'] for p in P.rglob('*.js')):errors.append('Extra child runtime JS not allowed')
scss=[p.relative_to(R).as_posix() for p in (P/'sass').rglob('*.scss')]
if any(p not in policy['reviewedFiles'] and (R/p).read_text(encoding='utf-8-sig').strip() for p in scss):errors.append('Unreviewed Sass content')
src=(P/'package.json').read_text(encoding='utf-8-sig');src=re.sub(r'("(?:\\.|[^"\\])*")|/\*[\s\S]*?\*/|//[^\r\n]*',lambda m:m[1] or '',src);metadata=json.loads(src)
if metadata['name']!='theme-nordic-blue-soft' or metadata['sencha']['extend']!='theme-nordic-blue' or metadata['sencha']['toolkit']!='classic':errors.append('Wrong inheritance/toolkit')
result={'status':'FAIL' if errors else 'PASS','childImages':len(actual),'reviewedFiles':len(policy['reviewedFiles']),'errors':errors};print(json.dumps(result,indent=2));sys.exit(bool(errors))
