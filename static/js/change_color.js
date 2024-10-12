menu_bg_colors=["#62476b","#58595B","#407A52","#044F67","#DF8600","#9D2933","#DB5A6B"]

function changeColor(){
   current_index_color=Cookies.get('index_color');
   current_index_color++;
   if ((current_index_color == null) || (current_index_color==menu_bg_colors.length)){
      Cookies.set('index_color', 0, { secure: true });
      $("#sidebar").css("background-color",menu_bg_colors[0]);
   }
   else{
      $("#sidebar").css("background-color",menu_bg_colors[current_index_color]);
      Cookies.set('index_color', current_index_color, { secure: true });
   }
}

current_index_color=Cookies.get('index_color');
if(current_index_color>=menu_bg_colors.length || current_index_color=="NaN"){
   current_index_color=0;
   Cookies.set('index_color', 0, { secure: true });
}
$("#sidebar").css("background-color",menu_bg_colors[current_index_color]);
