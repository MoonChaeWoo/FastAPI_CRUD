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

    let formData = $('#register_form').serialize();

    $.post('/register', formData, (result)=>{
        document.body.innerHTML = '';      
        document.write(result);
        alert('You have registered as a member!');
    }).fail(function(request, status, error) {
        if(request.status == 400){
            $('.register_error_message').text('Email already registered');
        }else{
            $('.register_error_message').text('There is a problem and registration is not possible. Contact your manager.');
        }
    });
})

