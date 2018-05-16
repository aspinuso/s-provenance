Ext.define('CF.model.Workflow', {
  extend: 'Ext.data.Model',

  fields: [{
    name: 'name'
  }, {
    name: 'desc'
  }, {
    name: 'status'
  }, {
    name: 'date',
    type: 'date',
    dateFormat: 'Y-m-d'
  }, {
    name: 'date2'
  }, {
    name: 'workflowId'
  }]
});