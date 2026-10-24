from pathlib import Path
import json,hashlib
from PIL import Image
ROOT=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');OUT=Path(__file__).parent;OUT.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
catalog=json.loads((ROOT/'artifacts/nordic-blue/TASK-003/icon-manifest.json').read_text(encoding='utf8'))
frozen={}
for a in catalog['assets']:
 if a['animationFrames']<=1:continue
 source=ROOT/a['builtPath'];dest=OUT/'frozen-gif-frame0'/Path(a['logicalResourcePath']).with_suffix('.png');dest.parent.mkdir(parents=True,exist_ok=True)
 with Image.open(source) as im:im.seek(0);im.convert('RGBA').save(dest)
 frozen[a['logicalResourcePath']]={'source':source.relative_to(ROOT).as_posix(),'sourceSha256':sha(source),'frameIndex':0,'sourceFrameCount':a['animationFrames'],'dimensions':list(Image.open(dest).size),'derivedPng':dest.relative_to(OUT).as_posix(),'derivedPngSha256':sha(dest),'policy':'Browser route only; original URL and CSS/layout unchanged, first composited source GIF frame served as same-size PNG. Original source files untouched.'}
(OUT/'frozen-resources.json').write_text(json.dumps(frozen,indent=2),encoding='utf8')
inputs=json.loads((ROOT/'artifacts/nordic-blue/TASK-005/input-hashes.json').read_text(encoding='utf8'))
for folder in ['TestApp/theme-lab','ext-7.7.0.31/build/classic/theme-classic/resources']:
 for p in (ROOT/folder).rglob('*'):
  if p.is_file():inputs[p.relative_to(ROOT).as_posix()]=sha(p)
for rel in ['ext-7.7.0.31/build/ext-all-debug.js','ext-7.7.0.31/classic/theme-classic/package.json','TestApp/ext/version.properties']:
 inputs[rel]=sha(ROOT/rel)
(OUT/'input-hashes.json').write_text(json.dumps(inputs,indent=2),encoding='utf8')
fonts={}
for name in ['tahoma.ttf','tahomabd.ttf','arial.ttf','arialbd.ttf','ariali.ttf','arialbi.ttf','verdana.ttf','verdanab.ttf']:
 p=Path('C:/Windows/Fonts')/name
 if p.exists():fonts[name]={'path':str(p),'size':p.stat().st_size,'sha256':sha(p)}
(OUT/'font-files.json').write_text(json.dumps(fonts,indent=2),encoding='utf8')
print(f'Prepared {len(frozen)} frame0 resources, {len(inputs)} input hashes, {len(fonts)} font hashes')
