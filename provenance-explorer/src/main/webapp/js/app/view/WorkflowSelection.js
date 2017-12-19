

var handleReuseResults = function(grid, rowIndex, colIndex) {
  var rec = workflowStore.getAt(rowIndex);

  Ext.getCmp('viewport').setLoading(true);
  // number of asynchronous calls remaining

  var numRemaining = 3;
  alert(rec.get('runId'))
  Ext.Ajax.request({
    url: "/j2ep-1.0/prov/workflowexecutions/" + encodeURIComponent(rec.get('runId')),
    params: {},
    method: 'GET',
    success: function(response) {
      var prov_object = JSON.parse(response.responseText);

      if (prov_object == null) {
        Ext.getCmp('viewport').setLoading(true);
        Ext.Msg.alert("Error", "Workflow missing from provenance repository. Please contact support and list the workflow name and username.");
        return;
      }

      prov_object.input.forEach(function(item) {
        prov_object[item.name] = item;
      });
      delete prov_object.input;

      Ext.Ajax.request({
        url: prov_object.solverconf.url.replace(/http:\/\/[^\/]*\//, '/'),
        success: function(response) {
          var object = JSON.parse(response.responseText);
          if (object === null) {
            Ext.Msg.alert("Failed to get workflow settings");
            Ext.getCmp('viewport').setLoading(false);
            return;
          }

          // reuse velocity when velocity model store finishes loading
          var velocityCombo = Ext.getCmp('velocity');
          velocityCombo.store.addListener('refresh', function() {
            velocityCombo.setValue(object.velocity_model);
            // manually trigger keyup, because change didn't work across browsers
            // but keyup isn't triggered by setvalue
            velocityCombo.fireEvent('keyup', velocityCombo);

            if (object.custom_mesh) {
              velocityCombo.up('form').getForm().findField('minlat').setValue(object.custom_mesh_boundaries.minlat);
              velocityCombo.up('form').getForm().findField('maxlat').setValue(object.custom_mesh_boundaries.maxlat);
              velocityCombo.up('form').getForm().findField('minlon').setValue(object.custom_mesh_boundaries.minlon);
              velocityCombo.up('form').getForm().findField('maxlon').setValue(object.custom_mesh_boundaries.maxlon);
            }

            CF.app.getController('Map').getStore('SolverConf').loadData(object.fields);

            // HACK ensure correct event binding order by binding here
            var eventLayer = CF.app.getController('Map').mapPanel.map.getLayersByName('Events')[0];
            CF.app.getController('Map').getStore('Event').bind(eventLayer);

            eventLayer.events.on({
              featureadded: function(event) {},
              featuresadded: function(event) {
                event.features.forEach(function(feature) {
                  if (object.events.indexOf(feature.data.eventId) >= 0) {
                    CF.app.getController('Map').mapPanel.map.getControl('dragselect').select(feature);
                  } else {
                    CF.app.getController('Map').mapPanel.map.getControl('dragselect').unselect(feature);
                  }
                });
                eventLayer.events.un(this);
                if (--numRemaining === 0) {
                  Ext.getCmp('viewport').setLoading(false);
                }
              },
              scope: this
            });

            // reuse events
            CF.app.getController('Map').getEvents(CF.app.getController('Map'), prov_object.quakeml.url.replace(/http:\/\/[^\/]*\//, '/'));

            var stationFileType = prov_object.stations['mime-type'] === 'application/xml' ? STXML_TYPE : STPOINTS_TYPE;
            var record = Ext.getCmp('station-filetype').getStore().findRecord('abbr', stationFileType);
            Ext.getCmp('station-filetype').select(stationFileType);

            // HACK ensure correct event binding order by binding here
            var stationLayer = CF.app.getController('Map').mapPanel.map.getLayersByName('Stations')[0];
            CF.app.getController('Map').getStore('Station').bind(stationLayer);

            stationLayer.events.on({
              featureadded: function(event) {},
              featuresadded: function(event) {
                event.features.forEach(function(feature) {
                  if (object.stations.indexOf(feature.data.network + '.' + feature.data.station) >= 0) {
                    CF.app.getController('Map').mapPanel.map.getControl('dragselect').select(feature);
                  } else {
                    CF.app.getController('Map').mapPanel.map.getControl('dragselect').unselect(feature);
                  }
                });
                stationLayer.events.un(this);
                if (--numRemaining === 0) {
                  Ext.getCmp('viewport').setLoading(false);
                }
              },
              scope: this
            });

            // reuse stations
            CF.app.getController('Map').getStations(CF.app.getController('Map'), prov_object.stations.url.replace(/http:\/\/[^\/]*\//, '/'), stationFileType);

            // Only set old workflow if it's still available
            if (prov_object.workflowId != null) {
              var workflowDropdown = Ext.getCmp('wfSelection');
              if (workflowDropdown.store.findRecord('workflowId', prov_object.workflowId) == null) {
                Ext.Msg.alert("Error", "Workflow used in old run not available anymore. Select a new workflow in the Submit tab.");
                workflowDropdown.clearValue();
              } else {
                workflowDropdown.setValue(prov_object.workflowId);
              }
            }

            Ext.getCmp('submitName').setValue(prov_object._id.slice(0, -14)); // remove runid
            Ext.getCmp('submitMessage').setValue(prov_object.description);
          }, this, {
            single: true
          });

          // set mesh when solverconfstore finishes loading
          CF.app.getController('Map').getStore('SolverConf').addListener('refresh', function() {
            // reuse mesh and trigger velocity store reload
            Ext.getCmp('meshes').setValue(object.mesh);
            // manually trigger keyup, because change didn't work across browsers
            // but keyup isn't triggered by setvalue
            Ext.getCmp('meshes').fireEvent('keyup', Ext.getCmp('meshes'));

            if (--numRemaining === 0) {
              Ext.getCmp('viewport').setLoading(false);
            }
          }, this, {
            single: true
          });

          // reuse solver
          var solverType = Ext.getCmp('solvertype');
          var solver = solverType.store.findRecord('name', object.solver);
          if (solver != null) {
            solverType.clearValue();
            solverType.setValue(solver.get('abbr'));
          } else {
            // TODO fix partial reuse when solver unavailable
            Ext.Msg.alert("Solver from old run now unavailable. Please select another one on the Solver tab.");
            Ext.getCmp('viewport').setLoading(false);
            return;
          }
        },
        failure: function(response) {
          Ext.Msg.alert("Error", "Failed to get workflow settings!");
          Ext.getCmp('viewport').setLoading(false);
        }
      })
    },
    failure: function(response) {
      Ext.Msg.alert("Error", "Failed to get workflow from provenance api!");
      Ext.getCmp('viewport').setLoading(false);
    }
  })
};





Ext.define('CF.view.WorkflowSelection', {
  extend: 'Ext.grid.Panel',
  alias: 'widget.workflowselection',
  requires: [
    'CF.store.Workflow',
    'Ext.grid.plugin.BufferedRenderer'
  ],

  width: 780,
  disableSelection: true,

  autoHeight: true,

  store: Ext.data.StoreManager.lookup('provWorkflowStore'),

  border: false,

  loadMask: true,

  columns: [{
      xtype: 'rownumberer',

      sortable: false
    }, {
      header: 'Run ID',
      dataIndex: 'runId',
      flex: 5,
      sortable: false
    }, {
      header: 'Workflow Name',
      dataIndex: 'workflowName',
      flex: 3,
      sortable: false,
      groupable: false
    }, {
      header: 'Description - Click to Edit',
      dataIndex: 'description',
      flex: 3,
      sortable: false,
      field: {
        xtype: 'textfield',
        allowBlank: true,
        maxLength: 50
      }
    }, {
      header: 'Date',
      dataIndex: 'date',
      flex: 3,
      sortable: false,
      groupable: false
    }, // custom mapping
    {
      xtype: 'actioncolumn',
      width: 20,
      icon: localResourcesPath + '/img/Farm-Fresh_arrow_rotate_clockwise.png',
      tooltip: 'Reuse',
      handler: handleReuseResults
    },
    {
      xtype: 'actioncolumn',
      width: 20,
      tdCls: 'Delete',
      items: [{
        icon: localResourcesPath + '/img/delete-icon.png', // Use a URL in the icon config
        tooltip: 'Delete',
        handler: function(grid, rowIndex, colIndex) {
          var rec = grid.getStore().getAt(rowIndex);

          var storeClassName = Ext.getClassName(grid.getStore());
          var tempStore = Ext.create(storeClassName, {
            buffered: false
          });
          tempStore.add(rec);
          var xx = tempStore.getAt(0)
          messagebox = Ext.Msg.confirm('Remove Run', 'Are you sure?', function(button) {
            if (button == 'yes') {
              var tempx = tempStore.getProxy();
              tempx.api.destroy = PROV_SERVICE_BASEURL + "workflowexecutions/" + xx.get("runId")+"/delete";

              tempStore.remove(xx);

              tempStore.sync({
                success: function(args) {
                  Ext.Ajax.request({
                    url: deleteWorkflowURL,
                    params: {
                      "workflowId": xx.get('systemId')
                    },
                    success: function(response) {
                      Ext.Msg.alert("Completed", "Data for Run ID "+xx.get("runId")+" has been successfully removed")
                    },
                    failure: function(response) {
					  Ext.Msg.alert("Error", "Error deleting workflow information from gUSE")
                    }
                  })
                  //PHPSESSID=vsb9rpreoten67g945pghhtde6
                 
                  Ext.util.Cookies.set('PHPSESSID',"1t1vt2c50oilnm21q9072gdbp6")
                   
                  
                  Ext.Ajax.request({
                    url: deleteWorkflowDataURL,
                    method: "POST",
                    withCredentials : true,
    				useDefaultXhrHeader : false,
                    params: {
                      "ruri": IRODS_URI,
                      "dirs[]":	xx.get("runId")

                    },
                    success: function(response) {
                      wfStore.load();
                    },
                    failure: function(response) {
                    
                    	
                    	Ext.Msg.alert("Error", "Error deleting data for Run ID "+xx.get("runId"))

                    }
                  })

                  // workflowStore.data.clear()
                  workflowStore.load()


                },

                faliure: function(args) {

                  Ext.Msg.alert("Error", "Delete failed!");

                }

              })



            }
          })
          messagebox.zIndexManager.bringToFront(messagebox);



        }



      }]
    }
  ],
  flex: 1,
  selType: 'cellmodel',
  plugins: [
    Ext.create('Ext.grid.plugin.CellEditing', {
      clicksToEdit: 1,
      listeners: {
        'validateedit': function(c, e, eOpts) {
          var r = e.rowIdx;
          var sr = workflowStore.getAt(r);

          sr.set(e.field, e.value);

          workflowStore.load()
        }
      }
    })
  ],

  /*   verticalScroller: {
        xtype: 'paginggridscroller'
    },*/



  /* plugins: [{
        ptype: 'bufferedrenderer'
    }],*/


  /* selModel: {
        pruneRemoved: false
    },
*/
  initComponent: function() {
    this.callParent(arguments);
  },

  viewConfig: {
    enableTextSelection: true,
    listeners: {

      itemclick: function(dv, record, item, index, e) {
        workflowStore.sync()
      },
      itemdblclick: function(dataview, record, item, index, e) {

        activityStore.setProxy({
          type: 'ajax',
          //url: PROV_SERVICE_BASEURL + 'activities/' + encodeURIComponent(record.get("runId"))+'?method=aggregate',
          url: PROV_SERVICE_BASEURL + '/workflowexecutions/'+encodeURIComponent(record.get("runId"))+'/instances',
          
          reader: {
            rootProperty: '@graph',
            totalProperty: 'totalCount'
          },
          simpleSortMode: true

        });
        sys.prune();
        artifactStore.data.clear();
        activityStore.data.clear();
        activityStore.load({
          callback: function() {
            currentRun = record.get("runId")
            Ext.getCmp('filtercurrent').enable();
            Ext.getCmp('searchartifacts').enable();
            Ext.getCmp('downloadscript').enable();




          }

        })

        activityStore.on('load', onStoreLoad, this, {
          single: true
        });
        currentRun = record.get("runId")
        owner = userSN

      }




    }
  }


});