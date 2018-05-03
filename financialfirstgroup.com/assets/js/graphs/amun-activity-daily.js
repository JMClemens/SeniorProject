// Define the height/width of our svg and its margins
var wdamargin = { top: 20, right: 10, bottom: 10, left: 40},
    wdawidth = 400 - wdamargin.right - wdamargin.left,
    wdaheight = 300 - wdamargin.top - wdamargin.bottom;

var parseDate = d3.time.format("%Y-%m-%d").parse;

var x = d3.time.scale().range([0, wdawidth]);
var y = d3.scale.linear().range([wdaheight, 0]);

// Define the axes
var xAxis = d3.svg.axis().scale(x)
    .orient("bottom").ticks(5);

var yAxis = d3.svg.axis().scale(y)
    .orient("left").ticks(5);

var valueline = d3.svg.line()
    .x(function(d) { return x(d.DateStamp); })
    .y(function(d) { return y(d.NumHits); });

// Adds the svg canvas
var amunDaily = d3.select("#w-daily-activity")
    .append("svg")
        .attr("width", wdawidth + wdamargin.left + wdamargin.right)
        .attr("height", wdaheight + wdamargin.top + wdamargin.bottom)
    .append("g")
        .attr("transform", 
              "translate(" + wdamargin.left + "," + wdamargin.top + ")");    
    
d3.csv("../assets/data/adailyhits.csv", function(error, data) {
  if (error) throw error;
  data.forEach(function(d) {
      d.DateStamp = parseDate(d.DateStamp);
      d.NumHits = +d.NumHits;
  });

    x.domain(d3.extent(data, function(d) { return d.DateStamp; }));
    y.domain([0, d3.max(data, function(d) { return d.NumHits; })]);

    // Add the valueline path.
    amunDaily.append("path")
        .attr("class", "line")
        .attr("d", valueline(data));
        
  // add circles to svg
  amunDaily.selectAll("a-points")
  .data(data).enter()
  .append("circle")
  .attr("r", 2)
  .attr('cx', function(d) { return x(d.DateStamp) ;})
  .attr('cy', function(d) { return y(d.NumHits) ;})
  .attr("fill", "black");
  
    // Add the X Axis
    amunDaily.append("g")
        .attr("class", "x axis")
        
        // TO DO:
        // Height wasnt working properly below. Using 270 for now. Make accessor to height to get proper value later
        .attr("transform", "translate(0," + 270 + ")")
        .call(xAxis);

    // Add the Y Axis
    amunDaily.append("g")
        .attr("class", "y axis")
        .call(yAxis);
});
var wdainter = setInterval(function() {
                wdaupdateData();
					// Redraw the graph every two minutes
        }, 120000); 

function wdaupdateData() {

	d3.select("#w-daily-activity").selectAll("*").remove();

	// Define the height/width of our svg and its margins
	var wdamargin = { top: 20, right: 10, bottom: 10, left: 40},
			wdawidth = 400 - wdamargin.right - wdamargin.left,
			wdaheight = 300 - wdamargin.top - wdamargin.bottom;

	var parseDate = d3.time.format("%Y-%m-%d").parse;

	var x = d3.time.scale().range([0, wdawidth]);
	var y = d3.scale.linear().range([wdaheight, 0]);

	// Define the axes
	var xAxis = d3.svg.axis().scale(x)
			.orient("bottom").ticks(5);

	var yAxis = d3.svg.axis().scale(y)
			.orient("left").ticks(5);

	var valueline = d3.svg.line()
			.x(function(d) { return x(d.DateStamp); })
			.y(function(d) { return y(d.NumHits); });

	// Adds the svg canvas
	var amunDaily = d3.select("#w-daily-activity")
			.append("svg")
					.attr("width", wdawidth + wdamargin.left + wdamargin.right)
					.attr("height", wdaheight + wdamargin.top + wdamargin.bottom)
			.append("g")
					.attr("transform", 
								"translate(" + wdamargin.left + "," + wdamargin.top + ")");  
	
	d3.csv("../assets/data/adailyhits.csv", function(error, data) {
  if (error) throw error;
  data.forEach(function(d) {
      d.DateStamp = parseDate(d.DateStamp);
      d.NumHits = +d.NumHits;
  });

    x.domain(d3.extent(data, function(d) { return d.DateStamp; }));
    y.domain([0, d3.max(data, function(d) { return d.NumHits; })]);

    // Add the valueline path.
    amunDaily.append("path")
        .attr("class", "line")
        .attr("d", valueline(data));
        
  // add circles to svg
  amunDaily.selectAll("a-points")
  .data(data).enter()
  .append("circle")
  .attr("r", 2)
  .attr('cx', function(d) { return x(d.DateStamp) ;})
  .attr('cy', function(d) { return y(d.NumHits) ;})
  .attr("fill", "black");
  
    // Add the X Axis
    amunDaily.append("g")
        .attr("class", "x axis")
        
        // TO DO:
        // Height wasnt working properly below. Using 270 for now. Make accessor to height to get proper value later
        .attr("transform", "translate(0," + 270 + ")")
        .call(xAxis);

    // Add the Y Axis
    amunDaily.append("g")
        .attr("class", "y axis")
        .call(yAxis);
	});
}