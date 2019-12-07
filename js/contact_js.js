$(function() {
  $("form[name='contact']").validate({
    // Specify validation rules
    rules: {
      name: {
        required: true,
        minlength: 2
      },
      email: {
        required: true,
        email: true
      },
      msg: {
        required: true,
        minlength: 5
      }
    },
    // Specify validation error messages
    messages: {
      name: "Please enter your full name",
      email: "Please enter a valid email address",
      msg: "Please enter a message over 5 characters"
    },
    // Make sure the form is submitted to the destination defined
    // in the "action" attribute of the form when valid
     submitHandler: function(form) {
    
    $.ajax({
      url: "//formspree.io/kvenuti@gmail.com",
      method: "POST",
      data: $(form).serialize(),
      dataType: "json",
      success: function(data) {
          $("form#contact :input").prop("disabled", true);
         
      },
      error: function(){
        console.log('error sending data');
      }
    });
    return false;
  }
  });
});