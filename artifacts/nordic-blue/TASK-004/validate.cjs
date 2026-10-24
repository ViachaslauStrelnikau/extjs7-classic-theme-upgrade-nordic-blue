const fs=require('node:fs'),path=require('node:path');
const {chromium}=require('C:/Users/Damned/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root='D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue',out=__dirname,plan=JSON.parse(fs.readFileSync(path.join(out,'icon-manifest.json'))),map=new Map(plan.entries.map(e=>[e.resource,e]));
const output=path.join(out,'review/runtime');fs.mkdirSync(output,{recursive:true});
function resource(url){let m=decodeURIComponent(url).match(/\/resources\/(images\/[^?#]+)/);return m&&m[1]}
(async()=>{const browser=await chromium.launch({channel:'msedge',headless:true});const results=[];
for(const dpr of [1,2])for(const mode of ['classic','nordic','fallback']){
 const context=await browser.newContext({viewport:{width:1320,height:1600},deviceScaleFactor:dpr,locale:'en-US',timezoneId:'Europe/Minsk'});const requests=[];let errors=[];
 await context.route('http://nordic-audit.test/**',async route=>{const url=new URL(route.request().url());let p=url.pathname==='/'?path.join(out,'fixture.html'):path.join(root,decodeURIComponent(url.pathname));let res=resource(url.href),e=map.get(res);
  if(mode!=='classic'&&e){let file=mode==='fallback'?e.outputs['1'].fallback:e.outputs[dpr].preferred;p=path.join(out,file);requests.push({resource:res,dpr,preferred:file})}
  try{const ext=path.extname(p);await route.fulfill({status:200,contentType:{'.html':'text/html','.js':'application/javascript','.css':'text/css','.gif':'image/gif','.png':'image/png','.woff':'font/woff','.woff2':'font/woff2','.ttf':'font/ttf'}[ext]||'application/octet-stream',body:fs.readFileSync(p)})}catch(e){errors.push('Missing '+p);await route.fulfill({status:404,body:'Missing'})}
 });
 const page=await context.newPage();page.on('pageerror',e=>errors.push(String(e)));await page.goto('http://nordic-audit.test/',{waitUntil:'networkidle'});await page.waitForFunction(()=>window.auditReady);await page.evaluate(()=>document.fonts.ready);
 if(mode!=='classic'){
  const sizes=Object.fromEntries(plan.entries.map(e=>[e.resource,e.classicDimensions]));
  await page.evaluate(({sizes,dpr})=>{let css=[];function walk(rs){for(let r of rs){if(r.styleSheet){walk(r.styleSheet.cssRules)}else if(r.style&&r.selectorText){let m=r.style.backgroundImage.match(/\/resources\/(images\/[^"')]+)/);if(!m)m=r.style.backgroundImage.match(/url\(["']?(images\/[^"')]+)/);if(m&&sizes[m[1]]){let [w,h]=sizes[m[1]];css.push(`${r.selectorText}{background-size:${w}px ${h}px!important}`)}}else if(r.cssRules)walk(r.cssRules)}}for(let sheet of document.styleSheets){try{walk(sheet.cssRules)}catch(e){}}
   // Resource selection is intercepted locally, sheet size remains in CSS px.
   for(const g of ['resize','move'])css.push(`.x-tool-${g}{background-image:url('/ext-7.7.0.31/build/classic/theme-classic/resources/images/tools/nordic-${g}.gif')!important;background-position-y:0!important;background-size:30px 15px!important}`);
   let style=document.createElement('style');style.textContent=css.join('\n');document.head.appendChild(style);
  },{sizes,dpr});
 }
 await page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));
 const data=await page.evaluate(()=>{const props=['width','height','boxSizing','paddingTop','paddingRight','paddingBottom','paddingLeft','borderTopWidth','borderRightWidth','borderBottomWidth','borderLeftWidth','fontFamily','fontSize','fontWeight','lineHeight','letterSpacing','marginTop','marginRight','marginBottom','marginLeft','display','visibility','backgroundPositionX','backgroundPositionY'];return {rows:auditRows.map(row=>({id:row.id,state:row.state,elements:Array.from(row.card.querySelectorAll('*')).map((e,i)=>{let r=e.getBoundingClientRect(),s=getComputedStyle(e);return {index:i,tag:e.tagName,classes:e.className,rect:{x:r.x,y:r.y,width:r.width,height:r.height},metrics:Object.fromEntries(props.map(k=>[k,s[k]])),pseudo:['::before','::after'].map(p=>{let s=getComputedStyle(e,p);return {pseudo:p,content:s.content,...Object.fromEntries(props.map(k=>[k,s[k]]))}})}})})),constructionErrors:auditErrors}});
 const file=`${mode}-${dpr}`;fs.writeFileSync(path.join(out,file+'-geometry.json'),JSON.stringify(data));
 for(const section of await page.locator('.audit-section').all()){const group=await section.getAttribute('data-group');await section.screenshot({path:path.join(output,`${file}-${group}.png`),animations:'disabled'})}
 results.push({mode,dpr,rows:data.rows.length,elements:data.rows.reduce((n,r)=>n+r.elements.length,0),errors,constructionErrors:data.constructionErrors,requests});await context.close();
}
const differences=[],exceptions=[];let compared=0;
for(const dpr of [1,2])for(const mode of ['nordic','fallback']){const a=JSON.parse(fs.readFileSync(path.join(out,`classic-${dpr}-geometry.json`))),b=JSON.parse(fs.readFileSync(path.join(out,`${mode}-${dpr}-geometry.json`)));if(a.rows.length!==b.rows.length)throw Error('Missing rows');
 for(let i=0;i<a.rows.length;i++){let ar=a.rows[i],br=b.rows[i];if(ar.id!==br.id||ar.state!==br.state||ar.elements.length!==br.elements.length)throw Error('Fixture mismatch');for(let j=0;j<ar.elements.length;j++){let ae=ar.elements[j],be=br.elements[j];compared++;for(const k of ['rect','metrics','pseudo'])if(JSON.stringify(ae[k])!==JSON.stringify(be[k])){
  const aa=structuredClone(ae[k]),bb=structuredClone(be[k]);if(k==='metrics'&&/x-tool-(resize|move)( |$)/.test(ae.classes)){exceptions.push({dpr,id:ar.id,state:ar.state,classes:ae.classes,from:aa.backgroundPositionY,to:bb.backgroundPositionY,reason:'Explicit resize/move adapter; old out-of-canvas wrap replaced by y=0 same 15px CSS box'});delete aa.backgroundPositionY;delete bb.backgroundPositionY}
  if(JSON.stringify(aa)!==JSON.stringify(bb))differences.push({dpr,id:ar.id,state:ar.state,index:j,classes:ae.classes,kind:k,classic:aa,nordic:bb});
 }}}
}
const report={status:!differences.length&&results.every(r=>!r.errors.length&&!r.constructionErrors.length)?'PASS':'FAIL',browser:await browser.version(),viewport:[1320,1600],dprs:[1,2],rowsPerRun:results[0].rows,elementComparisons:compared,differences,documentedArtworkOffsetAdapters:exceptions,runs:results,scope:'Technical isolated fixture, same Classic CSS and real Ext components. Hover/focus/pressed CSS states projected as TASK-003; not functional/theme release acceptance. 2x resources selected by route in preview only, integration not performed.'};fs.writeFileSync(path.join(out,'density-validation.json'),JSON.stringify(report,null,2));console.log(JSON.stringify({status:report.status,rows:report.rowsPerRun,elementComparisons:compared,differences:differences.slice(0,4),exceptions:exceptions.length,runs:results.map(r=>({mode:r.mode,dpr:r.dpr,errors:r.errors,resources:new Set(r.requests.map(x=>x.resource)).size}))}));await browser.close();if(report.status!=='PASS')process.exitCode=1;
})().catch(e=>{console.error(e);process.exit(1)});
