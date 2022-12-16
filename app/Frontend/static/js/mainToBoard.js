var $mainToBoard = $('#mainToBoard')
// href="/board"
$mainToBoard.click((evt) => {
    evt.preventDefault();

    $.get('/board', {}, () => {
        window.location.href = '/board'
    }).fail(function(request, status, error) {
        console.log('error', request.status);
        if(request.status == 401){
            alert('Please log in');
            window.location.href = '/login'
            return;
        }else if(request.status == 403){
            alert('Please register as a member');
            window.location.href = '/register'
            return;
        }else if(request.status == 500){
            alert('Please log in again');
            window.location.href = '/login'
            return;
        }else{
            alert('please contact the manager');
            return;
        }
    });
})