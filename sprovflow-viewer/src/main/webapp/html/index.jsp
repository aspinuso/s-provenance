
	<html>
	    <head>
	        <link rel="stylesheet" type="text/css" href="http://cdn.sencha.io/ext-4.1.0-gpl/resources/css/ext-all.css" />
	        <link rel="stylesheet" type="text/css" href="http://openlayers.org/api/2.12-rc3/theme/default/style.css" />
			<script src="http://openlayers.org/api/2.12-rc3/OpenLayers.js"></script>
			<script type="text/javascript" charset="utf-8" src="http://cdn.sencha.io/ext-4.1.0-gpl/ext.js"></script>
			<script type="text/javascript" charset="utf-8" src="<%=request.getContextPath()%>/js/app.js"></script>
			<style>
				.cf-header {
				    background-color: #252F49;
				    border-bottom: 1px solid #16191D;
				    color: white;
				    font-size: 16px;
				    font-weight: bold;
				    padding: 10px;
				    text-align: center;
				    text-shadow: 0 1px 0 #16191D;
				    
				}
				
				.cf-helpwindow {
				    background-color: #FFFFFF;
				    padding: 5px;
				}
				
				.cf-helpwindow div.cascade {
				    padding: 0 0 0 5px;
				}
				
				.cf-helpwindow h2 {
				    margin: 2px 0 0 0;
				}
			</style>
	    </head>
	
	    <body>
	      <div style=" background-color: red; display: none; left: 100px; position: absolute; top: 100px; z-index: 100;">
	       The user is:  {xtype: 'splitter'},<br><br>
	      </div>
	    </body>
	</html>