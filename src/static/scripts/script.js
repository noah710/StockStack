


$(document).ready(function() {

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
