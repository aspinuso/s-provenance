<!DOCTYPE html>
<meta charset="utf-8">
<style>

.node {
  font: 300 11px "Helvetica Neue", Helvetica, Arial, sans-serif;
  fill: #bbb;
}

 body{ text-align:center}
 
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
<body><center>

<script src="//d3js.org/d3.v3.min.js"></script>
<script>
PROV_SERVICE_BASEURL="/j2ep-1.0/prov/"
RAD_MODE='<%= request.getParameter("level") %>'
RAD_GB='<%= request.getParameter("groupby") %>'
qstring='<%= request.getQueryString() %>'
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
    .attr("transform", "translate(" + radius*1.5 + "," + radius*1.5 + ")");

var link = svg.append("g").selectAll(".link"),
    node = svg.append("g").selectAll(".node");

d3.json(PROV_SERVICE_BASEURL + "workflow/summaries?"+qstring, function(error, classes) {
  if (error) throw error;

   
  
  if (RAD_MODE=='vrange') 
  {
   nodes = cluster.nodes(packageHierarchyPE(classes));
   links = packageConnlistPEs(nodes);
   link = link
      .data(bundle(links))
    .enter().append("path")
      .each(function(d) {  d.source = d[0], d.target = d[d.length - 1];})
      .attr("class", "link")
      .attr("d", line)
      .attr("stroke", 'rgb(0,0,150)');
   
   }
   
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
      								
      								if (size<100)
      									return 'rgb('+0+','+Math.trunc(256-size*256/maxval)+','+0+')'
									if (size>=100 && size<1000)
										return 'rgb('+Math.trunc(256-256/maxval)+','+0+','+0+')'	
									if (size>=1000)
										{console.log(size)	
										return 'rgb('+0+','+0+','+Math.trunc(size*256/maxval)+')'	
										}
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
      								
      								if (size<100)
      									return 'rgb('+0+','+Math.trunc(256-size*256/maxval)+','+0+')'
									if (size>=100 && size<1000)
										return 'rgb('+Math.trunc(256-256/maxval)+','+0+','+0+')'	
									if (size>=1000)
										{console.log(size)	
										return 'rgb('+0+','+0+','+Math.trunc(size*256/maxval)+')'	
										}
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
      								
      								if (size<100)
      									return 'rgb('+0+','+Math.trunc(256-size*256/maxval)+','+0+')'
									if (size>=100 && size<1000)
										return 'rgb('+Math.trunc(256-256/maxval)+','+0+','+0+')'	
									if (size>=1000)
										{console.log(size)	
										return 'rgb('+0+','+0+','+Math.trunc(size*256/maxval)+')'	
										}
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

  
// Lazily construct the basic hierarchy from Instances ids .
function packageHierarchyInstances(classes,gb) {
 var map = {};
 var parent
 console.log(gb)
 var root = {name: 'process', children: []};
 classes.forEach(function(d) {
//    find(d.name, d);
	//if(!d.name.worker) d.name.worker="login";
	
    if (!map[d.name[gb]])
    	{console.log(d.name[gb])
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
    node.key=d.name.actedOnBehalfOf.substring(0,20)
    
    
    
   
 });
 
 console.log(root)
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
    else
    {
    	
    	node.key=d.name.instanceId.substring(0,45)
    	d.name.iterationId=d.name.instanceId
   	 }
    
   
 });
 
 console.log(root)
 return root
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
      
      connlist.push({source: map[d.name.instanceId], target: map[i._id.instanceId]});
      bundlesmap[d.name.instanceId+"_"+i._id.instanceId]=i.size
      if (i.size>maxval) maxval=i.size
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

</script>
</center>
</body>
