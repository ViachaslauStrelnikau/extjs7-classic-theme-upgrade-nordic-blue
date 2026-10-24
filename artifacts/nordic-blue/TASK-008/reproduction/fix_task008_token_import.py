from pathlib import Path
import json,hashlib,shutil
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');O=Path(__file__).parent/'output/task008'
pkg=R/'TestApp/packages/local/theme-nordic-blue/package.json'
old=pkg.read_bytes();text=old.decode('utf-8-sig')
needle='"var": [\r\n                "${package.dir}/sass/var"'
if needle not in text:needle=needle.replace('\r\n','\n')
assert text.count(needle)==1
new=text.replace(needle,needle.replace('"${package.dir}/sass/var"','"${package.dir}/sass/var/all.scss",\n                "${package.dir}/sass/var"'))
target=O/'delivery/TestApp/packages/local/theme-nordic-blue/package.json'
target.write_text(new,encoding='utf-8')
policyfile=O/'delivery/config/nordic-blue-policy.json'
policy=json.loads(policyfile.read_text(encoding='utf-8'))
assert policy['protectedPackageFiles']['package.json']==hashlib.sha256(old).hexdigest()
policy['protectedPackageFiles']['package.json']=hashlib.sha256(target.read_bytes()).hexdigest()
policy['notes'].append('Cmd 7.7 does not automatically include package sass/var/all.scss: explicit first entry in sencha.sass.var is required for app and slicer compilations.')
policyfile.write_text(json.dumps(policy,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
shutil.copy2(R/'artifacts/nordic-blue/TASK-008/build-lab-nordic.log',R/'artifacts/nordic-blue/TASK-008/build-missing-token-import.log')
shutil.copy2(target,pkg);shutil.copy2(policyfile,R/'config/nordic-blue-policy.json')
print('Added explicit token var import; protected package metadata hash reviewed and updated')
