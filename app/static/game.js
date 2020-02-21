// TODO add progress bar
$(document).ready(function() {
    current_round();
});

function current_round() {
    $.post('/current_round'
    ).done(function(response) {
        set_round(response);
    }).fail(function() {
        //$.get('/game_statistic');
    });
}

function next_round() {
    $.post('/next_round'
    ).done(function(response) {
        set_round(response);
    }).fail(function() {
        //$.get('/game_statistic');
    });
}

function check_answer(answer_index) {
    $.post('/get_correct_index',{answer_index: answer_index}
    ).done(function(response) {
        set_answer(parseInt(response.correct_index), answer_index);
    }).fail(function() {
        //$.get('/game_statistic');
    });
}

function set_answer(correct_index, answer_index) {
    if (correct_index != answer_index){
       $('#answer'.concat(answer_index)).css('background-color', '#ef0000');;
    }
    $('#answer'.concat(correct_index)).css('background-color', '#0cc908');
    for (i=0; i<4; i++){
        document.getElementById('answer'.concat(i)).disabled = 'disabled';
    }
    document.getElementById('button_next').disabled = '';
}

function set_round(response) {
    if (response.hasOwnProperty('redirect')) {
        window.location.href = response.redirect;
        return;
    }

    if (response.hasOwnProperty('value')) {
        document.getElementById('value').innerHTML = response['value'];
        if (response.hasOwnProperty('answers')) {
            for (i=0; i<4; i++){
                document.getElementById('answer'.concat(i)).value = response['answers'][i];
                document.getElementById('answer'.concat(i)).disabled = '';
                $('#answer'.concat(i)).css('background-color', '');
            }
        }
    }
    document.getElementById('button_next').disabled = 'disabled';
}