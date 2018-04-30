// Define the height/width of our svg and its margins
var margin = { top: 20, right: 10, bottom: 10, left: 40},
    width = 400 - margin.right - margin.left,
    height = 300 - margin.top - margin.bottom;

var parseDate = d3.time.format("%Y-%m-%d").parse;

var x = d3.time.scale().range([0, width]);
var y = d3.scale.linear().range([height, 0]);

// Define the axes
var xAxis = d3.svg.axis().scale(x)
    .orient("bottom").ticks(5);

var yAxis = d3.svg.axis().scale(y)
    .orient("left").ticks(5);

var valueline = d3.svg.line()
    .x(function(d) { return x(d.DateStamp); })
    .y(function(d) { return y(d.NumHits); });

// Adds the svg canvas
var kippoDaily = d3.select("#k-daily-activity")
    .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
    .append("g")
        .attr("transform", 
              "translate(" + margin.left + "," + margin.top + ")");    
    
d3.csv("../assets/data/kdailyhits.csv", function(error, data) {
  if (error) throw error;
  data.forEach(function(d) {
      d.DateStamp = parseDate(d.DateStamp);
      d.NumHits = +d.NumHits;
  });

    x.domain(d3.extent(data, function(d) { return d.DateStamp; }));
    y.domain([0, d3.max(data, function(d) { return d.NumHits; })]);

    // Add the valueline path.
    kippoDaily.append("path")
        .attr("class", "line")
        .attr("d", valueline(data));
        
  // add circles to svg
  kippoDaily.selectAll("circle")
  .data(data).enter()
  .append("circle")
  .attr("r", 2)
  .attr('cx', function(d) { return x(d.DateStamp) ;})
  .attr('cy', function(d) { return y(d.NumHits) ;})
  .attr("fill", "black");
  
    // Add the X Axis
    kippoDaily.append("g")
        .attr("class", "x axis")
        // TO DO:
        // Height wasnt working properly below. Using 270 for now. Make accessor to height to get proper value later
        .attr("transform", "translate(0," + 270 + ")")
        .call(xAxis);

    // Add the Y Axis
    kippoDaily.append("g")
        .attr("class", "y axis")
        .call(yAxis);
  });