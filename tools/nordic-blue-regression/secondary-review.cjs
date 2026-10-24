const fs=require('node:fs'),path=require('node:path');
const {chromium}=require('C:/Users/Damned/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const out=__dirname,dpr=Number(process.argv[2]||1),extract=fs.readFileSync(path.join(out,'extract.js'),'utf8');
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true,args:['--disable-gpu','--force-color-profile=srgb']});const records=[];
 for(const theme of ['classic','nordic']){
  const frozen=JSON.parse(fs.readFileSync(path.join(out,theme==='classic'?'classic-frozen-resources.json':'nordic-frozen-resources.json')));
  const context=await browser.newContext({viewport:{width:1280,height:1600},deviceScaleFactor:dpr,locale:'en-US',timezoneId:'Europe/Minsk',reducedMotion:'reduce',colorScheme:'light'});
  await context.route('**/*',async route=>{const u=route.request().url(),m=u.match(/\/resources\/(images\/[^?#]+)/),key=m&&m[1];if(key&&frozen[key]&&/\/(?:sdk\/build\/classic\/theme-classic|build\/theme-lab\/(?:classic|nordic)\/testing)\/resources\//.test(new URL(u).pathname))await route.fulfill({status:200,contentType:'image/png',body:fs.readFileSync(path.join(out,frozen[key].derivedPng))});else await route.continue();});
  const page=await context.newPage();let errors=[],bad=[];
  page.on('pageerror',e=>errors.push(String(e)));page.on('response',r=>{if(r.status()>=400)bad.push(r.url())});
  async function open(name,state='normal'){
   errors=[];bad=[];await page.mouse.up();await page.mouse.move(1279,1599);
   await page.goto(`${process.env.NORDIC_LAB_URL||'http://127.0.0.1:51752/theme-lab/'}index.html?theme=${theme}&case=${name}&state=${state}`,{waitUntil:'networkidle'});
   await page.waitForFunction(()=>window.themeLab||window.labBoot?.status==='ERROR');await page.evaluate(()=>themeLab.whenReady());await page.addScriptTag({content:extract+'\nwindow.extractBaseline=extractBaseline;'});
  }
  async function check(action,assertion){
   await page.evaluate(()=>themeLab.whenReady());
   const flags=await page.evaluate(()=>{
    const get=id=>themeLab.components.get(id),r={};let c;
    if(c=get('tabs.main'))r.tabs={active:c.getActiveTab().initialConfig.itemId,pages:c.items.items.map(p=>p.initialConfig.itemId),disabled:c.items.items.filter(p=>p.disabled).map(p=>p.initialConfig.itemId),scroll:c.tabBar.getLayout().overflowHandler.getScrollPosition?.()||0};
    if(c=get('menu.main'))r.menu={checked:get('menu.checked').checked,unchecked:get('menu.unchecked').checked,submenu:get('menu.parent').menu.isVisible(),disabled:get('menu.disabled').disabled};
    if(c=get('datepicker.main'))r.datepicker={value:Ext.Date.format(c.getValue(),'Y-m-d'),activeDay:Ext.Date.format(c.getActive(),'Y-m-d'),month:Ext.Date.format(c.getActive(),'Y-m'),monthPicker:!!(c.monthPicker&&c.monthPicker.isVisible()),disabled:!!c.disabled};
    if(c=get('progress.main'))r.progress={value:c.value,text:c.text};
    if(c=get('slider.horizontal'))r.slider={horizontal:c.getValue(),vertical:get('slider.vertical').getValue(),disabled:!!c.disabled};
    if(c=get('mask.main'))r.mask={visible:!!(c.loadMask&&c.loadMask.isVisible()),message:c.loadMask?.msg};return r;
   });
   if(!assertion(flags))throw Error('Unexpected action '+JSON.stringify({theme,dpr,action,flags}));
   const metrics=await page.evaluate(()=>extractBaseline());if(errors.length||bad.length||metrics.errors.length||metrics.duplicates.length)throw Error(JSON.stringify({errors,bad,metricErrors:metrics.errors}));
   const folder=path.join(out,'secondary-actions','dpr-'+dpr,theme);fs.mkdirSync(folder,{recursive:true});await page.screenshot({path:path.join(folder,action+'.png'),animations:'disabled',caret:'hide'});
   const file=path.join(folder,action+'.json');fs.writeFileSync(file,JSON.stringify({theme,dpr,action,flags,metrics,errors,bad}));records.push({theme,dpr,action,path:path.relative(out,file),screenshot:path.relative(out,path.join(folder,action+'.png')),passed:true});console.log(JSON.stringify({theme,dpr,action,status:'PASS'}));
  }
  const tabSelector=async(n,part='el')=>page.evaluate(({n,part})=>'#'+themeLab.component('tabs.page-'+n).tab[part].id,{n,part});
  await open('tabs');await page.locator(await tabSelector(1)).click();await check('tabs-mouse-select',s=>s.tabs.active==='lab-tabs--page-1');
  await page.locator(await tabSelector(3)).click({force:true});await check('tabs-disabled-ignored',s=>s.tabs.active==='lab-tabs--page-1'&&s.tabs.disabled.includes('lab-tabs--page-3'));
  await page.evaluate(()=>themeLab.component('tabs.page-0').tab.focus());await page.keyboard.press('ArrowRight');await check('tabs-keyboard-select',s=>s.tabs.active==='lab-tabs--page-1');
  await page.locator(await tabSelector(1,'closeEl')).click();await check('tabs-close-active',s=>!s.tabs.pages.includes('lab-tabs--page-1')&&s.tabs.pages.length===7);
  await open('tabs','overflow');const scroller=await page.evaluate(()=>'#'+themeLab.component('tabs.main').tabBar.getLayout().overflowHandler.getAfterScroller().id);await page.locator(scroller).click();
  await page.waitForFunction(()=>themeLab.component('tabs.main').tabBar.getLayout().overflowHandler.getScrollPosition()>0);await check('tabs-overflow-scroll',s=>s.tabs.scroll>0);
  await open('menu');await page.locator('[data-lab-id="menu.checked"]').click();await check('menu-checkbox-off',s=>s.menu.checked===false);
  await page.locator('[data-lab-id="menu.unchecked"]').click();await check('menu-checkbox-on',s=>s.menu.unchecked===true);
  await page.locator('[data-lab-id="menu.parent"]').hover();await page.waitForFunction(()=>themeLab.component('menu.parent').menu.isVisible());await check('menu-mouse-submenu',s=>s.menu.submenu);
  await open('menu');await page.evaluate(()=>themeLab.component('menu.parent').focus());await page.keyboard.press('ArrowRight');await page.waitForFunction(()=>themeLab.component('menu.parent').menu.isVisible());await check('menu-keyboard-submenu',s=>s.menu.submenu);
  await page.evaluate(()=>themeLab.component('menu.child').focus());await page.keyboard.press('ArrowLeft');await page.waitForFunction(()=>!themeLab.component('menu.parent').menu.isVisible());await check('menu-keyboard-return',s=>!s.menu.submenu);
  await page.locator('[data-lab-id="menu.disabled"]').click({force:true});await check('menu-disabled-state',s=>s.menu.disabled);
  await open('datepicker');const datePart=async part=>page.evaluate(part=>'#'+themeLab.component('datepicker.main')[part].id,part);
  await page.locator(await datePart('nextEl')).click();await check('datepicker-next-month',s=>s.datepicker.month==='2026-11');
  await page.locator(await datePart('prevEl')).click();await check('datepicker-prev-month',s=>s.datepicker.month==='2026-10');
  const dateRoot=await page.evaluate(()=>'#'+themeLab.component('datepicker.main').el.id);await page.locator(dateRoot+' .x-datepicker-active .x-datepicker-date').filter({hasText:/^15$/}).click();await check('datepicker-day-select',s=>s.datepicker.value==='2026-10-15');
  await page.evaluate(()=>themeLab.component('datepicker.main').focus());await page.keyboard.press('ArrowRight');await check('datepicker-keyboard-day',s=>s.datepicker.activeDay==='2026-10-16'&&s.datepicker.value==='2026-10-15');
  const today=await page.evaluate(()=>'#'+themeLab.component('datepicker.main').todayBtn.el.id);await page.locator(today).click();await check('datepicker-today',s=>s.datepicker.value==='2026-10-23');
  await open('progress');await page.evaluate(()=>themeLab.component('progress.main').updateProgress(1,'100% complete'));await check('progress-full',s=>s.progress.value===1&&s.progress.text==='100% complete');
  await page.evaluate(()=>themeLab.component('progress.main').updateProgress(0,'0% complete'));await check('progress-empty',s=>s.progress.value===0);
  await page.evaluate(()=>themeLab.component('progress.main').updateProgress(.42,'42% complete'));await check('progress-partial',s=>s.progress.value===.42);
  await open('slider');await page.evaluate(()=>themeLab.component('slider.horizontal').focus());await page.keyboard.press('ArrowRight');await check('slider-horizontal-keyboard',s=>s.slider.horizontal===43);
  await page.keyboard.press('End');await check('slider-horizontal-max',s=>s.slider.horizontal===100);await page.keyboard.press('Home');await check('slider-horizontal-min',s=>s.slider.horizontal===0);
  await page.evaluate(()=>themeLab.component('slider.vertical').focus());await page.keyboard.press('ArrowUp');await check('slider-vertical-keyboard',s=>s.slider.vertical===43);
  await open('slider');let box=await page.evaluate(()=>{const r=themeLab.component('slider.horizontal').thumbs[0].el.dom.getBoundingClientRect();return{x:r.x+r.width/2,y:r.y+r.height/2};});
  await page.mouse.move(box.x,box.y);await page.mouse.down();await page.mouse.move(box.x+60,box.y,{steps:10});await page.mouse.up();await check('slider-horizontal-drag',s=>s.slider.horizontal>42&&s.slider.horizontal<100);
  box=await page.evaluate(()=>{const r=themeLab.component('slider.vertical').thumbs[0].el.dom.getBoundingClientRect();return{x:r.x+r.width/2,y:r.y+r.height/2};});await page.mouse.move(box.x,box.y);await page.mouse.down();await page.mouse.move(box.x,box.y-40,{steps:10});await page.mouse.up();await check('slider-vertical-drag',s=>s.slider.vertical>42&&s.slider.vertical<100);
  await open('slider','disabled');await page.evaluate(()=>themeLab.component('slider.horizontal').focus());await page.keyboard.press('ArrowRight');await check('slider-disabled-ignored',s=>s.slider.disabled&&s.slider.horizontal===42);
  await open('mask');await check('mask-visible',s=>s.mask.visible);await page.evaluate(()=>themeLab.component('mask.main').setLoading(false));await check('mask-hide',s=>!s.mask.visible);
  await page.evaluate(()=>themeLab.component('mask.main').setLoading('Loading fixed data…'));await check('mask-show',s=>s.mask.visible&&s.mask.message==='Loading fixed data…');
  await context.close();
 }
 const folder=path.join(out,'secondary-actions','dpr-'+dpr);fs.writeFileSync(path.join(folder,'index.json'),JSON.stringify({status:'PASS',dpr,browser:await browser.version(),records},null,2));await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
