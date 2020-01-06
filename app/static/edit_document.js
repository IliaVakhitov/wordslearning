
function show_confirmation() {
    var delete_block = document.getElementById('delete_block');
    var buttons_block = document.getElementById('buttons_block');
    var dict_block = document.getElementById('dictionary_name_description');
    var words_block = document.getElementById('words_block');
    if (delete_block.style.display === "none") {
        delete_block.style.display = "block";
        buttons_block.style.display = "none";
        dict_block.style.display = "none";
        words_block.style.display = "none";
    } else {
        delete_block.style.display = "none";
        buttons_block.style.display = "inline";
        dict_block.style.display = "block";
        words_block.style.display = "block";
    }
}

function add_word(word_id) {
    var words_table = document.getElementById('words_table_body');
    var new_word_spelling = document.getElementById('new_word_spelling');
    var new_word_definition = document.getElementById('new_word_definition');
    var tr = document.createElement('tr');
    var td_spelling = document.createElement('td');
    var td_definition = document.createElement('td');
    var td_button_delete = document.createElement('td');

    input_value = document.createElement('input');
    input_value.setAttribute('id', 'word_spelling_'.concat(word_id));
    input_value.setAttribute('value', new_word_spelling.value);
    input_value.setAttribute('size', 25);
    input_value.setAttribute('onchange', 'save_word(word_id)'.replace('word_id', word_id));
    td_spelling.appendChild(input_value);

    input_definition = document.createElement('input');
    input_definition.setAttribute('id', 'word_definition_'.concat(word_id));
    input_definition.setAttribute('value', new_word_definition.value);
    input_definition.setAttribute('size', 35);
    input_definition.setAttribute('onchange', 'save_word(word_id)'.replace('word_id', word_id));
    td_definition.appendChild(input_definition);

    button_delete = document.createElement('button');
    button_delete.setAttribute('id', 'button_delete_'.concat(word_id));
    button_delete.appendChild(document.createTextNode('X'));
    button_delete.setAttribute('class', 'btn btn-danger');
    button_delete.setAttribute('onclick', 'delete_word(word_id);'.replace('word_id', word_id))
    td_button_delete.appendChild(button_delete);

    tr.setAttribute('id', 'word_'.concat(word_id));
    tr.appendChild(td_spelling);
    tr.appendChild(td_definition);
    tr.appendChild(td_button_delete);

    words_table.appendChild(tr);
}

function delete_word(word_id) {

    $.post('/delete_word', {
        word_id: word_id
    }).done(function(response) {
        document.getElementById('word_'.concat(word_id)).remove();
    }).fail(function() {
        // TODO
        alert('Bad');
    });
}

function add_new_word() {
    var spelling = document.getElementById('new_word_spelling').value.trim();
    var definition = document.getElementById('new_word_definition').value.trim();
    var dictionary_id = document.getElementById('dictionary_id').innerHTML;
    if (spelling == "") {
        spelling_msg = document.getElementById('spelling').innerHTML = "Please, fill this field!";
        return
    }
    if (definition == "") {
        definition_msg = document.getElementById('definition_msg').innerHTML = "Please, fill this field!";
        return
    }
    $.post('/add_word', {
        spelling: spelling,
        definition: definition,
        dictionary_id: dictionary_id
    }).done(function(response) {
        add_word(response['new_word_id'])
    }).fail(function() {
        // TODO
        alert('Bad');
    });
}

function save_word(word_id) {
    var spelling = document.getElementById('word_spelling_'.concat(word_id)).value.trim();
    var definition = document.getElementById('word_definition_'.concat(word_id)).value.trim();

    $.post('/save_word', {
        spelling: spelling,
        definition: definition,
        word_id: word_id
    }).done(function(response) {

    }).fail(function() {
        // TODO
        alert('Bad');
    });

}
