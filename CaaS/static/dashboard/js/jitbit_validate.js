$(document).ready(function() {

    $('#ssc_jitbit_config').hide()  
    $('#jitbit_success').hide()
    $('#jitbit_failed').hide()  

});

$("#jitbit_submit").click(function(e) {
    $('#overlay').fadeIn().delay(2000).fadeOut();
      console.log("hii")
      e.preventDefault(); // avoid to execute the actual submit of the form.
      
      var form = $("#jitbit-form");
      var url = '/jitbit/save_jitbit/'
      
      $.ajax({
      type: "POST",
      url: url,
      data: form.serialize(), // serializes the form's elements.
      success: function(data)
      {
        $("#ssc_jitbit_config").show();
        $("#jitbit_config").hide();
  
      },
      error: function(XMLHttpRequest, textStatus, errorThrown) {
      }
      });
      
      
      });
  
      $("#test_jitbit").click(function(e) {
        $('#overlay').fadeIn().delay(2000).fadeOut();
        $("#jitbit_success").hide();
        $("#jitbit_failed").hide();
        $('#jitbit_submit').prop('disabled', true);
        e.preventDefault(); // avoid to execute the actual submit of the form.
        
        var form = $("#jitbit-form");
        var url = '/jitbit/test_jitbit/'
        
        $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(), // serializes the form's elements.
        success: function(data)
        {
          $("#jitbit_success").show();
          $("#jitbit_failed").hide();
          $('#jitbit_submit').prop('disabled', false);
        
        
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
          $("#jitbit_failed").show();
          $("#jitbit_success").hide();
           $('#jitbit_submit').prop('disabled', true);
        }
        });
      });