Ext.define('CF.store.WorkflowInput', {
  extend: 'Ext.data.Store',
  requires: ['CF.model.WorkflowInput'],
  model: 'CF.model.WorkflowInput',
  alias: 'store.workflowinput',
  storeId: 'workflowinputStore'
});