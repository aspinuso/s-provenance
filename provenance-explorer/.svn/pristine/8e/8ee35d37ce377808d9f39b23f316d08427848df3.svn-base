/**
 * The GeoExt.panel.Map used in the application.  Useful to define map options
 * and stuff.
 * @extends GeoExt.panel.Map
 */
var layerStore = Ext.create("GeoExt.data.LayerStore");

Ext.define('CF.view.Map', {
    // Ext.panel.Panel-specific options:
    extend: 'GeoExt.panel.Map',
    alias : 'widget.cf_mappanel',
    requires: [
        'Ext.window.MessageBox',
        'GeoExt.Action',
        'GeoExt.LegendImage',
        'GeoExt.slider.LayerOpacity',
        'GeoExt.panel.Legend',
        'CF.view.help.Action'
    ],
    border: 'false',
    layout: 'fit',
    region: 'west',
    width: 600,
    // GeoExt.panel.Map-specific options :
    center: '13.3046875,40.48193359375',
    zoom: 4,
    layers: layerStore,

    initComponent: function() {
        var me = this,
            items = [],
            ctrl;
        
         var layers = [];

        
           var hwms = 
           new OpenLayers.Layer.WMS(
            "Hazard Map WMS (Epher) ",
            "http://gemmsrvr.ethz.ch/cgi-bin/mapserv?MAP=/var/www/mapfile/sharehazard.01.map&",
             {layers: 'hmap469',
             transparent: 'true',
             },{
             isBaseLayer: false
             }
        );
        
        
         var vecwms = 
           new OpenLayers.Layer.WMS(
            "Borders",
            "http://gemmsrvr.ethz.ch/cgi-bin/mapserv?map=/var/www/mapfile/worldvector.map&",
             {layers: 'wv_country_ol',
             transparent: 'true',
             },{
             isBaseLayer: false
             }
        );
        
         var geowms = 
           new OpenLayers.Layer.WMS(
            "Geology (OneGeology) ",
            " http://www.bgr.de/Service/OneGeology/BGR_Geological_Units_IGME5000/",
             {layers: 'EUROPE_BGR_5M_ONSH',
             transparent: 'true',
             },{
             isBaseLayer: false
             }
        );
        
        var faultswms = 
           new OpenLayers.Layer.WMS(
            "Faults (OneGeology)",
            " http://mapdmzrec.brgm.fr/cgi-bin/mapserv?map=/carto/ogg/mapFiles/GISEurope_Bedrock_and_Structural_Geology.map&",
             {layers: 'Europe_GISEurope_1500K_Faults',
             transparent: 'true',
             },{
             isBaseLayer: false
             }
        );
        
       
        
         layers.push(hwms);
         layers.push(vecwms);
         layers.push(geowms);
         layers.push(faultswms);
       
       
        
        OpenLayers.Control.CustomNavToolbar = OpenLayers.Class(OpenLayers.Control.Panel, {
	
				    /**
				     * Constructor: OpenLayers.Control.NavToolbar 
				     * Add our two mousedefaults controls.
				     *
				     * Parameters:
				     * options - {Object} An optional object whose properties will be used
				     *     to extend the control.
				     */
					
					
				    initialize: function(options) {
				        OpenLayers.Control.Panel.prototype.initialize.apply(this, [options]);
				        this.addControls([
				        new OpenLayers.Control.LayerSwitcher({'ascending':false}),
                      
                        new OpenLayers.Control.ZoomBox({alwaysZoom:false})
				        ]);
						// To make the custom navtoolbar use the regular navtoolbar style
						this.displayClass = 'olControlNavToolbar'
				    },
					
					
				
				    /**
				     * Method: draw 
				     * calls the default draw, and then activates mouse defaults.
				     */
				  /*  draw: function() {
				        var div = OpenLayers.Control.Panel.prototype.draw.apply(this, arguments);
                        this.defaultControl = this.controls[0];
				        return div;
				    }*/
				});
				
				
		var panel = new OpenLayers.Control.CustomNavToolbar();
	    
        map = new OpenLayers.Map('map', {
                    
                    numZoomLevels: 10
                    
                });
        map.addControl(panel);    
        map.addLayers(layers)
        hwms.setOpacity(0.5);
        geowms.setOpacity(0.5);
        faultswms.setOpacity(0.3);
       
        layerStore.bind(map)
         

        // ZoomToMaxExtent control, a "button" control
        items.push(Ext.create('Ext.button.Button', Ext.create('GeoExt.Action', {
            control: new OpenLayers.Control.ZoomToMaxExtent(),
            map: map,
            text: "max extent",
            tooltip: "zoom to max extent"
        })));

        
        

        items.push("-");

            items.push("->");

        // Help action
        items.push(
            Ext.create('Ext.button.Button', Ext.create('CF.view.help.Action', {
                windowContentEl: "help"
            }))
        );
        
        
        
        
        items.push(
        {
            xtype: 'splitbutton',
            text: 'Layers info',
            menuAlign: 'tr-br',
            menu: {
                xtype: 'menu',
                plain: true,
                items: [
                {
                    text: 'Hazard'
                },
                    {    
				        xtype: "gx_opacityslider",
				        layer: hwms,
				        aggressive: true,
				        vertical: false,
				        value:50,
				        height: 10,
						x: 10,
     				    y: 20
 			 		  } ,
 			 		 
 			 		  Ext.create('Ext.Button', {
						    text: 'View Legend',
    
   						    handler: function() {
 						       Ext.create('Ext.window.Window', {
  								   title:'Legend',
 								   height: 200,
								   width: 600,
							       layout: 'fit',
						           items:[Ext.create('Ext.panel.Panel', {
   									 bodyPadding: 5,  // Don't want content to crunch against the borders
 									 width: 600,
 									 autoScroll: true,
									 
    								 items: [{
        
 			 			               
 				  			           xtype: "gx_legendimage",
  							           
  							             
  							           url:'http://gemmsrvr.ethz.ch/cgi-bin/mapserv?MAP=/var/www/mapfile/sharehazard.01.map&TRANSPARENT=true&SERVICE=WMS&VERSION=1.1.1&REQUEST=GetLegendGraphic&STYLES=&FORMAT=image%2Fpng&SRS=EPSG%3A4326&VISIBILITY=true&LAYER=hmap469',

  			        				   padding: 5
      			 			     		 }]
      			 			     	 })
      			 			     	]
							}).show();
						    
							}					
						}),
 			 		 
 			 		 
 			 		 
 			 		 
 			 		 
 			 		  {
                    text: 'Borders'
                },
                    {    
				        xtype: "gx_opacityslider",
				        text: 'Boundaries',
   					    layer: vecwms,
				        aggressive: true,
				        vertical: false,
				        height: 10,
				    
						x: 10,
     				    y: 20
 			 		  },
 			 		   { 
                    text: 'Geology - Europe BGR 5M Geological Units - Onshore'
                },
                    {    
				        xtype: "gx_opacityslider",
				        text: 'Geology',
   					    layer: geowms,
				        aggressive: true,
				        vertical: false,
				        
				        height: 10,
				        value:50,
						x: 10,
     				    y: 20
 			 		  },
 			 		  Ext.create('Ext.Button', {
						    text: 'View Legend',
    
   						    handler: function() {
 						       Ext.create('Ext.window.Window', {
  								   title:'Legend',   
 								   height: 200,
								   width: 600,
							       layout: 'fit',
						           items:[Ext.create('Ext.panel.Panel', {
   									 bodyPadding: 5,  // Don't want content to crunch against the borders
 									 width: 600,
 									 autoScroll: true,
									 
    								 items: [{
        
 			 			               
 				  			           xtype: "gx_legendimage",
  							           
  							           
  							            
  							           url:'http://www.bgr.de/Service/OneGeology/BGR_Geological_Units_IGME5000/?version=1.3.0&service=WMS&request=GetLegendGraphic&sld_version=1.1.0&layer=EUROPE_BGR_5M_ONSH&format=image/png&STYLE=default',
  			        				   padding: 5
      			 			     		 }]
      			 			     	 })
      			 			     	]
							}).show();
						    
							}					
						}),
 			 		 
 			 		   {
                    text: 'Faults'
                },
                    {    
				        xtype: "gx_opacityslider",
				        text: 'Faults',
   					    layer: faultswms,
				        aggressive: true,
				        vertical: false,
				        height: 10,
				        value:30,
						x: 10,
     				    y: 20
 			 		  }
 			 		  
                		]
           		 }
      		  }

        );
        
        
                                                                                        
        
        
         
        
        Ext.apply(me, {
            map: map,
            dockedItems: [{
                xtype: 'toolbar',
                dock: 'top',
                items: items,
                style: {
                    border: 0,
                    padding: 0
                }
            }]
        });
                
        me.callParent(arguments);
    }
});
