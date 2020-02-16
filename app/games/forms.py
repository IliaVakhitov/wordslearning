from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class GameParametersForm(FlaskForm):
    game_type = StringField('Game type', validators=[DataRequired()])
    game_rounds = IntegerField('Game rounds', validators=[DataRequired()])
    submit = SubmitField('Start')
