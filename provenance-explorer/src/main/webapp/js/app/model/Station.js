Ext.define('CF.model.Station', {
  extend: 'Ext.data.Model',

  fields: [{
      name: 'symbolizer',
      convert: function(v, r) {
        //alert("selected: "+r.get('station'));
        return r.raw.layer.styleMap.createSymbolizer(r.raw, 'default');
      }
    }, {
      name: 'station',
      type: 'string',
      mapping: 'station'
    }, {
      name: 'network',
      type: 'string',
      mapping: 'network'
    }, {
      name: 'latitude',
      type: 'string',
      mapping: 'latitude'
    }, // custom mapping
    {
      name: 'longitude',
      type: 'string',
      mapping: 'longitude'
    }, // custom mapping
    {
      name: 'elevation',
      type: 'string',
      mapping: 'elevation'
    } // custom mapping
  ]

});