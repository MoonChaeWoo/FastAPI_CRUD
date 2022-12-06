$('#register_form').submit((evt) => {
    evt.preventDefault();

    $inputName = $('#inputName').val()
    $inputEmail = $('#inputEmail').val()
    $inputPassword = $('#inputPassword').val();
    $inputPasswordConfirm = $('#inputPasswordConfirm').val();

    if(!$inputName || !$inputEmail || !$inputPassword || !$inputPasswordConfirm){
        alert('Please enter your information completely')
        return;
    };

    if($inputPassword != $inputPasswordConfirm){
        alert('Recheck your password')
        return;
    };

    let formData = {
        "name": $inputName,
        "email": $inputEmail,
        "password": $inputPassword
      }

    $.ajax({
        type : "post",
        contentType: "application/json",
        data : JSON.stringify(formData),
        success : function(result) {
            document.write(result);
        }
    });
})

