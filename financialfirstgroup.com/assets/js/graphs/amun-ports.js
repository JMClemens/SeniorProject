// Define the height/width of our svg and its margins
var portmargin = { top: 50, right: 10, pbottom: 20, left: 40},
    portwidth = 500 - portmargin.right - portmargin.left,
    portheight = 300 - portmargin.top - portmargin.pbottom;

// Define svg    
var portChart = d3.select("#portCounts")
    .append("svg")
      .attr ({
        "width": portwidth + portmargin.right + portmargin.left,
        "height": portheight + portmargin.top + portmargin.pbottom,
      })
		.style("padding","10px")
    .append("g")
      .attr("transform","translate(" + portmargin.left + "," + portmargin.right + ")");

// Define x and y scales
var xPScale = d3.scale.ordinal()
    .rangeRoundBands([0,portwidth], 0.2, 0.2);

var yPScale = d3.scale.linear()
    .rangeRound([portheight,0]);

// Define axis
var xPAxis = d3.svg.axis()
    .scale(xPScale)
    .orient("bottom");
    
var yPAxis = d3.svg.axis()
    .scale(yPScale)
    .orient("left");

// Import Amun port frequency CSV file    
d3.csv("../assets/data/apc.csv", function(error, data) {
    
    if(error) console.log("Error: data not loaded");
    
    data.forEach(function(d) {      
      // + symbol convert from string representation of a number to an actual number
      d.Count = +d.Count;
      d.Port = d.Port;
    });
    
    // sort the frequency values
    data.sort(function(a,b) {
       return b.Count - a.Count
    });
    
    // specify domains of x and y scales
    xPScale.domain(data.map(function(d) { return d.Port }) );
    yPScale.domain([0,d3.max(data, function(d) { return d.Count; } )] );
    var yPDomain = yPScale.domain(); 
    yPAxis.ticks( Math.min(10, (yPDomain[1] - yPDomain[0]) ) );
    
    // draw bars
    portChart.selectAll('rect')
      .data(data)
      .enter()
      .append('rect')
      // next four lines are for cool loaded animation
      // start at zero, and make each rect go to their full height over 2s
      .attr("height", 0)
      .attr("y",portheight)
      .transition().duration(2000)
      .delay(function(d,i) { return i * 150;})
      .attr ({
        "x": function(d) { return xPScale(d.Port); },
        "y": function(d) { return yPScale(d.Count); },
        "width": xPScale.rangeBand(),
        "height": function(d) {return portheight - yPScale(d.Count);}
      })
      // Can use this notation below to fill a different color for each graph
      .style("fill", function(d,i) { return 'rgb(20, 20, ' + ((i * 30) + 100) + ')'});
      
      // label the bars
      portChart.selectAll('text')
        .data(data)
        .enter()
        .append('text')
        .text(function(d) { return d.Count; })
        .attr('x', function(d) { return xPScale(d.Port) + xPScale.rangeBand()/2;})
        .attr('y', function(d) { return yPScale(d.Count) - 1;})
        .style("fill", "black")
        .style("text-anchor", "middle");
      
      // draw x axis
      portChart.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + portheight + ")")
        .call(xPAxis)
        .selectAll('text')
        .attr("transform", "rotate(-60)")
        .attr("dx","-.8em")
        .attr("dy",".25em")
        .style("text-anchor","end")
        .style("font-size","12px");
      
      // draw y axis
      portChart.append("g")
        .attr("class","y axis")
        .call(yPAxis)
        .style("font-size","12px");
});