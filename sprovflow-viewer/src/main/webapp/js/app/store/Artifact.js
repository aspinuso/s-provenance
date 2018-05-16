/**
 * The store used for summits
 */
Ext.define('CF.store.Artifact', {
  extend: 'Ext.data.Store',
  requires: [
    'Ext.grid.*',
    'Ext.data.*',
    'Ext.util.*',
    'Ext.grid.plugin.BufferedRenderer',
    'CF.model.Artifact'
  ],

  model: 'CF.model.Artifact',
  alias: 'store.artifact',
  storeId: 'artifactStore',
  /*buffered: true,
    leadingBufferZone: 30,*/
  pageSize: 1000
});