$(document).ready(function() {
    
    // create the xhr request
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            draw(xmlHttp.responseText);
    }
    xmlHttp.open("GET", "/spy_ticker", true);
    xmlHttp.send(null);
});

function draw(outer_data) {
    var data = new google.visualization.DataTable();
    data.addColumn('date', 'Date');
    data.addColumn('number', 'Price');

    for (var m = 0; m < datesFormatted.length; m++) {
      data.addRow([datesFormatted[m], pricesFormatted[m]]);
    }

    var dataCount = datesFormatted.length;

    var options = {
      title: 'Asset Performance (Past Month)',
      pointsVisible: true,
      pointSize: 3,
      legend: {position: 'none'},
      hAxis: {
        format: 'MM/d',
        gridlines: {count: 5},
        pointSize: 2,
        //title: 'Date',
        titlePosition: 'none'
      },
      vAxis: {
        title: 'Price'
      }
    };

    var curPrice = pricesFormatted[pricesFormatted.length - 1];
    console.log('CUR PRICE: ' + curPrice);
    document.getElementById("myText").innerHTML = curPrice;

    var chart = new google.visualization.LineChart(document.getElementById("curve_chart"));

    chart.draw(data, options);
}

