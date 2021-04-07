$(document).ready(function() {

    // create the xhr request
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
        // whenever the request state changes, check if the data is ready
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            // handle data from request
            curated_cb(xmlHttp.responseText);
      }
    // request the portfolio then wait for the response with portfolio_cb
    xmlHttp.open("GET", "/curated_tickers", true); // true for asynchronous 
    xmlHttp.send(null);

});

function curated_cb(data){
    curated_tickers = JSON.parse(data); // parse to array

    // get table
    var table = document.getElementById("curated_stocks");
    // for each element, add an entry to the table
    for(let i = 0; i < curated_tickers.length; i++){
        // add new row to table
        var row = table.insertRow()
        // add cells to row
        var cell_ticker = row.insertCell(0)
        var cell_price = row.insertCell(1)
        
        // set cells to data
        cell_ticker.innerHTML = curated_tickers[i]
        cell_price.innerHTML = -1
    }
    fill_in_prices()
        

  }

function fill_in_prices(){
    // get table
    var table = document.getElementById("curated_stocks");

    // start at row 2 (row 1 is "Ticker")
    // get ticker name
    // request price data
    // fill in price data on callback, pass callback cell to insert to
    var xhr_reqs = [];
    for (var i = 1; i < table.rows.length; i++){
        (function(i){
            var ticker_name = table.rows[i].cells[0].innerHTML
            var ticker_price_cell = table.rows[i].cells[1] // going to tell callback put price here

            // get price
            console.log("new req " + i)
            xhr_reqs[i] = new XMLHttpRequest();
            xhr_reqs[i].onreadystatechange = function() { 
                // whenever the request state changes, check if the data is ready
                if (xhr_reqs[i].readyState == 4 && xhr_reqs[i].status == 200)
                    // handle data from request
                    insert_price(xhr_reqs[i].responseText, ticker_price_cell);
            }
            // request the portfolio then wait for the response with portfolio_cb
            xhr_reqs[i].open("GET", "/api/ticker_price/" + ticker_name, true); // true for asynchronous 
            xhr_reqs[i].send(null);
        })(i);
    }
}

function insert_price(response_data, cell){
    var price = JSON.parse(response_data)
    console.log("inserting " + price)
    cell.innerHTML = price
}