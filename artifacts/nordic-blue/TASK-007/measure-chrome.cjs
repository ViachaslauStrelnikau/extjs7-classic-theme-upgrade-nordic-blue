const fs=require('node:fs');
const {chromium}=require('C:/Users/Damned/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true,args:['--disable-gpu','--force-color-profile=srgb']});
 const page=await browser.newPage({viewport:{width:1280,height:1600},locale:'en-US',timezoneId:'Europe/Minsk'});
 await page.goto('http://127.0.0.1:51752/theme-lab/index.html?theme=nordic',{waitUntil:'networkidle'});
 await page.waitForFunction(()=>window.themeLab);await page.evaluate(()=>themeLab.whenReady());
 const evidence=await page.evaluate(()=>{
  const toBox=r=>[Math.floor(r.left),Math.floor(r.top),Math.ceil(r.right),Math.ceil(r.bottom)];
  const select=toBox(document.querySelector('#lab-theme').getBoundingClientRect());
  const element=document.querySelector('#lab-status'),old=element.textContent;
  const rows=[['all','normal'],...Object.entries(themeLab.cases).flatMap(([c,v])=>v.states.map(s=>[c,s]))];
  const rectsByScenario={};
  for(const [c,s]of rows){
   const bounds=[];
   for(const theme of ['classic','nordic']){
    const prefix='Ready · '+c+'/'+s+' · SDK 7.7.0.31 · ';
    element.textContent=prefix+theme+' · 2026-10-23';
    const range=document.createRange();range.setStart(element.firstChild,prefix.length);range.setEnd(element.firstChild,element.textContent.length);
    bounds.push(toBox(range.getBoundingClientRect()));
   }
   const suffix=[Math.min(...bounds.map(r=>r[0])),Math.min(...bounds.map(r=>r[1])),Math.max(...bounds.map(r=>r[2])),Math.max(...bounds.map(r=>r[3]))];
   rectsByScenario[c+'/'+s]=[select,suffix];
  }
  element.textContent=old;
  return{selectors:['#lab-theme (native HTML select)','#lab-status text range: theme name and following date only'],rectsByScenario,headerRect:toBox(document.querySelector('.lab-shell').getBoundingClientRect()),stageRect:toBox(document.querySelector('#lab-stage').getBoundingClientRect()),policy:'Only native lab metadata outside the Ext fixture; status prefix and every other pixel remain compared. Rects measured with DOM Range for each case/state in both profile labels. Raw images are never edited.'};
 });
 fs.writeFileSync(__dirname+'/lab-chrome.json',JSON.stringify(evidence,null,2));console.log(JSON.stringify({scenarios:Object.keys(evidence.rectsByScenario).length,overview:evidence.rectsByScenario['all/normal']}));await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
