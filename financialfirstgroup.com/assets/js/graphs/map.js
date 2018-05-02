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
    if(error2) console.log("Error: HTTP Coord/frequency data not loaded.");
      d3.csv("../assets/data/acf.csv", function(error3, winData) {
			if(error3) console.log("Error: Windows Coord/frequency data not loaded.");	
				d3.csv("../assets/data/kcf.csv", function(error4, kpData) {
				if(error4) console.log("Error: Kippo Coord/frequency data not loaded.");	
				
				countries = topojson.feature(topo, topo.objects.countries).features;
				
				projection
					.scale(width / 2 / Math.PI)
					.translate([(width / 2)-30, (height / 2)+50]);
				
				
				// manipulate our data into a usable format
				data.forEach(function(d) {      
					// + symbol convert from string representation of a number to an actual number
					d.Frequency = +d.Frequency;
					d.Coords = d.Coords.replace(/[\[\]"]+/g, '');
					d.Coords = d.Coords.split(',');
					d.Coords = d.Coords.map(x => parseFloat(x));
					d.Country = d.Country;
				});
				winData.forEach(function(d) {      
					// + symbol convert from string representation of a number to an actual number
					d.Frequency = +d.Frequency;
					d.Coords = d.Coords.replace(/[\[\]"]+/g, '');
					d.Coords = d.Coords.split(',');
					d.Coords = d.Coords.map(x => parseFloat(x));
					d.Country = d.Country;
				});
				kpData.forEach(function(d) {      
					// + symbol convert from string representation of a number to an actual number
					d.Frequency = +d.Frequency;
					d.Coords = d.Coords.replace(/[\[\]"]+/g, '');
					d.Coords = d.Coords.split(',');
					d.Coords = d.Coords.map(x => parseFloat(x));
					d.Country = d.Country;
				});
				
				/*
				TODO:
				These two lines update the # total attacks at the top of the overview page
				They need to be loaded elsewhere later
				*/
				
				var gTotalAttacks = d3.sum(data, function(d) {
					return d.Frequency;
				});

				var aTotalAttacks = d3.sum(winData, function(d) {
					return d.Frequency;
				});

				var kTotalAttacks = d3.sum(kpData, function(d) {
					return d.Frequency;
				});
				
				var total = gTotalAttacks+aTotalAttacks+kTotalAttacks;
				
				var gPercnt = parseFloat(((gTotalAttacks / (total))*100).toFixed(2));
				var aPercnt = parseFloat(((aTotalAttacks / (total))*100).toFixed(2));
				var kPercnt = parseFloat(((kTotalAttacks / (total))*100).toFixed(2));
				
				var glastopfTotalAttackText = d3.select("#glastopf-total-attacks").append("h3")
				.attr("class","title")
				.html(gTotalAttacks + " <small>total</small>");
				
				var glastopfPercntText = d3.select("#glastopf-total-attacks").append("h3")
				.attr("class","title")
				.html(gPercnt + "% <small>of total activity</small>");
				
				var amunTotalAttackText = d3.select("#windows-total-attacks").append("h3")
				.attr("class","title")
				.html(aTotalAttacks + " <small>total</small>");
				
				var amunPercntText = d3.select("#windows-total-attacks").append("h3")
				.attr("class","title")
				.html(aPercnt + "% <small>of total activity</small>");
				
				var kippoTotalAttackText = d3.select("#kippo-total-attacks").append("h3")
				.attr("class","title")
				.html(kTotalAttacks + " <small>total</small>");
				
				var kippoPercntText = d3.select("#kippo-total-attacks").append("h3")
				.attr("class","title")
				.html(kPercnt + "% <small>of total activity</small>");
				
				
				// create svg variable
				var svg = d3.select("#worldmap").append("svg")
								.attr("width", width)
								.attr("height", height);
								/* 
								Zoom Behavior not working as intended
								.call(d3.behavior.zoom().on("zoom", function () {
									svg.attr("transform", "translate(" + d3.event.translate + ")" + " scale(" + d3.event.scale + ")")
								}))
								.append("g");
								*/
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
						.attr("d",path);

					// put border around countries 
					svg.append("path")
						.datum(topojson.mesh(topo, topo.objects.countries, function(a, b) { return a !== b; }))
						.attr("class", "mesh")
						.attr("d", path);
					
					
					freqMax = d3.max(data, function(d) { return d.Frequency; });
					
					var radius = d3.scale.sqrt()
						.domain([0,freqMax])
						.range([0,12]);
				
					var kradius = d3.scale.sqrt()
						.domain([0,freqMax])
						.range([0,9]);

					// add circles to svg
				svg.selectAll("k-circle")
					.data(kpData).enter()
					.append("circle")
					.attr("r", function(d) { return kradius(d.Frequency); })
					.attr("transform", function(d) { 
							return "translate(" + projection([d.Coords[1]-3,d.Coords[0]]) + ")";
						})
					.attr("fill", "yellow")
					.style("opacity",0.8)
					.on("mouseover", function(d) {		
						div.transition()		
								.duration(200)		
								.style("opacity", .85);		
						div	.html(d.Country + "<br />SSH Hits: " + d.Frequency)	
								.style("left", (d3.event.pageX) + "px")		
								.style("top", (d3.event.pageY - 28) + "px");	
					})					
					.on("mouseout", function(d) {		
						div.transition()		
							.duration(500)		
							.style("opacity", 0);	
					 });
					
					
					svg.selectAll("g-circle")
					.data(data).enter()
					.append("circle")
					.attr("r", function(d) { return radius(d.Frequency); })
					.attr("transform", function(d) { 
							return "translate(" + projection([d.Coords[1]-1,d.Coords[0]]) + ")";
						})
					.attr("fill", "red")
					.style("opacity",0.8)
					.on("mouseover", function(d) {		
						div.transition()		
								.duration(200)		
								.style("opacity", .85);		
						div	.html(d.Country + "<br />HTTP Hits: " + d.Frequency)	
								.style("left", (d3.event.pageX) + "px")		
								.style("top", (d3.event.pageY - 28) + "px");	
					})					
					.on("mouseout", function(d) {		
						div.transition()		
							.duration(500)		
							.style("opacity", 0);	
					 });
					 
				svg.selectAll("w-circle")
					.data(winData).enter()
					.append("circle")
					.attr("r", function(d) { return radius(d.Frequency); })
					.attr("transform", function(d) { 
							return "translate(" + projection([d.Coords[1]+2,d.Coords[0]]) + ")";
						})
					.attr("fill", "purple")
					.style("opacity",0.7)
					.on("mouseover", function(d) {		
						div.transition()		
								.duration(200)		
								.style("opacity", .85);		
						div	.html(d.Country + "<br />Windows Hits: " + d.Frequency)	
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
	});
});