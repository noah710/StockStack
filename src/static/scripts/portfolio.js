// used to sum all gains and losses of assets
var total_gainloss = 0.0
var total_value = 0.0

// using this to wait for all values to be in table before calculating total
var num_inserted = 0

$(document).ready(function() {

    // create the xhr request
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
        // whenever the request state changes, check if the data is ready
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            // handle data from request
            portfolio_cb(xmlHttp.responseText);
      }
    // request the portfolio then wait for the response with portfolio_cb
    xmlHttp.open("GET", "/profile/portfolio", true); // true for asynchronous 
    xmlHttp.send(null);

    // create the graph xhr request
    var graph_xmlHttp = new XMLHttpRequest();
    graph_xmlHttp.onreadystatechange = function() {
        // whenever the request state changes, check if the data is ready
        if (graph_xmlHttp.readyState == 4 && graph_xmlHttp.status == 200)
            // handle data from request
            get_networth_graph_data(graph_xmlHttp.responseText);
    }
    graph_xmlHttp.open("GET", "/profile/chart", true);
    graph_xmlHttp.send(null);

  });
  
  function portfolio_cb(data){
    portfolio_data = JSON.parse(data);

    // get table
    var table = document.getElementById("portolio_table");
    // this is for making the remove link
    var link_base = '<a href="/profile/remove_ticker/' // start with this
    var link_mid = '">'// append ticker, then append this
    var link_end = '</a>' // append ticker, then append this
    // for each element, add an entry to the table
    for(let i = 0; i < portfolio_data.length; i++){
        // add new row to table
        var row = table.insertRow()
        // add cells to row
        var cell_ticker = row.insertCell(0)
        var cell_buy_price = row.insertCell(1)
        var cell_current_price = row.insertCell(2)
        var cell_amount = row.insertCell(3)
        var cell_costbasis = row.insertCell(4)
        var cell_total = row.insertCell(5)
        var cell_gainloss = row.insertCell(6)
        var cell_date = row.insertCell(7)
        var cell_remove = row.insertCell(8)
        // set cells to data
        cell_ticker.innerHTML = portfolio_data[i].ticker
        cell_buy_price.innerHTML = portfolio_data[i].price
        cell_amount.innerHTML = portfolio_data[i].amount
        cell_date.innerHTML = portfolio_data[i].date
        cell_costbasis.innerHTML = Math.round((cell_amount.innerHTML * cell_buy_price.innerHTML)*100) / 100 // this basically just rounds it to 2 decimal places
        cell_current_price.innerHTML = '--'
        cell_total.innerHTML = '--' // load this in async
        cell_gainloss.innerHTML = '--' // ^^
        cell_remove.innerHTML = link_base + portfolio_data[i].ticker + link_mid + '<p style="text-align:center; font-size:25px">&#10006;</p>' + link_end
      }
    get_current_values();
        

  }

  // need to async get prices and determine total and gain/loss relative to cost basis
  function get_current_values(){
    // get table
    var table = document.getElementById("portolio_table");

    // start at row 2 (row 1 is "Ticker")
    // get ticker name
    // request price data
    // fill in price data on callback, pass callback cell to insert to
    var xhr_reqs = [];
    for (var i = 1; i < table.rows.length; i++){
        (function(i){
            var ticker_name = table.rows[i].cells[0].innerHTML

            // get price
            xhr_reqs[i] = new XMLHttpRequest();
            xhr_reqs[i].onreadystatechange = function() { 
                // whenever the request state changes, check if the data is ready
                if (xhr_reqs[i].readyState == 4 && xhr_reqs[i].status == 200)
                    // handle data from request
                    insert_price(xhr_reqs[i].responseText, i);
            }
            // request the portfolio then wait for the response with portfolio_cb
            xhr_reqs[i].open("GET", "/api/ticker_price/" + ticker_name, true); // true for asynchronous 
            xhr_reqs[i].send(null);
        })(i);
    }
  }

  function insert_price(response_data, table_row){
    var table = document.getElementById("portolio_table");
    var price = JSON.parse(response_data)
    if(price == 0 && (table_row == (table.rows.length - 1))){
      //console.log("inserting totals from first if!")
      insert_totals()
      return;
    }else if (price == 0){
      return;
    }

    /* cell definitions
    var cell_buy_price = row.insertCell(1)
    var cell_current_price = row.insertCell(2)
    var cell_amount = row.insertCell(3)
    var cell_costbasis = row.insertCell(4)
    var cell_total = row.insertCell(5)
    var cell_gainloss = row.insertCell(6)
    var cell_date = row.insertCell(7)
    var cell_remove = row.insertCell(8)
    */
    // get cells we need to manipulate
    var cost_cell = table.rows[table_row].cells[1]
    var cell_current_price = table.rows[table_row].cells[2]
    var amount_cell = table.rows[table_row].cells[3]
    var total_cell = table.rows[table_row].cells[5] 
    var gainloss_cell = table.rows[table_row].cells[6]

    // set data
    total_cell.innerHTML = Math.round((price * amount_cell.innerHTML)*100) / 100 // this basically just rounds it to 2 decimal places
    cell_current_price.innerHTML = price
    
    var cost_basis = cost_cell.innerHTML * amount_cell.innerHTML
    var gainloss = total_cell.innerHTML - cost_basis 
    //console.log("inserted new price " + table_row)
    
    // keeping track of this for last cell
    total_gainloss = total_gainloss + gainloss
    total_value = total_value + (Math.round((price * amount_cell.innerHTML)*100) / 100)
    
    gainloss_cell.innerHTML = Math.round(gainloss * 100) / 100 // this basically just rounds it to 2 decimal places 
    if (gainloss >= 0){
      gainloss_cell.style.color = '#00cc00' 
    }else{
      gainloss_cell.style.color = 'red'
    }
    
    num_inserted += 1
    // if its the last ticker, insert the total amounts 
    if (num_inserted == (table.rows.length - 1)){
      //console.log("inserting totals from second if! " + table_row)
      insert_totals()
    }
  }

  function insert_totals(){
    var table = document.getElementById("portolio_table");

    var total_row = table.insertRow()
    total_row.insertCell(0)
    total_row.insertCell(1)
    total_row.insertCell(2)
    total_row.insertCell(3)
    total_row.insertCell(4).innerHTML = '<b>Totals</b>'
    var cell_total_val = total_row.insertCell(5)
    var cell_total_gainloss = total_row.insertCell(6)
    total_row.insertCell(7)
    total_row.insertCell(8)
    
    // round values
    cell_total_val.innerHTML = Math.round(total_value * 100) / 100
    cell_total_gainloss.innerHTML = Math.round(total_gainloss * 100) / 100

    if (total_gainloss >= 0){
      cell_total_gainloss.style.color = '#00cc00' 
    }else{
      cell_total_gainloss.style.color = 'red'
    }
  }
  
  
  function get_networth_graph_data(data) {

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
	    data.addColumn('number', 'Price ($)');
	
	    for (var m = 0; m < datesFormatted.length; m++) {
		    data.addRow([datesFormatted[m], pricesFormatted[m]]);
	    }
	
	    var dataCount = datesFormatted.length;
	
	    var options = {
		    title: 'Net Worth (Past Month)',
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
			  title: 'Value'
		  }
		};
	
		//var curPrice = pricesFormatted[pricesFormatted.length - 1];
		//console.log('CUR PRICE: ' + curPrice);
		//document.getElementById("myText").innerHTML = curPrice;
	
		var chart = new google.visualization.LineChart(document.getElementById("networth_chart"));
		chart.draw(data, options);
	}
}
