const fs=require('node:fs'),path=require('node:path');
const {chromium}=require('C:/Users/Damned/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const out=__dirname,dpr=Number(process.argv[2]||1),extract=fs.readFileSync(path.join(out,'extract.js'),'utf8');
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true,args:['--disable-gpu','--force-color-profile=srgb']});const records=[];
 for(const theme of ['classic','nordic']){
  const context=await browser.newContext({viewport:{width:1280,height:1600},deviceScaleFactor:dpr,locale:'en-US',timezoneId:'Europe/Minsk',reducedMotion:'reduce',colorScheme:'light'});
  const page=await context.newPage();let errors=[],bad=[];
  page.on('pageerror',e=>errors.push(String(e)));page.on('response',r=>{if(r.status()>=400)bad.push(r.url())});
  async function open(state='normal'){
   errors=[];bad=[];await page.mouse.up();await page.mouse.move(1279,1599);
   await page.goto(`${process.env.NORDIC_LAB_URL||'http://127.0.0.1:51752/theme-lab/'}index.html?theme=${theme}&case=window&state=${state}`,{waitUntil:'networkidle'});
   await page.evaluate(()=>themeLab.whenReady());await page.addScriptTag({content:extract+'\nwindow.extractBaseline=extractBaseline;'});
  }
  async function check(action,assertion){
   await page.evaluate(()=>themeLab.whenReady());
   const flags=await page.evaluate(()=>{const c=themeLab.component('window.main');return {visible:c.isVisible(),width:c.getWidth(),height:c.getHeight(),position:c.getPosition(),modal:!!c.modal,focusInside:c.el.dom.contains(document.activeElement)};});
   if(!assertion(flags))throw Error('Unexpected '+JSON.stringify({theme,dpr,action,flags}));
   const metrics=await page.evaluate(()=>extractBaseline());if(errors.length||bad.length||metrics.errors.length||metrics.duplicates.length)throw Error(JSON.stringify({errors,bad,metrics:metrics.errors}));
   const folder=path.join(out,'window-actions','dpr-'+dpr,theme);fs.mkdirSync(folder,{recursive:true});
   const file=path.join(folder,action+'.json');fs.writeFileSync(file,JSON.stringify({theme,dpr,action,flags,metrics,errors,bad}));await page.screenshot({path:path.join(folder,action+'.png'),animations:'disabled',caret:'hide'});
   records.push({theme,dpr,action,path:path.relative(out,file),passed:true});console.log(JSON.stringify({theme,dpr,action,status:'PASS'}));
  }
  await open();const initial=await page.evaluate(()=>themeLab.component('window.main').getPosition());console.log(JSON.stringify({initial}));
  let point=await page.evaluate(()=>{const r=themeLab.component('window.main').header.el.dom.getBoundingClientRect();return {x:r.x+80,y:r.y+r.height/2};});
  await page.mouse.move(point.x,point.y);await page.mouse.down();await page.mouse.move(point.x+60,point.y-30,{steps:12});await page.mouse.up();await page.mouse.move(1279,1599);
  await check('window-title-drag',s=>s.position[0]===initial[0]+60&&s.position[1]===initial[1]-30&&s.width===440&&s.height===240);
  const handle=await page.evaluate(()=>themeLab.component('window.main').resizer.southeast.id);
  let box=await page.locator('#'+handle).boundingBox();point={x:box.x+box.width/2,y:box.y+box.height/2};
  await page.mouse.move(point.x,point.y);await page.mouse.down();await page.mouse.move(point.x+50,point.y+30,{steps:12});await page.mouse.up();await page.mouse.move(1279,1599);
  await check('window-border-resize',s=>s.width===490&&s.height===270);
  const close=await page.evaluate(()=>'#'+themeLab.component('window.main').tools.find(t=>t.type==='close').el.id);await page.locator(close).click();await check('window-close-tool',s=>!s.visible);
  await open();await page.evaluate(()=>themeLab.component('window.ok').focus());await page.keyboard.press('Escape');await check('window-keyboard-escape',s=>!s.visible);
  await open('modal');await page.evaluate(()=>themeLab.component('window.ok').focus());
  for(let i=0;i<8;i++){await page.keyboard.press('Tab');await check('modal-tab-'+i,s=>s.visible&&s.modal&&s.focusInside);}
  await page.keyboard.press('Shift+Tab');await check('modal-reverse-tab',s=>s.focusInside);
  await page.keyboard.press('Escape');await check('modal-escape',s=>!s.visible);
  await context.close();
 }
 const folder=path.join(out,'window-actions','dpr-'+dpr);fs.writeFileSync(path.join(folder,'index.json'),JSON.stringify({status:'PASS',dpr,browser:await browser.version(),records},null,2));await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});

