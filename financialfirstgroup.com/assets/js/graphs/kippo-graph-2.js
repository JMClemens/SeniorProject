
var color = "blue";
// Define the height/width of our svg and its margins
var values = d3.range(1000).map(d3.random.normal(20, 5));

// A formatter for counts.
var formatCount = d3.format(",.0f");

var margin = {top: 20, right: 30, bottom: 30, left: 30},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

// Define x and y scales
/*
var max = d3.max(values);
var min = d3.min(values);
var x = d3.scale.linear()
      .domain([min, max])
      .range([0, width]);
      */

// Generate a histogram using twenty uniformly-spaced bins.
var data = d3.layout.histogram()
    .bins(x.ticks(20))
    (values);

var yMax = d3.max(data, function(d){return d.length});
var yMin = d3.min(data, function(d){return d.length});
var colorScale = d3.scale.linear()
            .domain([yMin, yMax])
            .range([d3.rgb(color).brighter(), d3.rgb(color).darker()]);


// Define axis
var xAxis = d3.svg.axis()
    .scale(xScale)
    .orient("bottom");

    // Define svg    
var dvg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    
var y = d3.scale.linear()
    .domain([0, yMax])
    .range([height, 0]);

// Import Glastopf country frequency CSV file    
d3.csv("../assets/data/kdur.csv", function(error, data) {
    
    if(error) console.log("Error: data not loaded");
    

    
    // specify domains of x and y scales
    xScale.domain(data.map(function(d) { return d.Country }) );
    yScale.domain([0,d3.max(data, function(d) { return d.Frequency; } )] );
    var yDomain = yScale.domain(); 
    yAxis.ticks( Math.min(10, (yDomain[1] - yDomain[0]) ) );
    
    // draw bars
    dvg.selectAll('rect')
      .data(data)
      .enter()
      .append('rect')
      // next four lines are for cool loaded animation
      // start at zero, and make each rect go to their full height over 2s
      .attr("height", 0)
      .attr("y",height)
      .transition().duration(2000)
      .delay(function(d,i) { return i * 150;})
      .attr ({
      })
      // Can use this notation below to fill a different color for each graph
      .style("fill", function(d,i) { return 'rgb(20, 20, ' + ((i * 30) + 100) + ')'});
      
      // label the bars
  dvg.selectAll(".bar")
    .data(data)
  .enter().append("g")
    .attr("class", "bar")
    .attr("transform", function(d) { return "translate(" + x(d.x) + "," + y(d.y) + ")"; });

bar.append("rect")
    .attr("x", 1)
    .attr("width", (x(data[0].dx) - x(0)) - 1)
    .attr("height", function(d) { return height - y(d.y); })
    .attr("fill", function(d) { return colorScale(d.y) });

bar.append("text")
    .attr("dy", ".75em")
    .attr("y", -12)
    .attr("x", (x(data[0].dx) - x(0)) / 2)
    .attr("text-anchor", "middle")
    .text(function(d) { return formatCount(d.y); });

dvg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis);
});
