"""Read-only, standard-library policy audit for the Nordic Blue source package."""
from pathlib import Path
import argparse, hashlib, json, re, struct, sys

def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def digest(data):
    return hashlib.sha256(data).hexdigest()

def clean_comments(text):
    """Keep character positions/newlines; do not interpret comment markers in strings."""
    out=list(text); i=0; quote=None
    while i<len(text):
        if quote:
            if text[i]=='\\': i+=2; continue
            if text[i]==quote: quote=None
            i+=1; continue
        if text[i] in "\"'": quote=text[i]; i+=1; continue
        if text[i:i+2]=='/*':
            end=text.find('*/',i+2)
            if end<0: raise ValueError('Unterminated block comment')
            for k in range(i,end+2):
                if out[k]!='\n': out[k]=' '
            i=end+2
        elif text[i:i+2]=='//':
            end=text.find('\n',i+2)
            if end<0: end=len(text)
            for k in range(i,end): out[k]=' '
            i=end
        else: i+=1
    if quote: raise ValueError('Unterminated string')
    return ''.join(out)

def validate_scss(text,rel,policy):
    errors=[]; assignments=[]
    def fail(code,message): errors.append({'code':code,'path':rel,'message':message})
    try: cleaned=clean_comments(text)
    except ValueError as e: fail('SYNTAX',str(e)); return errors,assignments
    reviewed=policy.get('allowedReviewedScss',{}).get(rel)
    if reviewed:
        if digest(text.encode('utf-8'))!=reviewed['sha256']: fail('REVIEWED_SCSS_CHANGED','Reviewed exact stylesheet changed')
        return errors,assignments
    pattern=re.compile(r'\s*\$([a-zA-Z_][a-zA-Z0-9_-]*)\s*:\s*dynamic\(\s*(\$nb-[a-z-]+|#[0-9a-fA-F]{6}|transparent|\x27none\x27)\s*\)\s*;')
    offset=0
    while cleaned[offset:].strip():
        m=pattern.match(cleaned,offset)
        if not m:
            fail('SCSS_NOT_ALLOWED','Only explicit dynamic(color/token) assignments are allowed; no CSS, imports, functions, images, UI mixins or geometry rules. Near: '+cleaned[offset:].strip()[:100]); break
        name,value=m.group(1,2);offset=m.end()
        assignments.append((name,value))
        if name in policy['tokens']:
            if rel!='sass/var/all.scss' or value.upper()!=policy['tokens'][name].upper(): fail('TOKEN_CONTRACT','Token name/value/path differs from canonical palette: $'+name)
        elif name in policy.get('allowGradientOverrides',{}):
            item=policy['allowGradientOverrides'][name]
            if rel!=item['path'] or value!=item['rhs'] or value!="'none'": fail('GRADIENT_CONTRACT','Only exact reviewed dynamic(\'none\') at its Ext namespace path is permitted: $'+name)
        elif name in policy['denyMetricVariables'] or name in policy['denyGlobalFlags'] or name=='base-color':
            fail('METRIC_OR_GLOBAL','Inherited metric/global flag must not be overridden: $'+name)
        elif name in policy['denyImageVariables'] or name in policy['reviewRequiredGradients']:
            fail('IMAGE_OR_GRADIENT','Requires separate component/icon review: $'+name)
        elif name not in policy['allowColorOverrides']:
            fail('UNLISTED_VARIABLE','Unknown/unlisted SDK variable or token alias: $'+name)
        else:
            item=policy['allowColorOverrides'][name]
            if rel!=item['path'] or value!=item['rhs']: fail('COLOR_CONTRACT','Wrong Ext namespace file or color expression: $'+name)
    return errors,assignments

def dimensions(data):
    if data[:8]==b'\x89PNG\r\n\x1a\n' and len(data)>=24: return list(struct.unpack('>II',data[16:24]))
    if data[:6] in [b'GIF87a',b'GIF89a'] and len(data)>=10: return list(struct.unpack('<HH',data[6:10]))
    raise ValueError('Only approved PNG/GIF runtime assets are supported')

def validate_image_bytes(data,item):
    errors=[]
    try:
        if dimensions(data)!=item['bitmapDimensions']: errors.append('IMAGE_DIMENSIONS')
    except ValueError: errors.append('IMAGE_FORMAT')
    if digest(data)!=item['sha256']: errors.append('UNAPPROVED_IMAGE_BYTES')
    if item['cssBackgroundSize']!=item['classicDimensions']: errors.append('CSS_IMAGE_SIZE')
    if item['bitmapDimensions']!=[v*item['density'] for v in item['classicDimensions']]: errors.append('DENSITY_CONTRACT')
    return errors

def canonical_images(manifest):
    result={}
    for entry in manifest['entries']:
        for density,value in entry['outputs'].items():
            for source_key,hash_key in [('fallback','fallbackSha256'),('preferred','sha256')]:
                source=value[source_key];rel=source.split('candidate/'+density+'x/')[1]
                if density!='1': rel=rel.replace('images/','images/@'+density+'x/',1)
                item={'id':entry['id'],'source':'artifacts/nordic-blue/TASK-004/'+source,'sha256':value[hash_key],
                      'density':int(density),'bitmapDimensions':value['bitmapDimensions'],'cssBackgroundSize':value['cssBackgroundSize'],
                      'classicDimensions':entry['classicDimensions'],'frameCount':value.get('frameCount',entry['frames'])}
                if rel in result and result[rel]!=item:
                    # A fallback PNG and its preferred PNG may share a path.
                    if result[rel]['sha256']!=item['sha256']: raise ValueError('Conflicting image contract '+rel)
                result[rel]=item
    return result

def audit(project,package,policy,icons,check_candidates=False):
    errors=[]; assignments=[]; counts={'scssFiles':0,'tokens':0,'colorOverrides':0,'gradientOverrides':0,'images':0,'candidateImages':0,'sdkFiles':0}
    def fail(code,path,message): errors.append({'code':code,'path':str(path),'message':message})
    for rel,expected in policy['sdkSources'].items():
        path=project/rel
        if not path.is_file() or digest(path.read_bytes())!=expected: fail('SDK_CHANGED',rel,'Installed SDK source does not match audited source')
        counts['sdkFiles']+=1
    for name,item in policy.get('allowGradientOverrides',{}).items():
        try:
            evidence=project/item['reviewEvidence'];review=read_json(evidence)
            geo=project/review['geometryReport']
            if name not in policy['reviewRequiredGradients'] or item['rhs']!="'none'" or digest(evidence.read_bytes())!=item['reviewSha256'] or review['status']!='PASS' or name not in review['variables'] or digest(geo.read_bytes())!=review['geometrySha256'] or read_json(geo)['status']!='PASS':
                fail('GRADIENT_REVIEW',name,'Missing or altered geometry review for the exact gradient hook')
            for decl in item['declarations']:
                line=(project/decl['path']).read_text(encoding='utf-8-sig').splitlines()[decl['line']-1]
                if not re.search(r'^\s*\$'+re.escape(name)+r'\s*:',line): fail('SDK_DECLARATION',name,'Gradient not declared at audited SDK line')
        except (OSError,ValueError,KeyError) as e: fail('GRADIENT_REVIEW',name,str(e))
    for name,item in policy['allowColorOverrides'].items():
        if name in policy['denyMetricVariables'] or name in policy['denyGlobalFlags'] or 'color' not in name:
            fail('INVALID_ALLOWLIST',name,'Only verified color variables can enter the allowlist')
        if not item['declarations'] or not item['consumers']: fail('UNUSED_SDK_VARIABLE',name,'No audited declaration/consumer')
        for decl in item['declarations']:
            source=project/decl['path']
            if not source.is_file() or not re.search(r'^\s*\$'+re.escape(name)+r'\s*:',source.read_text(encoding='utf-8-sig').splitlines()[decl['line']-1]):
                fail('SDK_DECLARATION',name,'Declaration not found at audited SDK line')
    try:
        approval_path=project/icons['approvalPath'];manifest_path=project/icons['manifestPath']
        approval=read_json(approval_path);manifest=read_json(manifest_path)
        if digest(approval_path.read_bytes())!=icons['approvalSha256'] or digest(manifest_path.read_bytes())!=icons['manifestSha256'] or approval['manifestSha256']!=icons['manifestSha256'] or approval['status']!='APPROVED':
            fail('ICON_APPROVAL',manifest_path,'Approval/hash does not match approved v2')
        if canonical_images(manifest)!=icons['runtimeImages'] or manifest['spriteContracts']!=icons['spriteContracts']:
            fail('ICON_GEOMETRY_POLICY',icons['manifestPath'],'Image dimensions, density, sprite offsets or runtime mapping differ from approved manifest')
        if check_candidates:
            for rel,item in icons['runtimeImages'].items():
                source=project/item['source']
                found=validate_image_bytes(source.read_bytes(),item)
                for code in found: fail(code,rel,'Approved candidate validation failed')
                counts['candidateImages']+=1
            for entry in manifest['entries']:
                master=manifest_path.parent/entry['master']
                if digest(master.read_bytes())!=entry['masterSha256']: fail('ICON_MASTER_CHANGED',entry['id'],'Vector master changed after approval')
    except (OSError,ValueError,KeyError) as e: fail('ICON_POLICY',icons['manifestPath'],str(e))
    for rel,expected in policy['protectedPackageFiles'].items():
        p=package/rel
        if not p.is_file() or digest(p.read_bytes())!=expected: fail('PACKAGE_CONFIG_CHANGED',rel,'Generated build/config scaffold changed; explicit review required')
    for p in sorted(package.rglob('*')):
        rel=p.relative_to(package).as_posix()
        if p.is_symlink(): fail('SYMLINK',rel,'Package links are not permitted');continue
        if not p.is_file(): continue
        if rel.startswith('overrides/'):
            fail('JS_OVERRIDES',rel,'overrides/ must remain empty');continue
        if p.suffix.lower()=='.scss':
            found,values=validate_scss(p.read_text(encoding='utf-8-sig'),rel,policy)
            errors.extend(found);assignments.extend((k,v,rel) for k,v in values);counts['scssFiles']+=1
        elif rel.startswith('resources/images/'):
            key=rel[len('resources/'):];item=icons['runtimeImages'].get(key)
            if not item: fail('UNLISTED_IMAGE',rel,'No approved image resource contract')
            else:
                for code in validate_image_bytes(p.read_bytes(),item): fail(code,rel,'Runtime image violates approved geometry/bytes')
            if not icons['integrationEnabled']: fail('ICON_INTEGRATION_PENDING',rel,'Icon contracts are recognized; integration is reserved for TASK-013')
            counts['images']+=1
        elif rel in policy['protectedPackageFiles'] or p.suffix.lower()=='.md': pass
        else: fail('RUNTIME_FILE_NOT_ALLOWED',rel,'Only reviewed source assignments and approved image assets are permitted; no JS, CSS, SVG/font or extra runtime files')
    occurrences={}
    for name,value,rel in assignments: occurrences.setdefault(name,[]).append((value,rel))
    for name in list(policy['tokens'])+list(policy['allowColorOverrides'])+list(policy.get('allowGradientOverrides',{})):
        n=len(occurrences.get(name,[]))
        if n!=1: fail('MISSING_OR_DUPLICATE',name,'Expected exactly one assignment; found '+str(n))
    references={value[1:] for _,value,_ in assignments if value.startswith('$nb-')}
    for name in policy['tokens']:
        if name not in references: fail('UNUSED_TOKEN',name,'Token has no SDK color consumer')
    counts['tokens']=sum(name in policy['tokens'] for name,_,_ in assignments)
    counts['colorOverrides']=sum(name in policy['allowColorOverrides'] for name,_,_ in assignments)
    counts['gradientOverrides']=sum(name in policy.get('allowGradientOverrides',{}) for name,_,_ in assignments)
    return {'status':'FAIL' if errors else 'PASS','sdk':policy['sdk'],'counts':counts,
            'iconIntegrationEnabled':icons['integrationEnabled'],'errors':errors}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--package-dir',type=Path)
    parser.add_argument('--policy',type=Path);parser.add_argument('--icons-policy',type=Path)
    parser.add_argument('--check-icon-candidates',action='store_true')
    parser.add_argument('--report',type=Path)
    args=parser.parse_args();root=args.project.resolve()
    policy=read_json(args.policy or root/'config/nordic-blue-policy.json')
    icons=read_json(args.icons_policy or root/policy['iconPolicy'])
    report=audit(root,args.package_dir or root/policy['package'],policy,icons,args.check_icon_candidates)
    text=json.dumps(report,ensure_ascii=False,indent=2)
    if args.report: args.report.write_text(text+'\n',encoding='utf-8')
    print(text);return 0 if report['status']=='PASS' else 1

if __name__=='__main__': sys.exit(main())
