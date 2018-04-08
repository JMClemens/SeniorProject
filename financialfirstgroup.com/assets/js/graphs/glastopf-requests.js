var width = 450,
		height = 450,
		radius = Math.min(width, height) / 2;
		
var color = ["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56", "#d0743c"];
	
d3.csv("grf.csv", function(error, data) {

  data.forEach(function(d) {
    d.Frequency = +d.Frequency;
  });
	
var svg = d3.select("g-request-pie").append("svg")
		.data(data)
    .attr("width", width)
    .attr("height", height)
    .append("g")
    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");
		
var pie = d3.layout.pie().value(function(d){return d.Frequency;});

// Declare an arc generator function
var arc = d3.svg.arc().outerRadius(radius);

// Select paths, use arc generator to draw
var arcs = svg.selectAll("g.slice")
		.data(pie)
		.enter()
		.append("g")
		.attr("class", "slice");
arcs.append("path")
    .attr("fill", function(d, i){return color[i];})
    .attr("d", function (d) {return arc(d);});
		
// Add text
arcs.append("text")
    .attr("transform", function(d){
        d.innerRadius = 100; /* Distance of label to the center*/
        d.outerRadius = r;
        return "translate(" + arc.centroid(d) + ")";}
    )
    .attr("text-anchor", "middle")
    .text( function(d) {return d.Frequency;});


	
