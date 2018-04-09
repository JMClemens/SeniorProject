d3.csv("../assets/data/grf.csv", function (error,data) {

  function tabulate(data, columns) {
		var table = d3.select('#requests-table')
				.append('table')
				.attr('class','table');
		var thead = table.append('thead')
				.attr('class','text-primary');
		var tbody = table.append('tbody');

		// sort our data values to appear descending
		data.sort(function(a,b) {
       return b.Frequency - a.Frequency
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
	tabulate(data, ['Request', 'Frequency']); // 2 column table

});