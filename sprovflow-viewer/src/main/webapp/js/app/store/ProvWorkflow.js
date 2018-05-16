/**
 * The store used for summits
 */
Ext.define('CF.store.ProvWorkflow', {
  extend: 'Ext.data.Store',
  restful: true,
  requires: [
    'Ext.grid.*',
    'Ext.data.*',
    'Ext.util.*',
    'Ext.grid.plugin.BufferedRenderer',
    'CF.model.ProvWorkflow'
  ],

  model: 'CF.model.ProvWorkflow',
  alias: 'store.prvworkflow',
  storeId: 'provWorkflowStore',

  // allow the grid to interact with the paging scroller by buffering
  trailingBufferZone: 60,
  buffered: true,
  leadingBufferZone: 10,
  pageSize: 1000,


  proxy: {
    type: 'ajax',
    actionMethods: {
      read: 'GET',
      update: 'POST',
      destroy: 'POST'
    },

    api: {
      read: PROV_SERVICE_BASEURL + 'workflowexecutions?usernames=' + userSN,
      update: PROV_SERVICE_BASEURL + 'workflowexecutions',
      destroy: PROV_SERVICE_BASEURL + 'workflow/delete/'
    },

    reader: {
      root: 'runIds',
      totalProperty: 'totalCount'
    },
    simpleSortMode: true

  },




  listeners: {


    update: {
      fn: function(s, r, o) {

        Ext.Ajax.request({
          method: 'POST',
          url: PROV_SERVICE_BASEURL + 'workflowexecutions/' + r.get('runId')+'/edit',
          params: {
            "doc": '{ "description":"' + r.get('description') + '"}'
          },

          failure: function(response) {

            alert("Workflow Run update failed")


          },

          success: function(response) {

            Ext.Ajax.request({
              url: updateWorkflowDescriptionURL,
              params: {
                "workflowId": r.get('runId'),
                "newText": r.get('description')
              },
              success: function(response) {

                wfStore.load();
              }
            });


          }


        });

      }


    },
    destroy: {
      fn: function(s, r, o) {

        Ext.Ajax.request({
          method: 'POST',
          url: PROV_SERVICE_BASEURL + 'workflowexecutions/' + r.get('runId')+"/delete",


          failure: function(response) {

            alert("Workflow Run delete failed")


          },

          success: function(response) {




          }


        });

      }


    }

  }




});