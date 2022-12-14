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
            return;
        }else if(request.status == 403){
            alert('Please register as a member');
            return;
        }else if(request.status == 500){
            alert('Please log in again');
            return;
        }else{
            alert('please contact the manager');
            return;
        }
    });
})