/****** SD Info functions *****/
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


function check_m5_status(last_update_time){
   var time_diff=new Date()-new Date(last_update_time);
   time_diff = time_diff/(1000*3600);
   if(time_diff<1){
      $("#status_icon").css("color","green");
   }
   else{
      $("#status_icon").css("color","gray");
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
         $("#status_icon").css("color","green");
         update_sd_info(message);
       }
       else if(message.topic=="m5_alive"){
         $("#status_icon").css("color","green");
       }
    }
 };

$("#upload_to_sd").click(function() {
   var file = document.getElementById('sd_file').files[0];
   var reader = new FileReader();
   var rawData = new ArrayBuffer();
   reader.onload = function(e) {
      rawData = e.target.result;
      iotMsSocket.send(rawData);
      alert("Se envió el archivo");
   }
   reader.readAsArrayBuffer(file);
});



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


 