Ext.define('CF.model.Artifact', {
  extend: 'Ext.data.Model',

  fields: [{
    name: 'parameters',
    type: 'string',
    mapping: 'value.parameterMap'
  }, {
    name: 'metadata',
    type: 'string',
    mapping: 'value.contentMap'
  }]
});