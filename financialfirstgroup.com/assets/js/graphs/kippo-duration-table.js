d3.text("../assets/data/kdur.csv", function(data) {
                var parsedCSV = d3.csv.parseRows(data);

                var container = d3.select("#k-duration-table")
                    .append("table")
										.attr('class','table')
										.append("tbody")
                    .selectAll("tr")
                        .data(parsedCSV).enter()
                        .append("tr")
                    .selectAll("td")
                        .data(function(d) { return d; }).enter()
                        .append("td")
                        .text(function(d) { return d; })
										 .selectAll("tr:first-child td")
												.attr('class','text-primary')
            });