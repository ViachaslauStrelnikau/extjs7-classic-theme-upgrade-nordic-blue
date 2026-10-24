from pathlib import Path
import shutil,sys
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');A=(R/'artifacts/nordic-blue/TASK-016').resolve();name=sys.argv[1];assert name in ['edge','chromium']
for relative in ['native-pages/'+name,'native-pages-'+name+'.log']:
 src=(A/relative).resolve();dst=src.with_name(src.name+'-concurrent-timeout')
 assert src.is_relative_to(A) and dst.is_relative_to(A) and src.exists() and not dst.exists();shutil.move(str(src),str(dst))
p=R/'tools/nordic-blue-acceptance/native-pages.cjs';s=p.read_text(encoding='utf-8-sig');old='await context.addInitScript({content:clock});'
if 'context.setDefaultTimeout(60000)' not in s:s=s.replace(old,'context.setDefaultTimeout(60000);'+old)
p.write_text(s,encoding='utf-8')
print('Preserved concurrent timeout diagnostic:',name)
