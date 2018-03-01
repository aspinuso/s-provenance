 <!DOCTYPE html>
<meta charset="utf-8">
<style>

 
 .my-legend .legend-title {
    text-align: left;
    margin-bottom: 8px;
    font-weight: bold;
    font-size: 120%;
    
    }
  .my-legend .legend-scale ul {
    margin: 0;
    padding: 0;
    float: left;
    list-style: none;
    }
  .my-legend .legend-scale ul li {
    display: block;
    float: left;
    width: 50px;
    margin-bottom: 6px;
    text-align: center;
    font-size: 80%;
    list-style: none;
    }
  .my-legend ul.legend-labels li span {
    display: block;
    float: left;
    height: 15px;
    width: 50px;
    }
  .my-legend .legend-source {
    font-size: 120%;
    clear: both;
    }
  .my-legend a {
    color: #777;
    }
    
.node {
  font: 300 11px "Helvetica Neue", Helvetica, Arial, sans-serif;
  fill: #bbb;
}

 body{ text-align:center;
 	   font-family:"Helvetica Neue", Helvetica, Arial, sans-serif;
 }
 
.node:hover {
  fill: #000;
}

.link {
  
  stroke-opacity: .3;
  fill: none;
  pointer-events: none;
}

.node:hover,
.node--source,
.node--target {
  font-weight: 700;
}

.node--source {
  fill: #2ca02c;
}

.node--target {
  fill: #d62728;
}

.link--source,
.link--target {
  stroke-opacity: 1;
  stroke-width: 2px;
}

.link--source {
  stroke: #d62728;
}

.link--target {
  stroke: #2ca02c;
}

</style>
<body>
<center>

<script src="//d3js.org/d3.v3.min.js"></script>
<script>
PROV_SERVICE_BASEURL="/j2ep-1.0/prov/"
RAD_MODE='<%= request.getParameter("level") %>'
RAD_GB='<%= request.getParameter("groupby") %>'
qstring='<%= request.getQueryString() %>'
RUN_ID='<%= request.getParameter("runId") %>'
USERS='<%= request.getParameter("users") %>'


USERS=USERS.split(',');


function getRandomColor() {
    var letters = '0123456789ABCDEF'.split('');
    var color = '#';
    for (var i = 0; i < 6; i++ ) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

usrclmap={}
USERS.forEach(function(d) {
							usrclmap[d]=getRandomColor()
	 						}
	 		 );

var diameter = 960,
    radius = diameter / 2,
    innerRadius = radius - 120;


var maxval=0
var bundlesmap=[]

var cluster = d3.layout.cluster()
    .size([360, innerRadius])
    .sort(null)
    .value(function(d) { return d.size; });

var bundle = d3.layout.bundle();

var line = d3.svg.line.radial()
    .interpolate("bundle")
    .tension(.75)
    .radius(function(d) { return d.y; })
    .angle(function(d) { return d.x / 180 * Math.PI; });

var svg = d3.select("body").append("svg")
    .attr("width", diameter*1.5)
    .attr("height", diameter*1.5)
    .attr("margin-left", 200)
  .append("g")
    .attr("transform", "translate(" + radius*1.5 + "," + radius*1.3 + ")");

var link = svg.append("g").selectAll(".link"), node = svg.append("g").selectAll(".node");

d3.json(PROV_SERVICE_BASEURL + "workflow/summaries?"+qstring, function(error, classes) {
  if (error) throw error;

if (RAD_MODE=='data') 
  {
   nodes = cluster.nodes(packageHierarchyData(classes,RAD_GB));
  
   links = packageConnlistData(nodes);
   //console.log(nodes)
   link = link
      .data(bundle(links))
    .enter().append("path")
      .each(function(d) {  d.source = d[0], d.target = d[d.length - 1];})
      .attr("class", "link")
      .attr("d", line)
      .attr("stroke", 'rgb(0,0,150)');
      
      
      
       node = node
      .data(nodes.filter(function(n) { return !n.children; }))
    .enter().append("text")
      .attr("class", "node")
      .attr("dy", ".31em")
      .attr("transform", function(d) { return "rotate(" + (d.x - 90) + ")translate(" + (d.y + 8) + ",0)" + (d.x < 180 ? "" : "rotate(180)"); })
      .style("fill", function(d) { return usrclmap[d.name.username]})
      .style("text-anchor", function(d) { return d.x < 180 ? "start" : "end"; })
      .text(function(d) { return d.key; })
      .on("mouseover", mouseovered)
      .on("mouseout", mouseouted);

   
   }
   else
    
  if (RAD_MODE=='vrange') 
  {
   nodes = cluster.nodes(packageHierarchyPE(classes,RAD_GB));
  
   links = packageConnlistPEs(nodes);
   link = link
      .data(bundle(links))
    .enter().append("path")
      .each(function(d) {  d.source = d[0], d.target = d[d.length - 1];})
      .attr("class", "link")
      .attr("d", line)
      .attr("stroke", 'rgb(0,0,150)');
      
      
      
       node = node
      .data(nodes.filter(function(n) { return !n.children; }))
    .enter().append("text")
      .attr("class", "node")
      .attr("dy", ".31em")
      .attr("transform", function(d) { return "rotate(" + (d.x - 90) + ")translate(" + (d.y + 8) + ",0)" + (d.x < 180 ? "" : "rotate(180)"); })
      .style("fill", function(d) { return usrclmap[d.name.username]})
      .style("text-anchor", function(d) { return d.x < 180 ? "start" : "end"; })
      .text(function(d) { return d.key; })
      .on("mouseover", mouseovered)
      .on("mouseout", mouseouted);

   
   }
   else
   
  if (RAD_MODE=='instances') {
  
  nodes = cluster.nodes(packageHierarchyInstances(classes,RAD_GB));
  links = packageConnlistInstances(nodes);
   
  	
  link = link
      .data(bundle(links))
    .enter().append("path")
      .each(function(d) {  d.source = d[0], d.target = d[d.length - 1];})
      .attr("class", "link")
      .attr("d", line)
      .attr("stroke", function(d) { var size=bundlesmap[d.source.name.instanceId+"_"+d.target.name.instanceId]
      								//console.log(d.source.name.instanceId+" "+size) 
      								if (size<100)
      									return 'rgb(255,0,0)'
									if (size>=100 && size<500)
										return '#FF8621'	
									if (size>=500 && size<1000)
										return 'rgb(59,230,0)'	
									if (size>=1000 && size<5000)
										return 'rgb(0,102,255)'	
									if (size>=5000 && size<10000)
										return 'rgb(119,0,255)'	
									if (size>=10000)
										return 'rgb(247,0,255)'	
									});
  
  } 
  
  if (RAD_MODE=='iterations') {
  
  nodes = cluster.nodes(packageHierarchyIterations(classes,RAD_GB));
  links = packageConnlistIterations(nodes);
  
  link = link
      .data(bundle(links))
    .enter().append("path")
      .each(function(d) {  d.source = d[0], d.target = d[d.length - 1];})
      .attr("class", "link")
      .attr("d", line)
      .attr("stroke", function(d) { var size=bundlesmap[d.source.name.iterationId+"_"+d.target.name.iterationId]
      								//console.log(d.source.name.iterationId+" "+size) 
      						/*		if (size<100)
      									return 'rgb('+0+','+Math.trunc(256-size*256/maxval)+','+0+')'
									if (size>=100 && size<1000)
										return 'rgb('+Math.trunc(256-256/maxval)+','+0+','+0+')'	
									if (size>=1000)
										{//console.log(size)	
										return 'rgb('+0+','+0+','+Math.trunc(size*256/maxval)+')'	
										}
									});*/
									
   									if (size<100)
      									return 'rgb(255,0,0)'
									if (size>=100 && size<500)
										return '#FF8621'	
									if (size>=500 && size<1000)
										return 'rgb(59,230,0)'	
									if (size>=1000 && size<5000)
										return 'rgb(0,102,255)'	
									if (size>=5000 && size<10000)
										return 'rgb(119,0,255)'	
									if (size>=10000)
										return 'rgb(247,0,255)'	
									});
  
  } 
  
    if (RAD_MODE=='prospective') {
  
  nodes = cluster.nodes(packageHierarchyProspective(classes,RAD_GB));
  links = packageConnlistProspective(nodes);
  link = link
      .data(bundle(links))
    .enter().append("path")
      .each(function(d) {  d.source = d[0], d.target = d[d.length - 1];})
      .attr("class", "link")
      .attr("d", line)
      .attr("stroke", function(d) { var size=bundlesmap[d.source.name.actedOnBehalfOf+"_"+d.target.name.actedOnBehalfOf]
      								//console.log(d.source.name.actedOnBehalfOf+" "+size) 
      								if (size<100)
      									return 'rgb(255,0,0)'
									if (size>=100 && size<500)
										return '#FF8621'		
									if (size>=500 && size<1000)
										return 'rgb(59,230,0)'	
									if (size>=1000 && size<5000)
										return 'rgb(0,102,255)'	
									if (size>=5000 && size<10000)
										return 'rgb(119,0,255)'	
									if (size>=10000)
										return 'rgb(247,0,255)'	
									});
  
  } 
  
  if (RAD_MODE=='workers') {
  
  nodes = cluster.nodes(packageHierarchyWorkers(classes));
  links = packageConnlistWorkers(nodes);
  
  } 
  
  if (RAD_MODE=='pid') {
  
  nodes = cluster.nodes(packageHierarchyPid(classes));
  links = packageConnlistPid(nodes);
  
  } 
   
  
 
  node = node
      .data(nodes.filter(function(n) { return !n.children; }))
    .enter().append("text")
      .attr("class", "node")
      .attr("dy", ".31em")
      .attr("transform", function(d) { return "rotate(" + (d.x - 90) + ")translate(" + (d.y + 8) + ",0)" + (d.x < 180 ? "" : "rotate(180)"); })
      .style("fill", function(d) { if (d.name.mapping == "multi") return "#A17A8E"; if (d.name.mapping == "mpi") return "#216880"; if (d.name.mapping == "simple") return "#bbb" ;})
      .style("text-anchor", function(d) { return d.x < 180 ? "start" : "end"; })
      .text(function(d) { return d.key; })
      .on("mouseover", mouseovered)
      .on("mouseout", mouseouted);
});

function mouseovered(d) {
  node
      .each(function(n) { n.target = n.source = false; });

  link
      .classed("link--target", function(l) { if (l.target === d) return l.source.source = true; })
      .classed("link--source", function(l) { if (l.source === d) return l.target.target = true; })
      .filter(function(l) { return l.target === d || l.source === d; })
      .each(function() { this.parentNode.appendChild(this); });

  node
      .classed("node--target", function(n) { return n.target; })
      .classed("node--source", function(n) { return n.source; });
}

function mouseouted(d) {
  link
      .classed("link--target", false)
      .classed("link--source", false);

  node
      .classed("node--target", false)
      .classed("node--source", false);
}

d3.select(self.frameElement).style("height", diameter + "px");

// Lazily construct the basic hierarchy from PE names.



function packageHierarchyData(classes,gb) {
 var map = {};
 var parent
 //console.log(gb)
 var root = {name: 'process', children: []};
 classes.forEach(function(d) {
//    find(d.name, d);
	//if(!d.name.worker) d.name.worker="login";
	
    if (!map[d.name[gb]])
    	{//console.log(d.name[gb])
    	 parent = {name: { name: d.name[gb]}, children: []};
    	 parent.parent=root
    	 parent.parent.children.push(parent)
    	 map[d.name[gb]]=parent
    	}
    
    var node = d
    //console.log(root) 
  	node.parent= map[d.name[gb]]
    node.parent.children.push(node)
    node.key=d.name.id.substring(0,45)
    
   
 });

 //console.log(root)
 return root
}


function packageHierarchyPE(classes,gb) {
 var map = {};
 var parent
 //console.log(gb)
 var root = {name: 'process', children: []};
 classes.forEach(function(d) {
//    find(d.name, d);
	//if(!d.name.worker) d.name.worker="login";
	
    if (!map[d.name[gb]])
    	{//console.log(d.name[gb])
    	 parent = {name: { name: d.name[gb]}, children: []};
    	 parent.parent=root
    	 parent.parent.children.push(parent)
    	 map[d.name[gb]]=parent
    	}
    
    var node = d
    //console.log(root) 
  	node.parent= map[d.name[gb]]
    node.parent.children.push(node)
    node.key=d.name.runId.substring(0,45)
    
   
 });

 //console.log(root)
 return root
}

// Lazily construct the basic hierarchy from Instances ids .
function packageHierarchyInstances(classes,gb) {
 var map = {};
 var parent
 //console.log(gb)
 var root = {name: 'process', children: []};
 classes.forEach(function(d) {
//    find(d.name, d);
	//if(!d.name.worker) d.name.worker="login";
	
    if (!map[d.name[gb]])
    	{//console.log(d.name[gb])
    	 parent = {name: { name: d.name[gb]}, children: []};
    	 parent.parent=root
    	 parent.parent.children.push(parent)
    	 map[d.name[gb]]=parent
    	}
    
    var node = d 
  	node.parent= map[d.name[gb]]
    node.parent.children.push(node)
    node.key=d.name.instanceId.substring(0,45)
    
   
 });
 
 //console.log(root)
 return root
}


// Lazily construct the basic hierarchy from Instances ids .
function packageHierarchyProspective(classes,gb) {
 var map = {};
 var parent
 var root = {name: 'process', children: []};
 classes.forEach(function(d) {
//    find(d.name, d);
	//if(!d.name.worker) d.name.worker="login";
	
    if (!map[d.name[gb]])
    	{
    	 parent = {name: { name: d.name[gb]}, children: []};
    	 parent.parent=root
    	 parent.parent.children.push(parent)
    	 map[d.name[gb]]=parent
    	}
    
    var node = d 
  	node.parent= map[d.name[gb]]
    node.parent.children.push(node)
    try {
    node.key=d.name.actedOnBehalfOf.substring(0,20)
    }catch (e){
    node.key=d.name.name
    }
    
    
   
 });
 
 //console.log(root)
 return root
}

// Lazily construct the basic hierarchy from Instances ids .
function packageHierarchyIterations(classes,gb) {
 var map = {};
 var parent
 var root = {name: 'process', children: []};
 classes.forEach(function(d) {
//    find(d.name, d);
	//if(!d.name.worker) d.name.worker="login";
	
     if (!map[d.name[gb]])
    	{
    	 parent = {name: { name: d.name[gb]}, children: []};
    	 parent.parent=root
    	 parent.parent.children.push(parent)
    	 map[d.name[gb]]=parent
    	}
    
    var node = d 
  	node.parent= map[d.name[gb]]
    node.parent.children.push(node)
    if (d.name.iterationId)
	    node.key=d.name.iterationId.substring(0,45)
    
    
   
 });
 
 //console.log(root)
 return root
}



// Return a list of imports for the given array of nodes.
function packageConnlistPEs(nodes) {
  var map = {},
      connlist = [];

  // Compute a map from name to node.
  nodes.forEach(function(d) {
    map[d.name.runId] = d;
  });

  // For each import, construct a link from the source to target node.
  
  nodes.forEach(function(d) {
    //console.log(map[d.name.run].connlist) 
    if (d.connlist) d.connlist.forEach(function(i) { 
    
      if (map[i]!=undefined){
      	  //console.log(map[d.name.run].name.run+" "+map[i])
	      connlist.push({source: map[d.name.runId], target: map[i]});
	      }
    });
  });

  return connlist;
}



function packageConnlistData(nodes) {
  var map = {},
      connlist = [];

  // Compute a map from name to node.
  nodes.forEach(function(d) {
    map[d.name.id] = d;
  });

  // For each import, construct a link from the source to target node.
  
  nodes.forEach(function(d) {
    //console.log(map[d.name.id].connlist) 
    if (d.connlist) d.connlist.forEach(function(i) { 
    //console.log(d.connlist) 
      if (map[i.id]!=undefined){
      	  console.log(map[d.name.id].name.id+" "+map[i.id].name.id)
	      connlist.push({source: map[d.name.id], target: map[i.id]});
	      }
    });
  });

  return connlist;
}


function packageConnlistInstances(nodes) {
  var map = {},
      connlist = [];

  // Compute a map from name to node.
  nodes.forEach(function(d) {
    map[d.name.instanceId] = d;
  });

  // For each import, construct a link from the source to target node.
  
  nodes.forEach(function(d) {
    if (d.connlist) d.connlist.forEach(function(i) { 
      if (map[i._id.instanceId]){
      connlist.push({source: map[d.name.instanceId], target: map[i._id.instanceId]});
      bundlesmap[d.name.instanceId+"_"+i._id.instanceId]=i.size
      if (i.size>maxval) maxval=i.size}
    });
  });

  return connlist;
}


function packageConnlistIterations(nodes) {
  var map = {},
      connlist = [];

  // Compute a map from name to node.
  nodes.forEach(function(d) {
    map[d.name.iterationId] = d;
  });

  // For each import, construct a link from the source to target node.
  
  nodes.forEach(function(d) {
    if (d.connlist) d.connlist.forEach(function(i) { 
      if (map[i._id.iterationId])
	      {connlist.push({source: map[d.name.iterationId], target: map[i._id.iterationId]});
    	  bundlesmap[d.name.iterationId+"_"+i._id.iterationId]=i.size
      	  if (i.size>maxval) maxval=i.size}
    });
  });

  return connlist;
}

function packageConnlistProspective(nodes) {
  var map = {},
      connlist = [];

  // Compute a map from name to node.
  nodes.forEach(function(d) {
    map[d.name.actedOnBehalfOf] = d;
  });

  // For each import, construct a link from the source to target node.
  
  nodes.forEach(function(d) {
    if (d.connlist) d.connlist.forEach(function(i) { 
      
      connlist.push({source: map[d.name.actedOnBehalfOf], target: map[i._id.actedOnBehalfOf]});
      bundlesmap[d.name.actedOnBehalfOf+"_"+i._id.actedOnBehalfOf]=i.size
      if (i.size>maxval) maxval=i.size
    });
  });

  return connlist;
}

function UpdateQueryString(key, value, url) {
    if (!url) url = window.location.href;
    var re = new RegExp("([?&])" + key + "=.*?(&|#|$)(.*)", "gi"),
        hash;

    if (re.test(url)) {
        if (typeof value !== 'undefined' && value !== null)
            return url.replace(re, '$1' + key + "=" + value + '$2$3');
        else {
            hash = url.split('#');
            url = hash[0].replace(re, '$1$3').replace(/(&|\?)$/, '');
            if (typeof hash[1] !== 'undefined' && hash[1] !== null) 
                url += '#' + hash[1];
            return url;
        }
    }
    else {
        if (typeof value !== 'undefined' && value !== null) {
            var separator = url.indexOf('?') !== -1 ? '&' : '?';
            hash = url.split('#');
            url = hash[0] + separator + key + '=' + value;
            if (typeof hash[1] !== 'undefined' && hash[1] !== null) 
                url += '#' + hash[1];
            return url;
        }
        else
            return url;
    }
}

function updateURLParameter(url, param, paramVal){
    var newAdditionalURL = "";
    var tempArray = url.split("?");
    var baseURL = tempArray[0];
    var additionalURL = tempArray[1];
    var temp = "";
    if (additionalURL) {
        tempArray = additionalURL.split("&");
        for (i=0; i<tempArray.length; i++){
            if(tempArray[i].split('=')[0] != param){
                newAdditionalURL += temp + tempArray[i];
                temp = "&";
            }
        }
    }

    var rows_txt = temp + "" + param + "=" + paramVal;
    return baseURL + "?" + newAdditionalURL + rows_txt;
}

function reload(par,sel){
  var myselect = document.getElementById(sel);
  url=window.location+""
  if (sel=='setrange'){
  	
  	url=updateURLParameter(url,'minidx',document.forms[0].minidx.value)
  	url=updateURLParameter(url,'maxidx',document.forms[0].maxidx.value)
  	url=updateURLParameter(url,'starttime',document.forms[0].starttime.value)
  	window.location=url
  
  	}
  	else
  	
  		window.location=updateURLParameter(url,par,myselect.value)
  
  
}


</script>
<h2>Radial Provenance Analysis for '<%= request.getParameter("runId") %>' with tags '<%= request.getParameter("tags") %>'</h2>
<div class='my-legend'>
<div class='legend-title'>Edges: Data Transfer (bytes)</div>
<div class='legend-scale'>
  <ul class='legend-labels'>
    <li><span style='background:rgb(255,0,0)'></span>100</li>
     <li><span style='background:#FF8621'></span>500</li>
    <li><span style='background:rgb(59,230,0)'></span>1000</li>
    <li><span style='background:rgb(0,102,255)'></span>5000</li>
     <li><span style='background:rgb(119,0,255)'></span>10000</li>
      <li><span style='background:rgb(247,0,255)'></span>>10000</li>
      
  </ul>
</div>
</div>

<br/>

<br/>
<div class='my-legend'>
<div class='legend-title'>Nodes: Mappings</div>
<div class='legend-scale'>
  <ul class='legend-labels'>
    <li><span style='background:#bbb'></span>simple</li>
     <li><span style='background:#A17A8E'></span>multi</li>
    <li><span style='background:#216880'></span>mpi</li>
  </ul>
</div>  
</div>

<br/>
<br/>



<div class='legend-source'>Level: <strong><%= request.getParameter("level") %></strong></div>

 <select onchange="reload('level','selectLevel')" id="selectLevel">
  <option value="xx">Select Level</option>
  <option value="prospective">prospective</option>
  <option value="instances">instances</option>
  <option value="iterations">iterations</option>
</select> 
<form name="indexrange">
<% if (request.getParameter("level").equals("iterations")) { %>
<strong>Iteration Range:</strong> 
  minidx
  <input type="number" name="minidx" min="0" value="<%= request.getParameter("minidx") %>">
  maxidx
  <input type="number" name="maxidx" min="1" value="<%= request.getParameter("maxidx") %>">
   start-time
  <input type="string" name="starttime"  value="<%= request.getParameter("starttime") %>">
  
  <input type="button" name="setrange" value="change range" onclick="reload('','setrange')" />
<% 
}
%>
</form>
<br/><br/>
<div class='legend-source'>Grouping: <strong><%= request.getParameter("groupby") %></strong></div>

 <select onchange="reload('groupby','selectGroup')" id="selectGroup">
  <option value="xx">Select Grouping</option>
  <option value="pid">pid</option>
  <option value="worker">worker</option>
  <option value="instanceId">instanceId</option>
  <option value="actedOnBehalfOf">actedOnBehalfOf</option>
  <option value="runId">runId</option>
  <option value="name">name</option>
</select> 
<br/><br/>
<div class='legend-source'>Tags: <strong><%= request.getParameter("tags") %></strong></div>

 <input type="text" id="mytags" placeholder="Insert tags..."/>
 <button type="button" onclick="reload('tags','mytags')">Go!</button>
</div>
<br/><br/>
</center>
</body>
