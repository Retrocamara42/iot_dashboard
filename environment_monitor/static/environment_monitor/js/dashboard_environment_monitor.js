/****** Dashboard functions *****/
function updateDataPointsTemperature(){
   puntos_temp=$('#puntos_temp').val();
   iotMsSocket.send(JSON.stringify({
       'message': {
           'command':'send_initial_data_temp',
           'max_points':puntos_temp,
        }
   }));
}

function updateDataPointsHumidity(){
   puntos_humid=$('#puntos_humid').val();
   iotMsSocket.send(JSON.stringify({
       'message': {
           'command':'send_initial_data_humid',
           'max_points':puntos_humid,
        }
   }));
}


/****** Socket functions *****/
iotMsSocket.onopen = function(e){
   // Temperature
   updateDataPointsTemperature();
   // Humidity
   updateDataPointsHumidity();
}



iotMsSocket.onmessage = function(e) {
   const data = JSON.parse(e.data);
   try{
      message=JSON.parse(data.message)[0];
   }catch(error){
      message=data.message[0];
   }
   // New data
   if(message.hasOwnProperty("topic")){
      // Temperature
      if(message.topic=="temperature"){
         // Remove first point
         temperatureChart.data.labels.shift();
         temperatureChart.data.datasets.forEach((dataset) => {
            dataset.data.shift();
         });
         // Add new point
         temperatureChart.data.labels.unshift(message['timestamp']);
         temperatureChart.data.datasets.forEach((dataset) => {
            dataset.data.unshift(message['temp']);
         });
         temperatureChart.update();
      }
      else if(message.topic=="humidity"){
         // Remove first point
         humidityChart.data.labels.shift();
         humidityChart.data.datasets.forEach((dataset) => {
            dataset.data.shift();
         });
         // Add new point
         humidityChart.data.labels.unshift(message['timestamp']);
         humidityChart.data.datasets.forEach((dataset) => {
            dataset.data.unshift(message['humid']);
         });
         humidityChart.update();
      }
   }
   // Initial data
   else if(message.hasOwnProperty("model")){
      // Temperature
      if(message.model=="environment_monitor.temperature"){
         if(typeof temperatureChart!=='undefined'){
            temperatureChart.destroy();
         }
         temperatureChart=drawChart(data["message"], '#temperature', 'temperature',
         'temperature', '#1c66c9', '#1c66c9', '°C');
      }
      // Humidity
      else if(message.model=="environment_monitor.humidity"){
         if(typeof humidityChart!=='undefined'){
            humidityChart.destroy();
         }
         humidityChart=drawChart(data["message"], '#humidity', 'humidity',
         'humidity', '#4db352', '#4db352', '%');
      }
   }
};

$('#monitor_ambiente').css("font-weight","bold");
$('#mon_amb_dashboard').css("font-weight","bold");

