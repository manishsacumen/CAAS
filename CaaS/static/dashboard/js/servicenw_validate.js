$(document).ready(function() {

    $('#ssc_servicenow_config').hide()  
    $('#servicenow_success').hide()
    $('#servicenow_failed').hide()  
    $('#servicenow_submit').prop('disabled', true);

});

$("#servicenow_submit").click(function(e) {
    $('#overlay').fadeIn().delay(2000).fadeOut();
      console.log("hii")
      e.preventDefault(); // avoid to execute the actual submit of the form.
      
      var form = $("#servicenow-form");
      var url = '/servicenow/save_servicenow/'
      
      $.ajax({
      type: "POST",
      url: url,
      data: form.serialize(), // serializes the form's elements.
      success: function(data)
      {
        $("#ssc_servicenow_config").show();
        $("#servicenow_config").hide();
  
      },
      error: function(XMLHttpRequest, textStatus, errorThrown) {
      }
      });
      
      
      });
  
      $("#test_servicenow").click(function(e) {
        $('#overlay').fadeIn().delay(2000).fadeOut();
        $("#servicenow_success").hide();
        $("#servicenowd_failed").hide();
        $('#servicenow_submit').prop('disabled', true);
        e.preventDefault(); // avoid to execute the actual submit of the form.
        
        var form = $("#servicenow-form");
        var url = '/servicenow/test_servicenow/'
        
        $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(), // serializes the form's elements.
        success: function(data)
        {
          $("#servicenow_success").show();
          $("#servicenow_failed").hide();
          $('#servicenow_submit').prop('disabled', false);
        
        
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
          $("#servicenow_failed").show();
          $("#servicenow_success").hide();
           $('#servicenow_submit').prop('disabled', true);
        }
        });
      });