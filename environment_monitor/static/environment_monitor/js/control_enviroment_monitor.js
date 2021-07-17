$("#btn_query").click(function() {
  data = $.ajax({
      url: "/environment_monitor/query_device/",
      dataType:"json",
      async: true,
      success: function(data) {
         if(data.indexOf("Error")!=-1)
            show_notification("success", data);
         else
            show_notification("failure", data);
      }
  }).responseText});
