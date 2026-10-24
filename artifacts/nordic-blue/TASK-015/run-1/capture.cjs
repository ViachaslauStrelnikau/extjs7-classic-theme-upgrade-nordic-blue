const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {chromium}=require('C:/Users/Damned/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const R='D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue',O=__dirname,dpr=Number(process.argv[2]||1),only=process.argv.slice(3);
const read=p=>JSON.parse(fs.readFileSync(p,'utf8').replace(/^\uFEFF/,'')),icons=read(path.join(R,'config/nordic-blue-icons.json')),manifest=read(path.join(R,icons.manifestPath)),extract=fs.readFileSync(path.join(O,'extract.js'),'utf8'),paint=fs.readFileSync(path.join(O,'paint.js'),'utf8');
const parent={};for(const e of manifest.entries)for(const [d,outputs]of Object.entries(e.outputs))for(const p of ['preferred','fallback']){let k=outputs[p].split(`candidate/${d}x/`)[1];if(d!=='1')k=k.replace('images/','images/@'+d+'x/');(parent[k]??=[]).push(e.resource);}
const key=s=>s.match(/\/resources\/(images\/[^?#"')]+)/)?.[1],urls=s=>[...s.matchAll(/url\(["']?([^"')]+)/g)].map(m=>m[1]);
const coverage=read(path.join(R,'artifacts/nordic-blue/TASK-005/coverage.json'));
const scenarios=only.length?only.map(s=>{const[name,state='normal']=s.split('/');return{name,state};}):[{name:'all',state:'normal'},...Object.entries(coverage.cases).flatMap(([name,states])=>states.map(state=>({name,state})))];
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true,args:['--disable-gpu','--force-color-profile=srgb']});const contexts={},pages={};let errors=[],bad=[];
 for(const theme of ['classic','nordic']){
  const context=contexts[theme]=await browser.newContext({viewport:{width:1280,height:1600},deviceScaleFactor:dpr,locale:'en-US',timezoneId:'Europe/Minsk',colorScheme:'light',reducedMotion:'reduce'});
  const frozen=read(path.join(O,theme+'-frozen-resources.json'));
  await context.route('**/*',async route=>{const k=key(route.request().url()),e=k&&frozen[k];if(e)await route.fulfill({status:200,contentType:'image/png',body:fs.readFileSync(path.join(O,e.derivedPng))});else await route.continue();});
  const page=pages[theme]=await context.newPage();page.on('pageerror',e=>errors.push(theme+': '+String(e)));page.on('response',r=>{if(r.status()>=400)bad.push(r.url())});
 }
 const records=[];
 for(const {name,state}of scenarios){
  const stem=name+'--'+state;const data={};errors=[];bad=[];
  for(const theme of ['classic','nordic']){
   const page=pages[theme];await page.mouse.up();await page.mouse.move(1279,1599);
   await page.goto(`${process.env.NORDIC_LAB_URL||'http://127.0.0.1:51752/theme-lab/'}index.html?theme=${theme}&case=${name}&state=${state}`,{waitUntil:'networkidle'});
   await page.waitForFunction(()=>window.themeLab||window.labBoot?.status==='ERROR');
   for(const a of await page.evaluate(()=>themeLab.pendingActions)){await page.locator(a.selector).hover();if(a.kind==='mousedown')await page.mouse.down();}
   await page.evaluate(()=>themeLab.whenReady());await page.addScriptTag({content:extract+'\n'+paint+'\nwindow.extractBaseline=extractBaseline;window.collectPaint=collectPaint;window.normalizePaint=normalizePaint;window.supportPlane=supportPlane;'});
   const metrics=await page.evaluate(()=>extractBaseline());if(metrics.errors.length||metrics.duplicates.length||!metrics.elementCount)throw Error('Invalid '+stem);
   const clip=await page.evaluate(all=>{const y=document.querySelector('#lab-stage').getBoundingClientRect().top;return{x:0,y,width:1280,height:(all?Math.max(1600,document.documentElement.scrollHeight):1600)-y};},name==='all');
   const folder=path.join(O,'captures','dpr-'+dpr,theme);fs.mkdirSync(folder,{recursive:true});
   await page.screenshot({path:path.join(folder,stem+'--raw.png'),clip,animations:'disabled',caret:'hide',scale:'device'});
   data[theme]={metrics,paint:await page.evaluate(()=>collectPaint()),clip,folder,allowed:[]};
  }
  const a=data.classic,b=data.nordic;if(a.paint.length!==b.paint.length)throw Error('Document count');
  const regions=[];
  for(let d=0;d<a.paint.length;d++){
   if(a.paint[d].length!==b.paint[d].length)throw Error('DOM count '+stem);
   for(let i=0;i<a.paint[d].length;i++){
    const x=a.paint[d][i],y=b.paint[d][i];if(x.tag!==y.tag||x.key!==y.key)throw Error('DOM tag/key mismatch');
    for(const [p,suffix]of [['style',''],['before','::before'],['after','::after']]){
     const old=urls(x[p].backgroundImage),next=urls(y[p].backgroundImage);
     if(next.length===1&&icons.runtimeImages[key(next[0])]){
      const bk=key(next[0]),ak=old.length===1?key(old[0]):null,item=icons.runtimeImages[bk];
      if(!parent[bk].includes(ak)&&!(item.id.startsWith('adapter/')&&ak==='images/tools/tool-sprites.gif'))throw Error('Unapproved parent '+stem+' '+y.key+suffix+' '+ak+' '+bk);
      if(item.density!==dpr)throw Error('Density mismatch');
      a.allowed.push(x.key+suffix);b.allowed.push(y.key+suffix);regions.push({node:x.key+suffix,parent:ak,runtime:bk,density:dpr,classicHost:x.rect,nordicHost:y.rect});
     }
    }
   }
  }
  for(const theme of ['classic','nordic']){
   const page=pages[theme],r=data[theme];r.normalization=await page.evaluate(ref=>normalizePaint(ref),a.paint);
   await page.evaluate(()=>themeLab.whenReady());r.normalizedMetrics=await page.evaluate(()=>extractBaseline());
   await page.screenshot({path:path.join(r.folder,stem+'--normalized.png'),clip:r.clip,animations:'disabled',caret:'hide',scale:'device'});
   await page.evaluate(list=>supportPlane(list),r.allowed);await page.screenshot({path:path.join(r.folder,stem+'--support.png'),clip:r.clip,animations:'disabled',caret:'hide',scale:'device',omitBackground:true});
   fs.writeFileSync(path.join(r.folder,stem+'.json'),JSON.stringify({case:name,state,dpr,theme,clip:r.clip,metrics:r.metrics,normalizedMetrics:r.normalizedMetrics,normalization:r.normalization,regions}));
  }
  if(errors.length||bad.length)throw Error(JSON.stringify({errors,bad}));
  records.push({case:name,state,stem,regions:regions.length});console.log(JSON.stringify({dpr,case:name,state,regions:regions.length,status:'CAPTURED'}));
 }
 const index={status:'PASS',browser:await browser.version(),dpr,records};fs.writeFileSync(path.join(O,'captures','dpr-'+dpr,'index.json'),JSON.stringify(index,null,2));await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
