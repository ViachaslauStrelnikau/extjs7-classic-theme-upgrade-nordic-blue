const {chromium}=require('C:/Users/Damned/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('node:fs'),path=require('node:path');
const root='D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue',output=__dirname;
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true});
 const context=await browser.newContext({viewport:{width:1320,height:1600},deviceScaleFactor:1,locale:'en-US',timezoneId:'Europe/Minsk'});
 await context.route('http://nordic-audit.test/**',async route=>{let url=new URL(route.request().url());let p=url.pathname==='/'?path.join(output,'fixture.html'):path.join(root,decodeURIComponent(url.pathname));try{let body=fs.readFileSync(p);let ext=path.extname(p);let type={'.html':'text/html','.js':'application/javascript','.css':'text/css','.gif':'image/gif','.png':'image/png','.woff':'font/woff','.woff2':'font/woff2','.ttf':'font/ttf'}[ext]||'application/octet-stream';await route.fulfill({status:200,contentType:type,body});}catch(e){await route.fulfill({status:404,body:'Missing '+url.pathname})}});
 const page=await context.newPage();let errors=[],bad=[];page.on('pageerror',e=>errors.push(String(e)));page.on('response',r=>{if(r.status()>=400)bad.push({url:r.url(),status:r.status()})});
 await page.goto('http://nordic-audit.test/',{waitUntil:'networkidle'});await page.waitForFunction(()=>window.auditReady,{timeout:45000});await page.evaluate(()=>document.fonts.ready);
 await page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
 const data=await page.evaluate(()=>{
  let styleRules=[];function walk(rules){for(let r of rules){if(r.styleSheet){try{walk(r.styleSheet.cssRules)}catch(e){}}else if(r.style){if(r.style.backgroundImage&&r.style.backgroundImage!=='none')styleRules.push({selector:r.selectorText,css:r.style.cssText});if(r.cssRules&&r.cssRules.length)walk(r.cssRules)}else if(r.cssRules){walk(r.cssRules)}}}for(let sheet of document.styleSheets){try{walk(sheet.cssRules)}catch(e){}}
  const rows=auditRows.map(row=>{let symbols=[];for(let e of row.card.querySelectorAll('*')){let rect=e.getBoundingClientRect();for(let pseudo of [null,'::before','::after']){let s=getComputedStyle(e,pseudo);if(pseudo&&(s.content==='none'||s.content==='normal'))continue;if(s.backgroundImage!=='none'&&s.display!=='none'&&rect.width>0&&rect.height>0){symbols.push({classes:e.className+(pseudo||''),tag:e.tagName,pseudo,rect:pseudo?null:rect.toJSON(),hostRect:pseudo?rect.toJSON():null,cssWidth:s.width,cssHeight:s.height,backgroundImage:s.backgroundImage,backgroundPositionX:s.backgroundPositionX,backgroundPositionY:s.backgroundPositionY,backgroundSize:s.backgroundSize,backgroundRepeat:s.backgroundRepeat,opacity:s.opacity,ancestorOpacity:Array.from((function*(p){while(p&&p!==row.card){yield p;p=p.parentElement}})(pseudo?e:e.parentElement)).map(p=>({classes:p.className,opacity:getComputedStyle(p).opacity})),visibility:s.visibility,display:s.display,boxSizing:s.boxSizing,border:s.borderWidth})}}}return {semanticId:row.id,state:row.state,method:row.method,symbols}});
  const nativeControls=Array.from(document.querySelectorAll('.audit-card select')).map(e=>({component:e.closest('.audit-card').dataset.semantic,state:e.closest('.audit-card').dataset.state,classes:e.className,rect:e.getBoundingClientRect().toJSON(),fontFamily:getComputedStyle(e).fontFamily}));
  return {version:Ext.getVersion().version,dpr:devicePixelRatio,rows,errors:auditErrors,styleRules,nativeControls};
 });
 data.browser=await browser.version();data.pageErrors=errors;data.badResponses=bad;
 fs.writeFileSync(path.join(output,'runtime.json'),JSON.stringify(data,null,2));
 for(let section of await page.locator('.audit-section').all()){let name=await section.getAttribute('data-group');await section.screenshot({path:path.join(output,'classic-'+name+'.png'),animations:'disabled'});}
 console.log(JSON.stringify({rows:data.rows.length,constructionErrors:data.errors,pageErrors:errors,badResponses:bad,symbols:data.rows.reduce((n,r)=>n+r.symbols.length,0),styleRules:data.styleRules.length,browser:data.browser}));
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
