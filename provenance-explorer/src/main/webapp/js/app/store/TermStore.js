Ext.define('CF.store.TermStore', { 
 						  extend:'Ext.data.Store',
   						  requires: [
    							 
							    'Ext.data.*',
							    'Ext.util.*',
							    
   							 		],
   						 
   						  model:   'CF.model.Terms',
   						  alias: 'store.termstore',
   						  storeId: 'termstore',
                sorters: [{
             property: 'term',
              direction: 'ASC'
               }],
    sortRoot: 'term',
    sortOnLoad: true,
    remoteSort: false,
   						  proxy: {
            type: 'ajax',
            url: PROV_SERVICE_BASEURL + '/terms?usernames='+userSN+'&aggregationLevel=username',
            reader: {
                type: 'json',
                root: 'terms'
            } 
        }
        
     				    
     				   
     				 
 						 
 						   
});


