$(document).ready(function() {
  $('#ssc_config').hide()  
  $("#jira_success").hide();
    $("#jira_failed").hide();
    $('#jira_submit').prop('disabled', true);
    $("#basic-form").validate({
      rules: {
        app_url : {
          required: true,
        },
        api_key: {
          required: true,
        },
        email: {
          required: true,
          email: true
        },
        project_key: {
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
        email: {
          required: "Email is required",
          email: "The email should be in the format: abc@domain.tld"
        },
        project_key: {
          required: "Project Key is required",

        }
      }
    });
  });

  $("#test_jira").click(function(e) {
    console.log("hii")
    e.preventDefault(); // avoid to execute the actual submit of the form.
    
    var form = $("#jira-form");
    var url = '/jira/test_jira/'
    
    $.ajax({
    type: "POST",
    url: url,
    data: form.serialize(), // serializes the form's elements.
    success: function(data)
    {
      $("#jira_success").show();
      $('#jira_submit').prop('disabled', false);
    
    
    },
    error: function(XMLHttpRequest, textStatus, errorThrown) {
      $("#jira_failed").show();
    
    }
    });
    
    
    });
    
    $("#jira_submit").click(function(e) {
    console.log("hii")
    e.preventDefault(); // avoid to execute the actual submit of the form.
    
    var form = $("#jira-form");
    var url = '/jira/jira_register/'
    
    $.ajax({
    type: "POST",
    url: url,
    data: form.serialize(), // serializes the form's elements.
    success: function(data)
    {
      $("#ssc_config").show();
      $("#jira_config").hide();

    },
    error: function(XMLHttpRequest, textStatus, errorThrown) {
    }
    });
    
    
    });