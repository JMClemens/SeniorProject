// Define the height/width of our svg and its margins
var countryMargin = { top: 20, right: 10, bottom: 120, left: 40},
    cwidth = 500 - countryMargin.right - countryMargin.left,
    cheight = 400 - countryMargin.top - countryMargin.bottom;

// Define svg    
var countryChart = d3.select("#g-country-frequency")
    .append("svg")
      .attr ({
        "width": cwidth + countryMargin.right + countryMargin.left,
        "cheight": cheight + countryMargin.top + countryMargin.bottom,
      })
		.style("padding","10px")
    .append("g")
      .attr("transform","translate(" + countryMargin.left + "," + countryMargin.right + ")");
	
// Import Glastopf country frequency CSV file    
d3.csv("../assets/data/gTop10C.csv", function(error, data) {
    
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
    
		// Define x and y scales
		var xScale = d3.scale.ordinal()
				.rangeRoundBands([0,cwidth], 0.2, 0.2);

		var yScale = d3.scale.linear()
				.rangeRound([cheight,0]);

		// Define axis
		var xAxis = d3.svg.axis()
				.scale(xScale)
				.orient("bottom");
		
		var yAxis = d3.svg.axis();
		
    // specify domains of x and y scales
    xScale.domain(data.map(function(d) { return d.Country }) );
    yScale.domain([0,d3.max(data, function(d) { return d.Frequency; } )] );
    var yDomain = yScale.domain(); 
		
		yAxis.scale(yScale)
				.orient("left")
				.ticks( Math.min(10, (yDomain[1] - yDomain[0]) ) );
    		
    // draw bars
    countryChart.selectAll('rect')
      .data(data)
      .enter()
      .append('rect')
      // next four lines are for cool loaded animation
      // start at zero, and make each rect go to their full height over 2s
      .attr("height", 0)
      .attr("y",cheight)
      .transition().duration(2000)
      .delay(function(d,i) { return i * 150;})
      .attr ({
        "x": function(d) { return xScale(d.Country); },
        "y": function(d) { return yScale(d.Frequency); },
        "width": xScale.rangeBand(),
        "height": function(d) {return cheight - yScale(d.Frequency);}
      })
      // Can use this notation below to fill a different color for each graph
      .style("fill", function(d,i) { return 'rgb(20, 20, ' + ((i * 30) + 100) + ')'});
     
      // label the bars
      countryChart.selectAll('text')
        .data(data)
        .enter()
        .append('text')
        .text(function(d) { return d.Frequency; })
        .attr('x', function(d) { return xScale(d.Country) + xScale.rangeBand()/2;})
        .attr('y', function(d) { return yScale(d.Frequency);})
        .style("fill", "black")
        .style("text-anchor", "middle");
      			
			
      // draw x axis
      countryChart.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + cheight + ")")
        .call(xAxis)
        .selectAll('text')
        .attr("transform", "rotate(-60)")
        .attr("dx","-.8em")
        .attr("dy",".25em")
        .style("text-anchor","end")
        .style("font-size","12px");
      
			
      // draw y axis
      countryChart.append("g")
        .attr("class","y axis")
        .call(yAxis)
        .style("font-size","12px");
									
});