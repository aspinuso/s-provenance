Ext.define('CF.store.Station', {
  extend: 'GeoExt.data.FeatureStore',
  requires: ['CF.model.Station'],
  model: 'CF.model.Station',
  alias: 'store.station',
  storeId: 'stationStore'
});