 Ext.define('CF.model.WorkflowInput', {
   extend: 'Ext.data.Model',

   fields: [{
     name: 'url',
     type: 'string',
     mapping: 'url'
   }, {
     name: 'mimetype',
     type: 'string',
     mapping: 'mime-type'
   }, {
     name: 'name',
     type: 'string',
     mapping: 'name'
   },
   {
     name: 'type',
     type: 'string',
     mapping: 'prov-type'
   },
   {
     name: 'provtype',
     type: 'string',
     mapping: 'prov:type'
   }]
 });