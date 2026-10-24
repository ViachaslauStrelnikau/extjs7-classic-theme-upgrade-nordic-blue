function collectPaint(){
 const docs=[document,...themeLab.editors.filter(e=>e.initialized&&e.getDoc()).map(e=>e.getDoc())];
 const props=['color','backgroundColor','borderTopColor','borderRightColor','borderBottomColor','borderLeftColor','outlineColor','boxShadow','textShadow','textDecorationColor','backgroundImage'];
 return docs.map((doc,d)=>[doc.body,...doc.body.querySelectorAll('*')].map((el,i)=>{
  el.setAttribute('data-visual-node',`d${d}-n${i}`);
  const get=p=>{const s=doc.defaultView.getComputedStyle(el,p);return Object.fromEntries(props.map(k=>[k,s[k]]));};
  const r=el.getBoundingClientRect(),frame=doc.defaultView.frameElement,fr=frame?.getBoundingClientRect();
  return {key:`d${d}-n${i}`,tag:el.tagName,rect:{x:r.x+(fr?fr.x+frame.clientLeft:0),y:r.y+(fr?fr.y+frame.clientTop:0),width:r.width,height:r.height},style:get(null),before:get('::before'),after:get('::after'),img:el.tagName==='IMG'?el.src:null};
 }));
}
function normalizePaint(reference){
 const docs=[document,...themeLab.editors.filter(e=>e.initialized&&e.getDoc()).map(e=>e.getDoc())];
 const transparent=s=>s==='transparent'||/rgba\([^)]*,\s*0\s*\)$/.test(s);
 const neutral=(s,bg=false)=>transparent(s)?'rgba(0, 0, 0, 0)':bg?'rgb(255, 255, 255)':'rgb(0, 0, 0)';
 const layers=s=>{let depth=0,start=0,result=[];for(let i=0;i<s.length;i++){if(s[i]==='(')depth++;if(s[i]===')')depth--;if(s[i]===','&&!depth){result.push(s.slice(start,i));start=i+1;}}result.push(s.slice(start));return result.filter(x=>!x.includes('gradient(')).join(',')||'none';};
 const cssName=s=>s.replace(/[A-Z]/g,m=>'-'+m.toLowerCase());let preserved=0,removed=0;
 docs.forEach((doc,d)=>{
  let rules='';const nodes=[doc.body,...doc.body.querySelectorAll('*')];
  if(nodes.length!==reference[d].length)throw Error('Normalization DOM count mismatch');
  nodes.forEach((el,i)=>{
   const ref=reference[d][i];if(el.tagName!==ref.tag||el.getAttribute('data-visual-node')!==ref.key)throw Error('Normalization node mismatch '+ref.key);
   for(const [suffix,rs] of [['',ref.style],['::before',ref.before],['::after',ref.after]]){
    const original=doc.defaultView.getComputedStyle(el,suffix||null).backgroundImage,kept=layers(original);
    preserved+=(original.match(/url\(/g)||[]).length;removed+=(original.match(/gradient\(/g)||[]).length;
    let declarations='';
    for(const [prop,value] of Object.entries(rs)){
     let v;if(prop==='backgroundImage')v=kept;
     else if(prop==='boxShadow'||prop==='textShadow')v=value.replace(/rgba?\([^)]*\)|#[0-9a-fA-F]{3,8}\b/g,'rgb(0, 0, 0)');
     else v=neutral(value,prop==='backgroundColor');
     declarations+=cssName(prop)+':'+v+'!important;';
    }
    rules+=`[data-visual-node="${ref.key}"]${suffix}{${declarations}}\n`;
   }
  });const style=doc.createElement('style');style.dataset.visualNormalization='true';style.textContent=rules;doc.head.appendChild(style);
 });return {preservedUrlLayers:preserved,removedGradientLayers:removed};
}
function supportPlane(allowed){
 const docs=[document,...themeLab.editors.filter(e=>e.initialized&&e.getDoc()).map(e=>e.getDoc())];
 docs.forEach((doc,d)=>{
  let rules='html,body,*{color:transparent!important;background-color:transparent!important;border-color:transparent!important;outline-color:transparent!important;box-shadow:none!important;text-shadow:none!important;text-decoration-color:transparent!important}*::before,*::after{color:transparent!important;background-color:transparent!important;border-color:transparent!important;outline-color:transparent!important;box-shadow:none!important;text-shadow:none!important}::-webkit-scrollbar,::-webkit-scrollbar-thumb,::-webkit-scrollbar-track,::-webkit-scrollbar-button,::-webkit-scrollbar-corner{background:transparent!important;border-color:transparent!important;color:transparent!important}';
  for(const el of [doc.body,...doc.body.querySelectorAll('*')]){
   const key=el.getAttribute('data-visual-node');
   for(const suffix of ['', '::before','::after']){
    rules+=`[data-visual-node="${key}"]${suffix}{color:transparent!important;background-color:transparent!important;border-color:transparent!important;outline-color:transparent!important;box-shadow:none!important;text-shadow:none!important;text-decoration-color:transparent!important}`;
    if(!allowed.includes(key+suffix))rules+=`[data-visual-node="${key}"]${suffix}{background-image:none!important}`;
   }
   if(el.tagName==='IMG'&&!allowed.includes(key+'@img'))rules+=`[data-visual-node="${key}"]{opacity:0!important}`;
  }
  const style=doc.createElement('style');style.textContent=rules;doc.head.appendChild(style);
 });
}
function planeBackground(color){
 const docs=[document,...themeLab.editors.filter(e=>e.initialized&&e.getDoc()).map(e=>e.getDoc())];
 for(const doc of docs)doc.documentElement.style.setProperty('background-color',color,'important');
}
