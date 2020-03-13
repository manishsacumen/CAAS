$(document).ready(function() {

    $('#ssc_zohodesk_config').hide()  
    $('#zohodesk_success').hide()
    $('#zohodesk_failed').hide()  
    $('#zohodesk_submit').prop('disabled', true);

});

$("#zohodesk_submit").click(function(e) {
    $('#zohodesk_overlay').fadeIn();
      console.log("hii")
      e.preventDefault(); // avoid to execute the actual submit of the form.
      
      var form = $("#zohodesk-form");
      var url = '/zohodesk/save_zohodesk/'
      
      $.ajax({
      type: "POST",
      url: url,
      data: form.serialize(), // serializes the form's elements.
      success: function(data)
      {
        $("#ssc_zohodesk_config").show();
        $("#zohodesk_config").hide();
        $('#zohodesk_overlay').fadeOut();
  
      },
      error: function(XMLHttpRequest, textStatus, errorThrown) {
        $('#zohodesk_overlay').fadeOut();
      }
      });
      
      
      });
  
      $("#test_zohodesk").click(function(e) {
        $('#zohodesk_overlay').fadeIn()
        $("#zohodesk_success").hide();
        $("#zohodesk_failed").hide();
        $('#zohodesk_submit').prop('disabled', true);
        e.preventDefault(); // avoid to execute the actual submit of the form.
        
        var form = $("#zohodesk-form");
        var url = '/zohodesk/test_zohodesk/'
        
        $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(), // serializes the form's elements.
        success: function(data)
        {
          $("#zohodesk_success").show();
          $("#zohodesk_failed").hide();
          $('#zohodesk_submit').prop('disabled', false);
          $('#zohodesk_overlay').fadeOut();
          $("#zohodesk-form :input").prop("readonly", true);
        
        
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
          $("#zohodesk_failed").show();
          $("#zohodesk_success").hide();
          $('#zohodesk_submit').prop('disabled', true);
          $('#zohodesk_overlay').fadeOut();
        }
        });
      });

function zohodesk_reset(data=null){

  if (data  = 'zohodesk'){
    document.getElementById("zohodesk-form").reset();
  }
  $("#zohodesk-form :input").prop("readonly", false);
  $('#zohodesk_success').hide()
  $('#zohodesk_failed').hide()
  $('#zohodesk_submit').prop('disabled', true);
}