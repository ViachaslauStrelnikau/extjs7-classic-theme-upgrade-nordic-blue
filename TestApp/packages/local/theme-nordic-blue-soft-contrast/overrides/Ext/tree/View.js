/** Theme-scoped native tree motion for Ext JS Classic 7.7. */
Ext.define('Ext.theme.nordicblue.softcontrast.tree.ViewOverride', {
    override: 'Ext.tree.View',

    expandDuration: 125,
    collapseDuration: 125,

    initComponent: function () {
        this.callParent(arguments);

        if (window.matchMedia &&
            window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            this.animate = false;
        }
    }
});
