 
 

 
 						
 Ext.define('CF.model.Artifact', {
    extend: 'Ext.data.Model',
 
  fields : [
  		    {name: 'wasGeneratedBy', type: 'string', mapping:'wasGeneratedBy'}, 
  		    {name: 'runId', type: 'string', mapping:'runId'}, 
            {name: 'ID', type: 'string', mapping:'id'},
            {name: 'content', type: 'string', convert: function (val){
            			 
    					return JSON.stringify(val)
    					}
    					},
    					
            {name: 'annotations', type: 'string',convert: function (val){
            			 
    					return JSON.stringify(val)
    					
            		}},
            {name: 'parameters', type: 'string',
            		convert: function (val){
            			 
    					return JSON.stringify(val)
    					
            		}},
            {name: 'location', type: 'string', mapping:'location'}, // custom mapping
            
            
        	], 
});
 						


 

/**
 * The store used for summits
 */
Ext.define('CF.store.ArtifactStore', { 
 						  extend:'Ext.data.Store',
   						  requires: [
    							'Ext.grid.*',
							    'Ext.data.*',
							    'Ext.util.*',
							    'Ext.grid.plugin.BufferedRenderer'
   							 		],
   						 
   						  model:   'CF.model.Artifact',
   						  alias: 'store.artifactstore',
   						  storeId: 'artifactStore',
   						  buffered: true,
   					      leadingBufferZone: 30,
   					      pageSize: 300,
   						  
 						   
 						});


