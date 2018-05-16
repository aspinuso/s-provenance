/**
 * Ext.Loader
 */
 

var sys = arbor.ParticleSystem();
sys.parameters({repulsion:-20, stiffness:1000,friction:-1.5})
//{repulsion:-10, stiffness:100, friction:1.0,gravity:true, dt:0.015}

Ext.Ajax.disableCaching = true;

Ext.Date.now = function () { return ""; }
 
Ext.Loader.setConfig({
    enabled: true,
    disableCaching: false,
    paths: {
        GeoExt: "../../../provenance-explorer/js/src/GeoExt",
        // for dev use
        Ext: "http://cdn.sencha.io/ext-4.1.0-gpl/src"
        // for build purpose
        //Ext: "extjs-4.1.0/src"
    }
});

/**
 * CF.app
 * A MVC application demo that uses GeoExt and Ext components to display
 * geospatial data.
 */
Ext.application({
    name: 'CF',
    appFolder: '../../../provenance-explorer/js/app',
    controllers: [
         
    ],
    autoCreateViewport: true
});

/**
 * For dev purpose only
 */
var ctrl, map, mapPanel;
