const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const pw=require('C:/Users/Damned/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const R='D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue',A=path.join(R,'artifacts/nordic-blue/TASK-021'),name=process.argv[2]||'edge',probe=process.argv.includes('--probe'),base=process.env.NORDIC_ACCEPTANCE_URL||'http://127.0.0.1:51754/';
const read=p=>JSON.parse(fs.readFileSync(p,'utf8').replace(/^\uFEFF/,'')),config=read(path.join(A,'browser-availability.json')).find(x=>x.name===name),extract=fs.readFileSync(path.join(A,'regression/extract.js'),'utf8'),fixture=fs.readFileSync(path.join(R,'TestApp/theme-lab/fixture.js'),'utf8'),clock=fs.readFileSync(path.join(R,'TestApp/theme-lab/clock.js'),'utf8'),shell=fs.readFileSync(path.join(R,'TestApp/theme-lab/index.html'),'utf8').split('<body>')[1].split('</body>')[0].replace(/<script[\s\S]*?<\/script>/g,''),labCss=fs.readFileSync(path.join(R,'TestApp/theme-lab/lab-shell.css'),'utf8');
const props=[...extract.match(/const properties=\[([\s\S]*?)\];/)[1].matchAll(/'([^']+)'/g)].map(x=>x[1]);
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
function realSnapshot(state,props){
 const elements=[],icons=[],duplicates=[],ids=new Set();
 const rect=e=>{const r=e.getBoundingClientRect();return{x:r.x,y:r.y,width:r.width,height:r.height}};
 const css=(e,pseudo)=>{const s=getComputedStyle(e,pseudo);return Object.fromEntries(props.map(p=>[p,s[p]]));};
 const urls=s=>[...s.matchAll(/url\(["']?([^"')]+)/g)].map(m=>m[1]);
 const visible=e=>{for(let p=e;p;p=p.parentElement){const s=getComputedStyle(p);if(s.display==='none'||s.visibility==='hidden'||s.opacity==='0')return false;}const r=rect(e);return r.width>0&&r.height>0;};
 function walk(el,id){
  if(['SCRIPT','STYLE','LINK','NOSCRIPT'].includes(el.tagName))return;
  el.dataset.realId=id;const r=rect(el),s=css(el),e={id,tag:el.tagName,role:el.getAttribute('role'),rect:r,client:{width:el.clientWidth,height:el.clientHeight},scroll:{width:el.scrollWidth,height:el.scrollHeight},visible:visible(el),computed:s,pseudos:[],text:[...el.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent).join('')};
  e.softRadius=el.matches('.x-window')?4:el.matches('.x-btn,.x-form-text,.x-boundlist,.x-menu')?3:0;if(ids.has(id))duplicates.push(id);ids.add(id);
  for(const p of ['::before','::after']){const c=css(el,p);if(c.content!=='none'&&c.content!=='normal'){e.pseudos.push({pseudo:p,rect:null,hostRect:r,computed:c});if(urls(c.backgroundImage).length)icons.push({id:id+p,resources:urls(c.backgroundImage),size:c.backgroundSize,offset:[c.backgroundPositionX,c.backgroundPositionY],hostRect:r,cssBox:[c.width,c.height]});}}
  if(urls(s.backgroundImage).length)icons.push({id,rect:r,resources:urls(s.backgroundImage),size:s.backgroundSize,offset:[s.backgroundPositionX,s.backgroundPositionY]});
  elements.push(e);let n=0;for(const child of el.children)if(!['SCRIPT','STYLE','LINK','NOSCRIPT'].includes(child.tagName))walk(child,id+'/'+child.tagName.toLowerCase()+'-'+n++);
 }
 walk(document.body,'real/body');elements.sort((a,b)=>a.id.localeCompare(b.id));icons.sort((a,b)=>a.id.localeCompare(b.id));
 const main=Ext.ComponentQuery.query('app-main')[0],grid=Ext.ComponentQuery.query('mainlist')[0],tabs=main.items.items;
 return {case:'real-app',state,environment:{sdk:Ext.getVersion().version,profile:{theme:window.acceptanceTheme},browser:navigator.userAgent,viewport:[innerWidth,innerHeight],dpr:devicePixelRatio},fixtureSemanticCount:elements.length,elementCount:elements.length,visibleElementCount:elements.filter(e=>e.visible).length,elements,icons,duplicates,unownedGraphics:[],activeElement:document.activeElement?.dataset.realId||null,scroll:[scrollX,scrollY],data:{active:tabs.indexOf(main.getActiveTab()),tabs:tabs.map(t=>t.title),header:main.getHeaderPosition(),message:Ext.Msg.isVisible(),selected:grid.getSelectionModel().getSelection().map(r=>r.get('name'))},stores:[{records:grid.getStore().getRange().map(r=>({name:r.get('name'),email:r.get('email'),phone:r.get('phone')}))}],errors:[]};
}
(async()=>{
if(config.status!=='AVAILABLE')throw Error('Browser unavailable');const browser=await pw[name==='firefox'?'firefox':'chromium'].launch(config.launchOptions),records=[];
for(const mode of probe?['testing']:['testing','development','production'])for(const dpr of probe?[1]:[1,2])for(const theme of ['classic','nordic'])for(const scope of ['lab','real']){
 const context=await browser.newContext({viewport:{width:1280,height:1600},deviceScaleFactor:dpr,locale:'en-US',timezoneId:'Europe/Minsk',colorScheme:'light',reducedMotion:'reduce'});context.setDefaultTimeout(60000);await context.addInitScript({content:clock});
 const page=await context.newPage();const errors=[],bad=[],responses=[];page.on('pageerror',e=>errors.push(String(e)));page.on('console',m=>{if(m.type()==='error')errors.push('console: '+m.text())});page.on('requestfailed',r=>errors.push('requestfailed: '+r.url()+' '+r.failure()?.errorText));page.on('response',r=>{responses.push({url:r.url(),status:r.status(),type:r.request().resourceType()});if(r.status()>=400)bad.push(r.url());});
 const prefix='build/'+(theme==='nordic'?(scope==='lab'?'theme-soft/':'theme-acceptance/soft/'):(scope==='lab'?'theme-lab/classic/':'theme-acceptance/classic/'))+mode+'/',url=base+prefix+'index.html?case=all&state=normal';
 const folder=path.join(A,probe?'native-probe':'native-pages',name,scope,mode,'dpr-'+dpr,theme);fs.mkdirSync(folder,{recursive:true});
 await page.goto(url,{waitUntil:'networkidle'});await page.waitForFunction(()=>window.Ext&&Ext.isReady&&Ext.getVersion);if(await page.evaluate(()=>Ext.getVersion().version)!=='7.7.0.31')throw Error('SDK mismatch');
 await page.reload({waitUntil:'networkidle'});await page.waitForFunction(()=>window.Ext&&Ext.isReady&&Ext.getVersion);if(await page.evaluate(()=>Ext.getVersion().version)!=='7.7.0.31')throw Error('SDK mismatch after cache reload');
 const manifest=await page.evaluate(()=>({packages:Ext.manifest.packages,css:Ext.manifest.css,js:Ext.manifest.js,loadOrder:Ext.manifest.loadOrder,toolkit:Ext.manifest.toolkit,theme:Ext.manifest.theme,flags:{theme:Ext.theme,enableFx:Ext.enableFx,rtl:Ext.isRTL}}));fs.writeFileSync(path.join(folder,'manifest.json'),JSON.stringify(manifest));
 if(!manifest.packages['theme-classic']||(theme==='nordic'?!manifest.packages['theme-nordic-blue-soft']:!!manifest.packages['theme-nordic-blue-soft']))throw Error('Wrong theme inclusion');
 const checkpoint=async state=>{
  await page.evaluate(()=>document.fonts.ready);await page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))));
  const metrics=scope==='lab'?await page.evaluate(()=>extractBaseline()):await page.evaluate(({state,props,source})=>Function('return ('+source+')')()(state,props),{state,props,source:realSnapshot.toString()});
  if(!metrics.elementCount||metrics.duplicates.length||metrics.errors.length)throw Error('Invalid metrics');
  fs.writeFileSync(path.join(folder,state+'.json'),JSON.stringify(metrics));await page.screenshot({path:path.join(folder,state+'.png'),fullPage:scope==='lab',animations:'disabled',caret:'hide'});
  records.push({browser:name,scope,mode,dpr,theme,state,path:path.relative(A,path.join(folder,state+'.json')).replaceAll('\\','/'),elements:metrics.elementCount});
 };
 if(scope==='lab'){
  await page.addStyleTag({content:labCss});await page.evaluate(({shell,theme,url,manifest})=>{document.body.innerHTML=shell;window.labBoot={theme,status:'LOADING',profile:{theme,manifestUrl:url.replace('index.html?case=all&state=normal','app.json'),package:theme==='nordic'?'theme-nordic-blue':'theme-classic',sdk:Ext.getVersion().version,css:manifest.css.map(c=>c.path),entry:'actual-built-output'}};},{shell,theme,url,manifest});await page.addScriptTag({content:fixture});await page.evaluate(()=>themeLab.whenReady());await page.addScriptTag({content:extract+'\nwindow.extractBaseline=extractBaseline;'});await checkpoint('overview');
 }else{
  await page.waitForFunction(()=>Ext.ComponentQuery.query('app-main').length&&Ext.ComponentQuery.query('mainlist')[0]?.getStore().getCount()===4);await page.evaluate(theme=>window.acceptanceTheme=theme,theme);await checkpoint('home-tall');
  const first=await page.evaluate(()=>'#'+Ext.ComponentQuery.query('mainlist')[0].getView().getNodes()[0].id+' .x-grid-cell:first-child');await page.locator(first).click();await page.waitForFunction(()=>Ext.Msg.isVisible());await checkpoint('selection-confirm');
  const no=await page.evaluate(()=>'#'+Ext.Msg.down('button[itemId=no]').el.id);await page.locator(no).click();await page.waitForFunction(()=>!Ext.Msg.isVisible());await checkpoint('confirm-no');
  for(let i=1;i<4;i++){const selector=await page.evaluate(i=>'#'+Ext.ComponentQuery.query('app-main')[0].items.getAt(i).tab.el.id,i);await page.locator(selector).click();await page.waitForFunction(i=>{const m=Ext.ComponentQuery.query('app-main')[0];return m.items.indexOf(m.getActiveTab())===i;},i);await checkpoint('tab-'+i);}
  await page.setViewportSize({width:1600,height:900});await page.waitForFunction(()=>Ext.ComponentQuery.query('app-main')[0].getHeaderPosition()==='left');await checkpoint('wide-responsive');
 }
 const declared=new Set([...manifest.js,...manifest.css,...(manifest.loadOrder||[])].filter(x=>x.path).map(x=>new URL(x.path,base+prefix).href.split('?')[0]));
 const unexpected=responses.filter(r=>['script','stylesheet'].includes(r.type)&&r.url.startsWith(base)&&!r.url.startsWith(base+prefix)&&!declared.has(r.url.split('?')[0]));
 const mixedModes=responses.filter(r=>r.url.startsWith(base+'build/')&&!r.url.startsWith(base+prefix));unexpected.push(...mixedModes);
 fs.writeFileSync(path.join(folder,'network.json'),JSON.stringify({errors,bad,unexpected,responses,entry:url}));if(errors.length||bad.length||unexpected.length)throw Error(JSON.stringify({name,scope,mode,dpr,theme,errors,bad,unexpected}));
 console.log(JSON.stringify({browser:name,scope,mode,dpr,theme,status:'PASS'}));await context.close();
}
fs.writeFileSync(path.join(A,(probe?'native-probe-':'native-pages-')+name+'.json'),JSON.stringify({status:'PASS',browser:config,records},null,2));await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
