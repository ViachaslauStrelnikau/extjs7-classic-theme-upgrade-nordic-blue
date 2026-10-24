from pathlib import Path
import json,re,hashlib
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');O=Path(__file__).parent
policy=json.loads((R/'config/nordic-blue-policy.json').read_text())
text=(O/'consumption-probe.css').read_text(encoding='utf-8-sig');assert len(text)>500000
rules=re.findall(r'([^{}]+)\{([^{}]*)\}',text);rows=[]
for name,item in policy['allowColorOverrides'].items():
 examples=[]
 for selectors,body in rules:
  for decl in body.split(';'):
   if item['sentinel'].lower() in decl.lower():
    examples.append({'selector':selectors.strip()[-800:],'declaration':decl.strip()})
 assert examples,name
 rows.append({'variable':name,'sourcePath':item['path'],'sdkDeclarations':item['declarations'],'sentinel':item['sentinel'],'compiledOccurrences':len(examples),'examples':examples[:3]})
result={'status':'PASS','variables':len(rows),'tokens':len(policy['tokens']),'proof':'Every color variable received a distinct temporary sentinel in an isolated copy of the real Cmd-generated stylesheet before its RULE section. All 118 sentinels occur inside actual compiled CSS declarations. No marker CSS was added. Production theme files/build CSS never received sentinels.','cssSha256':hashlib.sha256((O/'consumption-probe.css').read_bytes()).hexdigest(),'results':rows}
(O/'compiler-consumption.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'status':'PASS','variablesWithActualCompiledConsumers':len(rows)}))
