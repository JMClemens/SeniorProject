d3.csv("../assets/data/aOtherC.csv", function (error,data) {

  function tabulate(data, columns) {
		var table = d3.select('#a-country-table')
				.append('table')
				.attr('class','table');
		var thead = table.append('thead')
				.attr('class','text-primary');
		var tbody = table.append('tbody');

		data.forEach(function(d) {      
					// + symbol convert from string representation of a number to an actual number
					d.Countries = d.Countries.replace(/[\[\]']+/g, '');
				});
		
		// append the header row
		thead.append('tr')
		  .selectAll('th')
		  .data(columns).enter()
		  .append('th')
		    .text(function (column) { return column; });

		// create a row for each object in the data
		var rows = tbody.selectAll('tr')
		  .data(data)
		  .enter()
		  .append('tr');

		// create a cell in each row for each column
		var cells = rows.selectAll('td')
		  .data(function (row) {
		    return columns.map(function (column) {
		      return {column: column, value: row[column]};
		    });
		  })
		  .enter()
		  .append('td')
		    .text(function (d) { return d.value; });

	  return table;
	}

	// render the table(s)
	tabulate(data, ['Number of Hits', 'Countries']); // 2 column table

});