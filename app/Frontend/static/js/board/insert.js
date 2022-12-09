var $contentForm = $('#contentForm')

$contentForm.submit((evt) => {
    evt.preventDefault();

    if(!$('#board_title').val() || !$('#board_content').val()){
        alert('Please write title or content')
        return;
    }

    let formData = $contentForm.serialize();

    console.log('formData', formData);
});