$(document).ready(function() {

    $('#ssc_freshdesk_config').hide()  
    $('#freshdesk_success').hide()
    $('#freshdesk_failed').hide()  
    $('#freshdesk_submit').prop('disabled', true);

});

$("#freshdesk_submit").click(function(e) {
    $('#overlay').fadeIn().delay(2000).fadeOut();
      console.log("hii")
      e.preventDefault(); // avoid to execute the actual submit of the form.
      
      var form = $("#freshdesk-form");
      var url = '/freshdesk/save_Freshdesk/'
      
      $.ajax({
      type: "POST",
      url: url,
      data: form.serialize(), // serializes the form's elements.
      success: function(data)
      {
        $("#ssc_freshdesk_config").show();
        $("#freshdesk_config").hide();
  
      },
      error: function(XMLHttpRequest, textStatus, errorThrown) {
      }
      });
      
      
      });
  
      $("#test_freshdesk").click(function(e) {
        $('#overlay').fadeIn().delay(2000).fadeOut();
        $("#freshdesk_success").hide();
        $("#freshdesk_failed").hide();
        $('#freshdesk_submit').prop('disabled', true);
        e.preventDefault(); // avoid to execute the actual submit of the form.
        
        var form = $("#freshdesk-form");
        var url = '/freshdesk/test_Freshdesk/'
        
        $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(), // serializes the form's elements.
        success: function(data)
        {
          $("#freshdesk_success").show();
          $("#freshdesk_failed").hide();
          $('#freshdesk_submit').prop('disabled', false);
        
        
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
          $("#freshdesk_failed").show();
          $("#freshdesk_success").hide();
           $('#freshdesk_submit').prop('disabled', true);
        }
        });
      });