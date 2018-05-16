 Ext.define('CF.model.Event', {
   extend: 'Ext.data.Model',

   fields: [{
     name: 'symbolizer',
     convert: function(v, r) {
       return r.raw.layer.styleMap.createSymbolizer(r.raw, 'default');
     }
   }, {
     name: 'eventId',
     type: 'string',
     mapping: 'eventId'
   }, {
     name: 'description',
     type: 'string',
     mapping: 'description'
   }, {
     name: 'date',
     type: 'string',
     mapping: 'datetime'
   }, {
     name: 'depth',
     type: 'string',
     mapping: 'depth'
   }, {
     name: 'magnitude',
     type: 'string',
     mapping: 'magnitude'
   }, {
     name: 'latitude',
     type: 'string',
     mapping: 'latitude'
   }, {
     name: 'longitude',
     type: 'string',
     mapping: 'longitude'
   }, {
     name: 'tensor_mrr',
     type: 'string',
     mapping: 'tensor_mrr'
   }, {
     name: 'tensor_mtt',
     type: 'string',
     mapping: 'tensor_mtt'
   }, {
     name: 'tensor_mpp',
     type: 'string',
     mapping: 'tensor_mpp'
   }, {
     name: 'tensor_mrt',
     type: 'string',
     mapping: 'tensor_mrt'
   }, {
     name: 'tensor_mrp',
     type: 'string',
     mapping: 'tensor_mrp'
   }, {
     name: 'tensor_mtp',
     type: 'string',
     mapping: 'tensor_mtp'
   }]
 });