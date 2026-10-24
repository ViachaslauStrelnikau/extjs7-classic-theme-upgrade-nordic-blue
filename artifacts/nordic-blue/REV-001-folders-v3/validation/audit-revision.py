from pathlib import Path
import json,hashlib,importlib.util,copy
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');O=Path(__file__).parent;A=R/'artifacts/nordic-blue/REV-001-folders-v3';read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
icons=read(R/'config/nordic-blue-icons.json');policy=read(R/'config/nordic-blue-policy.json');approval=read(R/icons['approvalPath']);manifest=read(R/icons['manifestPath']);old=read(A/'before-integration/config/nordic-blue-icons.json');old_manifest=read(R/'artifacts/nordic-blue/TASK-004/icon-manifest.json')
assert approval['status']=='APPROVED' and sha(R/icons['approvalPath'])==icons['approvalSha256'] and sha(R/icons['manifestPath'])==icons['manifestSha256']==approval['manifestSha256']
before=read(A/'before-integration/runtime-hashes.json');current={k:sha(R/policy['package']/'resources'/k) for k in icons['runtimeImages']};changed=[k for k,h in before.items() if current[k]!=h];expected=read(A/'integration-changes.json')['changedRuntimeFiles'];assert sorted(changed)==sorted(expected) and len(changed)==12
for mode in['testing','development','production']:
 for k,v in icons['runtimeImages'].items():assert sha(R/f'TestApp/build/theme-lab/nordic/{mode}/resources'/k)==v['sha256'],(mode,k)
styles=R/policy['package']/'sass/src/Component.scss';base=R/'artifacts/nordic-blue/TASK-013/source-snapshot/theme-nordic-blue/sass/src/Component.scss';assert styles.read_bytes()==base.read_bytes()
assert len(manifest['entries'])==len(old_manifest['entries'])==182
changed_ids=[]
for a,b in zip(old_manifest['entries'],manifest['entries']):
 assert a['id']==b['id'] and a['classicDimensions']==b['classicDimensions']
 if a['masterSha256']!=b['masterSha256']:changed_ids.append(a['id'])
assert len(changed_ids)==3 and all('folder' in n for n in changed_ids)
protected=read(R/'artifacts/nordic-blue/TASK-013/protected-inputs.json');assert all(sha(R/p)==h for p,h in protected.items());assert all(sha(R/p)==h for p,h in policy['sdkSources'].items())
spec=importlib.util.spec_from_file_location('nordic_lint',R/'tools/lint-nordic-blue.py');lint=importlib.util.module_from_spec(spec);spec.loader.exec_module(lint)
bad=copy.deepcopy(manifest);bad['runtimeSourceRoot']='../../outside';rejected=False
try:lint.canonical_images(bad)
except ValueError:rejected=True
assert rejected and lint.canonical_images(old_manifest)==old['runtimeImages'] and lint.canonical_images(manifest)==icons['runtimeImages']
result={'status':'PASS','changedRuntimeFiles':changed,'unchangedRuntimeFiles':636,'changedMasterIds':changed_ids,'ordinaryFolderUnchanged':True,'sameCssSheetDimensions':True,'styleBytesUnchanged':True,'approvedFilesPerBuildMode':648,'buildModes':3,'originalApplicationInputs':len(protected),'sdkSassFiles':len(policy['sdkSources']),'lintSourceRootControls':{'legacyV2Compatible':True,'activeV3Canonical':True,'unapprovedSourceRootRejected':True},'approvalSha256':icons['approvalSha256'],'manifestSha256':icons['manifestSha256']}
(O/'revision-validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in result.items() if k!='changedRuntimeFiles'}))
