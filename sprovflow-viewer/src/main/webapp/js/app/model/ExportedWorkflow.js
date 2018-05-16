Ext.define("CF.model.ExportedWorkflow", {
  extend: "Ext.data.Model",
  fields: [{
    type: 'string',
    name: 'workflowName'
  }, {
    type: 'string',
    name: 'workflowId'
  }, {
    type: 'string',
    name: 'ownerId'
  }]
});