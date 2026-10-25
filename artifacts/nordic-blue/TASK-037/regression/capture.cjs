const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {chromium}=require('C:/Users/Damned/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const out=__dirname,root='D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue';
const base=process.env.NORDIC_LAB_URL||'http://127.0.0.1:51752/theme-lab/';
const theme=process.env.NORDIC_CAPTURE_THEME||'nordic';
const dpr=Number(process.argv[2]||1),pass=Number(process.argv[3]||1),only=process.argv.slice(4);
const coverage=JSON.parse(fs.readFileSync(path.join(root,'artifacts/nordic-blue/TASK-005/coverage.json'))),oldInspection=JSON.parse(fs.readFileSync(path.join(root,'artifacts/nordic-blue/TASK-005/inspection.json')));
const frozen=JSON.parse(fs.readFileSync(path.join(out,theme==='classic'?'classic-frozen-resources.json':'nordic-frozen-resources.json'))),extract=fs.readFileSync(path.join(out,'extract.js'),'utf8');
const sha=data=>crypto.createHash('sha256').update(data).digest('hex');
const folder=path.join(out,theme,only.length?`probe/dpr-${dpr}/pass-${pass}`:`captures/pass-${pass}/dpr-${dpr}`);fs.mkdirSync(folder,{recursive:true});
if(!only.length&&fs.existsSync(path.join(folder,'index.json'))&&process.env.NORDIC_BASELINE_RECAPTURE!=='1')throw Error('Existing capture index: use a separate copy/output set. Deliberate staged recapture requires NORDIC_BASELINE_RECAPTURE=1. Never refresh an accepted baseline to hide a regression.');
(async()=>{
const rasterArgs=process.env.NORDIC_CPU_RASTER==='1'?['--disable-gpu','--force-color-profile=srgb']:[];
const browser=await chromium.launch({channel:'msedge',headless:true,args:rasterArgs});
const context=await browser.newContext({viewport:{width:1280,height:1600},deviceScaleFactor:dpr,locale:'en-US',timezoneId:'Europe/Minsk',colorScheme:'light',reducedMotion:'reduce'});
const substitutions=[];
await context.route('**/*',async route=>{
 const url=route.request().url();let match=url.match(/\/resources\/(images\/[^?#]+)/),key=match&&match[1];
 if(key&&frozen[key]&&(/\/(?:sdk\/build\/classic\/theme-classic|build\/(?:theme-lab\/(?:classic|nordic)|theme-contrast)\/testing)\/resources\//.test(new URL(url).pathname))){const asset=frozen[key];substitutions.push({resource:key,url,sourceSha256:asset.sourceSha256,servedSha256:asset.derivedPngSha256});await route.fulfill({status:200,contentType:'image/png',body:fs.readFileSync(path.join(out,asset.derivedPng))});}else await route.continue();
});
const page=await context.newPage();let errors=[],bad=[],resources=[];
page.on('pageerror',e=>errors.push(String(e)));page.on('response',r=>{const record={url:r.url(),status:r.status(),type:r.request().resourceType()};resources.push(record);if(r.status()>=400)bad.push(record)});
const scenarios=only.length?only.map(x=>{const [name,state='normal']=x.split('/');return{name,state}}):[{name:'all',state:'normal'},...Object.entries(coverage.cases).flatMap(([name,states])=>states.map(state=>({name,state})))];
const records=[];
for(const {name,state}of scenarios){
 errors=[];bad=[];resources=[];substitutions.length=0;
 await page.mouse.up();await page.mouse.move(1279,1599);
 const url=new URL('index.html',base);url.search=new URLSearchParams({theme,case:name,state}).toString();
 await page.goto(url.href,{waitUntil:'networkidle'});await page.waitForFunction(()=>window.themeLab||window.labBoot?.status==='ERROR');
 const boot=await page.evaluate(()=>labBoot);if(boot.status==='ERROR')throw Error(name+'/'+state+' bootstrap: '+JSON.stringify(boot));
 await page.mouse.move(1279,1599);const pending=await page.evaluate(()=>themeLab.pendingActions);
 for(const a of pending){await page.locator(a.selector).hover();if(a.kind==='mousedown')await page.mouse.down();}
 await page.evaluate(()=>themeLab.whenReady());await page.addScriptTag({content:extract+'\nwindow.extractBaseline=extractBaseline;'});
 let metrics=await page.evaluate(()=>extractBaseline());
 const expected=oldInspection.results.find(r=>r.case===name&&r.state===state);
 if(!expected||metrics.fixtureSemanticCount!==expected.snapshot.length)throw Error('Fixture semantic count changed '+name+'/'+state+': '+metrics.fixtureSemanticCount+' != '+expected?.snapshot.length);
 if(metrics.duplicates.length)throw Error('Duplicate semantic IDs '+name+'/'+state+': '+JSON.stringify(metrics.duplicates));
 if(!metrics.elementCount||!metrics.visibleElementCount||errors.length||bad.length||metrics.errors.length)throw Error('Empty/error capture '+name+'/'+state+': '+JSON.stringify({errors,bad,metricsErrors:metrics.errors}));
 const stem=name+'--'+state,shot=path.join(folder,stem+'.png');
 // Raw browser raster, no pixel editing/normalization/masking. Animated GIF frame0 substitution is declared separately.
 await page.screenshot({path:shot,fullPage:name==='all',animations:'disabled',caret:'hide',scale:'device'});
 const after=await page.evaluate(()=>extractBaseline());
 if(JSON.stringify(metrics.elements)!==JSON.stringify(after.elements))throw Error('Metrics moved during screenshot '+stem);
 metrics.network={errors,badResponses:bad,resources,frame0Substitutions:[...substitutions]};metrics.capture={policy:'raw raster under declared first-GIF-frame policy; no image normalization or broad masks',dpr,pass,screenshot:path.basename(shot),screenshotSha256:sha(fs.readFileSync(shot)),browser:await browser.version()};
 const json=path.join(folder,stem+'.json');fs.writeFileSync(json,JSON.stringify(metrics));
 records.push({case:name,state,elementCount:metrics.elementCount,visibleElementCount:metrics.visibleElementCount,fixtureSemanticCount:metrics.fixtureSemanticCount,iconCount:metrics.icons.length,frame0Substitutions:substitutions.map(x=>x.resource),screenshot:path.basename(shot),metrics:path.basename(json),screenshotSha256:metrics.capture.screenshotSha256,metricsSha256:sha(fs.readFileSync(json))});
 console.log(JSON.stringify({dpr,pass,case:name,state,elements:metrics.elementCount,icons:metrics.icons.length,status:'CAPTURED'}));
}
const summary={theme,dpr,pass,browser:await browser.version(),rasterArgs,viewport:[1280,1600],locale:'en-US',timezone:'Europe/Minsk',records,scenarioCount:records.length};
fs.writeFileSync(path.join(folder,'index.json'),JSON.stringify(summary,null,2));await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
