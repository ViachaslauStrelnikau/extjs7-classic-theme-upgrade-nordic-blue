const fs=require('node:fs'),path=require('node:path');const{chromium}=require('C:/Users/Damned/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const O=__dirname,extract=fs.readFileSync(path.join(O,'extract.js'),'utf8'),paint=fs.readFileSync(path.join(O,'paint.js'),'utf8');
(async()=>{
const browser=await chromium.launch({channel:'msedge',headless:true,args:['--disable-gpu','--force-color-profile=srgb']});
for(const dpr of[1,2]){
 const context=await browser.newContext({viewport:{width:1280,height:1600},deviceScaleFactor:dpr,locale:'en-US',timezoneId:'Europe/Minsk',colorScheme:'light',reducedMotion:'reduce'}),page=await context.newPage();let errors=[],bad=[];
 page.on('pageerror',e=>errors.push(String(e)));page.on('response',r=>{if(r.status()>=400)bad.push(r.url())});
 async function open(theme){await page.goto(`${process.env.NORDIC_LAB_URL||'http://127.0.0.1:51752/theme-lab/'}index.html?theme=${theme}&case=tree&state=normal`,{waitUntil:'networkidle'});await page.evaluate(()=>themeLab.whenReady());await page.addScriptTag({content:extract+'\n'+paint+'\nwindow.extractBaseline=extractBaseline;window.collectPaint=collectPaint;window.normalizePaint=normalizePaint;'});}
 await open('classic');const ref=await page.evaluate(()=>collectPaint());
 for(const kind of['icon-shift-1px','adjacent-text-shift-1px','icon-artwork-filter']){
  await open('nordic');await page.evaluate(()=>collectPaint());
  const folder=path.join(O,'negative-controls','dpr-'+dpr,kind);fs.mkdirSync(folder,{recursive:true});
  const clip=await page.evaluate(()=>{const y=document.querySelector('#lab-stage').getBoundingClientRect().top;return{x:0,y,width:1280,height:1600-y};});
  const before=await page.evaluate(()=>extractBaseline());
  await page.screenshot({path:path.join(folder,'before.png'),clip,animations:'disabled',caret:'hide'});
  const install=async()=>page.evaluate(kind=>{const root=document.querySelector('[data-lab-id="tree.main/row/folder-alpha"]'),el=root.querySelector(kind==='adjacent-text-shift-1px'?'.x-tree-node-text':'.x-tree-icon');if(!el)throw Error('Missing control target');window.visualControl={el,style:el.getAttribute('style'),before:el.getBoundingClientRect().toJSON()};if(kind==='icon-artwork-filter')el.style.filter='brightness(0)';else{el.style.position='relative';el.style.left='1px';}return {before:visualControl.before,after:el.getBoundingClientRect().toJSON()};},kind);
  const rects=await install();if(kind.includes('shift')&&(rects.after.x!==rects.before.x+1||rects.after.width!==rects.before.width||rects.after.height!==rects.before.height))throw Error('Control did not move exactly 1 CSS px');
  const mutated=await page.evaluate(()=>extractBaseline());await page.screenshot({path:path.join(folder,'mutated-raw.png'),clip,animations:'disabled',caret:'hide'});
  await page.evaluate(()=>{const{el,style}=visualControl;if(style===null)el.removeAttribute('style');else el.setAttribute('style',style);delete window.visualControl;});await page.evaluate(()=>themeLab.whenReady());const restored=await page.evaluate(()=>extractBaseline());await page.screenshot({path:path.join(folder,'restored.png'),clip,animations:'disabled',caret:'hide'});
  await install();await page.evaluate(r=>normalizePaint(r),ref);await page.screenshot({path:path.join(folder,'mutated-normalized.png'),clip,animations:'disabled',caret:'hide'});
  fs.writeFileSync(path.join(folder,'metrics.json'),JSON.stringify({dpr,kind,rects,before,mutated,restored,errors,bad}));console.log(JSON.stringify({dpr,kind,status:'CAPTURED'}));
 }
 await context.close();
}await browser.close();})().catch(e=>{console.error(e);process.exit(1)});
