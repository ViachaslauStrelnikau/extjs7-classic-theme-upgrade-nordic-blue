"""Validate the separate approved contrast child; retain parent policies unchanged."""
from pathlib import Path
import hashlib,json,re,sys
R=Path(__file__).resolve().parents[1];P=R/'TestApp/packages/local/theme-nordic-blue-soft-contrast'
p=json.loads((R/'config/nordic-soft-contrast-policy.json').read_text(encoding='utf-8'));errors=[]
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
review=json.loads((R/p['decorativeReview']).read_text(encoding='utf-8'))
if sha(R/p['decorativeReview'])!=p['decorativeReviewSha256']:errors.append('Changed decorative review')
for f,h in p['reviewedFiles'].items():
 if not (R/f).is_file() or sha(R/f)!=h:errors.append('Unreviewed source '+f)
if sha(R/p['approval'])!=p['approvalSha256']:errors.append('Changed approval')
for f in P.rglob('*.scss'):
 text=f.read_text(encoding='utf-8')
 if text.strip() and f.relative_to(R).as_posix() not in p['reviewedFiles']:errors.append('Extra Sass '+str(f))
 if '/src/' in f.as_posix():
  for block in review['rules']:
   if text.count(block)!=1:errors.append('Missing/duplicate exact decorative rule')
   text=text.replace(block,'')
  props=re.findall(r'(?:^|[;{])\s*([a-z-]+)\s*:',text)
  if set(props)-set(p['approvedPaintProperties']):errors.append('Non-paint property '+str(set(props)-set(p['approvedPaintProperties'])))
 if '/var/' in f.as_posix():
  for line in text.splitlines():
   if line.strip() and not line.strip().startswith('//') and not re.fullmatch(r'\$[a-z-]+: dynamic\(#[0-9A-Fa-f]{6}\);',line):errors.append('Non-color variable '+line)
if any(f.is_file() for f in (P/'overrides').rglob('*')):errors.append('Ext override')
if any(P.rglob('*.js')):errors.append('Own runtime JS')
if any(f.is_file() and f.suffix.lower() in ['.png','.gif','.svg','.woff','.ttf'] for f in (P/'resources').rglob('*')):errors.append('Unapproved artwork/font')
s=(P/'package.json').read_text(encoding='utf-8');s=re.sub(r'("(?:\\.|[^"\\])*")|/\*[\s\S]*?\*/|//[^\r\n]*',lambda m:m[1] or '',s);meta=json.loads(s)
if meta['name']!=p['theme'] or meta['sencha']['extend']!=p['parent'] or meta['sencha']['toolkit']!='classic':errors.append('Inheritance')
print(json.dumps({'status':'FAIL' if errors else 'PASS','theme':p['theme'],'reviewedFiles':len(p['reviewedFiles']),'errors':errors},indent=2));sys.exit(bool(errors))
