/**
 * The store used for summits
 */
Ext.define('CF.store.Activity', {
  extend: 'Ext.data.BufferedStore',
  requires: [
    'Ext.grid.*',
    'Ext.data.*',
    'Ext.util.*',
    'Ext.grid.plugin.BufferedRenderer',
    'CF.model.Activity'
  ],

  model: 'CF.model.Activity',
  alias: 'store.activity',
  storeId: 'activityStore',

  leadingBufferZone: 300,
  pageSize: 100
});