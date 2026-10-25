const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {chromium}=require('C:/Users/Damned/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const out=__dirname,dpr=Number(process.argv[2]||1),extract=fs.readFileSync(path.join(out,'extract.js'),'utf8');
const targets=['button.normal','button.menu','button.split','toolbar.first'];
const states=['normal','hover','focus','pressed','focus-over','focus-pressed','disabled'];
(async()=>{
 const browser=await require('./browser-options.cjs').launch();
 const records=[],actions=[];
 for(const theme of ['classic','nordic']){
  const context=await browser.newContext({viewport:{width:1280,height:1600},deviceScaleFactor:dpr,locale:'en-US',timezoneId:'Europe/Minsk',reducedMotion:'reduce',colorScheme:'light'});
  const page=await context.newPage();let errors=[],bad=[];page.on('pageerror',e=>errors.push(String(e)));page.on('response',r=>{if(r.status()>=400)bad.push(r.url())});
  async function open(name,state='normal'){
   errors=[];bad=[];await page.mouse.up();await page.mouse.move(1279,1599);
   await page.goto(`${process.env.NORDIC_LAB_URL||'http://127.0.0.1:51752/theme-lab/'}index.html?theme=${theme}&case=${name}&state=${state}`,{waitUntil:'networkidle'});
   await page.waitForFunction(()=>window.themeLab||window.labBoot?.status==='ERROR');
   await page.evaluate(()=>themeLab.whenReady());await page.addScriptTag({content:extract+'\nwindow.extractBaseline=extractBaseline;'});
  }
  for(const target of targets){
   await open(target.startsWith('toolbar')?'toolbar':'button');
   for(const state of states){
    await page.mouse.up();await page.mouse.move(1279,1599);
    await page.evaluate(id=>{const c=themeLab.component(id);c.enable();c.blur();c.toggle(false,true);if(c.menu)c.hideMenu();},target);
    if(state==='pressed'||state==='focus-pressed'){
     await page.locator(`[data-lab-id="${target}"]`).hover();await page.mouse.down();
     if(state==='pressed')await page.evaluate(id=>themeLab.component(id).blur(),target);
    }
    if(state.startsWith('focus'))await page.evaluate(id=>themeLab.component(id).focus(),target);
    if(state==='hover'||state==='focus-over')await page.locator(`[data-lab-id="${target}"]`).hover();
    if(state==='disabled')await page.evaluate(id=>themeLab.component(id).disable(),target);
    await page.evaluate(()=>themeLab.whenReady());
    const metrics=await page.evaluate(()=>extractBaseline());
    const flags=await page.evaluate(id=>{const c=themeLab.component(id);return{pressed:c.el.hasCls('x-btn-pressed'),disabled:!!c.disabled,focus:!!c.hasFocus,classes:c.el.dom.className};},target);
    if(flags.disabled!==(state==='disabled')||flags.pressed!==['pressed','focus-pressed'].includes(state)||flags.focus!==state.startsWith('focus'))throw Error('Wrong actual state '+JSON.stringify({theme,target,state,flags}));
    if(errors.length||bad.length||metrics.errors.length||metrics.duplicates.length)throw Error(JSON.stringify({errors,bad,metricsErrors:metrics.errors}));
    const folder=path.join(out,'core-states-v3','dpr-'+dpr,theme);fs.mkdirSync(folder,{recursive:true});
    const stem=target+'--'+state;await page.screenshot({path:path.join(folder,stem+'.png'),animations:'disabled',caret:'hide'});
    fs.writeFileSync(path.join(folder,stem+'.json'),JSON.stringify({theme,target,state,dpr,flags,metrics,errors,bad}));
    records.push({theme,target,state,dpr,path:path.relative(out,path.join(folder,stem+'.json')),screenshot:path.relative(out,path.join(folder,stem+'.png'))});
   }
  }
  // Exercise existing component APIs and genuine mouse/keyboard entry points.
  await open('button');
  for(const target of ['button.menu','button.split']){
   const box=await page.locator(`[data-lab-id="${target}"]`).boundingBox();await page.mouse.click(box.x+box.width-5,box.y+box.height/2);await page.evaluate(()=>themeLab.whenReady());
   const visible=await page.evaluate(id=>themeLab.component(id).menu.isVisible(),target);if(!visible)throw Error('Menu arrow did not open '+target);
   await page.evaluate(id=>themeLab.component(id).menu.items.first().focus(),target);
   await page.keyboard.press('Escape');await page.waitForFunction(id=>!themeLab.component(id).menu.isVisible(),target);await page.evaluate(()=>themeLab.whenReady());
   const closed=await page.evaluate(id=>!themeLab.component(id).menu.isVisible(),target);if(!closed)throw Error('Escape did not close '+target);
   actions.push({theme,dpr,action:target+' mouse arrow + focus menu item + Escape',passed:true});
  }
  await page.evaluate(()=>themeLab.component('button.normal').focus());await page.keyboard.press('Space');await page.evaluate(()=>themeLab.whenReady());
  if(!await page.evaluate(()=>themeLab.component('button.normal').pressed))throw Error('Space did not toggle button');
  actions.push({theme,dpr,action:'default button focus + Space toggles',passed:true});
  await open('toolbar','overflow');
  const selector=await page.evaluate(()=>{const c=themeLab.component('toolbar.main').getLayout().overflowHandler.menuTrigger;return '#'+c.el.id;});
  await page.locator(selector).click();await page.evaluate(()=>themeLab.whenReady());
  if(!await page.evaluate(()=>themeLab.component('toolbar.main').getLayout().overflowHandler.menu.isVisible()))throw Error('Overflow did not open');
  await page.evaluate(()=>themeLab.component('toolbar.main').getLayout().overflowHandler.menu.items.first().focus());
  await page.keyboard.press('Escape');await page.waitForFunction(()=>!themeLab.component('toolbar.main').getLayout().overflowHandler.menu.isVisible());actions.push({theme,dpr,action:'toolbar overflow mouse + focus menu item + Escape',passed:true});
  await open('panel');
  const collapseSelector=await page.evaluate(()=>{const c=themeLab.component('panel.main');return '#'+c.collapseTool.el.id;});
  await page.locator(collapseSelector).click();await page.evaluate(()=>themeLab.whenReady());if(!await page.evaluate(()=>!!themeLab.component('panel.main').collapsed))throw Error('Panel did not collapse');
  await page.locator(collapseSelector).click();await page.evaluate(()=>themeLab.whenReady());if(await page.evaluate(()=>!!themeLab.component('panel.main').collapsed))throw Error('Panel did not expand');
  actions.push({theme,dpr,action:'panel collapse + expand mouse',passed:true});
  if(errors.length||bad.length)throw Error(JSON.stringify({errors,bad}));
  await context.close();
 }
 fs.writeFileSync(path.join(out,'core-states-v3','dpr-'+dpr,'index.json'),JSON.stringify({status:'PASS',dpr,browser:await browser.version(),records,actions},null,2));
 console.log(JSON.stringify({status:'PASS',dpr,states:records.length,actions:actions.length}));await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
