var socket = io("http://localhost:3000");



socket.on("server-send-result", function(data){
  $("#txtResult").val(JSON.parse(data).result)
});


$(document).ready(function(){
  

  $("#btnCheck").click(function(){
    socket.emit("client-send-Message", [ $("#txtPostMessage").val(), $("#txtTimeStamp").val(), 
    $("#txtNumLike").val(), $("#txtNumComment").val(), $("#txtNumShare").val()]);
  });


});
