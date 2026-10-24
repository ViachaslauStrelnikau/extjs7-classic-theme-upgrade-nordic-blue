// TASK-005 operational readiness/coverage evidence; release suites belong to TASK-014/015.
const fs=require('node:fs'),path=require('node:path');
const {chromium}=require('C:/Users/Damned/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root='D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue',out=__dirname,source=path.join(out,'src');
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true});const context=await browser.newContext({viewport:{width:1280,height:1600},deviceScaleFactor:1,locale:'en-US',timezoneId:'Europe/Minsk'});
 await context.route('http://theme-lab.test/**',async route=>{let rel=decodeURIComponent(new URL(route.request().url()).pathname).slice(1),p=rel.startsWith('TestApp/theme-lab/sdk/')?path.join(root,'ext-7.7.0.31',rel.slice('TestApp/theme-lab/sdk/'.length)):path.join(source,rel);if(!fs.existsSync(p))p=path.join(root,rel);try{await route.fulfill({status:200,contentType:{'.html':'text/html','.css':'text/css','.js':'application/javascript','.json':'application/json','.png':'image/png','.gif':'image/gif','.woff':'font/woff','.woff2':'font/woff2','.ttf':'font/ttf'}[path.extname(p)]||'application/octet-stream',body:fs.readFileSync(p)})}catch(e){await route.fulfill({status:404,body:'Missing '+rel})}});
 const page=await context.newPage();let errors=[],bad=[];page.on('pageerror',e=>errors.push(String(e)));page.on('response',r=>{if(r.status()>=400)bad.push(r.url())});
 async function open(name,state){errors=[];bad=[];await page.goto(`http://theme-lab.test/TestApp/theme-lab/index.html?theme=classic&case=${name}&state=${state}`,{waitUntil:'networkidle'});await page.waitForFunction(()=>window.themeLab||labBoot.status==='ERROR');const boot=await page.evaluate(()=>labBoot);if(boot.status==='ERROR')return {case:name,state,status:'FAIL',boot,errors,bad,fixture:await page.evaluate(()=>({errors:window.themeLab?.errors,status:document.getElementById('lab-status').textContent}))};
  await page.mouse.move(1279,1599);await page.evaluate(()=>{window.inputTrace=[];document.addEventListener('mousedown',e=>inputTrace.push({type:e.type,trusted:e.isTrusted,target:e.target.outerHTML.slice(0,300),pending:JSON.stringify(themeLab.pendingActions)}),true)});const pending=await page.evaluate(()=>themeLab.pendingActions);for(const a of pending){if(a.kind==='mousedown'){await page.locator(a.selector).hover();await page.mouse.down()}else await page.locator(a.selector).hover()}
  let evidence;try{await page.evaluate(()=>themeLab.whenReady());evidence=await page.evaluate(()=>({status:themeLab.status,environment:themeLab.environment(),snapshot:themeLab.snapshot(),components:Array.from(themeLab.components.keys()),errors:themeLab.errors}));}catch(e){evidence={status:'FAIL',error:String(e),details:await page.evaluate(()=>({errors:themeLab.errors,pending:themeLab.pendingActions,inputTrace:window.inputTrace,editors:themeLab.editors.map(e=>({initialized:e.initialized})),status:themeLab.status}))}}
  if(pending.some(a=>a.kind==='mousedown'))await page.mouse.up();return {case:name,state,...evidence,pageErrors:errors,badResponses:bad};
 }
 const args=process.argv.slice(2),results=[];
 if(args.length){for(const arg of args){const [name,state='normal']=arg.split('/');results.push(await open(name,state));console.log(JSON.stringify({case:name,state,status:results.at(-1).status,errors:results.at(-1).fixture||results.at(-1).error||results.at(-1).errors,details:results.at(-1).details}));}}
 else{
  const overview=await open('all','normal');results.push(overview);console.log(JSON.stringify({case:'all',status:overview.status,errors:overview.errors||overview.error,details:overview.details}));
  if(overview.status==='READY'){
   fs.mkdirSync(path.join(out,'screenshots'),{recursive:true});await page.screenshot({path:path.join(out,'screenshots/overview.png'),fullPage:true});
   const cases=await page.evaluate(()=>themeLab.cases);for(const [name,c]of Object.entries(cases))for(const state of c.states){const r=await open(name,state);results.push(r);console.log(JSON.stringify({case:name,state,status:r.status,error:r.error||r.errors||r.boot?.errors}));if(r.status==='READY'&&state==='normal')await page.screenshot({path:path.join(out,'screenshots',name+'.png')});}
  }
 }
 const report={browser:await browser.version(),scope:'TASK-005 readiness and coverage availability in the unchanged Classic TestApp build; not a geometry golden or full functional/release suite',results};fs.writeFileSync(path.join(out,args.length?'inspection-partial.json':'inspection.json'),JSON.stringify(report,null,2));await browser.close();if(results.some(r=>r.status!=='READY'||r.pageErrors?.length||r.badResponses?.length))process.exitCode=1;
})().catch(e=>{console.error(e);process.exit(1)});
