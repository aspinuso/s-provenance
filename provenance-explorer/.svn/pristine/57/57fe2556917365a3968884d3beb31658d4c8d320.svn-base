 
 

 
 						
 Ext.define('CF.model.Event', {
    extend: 'Ext.data.Model',
 
  fields : [
  		    {
            name: 'symbolizer',
            convert: function(v, r) {
                return r.raw.layer.styleMap.createSymbolizer(r.raw, 'default');
            	}
        	},
            {name: 'description', type: 'string', mapping:'description'},
            {name: 'date', type: 'string', mapping:'datetime'},
            {name: 'magnitude', type: 'string', mapping:'magnitude'},
            {name: 'latitude', type: 'string' , mapping:'latitude'}, // custom mapping
            {name: 'longitude', type: 'string' , mapping:'longitude'}, // custom mapping
            {name: 'depth', type: 'string' , mapping:'depth'} // custom mapping
            
        	], 
});
 						
  				
 


 

/**
 * The store used for summits
 */
Ext.define('CF.store.EventStore', {extend:'GeoExt.data.FeatureStore',
   						 // requires:['CF.model.Station','CF.model.Network'],
   						  model:   'CF.model.Event',
   						  alias: 'store.eventstore',
   						  storeId: 'eventStore',
   						  
   						  /*,
   						  proxy: new GeoExt.data.ProtocolProxy({
           							 protocol: protocol,
        							})
   						  
   						  
    					  proxy: {	 limitParam: undefined,
      						         startParam: undefined,
   						             paramName: undefined,
  						             pageParam: undefined,
 							         noCache:false,
    							     type: 'ajax',
   								     reader: {
   									          type: 'StationReader'
   									          ,
   									          record:'Station'
   									       //   root: 'FDSNStationXML',
										   //   getAssociatedDataRoot:function(data, associationName) {
 										//			 if(associationName == 'stations')
  										//					  return data;}
 						       }  
 								 }*/
 						 
 						   
 						});


