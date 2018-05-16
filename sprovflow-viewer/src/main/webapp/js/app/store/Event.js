Ext.define('CF.store.Event', {
  extend: 'GeoExt.data.FeatureStore',
  requires: ['CF.model.Event'],
  model: 'CF.model.Event',
  alias: 'store.event',
  storeId: 'eventStore'
});