$("#dashboard").addClass("active");
$("#start").removeClass("active");
$("#devices").removeClass("active");

$.ajax({
    type:"GET",
    url: "/dashboard/get_dashboard_data/",
    dataType:"json",
    async: true,
    success: function(data){
      $("#esp_solar #temp .value").text(data["esp"]["temp"]+" °C");
      $("#esp_solar #humid .value").text(data["esp"]["humid"]+" %");
      $("#atomm5_prototype #temp .value").text(data["m5"]["temp"]+" °C");
      $("#atomm5_prototype #humid .value").text(data["m5"]["humid"]+" %");
      $("#atomm5_prototype #press .value").text(data["m5"]["press"]+" atm");
    }
});