(function () {
    'use strict';
    const QUERY = new URLSearchParams(location.search);
    const selectedCase = QUERY.get('case') || 'all';
    const selectedState = QUERY.get('state') || 'normal';
    const rows = Array.from({length: 32}, (_, i) => ({
        id: 'person-' + String(i + 1).padStart(2, '0'),
        name: ['Ada', 'Boris', 'Clara', 'David'][i % 4] + ' ' + String(i + 1).padStart(2, '0'),
        team: ['Design', 'Engineering', 'Support', 'Sales'][i % 4],
        salary: 3000 + i * 125, active: i % 3 !== 0
    }));
    const tools = 'close minimize maximize restore toggle gear prev next pin unpin right left down up refresh plus minus search save help print expand collapse resize move expand-left expand-right expand-top expand-bottom collapse-left collapse-right collapse-top collapse-bottom'.split(' ');
    const cases = {
        panel: {title: 'Panel', states: ['normal', 'framed', 'collapsed', 'disabled', 'hover', 'focus']},
        window: {title: 'Window', states: ['normal', 'focus', 'modal', 'moved', 'resized']},
        button: {title: 'Button', states: ['normal', 'hover', 'focus', 'pressed', 'disabled', 'open']},
        toolbar: {title: 'Toolbar', states: ['normal', 'overflow', 'open', 'disabled']},
        form: {title: 'Form', states: ['normal', 'invalid', 'readonly', 'disabled', 'focus']},
        triggers: {title: 'Triggers', states: ['normal', 'hover', 'focus', 'pressed', 'disabled', 'open']},
        checks: {title: 'Checkbox/Radio', states: ['normal', 'checked', 'unchecked', 'disabled', 'focus']},
        fieldset: {title: 'Fieldset', states: ['normal', 'collapsed', 'checked', 'disabled']},
        editor: {title: 'HTML editor', states: ['normal', 'focus', 'readonly', 'disabled']},
        grid: {title: 'Grid', states: ['normal', 'hover', 'selected', 'focus', 'sort-asc', 'sort-desc', 'menu', 'resized', 'disabled']},
        paging: {title: 'Paging', states: ['normal', 'first', 'middle', 'last', 'disabled']},
        border: {title: 'BorderLayout', states: ['normal', 'collapsed', 'expanded']},
        tabs: {title: 'Tabs', states: ['normal', 'hover', 'selected', 'focus', 'overflow']},
        tree: {title: 'Tree', states: ['normal', 'collapsed', 'expanded', 'selected', 'focus', 'disabled']},
        datepicker: {title: 'DatePicker', states: ['normal', 'selected', 'prev', 'next', 'focus', 'disabled']},
        progress: {title: 'Progress', states: ['normal', 'partial', 'full']},
        slider: {title: 'Slider', states: ['normal', 'hover', 'focus', 'selected', 'disabled']},
        menu: {title: 'Menu', states: ['normal', 'open', 'checked', 'unchecked', 'focus', 'disabled']},
        tool: {title: 'Tool', states: ['normal', 'hover', 'focus', 'pressed', 'disabled']},
        mask: {title: 'Mask', states: ['normal', 'loading', 'hidden']}
    };
    const lab = window.themeLab = {
        schemaVersion: 1, fixtureVersion: 'theme-lab-v1', cases,
        case: selectedCase, state: selectedState, status: 'LOADING', errors: [],
        components: new Map(), stores: [], editors: [], pendingActions: [],
        fixedData: rows, clock: window.labClock, readinessRuns: 0,
        navigate(caseName, state = 'normal') {
            const url = new URL(location.href);url.searchParams.set('case', caseName);url.searchParams.set('state', state);location.href = url;
        },
        component(id) { const c = this.components.get(id);if (!c) throw new Error('Missing semantic component: ' + id);return c; },
        selector(id, part) { return '[data-lab-id="' + id + (part ? '/' + part : '') + '"]'; },
        snapshot() {
            const properties = ['fontFamily','fontSize','fontWeight','lineHeight','letterSpacing','textTransform','paddingTop','paddingRight','paddingBottom','paddingLeft','marginTop','marginRight','marginBottom','marginLeft','borderTopWidth','borderRightWidth','borderBottomWidth','borderLeftWidth','boxSizing','minWidth','minHeight','maxWidth','maxHeight'];
            let elements=Array.from(document.querySelectorAll('[data-lab-id]'));
            this.editors.filter(c=>c.initialized&&c.getDoc()&&c.getDoc().body).forEach(c=>{
                c.getDoc().body.dataset.labId='editor.main/content';elements.push(c.getDoc().body);
            });
            return elements.map(el => {
                const r = el.getBoundingClientRect(), s = getComputedStyle(el);
                return {id: el.dataset.labId, role: el.getAttribute('role'), coordinateSpace:el.ownerDocument===document?'viewport':'editor-iframe', visible: !!r.width && !!r.height && s.visibility !== 'hidden', rect: {x:r.x,y:r.y,width:r.width,height:r.height}, computed: Object.fromEntries(properties.map(k => [k,s[k]]))};
            }).sort((a,b) => a.id < b.id ? -1 : a.id > b.id ? 1 : 0);
        },
        environment() {
            return {sdk:Ext.getVersion().version, profile:labBoot.profile, date:new Date().toISOString(), timezone:Intl.DateTimeFormat().resolvedOptions().timeZone, uiLocale:'en-US', browserLocale:navigator.language, viewport:[innerWidth,innerHeight], dpr:devicePixelRatio, fonts:{Tahoma:document.fonts.check('12px Tahoma'),Arial:document.fonts.check('12px Arial')}, browser:navigator.userAgent};
        },
        async whenReady() {
            const start = performance.now(); let stable = 0, previous = '';
            await document.fonts.ready;
            while (performance.now() - start < 20000) {
                await new Promise(resolve => requestAnimationFrame(resolve));
                if (this.errors.length) throw new Error(this.errors.join('; '));
                if (this.editors.some(c => !c.initialized) || this.stores.some(s => s.isLoading()) || Ext.Component.runningLayoutContext || Ext.Component.layoutSuspendCount || this.pendingActions.length) { stable = 0; continue; }
                if (this.editors.some(c => c.getDoc() && c.getDoc().fonts && c.getDoc().fonts.status !== 'loaded')) { stable = 0; continue; }
                tagAll();
                const now = JSON.stringify(this.snapshot());
                stable = now === previous ? stable + 1 : 0; previous = now;
                if (stable >= 3) {
                    if (!this.components.size || !this.snapshot().length) throw new Error('Empty fixture');
                    this.status = 'READY'; this.readinessRuns++;
                    document.getElementById('lab-status').textContent = 'Ready · ' + this.case + '/' + this.state + ' · SDK ' + Ext.getVersion().version + ' · ' + labBoot.profile.theme + ' · 2026-10-23';
                    labBoot.status = 'READY'; return this.snapshot();
                }
            }
            throw new Error('Readiness timeout: editor/data/layout/pointer state pending ' + JSON.stringify(this.pendingActions));
        },
        async refreshEditor() {
            const editor = this.component('editor.main'); const value = editor.getValue();
            editor.updateLayout();editor.setValue(value);await this.whenReady();return value;
        }
    };
    // Public component API drivers. Mouse/keyboard are performed on semantic selectors by the caller.
    lab.actions={
        panelToggle(){const c=lab.component('panel.main');c.collapsed?c.expand(false):c.collapse(null,false);return lab.whenReady();},
        windowMove(x,y){lab.component('window.main').setPosition(x,y);return lab.whenReady();},
        windowResize(width,height){lab.component('window.main').setSize(width,height);return lab.whenReady();},
        windowClose(){lab.component('window.main').close();return lab.whenReady();},
        gridSelect(recordId){const c=lab.component('grid.main'),r=c.getStore().getById(recordId);if(!r)throw new Error('Unknown fixed record '+recordId);c.getSelectionModel().select(r);return lab.whenReady();},
        gridSort(direction){if(!['ASC','DESC'].includes(direction))throw new Error('Invalid sort direction');lab.component('grid.main').getStore().sort('name',direction);return lab.whenReady();},
        page(number){if(!Number.isInteger(number)||number<1||number>4)throw new Error('Page outside fixed data');lab.component('paging.main').getStore().loadPage(number);return lab.whenReady();},
        treeToggle(){const n=lab.component('tree.main').getStore().getNodeById('folder-alpha');n.isExpanded()?n.collapse():n.expand();return lab.whenReady();},
        dateMonth(delta){const c=lab.component('datepicker.main');if(delta===-1)c.showPrevMonth();else if(delta===1)c.showNextMonth();else throw new Error('Use month delta -1 or 1');return lab.whenReady();},
        menuToggle(){const c=lab.component('menu.checked');c.setChecked(!c.checked);return lab.whenReady();},
        sliderValue(value){if(value<0||value>100)throw new Error('Slider range 0..100');lab.component('slider.horizontal').setValue(value);return lab.whenReady();}
    };
    function named(id, cfg) { return Object.assign({itemId:'lab-' + id.replaceAll('.', '--')}, cfg); }
    function create(id, cfg, host) { return Ext.widget(named(id, Object.assign({renderTo:host}, cfg))); }
    function store(pageSize = 8) {
        const s = Ext.create('Ext.data.Store', {fields:['id','name','team','salary','active'],pageSize,proxy:{type:'memory',enablePaging:true,data:rows.map(r => Object.assign({}, r)),reader:{type:'json'}},autoLoad:false});
        lab.stores.push(s);s.loadPage(1);return s;
    }
    function tag(c, id) {
        if (!c.el || !c.el.dom) return;
        c.el.dom.dataset.labId = id;
        for (const p of ['inputEl','triggerWrap','body','header','titleEl','btnEl','btnInnerEl','arrowEl','textEl','innerWrap','inputWrap','tableWrap','bar','iframeEl','prevEl','nextEl','monthBtn','todayBtn']) {
            const el = c[p] && (c[p].dom || c[p].el && c[p].el.dom);
            if (el && el !== c.el.dom && !el.dataset.labId) el.dataset.labId = id + '/' + p;
        }
        if (c.isXType('pagingtoolbar')) {
            ['first','prev','next','last','refresh','inputItem','displayItem'].forEach(part => {
                const child=c.getComponent(part);if(child&&child.el)tag(child,id+'/'+part);
            });
        }
        if (c.isXType('gridpanel') || c.isXType('treepanel')) {
            const view=c.getView();if (!view) return;
            view.el.dom.dataset.labId=id+'/view';
            for (const node of view.getNodes()) {
                const record=view.getRecord(node);if (!record) continue;
                const rid=String(record.getId());node.dataset.labId=id+'/row/'+rid;
                c.getVisibleColumnManager().getColumns().forEach(col=>{const cell=view.getCell(record,col);if(cell&&cell.dom)cell.dom.dataset.labId=id+'/cell/'+rid+'/'+(col.dataIndex||col.initialConfig.itemId);});
            }
            c.headerCt.items.each(col=>{if(col.el)col.el.dom.dataset.labId=id+'/column/'+(col.dataIndex||col.initialConfig.itemId);});
        }
    }
    function tagAll() {
        Ext.ComponentManager.each((key,c) => {
            const item=c.initialConfig&&c.initialConfig.itemId;
            if (typeof item==='string' && item.startsWith('lab-')) { const id=item.slice(4).replaceAll('--', '.');lab.components.set(id,c);tag(c,id); }
        });
    }
    function target(c, part) { tagAll();const id=c.initialConfig.itemId.slice(4).replaceAll('--', '.');return lab.selector(id,part); }
    function pointer(c, state, part) {
        tagAll();const selector=target(c,part),el=document.querySelector(selector);
        if (!el) throw new Error('Pointer target missing '+selector);
        const action={kind:state==='pressed'?'mousedown':'hover',selector};lab.pendingActions.push(action);
        el.addEventListener(state==='pressed'?'mousedown':'mouseenter',()=>{lab.pendingActions=lab.pendingActions.filter(a=>a!==action);lab.whenReady().catch(fail);},{once:true,capture:true});
        document.getElementById('lab-status').textContent='Move pointer to the named component'+(state==='pressed'?' and hold the mouse button':'')+'; capture driver: '+selector;
    }
    function fail(e) { lab.errors.push(String(e));lab.status='ERROR';labBoot.status='ERROR';document.getElementById('lab-status').textContent=String(e);document.getElementById('lab-status').classList.add('lab-error'); }
    const factories={
        panel(host,state){
            const c=create('panel.main',{xtype:'panel',title:'Collapsible panel',width:580,height:230,frame:state==='framed',collapsible:true,animCollapse:false,collapsed:state==='collapsed',bodyPadding:12,html:'Stable panel content: Alpha / Beta',tools:[{type:'gear',itemId:'lab-panel--settings'}],buttons:[named('panel.save',{text:'Save'})]},host);
            if(state==='disabled')c.disable();if(state==='hover')pointer(c.down('tool[type=gear]'),'hover');if(state==='focus')c.down('button').focus();
        },
        window(host,state){
            host.style.height='460px';const pos=Ext.get(host).getXY();
            const c=create('window.main',{xtype:'window',title:'Window — move, resize, close',width:440,height:240,x:pos[0]+40,y:pos[1]+40,constrain:true,constrainTo:host,modal:state==='modal',resizable:true,draggable:true,closeAction:'hide',bodyPadding:12,html:'Drag the title; resize the border; Escape/close.',buttons:[named('window.ok',{text:'OK'}),named('window.cancel',{text:'Cancel'})]},host);c.show();
            if(state==='focus')c.down('button').focus();if(state==='moved')c.setPosition(pos[0]+150,pos[1]+75);if(state==='resized')c.setSize(530,290);
        },
        button(host,state){
            const c=create('button.row',{xtype:'container',width:1050,layout:{type:'hbox',align:'middle'},defaults:{margin:'0 12 0 0'},items:[named('button.normal',{xtype:'button',text:'Normal',enableToggle:true}),named('button.disabled',{xtype:'button',text:'Disabled',disabled:true}),named('button.menu',{xtype:'button',text:'Menu',menu:{items:[named('button.menu.option',{text:'Alpha'})]}}),named('button.split',{xtype:'splitbutton',text:'Split',menu:{items:[{text:'Beta'}]}})]},host);
            const b=c.items.first();if(state==='disabled')b.disable();if(state==='focus')b.focus();if(['hover','pressed'].includes(state))pointer(b,state);if(state==='open')c.items.getAt(2).showMenu();
        },
        toolbar(host,state){
            const c=create('toolbar.main',{xtype:'toolbar',width:state==='normal'?1100:340,layout:{overflowHandler:'menu'},items:[named('toolbar.first',{text:'Action 1'}),'-',...Array.from({length:9},(_,i)=>named('toolbar.action-'+i,{text:'Action '+(i+2)}))]},host);
            if(state==='disabled')c.disable();if(state==='open'){
                const handler=c.getLayout().overflowHandler;handler.menuTrigger.showMenu();
            }
        },
        form(host,state){
            const c=create('form.main',{xtype:'form',width:650,bodyPadding:12,defaults:{anchor:'100%',labelWidth:110},items:[
                named('form.text',{xtype:'textfield',fieldLabel:'Name',value:'Ada Nordic',allowBlank:false}),
                named('form.combo',{xtype:'combobox',fieldLabel:'Team',store:['Design','Engineering','Support'],value:'Design',editable:false}),
                named('form.date',{xtype:'datefield',fieldLabel:'Date',value:new Date(2026,9,23),format:'m/d/Y'}),
                named('form.time',{xtype:'timefield',fieldLabel:'Time',value:'09:30',format:'H:i',increment:30}),
                named('form.number',{xtype:'numberfield',fieldLabel:'Quantity',value:7,minValue:0,maxValue:20}),
                named('form.notes',{xtype:'textareafield',fieldLabel:'Notes',value:'Fixed multiline text.\nSecond line.',height:80})]},host);
            if(state==='invalid'){c.items.first().setValue('');c.items.first().validate();}if(state==='readonly')c.query('field').forEach(f=>f.setReadOnly(true));if(state==='disabled')c.disable();if(state==='focus')c.items.first().focus();
        },
        triggers(host,state){
            const c=create('triggers.main',{xtype:'container',width:700,layout:'anchor',defaults:{width:360,margin:'0 0 14 0'},items:[
                named('triggers.combo',{xtype:'combobox',fieldLabel:'Dropdown',store:['Alpha','Beta','Gamma'],value:'Alpha',queryMode:'local'}),
                named('triggers.date',{xtype:'datefield',fieldLabel:'Calendar',value:new Date(2026,9,23),format:'m/d/Y'}),
                named('triggers.spinner',{xtype:'numberfield',fieldLabel:'Spinner',value:5,minValue:0,maxValue:9}),
                named('triggers.search',{xtype:'textfield',fieldLabel:'Search',value:'Nordic',triggers:{search:{cls:'x-form-search-trigger'}}}),
                named('triggers.clear',{xtype:'textfield',fieldLabel:'Clear',value:'Alpha',triggers:{clear:{cls:'x-form-clear-trigger',handler:function(){this.setValue('');}}}})]},host);
            const b=c.items.first();if(state==='disabled')c.disable();if(state==='focus')b.focus();if(state==='open')b.expand();if(['hover','pressed'].includes(state)){
                tagAll();const t=b.getTrigger('picker').el.dom;t.dataset.labId='triggers.combo/picker';pointer(b,state,'picker');
            }
        },
        checks(host,state){
            const c=create('checks.main',{xtype:'container',width:600,layout:'anchor',items:[named('checks.unchecked',{xtype:'checkbox',boxLabel:'Unchecked',checked:false}),named('checks.checked',{xtype:'checkbox',boxLabel:'Checked',checked:true}),named('checks.disabled',{xtype:'checkbox',boxLabel:'Disabled checked',checked:true,disabled:true}),named('checks.radio-a',{xtype:'radio',name:'lab-radio',inputValue:'A',boxLabel:'Radio Alpha',checked:true}),named('checks.radio-b',{xtype:'radio',name:'lab-radio',inputValue:'B',boxLabel:'Radio Beta'})]},host);
            if(state==='checked')c.items.first().setValue(true);if(state==='unchecked')c.items.getAt(1).setValue(false);if(state==='disabled')c.disable();if(state==='focus')c.items.first().focus();
        },
        fieldset(host,state){
            const c=create('fieldset.main',{xtype:'container',width:650,items:[named('fieldset.collapsible',{xtype:'fieldset',title:'Collapsible fieldset',collapsible:true,collapsed:state==='collapsed',items:[named('fieldset.name',{xtype:'textfield',fieldLabel:'Name',value:'Alpha'})]}),named('fieldset.checkbox',{xtype:'fieldset',title:'Optional details',checkboxToggle:true,collapsed:state!=='checked',items:[{xtype:'textfield',fieldLabel:'Code',value:'N-042'}]})]},host);if(state==='disabled')c.disable();
        },
        editor(host,state){
            const c=create('editor.main',{xtype:'htmleditor',width:1120,height:290,value:'<p>Nordic Blue <b>fixed editor</b> content.</p>',enableFont:true},host);lab.editors.push(c);
            c.on('initialize',()=>{if(state==='readonly')c.setReadOnly(true);if(state==='disabled')c.disable();if(state==='focus')c.focus();});
        },
        grid(host,state){
            const s=store(8);const c=create('grid.main',{xtype:'grid',width:1120,height:330,store:s,stripeRows:true,selModel:{type:'rowmodel'},columns:[named('grid.name',{text:'Name',dataIndex:'name',width:260}),named('grid.team',{text:'Team',dataIndex:'team',width:260}),named('grid.salary',{text:'Salary',dataIndex:'salary',width:180}),named('grid.active',{xtype:'checkcolumn',text:'Active',dataIndex:'active',width:95})]},host);
            if(state==='selected')c.getSelectionModel().select(s.getById('person-03'));if(state==='sort-asc'||state==='sort-desc')s.sort('name',state==='sort-asc'?'ASC':'DESC');if(state==='resized')c.headerCt.items.first().setWidth(320);if(state==='disabled')c.disable();if(state==='focus')c.getView().focus();if(state==='hover'){
                tagAll();const node=c.getView().getNode(s.getAt(1));pointerTarget(node,'hover','grid.main/row/'+s.getAt(1).getId());
            }if(state==='menu'){const h=c.headerCt.items.first();c.headerCt.showMenuBy(null,h.el.dom,h);}
        },
        paging(host,state){
            const s=store(8);if(state==='middle')s.loadPage(2);if(state==='last')s.loadPage(4);
            const c=create('paging.main',{xtype:'grid',width:1120,height:320,store:s,columns:[{text:'Name',dataIndex:'name',width:350},{text:'Team',dataIndex:'team',width:300}],bbar:named('paging.toolbar',{xtype:'pagingtoolbar',store:s,displayInfo:true})},host);if(state==='disabled')c.disable();
        },
        border(host,state){
            create('border.main',{xtype:'panel',width:1120,height:450,layout:'border',items:[named('border.north',{region:'north',title:'North',height:80,split:true,collapsible:true,animCollapse:false}),named('border.south',{region:'south',title:'South',height:80,split:true,collapsible:true,animCollapse:false}),named('border.west',{region:'west',title:'West',width:190,split:true,collapsible:true,collapsed:state==='collapsed',animCollapse:false}),named('border.east',{region:'east',title:'East',width:190,split:true,collapsible:true,animCollapse:false}),named('border.center',{region:'center',title:'Center',html:'Fixed center content'})]},host);
        },
        tabs(host,state){
            const c=create('tabs.main',{xtype:'tabpanel',width:state==='overflow'?410:1120,height:250,activeTab:state==='selected'?1:0,items:Array.from({length:8},(_,i)=>named('tabs.page-'+i,{title:'Tab '+(i+1),closable:i!==0,disabled:i===3,html:'Fixed content '+(i+1)}))},host);
            c.tabBar.items.each((t,i)=>{t.initialConfig.itemId='lab-tabs--tab-'+i;});tagAll();if(state==='focus')c.tabBar.items.first().focus();if(state==='hover')pointer(c.tabBar.items.getAt(1),'hover');
        },
        tree(host,state){
            const s=Ext.create('Ext.data.TreeStore',{root:{id:'root',expanded:true,children:[{id:'folder-alpha',text:'Folder Alpha',expanded:state!=='collapsed',children:[{id:'leaf-1',text:'Leaf one',leaf:true},{id:'leaf-2',text:'Leaf two',leaf:true}]},{id:'folder-beta',text:'Folder Beta',expanded:false,children:[{id:'leaf-3',text:'Leaf three',leaf:true}]}]}});lab.stores.push(s);
            const c=create('tree.main',{xtype:'treepanel',width:650,height:280,rootVisible:false,useArrows:true,store:s,animate:false},host);if(state==='selected')c.getSelectionModel().select(s.getNodeById('leaf-1'));if(state==='disabled')c.disable();if(state==='focus')c.getView().focus();
        },
        datepicker(host,state){
            const c=create('datepicker.main',{xtype:'datepicker',value:new Date(2026,9,state==='selected'?15:23),showToday:true},host);if(state==='prev')c.showPrevMonth();if(state==='next')c.showNextMonth();if(state==='disabled')c.disable();if(state==='focus')c.focus();
        },
        progress(host,state){create('progress.main',{xtype:'progressbar',width:650,value:state==='full'?1:.42,text:state==='full'?'100% complete':'42% complete'},host);},
        slider(host,state){
            const c=create('slider.main',{xtype:'container',width:700,layout:'hbox',items:[named('slider.horizontal',{xtype:'slider',width:450,value:state==='selected'?70:42,minValue:0,maxValue:100}),named('slider.vertical',{xtype:'slider',vertical:true,height:200,width:30,value:state==='selected'?70:42,minValue:0,maxValue:100,margin:'0 0 0 50'})]},host);const h=c.items.first();if(state==='disabled')c.disable();if(state==='focus')h.focus();if(state==='hover'){
                h.thumbs[0].el.dom.dataset.labId='slider.horizontal/thumb';pointer(h,'hover','thumb');
            }
        },
        menu(host,state){
            const c=create('menu.main',{xtype:'menu',floating:false,width:330,items:[named('menu.parent',{text:'Submenu',menu:{items:[named('menu.child',{text:'Submenu action'})]}}),named('menu.checked',{xtype:'menucheckitem',text:'Checked option',checked:state!=='unchecked'}),named('menu.unchecked',{xtype:'menucheckitem',text:'Unchecked option',checked:state==='checked'}),{xtype:'menucheckitem',text:'Radio Alpha',group:'lab-menu-choice',checked:true},'-',named('menu.disabled',{text:'Disabled option',disabled:true}),named('menu.action',{text:'Action'})]},host);if(state==='disabled')c.disable();if(state==='focus')c.items.first().focus();if(state==='open')c.items.first().expandMenu(null,0);
        },
        tool(host,state){
            host.classList.add('lab-tool-grid');tools.forEach(type=>{const cell=document.createElement('div');cell.className='lab-tool-cell';const label=document.createElement('div');label.className='lab-tool-label';label.textContent=type;cell.appendChild(label);host.appendChild(cell);const c=create('tool.'+type,{xtype:'tool',type,disabled:state==='disabled'},cell);if(type==='gear'){if(state==='focus')c.focus();if(['hover','pressed'].includes(state))pointer(c,state);}});
        },
        mask(host,state){const c=create('mask.main',{xtype:'panel',title:'Loading target',width:650,height:240,html:'Fixed content behind load mask.'},host);if(state!=='hidden')c.setLoading('Loading fixed data…');}
    };
    function pointerTarget(el,state,id) {
        el.dataset.labId=id;const action={kind:state,selector:lab.selector(id)};lab.pendingActions.push(action);
        el.addEventListener('mouseenter',()=>{lab.pendingActions=lab.pendingActions.filter(a=>a!==action);lab.whenReady().catch(fail);},{once:true});
    }
    Ext.onReady(async function () {
        try {
            Ext.enableFx=false;Ext.tip.QuickTipManager.init();document.body.classList.add('lab-capture');
            const cs=document.getElementById('lab-case'),ss=document.getElementById('lab-state');
            cs.add(new Option('All components','all'));Object.entries(cases).forEach(([name,c])=>cs.add(new Option(c.title,name)));cs.value=selectedCase;
            if(selectedCase!=='all'&&!cases[selectedCase])throw new Error('Unknown fixture case '+selectedCase);
            const states=selectedCase==='all'?['normal']:cases[selectedCase].states;
            states.forEach(s=>ss.add(new Option(s,s)));ss.value=selectedState;
            if(!states.includes(selectedState))throw new Error('Unsupported state '+selectedCase+'/'+selectedState);
            document.getElementById('lab-theme').value=labBoot.theme;
            cs.addEventListener('change',()=>{ss.replaceChildren();(cs.value==='all'?['normal']:cases[cs.value].states).forEach(s=>ss.add(new Option(s,s)));});
            for(const name of selectedCase==='all'?Object.keys(cases):[selectedCase]){
                const section=document.createElement('section');section.className='lab-section';section.dataset.labCase=name;
                const heading=document.createElement('h2');heading.textContent=cases[name].title+' / '+selectedState;const host=document.createElement('div');host.className='lab-host';host.dataset.labHost=name;section.append(heading,host);document.getElementById('lab-stage').appendChild(section);
                factories[name](host,selectedState);
            }
            tagAll();lab.status=lab.pendingActions.length?'AWAITING_POINTER':'SETTLING';
            // Caller can perform the requested real mouse action before awaiting whenReady().
            lab.readyPromise=lab.pendingActions.length?null:lab.whenReady();
            if(lab.readyPromise)lab.readyPromise.catch(fail);
        } catch(error){fail(error);}
    });
}());

