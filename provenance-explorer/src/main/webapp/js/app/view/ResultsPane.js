
delete Ext.tip.Tip.prototype.minWidth;


iDROP='http://iren-web.renci.org/idrop-release/idrop.jnlp'   
RADIAL='d3js.jsp?minidx=0&maxidx=10&level=prospective&groupby=actedOnBehalfOf'	      	                    
PROV_SERVICE_BASEURL="/prov/"
var IRODS_URL = "http://dir-irods.epcc.ed.ac.uk/irodsweb/rodsproxy/"+userSN+".UEDINZone@dir-irods.epcc.ed.ac.uk:1247/UEDINZone"
var IRODS_URL_GSI = "gsiftp://dir-irods.epcc.ed.ac.uk/"
var IRODS_URI=userSN+".UEDINZone@dir-irods.epcc.ed.ac.uk:1247/UEDINZone/home/"+userSN+"/verce/"
var deleteWorkflowDataURL = "/j2ep-1.0/irods/irodsweb/services/delete.php"

var activityStore = Ext.create('CF.store.Activity');

var artifactStore = Ext.create('CF.store.Artifact');

var singleArtifactStore = Ext.create('CF.store.Artifact');

var workflowStore = Ext.create('CF.store.ProvWorkflow');

var workflowInputStore = Ext.create('CF.store.WorkflowInput');

var seismoMetaStore = Ext.create('CF.store.SeismoMeta');

var mimetypesStore = Ext.create('CF.store.Mimetype');

// specifies the userhome of whom we are going to access the data from (for sharing purposes)
owner = userSN
var dn_regex=/file:\/\/?([\w-]|([\da-z\.-]+)\.([a-z\.]{2,6}))+/

// ComboBox with multiple selection enabled
Ext.define('CF.view.metaCombo', {
  extend: 'Ext.form.field.ComboBox',
  alias: 'widget.metacombo',
  fieldLabel: 'Terms',
  name: 'keys',
  displayField: 'term',
  width: 200,
  inputAttrTpl: " data-qtip='Insert here a sequence of Terms divided by commas.<br/> Eg. magnitude,station' ",
  labelWidth: 40,
  labelAlign: 'right',
  margin: '10 10 30 10',
  colspan: 4,
  multiSelect: true,
  store: seismoMetaStore,
  queryMode: 'local',
  getInnerTpl: function() {
    return '<div data-qtip="{term}">{term}</div>';
  },
  initComponent: function() {
    this.callParent();
  },
  onCollapse: function() {
    this.callParent();
    if (this.picker.getSelectionModel().selection == null || this.picker.getSelectionModel().selection.length === 0) {
      this.value = this.getRawValue();
    }
  }
});

// Ext.override(Ext.selection.RowModel, {
//   isRowSelected: function(record, index) {
//     try {
//       return this.isSelected(record);
//     } catch (e) {
//       return false;
//     }
//   }
// });


function openRun(id)
{		if (id) 
		 	this.currentRun=id
        activityStore.setProxy({
          type: 'ajax',
          url: PROV_SERVICE_BASEURL + 'activities/' + encodeURIComponent(currentRun)+'?method=aggregate',
          reader: {
            rootProperty: 'activities',
            totalProperty: 'totalCount'
          },
          simpleSortMode: true

        });
        activityStore.data.clear()
        activityStore.on('load', onStoreLoad, this, {
          single: true
        });
        activityStore.load()
        

}

// ComboBox with single selection enabled
Ext.define('CF.view.mimeCombo', {
  extend: 'Ext.form.field.ComboBox',
  alias: 'widget.mimecombo',
  fieldLabel: 'mime-type',
  name: 'mime-type',
  displayField: 'mime',
  width: 300,
  labelWidth: 130,
  colspan: 4,
  store: mimetypesStore,
  queryMode: 'local',
  getInnerTpl: function() {
    return '<div data-qtip="{mime}">{mime} {desc}</div>';
  },
  initComponent: function() {
    this.callParent();
  }
});

var graphMode = ""

var currentRun

var deriv_run

var level = 1;

var colour = {
  orange: "#EEB211",
  darkblue: "#21526a",
  purple: "#941e5e",
  limegreen: "#c1d72e",
  darkgreen: "#619b45",
  lightblue: "#009fc3",
  pink: "#d11b67",
  red: "#ff0000",
  lightgrey:"#CCCCCC",
  black:"#000000"
}


function getRandomColor() {
    var letters = '0123456789ABCDEF'.split('');
    var color = '#';
    for (var i = 0; i < 6; i++ ) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}



var edgecol= colour.darkblue


var wasDerivedFromDephtree = function(data, graph, parent) {
  var col = colour.darkblue;
  

   
  if (!parent) {
    //col = colour.red

  }
  
  if (data.streams)
  { 
 
   
  if (data.streams[0].port==null && !(data.streams[0].port===undefined))
  {
   edgecol=colour.lightblue
   col = colour.lightgrey
  }
  
  if (!(data.feedbackIteration===undefined) && data.feedbackIteration)
  {
   edgecol=colour.lightblue
   col = colour.red
  }
 
  	if (data.streams[0].port=='_d4p_state')
  	{     //console.log(data.streams[0].port)
  		col = colour.lightblue
  		
 	 }
 	 
 	 
  }
  //var node = graph.addNode(data["id"],{label:data["_id"].substring(0,5),'color':col, 'shape':'dot', 'radius':19,'alpha':1,mass:2})
  //node.runId=data["runId"]
  //_d4p_state
  
 // if (!data.streams.port or data.streams.port=='')
  
  
  var nodea = graph.addNode(data["id"], {
    label: data["_id"].substring(0, 8),
    'color': col,
    'shape': 'dot',
    'radius': 19,
    'alpha': 1,
    'data': {'runId':data.runId},
    mass: 2
  });

  if (parent) {
    
  var edgecolour
    if(nodea.data.data.runId!=parent.data.data.runId)
	{    	 
			deriv_run=nodea.data.data.runId
    		edgecolour=colour.red
    		 
    		
    }
    else
	{     
			deriv_run=nodea.data.data.runId
			edgecolour=colour.darkblue
    		 
    }
    //console.log(parent.data.data.runId)
    graph.addEdge(parent, nodea, {
      length: 0.75,
      directed: true,
      weight: 4,
      color:edgecolour
    });

  }

  if (data["derivationIds"].length > 0 && typeof data["derivationIds"] != "undefined") {
    for (var i = 0; i < data["derivationIds"].length; i++) {
      if (data["derivationIds"][i]["wasDerivedFrom"]) {
        wasDerivedFromDephtree(data["derivationIds"][i]["wasDerivedFrom"], graph, nodea);
      }
    }
  }

};


var derivedDataDephtree = function(data, graph, parent) {
  var col = colour.darkblue;
   
   if (!parent) {
    //col = colour.red

  }
 if (data.streams)
  {
 if (data.streams[0].port==null && !(data.streams[0].port===undefined))
  {
  col = colour.lightgrey
  edgecol=colour.lightblue
  }
  
   if (data.streams[0].port=='_d4p_state')
  {
  col = colour.lightblue
  edgecol=colour.lightblue
  //edgecol=blue
  }
  }
  //var node = graph.addNode(data["id"],{label:data["_id"].substring(0,5),'color':col, 'shape':'dot', 'radius':19,'alpha':1,mass:2})
  //console.log(data['derivedData'])
  var nodea = graph.addNode(data["dataId"], {
    label: data["_id"].substring(0, 8),
    'color': col,
    'shape': 'dot',
    'radius': 19,
    'alpha': 1,
     'data': {'runId':data.runId},
    mass: 2
  });
   

  if (parent) {
   if(nodea.data.data.runId!=parent.data.data.runId)
	{    	 
			deriv_run=nodea.data.data.runId
    		edgecolour=colour.red
    		 
    		
    }
    else
	{     
			deriv_run=nodea.data.data.runId
			edgecolour=colour.purple
    		 
    }
    graph.addEdge(parent, nodea, {
      length: 0.75,
      directed: true,
      weight: 4,
      color:edgecolour
    });
  }

  if (typeof data["derivedData"] != "undefined" && data["derivedData"].length > 0) {
    for (var i = 0; i < data["derivedData"].length; i++) {
      if (data["derivedData"][i]) {
        if (i < 20)
          derivedDataDephtree(data["derivedData"][i], graph, nodea)
        else {
          var nodeb = graph.addNode(data["derivedData"][i], {
            label: "...too many",
            'color': colour.purple,
            'shape': 'dot',
            'radius': 19,
            'alpha': 1,
            mass: 2
          })


          graph.addEdge(nodeb, nodea,{
            length: 0.75,
            directed: true,
            weight: 2
          })
          break
        }
      }
    }
  }
};


var getMetadata = function(data, graph) {
  /*var node = graph.addNode(data["streams"][0]["id"]+"meata",{label:data["streams"][0]["id"] })
graph.addEdge(node.name,data["streams"][0]["id"],{label:"wasDerivedBy"})*/
  if (data["entities"][0]["location"] != "") {
    var loc = data["entities"][0]["location"].replace(/file:\/\/[\w-]+[\w.\/]+[\w\/]+pub/, "/intermediate/")
      //	loc=loc.replace(//,"")

    var params = graph.addNode(data["entities"][0]["id"] + "loc", {
      label: JSON.stringify(data["entities"][0]["location"]),
      'color': colour.darkblue,
      'link': loc
    })

    graph.addEdge( data["entities"][0]["id"],params.name, {
      label: "location",
      "weight": 10
    })
  }
};

var wasDerivedFromAddBranch = function(url) {
  $.getJSON(url, function(data) {
  	//console.log(data)
    wasDerivedFromDephtree(data, sys, null)
  });
}

var derivedDataAddBranch = function(url) {
  graphMode = "DERIVEDDATA"

  $.getJSON(url, function(data) {
    derivedDataDephtree(data, sys, null)
  });
};

var wasDerivedFromNewGraph = function(url) {
  graphMode = "WASDERIVEDFROM"

  sys.prune();
  wasDerivedFromAddBranch(url)
};

var derivedDataNewGraph = function(url) {
  sys.prune();
  derivedDataAddBranch(url)
};

var addMeta = function(url) {
  $.getJSON(url, function(data) {
    getMetadata(data, sys)
  });
};


Ext.define('CF.view.WorkflowOpenByRunID', {
  extend: 'Ext.form.Panel',
  alias: 'widget.workflowopenbyrunid',
  // The fields
  title: 'Open',
  height: 150,
  defaultType: 'textfield',
  layout: {
    align: 'center',
    pack: 'center',
    type: 'vbox'
  },
  items: [{
    xtype: 'fieldset',
    title: 'Here you can open Runs that other users have shared with you!',
    collapsible: false,
    width: '95%',
    margins: '20,10,10,10',
    defaults: {
      labelWidth: 10,
      anchor: '100%',
      layout: {
        type: 'hbox'
      }
    },
    items: [{
      xtype: 'fieldcontainer',

      combineErrors: true,
      msgTarget: 'under',
      items: [{
        xtype: 'textfield',
        fieldLabel: 'Run ID',
        labelAlign: 'right',
        width: 300,
        name: 'runId',
        allowBlank: false,
        inputAttrTpl: " data-qtip='Insert here any Run ID' ",
        anchor: '80%',
        allowBlank: false,
        margin: '10 0 10 0'

      }, {
        xtype: 'textfield',
        fieldLabel: 'Username',
        labelAlign: 'right',
        width: 300,
        name: 'usename',
        allowBlank: false,
        inputAttrTpl: " data-qtip='Insert here the username of who is sharing data with you!' ",
        anchor: '80%',
        allowBlank: false,
        margin: '10 0 10 0'

      }]
    }]
  }],

  buttons: [{
    text: 'Open',
    formBind: true, //only enabled once the form is valid

    handler: function() {
      var form = this.up('form').getForm();

      if (form.isValid()) {
		
        activityStore.setProxy({
          type: 'ajax',
          url: PROV_SERVICE_BASEURL + 'activities/' + encodeURIComponent(form.findField("runId").getValue(false).trim())+'?method=aggregate',
          reader: {
            rootProperty: 'activities',
            totalProperty: 'totalCount'
          },
          simpleSortMode: true
        });

        activityStore.data.clear();
        activityStore.load({
          callback: function() {
            currentRun = form.findField("runId").getValue(false).trim()
            deriv_run= currentRun
            owner = form.findField("usename").getValue(false).trim()
            Ext.getCmp('filtercurrent').enable();
            Ext.getCmp('searchartifacts').enable();
            Ext.getCmp('downloadscript').enable();
          }
        });

        activityStore.on('load', onStoreLoad, this, {
          single: true
        });

        currentRun = form.findField("runId").getValue(false).trim();
        deriv_run= currentRun
      };

      activityStore.load();
    }
  }]
});

Ext.define('CF.view.WorkflowValuesRangeSearch', {
  extend: 'Ext.form.Panel',
  alias: 'widget.workflowvaluesrangesearch',
  // The fields
  title: 'Search',
  height: 150,

  defaultType: 'textfield',
  layout: {
    align: 'center',
    pack: 'center',
    type: 'hbox'
  },
  items: [{
    xtype: 'fieldset',
    title: 'Search for runs across products metadata, data formats and parameters',
    collapsible: false,
    width: '95%',
    margins: '20,10,10,10',
    defaults: {
      labelWidth: 10,
      anchor: '100%',
      layout: {
        type: 'hbox'
      }
    },
    items: [{
      xtype: 'fieldcontainer',

      combineErrors: true,
      msgTarget: 'under',

      items: [{
          xtype: 'metacombo'
        }, {
          xtype: 'textfield',
          fieldLabel: 'Min values',
          name: 'minvalues',
          anchor: '80%',
          allowBlank: false,
          labelAlign: 'right',
          inputAttrTpl: " data-qtip='Insert here a sequence of min values related to the indicated Terms, divided by commas.<br/> Eg. 3.5,AQU' ",
          margin: '10 0 10 0'
        }, {
          xtype: 'textfield',
          fieldLabel: 'Max values',
          labelAlign: 'right',
          name: 'maxvalues',
          inputAttrTpl: " data-qtip='Insert here a sequence of max values related to the indicated Terms, divided by commas.<br/> Eg. 5,AQU' ",
          anchor: '80%',
          allowBlank: false,
          margin: '10 0 10 0'
        }

      ]
    }]
  }],

  buttons: [{
    text: 'Refresh',
    handler: function() {
      this.up('form').getForm().reset();
      workflowStore.getProxy().api.read = PROV_SERVICE_BASEURL + 'workflow/user/' + userSN;
      workflowStore.load();
    }
  }, {
    text: 'Search',
    formBind: true, //only enabled once the form is valid

    handler: function() {
      var form = this.up('form').getForm();
      var keys = form.findField("keys").getValue(false).trim();
      var minvalues = encodeURIComponent(form.findField("minvalues").getValue(false).trim());
      var maxvalues = encodeURIComponent(form.findField("maxvalues").getValue(false).trim());
      owner = userSN;

      if (form.isValid()) {
        workflowStore.getProxy().api.read = PROV_SERVICE_BASEURL + 'workflow/user/' + userSN + '?keys=' + keys + "&maxvalues=" + maxvalues + "&minvalues=" + minvalues;
      };

      //BUG: with a single load the grid doesn't synchronise when scrolled to the bottom
      workflowStore.load();
      workflowStore.load();
      //workflowStore.sync()
    }
  }]
});


Ext.define('CF.view.WorkFlowSelectionWindow', {
  extend: 'Ext.window.Window',
  alias: 'widget.workflowselectionwindow',
  requires: ['CF.view.WorkflowSelection'],
  title: 'Workflows Runs',
  height: 530,
  width: 850,
  closeAction: 'hide',
  layout: {
    type: 'vbox',
    align: 'stretch',
    pack: 'start'
  },
  items: [{
    xtype: 'tabpanel',
    border: 'false',
    layout: 'border',

    defaults: {
      split: true
    },

    items: [{
      xtype: 'workflowvaluesrangesearch'
    }, {
      xtype: 'workflowopenbyrunid'
    }]
  }, {
    xtype: 'workflowselection'
  }]

});

var onStoreLoad = function(store) {
  Ext.getCmp('viewworkflowinput').enable()
  Ext.getCmp('exportrun').enable();;
  Ext.getCmp("activitymonitor").setTitle(userSN+' - Run activity monitor - ' + currentRun)
}

var renderActivityID = function(value, p, record) {
if (record.data.streams)
   for (i=0;i<=record.data.streams.length;i++)
   {
   		
	if(record.data.streams[i]['con:immediateAccess'] && record.data.streams[i]['con:immediateAccess']!="")
	   	return Ext.String.format(
    		"<strong><i>{0}</i></strong>",
    		record.data.ID
  	   	);
  	if(record.data.streams[i].location && record.data.streams[i].location!='')
    	return Ext.String.format(
    		"<i>{0}</i>",
    		record.data.ID
  	   	);
  	return Ext.String.format(
    	"{0}",
    	record.data.ID
  	   );
  	
  	}
else  	
  	return Ext.String.format(
    	"{0}",
    	record.data.ID
  	   );
}
  	

Ext.define('CF.view.ActivityMonitor', {
  title: 'Run Activity monitor',
  width: '30%',
  region: 'west',
  extend: 'Ext.grid.Panel',
  alias: 'widget.activitymonitor',
  id: 'activitymonitor',
  requires: [
    'CF.store.Activity',
    'Ext.grid.plugin.BufferedRenderer'
  ],

  store: activityStore,
  trackOver: true,
  autoScroll: true,
  collapsible: true,

  dockedItems: {
    itemId: 'toolbar',
    xtype: 'toolbar',
    items: [{
      tooltip: 'Open Run',
      text: 'Open Run',

      handler: function(url) {
        if (this.workflowselectionwindow == null) {
          this.workflowselectionwindow = Ext.create('CF.view.WorkFlowSelectionWindow');
        }

        this.workflowselectionwindow.show();

        if (!workflowStore.isLoaded()) {
          workflowStore.getProxy().api.read = PROV_SERVICE_BASEURL + 'workflow/user/' + userSN;

          workflowStore.load();
        }
      }
    }, {
      tooltip: 'Refresh View',
      text: 'Refresh View',


      handler: openRun
    }, {
      tooltip: 'View Run Inputs',
      text: 'View Inputs',
      id: 'viewworkflowinput',
      disabled: 'true',

      handler: function() {
        workflowInputStore.setProxy({
          type: 'ajax',
          url: PROV_SERVICE_BASEURL + 'workflow/' + encodeURIComponent(currentRun),
          reader: {
            rootProperty: 'input',
            totalProperty: 'totalCount'
          },

          failure: function() {

            Ext.Msg.alert("Error", "Error loading Workflow Inputs");

          },
          simpleSortMode: true

        });

        if (typeof workflowIn != "undefined") {
          workflowIn.close();
        }

        workflowIn = Ext.create('Ext.window.Window', {
          title: 'Workflow input - ' + currentRun,
          height: 300,
          width: 500,
          layout: 'fit',
          items: [Ext.create('CF.view.WorkflowInputView')]

        }).show();
        workflowInputStore.data.clear()
        workflowInputStore.load()

      }
    },
    {
        tooltip: "Export the trace in a W3C-PROV JSON file",
        text: 'Get W3C-PROV',
        disabled: 'true',
  	    id: 'exportrun',

        handler: function() {
         window.open(PROV_SERVICE_BASEURL + 'workflow/export/' + encodeURIComponent(currentRun)+'?'+'all=True', 'Download')
          
     	}
    },
    {
        tooltip: "Manage Files and Permissions with iDROP",
        text: 'iDrop',
  	    id: 'idrop',
        handler: function() {
         window.open(iDROP, 'Download')
          
        }
      },
      {
        tooltip: "Radial Provenance Analysis",
        text: 'Radial',
  	    id: 'Radial',
        handler: function() {
         window.open(RADIAL+'&runId='+currentRun,'_blank')
          
        }
      }
    
    ]
  },

  plugins: [{
    ptype: 'bufferedrenderer'
  }],


  selModel: {
    pruneRemoved: false
  },

  border: false,

  loadMask: true,

  columns: [

    {
      xtype: 'rownumberer',
      width: 35,

      sortable: false
    },

    {
      header: 'ID',
      dataIndex: 'ID',
      flex: 3,
      sortable: true,
      renderer: renderActivityID
    },

    {
      header: 'Date',
      dataIndex: 'creationDate',
      flex: 3,
      sortable: true,
      groupable: false
    }, // custom mapping
    {
      header: 'Messages',
      dataIndex: 'errors',
      flex: 3,
      sortable: false
    }
  ],
  flex: 1,

  viewConfig: {
    listeners: {
      itemdblclick: function(dataview, record, item, index, e) {
        artifactStore.setProxy({
          type: 'ajax',
          url: PROV_SERVICE_BASEURL + 'entities/generatedby?iterationId=' + record.get("ID"),

          reader: {
            rootProperty: 'entities',
            totalProperty: 'totalCount'
          }
        });

        artifactStore.data.clear()
        artifactStore.load()
      }
    }
  },
});

var is_image = function(url, callback, errorcallback) {
  var img = new Image();
  if (typeof(errorcallback) === "function") {
    img.onerror = function() {
      errorcallback(url);
    }
  } else {
    img.onerror = function() {
      return false;
    }
  }
  if (typeof(callback) === "function") {
    img.onload = function() {
      callback(url);
    }
  } else {
    img.onload = function() {
      return true;
    }
  }
  img.src = url;
  
};


var viewData = function(url, open) { //var loc=url.replace = function(/file:\/\/[\w-]+/,"/intermediate-nas/")
  htmlcontent = "<br/><center><strong>Link to data files or data images preview....</strong></center><br/>"
  for (var i = 0; i < url.length; i++) {
    url[i] = url[i].replace(dn_regex, IRODS_URL + "/home/" + owner + "/verce/")


    htmlcontent = htmlcontent + "<center><div id='" + url[i] + "'><img   src='" + localResourcesPath + "/img/loading.gif'/></div></center><br/>"
    var id = url[i];
    var im = new Object()
    im.func = is_image
    im.func(id, function(val) {
      document.getElementById(val).innerHTML = "<img  width='80%' height='70%' src='" + val + "'/>"
    }, function(val) {
      document.getElementById(val).innerHTML = "<center><strong><a target='_blank'  href='" + val + "'>" + val.substring(val.lastIndexOf('/') + 1) + "</a></strong></center>"
    })

  }

  if (open) {
    Ext.create('Ext.window.Window', {
      title: 'Data File',
      height: 300,
      width: 500,
      layout: 'fit',
      items: [{
        overflowY: 'auto',
        overflowX: 'auto',

        xtype: 'panel',
        html: htmlcontent
      }]

    }).show();
  }
};

Ext.define('CF.view.StreamValuesRangeSearch', {
  extend: 'Ext.form.Panel',
  alias: 'streamvaluesrangesearch',
  // The fields
  title: 'Values\' Range',
  defaultType: 'textfield',
  layout: {
    align: 'center',
    pack: 'center',
    type: 'vbox'
  },

  items: [{
    xtype: 'metacombo'
  }, {
    fieldLabel: 'Min values (csv)',
    name: 'minvalues',
    inputAttrTpl: " data-qtip='Insert here a sequence of min values related to the indicated Terms, divided by commas.<br/> Eg. 3.5,AQU' ",

    allowBlank: true
  }, {
    fieldLabel: 'Max values (csv)',
    name: 'maxvalues',
    inputAttrTpl: " data-qtip='Insert here a sequence of max values related to the indicated Terms, divided by commas.<br/> Eg. 5,AQU' ",

    allowBlank: true
  }, {
    xtype: 'mimecombo'
  }],

  buttons: [{
    text: 'Search',
    formBind: true, //only enabled once the form is valid

    handler: function() {
      var form = this.up('form').getForm();
      var keys = this.up('form').getForm().findField("keys").getValue(false);
      var minvalues = encodeURIComponent(this.up('form').getForm().findField("minvalues").getValue(false));
      var maxvalues = encodeURIComponent(this.up('form').getForm().findField("maxvalues").getValue(false));
      var mimetype = this.up('form').getForm().findField("mime-type").getValue(false);
      if (keys == null) keys = "";
      if (form.isValid()) {
        artifactStore.setProxy({
          type: 'ajax',
          url: PROV_SERVICE_BASEURL + 'entities/values-range?runId=' + currentRun + "&keys=" + keys + "&maxvalues=" + maxvalues + "&minvalues=" + minvalues + "&mime-type=" + mimetype,

          reader: {
            rootProperty: 'entities',
            totalProperty: 'totalCount'
          },

          failure: function(response) {
            Ext.Msg.alert("Error", "Search Request Failed");
          }
        });
        artifactStore.data.clear();
        artifactStore.load();
      }
    }
  }]
});

Ext.define('FilterAjax', {
  extend: 'Ext.data.Connection',
  singleton: true,
  constructor: function(config) {
    this.callParent([config]);
    this.on("beforerequest", function() {
      Ext.getCmp("ArtifactView").el.mask("Loading", "x-mask-loading");

    });
    this.on("requestcomplete", function() {
      Ext.getCmp("ArtifactView").el.unmask();
    });
  }
});

Ext.define('CF.view.FilterOnAncestor', {
  extend: 'Ext.form.Panel',
  alias: 'filteronancestor',
  // The fields
  title: 'Ancestor Attributes\' Match',
  defaultType: 'textfield',
  layout: {
    align: 'center',
    pack: 'center',
    type: 'vbox'
  },


  items: [Ext.create('CF.view.metaCombo', {}), {
    fieldLabel: 'Attribute values (csv)',
    name: 'values',
    allowBlank: false
  }],

  buttons: [{
    text: 'Filter',
    formBind: true, //only enabled once the form is valid

    handler: function() {

      dataids = ""
      if (artifactStore.getAt(0).data.ID)
        dataids = artifactStore.getAt(0).data.ID

      for (var i = 1; i < artifactStore.getCount(); i++) {

        dataids += ',' + artifactStore.getAt(i).data.ID;
      }



      var form = this.up('form').getForm();
      var keys = form.findField("keys").getValue(false).trim()
      var minvalues = encodeURIComponent(form.findField("minvalues").getValue(false).trim())
      var maxvalues = encodeURIComponent(form.findField("maxvalues").getValue(false).trim())

      if (form.isValid()) {
        FilterAjax.request({

          method: 'POST',
          url: PROV_SERVICE_BASEURL + 'entities/filterOnAncestorsMeta',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          },
          success: function(response) {
            filtered = Ext.decode(response.responseText)
            artifactStore.clearFilter(true);
            if (filtered.length == 0)
              artifactStore.removeAll()
            else {
              artifactStore.filterBy(function(record, id) {
                if (Ext.Array.indexOf(filtered, record.data.ID) == -1) {
                  return false;
                }
                return true;
              }, this);

            }
          }

          ,
          failure: function(response) {

            Ext.Msg.alert("Error", "Filter Request Failed")


          },
          params: {
            ids: dataids,
            keys: keys,
            values: form.findField("values").getValue().trim()

          }
        });

      }
    }
  }]
});

Ext.define('CF.view.FilterOnAncestorValuesRange', {
  extend: 'Ext.form.Panel',
  alias: 'filteronancestorvaluesrange',
  // The fields
  title: 'Ancestors Values\' Range',
  defaultType: 'textfield',
  layout: {
    align: 'center',
    pack: 'center',
    type: 'vbox'
  },
  items: [Ext.create('CF.view.metaCombo', {}), {
    fieldLabel: 'Min values (csv)',
    name: 'minvalues',
    inputAttrTpl: " data-qtip='Insert here a sequence of min values related to the indicated Terms, divided by commas.<br/> Eg. 3.5,AQU' ",

    allowBlank: false
  }, {
    fieldLabel: 'Max values (csv)',
    name: 'maxvalues',
    inputAttrTpl: " data-qtip='Insert here a sequence of max values related to the indicated Terms, divided by commas.<br/> Eg. 5,AQU' ",

    allowBlank: false
  }],

  buttons: [{
    text: 'Filter',
    formBind: true, //only enabled once the form is valid

    handler: function() {
      dataids = ""
      if (artifactStore.getAt(0).data.ID) {
        dataids = artifactStore.getAt(0).data.ID
      }

      for (var i = 1; i < artifactStore.getCount(); i++) {
        dataids += ',' + artifactStore.getAt(i).data.ID;
      }

      var form = this.up('form').getForm();
      if (form.isValid()) {
        FilterAjax.request({
          method: 'POST',
          url: PROV_SERVICE_BASEURL + 'entities/filterOnAncestorsValuesRange',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          },
          success: function(response) {
            filtered = Ext.decode(response.responseText)
            artifactStore.clearFilter(true);
            if (filtered.length == 0)
              artifactStore.removeAll()
            else {
              artifactStore.filterBy(function(record, id) {
                if (Ext.Array.indexOf(filtered, record.data.ID) == -1) {
                  return false;
                }
                return true;
              }, this);

            }
          },
          failure: function(response) {
            Ext.Msg.alert("Error", "Filter Request Failed")
          },
          params: {
            ids: dataids,
            keys: form.findField("keys").getValue().trim(),
            minvalues: form.findField("minvalues").getValue().trim(),
            maxvalues: form.findField("maxvalues").getValue().trim()
          }
        });
      }
    }
  }]
});


Ext.define('CF.view.FilterOnMeta', {
  extend: 'Ext.form.Panel',
  alias: 'filteronmeta',
  // The fields
  title: 'Attributes Match',
  defaultType: 'textfield',
  layout: {
    align: 'center',
    pack: 'center',
    type: 'vbox'
  },

  items: [Ext.create('CF.view.metaCombo', {}), {
    fieldLabel: 'Attribute values (csv)',
    name: 'values',
    allowBlank: false
  }],

  buttons: [{
    text: 'Filter',
    formBind: true, //only enabled once the form is valid

    handler: function() {
      dataids = ""
      if (artifactStore.getAt(0).data.ID) {
        dataids = artifactStore.getAt(0).data.ID
      }

      for (var i = 1; i < artifactStore.getCount(); i++) {
        dataids += ',' + artifactStore.getAt(i).data.ID;
      }

      var form = this.up('form').getForm();
      if (form.isValid()) {
        FilterAjax.request({

          method: 'POST',
          url: PROV_SERVICE_BASEURL + 'entities/filterOnMeta',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          },
          success: function(response) {
            filtered = Ext.decode(response.responseText)
            artifactStore.clearFilter(true);
            if (filtered.length == 0)
              artifactStore.removeAll()
            else {
              artifactStore.filterBy(function(record, id) {
                if (Ext.Array.indexOf(filtered, record.data.ID) == -1) {
                  return false;
                }
                return true;
              }, this);
            }
          },
          failure: function(response) {
            Ext.Msg.alert("Error", "Filter Request Failed")
          },
          params: {
            ids: dataids,
            keys: form.findField("keys").getValue(false).trim(),
            values: form.findField("values").getValue().trim()
          }
        });
      }
    }
  }]
});

Ext.define('CF.view.AnnotationSearch', {
  extend: 'Ext.form.Panel',
  alias: 'annotationsearch',
  // The fields
  title: 'Annotations',
  defaultType: 'textfield',
  layout: {
    align: 'center',
    pack: 'center',
    type: 'vbox'
  },
  items: [{
    fieldLabel: 'Annotation keys (csv)',
    name: 'keys',
    allowBlank: false,
    margins: '0 0 0 0'
  }, {
    fieldLabel: 'Annotation values (csv)',
    name: 'values',
    allowBlank: false,
    margins: '0 0 0 0'
  }],

  buttons: [{
    text: 'Search',
    formBind: true, //only enabled once the form is valid

    handler: function() {
      var form = this.up('form').getForm();
      if (form.isValid()) {
        artifactStore.setProxy({
          type: 'ajax',
          url: PROV_SERVICE_BASEURL + 'entities/annotations?' + form.getValues(true),

          reader: {
            rootProperty: 'entities',
            totalProperty: 'totalCount'
          }
        });
        artifactStore.data.clear()
        artifactStore.load()
      }
    }
  }]
});

var searchartifactspane = Ext.create('Ext.window.Window', {
  title: 'Search Data',
  height: 230,
  width: 500,
  layout: 'fit',
  closeAction: 'hide',
  items: [{
    xtype: 'tabpanel',
    items: [
      Ext.create('CF.view.StreamValuesRangeSearch'),
      Ext.create('CF.view.AnnotationSearch')
    ]
  }]
});


var insertusername = Ext.create('Ext.window.Window', {
  title: 'Search Data',
  height: 230,
  width: 500,
  layout: 'fit',
  closeAction: 'hide',
  items: [{
    xtype: 'tabpanel',
    items: [
      Ext.create('CF.view.StreamValuesRangeSearch'),
      Ext.create('CF.view.AnnotationSearch')
    ]
  }]
});

var filterOnAncestorspane = Ext.create('Ext.window.Window', {
  title: 'Filter Current View',
  height: 230,
  width: 500,
  layout: 'fit',
  closeAction: 'hide',
  items: [{
    xtype: 'tabpanel',
    items: [
      Ext.create('CF.view.FilterOnMeta'),
      Ext.create('CF.view.FilterOnAncestorValuesRange')
    ]
  }]
});



var renderStream = function(value, p, record) {
  var location = "</br>"
  var contenthtm = ""
  var prov='<a href=\"'+PROV_SERVICE_BASEURL + 'workflow/export/data/'+record.data.ID+'?all=true\" target=\"_blank">Download Provenance</a><br/>'

  if (record.data.location != "") {
    location = '<a href="javascript:viewData(\'' + record.data.location + '\'.split(\',\'),true)">Open</a><br/>'
  }

  contentvis = JSON.parse(record.data.content)

  for (var key in contentvis) {
    if (typeof contentvis[key] == "object") {
      for (var key2 in contentvis[key])
        contenthtm += "<strong>" + key2 + ":</strong> " + contentvis[key][key2] + "<br/><br/>"
    } else {
      contenthtm = "<strong> Output Content: </strong>" + contentvis + "<br/><br/>"
    }
  }

  return Ext.String.format(
    '<div class="search-item" style="border:2px solid; box-shadow: 10px 10px 5px #888888;"><br/>' +
    '<strong>Data ID: {0} </strong> <br/> <br/></strong><hr/>' +
    '<strong>Lineage:</strong><br/><br/>' +
    '<strong><a href="javascript:wasDerivedFromNewGraph(\'' + PROV_SERVICE_BASEURL + 'wasDerivedFrom/{0}?level=' + level + '\')">Trace Backwards</a><br/><br/></strong>' +
    '<strong><a href="javascript:derivedDataNewGraph(\'' + PROV_SERVICE_BASEURL + 'derivedData/{0}?level=' + level + '\')">Trace Forward</a><br/><br/></strong>' +
    '<strong>{10}</strong><br/><hr/><br/>' +
    '<strong>Generated By :</strong> {1} <br/> <br/>' +
    '<strong>Run Id :</strong> {6} <br/> <br/>' +
    '<strong>Start Time Iteration :</strong>{11}<br/> <br/>' +
    '<strong>Production Time :</strong>{7}<br/> <br/>' +
    '<strong>output-port :</strong>{9}<br/> <br/>' +
    '<strong>Output Files :</strong> {4} <br/>' +
    '<strong>Output Metadata:</strong><br/><div style="font-size:15;padding: 10px; resize:both; overflow:auto; height:150px; background-color:#6495ed; color:white; border:2px solid; box-shadow: 10px 10px 5px #888888; width :700px;"> {5} </p></div><br/><br/>' +
    '<strong>Parameters :</strong>{2}<br/> <br/>' +
    '<strong>Annotations :</strong>{3}<br/> <br/>' +
    '<strong>Errors:</strong><div style="font-size:15;padding: 10px; resize:both; overflow:auto; height:150px;background-color:#6495ed; color:white; border:2px solid; box-shadow: 10px 10px 5px #888888; width :700px;"> {8}</div><br/><br/>' +
    '</div>',
    record.data.ID,
    record.data.wasGeneratedBy,
    record.data.parameters,
    record.data.annotations,
    location,
    contenthtm,
    record.data.runId,
    record.data.endTime,
    record.data.errors,
  	record.data.port,
  	prov,
  	record.data.startTime
  );
};

var renderStreamSingle = function(value, p, record) {
  var location = '</br>'
   
  if (record.data.location != "")
    location = '<a href="javascript:viewData(\'' + record.data.location + '\'.split(\',\'),true)">Open</a><br/>'

  return Ext.String.format(
    '<div class="search-item" style="border:2px solid; box-shadow: 10px 10px 5px #888888;"><br/>' +
    '<strong>Data ID: {0} </strong> <br/> <br/></strong><hr/>' +
    '<strong>Lineage:</strong><br/><br/>' +
    '<strong><a href="javascript:wasDerivedFromNewGraph(\'' + PROV_SERVICE_BASEURL + 'wasDerivedFrom/{0}?level=' + level + '\')">Trace Backwards</a><br/><br/></strong>' +
    '<strong><a href="javascript:derivedDataNewGraph(\'' + PROV_SERVICE_BASEURL + 'derivedData/{0}?level=' + level + '\')">Trace Forward</a><br/><br/><hr/></strong>' +
    '<strong>Generated By :</strong> {1} <br/> <br/>' +
    '<strong>Run Id :</strong> {6} <br/> <br/>' +
    '<strong>Start Time Iteration :</strong>{10}<br/> <br/>' +
    '<strong>Production Time :</strong>{7}<br/> <br/>' +
    '<strong>output-port :</strong>{9}<br/> <br/>' +
    '<strong>Output Files :</strong> {4} <br/>' +
    '<strong>Output Metadata:</strong><div style="font-size:15;padding: 10px; resize:both; overflow:auto; height:150px; background-color:#6495ed; color:white; border:2px solid; box-shadow: 10px 10px 5px #888888; width :700px;"> {5}</div><br/><br/>' +
    '<strong>Parameters :</strong>{2}<br/> <br/>' +
    '<strong>Annotations :</strong>{3}<br/> <br/>' +
    '<strong>Errors:</strong><div style="font-size:15;padding: 10px; resize:both; overflow:auto; height:150px; background-color:#6495ed; color:white; border:2px solid; box-shadow: 10px 10px 5px #888888; width :700px;"> {8}</div><br/><br/>' +
    '</div>',
    record.data.ID,
    record.data.wasGeneratedBy,
    record.data.parameters,
    record.data.annotations,
    location,
    record.data.content.substring(0, 1000) + "...",
    record.data.runId,
    record.data.endTime,
    record.data.errors,
    record.data.port,
    record.data.startTime
    
  );
};

var renderWorkflowInput = function(value, p, record) {
 
 if (record.data.provtype=='wfrun' || record.data.type=='wfrun')
 {  
 	 wfid=record.data.url.substr(record.data.url.lastIndexOf('/') + 1)
 	 if (wfid.indexOf('?')!=-1)
	 	 wfid=wfid.substr(0,wfid.indexOf('?'))
 	 
    
	  return Ext.String.format(
    '<br/><strong>Workflow: </strong>{0} - <a href="javascript:openRun(\'{3}\')">{3}</a><br/><br/>' +
    '<strong><a href="{1}" target="_blank">Get W3C-PROV Document</a><br/><br/>' +
    '<strong><a href="javascript: openRun(\'{4}\')">Refresh Current</a><br/>',
    record.data.name,
    record.data.url,
    record.data.mimetype,
    wfid,
    currentRun
  );
  }
else

  return Ext.String.format(
    '<br/><strong>File: </strong>{0} <br/> <br/>' +
    '<strong>url: <a href="{1}" target="_blank">Open</a><br/>' +
    '<strong>mime-type: </strong>{2}<br/> ',
    record.data.name,
    record.data.url,
    record.data.mimetype
  );
};




Ext.define('CF.view.SingleArtifactView', {
  extend: 'Ext.grid.Panel',
  region: 'south',
  width: '100%',
  height: 300,
  store: singleArtifactStore,
  disableSelection: true,
  hideHeaders: true,
  split: true,
  trackOver: true,
  autoScroll: true,

  // TODO replace, unsupported as of ExtJS 5
  // verticalScroller: {
  //   xtype: 'paginggridscroller'
  // },

  viewConfig: {
    enableTextSelection: true
  },

  columns: [{
    dataIndex: 'ID',
    field: 'ID',
    flex: 3,
    renderer: renderStream
  }]
});

Ext.define('CF.view.WorkflowInputView', {
  extend: 'Ext.grid.Panel',

  width: '100%',
  height: 400,

  store: workflowInputStore,
  disableSelection: true,
  hideHeaders: true,

  viewConfig: {
    enableTextSelection: true
  },

  columns: [{
    dataIndex: 'ID',
    field: 'ID',
    flex: 3,
    renderer: renderWorkflowInput
  }]
});

Ext.define('CF.view.ArtifactView', {
  id: 'ArtifactView',
  extend: 'Ext.grid.Panel',
  alias: 'widget.artifactview',
  requires: [
    'CF.store.Artifact',
    'Ext.grid.plugin.BufferedRenderer'
  ],
  region: 'south',
  width: '65%',
  height: 300,
  store: artifactStore,
  disableSelection: true,
  hideHeaders: true,
  split: true,
  collapsible: true,
  title: 'Data products',
  trackOver: true,
  autoScroll: true,
  collapsible: true,
  // TODO replace, unsupported as of ExtJS 5
  // verticalScroller: {
  //   xtype: 'paginggridscroller'
  // },
  viewConfig: {
    enableTextSelection: true
  },
  plugins: [{
    ptype: 'bufferedrenderer'

  }],

  columns: [{
    dataIndex: 'ID',
    field: 'ID',
    flex: 3,
    renderer: renderStream
  }],

  dockedItems: {
    itemId: 'toolbar',
    xtype: 'toolbar',
    items: [{
      text: 'Search',
      id: 'searchartifacts',
      iconCls: 'icon-add',
      disabled: 'true',
      handler: function() {
        searchartifactspane.show();
      }
    }, {
      text: 'Filter Current',
      id: 'filtercurrent',
      iconCls: 'icon-add',
      disabled: 'true',
      handler: function() {
        filterOnAncestorspane.show();
      }
    }, {
      tooltip: 'Download',
      text: 'Produce Download Script',
      id: 'downloadscript',
      disabled: 'true',
    
      handler: function(url) {
      
        var htmlcontent = "";

        artifactStore.each(function(record, id) {
          var location = record.get("location");

          if (location.indexOf(",") != -1) {
            var locations = location.split(",");

            for (var i = 0; i < locations.length; i++) {
              htmlcontent += "globus-url-copy -cred $X509_USER_PROXY " + locations[i].replace(dn_regex, IRODS_URL_GSI + "~/verce/"+currentRun+"/") + " ./ <br/>";
            }
          } else {
            htmlcontent += "globus-url-copy -cred $X509_USER_PROXY " + location.replace(dn_regex, IRODS_URL_GSI + "~/verce/"+currentRun+"/") + " ./ <br/>";
          }
        });
		
        if (this.window == null) {
        	
          this.window = Ext.create('Ext.window.Window', {
            title: 'Download Script',
            height: 360,
            width: 800,
            
            listeners:{
            	scope:this,
       		 	close:function(){
            	this.window = null
              	  
               	 
            	}
        	},
            layout: {
              type: 'vbox',
              align: 'stretch',
              pack: 'start'
            },
            items: [{
              overflowY: 'auto',
              overflowX: 'auto',
              height: 330,
              width: 800,
              xtype: 'panel',
              html: htmlcontent
            }]
          });
        }

        this.window.show();
      }
    }]
  }
});

Ext.define('CF.view.provenanceGraphsViewer', {
  extend: 'Ext.panel.Panel',
  alias: 'widget.provenancegraphsviewer',

  // configure how to read the XML Data
  region: 'center',
  title: 'Data Dependency Graph',
  split: true,
  collapsible: true,
  require: ['Ext.layout.container.Fit',
    'Ext.toolbar.Paging',
    'Ext.ux.form.SearchField',
    'Ext.ux.DataTip'
  ],
  height: 800,
  autoScroll: true,

  layout: 'fit',

  items: [{
    overflowY: 'auto',
    overflowX: 'auto',

    region: 'center',

    xtype: 'panel',
    html: '<strong>Double Click on the border nodes to expand. Right Click to see the content</strong>'+
          '<div class="my-legend">'+
		  '<div class="legend-title"></div>'+
		  '<div class="legend-scale">'+
          '<ul class="legend-labels">'+
    	  '<li><span style="background:'+colour.darkblue+'"></span>trace-bw</li>'+
    	  '<li><span style="background:'+colour.purple+'"></span>trace-fw</li>'+
    	  //'<li><span style="background:'+colour.red+'"></span>expanded</li>'+
     	  '<li><span style="background:'+colour.lightblue+'"></span>stateful</li>'+
   		  '<li><span style="background:'+colour.red+'"></span>cross-run</li>'+
   		  '</ul></div></div>'+
		  '<center> <div style="width:100%" height="700"><canvas id="viewportprov" width="1200" height="500"></canvas></div></center>'
  }],

  listeners: {
    render: function() {
      $(viewportprov).bind('contextmenu', function(e) {
        e.preventDefault();
        var pos = $(this).offset();
        var p = {
          x: e.pageX - pos.left,
          y: e.pageY - pos.top
        }
        selected = nearest = dragged = sys.nearest(p);

        if (selected != null && selected.node != null) {

          // dragged.node.tempMass = 10000
          dragged.node.fixed = true;
          //   addMeta('/j2ep-1.0/prov/streamchunk/?runid='+currentRun+'&id='+selected.node.name)
          singleArtifactStore.setProxy({
            type: 'ajax',
            url: PROV_SERVICE_BASEURL + 'entities/'+selected.node.name,
            reader: {
              rootProperty: 'entities',
              totalProperty: 'totalCount'
            }
          });

          var singleArtifactView = Ext.create('CF.view.SingleArtifactView');

          Ext.create('Ext.window.Window', {
            title: 'Data Detail',
            height: 350,
            width: 800,
            layout: 'fit',
            closeAction: 'hide',
            items: [{
                xtype: 'tabpanel',
                items: [
                  singleArtifactView
                ]
              }

            ]
          }).show();

          singleArtifactStore.data.clear();
          singleArtifactStore.load();
          window.event.returnValue = false;
        }
      });

      $(viewportprov).bind('dblclick', function(e) {
        var pos = $(this).offset();
        var p = {
          x: e.pageX - pos.left,
          y: e.pageY - pos.top
        }
        selected = nearest = dragged = sys.nearest(p);

        if (selected.node !== null) {
          // dragged.node.tempMass = 10000
          dragged.node.fixed = true;
          if (graphMode == "WASDERIVEDFROM") {
            wasDerivedFromAddBranch(PROV_SERVICE_BASEURL + 'wasDerivedFrom/' + selected.node.name + "?level=" + level)
          }

          if (graphMode == "DERIVEDDATA") {
            derivedDataAddBranch(PROV_SERVICE_BASEURL + 'derivedData/' + selected.node.name + "?level=" + level)
          }
        }
        return false;
      });
      sys.renderer = Renderer("#viewportprov");
    }
  }
});

Ext.define('CF.view.ResultsPane', {
  extend: 'Ext.panel.Panel',
  alias: 'widget.resultspane'
});

