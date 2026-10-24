from pathlib import Path
import shutil,json,hashlib
r=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue')
b=r/'artifacts/nordic-blue/TASK-006'
out=Path('output/task007');out.mkdir(exist_ok=True)
for name in ['extract.js','frozen-resources.json']:
 shutil.copy2(b/name,out/name)
shutil.copytree(b/'frozen-gif-frame0',out/'frozen-gif-frame0',dirs_exist_ok=True)
# Only substitute a copied Classic GIF after checking the actual generated build
# bytes against the accepted source hash. Future icon replacement must fail here.
frozen=json.loads((out/'frozen-resources.json').read_text())
for profile in ['classic','nordic']:
 for key,asset in frozen.items():
  p=r/f'TestApp/build/theme-lab/{profile}/testing/resources'/key
  assert hashlib.sha256(p.read_bytes()).hexdigest()==asset['sourceSha256'],str(p)
s=(b/'capture.cjs').read_text()
s=s.replace("const dpr=Number(process.argv[2]||1)","const theme=process.env.NORDIC_CAPTURE_THEME||'nordic';\nconst dpr=Number(process.argv[2]||1)")
s=s.replace("const out=__dirname,root=", "const out=__dirname,root=")
s=s.replace("path.join(out,only.length?", "path.join(out,theme,only.length?")
s=s.replace("theme:'classic',case:name,state", "theme,case:name,state")
s=s.replace("new URL(url).pathname.includes('/sdk/build/classic/theme-classic/resources/')", "(/\\/(?:sdk\\/build\\/classic\\/theme-classic|build\\/theme-lab\\/(?:classic|nordic)\\/testing)\\/resources\\//.test(new URL(url).pathname))")
s=s.replace("const summary={dpr,pass,", "const summary={theme,dpr,pass,")
(out/'capture.cjs').write_text(s,encoding='utf-8')
print(out)
