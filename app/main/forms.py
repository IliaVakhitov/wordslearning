from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from app.models import Dictionary
from flask import flash


class EditDictionaryForm(FlaskForm):
    dictionary_name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    submit = SubmitField('Save')

    def __init__(self, original_dictionary_name, original_description, *args, **kwargs):
        super(EditDictionaryForm, self).__init__(*args, **kwargs)
        self.original_dictionary_name = original_dictionary_name
        self.original_description = original_description

    def validate_dictionary_name(self, dictionary_name):
        if dictionary_name.data != self.original_dictionary_name:
            dictionary = Dictionary.query.filter_by(dictionary_name=self.dictionary_name.data).first()
            if dictionary is not None:
                flash('Please use a different name!')
                raise ValidationError('Please use a different name!')


class EditWordForm(FlaskForm):
    spelling = StringField('Spelling', validators=[DataRequired()])
    definition = StringField('Definition', validators=[DataRequired()])
    submit = SubmitField('Save')

    def __init__(self, original_spelling, original_definition, *args, **kwargs):
        super(EditWordForm, self).__init__(*args, **kwargs)
        self.original_spelling = original_spelling
        self.original_definition = original_definition

