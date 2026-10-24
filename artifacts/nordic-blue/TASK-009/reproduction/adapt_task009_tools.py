from pathlib import Path
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');O=Path(__file__).parent/'output/task009'
s=(R/'artifacts/nordic-blue/TASK-008/compare-geometry.py').read_text()
s=s.replace('import json,re,hashlib','import json,re,hashlib,sys')
s=s.replace('color_properties=',"phase=sys.argv[1] if len(sys.argv)>1 else 'flat'\ncolor_properties=")
s=s.replace("result[k]=color_pattern.sub('<color>',normalize(v))","result[k]=('none' if phase=='flat' and k=='backgroundImage' and 'gradient(' in v and 'url(' not in v else color_pattern.sub('<color>',normalize(v)))")
s=s.replace("folder=O/f'nordic/captures/pass-1/dpr-{dpr}'","folder=O/(f'nordic/probe/dpr-{dpr}/pass-1' if phase=='phase-a' else f'nordic/captures/pass-1/dpr-{dpr}')")
s=s.replace("assert index['scenarioCount']==102","assert index['scenarioCount']==(22 if phase=='phase-a' else 102)")
s=s.replace("O/'geometry-comparison.json'","O/(phase+'-geometry.json')")
s=s.replace('gradient/shadow structure is retained.','shadow structure is retained; in flat phase the reviewed gradient-only background layers are removed, image URLs remain compared through icon observations.')
(O/'compare-geometry.py').write_text(s,encoding='utf-8')
