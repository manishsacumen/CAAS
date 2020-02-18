$(document).ready(function() {

    $('#ssc_pagerduty_config').hide()  
    $('#pagerduty_success').hide()
    $('#pagerduty_failed').hide()  
    $('#pagerduty_submit').prop('disabled', true);

});

$("#pagerduty_submit").click(function(e) {
    $('#overlay').fadeIn().delay(2000).fadeOut();
      console.log("hii")
      e.preventDefault(); // avoid to execute the actual submit of the form.
      
      var form = $("#pagerduty-form");
      var url = '/pagerduty/save_pagerduty/'
      
      $.ajax({
      type: "POST",
      url: url,
      data: form.serialize(), // serializes the form's elements.
      success: function(data)
      {
        $("#ssc_pagerduty_config").show();
        $("#pagerduty_config").hide();
  
      },
      error: function(XMLHttpRequest, textStatus, errorThrown) {
      }
      });
      
      
      });
  
      $("#test_pagerduty").click(function(e) {
        $('#overlay').fadeIn().delay(2000).fadeOut();
        $("#pagerduty_success").hide();
        $("#pagerduty_failed").hide();
        $('#pagerduty_submit').prop('disabled', true);
        e.preventDefault(); // avoid to execute the actual submit of the form.
        
        var form = $("#pagerduty-form");
        var url = '/pagerduty/test_pagerduty/'
        
        $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(), // serializes the form's elements.
        success: function(data)
        {
          $("#pagerduty_success").show();
          $("#pagerduty_failed").hide();
          $('#pagerduty_submit').prop('disabled', false);
        
        
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
          $("#pagerduty_failed").show();
          $("#pagerduty_success").hide();
           $('#pagerduty_submit').prop('disabled', true);
        }
        });
      });