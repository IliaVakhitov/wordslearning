
$(document).ready(function() {
    current_round();
});

function update_progress(new_value) {
    var progress_bar = document.getElementById('progress_bar');
    var width = parseInt(progress_bar.getAttribute('aria-valuenow'));
    var id = setInterval(frame, 100);
    function frame() {
        if (width < new_value) {
            width++;
            progress_bar.style.width = width + '%';
            progress_bar.innerHTML = width + '%';
            progress_bar.setAttribute('aria-valuenow', width)
        }
    }
}

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
        update_progress(response.progress)
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
        window.location.href = response.redirect
        return;
    }

    if (response.hasOwnProperty('value')) {
        document.getElementById('value').innerHTML = response.value;
        if (response.hasOwnProperty('answers')) {
            for (i=0; i<4; i++){
                document.getElementById('answer'.concat(i)).value = response.answers[i];
                document.getElementById('answer'.concat(i)).disabled = '';
                $('#answer'.concat(i)).css('background-color', '');
            }
        }
    }
    document.getElementById('button_next').disabled = 'disabled';
}