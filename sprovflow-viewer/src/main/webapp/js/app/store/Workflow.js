Ext.define('CF.store.Workflow', {
  extend: 'Ext.data.ArrayStore',
  model: 'CF.model.Workflow',
  sortOnLoad: true,
  sorters: {
    property: 'date2',
    direction: 'DESC'
  }
});