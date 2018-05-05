var klrmargin = { top: 10, right: 10, bottom: 40, left: 70},
    w = 280 - klrmargin.right - klrmargin.left,
    h = 280 - klrmargin.top - klrmargin.bottom,
		r = Math.min(w, h) * 1.2;

var color = d3.scale.ordinal()
    .range(["#4BB543", "#FF0000"]);

var arc = d3.svg.arc()
    .outerRadius(r - 10)
    .innerRadius(0);

var pie = d3.layout.pie()
    .sort(null)
    .value(function (d) {
    return d.NumLogins;
});


d3.csv("../assets/data/kloginratio.csv", function(error, data) {

  data.forEach(function(d) {
		LoginStatus = d.LoginStatus,
		NumLogins = +d.NumLogins
  });

	
	var successLine = Object.entries(data)[0];
	var failLine = Object.entries(data)[1];	
	var successTotal = parseFloat(successLine[1]["NumLogins"]);
	var failTotal = parseFloat(failLine[1]["NumLogins"]);
	var totalLogins = successTotal + failTotal;
	var successPrcnt = parseFloat(((successTotal / (totalLogins))*100).toFixed(2));
	console.log(successPrcnt);
	var failPrcnt = parseFloat(((failTotal / (totalLogins))*100).toFixed(2));
	console.log(failPrcnt);

var totalText = d3.select("#k-login-chart").append("h4")
			.html("Total successful logins: " + successTotal + " - " + successPrcnt + "% of total attempts."
			+ "<br />" +"Total failed logins: " + failTotal + " - " + failPrcnt + "% of total attempts.")
			.style("margin", "10px 0 0 50px");
	
var mysvg = d3.select("#k-login-chart").append("svg")
    .attr("width", w)
    .attr("height", h)
    .append("g")
    .attr("transform", "translate(" + (r+klrmargin.left) + "," + (r+klrmargin.top) + ")");

    var gl = mysvg.selectAll(".arc")
        .data(pie(data))
        .enter().append("g")
        .attr("class", "arc");

    gl.append("path")
        .attr("d", arc)
        .style("fill", function (d) {
        return color(d.data.LoginStatus);
    });

    gl.append("text")
        .attr("transform", function (d) {
        return "translate(" + arc.centroid(d) + ")";
    })
        .attr("dy", ".35em")
        .style("text-anchor", "middle")
				.attr("fontSize","24px")
        .text(function (d) {
        return d.data.LoginStatus;
    });		
});