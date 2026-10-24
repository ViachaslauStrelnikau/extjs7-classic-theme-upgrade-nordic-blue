const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {chromium}=require('C:/Users/Damned/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const out=__dirname,root='D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue',plan=JSON.parse(fs.readFileSync(path.join(root,JSON.parse(fs.readFileSync(path.join(root,'config/nordic-blue-icons.json'))).manifestPath))),policy=JSON.parse(fs.readFileSync(path.join(root,'config/nordic-blue-icons.json'))),extract=fs.readFileSync(path.join(out,'extract.js'),'utf8');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
function asset(e,d){const x=e.outputs[d].preferred.split(`candidate/${d}x/`)[1];return d===1?x:x.replace('images/','images/@2x/')}
(async()=>{const browser=await chromium.launch({channel:'msedge',headless:true,args:['--disable-gpu','--force-color-profile=srgb']});const runs=[];
for(const mode of ['testing','development','production']){
 const base=path.join(root,'TestApp/build/theme-lab/nordic',mode,'resources');
 for(const [key,v]of Object.entries(policy.runtimeImages))if(sha(fs.readFileSync(path.join(base,key)))!==v.sha256)throw Error('Built asset bytes '+mode+'/'+key);
 for(const [dpr,fallback]of [[1,false],[2,false],[2,true]]){
  const density=fallback?1:dpr,context=await browser.newContext({viewport:{width:1280,height:1600},deviceScaleFactor:dpr,locale:'en-US',timezoneId:'Europe/Minsk',colorScheme:'light',reducedMotion:'reduce'});
  await context.route('**/theme-lab/profiles.json',async route=>{const p=JSON.parse(fs.readFileSync(path.join(root,'TestApp/theme-lab/profiles.json')));p.profiles.nordic.manifest=`../build/theme-lab/nordic/${mode}/app.json`;await route.fulfill({status:200,contentType:'application/json',body:JSON.stringify(p)});});
  if(fallback)await context.route('**/NordicThemeLab-all*.css*',async route=>{const response=await route.fetch();let css=await response.text();const pattern=/@media\s*\(\s*min-resolution\s*:\s*192dpi\s*\)/g;css=css.replace(pattern,'@media (min-resolution: 19200dpi)');await route.fulfill({response,body:css});});
  const page=await context.newPage();let bad=[],errors=[],responses=[];page.on('pageerror',e=>errors.push(String(e)));page.on('response',r=>{if(r.status()>=400)bad.push(r.url());const m=r.url().match(/\/resources\/(images\/[^?#]+)/);if(m&&policy.runtimeImages[m[1]])responses.push(r.body().then(b=>{if(sha(b)!==policy.runtimeImages[m[1]].sha256)throw Error('HTTP asset SHA '+r.url());return{url:r.url(),resource:m[1],sha256:sha(b),density:policy.runtimeImages[m[1]].density}}));});
  const label=mode+'-dpr-'+dpr+(fallback?'-fallback':'');const folder=path.join(out,'build-modes',label);fs.mkdirSync(folder,{recursive:true});
  for(let reload=0;reload<2;reload++){
   if(reload)await page.reload({waitUntil:'networkidle'});else await page.goto('http://127.0.0.1:51752/theme-lab/index.html?theme=nordic&case=all&state=normal',{waitUntil:'networkidle'});
   await page.evaluate(()=>themeLab.whenReady());await page.addScriptTag({content:extract+'\nwindow.extractBaseline=extractBaseline;'});const metrics=await page.evaluate(()=>extractBaseline());
   if(metrics.fixtureSemanticCount<100||metrics.errors.length||metrics.duplicates.length)throw Error('Incomplete native overview');
   const mapped=metrics.icons.flatMap(e=>e.resources||[]).map(u=>u.match(/\/resources\/(images\/[^?#]+)/)?.[1]).filter(k=>policy.runtimeImages[k]);if(!mapped.length||mapped.some(k=>policy.runtimeImages[k].density!==density))throw Error('Wrong native density '+label);
   fs.writeFileSync(path.join(folder,'native-'+reload+'.json'),JSON.stringify(metrics));
   if(!reload)await page.screenshot({path:path.join(folder,'native.png'),animations:'disabled',caret:'hide'});
  }
  const nativeHttp=await Promise.all(responses);if(errors.length||bad.length)throw Error(JSON.stringify({errors,bad}));
  const catalog=await context.newPage();catalog.on('pageerror',e=>errors.push(String(e)));catalog.on('response',r=>{if(r.status()>=400)bad.push(r.url())});
  const urlBase=`http://127.0.0.1:51752/build/theme-lab/nordic/${mode}/resources/`;const escape=s=>s.replaceAll('&','&amp;').replaceAll('<','&lt;');
  let styles=plan.entries.map((e,i)=>`.s${i}{width:${e.classicDimensions[0]}px;height:${e.classicDimensions[1]}px;background-image:url('${urlBase+asset(e,1)}');background-size:${e.classicDimensions[0]}px ${e.classicDimensions[1]}px}`).join('\n');
  styles+='\n@media (min-resolution: '+(fallback?'19200':'192')+'dpi){'+plan.entries.map((e,i)=>`.s${i}{background-image:url('${urlBase+asset(e,2)}')}`).join('')+'}';
  await catalog.setContent(`<html><head><style>body{font:12px Arial;background:#f4f7fc;color:#25374d;margin:18px}.grid{display:grid;grid-template-columns:repeat(4,300px);gap:8px}.card{background:white;border:1px solid #b7c8dc;padding:6px;overflow:auto}.sheet{background-repeat:no-repeat}h1{font-size:20px}p{height:26px;font-size:10px;word-break:break-all}${styles}</style></head><body><h1>Approved v3 folders В· built catalog В· ${label}</h1><div class=grid>${plan.entries.map((e,i)=>`<div class=card><p>${escape(e.id)} В· ${e.classicDimensions.join('Г—')} CSS px</p><div class="sheet s${i}" data-index="${i}"></div></div>`).join('')}</div></body></html>`);
  const sheets=await catalog.evaluate(async()=>Promise.all([...document.querySelectorAll('.sheet')].map(async el=>{const s=getComputedStyle(el),url=s.backgroundImage.match(/url\(["']?([^"')]+)/)[1],im=new Image();im.src=url;await im.decode();const r=el.getBoundingClientRect();return{index:Number(el.dataset.index),url,size:s.backgroundSize,rect:{width:r.width,height:r.height},bitmap:[im.naturalWidth,im.naturalHeight]}})));
  if(sheets.length!==182)throw Error('Missing catalog sheets');for(const s of sheets){const e=plan.entries[s.index],v=e.outputs[density];if(s.rect.width!==e.classicDimensions[0]||s.rect.height!==e.classicDimensions[1]||s.bitmap.join()!==v.bitmapDimensions.join()||s.url!==urlBase+asset(e,density))throw Error('Sheet contract '+e.id)}
  if(errors.length||bad.length)throw Error(JSON.stringify({errors,bad}));await catalog.screenshot({path:path.join(folder,'catalog.png'),fullPage:true,animations:'disabled'});
  const result={status:'PASS',mode,dpr,fallback,density,sheets,nativeHttp,errors,bad,scope:'Actual build mode CSS/native fixture with one cache reload; full 182-sheet catalog uses actual built resource URLs and the same density sheet contracts. Fallback simulates unsupported high-resolution media query in the response only; application source untouched.'};fs.writeFileSync(path.join(folder,'index.json'),JSON.stringify(result,null,2));runs.push({label,status:'PASS',mode,dpr,fallback,density,sheets:sheets.length,nativeResponses:nativeHttp.length});console.log(JSON.stringify(runs.at(-1)));await context.close();
 }
}
fs.writeFileSync(path.join(out,'build-mode-validation.json'),JSON.stringify({status:'PASS',browser:await browser.version(),runs},null,2));await browser.close();})().catch(e=>{console.error(e);process.exit(1)});
