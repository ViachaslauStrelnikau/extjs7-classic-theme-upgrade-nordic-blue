from pathlib import Path
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');O=Path(__file__).parent/'output/task009'
s=(R/'artifacts/nordic-blue/TASK-008/policy-controls.py').read_text()
s=s.replace("control('gradient-variable','$panel-header-background-gradient: dynamic(#123456);',expected='IMAGE_OR_GRADIENT')","control('gradient-variable','$panel-header-background-gradient: dynamic(#123456);',expected='GRADIENT_CONTRACT')")
addition='''
good,_=lint.validate_scss("$panel-header-background-gradient: dynamic('none');",'sass/var/panel/Panel.scss',policy)
rows.append({'name':'exact-reviewed-flat-gradient','expected':'ACCEPT','actualCodes':[x['code'] for x in good],'passed':not good})
control('non-reviewed-gradient',"$tab-background-gradient: dynamic('none');",'sass/var/tab/Tab.scss')
control('wrong-gradient-namespace',"$panel-header-background-gradient: dynamic('none');",'sass/var/button/Button.scss',expected='GRADIENT_CONTRACT')
control('different-gradient-enum',"$panel-header-background-gradient: dynamic('bevel');",expected='SCSS_NOT_ALLOWED')
control('none-is-not-a-color',"$panel-header-color: dynamic('none');",expected='COLOR_CONTRACT')
bad_policy=copy.deepcopy(policy);bad_policy['allowGradientOverrides']['panel-header-background-gradient']['reviewSha256']='0'*64
bad_review=lint.audit(R,R/policy['package'],bad_policy,icons)
codes=[x['code'] for x in bad_review['errors']]
rows.append({'name':'altered-gradient-review','expected':'REJECT','actualCodes':codes,'passed':'GRADIENT_REVIEW' in codes})
'''
assert "result={'status'" in s
s=s.replace("result={'status'",addition+"\nresult={'status'",1)
(O/'policy-controls.py').write_text(s,encoding='utf-8')
