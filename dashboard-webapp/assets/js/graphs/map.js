var width = 960;
var height = 500;

// set projection
var projection = d3.geo.mercator();

// create path variable
var path = d3.geo.path()
    .projection(projection);


d3.json("https://unpkg.com/world-atlas@1/world/110m.json", function(error, topo) { console.log(topo);

  	countries = topojson.feature(topo, topo.objects.countries).features

  	// set projection parameters
  	projection
      .scale(width / 2 / Math.PI)
      .translate([(width / 2)-30, (height / 2)+50])

    // create svg variable
    var svg = d3.select("#worldmap").append("svg")
    				.attr("width", width)
    				.attr("height", height);
    
    svg.append("rect")
      .attr("width", "100%")
      .attr("height","100%")
      .attr("fill","#A2E8E8");

    // points
    aa = [-122.490402, 37.786453];
    bb = [-122.389809, 37.72728];

	console.log(projection(aa),projection(bb));

	// add states from topojson
	svg.selectAll("path")
      .data(countries).enter()
      .append("path")
      .attr("class", "feature")
      .style("fill", "#71945A")
      .attr("d", path);

    // put boarder around countries 
  	svg.append("path")
      .datum(topojson.mesh(topo, topo.objects.countries, function(a, b) { return a !== b; }))
      .attr("class", "mesh")
      .attr("d", path);

    // add circles to svg
    svg.selectAll("circle")
		.data([aa,bb]).enter()
		.append("circle")
		.attr("cx", function (d) { console.log(projection(d)); return projection(d)[0]; })
		.attr("cy", function (d) { return projection(d)[1]; })
		.attr("r", "8px")
		.attr("fill", "red")

});