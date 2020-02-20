$('select_dictionaries').selectpicker();

$(function () {
    $("#game_rounds")
        .popover({ content: "Please, select value more than 3!" })
        .blur(function () {
            $(this).popover('hide');
        });
});

function check_game_rounds() {
    current_value = document.getElementById('game_rounds').value;
    if (current_value < 4){
        document.getElementById('game_rounds').value = 4;
    }
};

