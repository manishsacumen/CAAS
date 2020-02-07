$(document).ready(function() {

    $('#ssc_splunk_config').hide()  
    $('#splunk_success').hide()
    $('#splunk_failed').hide()

   

});


$("#splunk_submit").click(function(e) {
  $('#overlay').fadeIn().delay(2000).fadeOut();
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

    },
    error: function(XMLHttpRequest, textStatus, errorThrown) {
    }
    });
    
    
    });

    $("#test_splunk").click(function(e) {
      $('#overlay').fadeIn().delay(2000).fadeOut();
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
      
      
      },
      error: function(XMLHttpRequest, textStatus, errorThrown) {
        $("#splunk_failed").show();
        $("#splunk_success").hide();
         $('#splunk_submit').prop('disabled', true);
      }
      });
    });