function extractBaseline() {
    const nodes=new Map(),ids=new Map(),duplicates=[];
    function add(el,id,source){
        if(!el||el.nodeType!==1)return;
        if(nodes.has(el))return;
        if(ids.has(id)&&ids.get(id)!==el){duplicates.push(id);return;}
        nodes.set(el,{id,source});ids.set(id,el);
    }
    function dom(x){return x&&(x.dom||x.el&&x.el.dom);}
    function slug(s){return String(s).replace(/<[^>]*>/g,'').trim().toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');}
    document.querySelectorAll('[data-lab-id]').forEach(el=>add(el,el.dataset.labId,'fixture-semantic-id'));
    themeLab.editors.filter(e=>e.initialized&&e.getDoc()).forEach(e=>add(e.getDoc().body,'editor.main/content','fixture-iframe-body'));
    for(const [id,c]of themeLab.components)if(c.isXType&&c.isXType('tabpanel'))add(dom(c.tabBar),id+'/tab-bar','owning-tab-panel-bar');
    function menu(c,id){
        if(!c||!c.rendered||!c.el)return;add(c.el.dom,id,'owned-menu');
        if(c.items)c.items.each(item=>{
            const key=item.initialConfig.itemId||item.text||item.xtype;
            if(key)add(dom(item),id+'/item/'+slug(key),'menu-item-config');
            if(item.menu)menu(item.menu,id+'/submenu/'+slug(key));
        });
    }
    for(const [id,c] of themeLab.components){
        for(const key of ['labelEl','labelTextEl','errorWrapEl','errorEl','bodyWrap','innerEl','endEl','frameBody','inputCell','triggerCell','triggerEl','titleEl','btnWrap','btnIconEl','iconEl','collapseTool','tabBar','header','body','iframeEl'])add(dom(c[key]),id+'/ref/'+key,'component-child-reference');
        if(c.menu)menu(c.menu,id+'/menu');
        if(c.headerCt&&c.headerCt.menu)menu(c.headerCt.menu,id+'/header-menu');
        if(c.getLayout){const layout=c.getLayout();if(layout&&layout.overflowHandler&&layout.overflowHandler.menu)menu(layout.overflowHandler.menu,id+'/overflow-menu');}
        if(c.picker&&c.picker.rendered){
            const picker=c.picker;add(dom(picker),id+'/picker-panel','existing-picker');
            if(picker.getNodes)for(const n of picker.getNodes()){
                const record=picker.getRecord(n),key=record&&record.get(c.displayField||'field1');
                if(key!==undefined)add(n,id+'/option/'+slug(key),'option-display-value');
            }
        }
        if(c.getView&&c.getVisibleColumnManager){
            const view=c.getView(),columns=c.getVisibleColumnManager().getColumns();
            for(const node of view.getNodes()){
                const record=view.getRecord(node);if(!record)continue;
                for(const column of columns){const cell=view.getCell(record,column);add(cell&&(cell.dom||cell),id+'/cell/'+record.getId()+'/'+(column.dataIndex||column.initialConfig.itemId),'record-id-and-column-dataIndex');}
            }
        }
        if(c.loadMask&&c.loadMask.el){
            add(c.loadMask.el.dom,id+'/load-mask','target-load-mask');
            for(const ref of ['msgWrapEl','msgEl','msgInnerEl','maskEl'])add(dom(c.loadMask[ref]),id+'/load-mask/'+ref,'load-mask-child-reference');
        }
        if(c.isXType&&c.isXType('htmleditor')&&c.getToolbar()){
            const bar=c.getToolbar();add(dom(bar),id+'/toolbar','editor-toolbar');
            const actions=bar.items.items;
            const actionKey=item=>item&&(item.initialConfig.itemId||item.initialConfig.name||item.text||item.xtype);
            actions.forEach((item,i)=>{
                const separator=item.isXType('tbseparator');
                const key=separator?'separator-between-'+actionKey(actions[i-1])+'-and-'+actionKey(actions[i+1]):actionKey(item);
                if(key)add(dom(item),id+'/editor-action/'+slug(key),separator?'separator-adjacent-named-actions':'editor-action-config');
            });
            const doc=c.getDoc();if(doc){doc.querySelectorAll('p,b').forEach(el=>{const key=el.tagName.toLowerCase();if(doc.querySelectorAll(key).length===1)add(el,id+'/content/'+key,'fixed-editor-content');});}
        }
        if(c.isXType&&c.isXType('datepicker')&&c.el){
            c.el.dom.querySelectorAll('.x-datepicker-date').forEach(el=>{
                const value=el.dateValue||(el.firstChild&&el.firstChild.dateValue)||(el.parentElement&&el.parentElement.dateValue);
                if(!value)return;const d=new Date(value),date=d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');
                add(el,id+'/date/'+date,'calendar-date-value');add(el.closest('td'),id+'/date-cell/'+date,'calendar-date-value');
            });
        }
    }
    const roles={
        'native-text-input':'.x-form-text',
        'label-text':'.x-form-item-label-text','label-inner':'.x-form-item-label-inner',
        'field-error':'.x-form-error-msg','picker-trigger':'.x-form-trigger-default:not(.x-form-spinner)',
        'spinner-up':'.x-form-spinner-up','spinner-down':'.x-form-spinner-down',
        'button-inner':'.x-btn-inner','button-wrap':'.x-btn-wrap','button-icon':'.x-btn-icon-el',
        'tab-inner':'.x-tab-inner','tab-wrap':'.x-tab-wrap','tab-close':'.x-tab-close-btn',
        'tool-image':'.x-tool-tool-el','header-text':'.x-column-header-text','header-trigger':'.x-column-header-trigger',
        'cell-inner':'.x-grid-cell-inner','tree-icon':'.x-tree-icon','tree-expander':'.x-tree-expander','tree-text':'.x-tree-node-text',
        'slider-inner':'.x-slider-inner','slider-end':'.x-slider-end','slider-thumb':'.x-slider-thumb',
        'menu-item-text':'.x-menu-item-text','menu-item-icon':'.x-menu-item-icon','menu-item-arrow':'.x-menu-item-arrow',
        'progress-bar':'.x-progress-bar','progress-text-front':'.x-progress-text:not(.x-progress-text-back)','progress-text-back':'.x-progress-text-back',
        'loadmask':'.x-mask','loadmask-message':'.x-mask-msg','loadmask-message-inner':'.x-mask-msg-inner','loadmask-text':'.x-mask-msg-text',
        'resize-north':'.x-resizable-north','resize-south':'.x-resizable-south','resize-east':'.x-resizable-east','resize-west':'.x-resizable-west',
        'resize-northeast':'.x-resizable-northeast','resize-northwest':'.x-resizable-northwest','resize-southeast':'.x-resizable-southeast','resize-southwest':'.x-resizable-southwest'
    };
    function owner(el){let p=el;while(p){if(nodes.has(p))return nodes.get(p).id;p=p.parentElement;}return null;}
    const roots=Array.from(nodes.entries()),rootOwners=new Map(nodes);
    function originalOwner(el){let p=el;while(p){if(rootOwners.has(p))return rootOwners.get(p).id;p=p.parentElement;}return null;}
    for(const [root,{id}] of roots)for(const [role,selector]of Object.entries(roles)){
        const list=Array.from(root.querySelectorAll(selector)).filter(el=>originalOwner(el.parentElement)===id);
        if(list.length===1)add(list[0],id+'/part/'+role,'unique-owned-role');
    }
    // Mask floats outside its target's DOM; associate through the target's live LoadMask object.
    for(const [id,c]of themeLab.components){if(c.loadMask&&c.loadMask.el){add(c.loadMask.el.dom,id+'/load-mask','target-load-mask');}}
    if(themeLab.case==='window'&&themeLab.state==='modal'){
        const masks=Array.from(document.querySelectorAll('body>.x-mask')).filter(el=>el.getBoundingClientRect().width&&getComputedStyle(el).display!=='none');
        if(masks.length===1)add(masks[0],'window.main/modal-overlay','modal-window-mask');
    }
    // Include every image-bearing leaf, even when a stock widget does not publish it as a child ref.
    // Unique CSS roles under a named semantic owner are stable; never use generated Ext IDs or DOM indices.
    const unownedGraphics=[];
    for(const el of document.body.querySelectorAll('*')){
        let graphic=el.tagName==='IMG';
        for(const pseudo of [null,'::before','::after']){
            const s=getComputedStyle(el,pseudo);if(pseudo&&(s.content==='none'||s.content==='normal'))continue;
            if(/url\(/.test(s.backgroundImage))graphic=true;
        }
        if(!graphic||nodes.has(el))continue;
        const parentId=owner(el.parentElement);
        if(!parentId){if(el.closest('#lab-stage')&&el.getBoundingClientRect().width)unownedGraphics.push({classes:el.className,tag:el.tagName});continue;}
        const preferred=['x-form-checkbox','x-form-radio','x-form-cb-input','x-grid-checkcolumn','x-column-header-text-inner'];
        const key=preferred.find(k=>el.classList.contains(k))||Array.from(el.classList).filter(k=>k.startsWith('x-')).sort().join('.')||el.tagName.toLowerCase();
        add(el,parentId+'/graphic/'+key,'unique-image-bearing-css-role');
    }
    const properties=['fontFamily','fontSize','fontWeight','fontStyle','fontStretch','lineHeight','letterSpacing','wordSpacing','textTransform','textAlign','textIndent','whiteSpace','overflow','overflowX','overflowY','textOverflow','verticalAlign','paddingTop','paddingRight','paddingBottom','paddingLeft','marginTop','marginRight','marginBottom','marginLeft','borderTopWidth','borderRightWidth','borderBottomWidth','borderLeftWidth','borderTopStyle','borderRightStyle','borderBottomStyle','borderLeftStyle','borderTopColor','borderRightColor','borderBottomColor','borderLeftColor','borderTopLeftRadius','borderTopRightRadius','borderBottomLeftRadius','borderBottomRightRadius','boxSizing','width','height','minWidth','minHeight','maxWidth','maxHeight','position','top','left','right','bottom','transform','display','visibility','opacity','pointerEvents','zIndex','color','backgroundColor','backgroundImage','backgroundSize','backgroundPositionX','backgroundPositionY','backgroundRepeat','boxShadow','outlineStyle','outlineWidth','outlineOffset','outlineColor','content'];
    function rect(el){const r=el.getBoundingClientRect();return{x:r.x,y:r.y,width:r.width,height:r.height};}
    function urls(image){return Array.from(image.matchAll(/url\(["']?([^"')]+)["']?\)/g)).map(m=>{try{const u=new URL(m[1],location.href);return u.pathname+u.search}catch(e){return m[1]}});}
    function style(el,pseudo){const s=el.ownerDocument.defaultView.getComputedStyle(el,pseudo);return Object.fromEntries(properties.map(k=>[k,s[k]]));}
    function visible(el){let n=el;while(n){const s=n.ownerDocument.defaultView.getComputedStyle(n);if(s.display==='none'||s.visibility==='hidden'||s.opacity==='0')return false;n=n.parentElement;}const r=rect(el);return r.width>0&&r.height>0;}
    const elements=[],icons=[];
    for(const [el,meta]of nodes){
        const r=rect(el),css=style(el),entry={...meta,tag:el.tagName,role:el.getAttribute('role'),coordinateSpace:el.ownerDocument===document?'viewport':'editor-iframe',visible:visible(el),rect:r,client:{width:el.clientWidth,height:el.clientHeight},scroll:{width:el.scrollWidth,height:el.scrollHeight},computed:css,pseudos:[]};
        entry.softRadius=el.matches('.x-window')?4:el.matches('.x-btn,.x-form-text,.x-boundlist,.x-menu')?3:0;
        entry.reviewedShadows=[{"selector": ".nb-soft-float", "key": "[[false,0.0,5.0,16.0,0.0]]"}, {"selector": ".x-panel-header-default,\n.x-panel-header-default-framed,\n.x-window-header-default", "key": "[[true,3.0,0.0,0.0,0.0]]"}, {"selector": ".x-btn-default-small,\n.x-btn-default-toolbar-small", "key": "none"}, {"selector": ".x-btn-default-small.x-btn-pressed,\n.x-btn-default-toolbar-small.x-btn-pressed", "key": "[[true,0.0,1.0,2.0,0.0]]"}, {"selector": ".x-btn-default-small.x-btn-focus,\n.x-btn-default-toolbar-small.x-btn-focus", "key": "[[true,0.0,0.0,0.0,1.0]]"}, {"selector": ".nb-primary.x-btn-default-small.x-btn-focus,\n.nb-primary.x-btn-default-toolbar-small.x-btn-focus", "key": "[[true,0.0,0.0,0.0,1.0]]"}, {"selector": ".x-btn-default-small.x-btn-disabled,\n.x-btn-default-toolbar-small.x-btn-disabled", "key": "none"}, {"selector": ".x-form-text-default", "key": "none"}, {"selector": ".x-form-trigger-wrap-focus", "key": "[[true,0.0,0.0,0.0,1.0]]"}, {"selector": ".x-form-trigger-wrap-invalid", "key": "[[true,0.0,0.0,0.0,1.0]]"}, {"selector": ".x-grid-header-ct,\n.x-column-header", "key": "[[true,0.0,-1.0,0.0,0.0]]"}, {"selector": ".x-grid-cell-focused", "key": "[[true,0.0,0.0,0.0,1.0]]"}, {"selector": ".x-tab-default-top", "key": "none"}, {"selector": ".x-tab-default.x-tab-active", "key": "[[true,0.0,-3.0,0.0,0.0]]"}, {"selector": ".x-tab-default.x-tab-focus", "key": "[[true,0.0,0.0,0.0,1.0]]"}, {"selector": ".x-tab-default.x-tab-disabled", "key": "none"}, {"selector": ".x-column-header", "key": "[[true,0.0,-1.0,0.0,0.0]]"}, {"selector": ".x-column-header-first", "key": "[[true,0.0,-1.0,0.0,0.0]]"}, {"selector": ".x-grid-item-selected .x-grid-cell:first-child", "key": "[[true,3.0,0.0,0.0,0.0]]"}, {"selector": ".x-grid-item-selected .x-grid-cell-focused:first-child", "key": "[[true,3.0,0.0,0.0,0.0],[true,0.0,0.0,0.0,1.0]]"}, {"selector": ".x-tab-default.x-tab-active.x-tab-focus", "key": "[[true,0.0,-3.0,0.0,0.0],[true,0.0,0.0,0.0,1.0]]"}, {"selector": ".x-window-default.nb-soft-float", "key": "[[false,0.0,8.0,24.0,0.0]]"}, {"selector": ":root .x-column-header", "key": "none"}, {"selector": ":root .x-column-header.x-group-header", "key": "none"}, {"selector": ":root .x-column-header-over,\n:root .x-column-header-sort-ASC,\n:root .x-column-header-sort-DESC", "key": "none"}, {"selector": ":root .x-grid-item-over .x-grid-cell", "key": "[[true,0.0,1.0,0.0,0.0],[true,0.0,-1.0,0.0,0.0]]"}, {"selector": ":root .x-grid-item-selected .x-grid-cell", "key": "[[true,0.0,1.0,0.0,0.0],[true,0.0,-1.0,0.0,0.0]]"}, {"selector": ":root .x-grid-item-selected .x-grid-cell-first", "key": "[[true,2.0,0.0,0.0,0.0],[true,0.0,1.0,0.0,0.0],[true,0.0,-1.0,0.0,0.0]]"}, {"selector": ":root .x-grid-item-selected .x-grid-cell-last", "key": "[[true,-1.0,0.0,0.0,0.0],[true,0.0,1.0,0.0,0.0],[true,0.0,-1.0,0.0,0.0]]"}, {"selector": ":root .x-menu-item-active", "key": "[[true,3.0,0.0,0.0,0.0]]"}].filter(rule=>el.matches(rule.selector)).map(rule=>rule.key);entry.reviewedOutline=el.matches(':root .x-grid-item .x-grid-cell-focused,:root .x-btn-focus');entry.reviewedHeaderStripe=el.matches(':root .x-grid-header-ct');
        entry.reviewedFlatInput=el.matches('.x-form-text-default:not(.x-form-invalid-field):not(.x-form-invalid-field-default)');
        if('value'in el)entry.value=el.value;
        if('checked'in el)entry.checked=el.checked;
        for(const pseudo of ['::before','::after']){const ps=style(el,pseudo);if(ps.content!=='none'&&ps.content!=='normal'){const p={pseudo,rect:null,hostRect:r,computed:ps,note:'CSS pseudo-element has no native DOMRect API; host rect and exact computed box/offsets recorded, no fabricated coordinates.'};entry.pseudos.push(p);if(urls(ps.backgroundImage).length)icons.push({id:meta.id+pseudo,source:'pseudo-background',hostRect:r,cssBox:[ps.width,ps.height],offset:[ps.backgroundPositionX,ps.backgroundPositionY],size:ps.backgroundSize,repeat:ps.backgroundRepeat,resources:urls(ps.backgroundImage),visible:entry.visible,opacity:ps.opacity});}}
        if(urls(css.backgroundImage).length)icons.push({id:meta.id,source:'background',rect:r,cssBox:[css.width,css.height],offset:[css.backgroundPositionX,css.backgroundPositionY],size:css.backgroundSize,repeat:css.backgroundRepeat,resources:urls(css.backgroundImage),visible:entry.visible,opacity:css.opacity});
        if(el.tagName==='IMG'){const src=el.getAttribute('src');icons.push({id:meta.id,source:'img',rect:r,natural:[el.naturalWidth,el.naturalHeight],resources:src?[new URL(src,el.ownerDocument.location.href).pathname]:[],visible:entry.visible});}
        elements.push(entry);
    }
    elements.sort((a,b)=>a.id<b.id?-1:a.id>b.id?1:0);icons.sort((a,b)=>a.id<b.id?-1:a.id>b.id?1:0);
    const active=document.activeElement,activeId=active&&owner(active);
    return{schemaVersion:1,case:themeLab.case,state:themeLab.state,environment:themeLab.environment(),fixtureSemanticCount:themeLab.snapshot().length,elementCount:elements.length,visibleElementCount:elements.filter(e=>e.visible).length,duplicates,unownedGraphics,elements,icons,activeElement:activeId,scroll:[scrollX,scrollY],data:themeLab.fixedData,stores:themeLab.stores.map(s=>({count:s.getCount(),total:s.getTotalCount(),page:s.currentPage||null,records:s.getRange().map(r=>({id:r.getId(),name:r.get('name')||r.get('text')||null}))})),errors:themeLab.errors};
}
