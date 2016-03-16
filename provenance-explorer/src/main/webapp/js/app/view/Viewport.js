/**
 * The main application viewport, which displays the whole application
 * @extends Ext.Viewport
 */

userSN="aspinuso"
deleteWorkflowURL="portalurl/"
var networks = [{
        "abbr": "G",
        "name": "GEOSCOPE"
    }, {
        "abbr": "AU",
        "name": "Geoscience Australia"
    }, {
        "abbr": "AZ",
        "name": "ANZA Regional Network"
    }, {
        "abbr": "BK",
        "name": "Berkeley Digital Seismograph Network"
    }

];



Ext.define('CF.view.Viewport', {
    extend: 'Ext.Viewport',
    layout: 'fit',

    requires: [
        'Ext.layout.container.Border',
        'Ext.resizer.Splitter',
        'CF.view.ResultsPane'
         
    ],

    initComponent: function () {
        var me = this;

        Ext.apply(me, {  id: 'viewport',
            items: [{
                xtype: 'tabpanel',
                border: 'false',
                layout: 'border',
                defaults: {
                    split: true
                },

                items: [
                
                {
			                        xtype: 'panel',	// Earthquake & Station & Common
			                        title: 'Results',
			                        region: 'center',
			                        border: false,
			                         split: true,
			                      autoScroll:true,
			                        layout: {
 									           type: 'border',
									            padding: 5
 									       },
 								       defaults: {
 								           split: true
 								       },
			                        items: [	 
			                        Ext.create('CF.view.ActivityMonitor'),
			                       
            							         
			                        			
					                        { 
          									  region: 'center',
      								    	  layout: 'border',
      								   		  border: false,
      								   		  autoScroll:true,
    								   	 	  items: [
    								   	 			  
			   		                     			Ext.create('CF.view.provenanceGraphsViewer')
			   		                     			 
			   		                     			,
			   		                     			Ext.create('CF.view.ArtifactView')
			   		                     			]
			   		                     	}
			                        	
			                               
			                              ]
			                    },
			                    {
      xtype: 'panel',
      title: 'iRods',
      region: 'center',
      border: false,
      autoScroll: true,
      layout: 'border',
      defaults: {},
      items: [{
        xtype: "component",
        autoEl: {
          tag: "iframe",
          seamless: "seamless",
          src: ((navigator.userAgent.indexOf('Safari') != -1 && navigator.userAgent.indexOf('Chrome') == -1) ? "/j2ep-1.0/dir-irods/" : "http://dir-irods.epcc.ed.ac.uk/") + "irodsweb/browse.php?ruri=" + (userSN ? userSN + "@" : "") + "dir-irods.epcc.ed.ac.uk%3A1247/UEDINZone/home/" + (userSN ? userSN + "/verce" : "")
        },
        region: 'center',
        border: false
      }]
    }
            ]
          
          }]
          
        });

        me.callParent(arguments);
    }
});


selectedFile = "";

function fileSelection(filetype) {
	Ext.Ajax.request({
		url: getListURL,
		params: {
			userSN: userSN,
			filetype: filetype
		},
		success: function(response){
			showPopup(response.responseText, filetype);	        
		}
	});
}
function showPopup(htmlFileList, filetype)
{
	var filelist = Ext.widget('panel', {
        layout: {
            type: 'vbox',
            align: 'stretch'
        },
        border: false,
        bodyPadding: 10,
        html: htmlFileList,
        buttons: [{
            text: 'Cancel',
            handler: function() {
            	selectedFile = "";
                this.up('window').hide();
            }
        }, {
            text: 'Select',
            handler: function() {
            	parseSelectedFile(this.up('window'), filetype);
            }
        }]
    });

    win = Ext.widget('window', {
        title: 'Select existing file',
        closeAction: 'hide',
        width: 300,
        height: 350,
        layout: 'fit',
        resizable: true,
        modal: true,
        items: filelist
    });
    win.show();
}
function parseSelectedFile(win, filetype)
{
	if(selectedFile==="")
	{
		Ext.Msg.alert("Alert!", "Please, select a file by clicking on it");
	}
	else
	{
		if(filetype===EVENT_TYPE) 	getEvents(ctrl, selectedFile, new QuakeMLXMLFormat());
		if(filetype===STXML_TYPE) 	getStations(ctrl, selectedFile, new StationXMLFormat());
		if(filetype===STPOINTS_TYPE) 	getStations(ctrl, selectedFile, new PointsListFormat());
		selectedFile = "";
		win.hide();
	}
}
function selectFile(e)
{
	$("li").css('background-color', '');
	selectedFile = e.getAttribute('filePath');
	$(e).css('background-color', '#CED9E7');
}
  
