from pathlib import Path
import json, shutil
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue'); A=(R/'artifacts/nordic-blue/TASK-016').resolve(); T=R/'tools/nordic-blue-acceptance'; C=Path(__file__).parent
def archive(src,dst):
    src=(A/src).resolve(); dst=(A/dst).resolve()
    assert src.is_relative_to(A) and dst.is_relative_to(A) and src.exists() and not dst.exists()
    shutil.move(str(src),str(dst))
archive('native-pages','native-pages-initial')
for name in ['edge','chromium','firefox']:
    archive('native-pages-'+name+'.log','native-pages-'+name+'-initial.log')
archive('browsers/firefox','browsers/firefox-157-diagnostic')
shutil.copy2(A/'browser-availability.json',A/'browser-availability-initial.json')
browsers=json.loads((A/'browser-availability.json').read_text(encoding='utf-8-sig'))
compatible=json.loads((C/'output/task016-firefox-compatible.json').read_text(encoding='utf-8-sig'))
(A/'browser-availability.json').write_text(json.dumps([compatible if b['name']=='firefox' else b for b in browsers],indent=2),encoding='utf-8')
p=T/'probe-browsers.cjs';p.write_text(p.read_text(encoding='utf-8-sig').replace('firefox-1555','firefox-1534'),encoding='utf-8')
shutil.copy2(C/'build_task016_development_pages.py',T/'build-development-pages.py')
shutil.copy2(C/'output/task016-firefox-compatible.json',A/'firefox-compatible.json')
print('Archived diagnostics; configured Firefox 152.0.4')
