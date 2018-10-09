
var ros = new ROSLIB.Ros({
    url : 'ws://localhost:9090'
});

ros.on('connection', function() {
    console.log('Connected to websocket server.');
});

var record_pub = new ROSLIB.Topic({
    ros : ros,
    name : '/wake_word_recording',
    messageType : 'std_msgs/Bool'
});

$("#start_recording").click(function() {
    console.log("START");
    $("#is_training").show();
    record_pub.publish(new ROSLIB.Message({data: true}));
});
  
$("#stop_recording").click(function() {
    console.log("STOP");
    $("#is_training").hide();
    record_pub.publish(new ROSLIB.Message({data: false}));
});
  