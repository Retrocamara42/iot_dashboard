$(document).ready(function() {
    puntos_temp=$('#puntos_temp');
    data = $.ajax({
        url: "/environment_monitor/get_temperature_data/",
        dataType:"json",
        async: true,
        data:"{puntos_temp:"+puntos_temp+"}",
        success: function (data) {
           drawChart(data, '#temperature', 'temperature', 'temperature',
                    '#456990', '#456990', '°C');
        }
    }).responseText});


$(document).ready(function() {
  puntos_humid=$('#puntos_humid');
  data = $.ajax({
      url: "/environment_monitor/get_humidity_data/",
      dataType:"json",
      async: true,
      data:"{puntos_humid:"+puntos_humid+"}",
      success: function (data) {
         drawChart(data, '#humidity', 'humidity', 'humidity',
                  '#F45B69', '#F45B69', '%');
      }
  }).responseText});
