const fs=require('node:fs'),path=require('node:path');
const {chromium}=require('C:/Users/Damned/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const out=__dirname,dpr=Number(process.argv[2]||1),extract=fs.readFileSync(path.join(out,'extract.js'),'utf8');
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true,args:['--disable-gpu','--force-color-profile=srgb']});const records=[];
 for(const theme of ['classic','nordic']){
  const context=await browser.newContext({viewport:{width:1280,height:1600},deviceScaleFactor:dpr,locale:'en-US',timezoneId:'Europe/Minsk',reducedMotion:'reduce',colorScheme:'light'});
  const page=await context.newPage();let errors=[],bad=[];
  page.on('pageerror',e=>errors.push(String(e)));page.on('response',r=>{if(r.status()>=400)bad.push(r.url())});
  const el=id=>{
   const m=id.match(/^(grid|tree)\.main\/cell\/([^/]+)\/([^/]+)(.*)$/);
   if(!m)return page.locator(`[data-lab-id="${id}"]`);
   const col=m[1]==='tree'?1:({name:1,team:2,salary:3,active:4}[m[3]]);
   let selector=`[data-lab-id="${m[1]}.main/row/${m[2]}"] .x-grid-cell:nth-child(${col})`;
   if(m[4].includes('x-grid-checkcolumn'))selector+=' .x-grid-checkcolumn';
   else if(m[4].includes('tree-expander'))selector+=' .x-tree-expander';
   else if(m[4].includes('tree-text'))selector+=' .x-tree-node-text';
   return page.locator(selector);
  };
  async function open(name,state='normal'){
   errors=[];bad=[];await page.mouse.up();await page.mouse.move(1279,1599);
   await page.goto(`${process.env.NORDIC_LAB_URL||'http://127.0.0.1:51752/theme-lab/'}index.html?theme=${theme}&case=${name}&state=${state}`,{waitUntil:'networkidle'});
   await page.waitForFunction(()=>window.themeLab||window.labBoot?.status==='ERROR');await page.evaluate(()=>themeLab.whenReady());
   await page.addScriptTag({content:extract+'\nwindow.extractBaseline=extractBaseline;'});
  }
  async function check(action,assertion){
   await page.evaluate(()=>themeLab.whenReady());
   const flags=await page.evaluate(()=>{
    const result={};
    for(const id of ['grid.main','tree.main','paging.main']){
     const c=themeLab.components.get(id);if(!c)continue;const s=c.getStore(),sort=s.getSorters().first(),p=c.getView().getScrollable().getPosition();
     result[id]={selected:c.getSelectionModel().getSelection().map(r=>r.getId()),page:s.currentPage,sort:sort?{property:sort.getProperty(),direction:sort.getDirection()}:null,records:s.getRange().map(r=>({id:r.getId(),name:r.get('name')||null,active:r.get('active')??null})),widths:c.headerCt.items.items.map(h=>h.getWidth()),scroll:{x:p.x,y:p.y},menuVisible:!!(c.headerCt.menu&&c.headerCt.menu.isVisible())};
     if(id==='tree.main')result[id].alphaExpanded=s.getNodeById('folder-alpha').isExpanded();
     if(id==='paging.main'){const t=themeLab.component('paging.toolbar');result[id].disabled=Object.fromEntries(['first','prev','next','last','refresh'].map(k=>[k,!!t.getComponent(k).disabled]));}
    }return result;
   });
   if(!assertion(flags))throw Error('Unexpected action '+JSON.stringify({theme,dpr,action,flags}));
   const metrics=await page.evaluate(()=>extractBaseline());if(errors.length||bad.length||metrics.errors.length||metrics.duplicates.length)throw Error(JSON.stringify({errors,bad,metricErrors:metrics.errors}));
   const folder=path.join(out,'grid-actions','dpr-'+dpr,theme);fs.mkdirSync(folder,{recursive:true});
   await page.screenshot({path:path.join(folder,action+'.png'),animations:'disabled',caret:'hide'});
   const file=path.join(folder,action+'.json');fs.writeFileSync(file,JSON.stringify({theme,dpr,action,flags,metrics,errors,bad}));
   records.push({theme,dpr,action,path:path.relative(out,file),screenshot:path.relative(out,path.join(folder,action+'.png')),passed:true});console.log(JSON.stringify({theme,dpr,action,status:'PASS'}));
  }
  await open('grid');
  await el('grid.name/textEl').click();await check('grid-sort-asc',s=>s['grid.main'].sort?.direction==='ASC');
  await el('grid.name/textEl').click();await check('grid-sort-desc',s=>s['grid.main'].sort?.direction==='DESC');
  await open('grid');await el('grid.main/cell/person-01/name').click();await check('grid-row-select',s=>s['grid.main'].selected[0]==='person-01');
  await page.keyboard.press('ArrowDown');await check('grid-keyboard-next-row',s=>s['grid.main'].selected[0]==='person-02');
  const initialActive=await page.evaluate(()=>themeLab.component('grid.main').getStore().getById('person-01').get('active'));
  await el('grid.main/cell/person-01/active/part/cell-inner/graphic/x-grid-checkcolumn').click();await check('grid-checkcolumn-toggle',s=>s['grid.main'].records[0].active===!initialActive);
  await el('grid.name/titleEl').hover();const trigger=await page.evaluate(()=>'#'+themeLab.component('grid.name').triggerEl.id);await page.locator(trigger).click();await check('grid-header-menu-open',s=>s['grid.main'].menuVisible);
  await page.evaluate(()=>themeLab.component('grid.main').headerCt.menu.items.first().focus());await page.keyboard.press('Escape');await check('grid-header-menu-escape',s=>!s['grid.main'].menuVisible);
  await open('grid');
  const box=await page.evaluate(()=>{const r=themeLab.component('grid.name').el.dom.getBoundingClientRect();return {x:r.right-2,y:r.top+r.height/2};});
  await page.mouse.move(box.x,box.y);await page.mouse.down();await page.mouse.move(box.x+50,box.y,{steps:10});await page.mouse.up();await page.mouse.move(1279,1599);
  // Classic resizer uses pointer position relative to the header left edge:
  // 260 - 2 (inside edge) + 50 pixels = 308, not 310.
  await check('grid-column-resize-drag',s=>s['grid.main'].widths[0]===308);
  // Same existing component API on both themes to exercise overflowing viewports;
  // no fixture, application config, renderer, row height or column model edit.
  await page.evaluate(()=>themeLab.component('grid.main').setSize(480,160));await check('grid-compact-viewport',s=>s['grid.main'].widths[0]===308);
  await page.evaluate(()=>themeLab.component('grid.main').getView().getScrollable().scrollTo(90,44));await page.waitForFunction(()=>{const p=themeLab.component('grid.main').getView().getScrollable().getPosition();return p.x>0&&p.y>0;});
  await check('grid-scroll-both-axes',s=>s['grid.main'].scroll.x>0&&s['grid.main'].scroll.y>0);
  await open('tree');await el('tree.main/cell/folder-alpha/text/part/tree-expander').click();await check('tree-mouse-collapse',s=>!s['tree.main'].alphaExpanded);
  await el('tree.main/cell/folder-alpha/text/part/tree-expander').click();await check('tree-mouse-expand',s=>s['tree.main'].alphaExpanded);
  await el('tree.main/cell/leaf-1/text/part/tree-text').click();await check('tree-leaf-selection',s=>s['tree.main'].selected[0]==='leaf-1');
  await page.keyboard.press('ArrowDown');await check('tree-keyboard-next-leaf',s=>s['tree.main'].selected[0]==='leaf-2');
  await el('tree.main/cell/folder-alpha/text/part/tree-text').click();await page.keyboard.press('ArrowLeft');await check('tree-keyboard-collapse',s=>!s['tree.main'].alphaExpanded);
  await page.keyboard.press('ArrowRight');await check('tree-keyboard-expand',s=>s['tree.main'].alphaExpanded);
  await open('paging');await check('paging-first-boundary',s=>s['paging.main'].page===1&&s['paging.main'].disabled.first&&s['paging.main'].disabled.prev&&!s['paging.main'].disabled.next);
  await el('paging.toolbar/next').click();await check('paging-next',s=>s['paging.main'].page===2&&s['paging.main'].records[0].id==='person-09');
  await el('paging.toolbar/last').click();await check('paging-last-boundary',s=>s['paging.main'].page===4&&s['paging.main'].disabled.last&&s['paging.main'].disabled.next&&!s['paging.main'].disabled.prev);
  await el('paging.toolbar/prev').click();await check('paging-previous',s=>s['paging.main'].page===3&&s['paging.main'].records[0].id==='person-17');
  await el('paging.toolbar/first').click();await check('paging-first',s=>s['paging.main'].page===1&&s['paging.main'].records[0].id==='person-01');
  await el('paging.toolbar/inputItem/inputEl').fill('3');await page.keyboard.press('Enter');await check('paging-input-enter',s=>s['paging.main'].page===3&&s['paging.main'].records[0].id==='person-17');
  await el('paging.toolbar/refresh').click();await check('paging-refresh',s=>s['paging.main'].page===3&&s['paging.main'].records[0].id==='person-17');
  await context.close();
 }
 const folder=path.join(out,'grid-actions','dpr-'+dpr);fs.writeFileSync(path.join(folder,'index.json'),JSON.stringify({status:'PASS',dpr,browser:await browser.version(),records},null,2));await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
