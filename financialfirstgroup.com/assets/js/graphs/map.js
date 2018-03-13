var width = 960;
var height = 500;

// set projection
var projection = d3.geo.mercator();

// create path variable
var path = d3.geo.path()
    .projection(projection); 

    // Define the div for the tooltip
var div = d3.select("body").append("div")	
    .attr("class", "tooltip")				
    .style("opacity", 0);

d3.json("https://unpkg.com/world-atlas@1/world/110m.json", function(error1, topo) {
  if(error1) console.log("Error: topo json not loaded.");
  d3.csv("../assets/data/gcf.csv", function(error2, data) {
    if(error2) console.log("Error: Coord/frequency data not loaded.");
      
    countries = topojson.feature(topo, topo.objects.countries).features

    var gCoords = []
    
    data.forEach(function(d) {      
      // + symbol convert from string representation of a number to an actual number
      d.Frequency = +d.Frequency;
      d.Coords = d.Coords.replace(/[\[\]"]+/g, '');
      d.Coords = d.Coords.split(',');
      d.Coords = d.Coords.map(Number);
      d.Country = d.Country;
      console.log("Type of:", d.Coords[0], typeof(d.Coords[0]))
      console.log("d.frequency: ",d.Frequency, ". Type: ", typeof(d.Frequency))
      console.log("d.Coords: ",d.Coords, ". Type: ", typeof(d.Coords))
    });
    
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

    // add countries from topojson
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

      var min = Math.min.apply(Math, data.Frequency);
      var max = Math.max.apply(Math, data.Frequency);
      
      // add circles to svg
      svg.selectAll("circle")
      .data(data).enter()
      .append("circle")
      .attr("r", function(d) {
          return d.Frequency === 1 ? d.Frequency* 10 : d.Frequency / 2
      })
      .attr("transform", function(d) {
							return "translate(" + projection([
							  (d.Coords[0]),
							  (d.Coords[1])
							]) + ")";
						  })
      .attr("fill", "red")
      .on("mouseover", function(d) {		
        div.transition()		
            .duration(200)		
            .style("opacity", .9);		
        div	.html(d.Country)	
            .style("left", (d3.event.pageX) + "px")		
            .style("top", (d3.event.pageY - 28) + "px");	
      })					
      .on("mouseout", function(d) {		
        div.transition()		
          .duration(500)		
          .style("opacity", 0);	
        });	
      
  });
});