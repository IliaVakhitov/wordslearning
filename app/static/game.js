
$(document).ready(function() {
    next_round();
});

function next_round() {
    $.post('/next_round'
    ).done(function(response) {
        set_next_round(response);
    }).fail(function() {
        //$.get('/game_statistic');
    });
}

function set_next_round(response) {


    if (response.hasOwnProperty('redirect')) {
        window.location.href = response.redirect;
        return;
    }
    if (response.hasOwnProperty('value')) {
        document.getElementById('value').innerHTML = response['value'];
        if (response.hasOwnProperty('answers')) {
            for (i=0; i<4; i++){
                document.getElementById('answer'.concat(i)).value = response['answers'][i];
            }
        }
    }
}