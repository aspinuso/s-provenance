Ext.define('CF.model.Activity', {
  extend: 'Ext.data.Model',

  fields: [{
    name: 'ID',
    type: 'string',
    mapping: '_id'
  }, {
    name: 'instanceId',
    type: 'string',
    mapping: 'instanceId'
  }, {
    name: 'parameters',
    type: 'string',
    mapping: 'parameters'
  }, {
    name: 'creationDate',
    type: 'string',
    mapping: 'endTime'
  }, {
    name: 'errors',
    type: 'string',
    mapping: 'errors'
  }, {
    name: 'iterationIndex',
    type: 'string',
    mapping: 'iterationIndex'
  }]
});