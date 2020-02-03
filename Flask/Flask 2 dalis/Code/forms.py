from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email, InputRequired


class ContactForm(FlaskForm):
    
    name = StringField('Vardas', [DataRequired()])
    email = StringField('El.paštas', validators=[Email(message=('Neteisingas adresas.')), 
                                        DataRequired()])
    body = TextAreaField('Jūsų pranešimas', validators=[DataRequired(), 
                                        Length(min=10, 
                                        message=('Per trumpas tekstas.'))])
    submit = SubmitField('Submit')
