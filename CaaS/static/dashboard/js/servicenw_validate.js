$(document).ready(function() {

    $('#ssc_servicenow_config').hide()  
    $('#servicenow_success').hide()
    $('#servicenow_failed').hide()  
    $('#servicenow_submit').prop('disabled', true);
    $("#servicenow-form").validate({
      rules: {
        app_url : {
          required: true,
        },
        api_key: {
          required: true,
        },
        username: {
          required: true,
        },
        password: {
          required: true,
        }
      },
      messages : {
        app_url: {
          required: "App Url is required"
        },
        api_key: {
          required: "Api Key is required",
        },
        username: {
          required: "Username is required",
         
        },
        password: {
          required: "Password is required",

        }
      }
    });
  });

$("#servicenow_submit").click(function(e) {
    $('#overlay_servicenw').fadeIn();
      console.log("hii")
      e.preventDefault(); // avoid to execute the actual submit of the form.
      
      var form = $("#servicenow-form");
      var url = '/servicenow/save_servicenow/'
      
      $.ajax({
      type: "POST",
      url: url,
      data: form.serialize(), // serializes the form's elements.
      success: function(data)
      {
        $("#ssc_servicenow_config").show();
        $("#servicenow_config").hide();
        $('#overlay_servicenw').fadeOut();
  
      },
      error: function(XMLHttpRequest, textStatus, errorThrown) {
        $('#overlay_servicenw').fadeOut();
      }
      });
      
      
});
  
      $("#test_servicenow").click(function(e) {
        $('#overlay_servicenw').fadeIn();
        $("#servicenow_success").hide();
        $("#servicenowd_failed").hide();
        $('#servicenow_submit').prop('disabled', true);
        e.preventDefault(); // avoid to execute the actual submit of the form.
        
        var form = $("#servicenow-form");
        var url = '/servicenow/test_servicenow/'
        
        $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(), // serializes the form's elements.
        success: function(data)
        {
          $("#servicenow_success").show();
          $("#servicenow_failed").hide();
          $('#servicenow_submit').prop('disabled', false);
          $('#overlay_servicenw').fadeOut();
          $("#servicenow-form :input").prop("readonly", true);
        
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
          $("#servicenow_failed").show();
          $("#servicenow_success").hide();
           $('#servicenow_submit').prop('disabled', true);
           $('#overlay_servicenw').fadeOut();
        }
        });
      });

function servicenw_reset(data = null){
  if (data == "servicenw"){
    document.getElementById("servicenow-form").reset();
  }
  $("#servicenow-form :input").prop("readonly", false);
    $('#servicenow_success').hide()
    $('#servicenow_failed').hide()  
    $('#servicenow_submit').prop('disabled', true);


}