/*Menu Icon*/
jQuery('document').ready(function($){

  var menuBtn = $('.menu-icon'),
  menu = $('.navigation ul');

  menuBtn.click(function(){
    if (menu.hasClass('show')){
      menu.removeClass('show');
    }
    else{
      menu.addClass('show');
    }
  });
});

function getSelectValue(){
  if(document.getElementById('tb_question').value == "Yes") {
    document.getElementById("tb_date").style.visibility = "visible";
  }
  else{
    document.getElementById("tb_date").style.visibility = "hidden";
  }
}