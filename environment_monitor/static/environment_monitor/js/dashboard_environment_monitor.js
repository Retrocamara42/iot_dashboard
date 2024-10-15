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

function updateDataPointsPressure(){
   puntos_press=$('#puntos_press').val();
   iotMsSocket.send(JSON.stringify({
       'message': {
           'command':'send_initial_data_press',
           'max_points':puntos_press,
        }
   }));
}

/****** Socket functions *****/
iotMsSocket.onopen = function(e){
   // Temperature
   updateDataPointsTemperature();
   // Humidity
   updateDataPointsHumidity();
   // Pressure
   updateDataPointsPressure();
}



iotMsSocket.onmessage = function(e) {
   const data = JSON.parse(e.data);
   console.log(data);
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
         temperatureChart.data.labels.pop();
         temperatureChart.data.datasets.forEach((dataset) => {
            dataset.data.pop();
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
         humidityChart.data.labels.pop();
         humidityChart.data.datasets.forEach((dataset) => {
            dataset.data.pop();
         });
         // Add new point
         humidityChart.data.labels.unshift(message['timestamp']);
         humidityChart.data.datasets.forEach((dataset) => {
            dataset.data.unshift(message['humid']);
         });
         humidityChart.update();
      }
      else if(message.topic=="pressure"){
         // Remove first point
         pressureChart.data.labels.pop();
         pressureChart.data.datasets.forEach((dataset) => {
            dataset.data.pop();
         });
         // Add new point
         pressureChart.data.labels.unshift(message['timestamp']);
         pressureChart.data.datasets.forEach((dataset) => {
            dataset.data.unshift(message['press']);
         });
         pressureChart.update();
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
         console.log(data["message"]);
         humidityChart=drawChart(data["message"], '#humidity', 'humidity',
         'humidity', '#4db352', '#4db352', '%');
      }
      // Pressure
      else if(message.model=="environment_monitor.pressure"){
         if(typeof pressureChart!=='undefined'){
            pressureChart.destroy();
         }
         pressureChart=drawChart(data["message"], '#pressure', 'pressure',
         'pressure', '#ffb347', '#ffb347', 'atm');
      }
   }
};

$('#monitor_ambiente').css("font-weight","bold");
$('#mon_amb_dashboard').css("font-weight","bold");

