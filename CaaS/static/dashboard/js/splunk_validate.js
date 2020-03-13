$(document).ready(function() {

    $('#ssc_splunk_config').hide()  
    $('#splunk_success').hide()
    $('#splunk_failed').hide()
    $('#splunk_submit').prop('disabled', true);
   

});


$("#splunk_submit").click(function(e) {
  $('#splunk_overlay').fadeIn()
    console.log("hii")
    e.preventDefault(); // avoid to execute the actual submit of the form.
    
    var form = $("#splunk-form");
    var url = '/splunk/save_splunk/'
    
    $.ajax({
    type: "POST",
    url: url,
    data: form.serialize(), // serializes the form's elements.
    success: function(data)
    {
      $("#ssc_splunk_config").show();
      $("#splunk_config").hide();
      $('#splunk_overlay').fadeOut();

    },
    error: function(XMLHttpRequest, textStatus, errorThrown) {
      $('#splunk_overlay').fadeOut();
    }
    });
    
    
    });

    $("#test_splunk").click(function(e) {
      $('#splunk_overlay').fadeIn()
      $("#splunk_success").hide();
      $("#splunk_failed").hide();
      $('#splunk_submit').prop('disabled', true);
      e.preventDefault(); // avoid to execute the actual submit of the form.
      
      var form = $("#splunk-form");
      var url = '/splunk/test_splunk/'
      
      $.ajax({
      type: "POST",
      url: url,
      data: form.serialize(), // serializes the form's elements.
      success: function(data)
      {
        $("#splunk_success").show();
        $("#splunk_failed").hide();
        $('#splunk_submit').prop('disabled', false);
        $("#splunk-form :input").prop("readonly", true);
        $('#splunk_overlay').fadeOut();
      
      },
      error: function(XMLHttpRequest, textStatus, errorThrown) {
        $("#splunk_failed").show();
        $("#splunk_success").hide();
        $('#splunk_submit').prop('disabled', true);
        $('#splunk_overlay').fadeOut();
      }
      });
    });

    function splunk_reset(data  = null){
      if (data  = 'splunk'){
        document.getElementById("splunk-form").reset();
      }
      $("#splunk-form :input").prop("readonly", false);
      $('#splunk_success').hide()
      $('#splunk_failed').hide()
      $('#splunk_submit').prop('disabled', true);

    }