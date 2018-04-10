var width = 300,
		height = 300,
		radius = Math.min(width, height) / 2;
		
var dataset = [];

var color = d3.scale.category20();

var svg = d3.select('#pieChart')
	.append('svg')
	.attr('width', width)
	.attr('height', height)
	.append('g')
	.attr('transform', 'translate(' + (width / 2) +
		',' + (height / 2) + ')');
		
var arc = d3.svg.arc()
	.innerRadius(0)
	.outerRadius(radius);

var pie = d3.layout.pie()
	.value(function(d) { return d.count; })
	.sort(null);
	
d3.csv("../assets/data/apc.csv", function(error, data) {

  data.forEach(function(d) {
    dataset.push({
			label: d.Port,
			count: +d.Count
		})
  });
	
	var path = svg.selectAll('path')
	.data(pie(dataset))
	.enter()
	.append('path')
	.attr('d', arc)
	.attr('fill', function(d) {
		return color(d.data.label);
	});
	
});

