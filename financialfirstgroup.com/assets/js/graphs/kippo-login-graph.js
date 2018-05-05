// Define the height/width of our svg and its margins
var klmargin = { top: 30, right: 10, bottom: 40, left: 40},
    klwidth = 500 - klmargin.right - klmargin.left,
    klheight = 400 - klmargin.top - klmargin.bottom;

// Define svg    
var loginGraph = d3.select("#k-login-graph")
    .append("svg")
      .attr ({
        "width": klwidth + klmargin.right + klmargin.left,
        "height": klheight + klmargin.top + klmargin.bottom
      })
    .append("g")
      .attr("transform","translate(" + klmargin.left + "," + klmargin.top + ")");

// Define x and y scales
var xLScale = d3.scale.ordinal()
    .rangeBands([0,klwidth], 0.2, 0.2);

var yLScale = d3.scale.linear()
    .rangeRound([klheight,0]);

// Define axis
var xLAxis = d3.svg.axis()
    .scale(xLScale)
    .orient("bottom");
    
var yLAxis = d3.svg.axis();

// Import Glastopf country frequency CSV file    
d3.csv("../assets/data/kTop10Login.csv", function(error, data) {
    
    if(error) console.log("Error: data not loaded");
    
    data.forEach(function(d) {      
      // + symbol convert from string representation of a number to an actual number
      d.Frequency = +d.Frequency;
      d.Login = d.Login;
    });
    
    // sort the frequency values
    data.sort(function(a,b) {
       return b.Frequency - a.Frequency
    });
    
    // specify domains of x and y scales
    xLScale.domain(data.map(function(d) { return d.Login }) );
    yLScale.domain([0,d3.max(data, function(d) { return d.Frequency; } )] );
    var yLDomain = yLScale.domain(); 
    yLAxis.scale(yLScale)
    .orient("left")
		.ticks( Math.min(10, (yLDomain[1] - yLDomain[0]) ) );
    
    // draw bars
    loginGraph.selectAll('rect')
      .data(data)
      .enter()
      .append('rect')
      // next four lines are for cool loaded animation
      // start at zero, and make each rect go to their full height over 2s
      .attr("height", 0)
      .attr("y",klheight)
      .transition().duration(2000)
      .delay(function(d,i) { return i * 150;})
      .attr ({
        "x": function(d) { return xLScale(d.Login); },
        "y": function(d) { return yLScale(d.Frequency); },
        "width": xLScale.rangeBand(),
        "height": function(d) {return klheight - yLScale(d.Frequency);}
      })
      // Can use this notation below to fill a different color for each graph
      .style("fill", function(d,i) { return 'rgb(20, 20, ' + ((i * 30) + 100) + ')'});
      
      // label the bars
      loginGraph.selectAll('text')
        .data(data)
        .enter()
        .append('text')
        .text(function(d) { return d.Frequency; })
        .attr('x', function(d) { return xLScale(d.Login) + xLScale.rangeBand()/2;})
        .attr('y', function(d) { return yLScale(d.Frequency);})
        .style("fill", "black")
        .style("text-anchor", "middle");
      
      // draw x axis
      loginGraph.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + klheight + ")")
        .call(xLAxis)
        .selectAll('text')
        .attr("transform", "rotate(-60)")
        .attr("dx","-.8em")
        .attr("dy",".25em")
        .style("text-anchor","end")
        .style("font-size","12px");
      
      // draw y axis
      loginGraph.append("g")
        .attr("class","y axis")
        .call(yLAxis)
        .style("font-size","12px");
});