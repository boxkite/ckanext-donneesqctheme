function rewriteOrgUrl (){
    var suffix = '#data-section';
    $('.pagination a[href]').each( function(index){
      var previous =  $(this).attr('href');

      $(this).attr('href', previous + suffix);
    })
  
}

$(document).ready(
  /* This is the function that will get executed after the DOM is fully loaded */

  function () {
    rewriteOrgUrl();
  }
);