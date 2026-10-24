from pathlib import Path
import json,hashlib,math,html,re
from PIL import Image
ROOT=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue')
OUT=Path(__file__).parent
OUT.mkdir(parents=True,exist_ok=True)
BASE=json.loads((ROOT/'artifacts/nordic-blue/TASK-003/icon-manifest.json').read_text(encoding='utf8'))
BLUE='#3275D6'; INK='#43658B'; BORDER='#B7C8DC'; SOFT='#E3EDFC'
def path(d,fill='none',stroke='currentColor',sw=1.25):return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>'
def rect(x,y,w,h,fill='none',stroke='currentColor',r=0):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1"/>'
def circle(x,y,r,fill='none',stroke='currentColor'):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>'
def glyph(name):
 if name in ['right','left','up','down']:
  return {'right':path('M6 3.5 10.5 8 6 12.5'),'left':path('M10 3.5 5.5 8 10 12.5'),'up':path('M3.5 10 8 5.5 12.5 10'),'down':path('M3.5 6 8 10.5 12.5 6')}[name]
 if name in ['next','prev','first','last']:
  d='right' if name in ['next','last'] else 'left';s=glyph(d)
  if name in ['first','last']:s+=path('M12 4v8' if name=='last' else 'M4 4v8')
  return s
 if name in ['more','more-left']:return glyph('right' if name=='more' else 'left')+f'<g transform="translate({-4 if name=="more" else 4} 0)">{glyph("right" if name=="more" else "left")}</g>'
 if name in ['close','clear','remove-cross']:return path('M4.5 4.5 11.5 11.5M11.5 4.5 4.5 11.5')
 if name in ['plus','minus','toggle-up','toggle-down','expand','collapse']:
  return glyph('up' if name in ['toggle-up','collapse'] else 'down') if name not in ['plus','minus'] else path('M3.5 8h9'+('M8 3.5v9' if name=='plus' else ''))
 if name=='minimize':return path('M3.5 11.5h9')
 if name=='maximize':return rect(3.5,3.5,9,9)+path('M3.5 6h9')
 if name=='restore':return path('M5.5 3.5h7v7M3.5 5.5h7v7h-7z')
 if name=='search':return circle(6.8,6.8,3.7)+path('m9.5 9.5 3.1 3.1')
 if name=='calendar':return rect(2.5,3.5,11,10,SOFT)+path('M2.5 6.5h11M5 2.5v3M11 2.5v3M5 9h1M9 9h1M5 11h1')
 if name=='gear':
  # Eight regular teeth and a true punched-out hub: a cog, not an irregular flower.
  pts=[]
  for i in range(8):
   for da,r in [(-22.5,5.0),(-13,5.0),(-13,6.8),(13,6.8),(13,5.0),(22.5,5.0)]:
    a=math.radians(i*45+da);pts.append((8+math.cos(a)*r,8+math.sin(a)*r))
  d='M'+' L'.join(f'{x:.3f} {y:.3f}' for x,y in pts)+' Z M10.4 8a2.4 2.4 0 1 0-4.8 0a2.4 2.4 0 1 0 4.8 0Z'
  return f'<path d="{d}" fill="currentColor" fill-rule="evenodd"/>'
 if name=='refresh':return path('M12.5 6A4.8 4.8 0 0 0 4 4.5L2.5 6M2.5 3v3h3M3.5 10A4.8 4.8 0 0 0 12 11.5l1.5-1.5M13.5 13v-3h-3')
 if name in ['pin','unpin']:return path('m6 2.5 6 3-2 1 .3 3-2 2-2.3-2L3 9l1.3-3L4 4zM6 10l-3 3')+(path('M2 2l12 12',sw=1) if name=='unpin' else '')
 if name=='save':return path('M3 2.5h9l1.5 1.5v9.5h-11v-11z')+rect(5,2.5,5.5,4,SOFT)+rect(5,9,6,4.5,SOFT)
 if name=='print':return rect(2.5,6,11,6,SOFT)+rect(5,2.5,6,4,'white')+rect(5,10,6,3.5,'white')+path('M11 8h.5')
 if name in ['help','question','info','error','warning','exclamation','no','yes','drop-add']:
  s=path('M8 2 14 13H2z',SOFT) if name=='warning' else circle(8,8,6,SOFT)
  s+= {'help':path('M5.8 5.5C6 2.8 11.5 3.5 10 6.5L8 8v1.5M8 12h.01'), 'question':path('M5.8 5.5C6 2.8 11.5 3.5 10 6.5L8 8v1.5M8 12h.01'),'info':path('M8 7v5M8 4h.01'),'error':glyph('close'),'warning':path('M8 6v3.5M8 11.5h.01'),'exclamation':path('M8 4.5v5M8 12h.01'),'no':path('m4 12 8-8'),'yes':path('m4.5 8 2.5 2.5 4.5-5'),'drop-add':glyph('plus')}[name]
  return s
 if name=='resize':return path('M3.5 12.5 12.5 3.5M8 3.5h4.5V8M3.5 8v4.5H8')
 if name=='move':return path('M8 2v12M2 8h12M5.5 4.5 8 2l2.5 2.5M5.5 11.5 8 14l2.5-2.5M4.5 5.5 2 8l2.5 2.5M11.5 5.5 14 8l-2.5 2.5')
 if name in ['folder','folder-open']:return path('M2 4h5l1.5 1.5H14v7H2z',SOFT)+(path('M2 7h12l-2 5.5H2z',SOFT) if name=='folder-open' else '')
 if name=='leaf':return path('M4 2.5h5l3 3v8H4z',SOFT)+path('M9 2.5v3h3M6 8h4M6 10.5h4')
 if name in ['lock','unlock']:return rect(3.5,7,9,6.5,SOFT)+path('M5 7V5a3 3 0 0 1 6 0'+('' if name=='unlock' else 'v2'))+circle(8,10,0.7,BLUE,'none')
 if name=='group-clear':return path('M4 4 12 12M12 4 4 12',sw=2.25)
 if name in ['group','columns','summary','groups']:return rect(2.5,3,11,10,SOFT)+path('M2.5 6h11M6 3v10M9.5 3v10'+('M2.5 9.5h11' if name in ['group','groups','summary'] else ''))
 if name in ['asc','desc']:return path('M4 3h6M4 6h4M4 9h2M11.5 3v10M9 10.5l2.5 2.5 2.5-2.5' if name=='desc' else 'M4 3h2M4 6h4M4 9h6M11.5 13V3M9 5.5 11.5 3 14 5.5')
 if name.startswith('op-'):
  op=name[3:]; base={'eq':'M4 6h8M4 10h8','identical':'M4 4h8M4 8h8M4 12h8','gt':'M5 3l7 5-7 5','lt':'M11 3 4 8l7 5','gte':'M5 2l7 4-7 4M4 13h9','lte':'M11 2 4 6l7 4M3 13h9','in':'M4 4h5a4 4 0 0 1 0 8H4','like':'M2.5 9C5 1 10 15 13.5 7','empty':'M3.5 12.5 12.5 3.5','exists':'M4 3h8v10H4M5 8h7','fn':'M3 12h2l2-9h4M4 7h6M10 9l4 4M14 9l-4 4'}
  neg=op in ['neq','nidentical','nin','nlike']; key={'neq':'eq','nidentical':'identical','nin':'in','nlike':'like'}.get(op,op)
  return (circle(8,8,5) if key=='empty' else '')+path(base[key])+(path('M3 14 13 2',sw=1) if neg else '')
 if name in ['bold','italic','underline','increasefontsize','decreasefontsize','forecolor','backcolor']:
  if name=='bold':return path('M4.5 3h4a2.5 2.5 0 0 1 0 5h-4m0 0h4.5a2.5 2.5 0 0 1 0 5h-4.5zM4.5 3v10',sw=1.7)
  if name=='italic':return path('M7 3h5M4 13h5M9.5 3l-3 10')
  if name=='underline':return path('M4 3v5a4 4 0 0 0 8 0V3M3 14h10')
  return path('M3 11 7 2l4 9M4.5 8h5')+(path('M11 3h4M13 1v4') if name=='increasefontsize' else path('M11 3h4') if name=='decreasefontsize' else path('M2 14h12',sw=2.3))
 if name in ['insertorderedlist','insertunorderedlist']:return path('M6 4h8M6 8h8M6 12h8M2 3v2M2 8h1l-1 2h1M2 12h1v2H2' if name=='insertorderedlist' else 'M6 4h8M6 8h8M6 12h8M2 4h.2M2 8h.2M2 12h.2')
 if name in ['justifyleft','justifycenter','justifyright']:return path({'justifyleft':'M2 3h12M2 6h8M2 9h12M2 12h8','justifycenter':'M2 3h12M4 6h8M2 9h12M4 12h8','justifyright':'M2 3h12M6 6h8M2 9h12M6 12h8'}[name])
 if name=='sourceedit':return path('M5 4 1.5 8 5 12M11 4l3.5 4-3.5 4M9 2 7 14')
 if name=='createlink':return path('m6 10-1 1a2.8 2.8 0 0 1-4-4l3-3a2.8 2.8 0 0 1 4 0M10 6l1-1a2.8 2.8 0 0 1 4 4l-3 3a2.8 2.8 0 0 1-4 0M5.5 10.5l5-5')
 raise ValueError('No glyph '+name)
def put(name,x,y,w,h,color=INK):
 art=glyph(name)
 # Keep tiny chevrons/plus signs readable in the binary-alpha GIF fallback.
 scale=min(w,h)/16
 art=re.sub(r'stroke-width="([0-9.]+)"',lambda m:f'stroke-width="{max(float(m[1]),.85/scale):.3f}"',art)
 return f'<g color="{color}" transform="translate({x} {y}) scale({w/16} {h/16})">{art}</g>'
def svg(w,h,s):return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{s}</svg>'
def bg(x,y,w,h,i=0):return rect(x+.5,y+.5,w-1,h-1,['#F4F7FC','#E3EDF9','#D8E7FA','#EDF3F9','#E3EDF9','#EDF3F9'][i%6],BORDER)
TOOLS=['close','minimize','maximize','restore','toggle-up','toggle-down','gear','prev','next','pin','unpin','right','left','down','up','refresh','plus','minus','search','save','help','print','expand','collapse']
EDITOR=['bold','italic','underline','increasefontsize','decreasefontsize','insertorderedlist','insertunorderedlist','justifyleft','justifycenter','justifyright','forecolor','backcolor','sourceedit','createlink']
entries=[];jobs=[];skips=[]
def add(master,asset,body,frames=None,notes=''):
 w,h=asset['bitmapDimensions'].values(); dest=OUT/'masters'/master;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(svg(w,h,body),encoding='utf8')
 e={'id':asset['semanticId'],'resource':asset['logicalResourcePath'],'sourcePath':asset['sourcePath'],'sourceSha256':asset['sourceSha256'],'classicDimensions':[w,h],'master':'masters/'+master,'frames':asset['animationFrames'],'notes':notes,'runtimeSamples':asset['runtimeSamples'],'outputs':{}}
 if frames is None:frames=[body]
 for f,b in enumerate(frames):
  fp=dest if f==0 else dest.with_name(dest.stem+f'-frame-{f:02}.svg');fp.write_text(svg(w,h,b),encoding='utf8')
  for scale in [1,2]:
   target=f'rendered/{master[:-4]}-{scale}x-{f:02}.png';jobs.append({'source':str(fp.resolve()),'target':str((OUT/target).resolve()),'width':w*scale,'height':h*scale})
 e['frameDurationsMs']=[]
 with Image.open(ROOT/asset['sourcePath']) as im:
  e['loop']=im.info.get('loop');
  for f in range(im.n_frames if hasattr(im,'n_frames') else 1):im.seek(f);e['frameDurationsMs'].append(im.info.get('duration',0))
 entries.append(e)
for a in BASE['assets']:
 if a['decision']!='replace':continue
 rel=a['logicalResourcePath'][7:];w,h=a['bitmapDimensions'].values(); n=Path(rel).stem;body='';frames=None;note=''
 if rel in ['slider/slider-bg.png','slider/slider-v-bg.png','window/toast/fader.png']:
  skips.append({'resource':a['logicalResourcePath'],'decision':'inherit','reason':'Corrected TASK-003 classification: track/background paint, not a symbol. Preserve parent framing/repeat behavior; color treatment belongs to later component work.'});continue
 if rel=='tools/tool-sprites.gif':
  for y,g in enumerate(TOOLS):
   for x,c in enumerate([INK,BLUE]):body+=put(g,x*15,y*15,15,15,c)
 elif rel.startswith('editor/'):
  body=''.join(put(g,i*16,0,16,16) for i,g in enumerate(EDITOR))
 elif rel.startswith('form/') and ('trigger' in n or 'spinner' in n):
  ch=h//2 if 'spinner' in n else 24;g='calendar' if 'date-' in n else 'search' if 'search-' in n else 'close' if 'clear-' in n else 'down'
  for x in range(6):
   body+=bg(x*17,0,17,ch,x)
   body+=put('up' if 'spinner' in n else g,x*17+2,0 if 'spinner' in n else 3,13,ch if 'spinner' in n else 16,BLUE if x in [1,2,4] else INK)
   if 'spinner' in n:body+=bg(x*17,ch,17,ch,x)+put('down',x*17+2,ch,13,ch)
  note='Original 17px state columns retained; legacy trigger 240px canvas padding stays transparent.'
 elif rel in ['form/checkbox.gif','form/radio.gif']:
  for y in range(h//13):
   for x in range(4):
    col='#92A1B3' if x==3 or y==2 else BLUE if x in [1,2] else INK;fill=SOFT if y else 'white'
    if 'radio' in n:body+=f'<g color="{col}">'+circle(x*13+6.5,y*13+6.5,5,fill)+(circle(x*13+6.5,y*13+6.5,2.4,col,'none') if y else '')+'</g>'
    else:
     checked=y>0;frame='#A7B5C6' if x==3 or y==2 else BLUE if x in [1,2] or checked else INK
     body+=f'<rect x="{x*13+1.5}" y="{y*13+1.5}" width="10" height="10" rx="1" fill="{frame if checked else "white"}" stroke="{frame}" stroke-width="1.25"/>'
     if checked:body+=f'<g transform="translate({x*13} {y*13})">'+path('M3.7 6.5 5.7 8.7 9.4 4.3',stroke='white',sw=1.55)+'</g>'
 elif rel=='form/tag-field-item-close.gif':
  body=''.join(put('close',x*11,y*11,11,11,BLUE if x==1 else INK) for x in range(3) for y in range(2))
 elif rel.startswith('slider/'):
  cw,ch=(15,14) if '-v-' in n else (14,15)
  for i in range(6):
   x,y=i*cw,i*ch;body+=rect(x+1.5,y+1.5,cw-3,ch-3,SOFT,BLUE if i else BORDER,2)
   body+=f'<g color="{BLUE}">'+path(f'M{x+5} {y+5}v{ch-10}M{x+8} {y+5}v{ch-10}' if cw==14 else f'M{x+5} {y+5}h{cw-10}M{x+5} {y+8}h{cw-10}',sw=1)+'</g>'
 elif a['animationFrames']>1:
  frames=[];count=a['animationFrames'];dots=12 if w==32 else 8
  for f in range(count):
   b=''
   for i in range(dots):
    ang=2*math.pi*i/dots;phase=(i/dots-f/count)%1
    # Opaque RGB ramp survives GIF's binary alpha; every spoke remains visible.
    t=phase**1.5;rgb=tuple(round(a+(z-a)*t) for a,z in zip((183,200,220),(50,117,214)));color='#%02x%02x%02x'%rgb
    x1=w/2+math.sin(ang)*w*.235;y1=h/2-math.cos(ang)*h*.235;x2=w/2+math.sin(ang)*w*.385;y2=h/2-math.cos(ang)*h*.385
    b+=path(f'M{x1:.3f} {y1:.3f}L{x2:.3f} {y2:.3f}',stroke=color,sw=w*.078)
   frames.append(b)
  body=frames[0]
 elif rel.startswith('tree/elbow'):
  rtl='rtl' in n;cx=6 if rtl else 9
  if '-nl' not in n:
   body+=f'<g color="{BORDER}">'+path(f'M{cx+.5} 0v{10 if "end" in n else 20}M{cx+.5} 10.5h{-cx if rtl else 16-cx}',sw=1)+'</g>'
  if 'plus' in n or 'minus' in n:
   body+=rect(cx-3.5,6.5,7,7,'white',BORDER)+put('plus' if 'plus' in n else 'minus',cx-4,6,8,8)
 elif rel.startswith('tree/arrows'):
  for i,g in enumerate(['left' if 'rtl' in n else 'right','down','left' if 'rtl' in n else 'right','down']):body+=put(g,i*16+2,4,12,12,BLUE if i>=2 else INK)
 elif rel.startswith('tree/') and n.startswith(('folder','leaf')):body=put('leaf' if n.startswith('leaf') else 'folder-open' if 'open' in n else 'folder',0,0,w,h)
 elif 'scroll-' in n:
  direction=next(d for d in ['left','right','top','bottom'] if 'scroll-'+d in n);g={'top':'up','bottom':'down'}.get(direction,direction)
  if w==28 and h==42:
   for i in range(2):body+=bg(i*14,0,14,42,i)+put(g,i*14+1,4,12,14,BLUE if i else INK)
  elif w==36 and h==42:
   yy=3 if n.endswith('top') else 25
   for i in range(2):body+=bg(i*18,0,18,42,i)+put(g,i*18+2,yy,14,14)
  elif w==42 and h==36:
   xx=3 if n.endswith('left') else 25
   for i in range(2):body+=bg(0,i*18,42,18,i)+put(g,xx,i*18+2,14,14)
  elif w==35:
   for i in range(2):body+=bg(0,i*5,35,5,i)+put(g,14,i*5,7,5)
  elif h==35:
   for i in range(2):body+=bg(i*5,0,5,35,i)+put('left' if direction=='bottom' else 'right',i*5,14,5,7)
  else:raise ValueError(rel)
 elif 's-arrow' in n or 'split-arrow' in n:
  rtl='rtl' in n;bottom='s-arrow-b' in n
  if 'noline' not in n:body+=rect(0 if not rtl else w-1,0,w if bottom else 1,1 if bottom else h,BORDER,'none')
  g=('left' if rtl else 'right') if 'breadcrumb/' in rel and 'open' not in n else 'down'
  body+=put(g,(w-8)/2,4 if bottom else (h-8)/2,8,8)
 elif n.startswith('mini-'):
  direction=n[5:];g={'top':'up','bottom':'down'}.get(direction,direction)
  body=rect(.5,.5,w-1,h-1,'#F4F7FC',BORDER)+put(g,(w-5)/2,(h-5)/2,5,5)
 else:
  g=None;col=INK;x=y=0;gw=w;gh=h
  if n.startswith('op-'):g=n
  elif rel.startswith('grid/filters/'):g={'equals':'op-eq','find':'search','greater_than':'op-gt','less_than':'op-lt'}[n]
  elif n.startswith('page-'):g={'page-first':'first','page-last':'last','page-next':'next','page-prev':'prev'}[n.replace('-disabled','')]
  elif n.startswith('refresh'):g='refresh'
  elif n in ['add','remove']:g='plus' if n=='add' else 'minus'
  elif n=='columns':g='columns'
  elif n in ['group-by','groups','summary','group-clear']:g={'group-by':'group'}.get(n,n)
  elif n in ['group-expand','group-collapse']:
   body=rect(.5,.5,w-1,h-1,'white',BORDER);g='plus' if 'expand' in n else 'minus'
  elif n.startswith('hmenu-'):g={'hmenu-asc':'asc','hmenu-desc':'desc','hmenu-lock':'lock','hmenu-unlock':'unlock'}[n]
  elif 'gear' in n:g='gear'
  elif n in ['sort_asc','sort_desc']:
   body=path('M1 .5 4.5 4.5 8 .5Z' if n=='sort_desc' else 'M1 4.5 4.5 .5 8 4.5Z',fill=INK,stroke='none')
  elif n in ['col-move-bottom','col-move-top']:g='up' if n=='col-move-bottom' else 'down'
  elif n=='hd-pop':g='down'
  elif n.startswith('dd-insert-arrow'):g='left' if 'left' in n else 'right'
  elif n.startswith('dirty'):
   body=path(f'M{w if "rtl" in n else 0} 0h{-5 if "rtl" in n else 5}l{5 if "rtl" in n else -5} 5z',BLUE,'none')
  elif n=='invalid_line':body=path('M0 .5 2 2.5 4 .5',stroke='#BE5363',sw=1)
  elif n in ['default-group-checked','default-menubar-group-checked']:body=circle(7,8,3,BLUE,'none')
  elif n in ['default-checked','default-menubar-checked','default-unchecked','default-menubar-unchecked']:
   checked='unchecked' not in n;frame=BLUE if checked else INK
   body=f'<rect x="2.5" y="2.5" width="11" height="11" rx="1" fill="{BLUE if checked else "white"}" stroke="{frame}" stroke-width="1.25"/>'
   if checked:body+=path('M5 8 7.1 10.1 11.2 5.6',stroke='white',sw=1.75)
  elif 'menu-parent' in n:g='left' if 'left' in n else 'down' if 'menubar' in n else 'right'
  elif 'more' in n:g='more-left' if 'left' in n else 'more'
  elif n=='tab-default-close':g='close'
  elif n.startswith('arrow') or n.startswith('default-arrow'):g='down' if 'breadcrumb' not in rel or 'open' in n else 'left' if 'rtl' in n else 'right'
  elif n in ['left-btn','right-btn']:g='left' if n=='left-btn' else 'right'
  elif n.startswith('icon') or n=='exclamation':g=next(s for s in ['error','info','question','warning','exclamation'] if s in n)
  elif n.startswith('drop-'):
   if n in ['drop-add','drop-append','drop-no','drop-yes']:g={'drop-add':'drop-add','drop-append':'drop-add','drop-no':'no','drop-yes':'yes'}[n]
   else:
    body=put('group',1,1,14,14)+f'<g color="{BLUE}">'+path('M1 2h14' if n=='drop-above' else 'M1 14h14' if n=='drop-below' else 'M1 8h14')+'</g>'
  if g:
   if 'disabled' in n:col='#A7B5C6'
   if g in ['error','exclamation','no']:col='#BE5363'
   if g=='warning':col='#AD7C27'
   body+=put(g,x,y,gw,gh,col)
  if not body:raise ValueError('Unhandled '+rel)
 add(rel+'.svg',a,body,frames)
# Tools whose original offsets wrap beyond the parent canvas get explicit isolated candidates.
for g in ['resize','move']:
 a={'semanticId':'adapter/tool-'+g,'logicalResourcePath':'images/tools/nordic-'+g+'.gif','sourcePath':'TestApp/ext/classic/theme-classic/resources/images/tools/tool-sprites.gif','sourceSha256':next(a['sourceSha256'] for a in BASE['assets'] if a['logicalResourcePath']=='images/tools/tool-sprites.gif'),'bitmapDimensions':{'width':30,'height':15},'animationFrames':1,'runtimeSamples':[]}
 add('tools/nordic-'+g+'.gif.svg',a,put(g,0,0,15,15)+put(g,15,0,15,15,BLUE),notes='Separate 2-column adapter: normal x=0, hover x=-15; y=0. Original 15x15 box retained; only artwork mapping changes, pending approval.')
(OUT/'render-jobs.json').write_text(json.dumps(jobs),encoding='utf8')
(OUT/'candidate-plan.json').write_text(json.dumps({'version':'nordic-icons-v1','entries':entries,'reclassifiedNonIcons':skips},ensure_ascii=False,indent=2),encoding='utf8')
print(f'{len(entries)} sheets/adapters, {len(jobs)} vector exports, {len(skips)} corrected non-icon decisions')
