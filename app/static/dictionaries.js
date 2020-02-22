
function showFunction() {
    var edit_block = document.getElementById('edit_block');
    var btn = document.getElementById('btn_edit');
    if (edit_block.style.display === "none") {
        edit_block.style.display = "block";
        btn.style.display = "none";
    } else {
        edit_block.style.display = "none";
        btn.style.display = "inline";
    }
}

function hide_popover(){
    $('#dictionary_name').popover('hide');
}

function check_new_dictionary_name() {
    $.post('/check_dictionary_name', {dictionary_name: document.getElementById('dictionary_name').value}
    ).done(function(response) {
        if (response.name_available) {
             document.getElementById("new_dictionary").submit();
        } else {
            $('#dictionary_name').popover('show');
        }
    }).fail(function() {
        //
    });
}
