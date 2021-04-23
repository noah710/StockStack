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
        var cell_amount = row.insertCell(2)
        var cell_date = row.insertCell(3)
        var cell_remove = row.insertCell(4)
        // set cells to data
        cell_ticker.innerHTML = portfolio_data[i].ticker
        cell_buy_price.innerHTML = portfolio_data[i].price
        cell_amount.innerHTML = portfolio_data[i].amount
        cell_date.innerHTML = portfolio_data[i].date
        cell_remove.innerHTML = link_base + portfolio_data[i].ticker + link_mid + 'REMOVE' + link_end
    }
        

  }
  
  