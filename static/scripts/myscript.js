$(document).ready(function() {
  $('ul.nav li a.nav-link').click(function()
  {
    var target_id = $(this).attr('href')
    console.log(target_id)

    $('div.tab-pane').addClass('active')
    $('div.tab-pane.process-tab').removeClass('active')
    $('div' + target_id).addClass('active') 
  })

});