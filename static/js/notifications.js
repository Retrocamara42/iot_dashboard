function show_notification(notification_type, message){
  $("#notifyType").html(message);
  $("#notifyType").toggleClass("active");
  $("#notifyType").toggleClass(notification_type);

  setTimeout(function(){
    $("#notifyType").removeClass("active");
    $("#notifyType").removeClass(notification_type);
    $("#notifyType").html("");
},5000);
}
