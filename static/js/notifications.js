function show_notification(notification_type, message){
  $("#notifyType").html(message);
  $(".notify").toggleClass("active");
  $("#notifyType").removeClass(notification_type);

  setTimeout(function(){
    $(".notify").removeClass("active");
    $("#notifyType").removeClass(notification_type);
    $("#notifyType").html("");
},2500);
}
