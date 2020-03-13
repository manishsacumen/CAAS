$(document).ready(function() {

    $('#ssc_jitbit_config').hide()  
    $('#jitbit_success').hide()
    $('#jitbit_failed').hide()  
    $('#jitbit_submit').prop('disabled', true);

});

$("#jitbit_submit").click(function(e) {
  $('#jitbit_overlay').fadeIn()
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
        $('#jitbit_overlay').fadeOut();
  
      },
      error: function(XMLHttpRequest, textStatus, errorThrown) {
        $('#jitbit_overlay').fadeOut();
      }
      });
      
      
      });
  
      $("#test_jitbit").click(function(e) {
        $('#jitbit_overlay').fadeIn()
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
          $('#jitbit_overlay').fadeOut();
          $("#jitbit-form :input").prop("readonly", true);
        
        
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
          $("#jitbit_failed").show();
          $("#jitbit_success").hide();
           $('#jitbit_submit').prop('disabled', true);
           $('#jitbit_overlay').fadeOut();
        }
        });
      });

      function   jitbit_reset(data = null){
        if (data == 'jitbit') {
          document.getElementById("jitbit-form").reset();
        }
        $("#jitbit-form :input").prop("readonly", false);
        $("#jitbit_success").hide();
        $("#jitbit_failed").hide();
        $('#jitbit_submit').prop('disabled', true);
        // $('#overlay').fadeOut()
      }