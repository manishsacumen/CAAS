$(document).ready(function() {

    $('#ssc_agilecrm_config').hide()  
    $('#agilecrm_success').hide()
    $('#agilecrm_failed').hide()
    $('#agilecrm_submit').prop('disabled', true);
   

});


$("#agilecrm_submit").click(function(e) {
  // $('#overlay').fadeIn().delay(2000).fadeOut();
    console.log("hii")
    e.preventDefault(); // avoid to execute the actual submit of the form.
    
    var form = $("#agilecrm-form");
    var url = '/agilecrm/save_agilecrm/'
    
    $.ajax({
    type: "POST",
    url: url,
    data: form.serialize(), // serializes the form's elements.
    success: function(data)
    {
      $("#ssc_agilecrm_config").show();
      $("#agilecrm_config").hide();

    },
    error: function(XMLHttpRequest, textStatus, errorThrown) {
    }
    });
    
    
    });

    $("#test_agilecrm").click(function(e) {
      $('#overlay').fadeIn().delay(2000).fadeOut();
      $("#agilecrm_success").hide();
      $("#agilecrm_failed").hide();
      $('#agilecrm_submit').prop('disabled', true);
      e.preventDefault(); // avoid to execute the actual submit of the form.
      
      var form = $("#agilecrm-form");
      var url = '/agilecrm/test_agilecrm/'
      
      $.ajax({
      type: "POST",
      url: url,
      data: form.serialize(), // serializes the form's elements.
      success: function(data)
      {
        $("#agilecrm_success").show();
        $("#agilecrm_failed").hide();
        $('#agilecrm_submit').prop('disabled', false);
      
      
      },
      error: function(XMLHttpRequest, textStatus, errorThrown) {
        $("#agilecrm_failed").show();
        $("#agilecrm_success").hide();
         $('#agilecrm_submit').prop('disabled', true);
      }
      });
    });