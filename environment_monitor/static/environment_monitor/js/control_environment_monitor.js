$.ajaxSetup({
  headers: { "X-CSRFToken": Cookies.get('csrftoken') }
});


/***************** Device query ************************/
$("#btn_query").click(function() {
  data = $.ajax({
      type:"POST",
      url: "/environment_monitor/query_device/",
      dataType:"json",
      async: true,
      success: function(data) {
         if(data["response"].indexOf("Error")!=-1)
            show_notification("failure", data["response"]);
         else
            show_notification("success", data["response"]);
      }
  }).responseText});



/***************** Change sent frequency *******************/
$("#btn_freq").click(function() {
   frequency=$("#freq_env").val();
   data = $.ajax({
        type:"POST",
        url: "/environment_monitor/set_sent_frequency/",
        dataType:"json",
        data:{"freq":frequency},
        async: true,
        success: function(data) {
           if(data["response"].indexOf("Error")!=-1)
              show_notification("failure", data["response"]);
           else
              show_notification("success", data["response"]);
        }
 }).responseText});



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
