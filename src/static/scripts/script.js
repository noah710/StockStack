
// ! lets move this out of static so we'll see changes

$(document).ready(function() {

  console.log("starting xhr")
  var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            xhr_cb(xmlHttp.responseText);
    }
    xmlHttp.open("GET", "/sendYF", true); // true for asynchronous 
    xmlHttp.send(null);

console.log("ready")
  // pull from Flask route
  $.ajax({
    url:'/sendYF',
    dataType: 'json',
      success: function(data) {
        // test print
        console.log(data);
        for (let i = 0; i < data.length; i++) {
            
        }
      }
  });
});
// testing search results
function searchResults(query) {
  return 'query';
}


function xhr_cb(data){
  
  console.log(data);

}