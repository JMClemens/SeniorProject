d3.csv("data/test.csv", function(data) {
    for (var i = 0; i < data.length; i++) {
        console.log(data[i].dur);
    }
}); 