$('#login_form').submit(() => {
    if(!$('#inputEmail').val() || !$('#inputPassword').val()) alert('Enter your ID or password');
})