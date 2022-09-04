/****** SD Info functions *****/
Date.prototype.addHours = function(h) {
   this.setTime(this.getTime() + (h*60*60*1000));
   return this;
 }


function humanReadableSize(bytes){
   if(bytes>=1000000000){
     return String((bytes/1000000000).toFixed(1))+" GB";
   }
   else if(bytes>=1000000){
     return String((bytes/1000000).toFixed(1))+" MB";  
   }
   else if(bytes>=1000){
     return String((bytes/1000).toFixed(1))+" KB";
   }
   else{
     return String((bytes).toFixed(1))+" B";
   }
 }


function update_sd_info(sd_info){
   total_storage=humanReadableSize(sd_info["total_storage"])
   $("#total_storage").html("Almacenamiento total: <br>"+total_storage);
   free_storage=humanReadableSize(sd_info["free_storage"])
   $("#free_storage").html("Almacenamiento total: <br>"+free_storage);
   used_storage=humanReadableSize(sd_info["used_storage"])
   $("#used_storage").html("Almacenamiento total: <br>"+used_storage);
}


function change_status_on(){
   $("#status").html('<i id="status_icon" class="fas fa-power-off" '+
      'style="color:green" ></i>Conectado');
}


function change_status_off(){
   $("#status").html('<i id="status_icon" class="fas fa-power-off" '+
      'style="color:gray" ></i>Desconectado');
}

function check_m5_status(last_update_time){
   var last_update_date=new Date(last_update_time);
   last_update_date = last_update_date.addHours(10); // Time correction from DB
   var now=(new Date()).toUTCString();
   now=new Date(now.substring(0,now.length-3));
   var time_diff=now-last_update_date;
   time_diff = time_diff/(1000*3600);
   if(time_diff<1){
      change_status_on();
   }
   else{
      change_status_off();
   }
}


/****** Socket functions *****/
 iotMsSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    try{
       message=JSON.parse(data.message)[0];
    }catch(error){
       message=data.message[0];
    }
    // New data
    if(message.hasOwnProperty("topic")){
       // SD Info
       if(message.topic=="m5_sd_info"){
         change_status_on();
         update_sd_info(message);
       }
       else if(message.topic=="m5_alive"){
         change_status_on();
       }
    }
 };
/*
$("#upload_to_sd").click(function() {
   var file = document.getElementById('sd_file').files[0];
   var sd_filename = document.getElementById('sd_file').value;
   sd_filename=sd_filename.substring(sd_filename.lastIndexOf("\\")+1);
   console.log(sd_filename)
   var reader = new FileReader();
   var rawData = new ArrayBuffer();
   let sizeLength = 1;
   if (file.size > 0xffff){ sizeLength = 4; }
   else if (file.size > 0xff){ sizeLength = 2; }

   const utf8 = new TextEncoder();
   const nameBuffer = utf8.encode(sd_filename);
   const length = file.size + sizeLength + nameBuffer.length + 2;
   const buffer = new Uint8Array(length)

   let i = 0;
   buffer[i] = nameBuffer.length;
   buffer.set(i+=1, nameBuffer);
   const sizeView = new DataView(buffer)
   sizeView[`setUInt${sizeLength*8}`](i += nameBuffer, file.size)

   reader.onload = function(e) {
      rawData = e.target.result;
      buffer.set(rawData, i + sizeLength)
      iotMsSocket.send(buffer);
      alert("Se envió el archivo");
   }
   reader.readAsArrayBuffer(file);
});
*/


/***************** Load sd info ************************/
data = $.ajax({
   type:"POST",
   url: "/anim5_stack/load_sd_info/",
   dataType:"json",
   async: true,
   success: function(data){
      sd_info=JSON.parse(data)[0];
      check_m5_status(sd_info["fields"]["timestamp"]);
      update_sd_info(sd_info["fields"]);
   }
}).responseText;



$('#anim5_stack').css("font-weight","bold");
$('#anim5_sdmanager').css("font-weight","bold");


 