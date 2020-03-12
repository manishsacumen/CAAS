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

    },
    error: function(XMLHttpRequest, textStatus, errorThrown) {
    }
    });
    
    
    });

    $("#test_hubspot").click(function(e) {
      $('#overlay').fadeIn().delay(2000).fadeOut();
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
      
      
      },
      error: function(XMLHttpRequest, textStatus, errorThrown) {
        $("#hubspot_failed").show();
        $("#hubspot_success").hide();
         $('#hubspot_submit').prop('disabled', true);
      }
      });
    });