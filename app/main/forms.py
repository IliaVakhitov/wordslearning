from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class EditDictionaryForm(FlaskForm):
    dictionary_name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Save')

    def __init__(self, original_dictionary_name, *args, **kwargs):
        super(EditDictionaryForm, self).__init__(*args, **kwargs)
        self.original_dictionary_name = original_dictionary_name


class EditWordForm(FlaskForm):
    spelling = StringField('Spelling', validators=[DataRequired()])
    definition = StringField('Definition', validators=[DataRequired()])
    submit = SubmitField('Save')

    def __init__(self, original_spelling, original_definition, *args, **kwargs):
        super(EditWordForm, self).__init__(*args, **kwargs)
        self.original_spelling = original_spelling
        self.original_definition = original_definition

