from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import (
    LoginManager, UserMixin, current_user, 
    logout_user, login_user, login_required
)

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from flask_bcrypt import Bcrypt


import os
from datetime import datetime

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
key = 'blablablaverysecure'

app.config['SECRET_KEY'] = key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

bcrypt = Bcrypt(app)

###################################### Models ###################################################


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column("user_name", db.String(50), unique=True, nullable=False)
    email = db.Column("email", db.String(120), unique=True, nullable=False)
    password = db.Column("password", db.String(60), unique=True, nullable=False)
    notes = db.relationship("Note", back_populates='user')

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    body = db.Column('body', db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates='notes')

###################################### Forms ####################################################


class SignUpForm(FlaskForm):
    name = StringField('Name', [DataRequired()])
    email = StringField('Email', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    repeat_password = PasswordField('Repeat Password', [EqualTo('password', "Passwords must match")])
    submit = SubmitField('Sign in')

    def check_name_unique(self, name):
        user = User.query.filter_by(name=name.data).first()
        if user:
            raise ValidationError("Username taken!")

    def check_email_unique(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Username taken!")


class LogInForm(FlaskForm):
    email = StringField('Email', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField('Login')


class NoteForm(FlaskForm):
    body = TextAreaField('Note', [DataRequired()])
    submit = SubmitField('Submit')

###################################### Routes ###################################################

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignUpForm()
    if form.validate_on_submit():
        encrypted_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data, password=encrypted_password)
        db.session.add(user)
        db.session.commit()
        flash('Registration complete! You can sign up now!', 'info')
        return redirect(url_for('home'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        print('is_auth!!!!')
        return redirect(url_for('home'))
    form = LogInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Wrong email/password!", 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    form = NoteForm()
    if form.validate_on_submit():
        note = Note(
            body=form.body.data,
            user=current_user
            )
        db.session.add(note)
        db.session.commit()
    return render_template("notes.html", form=form)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)

