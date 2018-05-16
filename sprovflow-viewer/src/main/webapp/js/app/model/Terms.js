Ext.define('CF.model.Terms', {
  extend: 'Ext.data.Model',

  fields: [
  {
                        name: 'term',
                        mapping:'term'
                      },

  {
                        name: 'use',
                        mapping:'use'
    },
  {
                        name: 'type',
                        convert: function(v, record) {
                             
                            out=""
                            for (k in record.data.valuesByType)
                              out+= k + "|"+record.data.valuesByType[k]["count"]+";</br>"
                            return out
                        }
    }
    ]
  
});