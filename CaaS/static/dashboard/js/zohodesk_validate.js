$(document).ready(function() {

    $('#ssc_zohodesk_config').hide()  
    $('#zohodesk_success').hide()
    $('#zohodesk_failed').hide()  

});

$("#zohodesk_submit").click(function(e) {
    $('#overlay').fadeIn().delay(2000).fadeOut();
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
  
      },
      error: function(XMLHttpRequest, textStatus, errorThrown) {
      }
      });
      
      
      });
  
      $("#test_zohodesk").click(function(e) {
        $('#overlay').fadeIn().delay(2000).fadeOut();
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
        
        
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
          $("#zohodesk_failed").show();
          $("#zohodesk_success").hide();
           $('#zohodesk_submit').prop('disabled', true);
        }
        });
      });