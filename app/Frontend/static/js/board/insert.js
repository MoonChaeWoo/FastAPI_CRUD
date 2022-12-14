var $contentForm = $('#contentForm')
var $boardTitle = $('#board_title')
var $boardContent = $('#board_content')

$contentForm.submit((evt) => {
    evt.preventDefault();

    if(!$boardTitle.val() || !$boardContent.val()){
        alert('Please write title or content')
        return;
    }

    let formData = new FormData();

    formData.append('title', $boardTitle.val());
    formData.append('description', $boardContent.val());
    formData.append('uploadFile', $('#board_file')[0].files[0]);


    $.ajax({
        type : 'post',
        url : '/board/write',
        data : formData,
        processData : false,
        contentType : false,
        success : function(result){
            alert('success!')
        },
    });

    // processData  : false
    // -> 서버로 보내지는 data는 "application/x-www-from-urlencoded"에
    // 맞는 쿼리 문자열로 처리 및 변환된 형태이다.
    // DOMDocument 또는 기타 처리되지 않은 데이터(파일) 을 보낼 땐 이 옵션값을 false로 지정해야한다.

    // contnentType : false
    // -> default 값 : : "application/x-www-form-urlencoded; charset=UTF-8"
    // -> "multipart/form-data" 로 전송이 되게 옵션값을 false로 지정 
});