var express = require("express");
var app = express();
app.use(express.static("public"));
app.set("view engine", "ejs");
app.set("views", "./views");

var server = require("http").Server(app);
var io = require("socket.io")(server);
server.listen(3000);

var amqp = require('amqplib/callback_api');

io.on("connection", function(socket){
  console.log("Co nguoi ket noi " + socket.id);

  socket.on("client-send-Message", function(data){
    
    var input = data;
    amqp.connect('amqp://localhost', function(err, conn) {
      conn.createChannel(function(err, ch) {
        var simulations = 'simulations';
        ch.assertQueue(simulations, { durable: false });
        var results = 'results';
        ch.assertQueue(results, { durable: false });
        ch.sendToQueue(simulations, Buffer.from(JSON.stringify(input)));
        ch.consume(
          results,
          function(msg) {
            console.log(msg.content.toString());

            socket.emit("server-send-result", msg.content.toString());
          },
          { noAck: true }
        );
      });
      setTimeout(function() {
        conn.close();
      }, 30000);
    });
    
  });
});

app.get("/", function(req, res){
  res.render("trangchu");
});
