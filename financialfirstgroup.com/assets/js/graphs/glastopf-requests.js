// Define the height/width of our svg and its margins
var margin = { top: 20, right: 10, bottom: 100, left: 40},
    width = 400 - margin.right - margin.left,
    height = 300 - margin.top - margin.bottom;

// Define svg    
var svg = d3.select("#g-country-frequency")
    .append("svg")
      .attr ({
        "width": width + margin.right + margin.left,
        "height": height + margin.top + margin.bottom
      })
    .append("g")
      .attr("transform","translate(" + margin.left + "," + margin.right + ")");

// Define x and y scales
var xScale = d3.scale.ordinal()
    .rangeRoundBands([0,width], 0.2, 0.2);

var yScale = d3.scale.linear()
    .rangeRound([height,0]);

// Define axis
var xAxis = d3.svg.axis()
    .scale(xScale)
    .orient("bottom");
    
var yAxis = d3.svg.axis()
    .scale(yScale)
    .orient("left");

// Import Glastopf country frequency CSV file    
d3.csv("../assets/data/gcf.csv", function(error, data) {
    
    if(error) console.log("Error: data not loaded");
    
    data.forEach(function(d) {      
      // + symbol convert from string representation of a number to an actual number
      d.Frequency = +d.Frequency;
      d.Country = d.Country;
    });
    
    // sort the frequency values
    data.sort(function(a,b) {
       return b.Frequency - a.Frequency
    });
    
    // specify domains of x and y scales
    xScale.domain(data.map(function(d) { return d.Country }) );
    yScale.domain([0,d3.max(data, function(d) { return d.Frequency; } )] );
    
    // draw bars
    svg.selectAll('rect')
      .data(data)
      .enter()
      .append('rect')
      .attr ({
        "x": function(d) { return xScale(d.Country); },
        "y": function(d) { return yScale(d.Frequency); },
        "width": xScale.rangeBand(),
        "height": function(d) {return height - yScale(d.Frequency);}
      })
      // Can use this notation below to fill a different color for each graph
      .style("fill", function(d,i) { return 'rgb(20, 20, ' + ((i * 30) + 100) + ')'});
      
      svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);
      
      svg.append("g")
        .attr("class","y axis")
        .call(yAxis);
});