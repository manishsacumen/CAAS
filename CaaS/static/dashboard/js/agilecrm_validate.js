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
    $('#agile_overlay').fadeIn()
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
      $('#agile_overlay').fadeOut();

    },
    error: function(XMLHttpRequest, textStatus, errorThrown) {
      $('#agile_overlay').fadeOut();
    }
    });
    
    
    });

    $("#test_agilecrm").click(function(e) {
      $('#agile_overlay').fadeIn()
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
        $('#agile_overlay').fadeOut();
        $("#agile-form :input").prop("readonly", false);
      
      
      },
      error: function(XMLHttpRequest, textStatus, errorThrown) {
        $("#agilecrm_failed").show();
        $("#agilecrm_success").hide();
         $('#agilecrm_submit').prop('disabled', true);
         $('#agile_overlay').fadeOut();
      }
      });
    });

    function agilecrm_reset(data){
      if (data == 'agile') {
        document.getElementById("agile-form").reset();
      }
      $("#agile-form :input").prop("readonly", false);
      $("#agile_success").hide();
      $("#agile_failed").hide();
      $('#agile_submit').prop('disabled', true);
      // $('#overlay').fadeOut()

    }