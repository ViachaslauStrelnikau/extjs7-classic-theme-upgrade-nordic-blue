const fs=require('node:fs'),path=require('node:path');
const {chromium}=require('C:/Users/Damned/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const out=__dirname,dpr=Number(process.argv[2]||1),extract=fs.readFileSync(path.join(out,'extract.js'),'utf8');
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true,args:['--disable-gpu','--force-color-profile=srgb']});
 const records=[];
 for(const theme of ['classic','nordic']){
  const context=await browser.newContext({viewport:{width:1280,height:1600},deviceScaleFactor:dpr,locale:'en-US',timezoneId:'Europe/Minsk',reducedMotion:'reduce',colorScheme:'light'});
  const page=await context.newPage();let errors=[],bad=[];
  page.on('pageerror',e=>errors.push(String(e)));page.on('response',r=>{if(r.status()>=400)bad.push(r.url())});
  const input=async id=>page.locator(await page.evaluate(id=>'#'+themeLab.component(id).inputEl.id,id));
  const clickPart=async(id,part)=>{const selector=await page.evaluate(({id,part})=>{
   const c=themeLab.component(id);let el;
   if(part==='up'||part==='down')el=c.getTrigger('spinner')[part+'El'];
   else if(part==='collapse')el=c.toggleCmp.el;
   else if(part==='checkbox')el=c.checkboxCmp.inputEl;
   else el=c.getTrigger(part).el;
   return '#'+el.id;
  },{id,part});await page.locator(selector).click();};
  async function open(name,state='normal'){
   errors=[];bad=[];await page.mouse.move(1279,1599);
   await page.goto(`http://127.0.0.1:51752/theme-lab/index.html?theme=${theme}&case=${name}&state=${state}`,{waitUntil:'networkidle'});
   await page.waitForFunction(()=>window.themeLab||window.labBoot?.status==='ERROR');
   await page.evaluate(()=>themeLab.whenReady());await page.addScriptTag({content:extract+'\nwindow.extractBaseline=extractBaseline;'});
  }
  async function check(action,assertion){
   await page.evaluate(()=>themeLab.whenReady());
   const flags=await page.evaluate(()=>{
    const ids=['form.text','form.combo','form.date','form.time','form.number','form.notes','triggers.combo','triggers.date','triggers.spinner','triggers.clear','checks.unchecked','checks.checked','checks.disabled','checks.radio-a','checks.radio-b','fieldset.collapsible','fieldset.checkbox'];const result={};
    for(const id of ids){const c=themeLab.components.get(id);if(!c)continue;const v=c.getValue?c.getValue():null;result[id]={value:v instanceof Date?Ext.Date.format(v,'Y-m-d H:i'):v,raw:c.getRawValue?c.getRawValue():null,disabled:!!c.disabled,readOnly:!!c.readOnly,collapsed:!!c.collapsed,expanded:!!c.isExpanded,valid:c.isValid?c.isValid():null};}
    return result;
   });
   if(!assertion(flags))throw Error('Unexpected action result '+JSON.stringify({theme,dpr,action,flags}));
   const metrics=await page.evaluate(()=>extractBaseline());
   if(errors.length||bad.length||metrics.errors.length||metrics.duplicates.length)throw Error(JSON.stringify({errors,bad,metricsErrors:metrics.errors}));
   const folder=path.join(out,'form-actions','dpr-'+dpr,theme);fs.mkdirSync(folder,{recursive:true});
   await page.screenshot({path:path.join(folder,action+'.png'),animations:'disabled',caret:'hide'});
   const file=path.join(folder,action+'.json');fs.writeFileSync(file,JSON.stringify({theme,dpr,action,flags,metrics,errors,bad}));
   records.push({theme,dpr,action,path:path.relative(out,file),screenshot:path.relative(out,path.join(folder,action+'.png')),passed:true});
   console.log(JSON.stringify({theme,dpr,action,status:'PASS'}));
  }
  await open('form');
  await (await input('form.text')).fill('Nordic revised');await page.keyboard.press('Tab');
  await check('text-input',s=>s['form.text'].value==='Nordic revised');
  await (await input('form.notes')).fill('First line\nSecond line\nThird line');await page.keyboard.press('Tab');
  await check('textarea-input',s=>s['form.notes'].value==='First line\nSecond line\nThird line');
  await (await input('form.date')).fill('11/15/2026');await page.keyboard.press('Tab');
  await check('date-input',s=>s['form.date'].value==='2026-11-15 00:00');
  await clickPart('form.time','picker');
  const timeNode=await page.evaluate(()=>{const p=themeLab.component('form.time').getPicker();const r=p.getStore().findRecord('disp','10:00',0,false,true,true);if(!r)throw Error('Time record missing');return {selector:'#'+p.el.id+' .x-boundlist-item',index:p.getStore().indexOf(r)};});
  await page.locator(timeNode.selector).nth(timeNode.index).click();
  await check('time-picker-selection',s=>s['form.time'].raw==='10:00');
  await (await input('form.number')).focus();await page.keyboard.press('ArrowUp');
  await check('number-keyboard-up',s=>s['form.number'].value===8);
  await page.keyboard.press('ArrowDown');await check('number-keyboard-down',s=>s['form.number'].value===7);
  await (await input('form.number')).fill('20');await page.keyboard.press('ArrowUp');await check('number-max-bound',s=>s['form.number'].value===20);
  await (await input('form.text')).fill('');await page.keyboard.press('Tab');await check('required-invalid',s=>s['form.text'].valid===false);
  await open('form','readonly');await (await input('form.text')).focus();await page.keyboard.press('Control+a');await page.keyboard.type('Blocked');await page.keyboard.press('Tab');
  await check('readonly-blocks-input',s=>s['form.text'].readOnly&&s['form.text'].value==='Ada Nordic');
  await open('form','disabled');
  if(!await (await input('form.text')).isDisabled())throw Error('Disabled input is enabled');
  await check('disabled-input-state',s=>s['form.text'].disabled&&s['form.text'].value==='Ada Nordic');
  await open('triggers');await clickPart('triggers.combo','picker');await check('combo-open',s=>s['triggers.combo'].expanded);
  await page.keyboard.press('ArrowDown');await page.keyboard.press('Enter');
  await check('combo-keyboard-selection',s=>s['triggers.combo'].value==='Beta'&&!s['triggers.combo'].expanded);
  await clickPart('triggers.spinner','up');await check('spinner-mouse-up',s=>s['triggers.spinner'].value===6);
  await clickPart('triggers.spinner','down');await check('spinner-mouse-down',s=>s['triggers.spinner'].value===5);
  await clickPart('triggers.clear','clear');await check('clear-trigger',s=>s['triggers.clear'].value==='');
  await clickPart('triggers.date','picker');
  const next=await page.evaluate(()=>'#'+themeLab.component('triggers.date').getPicker().nextEl.id);await page.locator(next).click();
  const day=await page.evaluate(()=>{const p=themeLab.component('triggers.date').getPicker();return '#'+p.el.id+' .x-datepicker-active .x-datepicker-date';});
  await page.locator(day).filter({hasText:/^15$/}).click();
  await check('date-picker-next-select',s=>s['triggers.date'].value==='2026-11-15 00:00'&&!s['triggers.date'].expanded);
  await open('checks');await (await input('checks.unchecked')).focus();await page.keyboard.press('Space');await check('checkbox-space-on',s=>s['checks.unchecked'].value===true);
  await page.keyboard.press('Space');await check('checkbox-space-off',s=>s['checks.unchecked'].value===false);
  await (await input('checks.radio-a')).focus();await page.keyboard.press('ArrowDown');await check('radio-arrow-selection',s=>s['checks.radio-a'].value===false&&s['checks.radio-b'].value===true);
  if(!await (await input('checks.disabled')).isDisabled())throw Error('Disabled checkbox enabled');await check('checkbox-disabled-state',s=>s['checks.disabled'].value===true&&s['checks.disabled'].disabled);
  await open('fieldset');await clickPart('fieldset.collapsible','collapse');await check('fieldset-collapse',s=>s['fieldset.collapsible'].collapsed);
  await clickPart('fieldset.collapsible','collapse');await check('fieldset-expand',s=>!s['fieldset.collapsible'].collapsed);
  await clickPart('fieldset.checkbox','checkbox');await check('fieldset-checkbox-expand',s=>!s['fieldset.checkbox'].collapsed);
  await clickPart('fieldset.checkbox','checkbox');await check('fieldset-checkbox-collapse',s=>s['fieldset.checkbox'].collapsed);
  await context.close();
 }
 const folder=path.join(out,'form-actions','dpr-'+dpr);fs.writeFileSync(path.join(folder,'index.json'),JSON.stringify({status:'PASS',dpr,browser:await browser.version(),records},null,2));await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
