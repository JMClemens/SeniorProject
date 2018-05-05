// Define the height/width of our svg and its margins
var kdmargin = { top: 30, right: 10, bottom: 40, left: 40},
    kdwidth = 500 - kdmargin.right - kdmargin.left,
    kdheight = 400 - kdmargin.top - kdmargin.bottom;

// Define svg    
var durationGraph = d3.select("#k-duration-graph")
    .append("svg")
      .attr ({
        "width": kdwidth + kdmargin.right + kdmargin.left,
        "height": kdheight + kdmargin.top + kdmargin.bottom
      })
    .append("g")
      .attr("transform","translate(" + kdmargin.left + "," + kdmargin.top + ")");

// Define x and y scales
var xDScale = d3.scale.ordinal()
    .rangeBands([0,kdwidth], 0.2, 0.2);

var yDScale = d3.scale.linear()
    .rangeRound([kdheight,0]);

// Define axis
var xDAxis = d3.svg.axis()
    .scale(xDScale)
    .orient("bottom");
    
var yDAxis = d3.svg.axis();

// Import Glastopf country frequency CSV file    
d3.csv("../assets/data/kdur.csv", function(error, data) {
    
    if(error) console.log("Error: data not loaded");
    
    data.forEach(function(d) {      
      // + symbol convert from string representation of a number to an actual number
      d.Sessions = +d.Sessions;
      d.Duration = d.Duration;
    });
        
    // specify domains of x and y scales
    xDScale.domain(data.map(function(d) { return d.Duration }) );
    yDScale.domain([0,d3.max(data, function(d) { return d.Sessions; } )] );
    var yDDomain = yDScale.domain(); 
    yDAxis.scale(yDScale)
    .orient("left")
		.ticks( Math.min(10, (yDDomain[1] - yDDomain[0]) ) );
    
    // draw bars
    durationGraph.selectAll('rect')
      .data(data)
      .enter()
      .append('rect')
      // next four lines are for cool loaded animation
      // start at zero, and make each rect go to their full height over 2s
      .attr("height", 0)
      .attr("y",kdheight)
      .transition().duration(2000)
      .delay(function(d,i) { return i * 150;})
      .attr ({
        "x": function(d) { return xDScale(d.Duration); },
        "y": function(d) { return yDScale(d.Sessions); },
        "width": xDScale.rangeBand(),
        "height": function(d) {return kdheight - yDScale(d.Sessions);}
      })
      // Can use this notation below to fill a different color for each graph
      .style("fill", function(d,i) { return 'rgb(20, 20, ' + ((i * 30) + 100) + ')'});
      
      // label the bars
      durationGraph.selectAll('text')
        .data(data)
        .enter()
        .append('text')
        .text(function(d) { return d.Sessions; })
        .attr('x', function(d) { return xDScale(d.Duration) + xDScale.rangeBand()/2;})
        .attr('y', function(d) { return yDScale(d.Sessions);})
        .style("fill", "black")
        .style("text-anchor", "middle");
      
      // draw x axis
      durationGraph.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + kdheight + ")")
        .call(xDAxis)
        .selectAll('text')
        .attr("transform", "rotate(-60)")
        .attr("dx","-.8em")
        .attr("dy",".25em")
        .style("text-anchor","end")
        .style("font-size","12px");
      
      // draw y axis
      durationGraph.append("g")
        .attr("class","y axis")
        .call(yDAxis)
        .style("font-size","12px");
});