$(document).ready(function() {
  
  console.log("starting xhr")
  var xmlHttp = new XMLHttpRequest();
    // document is loaded
    // initialize XML request
    xmlHttp.init = function(){

        if( typeof XMLHttpRequest != 'undefined' ) {

          // initialize xmlhttprequest
            xmlHttp = new XMLHttpRequest();
            xmlHttp.open("GET", "/sendYF/GE", true);
            console.log("XMLHttpRequest created.");
            return true;
        }
        else {
          xmlHttp.open("GET", "/sendYF/GE", true);
        }

    };

    // define xml onreadystatechange
    xmlHttp.onreadystatechange = function() {

    if ( xmlHttp.readyState == 4 && xmlHttp.status == 200 ) xmlHttp.open("GET", "/sendYF/GE", true);
      //xhr_cb(xmlHttp.responseText);
    };

    // define xml send function
    xmlHttp.send = function(){

       if( xmlHttp.init() ) {
           xmlHttp.send(xmlHttp.formData);
           //console.log(xmlHttp.response);
       }
       else {
         xmlHttp.init();
       }
   };

   // define xml onload function (where potential chart construction will be)
   xmlHttp.onload = function() {

     xmlHttp.open("GET", "/sendYF/GE", true);
     var buff = xmlHttp.response
     console.log("data : " + xmlHttp.response);
     //console.log(request.response);
   };
   xmlHttp.init();
   xmlHttp.send();
   console.log("response : " + xmlHttp.response);
   // """""should""""" open our xml response

});
    /*
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
  */
//});

function xhr_cb(data){

  console.log(data);

}
