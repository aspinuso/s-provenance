
<html>
	    <head>
	         <link rel="stylesheet" type="text/css" href="http://cdn.sencha.io/ext-4.2.0-gpl/resources/css/ext-all.css" />
	        <link rel="stylesheet" type="text/css" href="http://openlayers.org/api/2.12-rc3/theme/default/style.css" />
						<script language="javascript" type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.10.1/jquery.min.js"></script>
			<script language="javascript" type="text/javascript" src="<%=request.getContextPath()%>/js/lib/arbor.js" ></script>
			<script language="javascript" type="text/javascript" src="<%=request.getContextPath()%>/js/_/graphics.js" ></script>
			<script language="javascript" type="text/javascript" src="<%=request.getContextPath()%>/js/_/renderer.js" ></script>
			
			<script src="http://openlayers.org/api/2.12-rc3/OpenLayers.js"></script>
			<script type="text/javascript" charset="utf-8" src="http://cdn.sencha.io/ext-4.2.0-gpl/ext-all-dev.js"></script>
  			<script type="text/javascript" charset="utf-8" src="<%=request.getContextPath()%>/js/app.js"></script>
 
			<style>
			#search-results a {
            color: #385F95;
            font:bold 11px tahoma, arial, helvetica, sans-serif;
            text-decoration:none;
        }

        #search-results a:hover {
            text-decoration:underline;
        }

        #search-results p {
            margin:3px !important;
        }

        .search-item {
            font:normal 11px tahoma, arial, helvetica, sans-serif;
            padding:3px 10px 3px 10px;
            border:1px solid #fff;
            border-bottom:1px solid #eeeeee;
            white-space:normal;
            color:#555;
        }
        .search-item h3 {
            display:block;
            font:inherit;
            font-weight:bold;
            color:#222;
        }

        .search-item h3 span {
            float: right;
            font-weight:normal;
            margin:0 0 5px 5px;
            width:100px;
            display:block;
            clear:none;
        }

        .x-form-clear-trigger {
            background-image: url(../../resources/themes/images/default/form/clear-trigger.gif);
        }

        .x-form-search-trigger {
            background-image: url(../../resources/themes/images/default/form/search-trigger.gif);
        }
        
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
	    <%@ include file="init.jsp" %>	
	      <div style=" background-color: red; display: none; left: 100px; position: absolute; top: 100px; z-index: 100;">
	       The user is: <br><br>
	      </div>
	    </body>
	</html>