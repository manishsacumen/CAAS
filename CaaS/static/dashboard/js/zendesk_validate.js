$(document).ready(function() {

    $('#ssc_zendesk_config').hide()  
    $('#zendesk_success').hide()
    $('#zendesk_failed').hide()  
    $('#zendesk_submit').prop('disabled', true);

});

$("#zendesk_submit").click(function(e) {
    $('#overlay').fadeIn().delay(2000).fadeOut();
      console.log("hii")
      e.preventDefault(); // avoid to execute the actual submit of the form.
      
      var form = $("#zendesk-form");
      var url = '/zendesk/save_zendesk/'
      
      $.ajax({
      type: "POST",
      url: url,
      data: form.serialize(), // serializes the form's elements.
      success: function(data)
      {
        $("#ssc_zendesk_config").show();
        $("#zendesk_config").hide();
  
      },
      error: function(XMLHttpRequest, textStatus, errorThrown) {
      }
      });
      
      
      });
  
      $("#test_zendesk").click(function(e) {
        $('#zendesk_overlay').fadeIn()
        $("#zendesk_success").hide();
        $("#zendesk_failed").hide();
        $('#zendesk_submit').prop('disabled', true);
        e.preventDefault(); // avoid to execute the actual submit of the form.
        
        var form = $("#zendesk-form");
        var url = '/zendesk/test_zendesk/'
        
        $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(), // serializes the form's elements.
        success: function(data)
        {
          $("#zendesk_success").show();
          $("#zendesk_failed").hide();
          $('#zendesk_submit').prop('disabled', false);
          $("#zendesk-form :input").prop("readonly", true);
          $('#zendesk_overlay').fadeOut()
        
        
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
          $("#zendesk_failed").show();
          $("#zendesk_success").hide();
           $('#zendesk_submit').prop('disabled', true);
           $('#zendesk_overlay').fadeOut()
        }
        });
      });
function zendesk_reset(data = null){
  if (data  = 'zendesk'){
    document.getElementById("zendesk-form").reset();
  }
  $("#zendesk-form :input").prop("readonly", false);
  $('#zendesk_success').hide()
  $('#zendesk_failed').hide()
  $('#zendesk_submit').prop('disabled', true);
}