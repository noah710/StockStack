$(document).ready(function() {
    var chart_xmlHttp = new XMLHttpRequest();
    chart_xmlHttp.onreadystatechange = function() {
        // whenever the request state changes, check if the data is ready
        if (chart_xmlHttp.readyState == 4 && chart_xmlHttp.status == 200)
            // handle data from request
            get_results_data(chart_xmlHttp.responseText);
    }

	var info_xmlHttp = new XMLHttpRequest();
	info_xmlHttp.onreadystatechange = function() {
        // whenever the request state changes, check if the data is ready
        if (info_xmlHttp.readyState == 4 && info_xmlHttp.status == 200)
            // handle data from request
            get_results_info(info_xmlHttp.responseText);
    }

    chart_xmlHttp.open("GET", "/results_page_data", true);
    chart_xmlHttp.send(null);

	info_xmlHttp.open("GET", "/results_page_info", true);
    info_xmlHttp.send(null);
});

function get_results_info(data) {
	dataParsed = JSON.parse(data);

	var symbol = dataParsed.ticker_symbol;
	var name = dataParsed.name;
	var country = dataParsed.country;
	var description = dataParsed.description;

	var ticker = document.getElementById("symbol");
    ticker.innerHTML = symbol;

	var company_name = document.getElementById("company_name");
	company_name.innerHTML = name;

	var company_country = document.getElementById("country");
	company_country.innerHTML = country;

	var company_desc = document.getElementById("description");
	company_desc.innerHTML = description;
}

function get_results_data(data) {
    
	dataParsed = JSON.parse(data);

    google.charts.load('current', {'packages':['corechart', 'line']});
	google.charts.setOnLoadCallback(drawChart(dataParsed));
	
	function drawChart(data) {

        const datesFormatted = new Array();
        const pricesFormatted = new Array();

        for (var i = 0; i < data.length; i++) {
            var price = data[i].price;
            var priceFormat = parseFloat(price);
            pricesFormatted.push(priceFormat);

            var date = data[i].date;
            var dateSplit = date.split("-");

            var year = dateSplit[0];
            var month = dateSplit[1];
            var day = dateSplit[2];

            var dateFormat = new Date(year, month - 1, day);
            datesFormatted.push(dateFormat);
        }
	
	    var data = new google.visualization.DataTable();
	    data.addColumn('date', 'Date');
	    data.addColumn('number', 'Price');
	
	    for (var m = 0; m < datesFormatted.length; m++) {
		    data.addRow([datesFormatted[m], pricesFormatted[m]]);
	    }
	
	    var dataCount = datesFormatted.length;
	
	    var options = {
		    title: 'Asset Performance (Past Month)',
		    animation: {
			    startup: true,
			    duration: 2000,
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
	
		var curPrice = pricesFormatted[pricesFormatted.length - 1];
		document.getElementById("myText").innerHTML = curPrice;
	
		var chart = new google.visualization.LineChart(document.getElementById("result_chart"));
		chart.draw(data, options);
	}
}