from pathlib import Path
import shutil
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');A=R/'artifacts/nordic-blue/TASK-016'
for d in [R/'TestApp/theme-lab',R/'TestApp/theme-acceptance/classic',R/'TestApp/theme-acceptance/nordic']:
 p=d/'local.properties';assert not p.exists();p.write_text('# Cmd development defaults skip these outputs. Acceptance must open real built pages.\n# This changes packaging only; debug/logger/development Sass defaults remain intact.\nskip.page=0\nskip.js=0\n',encoding='utf-8')
shutil.copy2(A/'development-output-commands.json',A/'development-output-cli-diagnostic.json')
shutil.copy2(A/'lab-classic-development-output.log',A/'lab-classic-development-output-cli-diagnostic.log')
