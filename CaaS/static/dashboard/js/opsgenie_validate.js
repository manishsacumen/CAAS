$(document).ready(function() {

    $('#ssc_opsgenie_config').hide()  
    $('#opsgenie_success').hide()
    $('#opsgenie_failed').hide()  
    $('#opsgenie_submit').prop('disabled', true);

});

$("#opsgenie_submit").click(function(e) {
  $('#opsgenie_overlay').fadeIn()
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
        $('#opsgenie_overlay').fadeOut();
  
      },
      error: function(XMLHttpRequest, textStatus, errorThrown) {
        $('#opsgenie_overlay').fadeOut();
      }
      });
      
      
      });
  
      $("#test_opsgenie").click(function(e) {
        $('#opsgenie_overlay').fadeIn()
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
          $('#opsgenie_overlay').fadeOut();
          $("#opsgenie-form :input").prop("readonly", true);
        
        
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
          $("#opsgenie_failed").show();
          $("#opsgenie_success").hide();
           $('#opsgenie_submit').prop('disabled', true);
           $('#opsgenie_overlay').fadeOut();
        }
        });
      });
function opsgenie_reset(data = null){
  if (data  = 'opsgenie'){
    document.getElementById("opsgenie-form").reset();
  }
  $("#opsgenie-form :input").prop("readonly", false);
  $('#opsgenie_success').hide()
  $('#opsgenie_failed').hide()
  $('#opsgenie_submit').prop('disabled', true);

}