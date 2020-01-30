$(document).ready(function(){
    // Hide displayed paragraphs
        $("#success").hide();
        $("#failed").hide();
        $('#ssc_submit').prop('disabled', true);
   
    
});





$("#test_ssc").click(function(e) {
    $("#success").hide();
    $("#failed").hide();
    $('#ssc_submit').prop('disabled', true);
   
    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $("#ssc-form");
    var url = '/ssc_connector/test_data/'

    $.ajax({
           type: "POST",
           url: url,
           data: form.serialize(), // serializes the form's elements.
           success: function(data)
           {
            $("#success").show();// show response from the php script.
            $('#ssc_submit').prop('disabled', false);
           },
           error: function(XMLHttpRequest, textStatus, errorThrown) {
            $("#failed").show();
            $('#ssc_submit').prop('disabled', true);
         }
         });


});