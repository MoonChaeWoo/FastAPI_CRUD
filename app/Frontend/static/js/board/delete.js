$deleteBtn = $('.deleteBtn');

$deleteBtn.click(function(){
    let answer = confirm("Are you sure you want to do this?");

    if(answer){
        $.post('/board/delete', {'id' : $(this).data('id')}, (result) => {
            alert("success delete!")
        }).fail(function(request, status, error){
            alert("fail delete")
        })
    }else{

    }
});