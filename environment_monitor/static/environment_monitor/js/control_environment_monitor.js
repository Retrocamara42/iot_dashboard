$.ajaxSetup({
  headers: { "X-CSRFToken": Cookies.get('csrftoken') }
});

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
