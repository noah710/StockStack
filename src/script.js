// app script
/////////////

// global array for filter data //
var globData = [];

// const for date objects
const monthNames = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
];





// query run each time the site is loaded / refreshed
$(document).ready(function() {
console.log("ready")
  // pull from Flask route
  $.ajax({
    url:'/sendYF',
    dataType: 'json',
      success: function(data) {
        // set to global array
        globData = data
        console.log("DATA FOUND")

        // test print
        for (let i = 0; i < 10; i++) {
          console.log(data);
        }
      }

    // pull from yf_nasdaq db
    ticker_list = si.tickers_nasdaq()
    console.log("List made")

    // calls in case we want to add variation for home page //
    // Dow si.tickers_dow()
    // S&P500 si.tickers_sp500()
    // Others si.tickers_other()

    // all tickers in currently selected list
    console.log("List : " + ticker_list)

  });
  console.log("got here")
// end DOM function
});

// testing search results
function searchResults(query) {
  return 'query';
}

// Create a MDY Object --> pass in mon/day/yr stringified
// will return according to local time ****
function format_date(date) {
    //
    let month = monthNames[date.getMonth()];
    let day = String(date.getDate()).padStart(2, '0');
    return month + " " + day;
}

// Create a date Object --> pass in date Stringified
// will return according to local time ****
function string_to_date(date) {

    var date_parts = date.split("/");
    // retrieve
    var day = date_parts[0];
    var month = date_parts[1];
    var year = date_parts[2].split(/[ ,]+/)[0];

    var dateObject = new Date(year, month - 1, day);
    // return new date object
    return dateObject;
}
