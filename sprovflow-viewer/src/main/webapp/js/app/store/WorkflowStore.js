 
 

 
 						
 Ext.define('CF.model.Worflow', {
    extend: 'Ext.data.Model',
 
  fields : [
  		     
            {name: 'runId', type: 'string', mapping:'_id'},
            {name: 'description', type: 'string', mapping:'description'},
            {name: 'date', type: 'string', mapping:'date'}
            
            
        	], 
});
 						


 

/**
 * The store used for summits
 */
Ext.define('CF.store.WorkflowStore', { 
 						  extend:'Ext.data.Store',
   						  requires: [
    							'Ext.grid.*',
							    'Ext.data.*',
							    'Ext.util.*',
							    'Ext.grid.plugin.BufferedRenderer'
   							 		],
   						 
   						  model:   'CF.model.Worflow',
   						  alias: 'store.workflowstore',
   						  storeId: 'workflowStore',
   						   
   						  // allow the grid to interact with the paging scroller by buffering
   					     buffered: true,
   					     leadingBufferZone: 30,
   					     pageSize: 15,
     				     
 					     
				         proxy: {
            // load using script tags for cross domain, if the data in on the same domain as
            // this page, an Ajax proxy would be better
   				         type: 'ajax',
  				          url: '/j2ep-1.0/prov/workflow/allruns',
  				          reader: {
   						             root: 'runIds',
  						             totalProperty: 'totalCount'
  						          },
  						  simpleSortMode: true
    
     					   },
        
     				    
     				   
     				 
 						 
 						   
 						});


