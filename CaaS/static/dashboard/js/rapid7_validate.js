$(document).ready(function() {

    $('#ssc_rapid_config').hide()  
    $('#rapid_success').hide()
    $('#rapid_failed').hide()  
    $('#rapid_submit').prop('disabled', true);

});

$("#rapid_submit").click(function(e) {
  $('#rapid_overlay').fadeIn()
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
        $('#rapid_overlay').fadeOut()
  
      },
      error: function(XMLHttpRequest, textStatus, errorThrown) {
        $('#rapid_overlay').fadeOut()
      }
      });
      
      
      });
  
      $("#test_rapid").click(function(e) {
        $('#rapid_overlay').fadeIn()
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
          $('#rapid_overlay').fadeOut()
          $("#rapid-form :input").prop("readonly", true);
        
        
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
          $("#rapid_failed").show();
          $("#rapid_success").hide();
           $('#rapid_submit').prop('disabled', true);
           $('#rapid_overlay').fadeOut()
           
        }
        });
      });
function rapid_reset(data= null){
  if (data  = 'rapid'){
    document.getElementById("rapid-form").reset();
  }
  $("#rapid-form :input").prop("readonly", false);
  $('#rapid_success').hide()
  $('#rapid_failed').hide()
  $('#rapid_submit').prop('disabled', true);

}