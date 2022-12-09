var $login_form = $('#login_form');

$login_form.submit((evt) => {
    evt.preventDefault();
    if(!$('#inputEmail').val() || !$('#inputPassword').val()){
        alert('Enter your ID or password');   
        return;
    };

    let formData = $login_form.serialize();

    $.post('/login/', formData, (result)=>{
        document.body.innerHTML = ''; 
        document.write(result);
    }).fail(function(request, status, error) {
        if(request.status == 400){
            $('.login_error_message').text('Please confirm your email or password');
        }else{
            $('.login_error_message').text('There is a problem and login is not possible. Contact your manager.');
        }
    });
});