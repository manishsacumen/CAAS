$(document).ready(function() {

    $('#ssc_solarwinds_config').hide()  
    $('#solarwinds_success').hide()
    $('#solarwinds_failed').hide()
    $('#solarwinds_submit').prop('disabled', true);
   

});


$("#solarwinds_submit").click(function(e) {
  // $('#overlay').fadeIn().delay(2000).fadeOut();
    console.log("hii")
    e.preventDefault(); // avoid to execute the actual submit of the form.
    $('#solarwinds_overlay').fadeIn()
    var form = $("#solarwinds-form");
    var url = '/solarwinds/save_solarwinds/'
    
    $.ajax({
    type: "POST",
    url: url,
    data: form.serialize(), // serializes the form's elements.
    success: function(data)
    {
      $("#ssc_solarwinds_config").show();
      $("#solarwinds_config").hide();
      $('#solarwinds_overlay').fadeOut();

    },
    error: function(XMLHttpRequest, textStatus, errorThrown) {
      $('#solarwinds_overlay').fadeOut();
    }
    });
    
    
    });

    $("#test_solarwinds").click(function(e) {
      $('#solarwinds_overlay').fadeIn()
      $("#solarwinds_success").hide();
      $("#solarwinds_failed").hide();
      $('#solarwinds_submit').prop('disabled', true);
      e.preventDefault(); // avoid to execute the actual submit of the form.
      
      var form = $("#solarwinds-form");
      var url = '/solarwinds/test_solarwinds/'
      
      $.ajax({
      type: "POST",
      url: url,
      data: form.serialize(), // serializes the form's elements.
      success: function(data)
      {
        $("#solarwinds_success").show();
        $("#solarwinds_failed").hide();
        $('#solarwinds_submit').prop('disabled', false);
        $('#solarwinds_overlay').fadeOut();
        $("#solarwinds-form :input").prop("readonly", true);
      
      },
      error: function(XMLHttpRequest, textStatus, errorThrown) {
        $("#solarwinds_failed").show();
        $("#solarwinds_success").hide();
         $('#solarwinds_submit').prop('disabled', true);
         $('#solarwinds_overlay').fadeOut();
      }
      });
    });

    function solarwinds_reset(data  = null){
      if (data  = 'solarwinds'){
        document.getElementById("solarwinds-form").reset();
      }
      $("#solarwinds-form :input").prop("readonly", false);
      $('#solarwinds_success').hide()
      $('#solarwinds_failed').hide()
      $('#solarwinds_submit').prop('disabled', true);

    }