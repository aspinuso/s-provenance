 Ext.define('CF.model.ProvWorkflow', {
   extend: 'Ext.data.Model',

   fields: [{
     name: 'runId',
     type: 'string',
     mapping: '_id'
   }, {
     name: 'workflowName',
     type: 'string',
     mapping: 'workflowName'
   }, {
     name: 'description',
     type: 'string',
     mapping: 'description'
   }, {
     name: 'date',
     type: 'string',
     mapping: 'startTime'
   }, {
     name: 'systemId',
     type: 'string',
     mapping: 'system_id'
   }]
 });