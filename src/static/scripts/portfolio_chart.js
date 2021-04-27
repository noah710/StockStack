
// Compare //
var compare = false;

// Current ticker //
var curr_ticker;
var total_for_curr_ticker = 0.0;

// array of historic asset value
var assetVal = [];

// global array for user portfolio data //
var globData = [];

$(document).ready(function() {

    // create xhr request
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() {
        // check state
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            // format user data and create chart
            formatUserData(xmlHttp.responseText);
      }
    // retrieve user data from /chart route in profile.py
    xmlHttp.open("GET", "/profile/chart", true);
    xmlHttp.send(null);
});

  // retrieve user historical asset values from profile.py
  function formatUserData(data) {

    // will parse cummulative user portfolio data here
    // and format for drawChart()
    console.log("Heres the data");
    console.log(data);
    // PRINTS AS
    // Heres the data
    // [
    //   {
    //     "amount": "20000.0",
    //     "date": "04/21/2008",
    //     "price": "1e-44",
    //     "ticker": "AMZN"
    //   },
    //   {
    //     "amount": "10.0",
    //     "date": "03.13/2014",
    //     "price": "0.5",
    //     "ticker": "GME"
    //   }
    // ]


    // drawChart with user data
    // drawChart()
  }
  google.charts.load('current', {'packages':['corechart', 'line']});
  google.charts.setOnLoadCallback(drawChart);

  function drawChart() {

  var dataJSON = '{{ data|tojson }}';
  var dataSplit = dataJSON.split(',');

  const dates = new Array();
  const prices = new Array();
  for (var i = 0; i < dataSplit.length; i++) {
    var curData = dataSplit[i];
    var curDataSplit = curData.split(':');

    if (i === 0 || i === (dataSplit.length) - 1) {
  	if (i === 0) {
  	  var firstPart = curDataSplit[0];
  	  var splitFirst = firstPart.split('{');
  	  dates.push(splitFirst[1]);
  	  prices.push(curDataSplit[1]);
  	} else {
  	  var firstPart = curDataSplit[1];
  	  var splitFirst = firstPart.split('}');
  	  dates.push(curDataSplit[0]);
  	  prices.push(splitFirst[0]);
  	}
    } else {
  	dates.push(curDataSplit[0]);
  	prices.push(curDataSplit[1]);
    }
  }

  const datesFormatted = new Array();
  const pricesFormatted = new Array();
  for (var k = 0; k < dates.length; k++) {
    var curDate = dates[k];
    var splitDate = curDate.split('-');
    if (k === 0) {
  	var year = splitDate[0].substring(1, 6);
  	var newDate = new Date(splitDate[0].substring(1, 6), splitDate[1] - 1, splitDate[2].substring(0, 2));
  	datesFormatted.push(newDate);
    } else {
  	var year = splitDate[0].substring(2, 6);
  	var newDate = new Date(splitDate[0].substring(2, 6), splitDate[1] - 1, splitDate[2].substring(0, 2));
  	datesFormatted.push(newDate);
    }
    var priceCur = prices[k];
    var subPrice = priceCur.substring(2, priceCur.length - 1);
    var priceC = (Number(subPrice));
    pricesFormatted.push(priceC);
  }

  var dataJSON = '{{ data|tojson }}';
  console.log(dataJSON);

  var data = new google.visualization.DataTable();
  data.addColumn('date', 'Date');
  data.addColumn('number', 'Price');

  for (var m = 0; m < datesFormatted.length; m++) {
    data.addRow([datesFormatted[m], pricesFormatted[m]]);
  }

  var dataCount = datesFormatted.length;

  var options = {
    title: 'SPDR S&P 500 ETF Trust (Past Month)',
    animation: {
  	startup: true,
  	duration: 1500,
  	easing: 'out',
    },
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

  //var curPrice = pricesFormatted[pricesFormatted.length - 1];
  //console.log('CUR PRICE: ' + curPrice);
  //document.getElementById("myText").innerHTML = curPrice;

  var chart = new google.visualization.LineChart(document.getElementById("curve_chart"));

  chart.draw(data, options);
  }
  console.log("Script");
