
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