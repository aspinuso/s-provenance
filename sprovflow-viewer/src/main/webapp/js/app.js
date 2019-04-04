/**
 * Ext.Loader
 */
 

var sys = arbor.ParticleSystem();
sys.parameters({repulsion:0, stiffness:1000,friction:0.5,graivty:true})

 

Ext.Ajax.disableCaching = true;

Ext.Date.now = function () { return ""; }
 
Ext.Loader.setConfig({
    enabled: true,
    disableCaching: false,
    paths: {
        GeoExt: "../../../sprovflow-viewer/js/src/GeoExt",
        // for dev use
        Ext: "https://cdn.sencha.io/ext-4.1.0-gpl/src"
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
    appFolder: '../../../sprovflow-viewer/js/app',
    controllers: [
         
    ],
    autoCreateViewport: true
});

/**
 * For dev purpose only
 */
var ctrl, map, mapPanel;
