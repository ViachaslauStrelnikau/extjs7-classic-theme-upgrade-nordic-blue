from pathlib import Path
import json,hashlib,shutil,html,math
from PIL import Image,ImageDraw,ImageFont
from make_task004 import ROOT,OUT
plan=json.loads((OUT/'candidate-plan.json').read_text(encoding='utf8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def gif_frame(im):
 alpha=im.getchannel('A');rgb=im.convert('RGB').quantize(colors=255);rgb.putpalette(rgb.getpalette()[:765]+[0,0,0]);rgb.paste(255,mask=alpha.point(lambda v:255 if v<128 else 0));rgb.info['transparency']=255;return rgb
for e in plan['entries']:
 master=e['master'][8:-4];w,h=e['classicDimensions'];ext=Path(e['resource']).suffix
 for scale in [1,2]:
  frames=[]
  for f in range(e['frames']):
   p=OUT/f'rendered/{master}-{scale}x-{f:02}.png';im=Image.open(p).convert('RGBA');im=im.resize((w*scale,h*scale),Image.Resampling.LANCZOS);frames.append(im)
  target=OUT/f'candidate/{scale}x/{e["resource"]}';target.parent.mkdir(parents=True,exist_ok=True)
  if ext=='.gif':
   gs=[gif_frame(im) for im in frames];kw={'transparency':255,'disposal':2,'optimize':False}
   if len(gs)>1:kw.update(save_all=True,append_images=gs[1:],duration=e['frameDurationsMs'],loop=e['loop'] if e['loop'] is not None else 0)
   gs[0].save(target,**kw)
  else:frames[0].save(target)
  # PNG is a sharper optional still-image resource; GIF fallback remains at original path/format.
  png=target.with_suffix('.png');frames[0].save(png)
  preferred=png if e['frames']==1 else target
  e['outputs'][str(scale)]={'fallback':target.relative_to(OUT).as_posix(),'preferred':preferred.relative_to(OUT).as_posix(),'bitmapDimensions':[w*scale,h*scale],'cssBackgroundSize':[w,h],'sha256':sha(preferred),'fallbackSha256':sha(target),'frameCount':e['frames']}
  with Image.open(target) as check:
   assert check.size==(w*scale,h*scale)
   assert check.n_frames==e['frames'],(e['resource'],check.n_frames)
   if check.n_frames>1:
    durations=[]
    for f in range(check.n_frames):check.seek(f);durations.append(check.info.get('duration',0))
    assert durations==e['frameDurationsMs'],(e['resource'],durations,e['frameDurationsMs'])
plan.update({'approval':{'status':'WAITING_USER_APPROVAL','decision':None,'approvedAt':None},'integration':'Not integrated. Technical preview only. TASK-013 requires explicit user approval of this manifest hash.','densitySelection':'1x original-format fallback; optional @media (min-resolution:2dppx) preferred 2x resource plus explicit original sheet background-size. Never double CSS positions/boxes.','style':'See icon-style.md','baselineManifestSha256':sha(ROOT/'artifacts/nordic-blue/TASK-003/icon-manifest.json'),'spriteContracts':json.loads((ROOT/'artifacts/nordic-blue/TASK-003/sprite-contracts.json').read_text(encoding='utf8')),'componentStates':json.loads((ROOT/'artifacts/nordic-blue/TASK-003/icon-manifest.json').read_text(encoding='utf8'))['components']})
(OUT/'icon-manifest.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf8')
(OUT/'manifest.sha256').write_text(sha(OUT/'icon-manifest.json')+'  icon-manifest.json\n')
# Complete raw sheets: Classic and Nordic 1x/2x, with all cells/animation frames retained.
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',13);small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',11)
groups={}
for e in plan['entries']:groups.setdefault(e['resource'].split('/')[1],[]).append(e)
review=OUT/'review';review.mkdir(exist_ok=True)
pages=[]
for group,entries in groups.items():
 for start in range(0,len(entries),18):
  subset=entries[start:start+18];rowheights=[max(144,min(400,e['classicDimensions'][1])+36) for e in subset]
  im=Image.new('RGB',(1120,sum(rowheights)+55),'#F4F7FC');d=ImageDraw.Draw(im);d.text((18,12),f'{group} / {start+1}-{start+len(subset)} : Classic | Nordic 1x | Nordic 2x at SAME CSS size | 4x detail',font=font,fill='#25374D');yy=45
  for e,rh in zip(subset,rowheights):
   d.text((14,yy),e['resource']+'  '+str(e['classicDimensions'])+(' animated '+str(e['frames'])+' frames' if e['frames']>1 else ''),font=small,fill='#304A68')
   orig=Image.open(ROOT/e['sourcePath']).convert('RGBA');one=Image.open(OUT/e['outputs']['1']['fallback']).convert('RGBA');two=Image.open(OUT/e['outputs']['2']['preferred']).convert('RGBA').resize(one.size,Image.Resampling.LANCZOS)
   if e['id'].startswith('adapter/'):orig=orig.crop((0,0,30,15))
   for x,a in [(18,orig),(290,one),(560,two)]:im.paste(a,(x,yy+23),a)
   # Explicitly enlarged 2x SOURCE pixels, not a claim that the icon should display at this size.
   detail=Image.open(OUT/e['outputs']['2']['preferred']).convert('RGBA');dx=max(0,detail.width//2-24) if one.width==200 else 0;dy=max(0,detail.height//2-24) if one.height==72 else 0
   crop=detail.crop((dx,dy,min(dx+48,detail.width),min(dy+48,detail.height)));crop=crop.resize((crop.width*2,crop.height*2),Image.Resampling.NEAREST);im.paste(crop,(835,yy+23),crop)
   yy+=rh;d.line((12,yy-4,1105,yy-4),fill='#DCE5EF')
  filename=f'{group}-{start//18+1:02}.png';im.save(review/filename);pages.append(filename)
index='<!doctype html><meta charset="utf-8"><title>Nordic icon set v1 — review</title><style>body{font:14px Arial;background:#F4F7FC;color:#25374D;margin:24px}img{max-width:100%}a{color:#3275D6}section{margin-bottom:32px}</style><h1>Nordic Blue icons v1</h1><p>Technical preview only. Same CSS sizes. Review approval is pending. GIF fallback and 2x PNG detail are exported from editable SVG masters.</p><p><a href="../icon-manifest.json">Manifest</a> · <a href="../icon-style.md">Style and adapter notes</a> · <a href="../density-validation.json">Density results</a></p>'
index+=''.join(f'<section><h2>{html.escape(p)}</h2><a href="{p}"><img src="{p}"></a></section>' for p in pages)
index+='<h2>Runtime states</h2>'+''.join(f'<section><h3>{group}</h3><p>Classic → Nordic DPR1 → Nordic DPR2 (browser screenshot pixels)</p><a href="runtime/classic-1-{group}.png">Classic</a> · <a href="runtime/nordic-1-{group}.png">Nordic 1x</a> · <a href="runtime/nordic-2-{group}.png">Nordic 2x</a></section>' for group in ['tools','fields','checkbox-radio','buttons-paging','grid','tree','tabs-toolbars','picker-slider-menu','editor','mask','message-status-layout'])
(review/'index.html').write_text(index,encoding='utf8')
# Compact semantic overview; all source cells appear in full review above.
im=Image.new('RGB',(1120,1080),'#F4F7FC');d=ImageDraw.Draw(im);title=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',23)
d.text((26,18),'Nordic Blue · icons v1',font=title,fill='#25374D');d.text((26,52),'Vector masters · original CSS size · independent 1x / 2x exports',font=font,fill='#687B92')
d.text((26,82),'Classic     Nordic     Detail (2x master export enlarged for review)',font=font,fill='#43658B')
samples=[e for e in plan['entries'] if e['classicDimensions'][0]<=32 and e['classicDimensions'][1]<=32 and not any(s in e['resource'] for s in ['disabled','rtl','default-arrow','dd-insert','menubar','op-n'])]
samples=samples[:64]
for i,e in enumerate(samples):
 x=26+(i%4)*274;y=119+(i//4)*58
 old=Image.open(ROOT/e['sourcePath']).convert('RGBA');new=Image.open(OUT/e['outputs']['1']['preferred']).convert('RGBA');two=Image.open(OUT/e['outputs']['2']['preferred']).convert('RGBA')
 im.paste(old,(x,y),old);im.paste(new,(x+43,y),new);two=two.resize((two.width*2,two.height*2),Image.Resampling.NEAREST)
 if two.width>66 or two.height>42:two.thumbnail((66,42),Image.Resampling.NEAREST)
 im.paste(two,(x+84,y),two);d.text((x+153,y+4),Path(e['resource']).stem[:18],font=small,fill='#43658B')
im.save(review/'overview.png')
print(f'Exported {len(plan["entries"])} sheets at 1x/2x, original formats + PNG, {len(pages)} full sheet review pages. All dimensions and animation timing verified.')
