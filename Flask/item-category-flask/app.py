from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

from flask_wtf import FlaskForm
from wtforms import (
    StringField, 
    SubmitField, 
    )
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
key = 'blablablaverysecure'

app.config['SECRET_KEY'] = key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)


class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100)) 
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    category = db.relationship("Category")

    def __init__(self, name, category_id):
        self.name = name
        self.category_id = category_id

    def __repr__(self):
        return f'Item({self.name})'


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'Category({self.name})'

def category_query():
    return Category.query


class ItemForm(FlaskForm):
    name = StringField('Item', [DataRequired()])
    category = QuerySelectField(
        query_factory=category_query,
        allow_blank=False,
        get_label='name', # <<<<<<<<<<<------------------VAAAAAAĄĄĄ!!!
        get_pk=lambda x: str(x)
    )
    submit = SubmitField('Submit')


class CategoryForm(FlaskForm):
    name = StringField('Name', [DataRequired()])
    submit = SubmitField('Submit')


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/items', methods=['GET', 'POST'])
def items():
    all_items = Item.query.all()
    form = ItemForm()
    if form.validate_on_submit():
        new_item = Item(
            name=form.name.data,
            category_id=form.category.data.id
        )
        db.session.add(new_item)
        db.session.commit()
        all_items = Item.query.all()
        return render_template('item.html', form=form, items=all_items)
    return render_template('item.html', form=form, items=all_items)

@app.route('/categories', methods=['GET', 'POST'])
def contacts():
    all_categories = Category.query.all()
    form = CategoryForm()
    if form.validate_on_submit():
        new_category = Category(name=form.name.data)
        db.session.add(new_category)
        db.session.commit()
        all_categories = Category.query.all()
        return render_template('category.html', form=form, cats=all_categories)
    return render_template('category.html', form=form, cats = all_categories)

@app.route('/delete_item/<int:id>')
def delete(id):
    item = Item.query.get(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('items'))

@app.route('/update_item/<int:id>', methods=['GET', 'POST'])
def update_item(id):
    item = Item.query.get(id)
    form = ItemForm()
    if form.validate_on_submit():
        item.name = form.name.data
        item.category_id = form.category.data.id
        db.session.commit()
        return redirect(url_for('items'))
    return render_template('update_item.html', form=form)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)



