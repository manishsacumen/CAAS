$(document).ready(function() {

    $('#ssc_opsgenie_config').hide()  
    $('#opsgenie_success').hide()
    $('#opsgenie_failed').hide()  

});

$("#opsgenie_submit").click(function(e) {
    $('#overlay').fadeIn().delay(2000).fadeOut();
      console.log("hii")
      e.preventDefault(); // avoid to execute the actual submit of the form.
      
      var form = $("#opsgenie-form");
      var url = '/opsgenie/save_opsgenie/'
      
      $.ajax({
      type: "POST",
      url: url,
      data: form.serialize(), // serializes the form's elements.
      success: function(data)
      {
        $("#ssc_opsgenie_config").show();
        $("#opsgenie_config").hide();
  
      },
      error: function(XMLHttpRequest, textStatus, errorThrown) {
      }
      });
      
      
      });
  
      $("#test_opsgenie").click(function(e) {
        $('#overlay').fadeIn().delay(2000).fadeOut();
        $("#opsgenie_success").hide();
        $("#opsgenie_failed").hide();
        $('#opsgenie_submit').prop('disabled', true);
        e.preventDefault(); // avoid to execute the actual submit of the form.
        
        var form = $("#opsgenie-form");
        var url = '/opsgenie/test_opsgenie/'
        
        $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(), // serializes the form's elements.
        success: function(data)
        {
          $("#opsgenie_success").show();
          $("#opsgenie_failed").hide();
          $('#opsgenie_submit').prop('disabled', false);
        
        
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
          $("#opsgenie_failed").show();
          $("#opsgenie_success").hide();
           $('#opsgenie_submit').prop('disabled', true);
        }
        });
      });