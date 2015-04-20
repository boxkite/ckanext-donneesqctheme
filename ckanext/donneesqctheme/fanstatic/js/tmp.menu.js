function setClickableTooltip(target, content, position, indelay){
      target.tooltip({
        show: {delay: indelay, duration:400 } ,
        position: position,
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
    newHeight = $('.resource-view').outerHeight() + 30;
    $('.dqc-preview').animate({height:newHeight}, 500);
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
      setClickableTooltip($(this), $(this).find("p").html(), { my: "left-40 center", at: "right top+50", collision: "none" }, 500);
      })

    $('.dqc-front').click(expandPreview);
    $('.dqc-contract').click(contractPreview);


});

/*

var formatMapper = {
  "CSV": "CSV: Données tabulaire pouvant être importées dans MS Excel et autres. <a href='/content/format#csv'>En savoir plus</a>", 
  "JSON": "JSON: Format structuré principalement pour être consommé par des applications. <a href='/content/format#json'>En savoir plus</a>"
  };


$(document).ready(function(){
    $('.resource-list span.format-label').each( function(index){

      setClickableTooltip($(this), formatMapper[$(this).html()], { my: "left center", at: "right top", collision: "none" }, 100);
      })
});
*/



$(document).ready(
  /* This is the function that will get executed after the DOM is fully loaded */

  function () {
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


