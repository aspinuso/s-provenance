Ext.define('CF.model.Artifact', {
  extend: 'Ext.data.Model',

  fields: [{
    name: 'wasGeneratedBy',
    type: 'string',
    mapping: 'wasGeneratedBy'
  }, {
    name: 'runId',
    type: 'string',
    mapping: 'runId'
  }, {
    name: 'ID',
    type: 'string',
    mapping: 'id'
  }, {
    name: 'endTime',
    type: 'string',
    mapping: 'endTime'
  }, {
    name: 'content',
    type: 'string',
    convert: function(val) {
      return JSON.stringify(val)
    }
  }, {
    name: 'errors',
    type: 'string',
    mapping: 'errors'
  }, {
    name: 'annotations',
    type: 'string',
    convert: function(val) {
      return JSON.stringify(val)
    }
  }, {
    name: 'parameters',
    type: 'string',
    convert: function(val) {
      return JSON.stringify(val)
    }
  }, {
    name: 'location',
    type: 'string',
    mapping: 'location'
  }]
});