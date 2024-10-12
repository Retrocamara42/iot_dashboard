const device_name = "anim5";

/****** Socket declaration *****/
const iotMsSocket = new WebSocket(
   ((window.location.protocol === 'https:') ? 'wss://' : 'ws://')
   + window.location.host
   + '/ws/anim5stack/'
   + device_name
   + '/'
);


iotMsSocket.onclose = function(e) {
   console.error('Iot socket closed unexpectedly');
};
