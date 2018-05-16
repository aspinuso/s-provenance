 
 

 
 						
 Ext.define('CF.model.Activity', {
    extend: 'Ext.data.Model',
 
  fields : [
  		     
            {name: 'ID', type: 'string', mapping:'_id'},
            {name: 'instanceId', type: 'string', mapping:'instanceId'},
            {name: 'parameters', type: 'string', mapping:'parameters'},
            {name: 'creationDate', type: 'string', mapping:'creationDate'}, // custom mapping
            {name: 'error', type: 'string' , convert: function (val){
            			 				return JSON.stringify(val)
    							}
    					}, // custom mapping
            {name: 'iterationIndex', type: 'string' , mapping:'iterationIndex'} // custom mapping
            
        	], 
});
 						


 

/**
 * The store used for summits
 */
Ext.define('CF.store.ActivityStore', { 
 						  extend:'Ext.data.Store',
   						  requires: [
    							'Ext.grid.*',
							    'Ext.data.*',
							    'Ext.util.*',
							    'Ext.grid.plugin.BufferedRenderer'
   							 		],
   						 
   						  model:   'CF.model.Activity',
   						  alias: 'store.activitystore',
   						  storeId: 'activityStore',
   						   
   						  // allow the grid to interact with the paging scroller by buffering
   					     buffered: true,
   					     leadingBufferZone: 30,
   					     pageSize: 300,
     				     
 					     
				         proxy: {
            // load using script tags for cross domain, if the data in on the same domain as
            // this page, an Ajax proxy would be better
   				         type: 'ajax',
  				          url: '/j2ep-1.0/prov/run/?id=http%3A%2F%2Flocalhost%3A8080%2FDispelGateway%2Fservices%2Fprocess-6bd8e593-0847-443e-a842-e69635c2c2c6',
  				          reader: {
   						             root: 'activities',
  						             totalProperty: 'totalCount'
  						          },
  						  simpleSortMode: true
    
     					   },
        
     				    
     				   
     				 
 						 
 						   
 						});


