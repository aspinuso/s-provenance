Ext.define("CF.model.Mesh", {
  extend: "Ext.data.Model",
  fields: [{
    type: 'string',
    name: 'name'
  }, {
    type: 'long',
    name: 'geo_minLat'
  }, {
    type: 'long',
    name: 'geo_maxLat'
  }, {
    type: 'long',
    name: 'geo_minLon'
  }, {
    type: 'long',
    name: 'geo_maxLon'
  }, {
    type: 'string',
    name: 'geo_proj'
  }, {
    type: 'array',
    name: 'velmod'
  }, {
    type: 'array',
    name: 'values'
  }]
});