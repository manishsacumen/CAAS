$(document).ready(function() {

    $('#ssc_rapid_config').hide()  
    $('#rapid_success').hide()
    $('#rapid_failed').hide()  
    $('#rapid_submit').prop('disabled', true);

});

$("#rapid_submit").click(function(e) {
    $('#overlay').fadeIn().delay(2000).fadeOut();
      console.log("hii")
      e.preventDefault(); // avoid to execute the actual submit of the form.
      
      var form = $("#rapid-form");
      var url = '/rapid/save_rapid/'
      
      $.ajax({
      type: "POST",
      url: url,
      data: form.serialize(), // serializes the form's elements.
      success: function(data)
      {
        $("#ssc_rapid_config").show();
        $("#rapid_config").hide();
  
      },
      error: function(XMLHttpRequest, textStatus, errorThrown) {
      }
      });
      
      
      });
  
      $("#test_rapid").click(function(e) {
        $('#overlay').fadeIn().delay(2000).fadeOut();
        $("#rapid_success").hide();
        $("#rapid_failed").hide();
        $('#rapid_submit').prop('disabled', true);
        e.preventDefault(); // avoid to execute the actual submit of the form.
        
        var form = $("#rapid-form");
        var url = '/rapid/test_rapid/'
        
        $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(), // serializes the form's elements.
        success: function(data)
        {
          $("#rapid_success").show();
          $("#rapid_failed").hide();
          $('#rapid_submit').prop('disabled', false);
        
        
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
          $("#rapid_failed").show();
          $("#rapid_success").hide();
           $('#rapid_submit').prop('disabled', true);
        }
        });
      });