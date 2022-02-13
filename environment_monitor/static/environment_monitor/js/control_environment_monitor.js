iotMsSocket.onmessage = function(e) {
   const data = JSON.parse(e.data);
   console.log(data)
   message=JSON.parse(data.message)[0]
   // Commands
   if(message.hasOwnProperty("command_response")){
      if(message["command_response"].indexOf("Error")!=-1){
         show_notification("failure", message["command_response"]);
      }
      else{
         show_notification("success", message["command_response"]);
      }
   }
};

/****** Command functions *****/
$("#btn_query").click(function() {
   iotMsSocket.send(JSON.stringify({
       'message': {
           'command':'query_device'
        }
   }));
});


$("#btn_freq").click(function() {
   frequency=$("#freq_env").val();
   iotMsSocket.send(JSON.stringify({
       'message': {
           'command':'set_frequency',
           'freq':frequency,
        }
   }));
});

/***************** Load device data ************************/
data = $.ajax({
    type:"POST",
    url: "/home/get_device_data/",
    dataType:"json",
    async: true,
    success: function(data){
      device=JSON.parse(data)[0]
      $("#freq_env").val(device["fields"]["sent_frequency"]);
    }
}).responseText;


$('#monitor_ambiente').css("font-weight","bold");
$('#mon_amb_control').css("font-weight","bold");