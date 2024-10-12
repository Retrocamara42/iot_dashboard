const device_name = "iot_ms";
var temperatureChart;
var humidityChart;
var pressureChart;

/****** Socket declaration *****/
const iotMsSocket = new WebSocket(
   ((window.location.protocol === 'https:') ? 'wss://' : 'ws://')
   + window.location.host
   + '/ws/environment_monitor/'
   + device_name
   + '/'
);


iotMsSocket.onclose = function(e) {
   console.error('Iot socket closed unexpectedly');
};
