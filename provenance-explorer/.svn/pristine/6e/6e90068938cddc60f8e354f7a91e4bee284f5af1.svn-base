

 var networks = [
        {"abbr":"G","name":"GEOSCOPE"},
        {"abbr":"AU","name":"Geoscience Australia"},
        {"abbr":"AZ","name":"ANZA Regional Network"},
        {"abbr":"BK","name":"Berkeley Digital Seismograph Network"}
        
    ];

Ext.regModel('NetworkCombo', {
    fields: [
        {type: 'string', name: 'abbr'},
        {type: 'string', name: 'name'}
        
    ]
});

	




// The data store holding the states
var store = Ext.create('Ext.data.Store', {
    model: 'NetworkCombo',
    data: networks
});



// ComboBox with multiple selection enabled
var multiCombo = Ext.create('Ext.form.field.ComboBox', {
    fieldLabel: 'Networks',
    name: 'net',
    displayField: 'abbr',
    allowBlank: false,
    width: 300,
    labelWidth: 130,
    store: store,
    value:"G",
    queryMode: 'local',
    getInnerTpl: function() {
        return '<div data-qtip="{abbr}">{abbr} {name}</div>';
    }
});


Ext.define('CF.view.StationSearch', {
     extend:'Ext.form.Panel',
     alias: 'widget.mypanel',
    
    // configure how to read the XML Data
    
    
     errorReader : {
  			  type : 'xml',
		      model: 'Station'
    
		},
     
    items: [multiCombo
   			 
            ],
     buttons: [{
    	itemId: 'station_but',
        text: 'Search'
       
    },
    {
    	itemId: 'station_cl_but',
        text: 'Clear'
       
    }]
});

    
