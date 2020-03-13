$(document).ready(function() {

    $('#ssc_hubspot_config').hide()  
    $('#hubspot_success').hide()
    $('#hubspot_failed').hide()
    $('#hubspot_submit').prop('disabled', true);
   

});


$("#hubspot_submit").click(function(e) {
  // $('#overlay').fadeIn().delay(2000).fadeOut();
    console.log("hii")
    e.preventDefault(); // avoid to execute the actual submit of the form.
    $('#hubspot_overlay').fadeIn()
    var form = $("#hubspot-form");
    var url = '/hubspot/save_hubspot/'
    
    $.ajax({
    type: "POST",
    url: url,
    data: form.serialize(), // serializes the form's elements.
    success: function(data)
    {
      $("#ssc_hubspot_config").show();
      $("#hubspot_config").hide();
      $('#hubspot_overlay').fadeOut();

    },
    error: function(XMLHttpRequest, textStatus, errorThrown) {
      $('#hubspot_overlay').fadeOut();
    }
    });
    
    
    });

    $("#test_hubspot").click(function(e) {
      $('#hubspot_overlay').fadeIn()
      $("#hubspot_success").hide();
      $("#hubspot_failed").hide();
      $('#hubspot_submit').prop('disabled', true);
      e.preventDefault(); // avoid to execute the actual submit of the form.
      
      var form = $("#hubspot-form");
      var url = '/hubspot/test_hubspot/'
      
      $.ajax({
      type: "POST",
      url: url,
      data: form.serialize(), // serializes the form's elements.
      success: function(data)
      {
        $("#hubspot_success").show();
        $("#hubspot_failed").hide();
        $('#hubspot_submit').prop('disabled', false);
        $('#hubspot_overlay').fadeOut();
        $("#hubspot-form :input").prop("readonly", true);
      
      
      },
      error: function(XMLHttpRequest, textStatus, errorThrown) {
        $("#hubspot_failed").show();
        $("#hubspot_success").hide();
         $('#hubspot_submit').prop('disabled', true);
         $('#hubspot_overlay').fadeOut();
      }
      });
    });
  function   hubspot_reset(data = null){
    if (data == 'hubspot') {
      document.getElementById("hubspot-form").reset();
    }
    $("#hubspot-form :input").prop("readonly", false);
    $("#hubspot_success").hide();
    $("#hubspot_failed").hide();
    $('#hubspot_submit').prop('disabled', true);
    // $('#overlay').fadeOut()
  }