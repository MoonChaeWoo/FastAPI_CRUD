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
        alert("You have become a member.");
        document.write(result);
    });
})

