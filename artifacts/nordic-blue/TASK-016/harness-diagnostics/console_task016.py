from pathlib import Path
import shutil
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');A=(R/'artifacts/nordic-blue/TASK-016').resolve()
for name in ['native-pages','native-page-comparison.json']+[f'native-pages-{n}{ext}' for n in ['edge','chromium','firefox'] for ext in ['.json','.log']]:
 src=(A/name).resolve();dst=(A/(src.stem+'-before-console-audit'+src.suffix)).resolve()
 assert src.is_relative_to(A) and dst.is_relative_to(A) and src.exists() and not dst.exists()
 shutil.move(str(src),str(dst))
p=R/'tools/nordic-blue-acceptance/native-pages.cjs';s=p.read_text(encoding='utf-8-sig');old="page.on('pageerror',e=>errors.push(String(e)));";assert s.count(old)==1;s=s.replace(old,old+"page.on('console',m=>{if(m.type()==='error')errors.push('console: '+m.text())});page.on('requestfailed',r=>errors.push('requestfailed: '+r.url()+' '+r.failure()?.errorText));");p.write_text(s,encoding='utf-8')
print('Preserved first complete native pass; added explicit console/error and failed-request capture')
