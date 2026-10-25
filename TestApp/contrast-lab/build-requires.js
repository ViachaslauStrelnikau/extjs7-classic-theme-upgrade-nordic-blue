// Include this file in the lab build profile's JS inputs in TASK-007 so Cmd retains all fixture CSS.
// It is not loaded by TestApp's production entry point or by the standalone fixture.
Ext.require([
    'Ext.panel.Panel','Ext.window.Window','Ext.button.Button','Ext.button.Split',
    'Ext.toolbar.Toolbar','Ext.toolbar.Paging','Ext.form.Panel',
    'Ext.form.field.Text','Ext.form.field.ComboBox','Ext.form.field.Date',
    'Ext.form.field.Time','Ext.form.field.Number','Ext.form.field.TextArea',
    'Ext.form.field.Checkbox','Ext.form.field.Radio','Ext.form.FieldSet',
    'Ext.form.field.HtmlEditor','Ext.grid.Panel','Ext.grid.column.Check',
    'Ext.layout.container.Border','Ext.tab.Panel','Ext.tree.Panel',
    'Ext.picker.Date','Ext.ProgressBar','Ext.slider.Single','Ext.menu.Menu',
    'Ext.menu.CheckItem','Ext.panel.Tool','Ext.LoadMask'
]);
