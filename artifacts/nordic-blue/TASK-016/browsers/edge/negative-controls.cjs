const fs=require('node:fs'),path=require('node:path');const{chromium}=require('C:/Users/Damned/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{const browser=await require('./browser-options.cjs').launch();
for(const dpr of [1,2]){const context=await browser.newContext({viewport:{width:1280,height:1600},deviceScaleFactor:dpr,locale:'en-US',timezoneId:'Europe/Minsk',reducedMotion:'reduce',colorScheme:'light'});const page=await context.newPage();
 await page.goto(`${process.env.NORDIC_LAB_URL||'http://127.0.0.1:51752/theme-lab/'}index.html?theme=nordic&case=button&state=normal`,{waitUntil:'networkidle'});await page.evaluate(()=>themeLab.whenReady());await page.addScriptTag({content:fs.readFileSync(path.join(__dirname,'extract.js'),'utf8')+'\nwindow.extractBaseline=extractBaseline;'});
 const dir=path.join(__dirname,'negative-controls','dpr-'+dpr);fs.mkdirSync(dir,{recursive:true});
 const save=async name=>{await page.evaluate(()=>themeLab.whenReady());fs.writeFileSync(path.join(dir,name+'.json'),JSON.stringify(await page.evaluate(()=>extractBaseline())));await page.screenshot({path:path.join(dir,name+'.png'),animations:'disabled',caret:'hide'});};
 await save('before');
 for(const kind of ['shift-1px','font-size']){
  await page.evaluate(kind=>{const c=themeLab.component('button.normal'),el=kind==='font-size'?c.btnInnerEl.dom:c.el.dom;window.controlElement=el;window.controlOriginal=el.getAttribute('style');if(kind==='shift-1px')el.style.transform='translateX(1px)';else el.style.fontSize=(parseFloat(getComputedStyle(el).fontSize)+1)+'px';},kind);
  await save(kind);await page.evaluate(()=>{if(controlOriginal===null)controlElement.removeAttribute('style');else controlElement.setAttribute('style',controlOriginal);delete window.controlElement;delete window.controlOriginal;});await save(kind+'-restored');
 }
 await context.close();
}await browser.close();})().catch(e=>{console.error(e);process.exit(1)});
