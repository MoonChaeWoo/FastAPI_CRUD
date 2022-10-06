$('#contentForm').on('submit', function(evt){
    evt.preventDefault();

    var formData = new FormData(this);

    $.ajax({
        type : 'POST',
        enctype : 'multipart/form-data',
        url : '/test',
        data : formData,
        processData : false,
        contentType : false,
        cache : false,
        success : function(result){

        },
        error : function(){
            
        }
    });
});