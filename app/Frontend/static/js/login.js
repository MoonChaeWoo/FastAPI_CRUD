$('#login_form').submit((evt) => {
    evt.preventDefault();
    if(!$('#inputEmail').val() || !$('#inputPassword').val()){
        alert('Enter your ID or password');   
        return;
    };

    let formData = $('#login_form').serialize();

    $.post('/login/', formData, (result)=>{
        document.write(result);
    });
})