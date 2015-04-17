function setClickableTooltip(target, content){
      target.tooltip({
        show: {delay: 500, duration:400 } ,
        position: { my: "left-40 center", at: "right top+50", collision: "none" },
        content: content, //from params
        hide: { effect: "" }, //fadeOut
        close: function(event, ui){
            ui.tooltip.hover(
                function () {
                    $(this).stop(true).fadeTo(400, 1); 
                },
                function () {
                    $(this).fadeOut("400", function(){
                        $(this).remove(); 
                    })
                }
            );
        }  
    });
}


function expandPreview (){
    $('.dqc-preview').animate({height:'460px'}, 500);
    $('.resource-view').animate({'margin-top':'0px'}, 500);
    $('.dqc-front').css('z-index', -1000);

}

function contractPreview (){
    $('.dqc-preview').animate({height:'200px'}, 500);
    $('.resource-view').animate({'margin-top':'-85px'}, 500);
    $('.dqc-front').css('z-index', 1000);

}


$(document).ready(function(){
    $('.media-item').each( function(index){
      setClickableTooltip($(this), $(this).find("p").html());
      })

    $('.dqc-front').click(expandPreview);
    $('.dqc-contract').click(contractPreview);


});





$(document).ready(
  /* This is the function that will get executed after the DOM is fully loaded */
  function () {
    /* Next part of code handles hovering effect and submenu appearing */
    $('.nav-pills li').hover(
      function () { //appearing on hover
        $('ul', this).fadeIn();
      },
      function () { //disappearing on hover
        $('ul', this).fadeOut();
      }
    );
  }
);


