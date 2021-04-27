$(document).ready(function() {

    // create the curated xhr request
    var curated_xmlHttp = new XMLHttpRequest();
    curated_xmlHttp.onreadystatechange = function() { 
        // whenever the request state changes, check if the data is ready
        if (curated_xmlHttp.readyState == 4 && curated_xmlHttp.status == 200)
            // handle data from request
            curated_cb(curated_xmlHttp.responseText);
      }
    // create the gainers xhr request
    var gainers_xmlHttp = new XMLHttpRequest();
    gainers_xmlHttp.onreadystatechange = function() { 
        // whenever the request state changes, check if the data is ready
        if (gainers_xmlHttp.readyState == 4 && gainers_xmlHttp.status == 200)
            // handle data from request
            gainers_cb(gainers_xmlHttp.responseText);
      }
    // create the losers xhr request
    var losers_xmlHttp = new XMLHttpRequest();
    losers_xmlHttp.onreadystatechange = function() { 
        // whenever the request state changes, check if the data is ready
        if (losers_xmlHttp.readyState == 4 && losers_xmlHttp.status == 200)
            // handle data from request
            losers_cb(losers_xmlHttp.responseText);
      }
	// create the active xhr request
    var active_xmlHttp = new XMLHttpRequest();
    active_xmlHttp.onreadystatechange = function() { 
        // whenever the request state changes, check if the data is ready
        if (active_xmlHttp.readyState == 4 && active_xmlHttp.status == 200)
            // handle data from request
            active_cb(active_xmlHttp.responseText);
      }
	  
    // request curated
    curated_xmlHttp.open("GET", "/curated_tickers", true); // true for asynchronous 
    curated_xmlHttp.send(null);
    // request active
    active_xmlHttp.open("GET", "/active_tickers", true); // true for asynchronous 
    active_xmlHttp.send(null);
    // request gainers
    gainers_xmlHttp.open("GET", "/top_tickers", true); // true for asynchronous 
    gainers_xmlHttp.send(null);
    // request losers
    losers_xmlHttp.open("GET", "/bottom_tickers", true); // true for asynchronous 
    losers_xmlHttp.send(null);

});

function curated_cb(data){
    curated_tickers = JSON.parse(data); // parse to array

    // get table
    var table = document.getElementById("curated_stocks");
    var name_base = '<a href="/results/' // start with this
    var name_mid = '">'// append ticker, then append this
    var name_end = '</a>' // append ticker, then append this
    // for each element, add an entry to the table
    for(let i = 0; i < curated_tickers.length; i++){
        // add new row to table
        var row = table.insertRow()
        // add cells to row
        var cell_ticker = row.insertCell(0)
        var cell_price = row.insertCell(1)
        
        // set ticker to results hyperlink
        // will look like  <a href="/results/TICKER">TICKER</a>
        // to extract ticker name, innerHTML.split(">")[1].split("<")[0]
        cell_ticker.innerHTML = name_base + curated_tickers[i] + name_mid + curated_tickers[i] + name_end
        cell_price.innerHTML = "--"
    }
    fill_in_prices("curated_stocks")        

  }

  function gainers_cb(data){
    gainers_tickers = JSON.parse(data); // parse to array

    // get table
    var table = document.getElementById("gainer_stocks");
    var name_base = '<a href="/results/' // start with this
    var name_mid = '">'// append ticker, then append this
    var name_end = '</a>' // append ticker, then append this
    // for each element, add an entry to the table
    for(let i = 0; i < gainers_tickers.length; i++){
        // add new row to table
        var row = table.insertRow()
        // add cells to row
        var cell_ticker = row.insertCell(0)
        var cell_price = row.insertCell(1)
        
        // set ticker to results hyperlink
        // will look like  <a href="/results/TICKER">TICKER</a>
        // to extract ticker name, innerHTML.split(">")[1].split("<")[0]
        cell_ticker.innerHTML = name_base + gainers_tickers[i] + name_mid + gainers_tickers[i] + name_end
        cell_price.innerHTML = "--"
    }
    fill_in_prices("gainer_stocks")

  }


function losers_cb(data){
    losers_tickers = JSON.parse(data); // parse to array

    // get table
    var table = document.getElementById("loser_stocks");
    var name_base = '<a href="/results/' // start with this
    var name_mid = '">'// append ticker, then append this
    var name_end = '</a>' // append ticker, then append this
    // for each element, add an entry to the table
    for(let i = 0; i < losers_tickers.length; i++){
        // add new row to table
        var row = table.insertRow()
        // add cells to row
        var cell_ticker = row.insertCell(0)
        var cell_price = row.insertCell(1)
        
        // set ticker to results hyperlink
        // will look like  <a href="/results/TICKER">TICKER</a>
        // to extract ticker name, innerHTML.split(">")[1].split("<")[0]
        cell_ticker.innerHTML = name_base + losers_tickers[i] + name_mid + losers_tickers[i] + name_end
        cell_price.innerHTML = "--"
    }
    fill_in_prices("loser_stocks")

  }
  
function active_cb(data){
    active_tickers = JSON.parse(data); // parse to array

    // get table
    var table = document.getElementById("active_stocks");
    var name_base = '<a href="/results/' // start with this
    var name_mid = '">'// append ticker, then append this
    var name_end = '</a>' // append ticker, then append this
    // for each element, add an entry to the table
    for(let i = 0; i < active_tickers.length; i++){
        // add new row to table
        var row = table.insertRow()
        // add cells to row
        var cell_ticker = row.insertCell(0)
        var cell_price = row.insertCell(1)
        
        // set ticker to results hyperlink
        // will look like  <a href="/results/TICKER">TICKER</a>
        // to extract ticker name, innerHTML.split(">")[1].split("<")[0]
        cell_ticker.innerHTML = name_base + active_tickers[i] + name_mid + active_tickers[i] + name_end
        cell_price.innerHTML = "--"
    }
    fill_in_prices("active_stocks")

  }

function fill_in_prices(table_id){
    // get table
    var table = document.getElementById(table_id);

    // start at row 2 (row 1 is "Ticker")
    // get ticker name
    // request price data
    // fill in price data on callback, pass callback cell to insert to
    var xhr_reqs = [];
    for (var i = 1; i < table.rows.length; i++){
        (function(i){
            var ticker_name = table.rows[i].cells[0].innerHTML
            var ticker_name = ticker_name.split(">")[1].split("<")[0] // retrieve only ticker
            var ticker_price_cell = table.rows[i].cells[1] // going to tell callback put price here

            // get price
            console.log("new req " + i + " " + table_id)
            xhr_reqs[i] = new XMLHttpRequest();
            xhr_reqs[i].onreadystatechange = function() { 
                // whenever the request state changes, check if the data is ready
                if (xhr_reqs[i].readyState == 4 && xhr_reqs[i].status == 200)
                    // handle data from request
                    insert_price(xhr_reqs[i].responseText, ticker_price_cell);
            }
            // request the portfolio then wait for the response with portfolio_cb
            xhr_reqs[i].open("GET", "/api/ticker_price_change/" + ticker_name, true); // true for asynchronous 
            xhr_reqs[i].send(null);
        })(i);
    }
}

function insert_price(response_data, cell){
    var price = JSON.parse(response_data)
    console.log("inserting " + price)
    var color = "lightgreen";
    // if price is negative, make positive and set color to red
    if(price < 0){
        price = price * -1;
        color = "red";   
    }
    cell.innerHTML = price;
    cell.style.color = color;
<<<<<<< Updated upstream
=======
}

function get_graph_data(data) {

    dataParsed = JSON.parse(data);
    console.log("Data parsed:");
    console.log(dataParsed);

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

      console.log("Prices: ");
      console.log(pricesFormatted);
      console.log("Dates: ");
      console.log(datesFormatted);
	
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
>>>>>>> Stashed changes
}