from pathlib import Path
import importlib.util,json,copy,struct
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');O=Path(__file__).parent
spec=importlib.util.spec_from_file_location('nordic_lint',R/'tools/lint-nordic-blue.py');lint=importlib.util.module_from_spec(spec);spec.loader.exec_module(lint)
policy=lint.read_json(R/'config/nordic-blue-policy.json');icons=lint.read_json(R/policy['iconPolicy'])
rows=[]
def control(name,text,path='sass/var/panel/Panel.scss',expected=None):
 errors,_=lint.validate_scss(text,path,policy);codes=[x['code'] for x in errors]
 ok=bool(errors) and (expected is None or expected in codes)
 rows.append({'name':name,'expected':'REJECT','actualCodes':codes,'passed':ok})
control('metric-padding','$panel-header-padding: dynamic(#123456);',expected='METRIC_OR_GLOBAL')
control('metric-font-size','$font-size: dynamic(#123456);',expected='METRIC_OR_GLOBAL')
control('metric-radius','$panel-border-radius: dynamic(#123456);',expected='METRIC_OR_GLOBAL')
control('realistic-font-size','$font-size: dynamic(13px);',expected='SCSS_NOT_ALLOWED')
control('realistic-header-padding','$panel-header-padding: dynamic(8px);',expected='SCSS_NOT_ALLOWED')
control('global-base-color','$base-color: dynamic(#123456);',expected='METRIC_OR_GLOBAL')
control('image-variable','$tool-background-image: dynamic(#123456);')
control('gradient-variable','$panel-header-background-gradient: dynamic(#123456);',expected='GRADIENT_CONTRACT')
control('unknown-sdk-variable','$panel-magical-color: dynamic($nb-surface);',expected='UNLISTED_VARIABLE')
control('short-token-alias','$nb-header: dynamic(#E8EFF8);','sass/var/all.scss',expected='UNLISTED_VARIABLE')
control('wrong-namespace','$panel-header-color: dynamic($nb-heading);','sass/var/button/Button.scss',expected='COLOR_CONTRACT')
control('unlisted-color-expression','$panel-header-color: dynamic($nb-accent);',expected='COLOR_CONTRACT')
control('literal-css-width','.x-panel { width: 800px; }',expected='SCSS_NOT_ALLOWED')
control('literal-css-image-position','.x-tool { background-position: 0 -18px; }',expected='SCSS_NOT_ALLOWED')
control('literal-css-hidpi-size','.x-tool { background-size: 60px 720px; }',expected='SCSS_NOT_ALLOWED')
control('ui-mixin',"@include extjs-panel-ui($ui: 'nordic');",expected='SCSS_NOT_ALLOWED')
control('hidden-import',"/* safe? */ @import 'another-file';",expected='SCSS_NOT_ALLOWED')
control('function-call',"$panel-header-color: dynamic(adjust-color($nb-heading,$lightness:1%));",expected='SCSS_NOT_ALLOWED')
control('unterminated-comment','/* $panel-header-color: dynamic($nb-heading);',expected='SYNTAX')
good,assignments=lint.validate_scss('// valid\n$panel-header-color: dynamic($nb-heading);','sass/var/panel/Panel.scss',policy)
rows.append({'name':'allow-listed-color','expected':'ACCEPT','actualCodes':[x['code'] for x in good],'passed':not good and len(assignments)==1})
item=next(v for v in icons['runtimeImages'].values() if v['density']==1 and v['source'].endswith('.png'))
data=(R/item['source']).read_bytes();valid=lint.validate_image_bytes(data,item)
rows.append({'name':'approved-icon-1x-contract','expected':'ACCEPT_CONTRACT_ONLY','actualCodes':valid,'passed':not valid})
item2=next(v for v in icons['runtimeImages'].values() if v['density']==2 and v['source'].endswith('.png'))
valid2=lint.validate_image_bytes((R/item2['source']).read_bytes(),item2)
rows.append({'name':'approved-icon-2x-unchanged-css-size','expected':'ACCEPT_CONTRACT_ONLY','actualCodes':valid2,'passed':not valid2})
changed=bytearray(data);changed[16:20]=struct.pack('>I',item['bitmapDimensions'][0]+1)
codes=lint.validate_image_bytes(changed,item)
rows.append({'name':'resized-runtime-icon','expected':'REJECT','actualCodes':codes,'passed':'IMAGE_DIMENSIONS' in codes and 'UNAPPROVED_IMAGE_BYTES' in codes})
changed_item=copy.deepcopy(item2);changed_item['cssBackgroundSize']=[v*2 for v in item2['classicDimensions']]
codes=lint.validate_image_bytes((R/item2['source']).read_bytes(),changed_item)
rows.append({'name':'doubled-physical-css-size','expected':'REJECT','actualCodes':codes,'passed':'CSS_IMAGE_SIZE' in codes})
changed_icons=copy.deepcopy(icons);changed_icons['spriteContracts']['formTrigger']['cssWidthPx']=18
report=lint.audit(R,R/policy['package'],policy,changed_icons)
codes=[x['code'] for x in report['errors']]
rows.append({'name':'sprite-contract-changed','expected':'REJECT','actualCodes':codes,'passed':'ICON_GEOMETRY_POLICY' in codes})
# Full-package checks operate on disposable copies of only the small child package.
import shutil
base=O/'control-package';shutil.copytree(R/policy['package'],base,dirs_exist_ok=True)
def package_control(name,rel,payload,expected):
 p=base/rel;p.parent.mkdir(parents=True,exist_ok=True)
 prior=p.read_bytes() if p.exists() else None;p.write_bytes(payload)
 try:report=lint.audit(R,base,policy,icons);codes=[x['code'] for x in report['errors']]
 finally:
  if prior is None:p.unlink()
  else:p.write_bytes(prior)
 rows.append({'name':name,'expected':'REJECT','actualCodes':codes,'passed':expected in codes})
package_control('new-js-override','overrides/Panel.js',b"Ext.define('NB.Panel',{override:'Ext.panel.Panel'});",'JS_OVERRIDES')
package_control('new-icon-font','resources/nordic.woff',b'font','RUNTIME_FILE_NOT_ALLOWED')
package_control('unlisted-image','resources/images/unreviewed.png',data,'UNLISTED_IMAGE')
enabled_icons=icons;icons=copy.deepcopy(icons);icons['integrationEnabled']=False
package_control('integration-before-task-013','resources/'+next(k for k,v in icons['runtimeImages'].items() if v==item),data,'ICON_INTEGRATION_PENDING')
icons=enabled_icons
original=(base/'sass/var/panel/Panel.scss').read_bytes()
package_control('duplicate-sdk-assignment','sass/var/panel/Panel.scss',original+b'\n$panel-header-color: dynamic($nb-heading);\n','MISSING_OR_DUPLICATE')
package_control('missing-sdk-assignment','sass/var/panel/Panel.scss',b'','MISSING_OR_DUPLICATE')
package_control('changed-generated-package-config','package.json',b'{}','PACKAGE_CONFIG_CHANGED')
full=lint.audit(R,R/policy['package'],policy,icons,True)
rows.append({'name':'real-package-and-complete-approved-candidates','expected':'ACCEPT','actualCodes':[x['code'] for x in full['errors']],'passed':full['status']=='PASS'})

good,_=lint.validate_scss("$panel-header-background-gradient: dynamic('none');",'sass/var/panel/Panel.scss',policy)
rows.append({'name':'exact-reviewed-flat-gradient','expected':'ACCEPT','actualCodes':[x['code'] for x in good],'passed':not good})
control('non-reviewed-gradient',"$grid-cell-special-background-gradient: dynamic('none');",'sass/var/view/Table.scss')
control('wrong-gradient-namespace',"$panel-header-background-gradient: dynamic('none');",'sass/var/button/Button.scss',expected='GRADIENT_CONTRACT')
control('different-gradient-enum',"$panel-header-background-gradient: dynamic('bevel');",expected='SCSS_NOT_ALLOWED')
control('none-is-not-a-color',"$panel-header-color: dynamic('none');",expected='COLOR_CONTRACT')
bad_policy=copy.deepcopy(policy);bad_policy['allowGradientOverrides']['panel-header-background-gradient']['reviewSha256']='0'*64
bad_review=lint.audit(R,R/policy['package'],bad_policy,icons)
codes=[x['code'] for x in bad_review['errors']]
rows.append({'name':'altered-gradient-review','expected':'REJECT','actualCodes':codes,'passed':'GRADIENT_REVIEW' in codes})

reviewed=(R/policy['package']/'sass/src/Component.scss').read_text(encoding='utf-8-sig')
for name,changed in [('icon-sheet-size',reviewed.replace('background-size: 10px 10px','background-size: 20px 20px',1)),('icon-add-width',reviewed+'\n.x-tool{width:30px;}'),('icon-media-density',reviewed.replace('192dpi','96dpi')),('icon-adapter-offset',reviewed.replace('background-position-y: 0px','background-position-y: -15px',1))]:
 control(name,changed,'sass/src/Component.scss','REVIEWED_SCSS_CHANGED')
control('icon-css-wrong-namespace',reviewed,'sass/src/IconBad.scss','SCSS_NOT_ALLOWED')
ok,_=lint.validate_scss(reviewed,'sass/src/Component.scss',policy);rows.append({'name':'exact-reviewed-icon-css','expected':'ACCEPT','actualCodes':[x['code'] for x in ok],'passed':not ok})
result={'status':'PASS' if all(x['passed'] for x in rows) else 'FAIL','controls':rows,'realPackage':full,'note':'All mutations are in strings or a disposable copy of the child package; application/SDK/approved artwork are untouched. TASK-013 enables only exact approved assets and SHA-bound resource CSS. Disabling integration still rejects every installed image.'}
(O/'policy-controls.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'status':result['status'],'controls':len(rows),'failures':[x for x in rows if not x['passed']]}))
if result['status']!='PASS':raise SystemExit(1)
