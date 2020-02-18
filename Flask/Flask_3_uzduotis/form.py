from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class MessageForm(FlaskForm):
    fname = StringField('Vardas', [DataRequired()])
    lname = StringField('Pavardė', [DataRequired()])
    comment = TextAreaField('Komentaras')
    submit = SubmitField('Pasirašyti')