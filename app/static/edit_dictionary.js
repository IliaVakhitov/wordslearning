
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
    var new_word_spelling = document.getElementById('word_spelling_0');
    var new_word_definition = document.getElementById('word_definition_0');
    var tr = document.createElement('tr');
    var td_spelling = document.createElement('td');
    var td_definition = document.createElement('td');
    var td_button_delete = document.createElement('td');

    input_value = document.createElement('input');
    input_value.setAttribute('id', 'word_spelling_'.concat(word_id));
    input_value.setAttribute('value', new_word_spelling.value);
    //input_value.setAttribute('size', 25);
    input_value.setAttribute('class', 'form-control form-control');
    input_value.setAttribute('required', '');
    input_value.setAttribute('placeholder', 'Enter word or phrase');
    input_value.setAttribute('onchange', 'save_word(word_id)'.replace('word_id', word_id));
    td_spelling.appendChild(input_value);

    input_definition = document.createElement('input');
    input_definition.setAttribute('id', 'word_definition_'.concat(word_id));
    input_definition.setAttribute('value', new_word_definition.value);
    //input_definition.setAttribute('size', 35);
    input_definition.setAttribute('class', 'form-control form-control');
    input_definition.setAttribute('required', '');
    input_definition.setAttribute('placeholder', 'Enter definition');
    input_definition.setAttribute('onchange', 'save_word(word_id)'.replace('word_id', word_id));
    td_definition.appendChild(input_definition);

    button_delete = document.createElement('button');
    button_delete.setAttribute('id', 'button_delete_'.concat(word_id));
    button_delete.appendChild(document.createTextNode('X'));
    button_delete.setAttribute('class', 'btn btn-outline-danger btn');
    button_delete.setAttribute('onclick', 'delete_word(word_id);'.replace('word_id', word_id))
    td_button_delete.appendChild(button_delete);

    tr.setAttribute('id', 'word_'.concat(word_id));
    tr.appendChild(td_spelling);
    tr.appendChild(td_definition);
    tr.appendChild(td_button_delete);

    words_table.appendChild(tr);
    new_word_spelling.value = '';
    new_word_definition.value = '';
}

function delete_word(word_id) {
    $.post('/delete_word',
        {word_id: word_id}
    ).done(function(response) {
        hide_popover(word_id);
        document.getElementById('word_'.concat(word_id)).remove();
    });
}

function get_definition(word_id) {
    var spelling = document.getElementById('word_spelling_'.concat(word_id)).value.trim();
    // TODO add spinner
    $.post('/get_definition',
        {spelling: spelling,
        word_id: word_id}
    ).done(function(response) {
        if (response.hasOwnProperty('error')) {
            return;
        }
        if (response.hasOwnProperty('definitions') && response.definitions.length > 0) {
            document.getElementById('dropdown_button_'.concat(word_id)).style.display = "inline";
            var list = document.getElementById('dropdown_definitions_'.concat(word_id));
            var length = list.children.length;
            for (i=length-1; i>-1; i--) {
                list.removeChild(list.children[i]);
            }
            for (online_definition in response.definitions) {
                result = response.definitions[online_definition].definition;
                result = result.charAt(0).toUpperCase() + result.slice(1);

                var link = document.createElement("a");
                var text = document.createTextNode(result);
                link.appendChild(text);
                link.setAttribute('class', 'dropdown-item');
                link.setAttribute('href', '#');
                var function_call = 'select_definition(word_id, text)'.replace('text', '\''+result+'\'');
                function_call = function_call.replace('word_id', word_id)
                link.setAttribute('onclick', function_call);
                list.appendChild(link);
            }
        }
    });
}

function show_get_buttons(word_id, value) {
    document.getElementById('group_definition_'.concat(word_id)).style.display = 'inline';
}

function select_definition(word_id, text) {
    document.getElementById('word_definition_'.concat(word_id)).value = text;
    if (word_id != 0) {
        save_word(word_id);
    }
}

function add_new_word() {
    var spelling = document.getElementById('word_spelling_0').value.trim();
    var definition = document.getElementById('word_definition_0').value.trim();
    var dictionary_id = document.getElementById('dictionary_id').innerHTML;
    if (spelling == "") {
        $('#word_spelling_0').popover('show');
        return;
    }
    if (definition == "") {
        $('#word_definition_0').popover('show');
        return;
    }
    $.post('/add_word', {
        spelling: spelling,
        definition: definition,
        dictionary_id: dictionary_id
    }).done(function(response) {
        add_word(response['new_word_id']);
        hide_popover(0);
    });
}

function save_word(word_id) {
    var spelling = document.getElementById('word_spelling_'.concat(word_id)).value.trim();
    var definition = document.getElementById('word_definition_'.concat(word_id)).value.trim();
    if (spelling == "") {
        $('#word_spelling_'.concat(word_id)).popover('show');
        return;
    }
    if (definition == "") {
        $('#word_definition_'.concat(word_id)).popover('show');
        return;
    }
    $.post('/save_word', {
        spelling: spelling,
        definition: definition,
        word_id: word_id
    }).done(function(response) {
        document.getElementById('group_definition_'.concat(word_id)).style.display = 'none';
        hide_popover(word_id);
    });
}

function hide_popover(word_id) {
    $('#word_spelling_'.concat(word_id)).popover('hide');
    $('#word_definition_'.concat(word_id)).popover('hide');
}

//TODO Add get buttons to new word