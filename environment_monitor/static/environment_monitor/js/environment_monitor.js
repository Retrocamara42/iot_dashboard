$.ajaxSetup({
  headers: { "X-CSRFToken": Cookies.get('csrftoken') }
});

var temperatureChart;
var humidityChart;


function getTemperatureDataByPoints(){
    puntos_temp=$('#puntos_temp').val();
    data = $.ajax({
        type:"POST",
        url: "/environment_monitor/get_temperature_data/",
        dataType:"json",
        async: true,
        data:{"puntos_temp":puntos_temp},
        success: function (data) {
           if (typeof temperatureChart!=='undefined'){
             /* Remove old data
             temperatureChart.data.labels.pop();
             temperatureChart.data.datasets.forEach((dataset) => {
                 dataset.data.pop();
             });
             // Add new data
             for(let record of JSON.parse(data)){
                temperatureChart.data.labels.push(record["fields"]['timestamp']);
                temperatureChart.data.datasets.forEach((dataset) => {
                    dataset.data.push(record["fields"]['temperature']);
                });
             }
             temperatureChart.update();*/
             temperatureChart.destroy();
           }
           temperatureChart=drawChart(data, '#temperature', 'temperature', 'temperature',
               '#456990', '#456990', '°C');
        }
    }).responseText
}


function getHumidityDataByPoints(){
  puntos_humid=$('#puntos_humid').val();
  data = $.ajax({
      type:"POST",
      url: "/environment_monitor/get_humidity_data/",
      dataType:"json",
      async: true,
      data:{"puntos_humid":puntos_humid},
      success: function (data) {
         if (typeof humidityChart!=='undefined'){
            humidityChart.destroy();
         }
         humidityChart=drawChart(data, '#humidity', 'humidity', 'humidity',
                  '#2e7d32', '#2e7d32', '%');
      }
  }).responseText
}


$(document).ready(getTemperatureDataByPoints);
$(document).ready(getHumidityDataByPoints);
