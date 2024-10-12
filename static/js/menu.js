var nav_item_states=Cookies.get('nav_item_states');
if(nav_item_states == null){
   Cookies.set('nav_item_states', [0,0], { secure: true });
}
else{
   nav_item_states=nav_item_states.split(",");
   $('.nav-expandable').each(function(i, obj){
      if(parseInt(nav_item_states[i])==1){
         $(obj).attr('class',"nav-item nav-expandable nav-open");
      }
   });
}

$(".nav-expandable").click(function() {
   classes=$(this).attr('class');
   nav_item_index=-1;
   current_obj=$(this);
   $('.nav-item').each(function(i, obj) {
      if(current_obj.is($(obj))){
         nav_item_index=i;
      }
   });
   if(classes.indexOf("nav-closed")>=0){
      $(this).attr('class',"nav-item nav-expandable nav-open");
      nav_item_states[nav_item_index]=1;
      Cookies.set('nav_item_states', nav_item_states, { secure: true });
   }
   else{
      $(this).attr('class',"nav-item nav-expandable nav-closed");
      nav_item_states[nav_item_index]=0;
      Cookies.set('nav_item_states', nav_item_states, { secure: true });
   }
});
